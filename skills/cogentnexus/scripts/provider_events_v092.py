#!/usr/bin/env python3
"""Provider event stream adapter for CogentNexus v0.9.2.

Events are evidence, not recovery policy. The adapter intentionally treats
prompt-progress observations as suppression-only proof of life. A parser bug can
therefore delay destructive recovery but can never authorize it.

LM Studio exposes runtime progress through `lms log stream --source runtime`.
This module consumes that blocking stream without polling and persists the latest
provider event. If the stream ends and the provider is actually unreachable, it
publishes `provider_dead` and wakes the Host immediately; periodic supervisor
reconciliation remains a safety fallback.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import signal
import subprocess
import sys
import time
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import provider

SCHEMA_VERSION = 1
PROGRESS_RE = re.compile(
    r"(?i)(?:prompt[^\n]{0,80}?(?:process|processing|eval|prefill)[^\n]{0,80}?)(\d+(?:\.\d+)?)\s*%"
)
GENERATION_RE = re.compile(r"(?i)(?:first\s+token|generation\s+(?:started|start)|decode\s+(?:started|start))")


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def state_path(root: Path) -> Path:
    return root / "host" / "provider-events-v092.json"


def pid_path(root: Path, provider_name: str) -> Path:
    return root / "host" / f"provider-events-{provider_name}.pid"


def lock_path(root: Path) -> Path:
    return root / "host" / ".provider-events-v092.lock"


@contextmanager
def _lock(root: Path, timeout: float = 5.0):
    path = lock_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    deadline = time.monotonic() + timeout
    while True:
        try:
            fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(fd, str(os.getpid()).encode())
            os.close(fd)
            break
        except FileExistsError:
            try:
                if time.time() - path.stat().st_mtime > 60:
                    path.unlink()
                    continue
            except FileNotFoundError:
                continue
            if time.monotonic() >= deadline:
                raise TimeoutError(f"provider event lock timeout: {path}")
            time.sleep(0.025)
    try:
        yield
    finally:
        path.unlink(missing_ok=True)


def _blank() -> dict[str, Any]:
    return {"schemaVersion": SCHEMA_VERSION, "sequence": 0, "providers": {}}


def load_state(root: Path) -> dict[str, Any]:
    path = state_path(root)
    if not path.exists():
        return _blank()
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return _blank()
    if not isinstance(value, dict) or value.get("schemaVersion") != SCHEMA_VERSION:
        return _blank()
    value.setdefault("sequence", 0)
    value.setdefault("providers", {})
    return value


def _atomic(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def publish(root: Path, provider_name: str, event_type: str, evidence: Any = None) -> dict[str, Any]:
    provider_name = provider.normalize_provider(provider_name)
    with _lock(root):
        state = load_state(root)
        sequence = int(state.get("sequence", 0)) + 1
        state["sequence"] = sequence
        stamp = now_iso()
        event = {
            "sequence": sequence,
            "provider": provider_name,
            "type": str(event_type),
            "at": stamp,
            "evidence": evidence if evidence is not None else {},
        }
        providers_state = state.setdefault("providers", {})
        value = providers_state.get(provider_name)
        if not isinstance(value, dict):
            value = {"consumedFailureSequence": 0}
            providers_state[provider_name] = value
        value["lastEvent"] = event
        if event_type == "prompt_progress":
            value["lastProgress"] = event
        if event_type in {"provider_dead", "provider_unreachable", "provider_connection_refused"}:
            value["lastFailure"] = event
        if event_type in {"provider_ready", "model_completed", "stable_success"}:
            value["lastSuccess"] = event
        state["updatedAt"] = stamp
        _atomic(state_path(root), state)
        return event


def latest_progress(root: Path, provider_name: str) -> dict[str, Any] | None:
    provider_name = provider.normalize_provider(provider_name)
    state = load_state(root)
    providers_state = state.get("providers") if isinstance(state.get("providers"), dict) else {}
    value = providers_state.get(provider_name) if isinstance(providers_state.get(provider_name), dict) else {}
    event = value.get("lastProgress") if isinstance(value, dict) else None
    return event if isinstance(event, dict) else None


def consume_failure(root: Path, provider_name: str) -> dict[str, Any] | None:
    """Consume each destructive failure event at most once."""
    provider_name = provider.normalize_provider(provider_name)
    with _lock(root):
        state = load_state(root)
        providers_state = state.get("providers") if isinstance(state.get("providers"), dict) else {}
        value = providers_state.get(provider_name) if isinstance(providers_state.get(provider_name), dict) else {}
        failure = value.get("lastFailure") if isinstance(value, dict) else None
        if not isinstance(failure, dict):
            return None
        sequence = int(failure.get("sequence", 0) or 0)
        consumed = int(value.get("consumedFailureSequence", 0) or 0)
        if sequence <= consumed:
            return None
        value["consumedFailureSequence"] = sequence
        state["updatedAt"] = now_iso()
        _atomic(state_path(root), state)
        return failure


def parse_runtime_line(line: str) -> tuple[str, dict[str, Any]] | None:
    text = (line or "").strip()
    if not text:
        return None
    progress = PROGRESS_RE.search(text)
    if progress:
        try:
            percent = max(0.0, min(100.0, float(progress.group(1))))
        except ValueError:
            percent = None
        return "prompt_progress", {"percent": percent, "line": text[-1000:]}
    if GENERATION_RE.search(text):
        return "generation_started", {"line": text[-1000:]}
    return None


def _pid_alive(pid: int) -> bool:
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def adapter_status(root: Path, provider_name: str) -> dict[str, Any]:
    provider_name = provider.normalize_provider(provider_name)
    path = pid_path(root, provider_name)
    try:
        pid = int(path.read_text(encoding="utf-8").strip())
    except Exception:
        return {"provider": provider_name, "running": False, "pid": None}
    alive = _pid_alive(pid)
    if not alive:
        path.unlink(missing_ok=True)
    return {"provider": provider_name, "running": alive, "pid": pid if alive else None}


def stop_adapter(root: Path, provider_name: str | None = None) -> dict[str, Any]:
    names = [provider.normalize_provider(provider_name)] if provider_name else list(provider.SUPPORTED_PROVIDERS)
    stopped = []
    for name in names:
        status = adapter_status(root, name)
        pid = status.get("pid")
        if isinstance(pid, int):
            try:
                os.kill(pid, signal.SIGTERM)
                stopped.append({"provider": name, "pid": pid, "stopped": True})
            except OSError as error:
                stopped.append({"provider": name, "pid": pid, "stopped": False, "error": str(error)})
        pid_path(root, name).unlink(missing_ok=True)
    return {"stopped": stopped}


def _background_python() -> str:
    executable = Path(sys.executable)
    pythonw = executable.with_name("pythonw.exe")
    return str(pythonw) if os.name == "nt" and pythonw.exists() else str(executable)


def ensure_adapter(root: Path, provider_name: str) -> dict[str, Any]:
    provider_name = provider.normalize_provider(provider_name)
    if provider_name != "lmstudio":
        stop_adapter(root, "lmstudio")
        return {"provider": provider_name, "supported": False, "running": False, "reason": "no provider progress stream adapter required"}
    current = adapter_status(root, provider_name)
    if current.get("running"):
        return {**current, "supported": True, "started": False}
    cli = provider.find_lms_cli()
    if not cli:
        return {"provider": provider_name, "supported": True, "running": False, "error": "LM Studio lms CLI unavailable"}
    command = [
        _background_python(),
        str(Path(__file__).resolve()),
        "--root", str(root.resolve()),
        "daemon", "--provider", provider_name,
    ]
    kwargs: dict[str, Any] = {"stdin": subprocess.DEVNULL, "stdout": subprocess.DEVNULL, "stderr": subprocess.DEVNULL}
    if os.name == "nt":
        kwargs["creationflags"] = getattr(subprocess, "CREATE_NO_WINDOW", 0) | getattr(subprocess, "DETACHED_PROCESS", 0)
    else:
        kwargs["start_new_session"] = True
    proc = subprocess.Popen(command, **kwargs)
    return {"provider": provider_name, "supported": True, "running": True, "started": True, "pid": proc.pid, "command": command}


def select_provider(root: Path, provider_name: str) -> dict[str, Any]:
    stop_adapter(root)
    return ensure_adapter(root, provider_name)


def _wake_host(root: Path) -> dict[str, Any]:
    host = Path(__file__).resolve().with_name("host_control_v092.py")
    try:
        proc = subprocess.Popen(
            [sys.executable, str(host), "--root", str(root.resolve()), "supervisor", "tick", "--execute-safe"],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            **({"creationflags": getattr(subprocess, "CREATE_NO_WINDOW", 0)} if os.name == "nt" else {"start_new_session": True}),
        )
        return {"started": True, "pid": proc.pid}
    except Exception as error:
        return {"started": False, "error": str(error)}


def run_lmstudio_daemon(root: Path) -> int:
    cli = provider.find_lms_cli()
    if not cli:
        publish(root, "lmstudio", "adapter_error", {"error": "lms CLI unavailable"})
        return 2
    pid_file = pid_path(root, "lmstudio")
    pid_file.parent.mkdir(parents=True, exist_ok=True)
    pid_file.write_text(str(os.getpid()), encoding="utf-8")
    publish(root, "lmstudio", "adapter_started", {"pid": os.getpid()})
    command = [cli, "log", "stream", "--source", "runtime"]
    try:
        proc = subprocess.Popen(
            command,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            bufsize=1,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0) if os.name == "nt" else 0,
        )
        assert proc.stdout is not None
        for line in proc.stdout:
            parsed = parse_runtime_line(line)
            if parsed is None:
                continue
            event_type, evidence = parsed
            publish(root, "lmstudio", event_type, evidence)
        code = proc.wait()
        health = provider.probe("lmstudio", timeout=3.0)
        if not health.get("healthy"):
            event = publish(root, "lmstudio", "provider_dead", {
                "source": "lmstudio-runtime-stream-ended",
                "streamExitCode": code,
                "providerHealth": health,
            })
            _wake_host(root)
            return 1
        publish(root, "lmstudio", "adapter_disconnected", {
            "streamExitCode": code,
            "providerHealth": health,
        })
        return 0
    except Exception as error:
        health = provider.probe("lmstudio", timeout=3.0)
        event_type = "provider_dead" if not health.get("healthy") else "adapter_error"
        publish(root, "lmstudio", event_type, {"error": str(error), "providerHealth": health})
        if event_type == "provider_dead":
            _wake_host(root)
        return 1
    finally:
        try:
            if pid_file.exists() and pid_file.read_text(encoding="utf-8").strip() == str(os.getpid()):
                pid_file.unlink()
        except Exception:
            pass


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    sub = parser.add_subparsers(dest="command", required=True)
    daemon = sub.add_parser("daemon")
    daemon.add_argument("--provider", required=True)
    status = sub.add_parser("status")
    status.add_argument("--provider", default="lmstudio")
    stop = sub.add_parser("stop")
    stop.add_argument("--provider")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    if args.command == "daemon":
        name = provider.normalize_provider(args.provider)
        if name != "lmstudio":
            return 0
        return run_lmstudio_daemon(root)
    if args.command == "status":
        print(json.dumps(adapter_status(root, args.provider), ensure_ascii=False, indent=2))
        return 0
    if args.command == "stop":
        print(json.dumps(stop_adapter(root, args.provider), ensure_ascii=False, indent=2))
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
