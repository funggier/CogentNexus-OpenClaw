from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "skills" / "cogentnexus-openclaw" / "templates" / "supervisor" / "windows-task.xml"
NS = {"t": "http://schemas.microsoft.com/windows/2004/02/mit/task"}


def test_windows_supervisor_recovery_budget_exceeds_bounded_host_transaction():
    document = ET.parse(TEMPLATE).getroot()
    settings = document.find("t:Settings", NS)
    assert settings is not None
    assert settings.findtext("t:MultipleInstancesPolicy", namespaces=NS) == "IgnoreNew"
    assert settings.findtext("t:ExecutionTimeLimit", namespaces=NS) == "PT15M"
