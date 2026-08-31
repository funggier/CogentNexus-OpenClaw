#!/usr/bin/env python3
"""Provider event stream adapter for CogentNexus-OpenClaw v0.9.2.

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
import errno
import json
import os
import re
import shutil
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
ADAPTER_STARTUP_SECONDS = 5.0
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


def ownership_lock_path(root: Path, provider_name: str) -> Path:
    return root / "host" / f"provider-events-{provider_name}.owner.lock"


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


def _prepare_ownership_file(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    handle = open(path, "a+b", buffering=0)
    handle.seek(0, os.SEEK_END)
    if handle.tell() == 0:
        handle.write(b"\0")
    handle.seek(0)
    return handle


def _acquire_ownership(handle, *, nonblocking: bool) -> None:
    handle.seek(0)
    if os.name == "nt":
        import msvcrt

        mode = msvcrt.LK_NBLCK if nonblocking else msvcrt.LK_LOCK
        msvcrt.locking(handle.fileno(), mode, 1)
        return
    import fcntl

    operation = fcntl.LOCK_EX | (fcntl.LOCK_NB if nonblocking else 0)
    fcntl.flock(handle.fileno(), operation)


def _release_ownership(handle) -> None:
    handle.seek(0)
    if os.name == "nt":
        import msvcrt

        msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
        return
    import fcntl

    fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


@contextmanager
def _ownership_lease(root: Path, provider_name: str):
    path = ownership_lock_path(root, provider_name)
    handle = _prepare_ownership_file(path)
    acquired = False
    try:
        _acquire_ownership(handle, nonblocking=True)
        acquired = True
        yield
    finally:
        if acquired:
            try:
                _release_ownership(handle)
            except OSError:
                pass
        handle.close()


def _ownership_state(root: Path, provider_name: str) -> dict[str, Any]:
    """Read ownership without mutating adapter files."""
    path = ownership_lock_path(root, provider_name)
    if not path.exists():
        return {"held": False, "path": str(path)}
    try:
        handle = open(path, "r+b", buffering=0)
    except OSError as error:
        return {"held": None, "path": str(path), "error": str(error)}
    acquired = False
    try:
        try:
            _acquire_ownership(handle, nonblocking=True)
            acquired = True
        except OSError as error:
            if error.errno in {errno.EACCES, errno.EAGAIN, errno.EDEADLK}:
                return {"held": True, "path": str(path)}
            return {"held": None, "path": str(path), "error": str(error)}
        return {"held": False, "path": str(path)}
    finally:
        if acquired:
            try:
                _release_ownership(handle)
            except OSError:
                pass
        handle.close()


def adapter_status(root: Path, provider_name: str) -> dict[str, Any]:
    """Read-only status; never deletes stale pid/lock files."""
    provider_name = provider.normalize_provider(provider_name)
    path = pid_path(root, provider_name)
    observed_pid = None
    try:
        observed_pid = int(path.read_text(encoding="utf-8").strip())
    except Exception:
        pass
    alive = _pid_alive(observed_pid) if isinstance(observed_pid, int) else False
    ownership = _ownership_state(root, provider_name)
    held = ownership.get("held")
    running = bool(alive and held is True)
    degraded = bool((held is True and not alive) or (alive and held is not True) or held is None)
    return {
        "provider": provider_name,
        "running": running,
        "pid": observed_pid if running else None,
        "observedPid": observed_pid,
        "pidAlive": alive,
        "ownershipHeld": held,
        "ownershipPath": ownership.get("path"),
        "ownershipError": ownership.get("error"),
        "degraded": degraded,
    }


def _terminate_process_tree(pid: int) -> dict[str, Any]:
    if os.name == "nt":
        taskkill = shutil.which("taskkill") or shutil.which("taskkill.exe")
        if not taskkill:
            return {"ok": False, "error": "taskkill unavailable"}
        proc = subprocess.run(
            [taskkill, "/PID", str(pid), "/T", "/F"],
            capture_output=True,
            text=True,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        return {
            "ok": proc.returncode == 0,
            "exitCode": proc.returncode,
            "stdout": proc.stdout.strip(),
            "stderr": proc.stderr.strip(),
        }
    try:
        os.killpg(pid, signal.SIGTERM)
        return {"ok": True}
    except ProcessLookupError:
        return {"ok": True, "alreadyStopped": True}
    except OSError as error:
        return {"ok": False, "error": str(error)}


def _cleanup_unowned_files(root: Path, provider_name: str, observed_pid: int | None = None) -> None:
    pid_file = pid_path(root, provider_name)
    try:
        if observed_pid is None:
            pid_file.unlink(missing_ok=True)
        elif pid_file.exists() and pid_file.read_text(encoding="utf-8").strip() == str(observed_pid):
            pid_file.unlink()
    except Exception:
        pass
    ownership = _ownership_state(root, provider_name)
    if ownership.get("held") is False:
        try:
            ownership_lock_path(root, provider_name).unlink(missing_ok=True)
        except Exception:
            pass


def stop_adapter(root: Path, provider_name: str | None = None) -> dict[str, Any]:
    names = [provider.normalize_provider(provider_name)] if provider_name else list(provider.SUPPORTED_PROVIDERS)
    stopped = []
    for name in names:
        status = adapter_status(root, name)
        pid = status.get("pid")
        if isinstance(pid, int):
            result = _terminate_process_tree(pid)
            stopped.append({"provider": name, "pid": pid, "stopped": bool(result.get("ok")), "termination": result})
            if result.get("ok"):
                _cleanup_unowned_files(root, name, pid)
            continue

        observed_pid = status.get("observedPid")
        if status.get("ownershipHeld") is True:
            # Ownership is live but the pid cannot be verified. Never guess a
            # process id for destructive cleanup.
            stopped.append({
                "provider": name,
                "pid": observed_pid,
                "stopped": False,
                "error": "adapter ownership is live but pid identity is unverifiable; refusing process termination",
            })
            continue

        _cleanup_unowned_files(root, name, observed_pid if isinstance(observed_pid, int) else None)
        stopped.append({
            "provider": name,
            "pid": observed_pid,
            "stopped": True,
            "alreadyStopped": True,
            "stalePidSuppressed": isinstance(observed_pid, int),
        })
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
    if current.get("ownershipHeld") is True:
        return {
            **current,
            "supported": True,
            "started": False,
            "error": "provider event adapter ownership is live but pid is unverifiable; refusing duplicate adapter start",
        }
    _cleanup_unowned_files(
        root,
        provider_name,
        current.get("observedPid") if isinstance(current.get("observedPid"), int) else None,
    )

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

    # This short loop is startup synchronization only; it is not a recovery
    # timer. The daemon writes its PID only after acquiring the OS ownership lock.
    deadline = time.monotonic() + ADAPTER_STARTUP_SECONDS
    last = adapter_status(root, provider_name)
    while time.monotonic() < deadline:
        if last.get("running") and last.get("pid") == proc.pid:
            return {**last, "supported": True, "started": True, "command": command}
        code = proc.poll()
        if code is not None:
            _cleanup_unowned_files(root, provider_name, proc.pid)
            return {
                "provider": provider_name,
                "supported": True,
                "running": False,
                "started": False,
                "pid": None,
                "error": f"provider event adapter exited during startup with code {code}",
                "command": command,
            }
        time.sleep(0.025)
        last = adapter_status(root, provider_name)

    termination = _terminate_process_tree(proc.pid)
    _cleanup_unowned_files(root, provider_name, proc.pid)
    return {
        "provider": provider_name,
        "supported": True,
        "running": False,
        "started": False,
        "pid": None,
        "error": "provider event adapter did not acquire ownership before startup synchronization expired",
        "termination": termination,
        "command": command,
        "lastStatus": last,
    }


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
    try:
        with _ownership_lease(root, "lmstudio"):
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
                    publish(root, "lmstudio", "provider_dead", {
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
    except OSError as error:
        # Another verified adapter owns the lock. Do not publish a provider
        # failure: this is adapter duplication/ownership evidence only.
        try:
            if pid_file.exists() and pid_file.read_text(encoding="utf-8").strip() == str(os.getpid()):
                pid_file.unlink()
        except Exception:
            pass
        return 3


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
