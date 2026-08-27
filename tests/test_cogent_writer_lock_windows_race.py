import importlib.util
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "cogentnexus-openclaw" / "scripts" / "cogent.py"
SPEC = importlib.util.spec_from_file_location("cogent_writer_lock_race", SCRIPT)
assert SPEC and SPEC.loader
cogent = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(cogent)


def test_writer_lock_retries_short_transient_permission_error_when_lock_is_absent(tmp_path, monkeypatch):
    lock = tmp_path / "task" / ".lock"
    real_open = cogent.os.open
    calls = 0

    def transient_open(path, flags, *args, **kwargs):
        nonlocal calls
        calls += 1
        if calls == 1:
            raise PermissionError(13, "simulated transient Windows create/delete race", str(path))
        return real_open(path, flags, *args, **kwargs)

    monkeypatch.setattr(cogent.os, "open", transient_open)

    with cogent.writer_lock(lock, timeout=1):
        assert lock.exists()

    assert calls == 2
    assert not lock.exists()


def test_writer_lock_still_fails_closed_on_persistent_permission_error(tmp_path, monkeypatch):
    lock = tmp_path / "task" / ".lock"
    calls = 0

    def denied_open(path, flags, *args, **kwargs):
        nonlocal calls
        calls += 1
        raise PermissionError(13, "simulated persistent denial", str(path))

    monkeypatch.setattr(cogent.os, "open", denied_open)

    with pytest.raises(PermissionError, match="persistent denial"):
        with cogent.writer_lock(lock, timeout=1):
            pass

    assert calls <= 5, "persistent permission denial must not spin until the normal lock timeout"
