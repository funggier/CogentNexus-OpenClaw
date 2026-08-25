#!/usr/bin/env python3
"""CogentNexus-OpenClaw owned-runtime authority.

Establishes one stable, product-owned Python runtime under the CogentNexus
application-data boundary so durable launcher/startup execution never depends
on an ambient PATH Python or a registration-time executor venv.

Design notes (Task CNX-20260825-063):
- The system/base Python remains an installation prerequisite; this module
  deliberately provisions a product-owned virtual environment from a verified
  non-venv base interpreter and treats that environment as the product's
  runtime dependency. It is NOT claimed to be fully standalone.
- Provisioning fails closed: if no valid base interpreter can be verified,
  callers must surface an actionable error instead of falling back to an
  arbitrary ``sys.executable``.
- A small non-secret manifest records interpreter provenance/version and the
  exact owned runtime paths so install-over can validate or recreate it.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import sysconfig
from pathlib import Path
from typing import Any

MANIFEST_NAME = "runtime-manifest.json"
RUNTIME_DIR_NAME = "python"
SCHEMA_VERSION = 1


class RuntimeProvisioningError(RuntimeError):
    """Raised when the owned runtime cannot be provisioned or verified."""


def creation_flags() -> int:
    return getattr(subprocess, "CREATE_NO_WINDOW", 0) if os.name == "nt" else 0


def app_data_root(env: dict[str, str] | None = None) -> Path:
    values = env if env is not None else dict(os.environ)
    local = values.get("LOCALAPPDATA")
    if not local:
        raise RuntimeProvisioningError("LOCALAPPDATA is not set; cannot resolve CogentNexus application-data boundary")
    return Path(local) / "CogentNexus-OpenClaw"


def runtime_root(env: dict[str, str] | None = None) -> Path:
    return app_data_root(env) / "runtime" / RUNTIME_DIR_NAME


def _venv_site_packages(runtime: Path, base: Path) -> Path:
    scripts = "Scripts" if os.name == "nt" else "bin"
    suffix = ""
    if os.name != "nt":
        version = f"{sys.version_info.major}.{sys.version_info.minor}"
        suffix = f"-cpython-{version}"
    return runtime / "lib" if os.name == "nt" else runtime / "lib"


def _interpreter_paths(runtime: Path) -> tuple[Path, Path]:
    scripts = runtime / ("Scripts" if os.name == "nt" else "bin")
    foreground = scripts / ("python.exe" if os.name == "nt" else "python3")
    background = scripts / ("pythonw.exe",) if os.name == "nt" else (scripts / "python3",)
    return foreground, background


def _probe(interpreter: Path, timeout: int = 30) -> str:
    if not interpreter.exists():
        raise RuntimeProvisioningError(f"owned interpreter missing: {interpreter}")
    result = subprocess.run(
        [str(interpreter), "-c", "import json,sys;print(json.dumps({'version':sys.version,'base':getattr(sys,'base_prefix','')}))"],
        capture_output=True,
        text=True,
        timeout=timeout,
        creationflags=creation_flags(),
    )
    if result.returncode != 0:
        raise RuntimeProvisioningError(f"owned interpreter probe failed ({result.returncode}): {interpreter}")
    return result.stdout.strip()


def resolve_base_interpreter(candidate: Path | None = None) -> Path:
    """Resolve a valid NON-venv base interpreter.

    Never accepts a venv interpreter as durable authority. When invoked inside
    a venv, resolves the real base executable via standard metadata.
    """
    chosen: Path | None = candidate
    if chosen is None:
        base_exec = getattr(sys, "_base_executable", None) or getattr(sys, "base_prefix", None)
        if base_exec:
            prefix = Path(base_exec)
            chosen = prefix / ("python.exe" if os.name == "nt" else "bin/python3")
            if not chosen.exists():
                chosen = Path(sys.executable)
        else:
            chosen = Path(sys.executable)
    chosen = Path(chosen).resolve()
    # Reject venv paths: a venv python has pyvenv.cfg beside its parent.
    probe = subprocess.run(
        [str(chosen), "-c",
         "import json,sys,os;"
         "print(json.dumps({'is_venv': sys.prefix != getattr(sys,'base_prefix',sys.prefix)}))"],
        capture_output=True, text=True, timeout=30, creationflags=creation_flags(),
    )
    if probe.returncode != 0:
        raise RuntimeProvisioningError(f"bootstrap interpreter probe failed: {chosen}")
    try:
        info = json.loads(probe.stdout.strip())
    except json.JSONDecodeError as error:
        raise RuntimeProvisioningError(f"unreadable interpreter probe output: {chosen}") from error
    if info.get("is_venv"):
        base_exec = getattr(sys, "_base_executable", "")
        # Ask the venv itself for its base executable.
        deeper = subprocess.run(
            [str(chosen), "-c",
             "import json,sys;print(json.dumps(getattr(sys,'_base_executable','') or ''))"],
            capture_output=True, text=True, timeout=30, creationflags=creation_flags(),
        )
        if deeper.returncode == 0:
            value = deeper.stdout.strip().strip('"')
            if value and Path(value).exists() and Path(value).resolve() != chosen:
                return resolve_base_interpreter(Path(value))
        base_hint = Path(base_exec) if base_exec else None
        if base_hint and base_hint.exists():
            resolved = base_hint.resolve()
            if resolved != chosen:
                return resolve_base_interpreter(resolved)
        raise RuntimeProvisioningError(
            "bootstrap Python is a venv without resolvable base interpreter; "
            "install a system Python before installing CogentNexus-OpenClaw"
        )
    return chosen


def provisioned_manifest(root: Path | None = None, env: dict[str, str] | None = None) -> dict[str, Any] | None:
    path = (root or runtime_root(env)) / MANIFEST_NAME
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        return value if isinstance(value, dict) else None
    except Exception:
        return None


def validate_runtime(manifest: dict[str, Any] | None, env: dict[str, str] | None = None) -> bool:
    if not isinstance(manifest, dict):
        return False
    expected_root = str(runtime_root(env))
    if manifest.get("runtimeRoot", "").lower() != expected_root.lower():
        return False
    for key in ("foregroundInterpreter", "backgroundInterpreter"):
        value = manifest.get(key)
        if not isinstance(value, str) or not value:
            return False
        if not str(value).lower().startswith(expected_root.lower()):
            return False
        if not Path(value).exists():
            return False
    return True


def ensure_runtime(bootstrap: Path | None = None, env: dict[str, str] | None = None, force: bool = False) -> dict[str, Any]:
    """Provision/verify the CogentNexus-owned runtime and return its manifest."""
    root = runtime_root(env)
    existing = provisioned_manifest(root, env)
    if not force and validate_runtime(existing, env):
        _probe(Path(existing["backgroundInterpreter"]))
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
    fg_probe = _probe(foreground)
    if os.name == "nt":
        bg_probe = _probe(background)
    else:
        bg_probe = fg_probe
    try:
        version = json.loads(fg_probe).get("version", "")
    except Exception:
        version = ""

    manifest = {
        "schemaVersion": SCHEMA_VERSION,
        "runtimeRoot": str(root),
        "foregroundInterpreter": str(foreground),
        "backgroundInterpreter": str(background),
        "baseInterpreter": str(base),
        "pythonVersion": version.split(" ")[0],
        "platform": sys.platform,
    }
    (root / MANIFEST_NAME).write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    if not validate_runtime(manifest, env):
        raise RuntimeProvisioningError("owned runtime manifest failed validation immediately after provisioning")
    return manifest


def require_background_interpreter(env: dict[str, str] | None = None) -> Path:
    """Return the product-owned background interpreter or fail closed."""
    manifest = provisioned_manifest(runtime_root(env), env)
    if not validate_runtime(manifest, env):
        raise RuntimeProvisioningError(
            "CogentNexus-owned runtime is missing or invalid; run the installer to provision it"
        )
    return Path(manifest["backgroundInterpreter"])


def require_foreground_interpreter(env: dict[str, str] | None = None) -> Path:
    """Return the product-owned foreground interpreter or fail closed."""
    manifest = provisioned_manifest(runtime_root(env), env)
    if not validate_runtime(manifest, env):
        raise RuntimeProvisioningError(
            "CogentNexus-owned runtime is missing or invalid; run the installer to provision it"
        )
    return Path(manifest["foregroundInterpreter"])


def _cli(argv: list[str]) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="CogentNexus owned-runtime authority")
    sub = parser.add_subparsers(dest="command", required=True)
    ensure = sub.add_parser("ensure-runtime", help="provision/verify the owned runtime")
    ensure.add_argument("--app-data", default=None, help="CogentNexus application-data root override")
    ensure.add_argument("--force", action="store_true")
    show = sub.add_parser("show", help="print current runtime manifest as JSON")
    show.add_argument("--app-data", default=None)
    args = parser.parse_args(argv)
    env = {"LOCALAPPDATA": args.app_data} if args.app_data else None
    try:
        if args.command == "ensure-runtime":
            manifest = ensure_runtime(env=env, force=args.force)
        else:
            manifest = provisioned_manifest(runtime_root(env), env)
            if manifest is None:
                raise RuntimeProvisioningError("owned runtime is not provisioned")
        print(json.dumps(manifest, indent=2))
        return 0
    except RuntimeProvisioningError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(_cli(sys.argv[1:]))
