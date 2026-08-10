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
- Cross-platform deterministic supervisor with confirmed health probes, verified recovery, cooldowns, and circuit breaking
- Native scheduler templates for Windows Task Scheduler, systemd, launchd, cron, Docker Compose, and Kubernetes
- Fixed or adaptive concurrency admission with one inference lane as the safe default
- Durable context handoff with live OpenClaw token observation, integrity binding, worker leases, generation fencing, and session rotation thresholds
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
    python skills/cogentnexus/scripts/phase3.py self-test

## Quick start

    python skills/cogentnexus/scripts/cogent.py task init --task-id CNX-001 --goal "Produce a verified artifact"
    python skills/cogentnexus/scripts/cogent.py probe all --task-id CNX-001
    python skills/cogentnexus/scripts/cogent.py run --task-id CNX-001 --step compile --command "python -m py_compile artifact.py"
    python skills/cogentnexus/scripts/cogent.py verify run --task-id CNX-001 --exists artifact.py --hash artifact.py
    python skills/cogentnexus/scripts/cogent.py recover plan --task-id CNX-001
    python skills/cogentnexus/scripts/cogent.py capability find "GitHub repository"
    python skills/cogentnexus/scripts/phase3.py supervisor tick
    python skills/cogentnexus/scripts/phase3.py concurrency status
    python skills/cogentnexus/scripts/phase3.py context status --used-tokens 18000 --maximum-tokens 32768
    python skills/cogentnexus/scripts/phase3.py context bind --task-id TASK-1 --session-key SESSION-KEY --next-action "resume smallest pending step"
    python skills/cogentnexus/scripts/phase3.py context monitor --task-id TASK-1 --execute-safe
    python skills/cogentnexus/scripts/phase3.py scheduler render --backend systemd

Runtime task data is stored under .cogent/tasks/<task-id>/ and is intentionally excluded from version control.

## Status

Phase 3 is implemented. Periodic supervision is deterministic and consumes no inference lane. Recovery remains evidence-gated and bounded; permission bypass, dependency installation, deletion, and unapproved external actions are never automatic. Concurrency defaults to one inference lane and scales only within an explicit adaptive ceiling.
