# CogentNexus

CogentNexus is a **durable Host/control layer for OpenClaw**. It keeps accepted user intent outside the lifetime of a single model call, OpenClaw session, Gateway process, delivery attempt, or context window.

## Current status

**Version:** 0.9.1  
**Operational baseline:** 2026-08-20  
**Accepted Recovery Core checkpoint:** `eadb89099637d24f96e265a500d66c577aa939a3`  
**Validated OpenClaw baseline:** `2026.7.1-2`

The v0.9.1 recovery core is suitable for **general single-node managed use** on the validated Windows/OpenClaw/Ollama stack. The core Ticket-first, Host-authority, Direct Recovery, restart-ownership, durable response, and delivery boundaries have passed live acceptance. It is not claimed to be fully production-hardened for every failure mode or future OpenClaw release.

See [docs/CURRENT_STATE.md](docs/CURRENT_STATE.md) for the exact supported/accepted boundary.

> **Continuity invariant:** once an eligible user message is durably accepted, it must not silently disappear. It must eventually become delivered/completed, cancelled, or explicitly failed with durable evidence.

## Architecture

```text
User / Channel
      |
      v
Durable Ticket admission
      |
      v
CogentNexus Host authority
  - desired runtime state
  - CPU-only deterministic supervision
  - lifecycle / cancellation / generation fences
      |
      v
OpenClaw Gateway + provider
      |
      +--> DIRECT / LOOKUP / ACTION / STAGED
      |
      v
Response-ready commit
      |
      v
Direct result / outbox delivery
      |
      v
Delivery confirmed -> completed
```

In MANAGED mode, CogentNexus is the recovery authority for work it durably owns. OpenClaw native restart continuation is consumed only when the exact native restart envelope matches durable CNX ownership. Transient SQLite `BUSY`/WAL contention during authority polling is not treated as revocation and must not create a second inference attempt.

## Operating modes

- **MANAGED** — Ticket-first continuity and CNX lifecycle/recovery ownership are active.
- **PASSTHROUGH** — CNX interception/background ownership are disabled; OpenClaw behaves natively.
- **MAINTENANCE** — deliberate stop state; durable state is preserved and recovery must not fight operator intent.

`disable` and `stop` are intentionally different: `disable` returns to native OpenClaw, while `stop` preserves managed intent but deliberately stops the managed runtime.

## Core capabilities

- durable SQLite Ticket admission before inference for eligible managed owner messages;
- lightweight DIRECT work without forcing every message into a heavyweight workflow;
- external Host Controller with persisted desired runtime state;
- Gateway/provider lifecycle control and deliberate-stop fencing;
- Direct Recovery for genuinely pre-response interrupted work;
- original provider/model provenance fencing during recovery;
- single-owner recovery across OpenClaw native restart behavior;
- transient SQLite BUSY tolerance at the authority-read boundary;
- recursive/self-intake suppression for recovery continuations;
- response-ready immutability and one durable `direct_result`;
- delivery confirmation and exactly-once-ish CNX delivery semantics;
- ticket/session cancellation and terminal fencing;
- worker leases, generations, duplicate suppression, bounded retries, durable outboxes;
- verified STAGED workflows, artifact hashes, validators, bounded repair and checkpoints;
- context handoff/rotation and durable lesson/evidence storage;
- deterministic supervisor probes that perform no model inference.

## Acceptance checkpoint

The accepted Windows live Test A v16 demonstrated one Host-authorized recovery attempt, original provider/model preservation, no recursive Ticket, no same-session duplicate Ticket, no escaped database-lock retry, no native-restart ownership collision, one durable result, and one confirmed delivery.

The isolated validation run also passed targeted v094 tests (3/3), targeted v099 tests (11/11), the full plugin suite (49 files / 237 tests), plugin validation/build, evaluation, and regenerated distribution hash fences.

## Known boundaries

Not yet claimed as fully accepted/hardened:

- real power-loss/cold-boot acceptance;
- compatibility with OpenClaw versions newer than `2026.7.1-2`;
- disk-full/database-corruption disaster recovery;
- high-concurrency/long soak guarantees beyond current tests;
- exactly-once external side effects when the external system has no idempotency/verification contract.

These boundaries do not prevent ordinary general use; they define where stronger operational guarantees still require additional acceptance work.

## Install

Stable release install instructions:

- [English install guide](docs/INSTALL.md)
- [คู่มือติดตั้งภาษาไทย](docs/INSTALL.th.md)
- [Clean reinstall](docs/CLEAN_REINSTALL.md)
- [ล้างและติดตั้งใหม่แบบสะอาด](docs/CLEAN_REINSTALL.th.md)

From an extracted release/source checkout on Windows:

```powershell
.\scripts\install.ps1
```

Clean reinstall with backup-first behavior:

```powershell
.\scripts\clean-reinstall.ps1
```

## Everyday control

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
python scripts/check_baseline_consistency.py
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

## Documentation map

- [Current operational state](docs/CURRENT_STATE.md)
- [Architecture / invariants](docs/BASELINE.md)
- [Continuity acceptance](docs/CONTINUITY_TESTS.th.md)
- [Knowledge and evidence model](docs/KNOWLEDGE.md)
- [Ticket-first admission](docs/phase0-ticket-first.md)
- [v0.9.1 release notes](docs/releases/v0.9.1.md)

Historical release notes and benchmark documents are intentionally preserved as historical evidence rather than rewritten to match the current release.
