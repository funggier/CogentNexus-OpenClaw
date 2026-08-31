#!/usr/bin/env python3
import plistlib
import xml.etree.ElementTree as element_tree
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "templates" / "supervisor"
LIFECYCLE = ROOT / "templates" / "lifecycle"
COMMAND_TEMPLATES = (
    "windows-task.xml", "cogentnexus-openclaw-supervisor.service", "ai.cogentnexus.openclaw.supervisor.plist",
    "cron.txt", "docker-compose.yml", "kubernetes-probes.yaml"
)

def main():
    element_tree.parse(TEMPLATES / "windows-task.xml")
    launchd = plistlib.loads((TEMPLATES / "ai.cogentnexus.openclaw.supervisor.plist").read_bytes())
    compose = yaml.safe_load((TEMPLATES / "docker-compose.yml").read_text(encoding="utf-8"))
    kubernetes = yaml.safe_load((TEMPLATES / "kubernetes-probes.yaml").read_text(encoding="utf-8"))
    if not isinstance(compose, dict) or not isinstance(kubernetes, dict):
        raise SystemExit("container template is not a mapping")
    service = (TEMPLATES / "cogentnexus-openclaw-supervisor.service").read_text(encoding="utf-8")
    timer = (TEMPLATES / "cogentnexus-openclaw-supervisor.timer").read_text(encoding="utf-8")
    cron = (TEMPLATES / "cron.txt").read_text(encoding="utf-8")
    if ("Type=oneshot" not in service or "StandardInput=null" not in service
            or "StandardOutput=journal" not in service or "StandardError=journal" not in service
            or "OnUnitActiveSec=1m" not in timer or "Persistent=true" not in timer):
        raise SystemExit("systemd template contract failed")
    if launchd.get("ProcessType") != "Background":
        raise SystemExit("launchd background contract failed")
    if not cron.startswith("* * * * *") or "</dev/null >/dev/null 2>&1" not in cron:
        raise SystemExit("cron template contract failed")
    service_config = compose.get("services", {}).get("openclaw", {})
    if service_config.get("stdin_open") is not False or service_config.get("tty") is not False:
        raise SystemExit("Docker background contract failed")
    if kubernetes.get("stdin") is not False or kubernetes.get("tty") is not False:
        raise SystemExit("Kubernetes background contract failed")
    for name in COMMAND_TEMPLATES:
        if "{{RUNTIME}}" not in (TEMPLATES / name).read_text(encoding="utf-8"):
            raise SystemExit(f"missing runtime placeholder: {name}")
    lifecycle_names = (
        "start-cogentnexus-openclaw.cmd", "stop-cogentnexus-openclaw.cmd",
        "start-cogentnexus-openclaw.sh", "stop-cogentnexus-openclaw.sh", "README.md",
    )
    for name in lifecycle_names:
        if not (LIFECYCLE / name).is_file():
            raise SystemExit(f"missing lifecycle launcher: {name}")
    start_contract = (
        (LIFECYCLE / "start-cogentnexus-openclaw.cmd").read_text(encoding="utf-8")
        + (LIFECYCLE / "start-cogentnexus-openclaw.sh").read_text(encoding="utf-8")
    )
    stop_contract = (
        (LIFECYCLE / "stop-cogentnexus-openclaw.cmd").read_text(encoding="utf-8")
        + (LIFECYCLE / "stop-cogentnexus-openclaw.sh").read_text(encoding="utf-8")
    )
    if start_contract.count("lifecycle start --provider") != 2:
        raise SystemExit("portable start lifecycle contract failed")
    if stop_contract.count("lifecycle stop --provider") != 2:
        raise SystemExit("portable stop lifecycle contract failed")
    if stop_contract.count("planned host shutdown") != 2:
        raise SystemExit("portable maintenance reason contract failed")
    print("Cross-platform template validation: PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
