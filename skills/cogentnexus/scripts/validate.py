#!/usr/bin/env python3
import argparse, ast, json, subprocess, sys
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
    "assets/task-state-template.json", "assets/execution-manifest-template.md", "assets/lesson-template.md",
    "assets/runtime-state-template.json", "assets/ledger-event-template.json", "assets/capability-template.json",
    "assets/recovery-plan-template.json", "assets/runtime-config-template.json", "assets/workflow-manifest-template.json",
    "templates/supervisor/windows-task.xml", "templates/supervisor/cogentnexus-supervisor.service",
    "templates/supervisor/cogentnexus-supervisor.timer", "templates/supervisor/ai.cogentnexus.supervisor.plist",
    "templates/supervisor/cron.txt", "templates/supervisor/docker-compose.yml",
    "templates/supervisor/kubernetes-probes.yaml"
]
PYTHON_FILES = [
    "scripts/task_state.py", "scripts/cogent.py", "scripts/artifact_manifest.py",
    "scripts/capability_registry.py", "scripts/recovery_controller.py", "scripts/runtime.py", "scripts/startup.py", "scripts/workflow.py", "scripts/validate_templates.py"
]
JSON_FILES = [
    "assets/task-state-template.json", "assets/runtime-state-template.json", "assets/ledger-event-template.json",
    "assets/capability-template.json", "assets/recovery-plan-template.json", "assets/runtime-config-template.json",
    "assets/workflow-manifest-template.json"
]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace-singleton", action="store_true")
    args = parser.parse_args()
    skill = ROOT / "SKILL.md"
    text = skill.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise SystemExit("SKILL.md: missing YAML frontmatter")
    metadata = yaml.safe_load(text.split("---", 2)[1])
    if set(metadata) != {"name", "description"} or metadata["name"] != "cogentnexus":
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
    if [path for path in ROOT.rglob("SKILL.md") if path != skill]:
        raise SystemExit("nested SKILL.md files are forbidden")
    if args.workspace_singleton:
        directories = sorted(path.name for path in WORKSPACE_SKILLS.iterdir() if path.is_dir())
        if directories != ["cogentnexus"]:
            raise SystemExit(f"workspace skills must contain only cogentnexus; found: {directories}")
    phase2 = subprocess.run([sys.executable, str(ROOT / "scripts" / "cogent.py"), "--help"], capture_output=True, text=True)
    runtime_cli = subprocess.run([sys.executable, str(ROOT / "scripts" / "runtime.py"), "--help"], capture_output=True, text=True)
    workflow = subprocess.run([sys.executable, str(ROOT / "scripts" / "workflow.py"), "--help"], capture_output=True, text=True)
    startup = subprocess.run([sys.executable, str(ROOT / "scripts" / "startup.py"), "--help"], capture_output=True, text=True)
    if phase2.returncode or not all(word in phase2.stdout for word in ("state", "run", "probe", "verify", "ledger", "recover", "capability", "policy")):
        raise SystemExit("Phase 1-2 CLI validation failed")
    if runtime_cli.returncode or not all(word in runtime_cli.stdout for word in ("supervisor", "concurrency", "context", "scheduler")):
        raise SystemExit("runtime CLI validation failed")
    if workflow.returncode or not all(word in workflow.stdout for word in ("validate", "init", "tick", "run", "status", "supervise", "self-test")):
        raise SystemExit("Workflow CLI validation failed")
    if startup.returncode or not all(word in startup.stdout for word in ("status", "enable", "disable", "ensure")):
        raise SystemExit("Startup CLI validation failed")
    workflow_test = subprocess.run([sys.executable, str(ROOT / "scripts" / "workflow.py"), "self-test"], capture_output=True, text=True)
    if workflow_test.returncode or "PASS" not in workflow_test.stdout:
        raise SystemExit(workflow_test.stderr or workflow_test.stdout or "Workflow self-test failed")
    templates = subprocess.run([sys.executable, str(ROOT / "scripts" / "validate_templates.py")], capture_output=True, text=True)
    if templates.returncode:
        raise SystemExit(templates.stderr or templates.stdout)
    print("CogentNexus validation: PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
