# CogentNexus

CogentNexus is a **durable Host/control layer for OpenClaw**. It keeps accepted user intent outside the lifetime of a single model call, OpenClaw session, Gateway process, delivery attempt, or context window.

## Current status

**Core version:** 0.9.2  
**OpenClaw Bridge package:** 0.9.1 (unchanged payload)  
**Operational baseline:** 2026-08-21  
**Accepted Recovery Core checkpoint:** `eadb89099637d24f96e265a500d66c577aa939a3`  
**Validated OpenClaw baseline:** `2026.7.1-2`

v0.9.2 keeps the accepted v0.9.1 Ticket/Recovery/Delivery Core and adds a provider-neutral Host boundary, durable provider selection, LM Studio lifecycle support, and a read-only pre-flight inspection namespace.

The accepted live Recovery Core remains the validated Windows/OpenClaw/Ollama baseline. LM Studio support is implemented and covered by repository validation/unit tests, but should receive a local live acceptance run before the same provider-specific operational confidence is assumed.

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
  - selected provider
  - CPU-only deterministic supervision
  - lifecycle / cancellation / generation fences
      |
      v
OpenClaw Gateway + selected provider
      |
      +--> Ollama :11434
      +--> LM Studio :1234
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

## Provider selection

Ollama and LM Studio may be installed on the same machine. Their normal loopback endpoints are separate, and CogentNexus supervises only the **selected provider**.

```powershell
.\cnx.cmd start --provider ollama
.\cnx.cmd start --provider lmstudio
```

A successful explicit start commits the provider selection durably. Later starts/restarts reuse the last successfully selected provider:

```powershell
.\cnx.cmd start
.\cnx.cmd restart
```

Provider selection is transactional. CogentNexus does not commit a new selected provider until provider and Gateway verification succeeds. An interrupted switch leaves a durable `providerTransition` marker so the next start can resume the same target rather than silently guessing or falling back.

`stop`, `disable`, reboot and ordinary restart preserve the selected provider. `reset` returns CNX to fresh-install semantics: if both providers are installed, the reset command requires an explicit `--provider` choice.

See [Provider lifecycle](docs/PROVIDERS.md).

## Pre-flight checks

All diagnostic inspection is grouped under `check` and is **read-only**.

```powershell
.\cnx.cmd check system
.\cnx.cmd check system --provider lmstudio
.\cnx.cmd check provider
.\cnx.cmd check provider ollama
.\cnx.cmd check gateway
.\cnx.cmd check model
.\cnx.cmd check storage
.\cnx.cmd check recovery
.\cnx.cmd check delivery
.\cnx.cmd check resources
```

`check system` is the full aircraft-style pre-flight inspection. It evaluates installation/state/configuration, OpenClaw, provider discovery/readiness, model routing, Gateway, Ticket storage, recovery/delivery state, and resource headroom, then returns one verdict:

- `READY`
- `READY_WITH_WARNINGS`
- `NOT_READY`
- `INDETERMINATE`

Checks never start/restart a process, repair state, change provider selection, rewrite config, or mutate the Ticket database. They end with `No state was changed.`

See [System pre-flight checks](docs/CHECK_SYSTEM.md).

## Core capabilities

- durable SQLite Ticket admission before inference for eligible managed owner messages;
- lightweight DIRECT work without forcing every message into a heavyweight workflow;
- external Host Controller with persisted desired runtime state;
- provider-neutral local lifecycle boundary for Ollama and LM Studio;
- durable selected-provider state and interrupted provider-transition fencing;
- Gateway/provider lifecycle control and deliberate-stop fencing;
- read-only component/system pre-flight checks;
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

## Why this matters in practice

Local inference can fail transiently and non-deterministically: the same model/configuration/tool surface can stall in one run and complete normally on a later retry. CogentNexus keeps the accepted intent durable outside that individual model call and can recover only the layer that actually failed.

The recovery boundary remains strict:

- model call stalled and no durable result exists -> bounded inference recovery may be eligible;
- durable result exists but delivery failed -> retry delivery only, never regenerate;
- an external side effect may already have happened -> require idempotency/receipt/read-after-write evidence before doing anything again.

See [Transient model-call stall recovery](docs/TRANSIENT_STALL_RECOVERY.md).

## Acceptance checkpoint

The accepted Windows live Test A v16 demonstrated one Host-authorized recovery attempt, original provider/model preservation, no recursive Ticket, no same-session duplicate Ticket, no escaped database-lock retry, no native-restart ownership collision, one durable result, and one confirmed delivery.

v0.9.2 deliberately layers provider selection/checks above that accepted Core rather than rewriting its Ticket, classification, durable-result, or delivery fences.

## Known boundaries

Not yet claimed as fully accepted/hardened:

- LM Studio live recovery acceptance on the target Windows machine;
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
.\scripts\install.ps1 -Provider ollama
# or
.\scripts\install.ps1 -Provider lmstudio
```

If exactly one supported provider is installed, `-Provider` may be omitted. If both are installed on a fresh CNX state, explicit selection is required.

## Everyday control

```powershell
.\cnx.cmd status
.\cnx.cmd provider list
.\cnx.cmd check system
.\cnx.cmd start
.\cnx.cmd start --provider lmstudio
.\cnx.cmd stop
.\cnx.cmd restart
.\cnx.cmd restart --provider ollama
.\cnx.cmd gateway start
.\cnx.cmd gateway stop
.\cnx.cmd gateway restart
.\cnx.cmd ticket list
.\cnx.cmd ticket cancel <ticket-id>
.\cnx.cmd session cancel <session-key>
.\cnx.cmd disable
.\cnx.cmd enable
.\cnx.cmd reset
.\cnx.cmd uninstall
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
- [Provider lifecycle](docs/PROVIDERS.md)
- [System pre-flight checks](docs/CHECK_SYSTEM.md)
- [Transient stall recovery](docs/TRANSIENT_STALL_RECOVERY.md)
- [Continuity acceptance](docs/CONTINUITY_TESTS.th.md)
- [Knowledge and evidence model](docs/KNOWLEDGE.md)
- [Ticket-first admission](docs/phase0-ticket-first.md)
- [v0.9.2 release notes](docs/releases/v0.9.2.md)

Historical release notes and benchmark documents are intentionally preserved as historical evidence rather than rewritten to match the current release.
