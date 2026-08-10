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
- Portable, maintenance-fenced lifecycle launchers for Windows, Linux, and macOS
- Fixed or adaptive concurrency admission with one inference lane as the safe default
- Durable context handoff with live OpenClaw token observation, integrity binding, worker leases, generation fencing, and session rotation thresholds
- Verified workflow DAGs with command/Ollama executors, deterministic validators, bounded retries, and artifact hashes
- Always-on workflow discovery and detached controller resumption from the native periodic supervisor
- Automatic context-pressure rotation for bound durable tasks through a clean TaskFlow worker session
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
    python skills/cogentnexus/scripts/workflow.py self-test

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
    python skills/cogentnexus/scripts/phase3.py context rotations --task-id TASK-1
    python skills/cogentnexus/scripts/phase3.py scheduler render --backend systemd
    python skills/cogentnexus/scripts/workflow.py validate workflow-manifest.json
    python skills/cogentnexus/scripts/workflow.py --root . init workflow-manifest.json
    python skills/cogentnexus/scripts/workflow.py --root . supervise
    python skills/cogentnexus/scripts/workflow.py --root . supervise --execute

## Start and stop safely

Portable wrappers are available in `skills/cogentnexus/templates/lifecycle/`:

- Windows: `start-cogentnexus.cmd` and `stop-cogentnexus.cmd`
- Linux/macOS: `start-cogentnexus.sh` and `stop-cogentnexus.sh`

Run a wrapper from the workspace whose runtime data should be stored under `.cogent`, or set `COGENTNEXUS_ROOT` to an absolute runtime-data directory. On Linux/macOS, make the shell wrappers executable once with `chmod +x`.

The stop wrapper enables maintenance mode before stopping OpenClaw and the local provider, preventing the supervisor from immediately restarting them. The start wrapper verifies service health before clearing maintenance mode and is safe to invoke when services are already healthy.

Runtime task data is stored under .cogent/tasks/<task-id>/ and is intentionally excluded from version control.

## Status

Phase 5 always-on resumption is implemented. Periodic supervision remains deterministic and consumes no inference lane; it discovers resumable workflows and launches separately fenced controllers that continue from durable evidence. Recovery remains evidence-gated and bounded; permission bypass, dependency installation, deletion, and unapproved external actions are never automatic. Concurrency defaults to one inference lane and scales only within an explicit adaptive ceiling.
