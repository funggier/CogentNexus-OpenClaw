#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise SystemExit(f"expected patch anchor not found in {path}: {old[:120]!r}")
    if text.count(old) != 1:
        raise SystemExit(f"patch anchor is not unique in {path}: {old[:120]!r}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8", newline="\n")


runtime = ROOT / "skills/cogentnexus/scripts/runtime.py"
host = ROOT / "skills/cogentnexus/scripts/host.py"

replace_once(
    runtime,
    '''def start_ollama_windows():\n    candidates = [\n        Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "Ollama" / "ollama app.exe",\n        Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "Ollama" / "ollama.exe"\n    ]\n    for candidate in candidates:\n        if candidate.is_file():\n            flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)\n            subprocess.Popen([str(candidate)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=flags)\n            return {"ok": True, "command": [str(candidate)]}\n    return {"ok": False, "error": "Ollama application not found"}\n\ndef recover_component(name, config):\n    timeout = int(config["supervisor"]["commandTimeoutSeconds"])\n    if name == "gateway":\n        executable = openclaw_executable()\n        return run_command([executable, "gateway", "start"], max(timeout, 60)) if executable else {"ok": False, "error": "openclaw CLI unavailable"}\n    if name == "ollama" and config["supervisor"].get("allowOllamaStart"):\n        if os.name == "nt":\n            return start_ollama_windows()\n        if shutil.which("systemctl"):\n            return run_command(["systemctl", "--user", "start", "ollama"], max(timeout, 60))\n    return {"ok": False, "error": "no authorized recovery adapter"}\n''',
    '''def start_ollama_windows():\n    # Prefer the server command directly: it is deterministic, headless, and is\n    # the supported standalone/service entry point on Windows. Fall back to the\n    # desktop application only when the CLI binary cannot be resolved.\n    cli_candidates = [\n        shutil.which("ollama"),\n        str(Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "Ollama" / "ollama.exe"),\n    ]\n    for value in cli_candidates:\n        if not value:\n            continue\n        candidate = Path(value)\n        if candidate.is_file():\n            flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)\n            command = [str(candidate), "serve"]\n            subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=flags)\n            return {"ok": True, "command": command}\n    app = Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "Ollama" / "ollama app.exe"\n    if app.is_file():\n        flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)\n        subprocess.Popen([str(app)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=flags)\n        return {"ok": True, "command": [str(app)]}\n    return {"ok": False, "error": "Ollama application not found"}\n\ndef recover_component(name, config, explicit_authority=False):\n    timeout = int(config["supervisor"]["commandTimeoutSeconds"])\n    if name == "gateway":\n        executable = openclaw_executable()\n        return run_command([executable, "gateway", "start"], max(timeout, 60)) if executable else {"ok": False, "error": "openclaw CLI unavailable"}\n    if name == "ollama" and (explicit_authority or config["supervisor"].get("allowOllamaStart")):\n        if os.name == "nt":\n            return start_ollama_windows()\n        if shutil.which("systemctl"):\n            return run_command(["systemctl", "--user", "start", "ollama"], max(timeout, 60))\n        return {"ok": False, "error": "no supported Ollama start adapter"}\n    return {"ok": False, "error": "no authorized recovery adapter"}\n''',
)

replace_once(
    runtime,
    '''def wait_for_runtime_health(config, timeout_seconds=30):\n    """Poll bounded runtime readiness so slow Gateway warm-up needs no second start."""\n''',
    '''def wait_for_runtime_health(config, timeout_seconds=30, require_ollama=True):\n    """Poll bounded readiness for exactly the components requested by the caller."""\n''',
)
replace_once(
    runtime,
    '''        if verified["gateway"]["healthy"] and verified["ollama"]["healthy"]:\n            return verified, attempts, True\n''',
    '''        if verified["gateway"]["healthy"] and (not require_ollama or verified["ollama"]["healthy"]):\n            return verified, attempts, True\n''',
)
replace_once(
    runtime,
    '''        if args.provider and not initial["ollama"]["healthy"]:\n            results["ollama"] = recover_component("ollama", config)\n''',
    '''        if args.provider and not initial["ollama"]["healthy"]:\n            # --provider is an explicit operator/Host request. It authorizes this\n            # bounded provider start without weakening autonomous supervisor fences.\n            results["ollama"] = recover_component("ollama", config, explicit_authority=True)\n''',
)
replace_once(
    runtime,
    '''        verified, verification_attempts, healthy = wait_for_runtime_health(config, timeout_seconds=30)\n''',
    '''        verified, verification_attempts, healthy = wait_for_runtime_health(\n            config, timeout_seconds=30, require_ollama=bool(args.provider)\n        )\n''',
)

replace_once(
    host,
    '''    cutoff = now_iso()\n    before = gateway_status()\n    args = ["supervisor", "tick"] + (["--execute-safe"] if execute_safe else [])\n    result = runtime(root, *args, timeout=180, check=False)\n    after = gateway_status()\n    recovered = []\n    if not before.get("healthy") and after.get("healthy"):\n        recovered = promote_interrupted_direct(root, cutoff, "CogentNexus Host confirmed Gateway recovery; prior direct turn was interrupted")\n    return {\n        "result": "ok" if result.returncode == 0 else "runtime-error",\n        "before": before,\n        "after": after,\n        "runtime": parse_json_output(result.stdout) if result.stdout.strip() else {"stderr": result.stderr.strip()},\n        "recoveredTickets": recovered,\n    }\n''',
    '''    cutoff = now_iso()\n    before = gateway_status()\n    lifecycle_status = runtime(root, "lifecycle", "status", timeout=60, check=False)\n    lifecycle_before = (\n        parse_json_output(lifecycle_status.stdout)\n        if lifecycle_status.stdout.strip()\n        else {"exitCode": lifecycle_status.returncode, "stderr": lifecycle_status.stderr.strip()}\n    )\n    provider_required = state.get("desiredProvider") == "running"\n    provider_healthy = bool(\n        isinstance(lifecycle_before, dict)\n        and isinstance(lifecycle_before.get("ollama"), dict)\n        and lifecycle_before["ollama"].get("healthy")\n    )\n    reconcile = None\n    if execute_safe and (not before.get("healthy") or (provider_required and not provider_healthy)):\n        reconcile_args = ["lifecycle", "start"] + (["--provider"] if provider_required else [])\n        reconcile_result = runtime(root, *reconcile_args, timeout=240, check=False)\n        reconcile = {\n            "exitCode": reconcile_result.returncode,\n            "output": parse_json_output(reconcile_result.stdout) if reconcile_result.stdout.strip() else None,\n            "stderr": reconcile_result.stderr.strip(),\n            "providerRequired": provider_required,\n        }\n    args = ["supervisor", "tick"] + (["--execute-safe"] if execute_safe else [])\n    result = runtime(root, *args, timeout=180, check=False)\n    after = gateway_status()\n    recovered = []\n    if not before.get("healthy") and after.get("healthy"):\n        recovered = promote_interrupted_direct(root, cutoff, "CogentNexus Host confirmed Gateway recovery; prior direct turn was interrupted")\n    return {\n        "result": "ok" if result.returncode == 0 else "runtime-error",\n        "before": before,\n        "lifecycleBefore": lifecycle_before,\n        "reconcile": reconcile,\n        "after": after,\n        "runtime": parse_json_output(result.stdout) if result.stdout.strip() else {"stderr": result.stderr.strip()},\n        "recoveredTickets": recovered,\n    }\n''',
)

# Regression coverage for explicit authority, gateway-only readiness, and Host
# desired-state reconciliation after a provider outage/reboot.
test_path = ROOT / "tests/test_provider_recovery_authority.py"
test_path.write_text('''from __future__ import annotations\n\nimport importlib.util\nimport json\nimport subprocess\nimport tempfile\nimport unittest\nfrom pathlib import Path\nfrom unittest import mock\n\nROOT = Path(__file__).resolve().parents[1]\n\ndef load(name: str, path: Path):\n    spec = importlib.util.spec_from_file_location(name, path)\n    module = importlib.util.module_from_spec(spec)\n    assert spec and spec.loader\n    spec.loader.exec_module(module)\n    return module\n\nruntime = load("cnx_runtime_provider_test", ROOT / "skills/cogentnexus/scripts/runtime.py")\nhost = load("cnx_host_provider_test", ROOT / "skills/cogentnexus/scripts/host.py")\n\nclass ProviderRecoveryAuthorityTests(unittest.TestCase):\n    def config(self):\n        return runtime.deep_merge(runtime.DEFAULT_CONFIG, {"supervisor": {"allowOllamaStart": False}})\n\n    def test_explicit_provider_start_bypasses_only_autonomous_fence(self):\n        config = self.config()\n        with mock.patch.object(runtime.os, "name", "nt"), mock.patch.object(\n            runtime, "start_ollama_windows", return_value={"ok": True, "command": ["ollama", "serve"]}\n        ) as starter:\n            result = runtime.recover_component("ollama", config, explicit_authority=True)\n        self.assertTrue(result["ok"])\n        starter.assert_called_once_with()\n\n    def test_autonomous_provider_recovery_stays_fenced_by_default(self):\n        config = self.config()\n        with mock.patch.object(runtime.os, "name", "nt"), mock.patch.object(runtime, "start_ollama_windows") as starter:\n            result = runtime.recover_component("ollama", config)\n        self.assertFalse(result["ok"])\n        self.assertEqual(result["error"], "no authorized recovery adapter")\n        starter.assert_not_called()\n\n    def test_gateway_only_readiness_does_not_require_ollama(self):\n        config = self.config()\n        with mock.patch.object(runtime, "gateway_probe", return_value={"healthy": True}), mock.patch.object(\n            runtime, "ollama_probe", return_value={"healthy": False}\n        ):\n            _, _, gateway_only = runtime.wait_for_runtime_health(config, timeout_seconds=0, require_ollama=False)\n            _, _, provider_required = runtime.wait_for_runtime_health(config, timeout_seconds=0, require_ollama=True)\n        self.assertTrue(gateway_only)\n        self.assertFalse(provider_required)\n\n    def test_host_desired_provider_reconciles_with_explicit_lifecycle_start(self):\n        with tempfile.TemporaryDirectory() as tmp:\n            root = Path(tmp) / ".cogent"\n            host.save_state(root, {\n                "schemaVersion": 1, "mode": "managed", "desiredGateway": "running",\n                "desiredProvider": "running", "generation": 3\n            })\n            calls = []\n            def fake_runtime(_root, *args, **kwargs):\n                calls.append(args)\n                if args[:2] == ("lifecycle", "status"):\n                    return subprocess.CompletedProcess(args, 0, json.dumps({\n                        "gateway": {"healthy": True}, "ollama": {"healthy": False}\n                    }), "")\n                if args[:2] == ("lifecycle", "start"):\n                    return subprocess.CompletedProcess(args, 0, json.dumps({"started": True}), "")\n                return subprocess.CompletedProcess(args, 0, json.dumps({"status": "healthy"}), "")\n            with mock.patch.object(host, "gateway_status", return_value={"healthy": True}), mock.patch.object(host, "runtime", side_effect=fake_runtime):\n                result = host.supervisor_tick(root, True)\n            self.assertIn(("lifecycle", "start", "--provider"), calls)\n            self.assertTrue(result["reconcile"]["providerRequired"])\n            self.assertEqual(result["reconcile"]["exitCode"], 0)\n\nif __name__ == "__main__":\n    unittest.main()\n''', encoding="utf-8", newline="\n")

# Patch release metadata.
(ROOT / "VERSION").write_text("0.8.2\n", encoding="utf-8")
for rel in ("plugins/cogentnexus-rotation/package.json", "plugins/cogentnexus-rotation/openclaw.plugin.json", "plugins/cogentnexus-rotation/package-lock.json"):
    path = ROOT / rel
    data = json.loads(path.read_text(encoding="utf-8"))
    data["version"] = "0.8.2"
    if rel.endswith("package-lock.json"):
        data.setdefault("packages", {}).setdefault("", {})["version"] = "0.8.2"
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")

for rel in ("README.md", "docs/INSTALL.md", "docs/INSTALL.th.md"):
    path = ROOT / rel
    text = path.read_text(encoding="utf-8")
    text = text.replace("v0.8.1", "v0.8.2").replace("cogentnexus-v0.8.1", "cogentnexus-v0.8.2")
    path.write_text(text, encoding="utf-8", newline="\n")

release = ROOT / "docs/releases/v0.8.2.md"
release.write_text('''# CogentNexus v0.8.2\n\nv0.8.2 fixes managed local-provider recovery discovered during a real Windows v0.8.1 installation.\n\n## Fixed\n\n- `cnx enable` and `cnx start` now treat an explicit `--provider` lifecycle request as bounded authority to start the local Ollama provider even while autonomous low-level recovery remains fenced by `allowOllamaStart`.\n- Host supervisor reconciliation now uses persisted `desiredProvider=running` to restore Ollama after a crash/reboot before continuing normal runtime supervision.\n- Gateway-only lifecycle starts no longer fail merely because Ollama is intentionally unavailable.\n- Windows managed Ollama startup prefers the deterministic `ollama serve` server command, with the desktop app retained as a fallback.\n\n## Compatibility\n\nNo Ticket, policy, session-generation, or continuity schema changes from v0.8.1. Existing `.cogent` state and installed bridge data remain compatible.\n''', encoding="utf-8", newline="\n")

print("v0.8.2 provider recovery patch applied")
