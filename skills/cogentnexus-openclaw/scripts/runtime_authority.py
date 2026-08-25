#!/usr/bin/env python3
"""CogentNexus-OpenClaw owned-runtime authority.

Establishes one stable, product-owned Python runtime under the CogentNexus
application-data boundary so durable launcher/startup execution never depends
on an ambient PATH Python or a registration-time executor venv.

Contract (Task CNX-20260825-064):
- ``app_data_root(env)`` derives the exact product root from the LOCALAPPDATA
  base: ``<LOCALAPPDATA>\\CogentNexus-OpenClaw``.
- ``runtime_root_from_application_data(root)`` accepts an ALREADY-EXACT product
  root and appends only ``runtime\\python``. The two forms must never be mixed;
  no API/CLI argument ambiguously means both.
- The system/base Python remains an installation prerequisite; this module
  provisions a product-owned virtual environment from a verified non-venv base
  interpreter. It is deliberately NOT claimed to be fully standalone.
- Provisioning fails closed; callers never fall back to arbitrary
  ``sys.executable`` for durable execution authority.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

MANIFEST_NAME = "runtime-manifest.json"
RUNTIME_DIR_NAME = "python"
PRODUCT_DIR_NAME = "CogentNexus-OpenClaw"
SCHEMA_VERSION = 1


class RuntimeProvisioningError(RuntimeError):
    """Raised when the owned runtime cannot be provisioned or verified."""


def creation_flags() -> int:
    return getattr(subprocess, "CREATE_NO_WINDOW", 0) if os.name == "nt" else 0


def app_data_root(env: dict[str, str] | None = None) -> Path:
    """Derive the exact CogentNexus product root from a LOCALAPPDATA base."""
    values = env if env is not None else dict(os.environ)
    local = values.get("LOCALAPPDATA")
    if not local:
        raise RuntimeProvisioningError("LOCALAPPDATA is not set; cannot resolve CogentNexus application-data boundary")
    return Path(local) / PRODUCT_DIR_NAME


def runtime_root_from_application_data(application_data_root: Path | str) -> Path:
    """Return the runtime root under an EXACT product application-data root."""
    return Path(application_data_root) / "runtime" / RUNTIME_DIR_NAME


def runtime_root(env: dict[str, str] | None = None) -> Path:
    return runtime_root_from_application_data(app_data_root(env))


def _interpreter_paths(runtime: Path) -> tuple[Path, Path]:
    scripts = runtime / ("Scripts" if os.name == "nt" else "bin")
    if os.name == "nt":
        return scripts / "python.exe", scripts / "pythonw.exe"
    return scripts / "python3", scripts / "python3"


def _probe_foreground(interpreter: Path, timeout: int = 60) -> str:
    if not interpreter.is_file():
        raise RuntimeProvisioningError(f"owned foreground interpreter missing: {interpreter}")
    result = subprocess.run(
        [str(interpreter), "-c", "import json,sys;print(json.dumps({'version':sys.version}))"],
        capture_output=True, text=True, timeout=timeout, creationflags=creation_flags(),
    )
    if result.returncode != 0:
        raise RuntimeProvisioningError(f"owned foreground probe failed ({result.returncode}): {interpreter}")
    return result.stdout.strip()


def _probe_background(interpreter: Path, sentinel_dir: Path, timeout: int = 60) -> None:
    """Exit-only/sentinel probe that assumes no console stdio exists."""
    if not interpreter.is_file():
        raise RuntimeProvisioningError(f"owned background interpreter missing: {interpreter}")
    sentinel = sentinel_dir / "cnx-bg-sentinel.txt"
    try:
        result = subprocess.run(
            [str(interpreter), "-c", f"open(r'{sentinel}','w').write('ok')"],
            capture_output=True, text=True, timeout=timeout,
            creationflags=creation_flags() | getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        if result.returncode != 0:
            raise RuntimeProvisioningError(
                f"owned background interpreter probe failed ({result.returncode}): {interpreter}: {result.stderr.strip()[:200]}"
            )
        if not sentinel.exists():
            raise RuntimeProvisioningError(f"owned background interpreter did not execute probe: {interpreter}")
    finally:
        try:
            sentinel.unlink(missing_ok=True)
        except Exception:
            pass


def resolve_base_interpreter(candidate: Path | str | None = None) -> Path:
    """Resolve a verified NON-venv base interpreter; never accept a venv path."""
    chosen: Path | None = Path(candidate).resolve() if candidate else None
    if chosen is None:
        base_exec = getattr(sys, "_base_executable", "") or getattr(sys, "base_prefix", "")
        chosen = Path(base_exec) if base_exec else Path(sys.executable)
        exe_name = "python.exe" if os.name == "nt" else "python3"
        guess = (Path(base_exec) / exe_name) if base_exec and not Path(base_exec).suffix == ".exe" else Path(chosen)
        chosen = guess if guess.exists() else Path(sys.executable)

    def venv_state(interpreter: Path) -> bool:
        probe = subprocess.run(
            [str(interpreter), "-c",
             "import json,sys;print(json.dumps({'is_venv': sys.prefix != getattr(sys,'base_prefix',sys.prefix),"
             "'base_exec': getattr(sys,'_base_executable','') or ''}))"],
            capture_output=True, text=True, timeout=30, creationflags=creation_flags(),
        )
        if probe.returncode != 0:
            raise RuntimeProvisioningError(f"bootstrap interpreter probe failed: {interpreter}")
        return json.loads(probe.stdout.strip())

    info = venv_state(chosen)
    if info.get("is_venv"):
        base_exec = info.get("base_exec") or ""
        if base_exec and Path(base_exec).exists() and Path(base_exec).resolve() != chosen:
            return resolve_base_interpreter(Path(base_exec))
        raise RuntimeProvisioningError(
            f"bootstrap Python '{chosen}' is a venv without a resolvable non-venv base interpreter; "
            "install a system Python before installing CogentNexus-OpenClaw"
        )
    return chosen


def provisioned_manifest(application_data_root: Path | str | None = None) -> dict[str, Any] | None:
    path = runtime_root_from_application_data(application_data_root or app_data_root()) / MANIFEST_NAME
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        return value if isinstance(value, dict) else None
    except Exception:
        return None


def validate_runtime(manifest: dict[str, Any] | None, application_data_root: Path | str | None = None) -> bool:
    """Ancestry-based manifest validation against the EXACT product root.

    Uses resolved-path parent relationships instead of string prefixes so a
    sibling such as ``CogentNexus-OpenClaw-evil`` cannot validate.
    """
    if not isinstance(manifest, dict):
        return False
    expected_app_root = Path(application_data_root).resolve() if application_data_root else app_data_root().resolve()
    expected_runtime = (expected_app_root / "runtime" / RUNTIME_DIR_NAME)
    try:
        declared_runtime = Path(manifest.get("runtimeRoot", "")).resolve()
    except Exception:
        return False
    if declared_runtime != expected_runtime.resolve():
        return False
    for key in ("foregroundInterpreter", "backgroundInterpreter"):
        value = manifest.get(key)
        if not isinstance(value, str) or not value:
            return False
        interp = Path(value)
        try:
            resolved = interp.resolve()
        except Exception:
            return False
        # ancestry check: <app-root>/runtime/python/<Scripts>/<exe>
        try:
            resolved.relative_to(expected_runtime.resolve())
        except ValueError:
            return False
        if not resolved.is_file():
            return False
    return True


def ensure_runtime(
    application_data_root: Path | str | None = None,
    bootstrap: Path | str | None = None,
    force: bool = False,
    env: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Provision/verify the owned runtime and return its manifest.

    ``application_data_root`` accepts either an exact product root or, when
    only ``env`` is given, derives it from LOCALAPPDATA — never both layered.
    """
    root = (
        runtime_root_from_application_data(application_data_root)
        if application_data_root
        else runtime_root(env)
    )
    exact_app_root = root.parents[1]
    existing = provisioned_manifest(exact_app_root)
    if not force and validate_runtime(existing, exact_app_root):
        _probe_foreground(Path(existing["foregroundInterpreter"]))
        return existing

    base = resolve_base_interpreter(bootstrap)
    root.parent.mkdir(parents=True, exist_ok=True)
    create = subprocess.run(
        [str(base), "-m", "venv", str(root)],
        capture_output=True, text=True, timeout=600, creationflags=creation_flags(),
    )
    if create.returncode != 0:
        raise RuntimeProvisioningError(
            f"failed to provision CogentNexus-owned runtime at {root}: {create.stderr.strip()[:400]}"
        )

    foreground, background = _interpreter_paths(root)
    fg_probe = _probe_foreground(foreground)
    _probe_background(background, sentinel_dir=root.parent)

    version = ""
    try:
        version = json.loads(fg_probe).get("version", "").split(" ")[0]
    except Exception:
        pass

    manifest = {
        "schemaVersion": SCHEMA_VERSION,
        "runtimeRoot": str(root),
        "applicationDataRoot": str(exact_app_root),
        "foregroundInterpreter": str(foreground),
        "backgroundInterpreter": str(background),
        "baseInterpreter": str(base),
        "pythonVersion": version,
        "platform": sys.platform,
    }
    (root / MANIFEST_NAME).write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    if not validate_runtime(manifest, exact_app_root):
        raise RuntimeProvisioningError("owned runtime manifest failed validation immediately after provisioning")
    return manifest


def require_background_interpreter(application_data_root: Path | str | None = None) -> Path:
    """Return ONLY the validated product-owned background interpreter, or fail closed."""
    manifest = provisioned_manifest(application_data_root or app_data_root())
    if not validate_runtime(manifest, application_data_root or app_data_root()):
        raise RuntimeProvisioningError(
            "CogentNexus-owned runtime is missing or invalid; run the installer to provision it"
        )
    return Path(manifest["backgroundInterpreter"])


def require_foreground_interpreter(application_data_root: Path | str | None = None) -> Path:
    """Return ONLY the validated product-owned foreground interpreter, or fail closed."""
    manifest = provisioned_manifest(application_data_root or app_data_root())
    if not validate_runtime(manifest, application_data_root or app_data_root()):
        raise RuntimeProvisioningError(
            "CogentNexus-owned runtime is missing or invalid; run the installer to provision it"
        )
    return Path(manifest["foregroundInterpreter"])


def _cli(argv: list[str]) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="CogentNexus owned-runtime authority")
    sub = parser.add_subparsers(dest="command", required=True)
    ensure = sub.add_parser("ensure-runtime", help="provision/verify the owned runtime")
    ensure.add_argument("--application-data-root", default=None,
                        help="EXACT CogentNexus product application-data root")
    ensure.add_argument("--force", action="store_true")
    show = sub.add_parser("show", help="print current runtime manifest as JSON")
    show.add_argument("--application-data-root", default=None)
    args = parser.parse_args(argv)
    app_root = Path(args.application_data_root) if args.application_data_root else None
    try:
        if args.command == "ensure-runtime":
            manifest = ensure_runtime(application_data_root=app_root, force=args.force)
        else:
            manifest = provisioned_manifest(app_root or app_data_root())
            if manifest is None:
                raise RuntimeProvisioningError("owned runtime is not provisioned")
        print(json.dumps(manifest, indent=2))
        return 0
    except RuntimeProvisioningError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(_cli(sys.argv[1:]))
