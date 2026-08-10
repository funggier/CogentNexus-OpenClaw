# CogentNexus

CogentNexus is an evidence-backed cognitive runtime toolkit for OpenClaw. It keeps durable task state outside the model, records an append-only execution ledger, probes the runtime environment, and rejects completion when deterministic verification evidence is missing or stale.

## Current capabilities

- Atomic, revisioned task state with checkpoint, resume, commit, and rollback
- System and workspace probes
- Bounded command execution with ACTION, OBSERVATION, and FAILURE events
- Verification bound to state revision and artifact SHA-256
- Completion rejection after artifact tampering
- Deterministic file and directory artifact manifests
- Cross-process writer locking and prepared-transaction recovery
- Failure classification and dry-run recovery planning
- Safe internal recovery adaptation with retry budgets and circuit breaking
- Machine-readable runtime, executable, and OpenClaw skill capability registry
- Minimal ledger records without chain-of-thought

## Layout

    skills/
    └── cogentnexus/
        ├── SKILL.md
        ├── assets/
        ├── references/
        └── scripts/

The nested layout preserves the OpenClaw workspace contract and lets the runtime locate its workspace root deterministically.

## Validate

Requires Python 3.10 or newer and PyYAML.

    python -m pip install -r requirements-dev.txt
    python skills/cogentnexus/scripts/validate.py --workspace-singleton
    python skills/cogentnexus/scripts/cogent.py self-test

## Quick start

    python skills/cogentnexus/scripts/cogent.py task init --task-id CNX-001 --goal "Produce a verified artifact"
    python skills/cogentnexus/scripts/cogent.py probe all --task-id CNX-001
    python skills/cogentnexus/scripts/cogent.py run --task-id CNX-001 --step compile --command "python -m py_compile artifact.py"
    python skills/cogentnexus/scripts/cogent.py verify run --task-id CNX-001 --exists artifact.py --hash artifact.py
    python skills/cogentnexus/scripts/cogent.py recover plan --task-id CNX-001
    python skills/cogentnexus/scripts/cogent.py capability find "GitHub repository"

Runtime task data is stored under .cogent/tasks/<task-id>/ and is intentionally excluded from version control.

## Status

Phase 2 is implemented. Recovery remains dry-run by default and safe apply is limited to reversible internal state adaptations; permission bypass, dependency installation, deletion, and external actions are never automatic.
