"""Task-scoped, fail-closed Supervisor quiescence lease."""
from __future__ import annotations

import json
import os
import time
import uuid
from pathlib import Path
from typing import Any


class QuiescenceError(RuntimeError):
    pass


class QuiescenceBusyError(QuiescenceError):
    pass


class QuiescenceTimeoutError(QuiescenceError):
    pass


class QuiescenceOwnerError(QuiescenceError):
    pass


def lease_path(root: Path) -> Path:
    return root / "host" / "supervisor-quiescence.json"


def _read_raw(path: Path) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None
    except (OSError, json.JSONDecodeError) as exc:
        raise QuiescenceError(f"quiescence lease is unreadable: {exc}") from exc
    if not isinstance(value, dict) or value.get("schemaVersion") != 1:
        raise QuiescenceError("quiescence lease has invalid schema")
    return value


def read(root: Path, now: float | None = None) -> dict[str, Any]:
    path = lease_path(root)
    value = _read_raw(path)
    if value is None:
        return {"status": "absent", "path": str(path)}
    current = time.time() if now is None else now
    if float(value.get("expiresAt", 0)) <= current:
        return {"status": "stale", "path": str(path), "lease": value}
    return {"status": "active", "path": str(path), "lease": value, "owner": value.get("owner")}


def _write_exclusive(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = (json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8")
    fd = os.open(str(path), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
    except BaseException:
        try:
            path.unlink()
        except OSError:
            pass
        raise


def acquire(root: Path, owner: str, *, now: float | None = None, ttl: float = 300.0, timeout: float = 0.0, poll: float = 0.025) -> dict[str, Any]:
    if not owner or ttl <= 0 or timeout < 0:
        raise ValueError("owner, positive ttl, and non-negative timeout are required")
    started = time.monotonic()
    current = time.time() if now is None else now
    path = lease_path(root)
    while True:
        try:
            value = {"schemaVersion": 1, "owner": owner, "token": uuid.uuid4().hex, "acquiredAt": current, "expiresAt": current + ttl}
            _write_exclusive(path, value)
            return value
        except FileExistsError:
            existing = read(root, now=current)
            if existing["status"] == "stale":
                stale = existing.get("lease") or {}
                try:
                    current_raw = _read_raw(path)
                    if current_raw != stale:
                        raise QuiescenceBusyError("quiescence lease changed while reclaiming stale owner")
                    path.unlink()
                except FileNotFoundError:
                    continue
                continue
            if time.monotonic() - started >= timeout:
                if timeout == 0:
                    raise QuiescenceBusyError("Supervisor quiescence lease is held by another owner")
                raise QuiescenceTimeoutError("timed out waiting for Supervisor quiescence lease")
            time.sleep(poll)
            if now is None:
                current = time.time()


def release(root: Path, owner: str, *, token: str | None = None, now: float | None = None) -> dict[str, Any]:
    del now
    path = lease_path(root)
    value = _read_raw(path)
    if value is None:
        return {"released": False, "status": "absent", "path": str(path)}
    if value.get("owner") != owner or (token is not None and value.get("token") != token):
        raise QuiescenceOwnerError("quiescence lease owner/token mismatch")
    try:
        path.unlink()
    except FileNotFoundError:
        return {"released": False, "status": "absent", "path": str(path)}
    return {"released": True, "status": "released", "path": str(path), "owner": owner}


def supervisor_is_quiesced(root: Path, now: float | None = None) -> bool:
    return read(root, now=now)["status"] == "active"


def supervisor_quiesced_result(root: Path, now: float | None = None) -> dict[str, Any] | None:
    """Return a state-free Supervisor result while an activation lease is active."""
    current = read(root, now=now)
    if current["status"] != "active":
        return None
    return {
        "result": "quiesced",
        "mode": None,
        "action": "none",
        "quiescence": current,
    }
