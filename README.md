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
- Verified Gateway auto-recovery after an unplanned stop, using connectivity evidence rather than the OpenClaw CLI exit code alone
- Bounded startup readiness polling so normal Gateway warm-up completes with one `lifecycle start` command
- Native scheduler templates for Windows Task Scheduler, systemd, launchd, cron, Docker Compose, and Kubernetes
- Portable, maintenance-fenced lifecycle launchers for Windows, Linux, and macOS
- Fixed or adaptive concurrency admission with one inference lane as the safe default
- Durable context handoff with live OpenClaw token observation, integrity binding, worker leases, generation fencing, and session rotation thresholds
- Verified workflow DAGs with command/Ollama executors, deterministic validators, bounded retries, and artifact hashes
- Always-on workflow discovery and detached controller resumption from the native periodic supervisor
- Automatic context-pressure rotation for bound durable tasks through a clean TaskFlow worker session
- Pre-inference admission of explicit durable requests into owner-bound, checkpointed component workflows
- Domain-aware durable compilation for software systems, EA/trading systems, file operations, analysis, fiction, design, translation, and general work
- Arbitrary named-artifact generation with deterministic existence, size, encoding, and format/syntax validation
- Idempotent workflow intake and deterministic component assembly before verified owner continuation
- Minimal ledger records without chain-of-thought

## Optional background startup

CogentNexus can run its recovery supervisor silently in the background. The
choice is persisted and preserved across updates:

```bash
python skills/cogentnexus/scripts/startup.py status
python skills/cogentnexus/scripts/startup.py enable
python skills/cogentnexus/scripts/startup.py disable
python skills/cogentnexus/scripts/startup.py ensure
```

On Windows, the enabled supervisor uses `pythonw.exe` and a hidden Scheduled
Task to avoid console-window flashes. Disabling startup removes only the
automatic trigger; durable state and manual lifecycle startup remain available.

## Layout

    skills/
    └── cogentnexus/
        ├── SKILL.md
        ├── assets/
        ├── references/
        └── scripts/

The nested layout preserves the OpenClaw workspace contract and lets the runtime locate its workspace root deterministically.

## Installation

Automated installers copy the skill, validate it, build and link the OpenClaw
plugin, restart Gateway, and verify runtime health.

Windows PowerShell:

    .\scripts\install.ps1

Linux or macOS:

    chmod +x scripts/install.sh
    ./scripts/install.sh

See [the installation guide](docs/INSTALL.md) for prerequisites, workspace
selection, manual installation, updating, and troubleshooting.

For stable installations, use a versioned archive from
[GitHub Releases](https://github.com/funggier/cogentnexus/releases) and verify
it against the published `SHA256SUMS.txt` before running the installer.

See the [v0.2.1 release notes](docs/releases/v0.2.1.md) for the problems fixed,
behavior changes, verification evidence, and remaining context-limit caveat.

## Validate

Requires Python 3.10 or newer and PyYAML.

    python -m pip install -r requirements-dev.txt
    python skills/cogentnexus/scripts/validate.py --workspace-singleton
    python skills/cogentnexus/scripts/cogent.py self-test
    python skills/cogentnexus/scripts/runtime.py self-test
    python skills/cogentnexus/scripts/workflow.py self-test

## Benchmarks

[`benchmarks/single-ai-hybrid-e2e`](benchmarks/single-ai-hybrid-e2e) contains a
reusable end-to-end task for comparing a single model with and without
CogentNexus. It includes the model prompt, an independent root-gate validator,
and a Thai-language testing guide with fairness and reporting rules.

## Quick start

    python skills/cogentnexus/scripts/cogent.py task init --task-id CNX-001 --goal "Produce a verified artifact"
    python skills/cogentnexus/scripts/cogent.py probe all --task-id CNX-001
    python skills/cogentnexus/scripts/cogent.py run --task-id CNX-001 --step compile --command "python -m py_compile artifact.py"
    python skills/cogentnexus/scripts/cogent.py verify run --task-id CNX-001 --exists artifact.py --hash artifact.py
    python skills/cogentnexus/scripts/cogent.py recover plan --task-id CNX-001
    python skills/cogentnexus/scripts/cogent.py capability find "GitHub repository"
    python skills/cogentnexus/scripts/runtime.py supervisor tick
    python skills/cogentnexus/scripts/runtime.py concurrency status
    python skills/cogentnexus/scripts/runtime.py context status --used-tokens 18000 --maximum-tokens 32768
    python skills/cogentnexus/scripts/runtime.py context bind --task-id TASK-1 --session-key SESSION-KEY --next-action "resume smallest pending step"
    python skills/cogentnexus/scripts/runtime.py context monitor --task-id TASK-1 --execute-safe
    python skills/cogentnexus/scripts/runtime.py context rotations --task-id TASK-1
    python skills/cogentnexus/scripts/runtime.py scheduler render --backend systemd
    python skills/cogentnexus/scripts/workflow.py validate workflow-manifest.json
    python skills/cogentnexus/scripts/workflow.py --root . init workflow-manifest.json --operator-unbound --operator-reason "operator-managed workflow"
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

Phase 4 verified workflows and Phase 5 always-on resumption are implemented. Periodic supervision remains deterministic and consumes no inference lane; it discovers resumable workflows and launches separately fenced controllers that continue from durable evidence. Command child PIDs are fenced independently from controller PIDs, so controller death cannot trigger a duplicate launch while the child is still active. Recovery remains evidence-gated and bounded; permission bypass, dependency installation, deletion, and unapproved external actions are never automatic. Concurrency defaults to one inference lane and scales only within an explicit adaptive ceiling.
