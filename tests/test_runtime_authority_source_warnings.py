import warnings
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_AUTHORITY = ROOT / "skills" / "cogentnexus-openclaw" / "scripts" / "runtime_authority.py"


def test_runtime_authority_source_has_no_invalid_escape_warning():
    source = RUNTIME_AUTHORITY.read_text(encoding="utf-8")

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        compile(source, str(RUNTIME_AUTHORITY), "exec")

    invalid_escape = [
        warning
        for warning in caught
        if "invalid escape sequence" in str(warning.message)
    ]
    assert not invalid_escape, [str(warning.message) for warning in invalid_escape]
