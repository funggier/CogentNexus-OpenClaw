import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "cogentnexus-openclaw" / "scripts"
CNXCLAW = SCRIPTS / "cnxclaw_v093.py"
HOST = SCRIPTS / "host.py"
COMMAND_RE = re.compile(r"(?im)^\s*(?:\.\\)?cnxclaw\.cmd\s+([a-z][a-z0-9-]*)\b")
HELP_COMMAND_RE = re.compile(r"(?im)^\s*cnxclaw\.cmd\s+([a-z][a-z0-9-]*)\b")


def current_docs():
    paths = [ROOT / "README.md"]
    paths.extend(sorted((ROOT / "docs").glob("*.md")))
    paths.extend(
        ROOT / "docs" / "operations" / name
        for name in ("STATUS.md", "ROADMAP.md", "DECISIONS.md")
    )
    return paths


def run_help(script: Path) -> str:
    result = subprocess.run(
        [sys.executable, str(script), "--help"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, f"{script} --help failed: {result.stderr or result.stdout}"
    return result.stdout


def current_cli_top_level_commands():
    facade_help = run_help(CNXCLAW)
    facade_commands = {match.group(1).lower() for match in HELP_COMMAND_RE.finditer(facade_help)}

    host_help = run_help(HOST)
    choices = re.search(r"\{([a-z0-9,-]+)\}", host_help, flags=re.IGNORECASE)
    assert choices, f"could not derive delegated Host commands from help:\n{host_help}"
    host_commands = {item.lower() for item in choices.group(1).split(",") if item}

    commands = facade_commands | host_commands
    assert {"status", "check", "provider", "start", "stop", "restart", "enable", "disable", "reset", "uninstall"} <= commands
    assert {"gateway", "supervisor", "ticket", "session", "policy"} <= commands
    return commands


def test_current_user_docs_only_teach_supported_cnxclaw_top_level_commands():
    supported = current_cli_top_level_commands()
    examples = []

    for path in current_docs():
        text = path.read_text(encoding="utf-8")
        for match in COMMAND_RE.finditer(text):
            examples.append((path.relative_to(ROOT).as_posix(), match.group(1).lower(), match.group(0).strip()))

    assert examples, "no current cnxclaw.cmd command examples were discovered"
    invalid = [example for example in examples if example[1] not in supported]
    assert not invalid, f"current docs contain unsupported cnxclaw.cmd top-level commands: {invalid}"
