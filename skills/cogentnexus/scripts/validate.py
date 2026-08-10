#!/usr/bin/env python3
import argparse,ast,json,subprocess,sys
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[1]; WORKSPACE_SKILLS=ROOT.parent
EXPECTED=["references/constitution.md","references/task-loop.md","references/execution-success.md","references/resource-survival.md",
"references/minimal-memory.md","references/lesson-learning.md","references/task-resumption.md","references/output-verification.md",
"references/architecture.md","references/runtime-toolkit.md","scripts/task_state.py","scripts/cogent.py","assets/task-state-template.json",
"assets/execution-manifest-template.md","assets/lesson-template.md","assets/runtime-state-template.json","assets/ledger-event-template.json"]
def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--workspace-singleton",action="store_true"); args=parser.parse_args()
    skill=ROOT/"SKILL.md"; text=skill.read_text(encoding="utf-8")
    if not text.startswith("---\n"): raise SystemExit("SKILL.md: missing YAML frontmatter")
    metadata=yaml.safe_load(text.split("---",2)[1])
    if set(metadata)!={"name","description"} or metadata["name"]!="cogentnexus": raise SystemExit("SKILL.md: invalid frontmatter")
    for relative in EXPECTED:
        path=ROOT/relative
        if not path.is_file(): raise SystemExit(f"missing required file: {relative}")
        if relative.startswith("references/") and relative not in text: raise SystemExit(f"SKILL.md does not route reference: {relative}")
    for relative in ("assets/task-state-template.json","assets/runtime-state-template.json","assets/ledger-event-template.json"):
        json.loads((ROOT/relative).read_text(encoding="utf-8"))
    for relative in ("scripts/task_state.py","scripts/cogent.py"): ast.parse((ROOT/relative).read_text(encoding="utf-8"),filename=relative)
    if [p for p in ROOT.rglob("SKILL.md") if p!=skill]: raise SystemExit("nested SKILL.md files are forbidden")
    if args.workspace_singleton:
        directories=sorted(p.name for p in WORKSPACE_SKILLS.iterdir() if p.is_dir())
        if directories!=["cogentnexus"]: raise SystemExit(f"workspace skills must contain only cogentnexus; found: {directories}")
    help_text=subprocess.run([sys.executable,str(ROOT/"scripts"/"cogent.py"),"--help"],capture_output=True,text=True)
    if help_text.returncode or not all(word in help_text.stdout for word in ("state","run","probe","verify","ledger")): raise SystemExit("runtime CLI validation failed")
    print("CogentNexus validation: PASS"); return 0
if __name__=="__main__": raise SystemExit(main())
