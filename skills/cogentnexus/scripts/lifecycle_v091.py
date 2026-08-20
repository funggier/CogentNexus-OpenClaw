#!/usr/bin/env python3
"""CogentNexus destructive lifecycle commands for cnx.cmd.

`reset` returns the currently installed release to fresh-install state without
changing program files or release version. `uninstall` restores native
OpenClaw first, then removes CogentNexus-owned state, plugin registration,
startup integration, skill files, and the cnx.cmd launcher.

Both commands require an explicit interactive `y` confirmation. Any other
input, including Enter, cancels without mutation.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve()
SKILL = HERE.parents[1]
WORKSPACE = SKILL.parents[1]
STATE_ROOT = WORKSPACE.parent
DEFAULT_ROOT = WORKSPACE / ".cogent"
PLUGIN_ID = "cogentnexus-rotation"
EXTENSION = STATE_ROOT / "extensions" / PLUGIN_ID
LAUNCHER = WORKSPACE / "cnx.cmd"
HOST_CONTROL = HERE.with_name("host_control_v091.py")
HOST = HERE.with_name("host_v091.py")
STARTUP = HERE.with_name("startup_v091.py")
BOOTSTRAP = EXTENSION / "scripts" / "bootstrap-ticket-db.mjs"


def local_cnx_data_root() -> Path | None:
    """Return the installer-owned Windows backup root, never an arbitrary parent."""
    value = os.environ.get("LOCALAPPDATA")
    if not value:
        return None
    return Path(value).expanduser().resolve() / "CogentNexus"


def creation_flags(detached: bool = False) -> int:
    if os.name != "nt":
        return 0
    flags = subprocess.CREATE_NO_WINDOW
    if detached:
        flags |= subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
    return flags


def run(cmd: list[str], timeout: int = 180, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=timeout,
        creationflags=creation_flags(),
    )
    if check and result.returncode != 0:
        detail = (result.stderr or result.stdout or f"command failed: {cmd}").strip()
        raise RuntimeError(detail)
    return result


def forward(result: subprocess.CompletedProcess[str]) -> None:
    if result.stdout:
        sys.stdout.write(result.stdout)
    if result.stderr:
        sys.stderr.write(result.stderr)


def openclaw_executable() -> str:
    names = ("openclaw.cmd", "openclaw.exe", "openclaw") if os.name == "nt" else ("openclaw",)
    for name in names:
        found = shutil.which(name)
        if found:
            return found
    raise FileNotFoundError("OpenClaw CLI not found on PATH")


def node_executable() -> str:
    found = shutil.which("node")
    if not found:
        raise FileNotFoundError("Node.js is required for CogentNexus schema bootstrap")
    return found


def confirm(action: str) -> bool:
    if action == "reset":
        print("WARNING: CogentNexus will be reset to fresh-install state.")
        print("")
        print("This permanently removes CogentNexus Tickets, recovery/delivery/runtime state,")
        print("session authority, workflow runtime data, diagnostics, and CNX configuration changes.")
        print("Installed CogentNexus program files and release version remain unchanged.")
        print("OpenClaw and Ollama data are not removed.")
    elif action == "uninstall":
        print("WARNING: This will completely remove CogentNexus.")
        print("")
        print("CogentNexus runtime state, configuration, startup integration, OpenClaw plugin,")
        print("skill files, backups, and cnx.cmd will be removed.")
        print("OpenClaw and Ollama are not removed.")
    else:
        raise ValueError(f"unsupported destructive lifecycle action: {action}")
    print("")
    try:
        answer = input("Continue? [y/N]: ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        print("")
        answer = ""
    if answer != "y":
        print(f"CogentNexus {action} cancelled. No changes were made.")
        return False
    return True


def disable_managed(root: Path) -> None:
    result = run([sys.executable, str(HOST_CONTROL), "--root", str(root), "disable"], timeout=240, check=False)
    forward(result)
    if result.returncode != 0:
        raise RuntimeError("cnx disable failed; refusing destructive lifecycle while CNX ownership may still be MANAGED")


def disable_startup(root: Path) -> None:
    result = run([sys.executable, str(STARTUP), "--root", str(root), "disable"], timeout=120, check=False)
    if result.returncode != 0:
        detail = (result.stderr or result.stdout or "startup adapter disable failed").strip()
        raise RuntimeError(detail)


def config_unset(path: str) -> None:
    exe = openclaw_executable()
    # Missing paths are already equivalent to fresh-install defaults.
    run([exe, "config", "unset", path], timeout=60, check=False)


def reset_plugin_configuration() -> None:
    config_unset(f"plugins.entries.{PLUGIN_ID}.config")
    config_unset(f"plugins.entries.{PLUGIN_ID}.hooks")


def bootstrap_ticket_database() -> None:
    if not BOOTSTRAP.is_file():
        raise RuntimeError(
            "installed CogentNexus plugin lacks scripts/bootstrap-ticket-db.mjs; "
            "the release package cannot provide a verified fresh reset"
        )
    run([node_executable(), str(BOOTSTRAP), "--workspace", str(WORKSPACE)], timeout=120, check=True)


def gateway_health() -> dict[str, Any]:
    result = run([openclaw_executable(), "gateway", "status"], timeout=60, check=False)
    evidence = f"{result.stdout}\n{result.stderr}"
    return {
        "healthy": result.returncode == 0 and "Runtime: running" in evidence and "Connectivity probe: ok" in evidence,
        "exitCode": result.returncode,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
    }


def verify_plugin_loaded() -> dict[str, Any]:
    result = run([openclaw_executable(), "plugins", "inspect", PLUGIN_ID, "--runtime", "--json"], timeout=60, check=True)
    try:
        value = json.loads(result.stdout)
    except json.JSONDecodeError as error:
        raise RuntimeError("OpenClaw plugin inspect returned invalid JSON") from error
    plugin = value.get("plugin") if isinstance(value, dict) and isinstance(value.get("plugin"), dict) else {}
    if plugin.get("enabled") is not True or plugin.get("activated") is not True or plugin.get("status") != "loaded":
        raise RuntimeError(
            "CogentNexus plugin did not return to loaded MANAGED runtime after reset: "
            f"enabled={plugin.get('enabled')} activated={plugin.get('activated')} status={plugin.get('status')}"
        )
    return plugin


def reset(root: Path) -> int:
    if not confirm("reset"):
        return 0
    try:
        disable_managed(root)
        disable_startup(root)
        reset_plugin_configuration()
        if root.exists():
            shutil.rmtree(root)

        # Recreate the same baseline sequence as a fresh release install while
        # retaining the already-installed release files and plugin payload.
        run([sys.executable, str(HOST), "--root", str(root), "init"], timeout=120, check=True)
        bootstrap_ticket_database()
        run([sys.executable, str(HOST), "--root", str(root), "policy", "apply"], timeout=120, check=True)
        enabled = run([sys.executable, str(HOST_CONTROL), "--root", str(root), "enable"], timeout=300, check=False)
        forward(enabled)
        if enabled.returncode != 0:
            raise RuntimeError("CogentNexus transactional enable failed after reset")

        plugin = verify_plugin_loaded()
        gateway = gateway_health()
        if not gateway.get("healthy"):
            raise RuntimeError("OpenClaw Gateway failed health verification after CogentNexus reset")
        print("")
        print("COGENTNEXUS RESET: PASS")
        print(f"Workspace : {WORKSPACE}")
        print(f"Plugin    : {plugin.get('status')}")
        print("State     : fresh-install MANAGED")
        return 0
    except Exception as error:
        # Never leave an uncertain partially reinitialized installation claiming
        # MANAGED authority. Best-effort disable preserves native OpenClaw.
        try:
            if (root / "host" / "controller.json").exists():
                run([sys.executable, str(HOST_CONTROL), "--root", str(root), "disable"], timeout=240, check=False)
        except Exception:
            pass
        print(json.dumps({
            "result": "error",
            "action": "reset",
            "error": str(error),
            "safety": "CogentNexus was left disabled/PASSTHROUGH when possible; no automatic inference recovery was attempted",
        }, ensure_ascii=False, indent=2))
        return 1


def plugin_registered() -> bool:
    result = run([openclaw_executable(), "plugins", "list", "--json"], timeout=60, check=False)
    return result.returncode == 0 and PLUGIN_ID in result.stdout


def remove_linked_load_paths() -> None:
    exe = openclaw_executable()
    current = run([exe, "config", "get", "plugins.load.paths", "--json"], timeout=60, check=False)
    if current.returncode != 0 or not current.stdout.strip():
        return
    try:
        value = json.loads(current.stdout)
    except json.JSONDecodeError:
        return
    if not isinstance(value, list):
        return
    filtered = [item for item in value if not (isinstance(item, str) and PLUGIN_ID.lower() in item.lower())]
    if filtered == value:
        return
    run(
        [exe, "config", "set", "plugins.load.paths", json.dumps(filtered, separators=(",", ":")), "--strict-json", "--replace"],
        timeout=60,
        check=True,
    )


def uninstall_plugin() -> None:
    exe = openclaw_executable()
    if plugin_registered():
        result = run([exe, "plugins", "uninstall", PLUGIN_ID, "--force"], timeout=180, check=False)
        forward(result)
        if result.returncode != 0:
            raise RuntimeError("OpenClaw CogentNexus plugin uninstall failed")
    remove_linked_load_paths()
    config_unset(f"plugins.entries.{PLUGIN_ID}")
    if plugin_registered():
        raise RuntimeError("CogentNexus plugin remains registered after uninstall cleanup")


def schedule_windows_cleanup(paths: list[Path]) -> None:
    cleanup = Path(tempfile.gettempdir()) / f"cogentnexus-uninstall-{os.getpid()}.cmd"
    lines = ["@echo off", "timeout /t 2 /nobreak >nul"]
    for path in paths:
        escaped = str(path).replace('"', '""')
        if path.suffix.lower() in {".cmd", ".bat", ".exe"}:
            lines.append(f'del /f /q "{escaped}" >nul 2>&1')
        else:
            lines.append(f'rmdir /s /q "{escaped}" >nul 2>&1')
    lines.append('del /f /q "%~f0" >nul 2>&1')
    cleanup.write_text("\r\n".join(lines) + "\r\n", encoding="ascii")
    subprocess.Popen(
        ["cmd.exe", "/d", "/c", str(cleanup)],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        close_fds=True,
        creationflags=creation_flags(detached=True),
    )


def uninstall_owned_paths(root: Path) -> list[Path]:
    owned = [root, EXTENSION, SKILL, LAUNCHER]
    local_root = local_cnx_data_root()
    if local_root is not None:
        owned.append(local_root)
    # Preserve order while preventing duplicate deletion when custom paths overlap.
    result: list[Path] = []
    seen: set[str] = set()
    for path in owned:
        key = os.path.normcase(str(path.resolve()))
        if key in seen:
            continue
        seen.add(key)
        result.append(path)
    return result


def uninstall(root: Path) -> int:
    if not confirm("uninstall"):
        return 0
    try:
        disable_managed(root)
        disable_startup(root)
        uninstall_plugin()

        gateway = gateway_health()
        if not gateway.get("healthy"):
            raise RuntimeError("native OpenClaw Gateway is not healthy after CogentNexus uninstall boundary")

        owned = uninstall_owned_paths(root)
        if os.name == "nt":
            # cnx.cmd and this Python module may still be executing. Delete them
            # only after this process and its parent batch file have returned.
            schedule_windows_cleanup(owned)
        else:
            for path in owned:
                if path.is_dir():
                    shutil.rmtree(path, ignore_errors=False)
                elif path.exists():
                    path.unlink()

        print("")
        print("COGENTNEXUS UNINSTALL: PASS")
        print("OpenClaw : native / healthy")
        print("Ollama   : unchanged")
        if os.name == "nt":
            print("Cleanup  : cnx.cmd and remaining CNX files/backups scheduled for removal after command exit")
        return 0
    except Exception as error:
        print(json.dumps({
            "result": "error",
            "action": "uninstall",
            "error": str(error),
            "safety": "destructive file cleanup was not scheduled unless native OpenClaw health was verified",
        }, ensure_ascii=False, indent=2))
        return 1


def main(command: str, root: Path | None = None) -> int:
    resolved = (root or DEFAULT_ROOT).resolve()
    if command == "reset":
        return reset(resolved)
    if command == "uninstall":
        return uninstall(resolved)
    raise ValueError(f"unsupported lifecycle command: {command}")


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in {"reset", "uninstall"}:
        print("Usage: lifecycle_v091.py reset|uninstall", file=sys.stderr)
        raise SystemExit(2)
    raise SystemExit(main(sys.argv[1]))
