# CogentNexus

CogentNexus is a **durable host control layer for OpenClaw**. It sits outside the model and, in managed mode, outside the OpenClaw Gateway lifecycle so accepted user work can survive model failure, Gateway interruption, deliberate restart, and machine reboot.

Its central invariant is simple:

> Once a user message is durably accepted, it must not silently disappear. It must eventually become delivered/completed, cancelled, or explicitly failed with evidence.

CogentNexus does **not** make every request heavy. Every eligible owner message can be committed to a lightweight durable Ticket before inference, while the request itself is still routed through the lightest reliable execution lane. Greetings and ordinary conversation remain direct; complex or interruption-prone work can escalate into verified durable workflows only when needed.

CogentNexus also remains optional. `cnx disable` enters **PASSTHROUGH** mode, removes CogentNexus interception and lifecycle ownership, and returns OpenClaw to normal native operation without deleting durable state.

CogentNexus Core is part of the [CogentNexus Ecosystem](https://github.com/funggier/cogentnexus-ecosystem), together with companion routing and review policies such as Staged Capability Loop.

## Architecture

```text
User / Channel
      |
      v
CogentNexus Host Controller
      |-- durable Ticket intake
      |-- desired/actual runtime state
      |-- CPU-only supervision and recovery
      |-- cancellation and session fencing
      |
      v
OpenClaw Gateway
      |
      v
Admission / execution lane
  | DIRECT   -> lightweight conversation
  | LOOKUP   -> focused read-only work
  | ACTION   -> bounded reversible work
  ` STAGED   -> durable verified workflow
      |
      v
LLM / tools / reviewers
```

The Host Controller is intentionally independent of OpenClaw inference. It can preserve state, detect runtime failure, restart managed components, and resume committed work without using an inference lane itself.

## Operating modes

- **MANAGED** — CogentNexus owns Ticket-first continuity, recovery supervision, and managed OpenClaw lifecycle behavior.
- **PASSTHROUGH** — CogentNexus interception and background ownership are disabled; OpenClaw behaves normally.
- **MAINTENANCE** — intentional stop state; durable state is preserved and the supervisor must not restart components against operator intent.

`disable` and `stop` therefore mean different things: disabling returns control to native OpenClaw; stopping records deliberate maintenance.

## What CogentNexus guarantees

CogentNexus separates three concerns that should not be conflated:

1. **Continuity** — the Host Controller keeps accepted work from disappearing.
2. **Execution depth** — lane policy chooses the lightest reliable way to handle the request.
3. **Verification** — durable workflows use deterministic evidence, bounded review, and checkpointed recovery before claiming completion.

This means Ticket-first intake does not imply staged execution. A message such as `สวัสดีครับ` may have a durable Ticket while still receiving a normal lightweight reply.

## Current capabilities

- Durable SQLite Ticket intake before inference for managed owner messages
- External Host Controller with persisted desired runtime state
- MANAGED, PASSTHROUGH, and MAINTENANCE operating modes
- Gateway lifecycle control with deliberate-stop fencing
- Recovery of committed direct Tickets after confirmed Gateway interruption
- Ticket and session cancellation with terminal fencing and durable outbox support
- Automatic continuation after restart or reboot when managed state requests a running runtime
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
- Cross-platform deterministic supervisor with health probes, verified recovery, cooldowns, and circuit breaking
- Bounded startup readiness polling
- Native scheduler templates for Windows Task Scheduler, systemd, launchd, cron, Docker Compose, and Kubernetes
- Fixed or adaptive concurrency admission with one inference lane as the safe default
- Durable context handoff with live token observation, integrity binding, worker leases, generation fencing, and session rotation thresholds
- Verified workflow DAGs with command/Ollama executors, deterministic validators, bounded retries, and artifact hashes
- Always-on workflow discovery and detached controller resumption from the native periodic supervisor
- Automatic context-pressure rotation for bound durable tasks through a clean TaskFlow worker session
- Domain-aware durable compilation for software, trading/EA systems, file operations, analysis, fiction, design, translation, and general work
- Arbitrary named-artifact generation with deterministic existence, size, encoding, and syntax validation
- Minimal ledger records without chain-of-thought
- Bounded external research with provenance, TTL snapshots, corroboration, and prompt-injection isolation
- Deterministic evaluation for interruption, retry, duplication, retrieval quality, and SQLite scale decisions

## Installation

For stable installations, download a versioned archive from [GitHub Releases](https://github.com/funggier/cogentnexus/releases) and verify it against `SHA256SUMS.txt`.

Windows PowerShell:

```powershell
.\scripts\install.ps1
```

Linux or macOS:

```sh
chmod +x scripts/install.sh
./scripts/install.sh
```

A normal Windows installation installs and validates the skill/plugin, writes the bounded managed policy into the OpenClaw workspace, initializes Host state, enables Ticket-first managed settings, creates `cnx.cmd`, enables the hidden Host supervisor, and verifies the runtime unless restart was explicitly skipped.

See [docs/INSTALL.md](docs/INSTALL.md) for prerequisites, upgrade behavior, passthrough mode, and troubleshooting.

## Everyday control

From the OpenClaw workspace on Windows:

```powershell
.\cnx.cmd status
.\cnx.cmd start
.\cnx.cmd stop
.\cnx.cmd restart
.\cnx.cmd gateway restart
.\cnx.cmd ticket list
.\cnx.cmd ticket cancel <ticket-id>
.\cnx.cmd session cancel <session-key>
.\cnx.cmd disable
.\cnx.cmd enable
```

Key semantics:

- `start` — request MANAGED runtime running and resume eligible committed work.
- `stop` — enter MAINTENANCE; do not auto-recover until started again.
- `restart` — preserve managed intent, restart runtime, then continue eligible committed work.
- `disable` — enter PASSTHROUGH so OpenClaw works natively without CogentNexus interception.
- `enable` — re-enter MANAGED mode and reconcile the managed runtime.

## Background supervision

CogentNexus supervision is deterministic and consumes no inference lane. On Windows it runs through a hidden Scheduled Task using `pythonw.exe`; equivalent scheduler integrations are available for other platforms.

The supervisor reasons from persisted desired state, health evidence, leases, generations, and terminal Ticket/workflow state. It distinguishes an unplanned failure from an intentional stop so it does not fight operator intent.

## Layout

```text
skills/
└── cogentnexus/
    ├── SKILL.md
    ├── assets/
    ├── references/
    └── scripts/
```

Runtime data is stored under `.cogent/` and intentionally excluded from version control.

## Validate

Requires Python 3.10+ and the development dependencies.

```sh
python -m pip install -r requirements-dev.txt
python skills/cogentnexus/scripts/validate.py --workspace-singleton
python skills/cogentnexus/scripts/cogent.py self-test
python skills/cogentnexus/scripts/runtime.py self-test
python skills/cogentnexus/scripts/workflow.py self-test
python -m unittest discover -s tests -v
cd plugins/cogentnexus-rotation
npm ci
npm test
npm run evaluation
npm audit --omit=dev
npm run plugin:validate
```

## Release notes

See [v0.7.0](docs/releases/v0.7.0.md) for the Host Controller, Ticket-first continuity, passthrough mode, cancellation controls, installer integration, and release validation introduced with the managed-host architecture.

## Design principle

OpenClaw must remain usable without CogentNexus, and CogentNexus must be able to preserve control state without relying on a live OpenClaw inference process. When combined, CogentNexus enhances OpenClaw with durable continuity rather than becoming a dependency that can take OpenClaw down with it.
