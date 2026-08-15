# CogentNexus

CogentNexus is a **durable host control layer for OpenClaw**.

It keeps accepted user work outside the lifetime of any one LLM call, OpenClaw session, Gateway process, or machine uptime. In managed mode, messages can be committed to a lightweight durable Ticket before inference; deterministic supervision can then recover eligible work after interruption without forcing every request into a heavyweight workflow.

> **Continuity invariant:** once an eligible user message is durably accepted, it must not silently disappear. It must eventually become delivered/completed, cancelled, or explicitly failed with evidence.

CogentNexus is also deliberately optional. `cnx disable` enters **PASSTHROUGH** mode, removes CogentNexus interception/background ownership, and returns OpenClaw to normal native operation without deleting durable CogentNexus state.

## Baseline architecture

```text
User / Channel
      |
      v
CogentNexus Host Controller
  - Ticket-first durability
  - desired runtime state
  - CPU-only supervision
  - lifecycle / cancellation fencing
      |
      v
OpenClaw Gateway
      |
      v
Request lane
  DIRECT  -> ordinary conversation
  LOOKUP  -> focused read-only retrieval
  ACTION  -> bounded reversible execution
  STAGED  -> durable verified workflow
      |
      v
LLM / tools / validators / reviewers
```

The architecture intentionally separates three concerns:

1. **Continuity** — Host/Ticket state keeps accepted work from disappearing.
2. **Execution depth** — the lightest reliable lane is chosen before heavy workflow machinery is loaded.
3. **Verification** — consequential durable work advances only from measured evidence and bounded controller state.

A greeting such as `สวัสดีครับ` may therefore have a durable Ticket and still receive a normal lightweight DIRECT reply.

See [docs/BASELINE.md](docs/BASELINE.md) for the canonical v0.8 architecture and invariants.

## Operating modes

- **MANAGED** — CogentNexus owns Ticket-first continuity, deterministic recovery supervision, and managed runtime lifecycle behavior.
- **PASSTHROUGH** — CogentNexus interception/background ownership are disabled; OpenClaw behaves normally.
- **MAINTENANCE** — deliberate stop state; durable state is preserved and automatic recovery must not fight operator intent.

`disable` and `stop` are intentionally different:

- `disable` -> PASSTHROUGH, OpenClaw remains normally usable.
- `stop` -> MAINTENANCE, managed runtime is intentionally stopped.

## Core capabilities

- durable SQLite Ticket intake before inference for managed owner messages;
- external Host Controller with persisted desired runtime state;
- MANAGED / PASSTHROUGH / MAINTENANCE ownership semantics;
- Gateway/provider lifecycle control with deliberate-stop fencing;
- recovery of committed direct Tickets after confirmed Gateway interruption;
- Ticket and session cancellation with terminal fencing;
- automatic continuation of eligible committed work after restart/reboot;
- atomic revisioned task state, checkpoint/resume/commit/rollback;
- deterministic supervisor with health probes, cooldowns, retry budgets, and circuit breaking;
- worker leases, generation fencing, duplicate suppression, and durable outbox delivery;
- verified workflow DAGs, artifact hashes, deterministic validators, and bounded repair;
- context handoff/rotation for long-running local-model work;
- bounded external research and evidence-backed lesson storage;
- deterministic interruption/retry/duplication/retrieval/SQLite evaluation gates.

The periodic supervisor itself performs no model inference.

## Install

For a stable installation, use a versioned GitHub Release and verify `SHA256SUMS.txt` before running the installer.

Windows PowerShell:

```powershell
.\scripts\install.ps1
```

Linux/macOS:

```sh
chmod +x scripts/install.sh
./scripts/install.sh
```

Detailed guides:

- [English installation guide](docs/INSTALL.md)
- [คู่มือติดตั้ง Windows แบบจับมือทำ (ภาษาไทย)](docs/INSTALL.th.md)

A normal Windows installation validates the package, installs the skill/plugin and bounded workspace policy, initializes Host state, enables Ticket-first managed settings, creates `cnx.cmd`, enables the hidden Host supervisor, reconciles Gateway/provider state, and verifies health.

## Everyday control

From the OpenClaw workspace on Windows:

```powershell
.\cnx.cmd status
.\cnx.cmd start
.\cnx.cmd stop
.\cnx.cmd restart
.\cnx.cmd gateway start
.\cnx.cmd gateway stop
.\cnx.cmd gateway restart
.\cnx.cmd ticket list
.\cnx.cmd ticket cancel <ticket-id>
.\cnx.cmd session cancel <session-key>
.\cnx.cmd disable
.\cnx.cmd enable
```

## Validation

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

## Project layout

```text
skills/cogentnexus/     policy, references, deterministic runtime
plugins/                OpenClaw bridge / Ticket integration
scripts/                installers and packaging helpers
tests/                  baseline and Host/runtime tests
docs/                   canonical architecture, install guides, release history
```

Runtime state lives under the OpenClaw workspace `.cogent/` directory and is intentionally excluded from version control.

## Compatibility philosophy

OpenClaw must remain usable without CogentNexus, and CogentNexus must be able to preserve durable control state without a live OpenClaw inference process. When used together, CogentNexus should increase continuity and verifiability without becoming a single point of failure for native OpenClaw operation.
