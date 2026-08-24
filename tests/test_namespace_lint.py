import importlib.util
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / "scripts/check_namespace_isolation.py"
SPEC = importlib.util.spec_from_file_location("namespace_lint", SCRIPT)
assert SPEC and SPEC.loader
lint = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(lint)


def test_case_variants_and_generic_operational_names_fail():
    fixtures = [
        ("scripts/example.py", "COGENTNEXUS RESET: PASS"),
        ("scripts/example.py", "CogentNexus uninstall"),
        ("scripts/example.py", "CoGeNtNeXuS-ticket-recovery"),
        ("templates/cogentnexus-uninstall.cmd", "safe"),
        ("scripts/example.py", 'Path(".CoGeNt")'),
        ("scripts/example.py", '"CNX_MODEL"'),
    ]
    for relative, text in fixtures:
        assert lint.find_violations(relative, text), (relative, text)


def test_canonical_variants_and_historical_evidence_pass():
    assert not lint.find_violations("scripts/example.py", "CogentNexus-OpenClaw cnxclaw CNXCLAW_MODEL")
    assert not lint.find_violations("templates/cogentnexus-openclaw-cleanup.cmd", "CogentNexus-HermesAgent")
    assert not lint.find_violations("docs/operations/coordination/reports/old.md", "COGENTNEXUS RESET")
