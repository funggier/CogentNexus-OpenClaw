# CogentNexus v0.9.3 — Ollama-only provider decision

## Decision

Starting with v0.9.3, CogentNexus supports **Ollama only** as its managed local inference provider.

The released v0.9.2 remains immutable. Its historical LM Studio compatibility code may remain in the v0.9.2 tag and as legacy upgrade/native-restore implementation details, but v0.9.3 operator-facing control paths do not select, start, stop, probe, advertise, or test LM Studio.

## Operational consequences

- `install.ps1` and `install.sh` default to Ollama and reject other providers.
- `cnx_v093.py` forces provider-bearing lifecycle transitions to Ollama.
- `provider_v093.py` exposes only Ollama.
- LM Studio installations are left untouched on user machines.
- An upgrade from an already-managed v0.9.2 deployment first uses the old launcher to enter PASSTHROUGH/native state before v0.9.3 files are installed.
- Recovery Reality testing targets OpenClaw Gateway + Ollama only.

## Motivation

The provider-neutral experiment established that the important failure/recovery classes are largely shared while the LM Studio path adds additional resident memory pressure, event-adapter ownership, route compatibility fields, process-lifecycle behavior, and test surface. v0.9.3 therefore trades provider breadth for a smaller and more deterministic continuity boundary.

## Non-goals

- Do not modify the published `v0.9.2` tag/release.
- Do not uninstall LM Studio from a user's machine.
- Do not make elapsed time the recovery authority.
- Do not discard v0.9.2 native-restore knowledge required to safely migrate an older managed deployment.
