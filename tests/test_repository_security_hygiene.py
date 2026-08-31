from __future__ import annotations

import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

_GENERATED_DIRS = {
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "coverage",
    "htmlcov",
    "build",
    "dist",
}
_GENERATED_SUFFIXES = {
    ".log",
    ".sqlite",
    ".sqlite3",
    ".db",
    ".tmp",
    ".temp",
    ".bak",
    ".backup",
    ".old",
    ".orig",
}
_PRIVATE_KEY_RE = re.compile(
    r"-----BEGIN (?:RSA |EC |DSA |OPENSSH )?" + r"PRIVATE KEY-----"
)
_OPENAI_KEY_RE = re.compile(r"\b" + r"sk-" + r"[A-Za-z0-9_-]{20,}\b")
_BEARER_RE = re.compile(r"(?i)\bBearer\s+([A-Za-z0-9._~+/=-]{20,})")
_AUTH_RE = re.compile(
    r"(?i)Authorization\s*:\s*(?:Bearer|Basic)\s+([A-Za-z0-9._~+/=-]{20,})"
)
_ASSIGNMENT_RE = re.compile(
    r"(?i)\b(?:dashboard[_-]?)?(?:token|password)\s*[:=]\s*[\"']"
    r"([A-Za-z0-9._~+/=-]{20,})[\"']"
)
_PLACEHOLDER_MARKERS = (
    "placeholder",
    "example",
    "dummy",
    "fake",
    "redacted",
    "not-a-real",
    "not_real",
    "test-token",
    "test_token",
    "changeme",
    "xxxxxxxx",
)


def _tracked_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
    )
    return [ROOT / Path(item.decode("utf-8")) for item in result.stdout.split(b"\0") if item]


def _is_placeholder(value: str) -> bool:
    lowered = value.lower()
    return any(marker in lowered for marker in _PLACEHOLDER_MARKERS)


def _text_lines(path: Path) -> list[str]:
    data = path.read_bytes()
    if b"\0" in data:
        return []
    try:
        return data.decode("utf-8").splitlines()
    except UnicodeDecodeError:
        return []


def test_tracked_repository_has_no_generated_or_runtime_residue() -> None:
    offenders: list[str] = []
    for path in _tracked_files():
        relative = path.relative_to(ROOT)
        parts = set(relative.parts)
        if parts & _GENERATED_DIRS or relative.suffix.lower() in _GENERATED_SUFFIXES:
            offenders.append(relative.as_posix())
        if "secrets" in parts or "credentials" in parts:
            offenders.append(relative.as_posix())
        if len(relative.parts) >= 2 and tuple(relative.parts[:2]) in {
            ("config", "private"),
            ("config", "local"),
        }:
            offenders.append(relative.as_posix())

    assert not offenders, "tracked generated/runtime residue: " + ", ".join(sorted(set(offenders)))


def test_tracked_repository_has_no_high_confidence_literal_credentials() -> None:
    findings: list[str] = []
    patterns = (
        ("private-key-header", _PRIVATE_KEY_RE, False),
        ("openai-key", _OPENAI_KEY_RE, False),
        ("authorization", _AUTH_RE, True),
        ("bearer-token", _BEARER_RE, True),
        ("token-or-password-assignment", _ASSIGNMENT_RE, True),
    )

    for path in _tracked_files():
        relative = path.relative_to(ROOT).as_posix()
        for line_number, line in enumerate(_text_lines(path), start=1):
            for label, pattern, has_capture in patterns:
                for match in pattern.finditer(line):
                    candidate = match.group(1) if has_capture else match.group(0)
                    if _is_placeholder(candidate) or _is_placeholder(line):
                        continue
                    findings.append(f"{relative}:{line_number}:{label}")

    assert not findings, "high-confidence literal credential candidates: " + ", ".join(findings)
