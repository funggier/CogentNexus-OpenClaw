#!/usr/bin/env python3
import plistlib
import xml.etree.ElementTree as element_tree
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "templates" / "supervisor"
COMMAND_TEMPLATES = (
    "windows-task.xml", "cogentnexus-supervisor.service", "ai.cogentnexus.supervisor.plist",
    "cron.txt", "docker-compose.yml", "kubernetes-probes.yaml"
)

def main():
    element_tree.parse(TEMPLATES / "windows-task.xml")
    launchd = plistlib.loads((TEMPLATES / "ai.cogentnexus.supervisor.plist").read_bytes())
    compose = yaml.safe_load((TEMPLATES / "docker-compose.yml").read_text(encoding="utf-8"))
    kubernetes = yaml.safe_load((TEMPLATES / "kubernetes-probes.yaml").read_text(encoding="utf-8"))
    if not isinstance(compose, dict) or not isinstance(kubernetes, dict):
        raise SystemExit("container template is not a mapping")
    service = (TEMPLATES / "cogentnexus-supervisor.service").read_text(encoding="utf-8")
    timer = (TEMPLATES / "cogentnexus-supervisor.timer").read_text(encoding="utf-8")
    cron = (TEMPLATES / "cron.txt").read_text(encoding="utf-8")
    if ("Type=oneshot" not in service or "StandardInput=null" not in service
            or "StandardOutput=journal" not in service or "StandardError=journal" not in service
            or "OnUnitActiveSec=5m" not in timer or "Persistent=true" not in timer):
        raise SystemExit("systemd template contract failed")
    if launchd.get("ProcessType") != "Background":
        raise SystemExit("launchd background contract failed")
    if not cron.startswith("*/5 * * * *") or "</dev/null >/dev/null 2>&1" not in cron:
        raise SystemExit("cron template contract failed")
    service_config = compose.get("services", {}).get("openclaw", {})
    if service_config.get("stdin_open") is not False or service_config.get("tty") is not False:
        raise SystemExit("Docker background contract failed")
    if kubernetes.get("stdin") is not False or kubernetes.get("tty") is not False:
        raise SystemExit("Kubernetes background contract failed")
    for name in COMMAND_TEMPLATES:
        if "{{PHASE3}}" not in (TEMPLATES / name).read_text(encoding="utf-8"):
            raise SystemExit(f"missing Phase 3 placeholder: {name}")
    print("Cross-platform template validation: PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
