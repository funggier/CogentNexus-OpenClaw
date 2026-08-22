#!/usr/bin/env python3
"""CogentNexus v0.9.3 Ollama-only provider facade.

v0.9.3 intentionally removes LM Studio from the supported provider surface.
The released v0.9.2 modules remain in-tree for upgrade/native-restore compatibility,
but new v0.9.3 control paths never select, start, stop, probe, or advertise LM Studio.
"""
from __future__ import annotations

from typing import Any

import provider as legacy

SUPPORTED_PROVIDERS = ("ollama",)
DEFAULT_ENDPOINTS = {"ollama": legacy.DEFAULT_ENDPOINTS["ollama"]}
MODEL_PROVIDER_PREFIXES = {"ollama": "ollama"}


def normalize_provider(name: str) -> str:
    value = (name or "").strip().lower().replace("-", "")
    if value != "ollama":
        raise ValueError("unsupported provider in CogentNexus v0.9.3; only 'ollama' is supported")
    return "ollama"


def detect(name: str = "ollama") -> dict[str, Any]:
    normalize_provider(name)
    return legacy.detect("ollama")


def probe(name: str = "ollama", timeout: float = 5.0) -> dict[str, Any]:
    normalize_provider(name)
    return legacy.probe("ollama", timeout=timeout)


def inventory(timeout: float = 2.0) -> dict[str, dict[str, Any]]:
    return {"ollama": probe("ollama", timeout=timeout)}


def installed_providers() -> list[str]:
    return ["ollama"] if detect("ollama").get("installed") else []


def start(name: str = "ollama", timeout: float = 30.0) -> dict[str, Any]:
    normalize_provider(name)
    return legacy.start("ollama", timeout=timeout)


def stop(name: str = "ollama", timeout: float = 30.0) -> dict[str, Any]:
    normalize_provider(name)
    return legacy.stop("ollama", timeout=timeout)


def openclaw_executable() -> str | None:
    return legacy.openclaw_executable()


def openclaw_model_status() -> dict[str, Any]:
    return legacy.openclaw_model_status()


def model_provider(model_ref: str | None) -> str | None:
    if not isinstance(model_ref, str) or "/" not in model_ref:
        return None
    prefix = model_ref.split("/", 1)[0].strip().lower()
    return "ollama" if prefix == "ollama" else None
