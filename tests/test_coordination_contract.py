from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CURRENT_COORDINATION = (
    ROOT / "AGENTS.md",
    ROOT / "docs" / "operations" / "coordination" / "README.md",
    ROOT / "docs" / "operations" / "coordination" / "SIGNALS.md",
    ROOT / "docs" / "operations" / "coordination" / "WATCH_MODE.md",
    ROOT / "docs" / "operations" / "coordination" / "CODEX_BOOTSTRAP.md",
    ROOT / "docs" / "operations" / "coordination" / "PROBLEM_LOOP.md",
)


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_current_coordination_uses_canonical_repository_identity():
    violations = []
    for path in CURRENT_COORDINATION:
        text = _text(path)
        if "funggier/cogentnexus" in text.lower() and "funggier/cogentnexus-openclaw" not in text.lower():
            violations.append(str(path.relative_to(ROOT)))
    assert not violations, "stale repository identity in living coordination docs: " + ", ".join(violations)


def test_current_coordination_uses_ready_for_hermes_gate():
    violations = []
    for path in CURRENT_COORDINATION:
        if "READY_FOR_CODEX" in _text(path):
            violations.append(str(path.relative_to(ROOT)))
    assert not violations, "stale READY_FOR_CODEX gate in living coordination docs: " + ", ".join(violations)


def test_current_coordination_does_not_pin_superseded_recovery_branch():
    old_branch = "agent/v0.9.3-recovery-reality-tests"
    violations = []
    for path in CURRENT_COORDINATION:
        if old_branch in _text(path):
            violations.append(str(path.relative_to(ROOT)))
    assert not violations, "superseded coordination branch in living docs: " + ", ".join(violations)


def test_current_coordination_names_hermes_codex_executor_contract():
    combined = "\n".join(_text(path) for path in CURRENT_COORDINATION)
    assert "Hermes/Codex" in combined
    assert "READY_FOR_HERMES" in combined
