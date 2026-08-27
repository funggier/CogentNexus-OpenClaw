#!/usr/bin/env python3
import argparse, ast, importlib.util, json, subprocess, sys, tempfile, time
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_SKILLS = ROOT.parent
EXPECTED = [
    "references/constitution.md", "references/task-loop.md", "references/execution-success.md",
    "references/resource-survival.md", "references/minimal-memory.md", "references/lesson-learning.md",
    "references/task-resumption.md", "references/output-verification.md", "references/architecture.md",
    "references/runtime-toolkit.md", "references/recovery-controller.md", "references/capability-registry.md",
    "references/artifact-integrity.md", "references/runtime-supervisor.md", "references/concurrency-manager.md",
    "references/context-continuity.md", "references/scheduler-adapters.md", "references/startup-policy.md",
    "scripts/task_state.py", "scripts/cogent.py", "scripts/artifact_manifest.py",
    "scripts/capability_registry.py", "scripts/recovery_controller.py", "scripts/runtime.py", "scripts/startup.py", "scripts/workflow.py", "scripts/validate_templates.py",
    "scripts/provider.py", "scripts/checks.py", "scripts/checks_v092.py", "scripts/cnxclaw.py",
    "scripts/openclaw_route_v092.py", "scripts/openclaw_runtime_boundary_v092.py", "scripts/provider_recovery_v092.py",
    "scripts/host_provider_v092.py", "scripts/host_v092.py", "scripts/host_control_v092.py", "scripts/startup_v092.py", "scripts/lifecycle_v092.py",
    "assets/task-state-template.json", "assets/execution-manifest-template.md", "assets/lesson-template.md",
    "assets/runtime-state-template.json", "assets/ledger-event-template.json", "assets/capability-template.json",
    "assets/recovery-plan-template.json", "assets/runtime-config-template.json", "assets/workflow-manifest-template.json",
    "templates/supervisor/windows-task.xml", "templates/supervisor/cogentnexus-openclaw-supervisor.service",
    "templates/supervisor/cogentnexus-openclaw-supervisor.timer", "templates/supervisor/ai.cogentnexus.openclaw.supervisor.plist",
    "templates/supervisor/cron.txt", "templates/supervisor/docker-compose.yml",
    "templates/supervisor/kubernetes-probes.yaml", "templates/lifecycle/cnxclaw.cmd"
]
PYTHON_FILES = [
    "scripts/task_state.py", "scripts/cogent.py", "scripts/artifact_manifest.py",
    "scripts/capability_registry.py", "scripts/recovery_controller.py", "scripts/runtime.py", "scripts/startup.py", "scripts/workflow.py", "scripts/validate_templates.py",
    "scripts/provider.py", "scripts/checks.py", "scripts/checks_v092.py", "scripts/cnxclaw.py",
    "scripts/openclaw_route_v092.py", "scripts/openclaw_runtime_boundary_v092.py", "scripts/provider_recovery_v092.py",
    "scripts/host_provider_v092.py", "scripts/host_v092.py", "scripts/host_control_v092.py", "scripts/startup_v092.py", "scripts/lifecycle_v092.py"
]
JSON_FILES = [
    "assets/task-state-template.json", "assets/runtime-state-template.json", "assets/ledger-event-template.json",
    "assets/capability-template.json", "assets/recovery-plan-template.json", "assets/runtime-config-template.json",
    "assets/workflow-manifest-template.json"
]

def validate_windows_task_encoding():
    spec = importlib.util.spec_from_file_location("cnxclaw_startup", ROOT / "scripts" / "startup.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    template = (ROOT / "templates" / "supervisor" / "windows-task.xml").read_text(encoding="utf-8")
    with tempfile.TemporaryDirectory() as directory:
        definition = Path(directory) / "task.xml"
        module.write_windows_definition(definition, template)
        payload = definition.read_bytes()
        if not payload.startswith(b"\xff\xfe"):
            raise SystemExit("Windows task XML must have a UTF-16LE BOM")
        document = payload.decode("utf-16")
        if 'encoding="UTF-16"' not in document:
            raise SystemExit("Windows task XML declaration must match its UTF-16 encoding")

def run_workflow_self_test():
    attempts = 2 if sys.platform == "win32" else 1
    last = None
    for attempt in range(1, attempts + 1):
        result = subprocess.run([sys.executable, str(ROOT / "scripts" / "workflow.py"), "self-test"], capture_output=True, text=True)
        last = result
        if result.returncode == 0 and "PASS" in result.stdout:
            return
        combined = f"{result.stdout}\n{result.stderr}"
        runner_teardown_race = "assert runner_pid" in combined and ("WinError 32" in combined or "PermissionError" in combined)
        controller_teardown_race = all(marker in combined for marker in (
            "WF-TEST-SUPERVISE", "not process_alive(child_pid)", "AssertionError",
        ))
        retryable = sys.platform == "win32" and (runner_teardown_race or controller_teardown_race)
        if not retryable or attempt >= attempts:
            break
        time.sleep(1.0)
    raise SystemExit((last.stderr or last.stdout or "Workflow self-test failed") if last else "Workflow self-test failed")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace-singleton", action="store_true")
    args = parser.parse_args()
    skill = ROOT / "SKILL.md"
    text = skill.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise SystemExit("SKILL.md: missing YAML frontmatter")
    metadata = yaml.safe_load(text.split("---", 2)[1])
    if set(metadata) != {"name", "description"} or metadata["name"] != "CogentNexus-OpenClaw":
        raise SystemExit("SKILL.md: invalid frontmatter")
    for relative in EXPECTED:
        path = ROOT / relative
        if not path.is_file():
            raise SystemExit(f"missing required file: {relative}")
        if relative.startswith("references/") and relative not in text:
            raise SystemExit(f"SKILL.md does not route reference: {relative}")
    for relative in JSON_FILES:
        json.loads((ROOT / relative).read_text(encoding="utf-8"))
    for relative in PYTHON_FILES:
        ast.parse((ROOT / relative).read_text(encoding="utf-8"), filename=relative)
    validate_windows_task_encoding()
    if [path for path in ROOT.rglob("SKILL.md") if path != skill]:
        raise SystemExit("nested SKILL.md files are forbidden")
    if args.workspace_singleton:
        directories = sorted(path.name for path in WORKSPACE_SKILLS.iterdir() if path.is_dir())
        if directories != ["cogentnexus-openclaw"]:
            raise SystemExit(f"workspace skills must contain only cogentnexus; found: {directories}")
    phase2 = subprocess.run([sys.executable, str(ROOT / "scripts" / "cogent.py"), "--help"], capture_output=True, text=True)
    runtime_cli = subprocess.run([sys.executable, str(ROOT / "scripts" / "runtime.py"), "--help"], capture_output=True, text=True)
    workflow = subprocess.run([sys.executable, str(ROOT / "scripts" / "workflow.py"), "--help"], capture_output=True, text=True)
    startup = subprocess.run([sys.executable, str(ROOT / "scripts" / "startup.py"), "--help"], capture_output=True, text=True)
    cnx = subprocess.run([sys.executable, str(ROOT / "scripts" / "cnxclaw.py"), "--help"], capture_output=True, text=True)
    if phase2.returncode or not all(word in phase2.stdout for word in ("state", "run", "probe", "verify", "ledger", "recover", "capability", "policy")):
        raise SystemExit("Phase 1-2 CLI validation failed")
    if runtime_cli.returncode or not all(word in runtime_cli.stdout for word in ("supervisor", "concurrency", "context", "scheduler")):
        raise SystemExit("runtime CLI validation failed")
    if workflow.returncode or not all(word in workflow.stdout for word in ("validate", "init", "tick", "run", "status", "supervise", "self-test")):
        raise SystemExit("Workflow CLI validation failed")
    if startup.returncode or not all(word in startup.stdout for word in ("status", "enable", "disable", "ensure")):
        raise SystemExit("Startup CLI validation failed")
    if cnx.returncode or not all(word in cnx.stdout for word in ("check system", "provider list", "--provider ollama|lmstudio", "reset", "uninstall")):
        raise SystemExit("v0.9.2 CNXCLAW CLI validation failed")
    run_workflow_self_test()
    templates = subprocess.run([sys.executable, str(ROOT / "scripts" / "validate_templates.py")], capture_output=True, text=True)
    if templates.returncode:
        raise SystemExit(templates.stderr or templates.stdout)
    print("CogentNexus-OpenClaw validation: PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
