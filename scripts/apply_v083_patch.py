#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"expected exactly one match in {path}, found {count}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8", newline="\n")


runtime = ROOT / "skills/cogentnexus/scripts/runtime.py"
old_stop = '''def stop_ollama(config):
    timeout = int(config["supervisor"]["commandTimeoutSeconds"])
    if os.name == "nt":
        executable = shutil.which("taskkill")
        return run_command([executable, "/IM", "ollama.exe", "/T"], timeout) if executable else {"ok": False, "error": "taskkill unavailable"}
    if shutil.which("systemctl"):
        return run_command(["systemctl", "--user", "stop", "ollama"], max(timeout, 60))
    return {"ok": False, "error": "no managed Ollama stop adapter"}
'''
new_stop = '''def stop_ollama(config):
    timeout = int(config["supervisor"]["commandTimeoutSeconds"])
    initial = ollama_probe(config)
    if not initial.get("enabled") or not initial.get("healthy"):
        return {"ok": True, "skipped": True, "reason": "already stopped", "initial": initial}
    if os.name == "nt":
        executable = shutil.which("taskkill")
        if not executable:
            return {"ok": False, "error": "taskkill unavailable"}
        # The desktop tray process can respawn the server, so terminate it first,
        # then force the server process tree down. /F is required for child
        # processes that Windows refuses to terminate gracefully.
        attempts = []
        for image in ("ollama app.exe", "ollama.exe"):
            command = [executable, "/IM", image, "/T", "/F"]
            attempts.append({"image": image, "command": command, "result": run_command(command, timeout)})
        return {"ok": any(item["result"].get("ok") for item in attempts), "attempts": attempts}
    if shutil.which("systemctl"):
        return run_command(["systemctl", "--user", "stop", "ollama"], max(timeout, 60))
    return {"ok": False, "error": "no managed Ollama stop adapter"}
'''
replace_once(runtime, old_stop, new_stop)

anchor = '''def lifecycle_cmd(args):
'''
helper = '''def wait_for_runtime_stopped(config, timeout_seconds=30, require_ollama=True):
    """Poll bounded shutdown verification for exactly the components requested."""
    deadline = time.monotonic() + max(0.0, float(timeout_seconds))
    attempts = 0
    verified = None
    while True:
        attempts += 1
        verified = {
            "gateway": gateway_probe(int(config["supervisor"]["commandTimeoutSeconds"])),
            "ollama": ollama_probe(config),
        }
        gateway_stopped = not verified["gateway"].get("healthy", False)
        provider_stopped = (not verified["ollama"].get("enabled", True)) or (not verified["ollama"].get("healthy", False))
        stopped = {"gateway": gateway_stopped, "ollama": provider_stopped}
        if gateway_stopped and (not require_ollama or provider_stopped):
            return verified, stopped, attempts, True
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            return verified, stopped, attempts, False
        time.sleep(min(1.0, remaining))

'''
replace_once(runtime, anchor, helper + anchor)

old_lifecycle_stop = '''    if args.command_name == "stop":
        marker = marker or set_maintenance(root, args.reason, args.owner)
        executable = openclaw_executable()
        results = {"gateway": run_command([executable, "gateway", "stop"], 60) if executable else {"ok": False, "error": "openclaw CLI unavailable"}}
        if args.provider:
            results["ollama"] = stop_ollama(config)
        append_runtime_event(root, "ACTION", "Runtime stopped for intentional shutdown", {"providerRequested": bool(args.provider), "results": results})
        emit({"maintenance": marker, "results": results, "safeToPowerOff": bool(results["gateway"].get("ok"))})
        return 0 if results["gateway"].get("ok") else 2
'''
new_lifecycle_stop = '''    if args.command_name == "stop":
        marker = marker or set_maintenance(root, args.reason, args.owner)
        executable = openclaw_executable()
        results = {"gateway": run_command([executable, "gateway", "stop"], 60) if executable else {"ok": False, "error": "openclaw CLI unavailable"}}
        if args.provider:
            results["ollama"] = stop_ollama(config)
        verified, verified_stopped, verification_attempts, stopped = wait_for_runtime_stopped(
            config, timeout_seconds=30, require_ollama=bool(args.provider)
        )
        verification = {"attempts": verification_attempts, "timeoutSeconds": 30}
        append_runtime_event(root, "ACTION", "Runtime stopped for intentional shutdown" if stopped else "Runtime shutdown incomplete", {
            "providerRequested": bool(args.provider), "results": results, "verified": verified,
            "verifiedStopped": verified_stopped, "verification": verification, "safeToPowerOff": stopped,
        })
        emit({"maintenance": marker, "results": results, "verified": verified, "verifiedStopped": verified_stopped,
              "verification": verification, "safeToPowerOff": stopped})
        return 0 if stopped else 2
'''
replace_once(runtime, old_lifecycle_stop, new_lifecycle_stop)

# Version metadata.
(ROOT / "VERSION").write_text("0.8.3\n", encoding="utf-8")
for rel, limit in (
    ("plugins/cogentnexus-rotation/package.json", 1),
    ("plugins/cogentnexus-rotation/openclaw.plugin.json", 1),
    ("plugins/cogentnexus-rotation/package-lock.json", 2),
):
    path = ROOT / rel
    text = path.read_text(encoding="utf-8")
    old = '"version": "0.8.2"'
    if text.count(old) < limit:
        raise SystemExit(f"not enough version matches in {rel}")
    path.write_text(text.replace(old, '"version": "0.8.3"', limit), encoding="utf-8", newline="\n")

# Regression tests from the real Windows failure.
test = ROOT / "tests/test_windows_stop_lifecycle.py"
test.write_text(r'''from __future__ import annotations

import argparse
import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]


def load_runtime():
    spec = importlib.util.spec_from_file_location("cnx_runtime_windows_stop_test", ROOT / "skills/cogentnexus/scripts/runtime.py")
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


runtime = load_runtime()


class WindowsStopLifecycleTests(unittest.TestCase):
    def config(self):
        return runtime.deep_merge(runtime.DEFAULT_CONFIG, {"supervisor": {"commandTimeoutSeconds": 1}})

    def test_windows_stop_force_terminates_desktop_and_server_trees(self):
        config = self.config()
        healthy = {"name": "ollama", "enabled": True, "healthy": True, "evidence": "fixture"}
        with mock.patch.object(runtime.os, "name", "nt"), \
             mock.patch.object(runtime, "ollama_probe", return_value=healthy), \
             mock.patch.object(runtime.shutil, "which", return_value=r"C:\\Windows\\System32\\taskkill.exe"), \
             mock.patch.object(runtime, "run_command", side_effect=[
                 {"ok": False, "exitCode": 128, "stderr": "not running"},
                 {"ok": True, "exitCode": 0, "stderr": ""},
             ]) as runner:
            result = runtime.stop_ollama(config)
        self.assertTrue(result["ok"])
        self.assertEqual(runner.call_count, 2)
        first = runner.call_args_list[0].args[0]
        second = runner.call_args_list[1].args[0]
        self.assertEqual(first[-4:], ["/IM", "ollama app.exe", "/T", "/F"])
        self.assertEqual(second[-4:], ["/IM", "ollama.exe", "/T", "/F"])

    def test_shutdown_verification_requires_requested_provider_to_be_down(self):
        config = self.config()
        with mock.patch.object(runtime, "gateway_probe", return_value={"enabled": True, "healthy": False}), \
             mock.patch.object(runtime, "ollama_probe", return_value={"enabled": True, "healthy": True}):
            _, stopped, _, safe = runtime.wait_for_runtime_stopped(config, timeout_seconds=0, require_ollama=True)
        self.assertTrue(stopped["gateway"])
        self.assertFalse(stopped["ollama"])
        self.assertFalse(safe)

    def test_lifecycle_stop_does_not_claim_safe_poweroff_when_provider_remains_up(self):
        config = self.config()
        args = argparse.Namespace(
            root=Path(tempfile.mkdtemp()), command_name="stop", reason="planned shutdown", owner="operator", provider=True
        )
        emitted = []
        with mock.patch.object(runtime, "load_config", return_value=config), \
             mock.patch.object(runtime, "maintenance_status", return_value=None), \
             mock.patch.object(runtime, "set_maintenance", return_value={"active": True}), \
             mock.patch.object(runtime, "openclaw_executable", return_value="openclaw"), \
             mock.patch.object(runtime, "run_command", return_value={"ok": True, "exitCode": 0}), \
             mock.patch.object(runtime, "stop_ollama", return_value={"ok": False, "exitCode": 128}), \
             mock.patch.object(runtime, "wait_for_runtime_stopped", return_value=(
                 {"gateway": {"healthy": False}, "ollama": {"enabled": True, "healthy": True}},
                 {"gateway": True, "ollama": False}, 2, False,
             )), \
             mock.patch.object(runtime, "append_runtime_event"), \
             mock.patch.object(runtime, "emit", side_effect=emitted.append):
            code = runtime.lifecycle_cmd(args)
        self.assertEqual(code, 2)
        self.assertFalse(emitted[-1]["safeToPowerOff"])
        self.assertFalse(emitted[-1]["verifiedStopped"]["ollama"])

    def test_lifecycle_stop_uses_verified_shutdown_as_terminal_truth(self):
        config = self.config()
        args = argparse.Namespace(
            root=Path(tempfile.mkdtemp()), command_name="stop", reason="planned shutdown", owner="operator", provider=True
        )
        emitted = []
        with mock.patch.object(runtime, "load_config", return_value=config), \
             mock.patch.object(runtime, "maintenance_status", return_value=None), \
             mock.patch.object(runtime, "set_maintenance", return_value={"active": True}), \
             mock.patch.object(runtime, "openclaw_executable", return_value="openclaw"), \
             mock.patch.object(runtime, "run_command", return_value={"ok": True, "exitCode": 0}), \
             mock.patch.object(runtime, "stop_ollama", return_value={"ok": True}), \
             mock.patch.object(runtime, "wait_for_runtime_stopped", return_value=(
                 {"gateway": {"healthy": False}, "ollama": {"enabled": True, "healthy": False}},
                 {"gateway": True, "ollama": True}, 1, True,
             )), \
             mock.patch.object(runtime, "append_runtime_event"), \
             mock.patch.object(runtime, "emit", side_effect=emitted.append):
            code = runtime.lifecycle_cmd(args)
        self.assertEqual(code, 0)
        self.assertTrue(emitted[-1]["safeToPowerOff"])
        self.assertTrue(emitted[-1]["verifiedStopped"]["ollama"])


if __name__ == "__main__":
    unittest.main()
''', encoding="utf-8", newline="\n")

release = ROOT / "docs/releases/v0.8.3.md"
release.write_text('''# CogentNexus v0.8.3\n\nv0.8.3 fixes Windows managed shutdown semantics discovered during real end-to-end testing of v0.8.2.\n\n## Fixed\n\n- Windows Ollama shutdown now force-terminates the desktop/tray process tree and `ollama.exe` server tree so child processes cannot block or immediately respawn the provider.\n- `cnx stop` now verifies the Gateway and, when requested, Ollama are actually down before reporting shutdown success.\n- `safeToPowerOff` is now derived from verified component state rather than the Gateway stop command alone.\n- A requested provider that remains healthy makes lifecycle stop return a non-zero status instead of falsely reporting a safe shutdown.\n\n## Compatibility\n\nNo Ticket, policy, delivery, or continuity schema changes from v0.8.2. Existing `.cogent` state remains compatible.\n''', encoding="utf-8", newline="\n")

print("Applied v0.8.3 Windows shutdown lifecycle patch")
