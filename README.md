# CogentNexus-OpenClaw

CogentNexus-OpenClaw is a durable Host/control layer for OpenClaw. It keeps accepted user intent outside the lifetime of a single model call, OpenClaw session, Gateway process, delivery attempt, or context window.

## Current status

- **Current release:** `v0.9.5` — published and operationally validated
- **v0.9.5 release baseline:** `50be0b973c30fd8d1528aaac3497c0fc3b0b4d95`
- **Git tag:** `v0.9.5` → exact release baseline above
- **GitHub Release:** `CogentNexus-OpenClaw v0.9.5`
- **Validated OpenClaw baseline:** `2026.7.1-2 (0790d9f)`
- **Managed provider:** Ollama
- **Cloud provider mode:** OpenClaw-owned pass-through

The v0.9.5 release completed final runtime acceptance, exact-head release-gating checks, controlled actionable-wake validation, merge verification, immutable tag verification, and post-release exact-tag installation/runtime verification.

See [docs/CURRENT_STATE.md](docs/CURRENT_STATE.md) for the authoritative current operational state and [docs/POST_RELEASE_BASELINE.md](docs/POST_RELEASE_BASELINE.md) for the published-release baseline.

> **Continuity invariant:** once eligible work is durably accepted, it must not silently disappear. It must eventually become delivered/completed, cancelled, or explicitly failed with durable evidence.

## Architecture

```text
User / Channel
      |
      v
Durable Ticket admission
      |
      v
CogentNexus-OpenClaw Host authority
  - desired runtime state
  - provider/runtime ownership boundaries
  - deterministic supervision
  - cancellation / generation fences
      |
      v
OpenClaw Gateway + managed provider
      |
      +--> DIRECT / LOOKUP / ACTION / STAGED
      |
      v
Response-ready commit
      |
      v
Durable result / delivery
      |
      v
Delivery confirmed -> completed
```

## Operating modes

- **MANAGED** — Ticket-first continuity and CNXCLAW lifecycle/recovery ownership are active.
- **PASSTHROUGH** — CNXCLAW interception/background ownership are disabled; OpenClaw behaves natively.
- **MAINTENANCE** — deliberate stop state; durable state is preserved and recovery must not fight operator intent.

`disable` returns to native OpenClaw. `stop` preserves managed intent but deliberately stops the managed runtime.

## Provider contract

v0.9.5 manages Ollama health, lifecycle, and recovery. Cloud routes remain OpenClaw-owned pass-through: OpenClaw owns authentication, model routing, provider runtime, lifecycle, probing, and recovery. CogentNexus-OpenClaw keeps only the provider-independent continuity boundary and never reads, copies, persists, refreshes, or logs Cloud credentials.

```powershell
.\cnxclaw.cmd start
.\cnxclaw.cmd start --provider ollama
.\cnxclaw.cmd check provider
.\cnxclaw.cmd check provider ollama
```

Historical LM Studio behavior belongs to the frozen historical provider layer and is not a current managed v0.9.5 provider contract.

See [docs/PROVIDERS.md](docs/PROVIDERS.md).

## Core capabilities

- durable SQLite Ticket admission before inference for eligible managed owner messages;
- lightweight DIRECT lane without forcing every message into a heavyweight workflow;
- persisted Host Controller desired runtime state;
- Ollama lifecycle and recovery control;
- Gateway lifecycle control and deliberate-stop fencing;
- read-only component/system pre-flight checks;
- bounded recovery for genuinely interrupted pre-response work;
- original provider/model provenance fencing during recovery;
- single-owner recovery across OpenClaw native restart behavior;
- transient SQLite BUSY tolerance at the authority-read boundary;
- recursive/self-intake suppression for recovery continuations;
- response-ready immutability and one durable `direct_result`;
- delivery confirmation and duplicate suppression;
- silent-sentinel fencing so bare `NO_REPLY` is not promoted into durable visible content;
- bounded same-run sentinel finalization handling;
- ticket/session cancellation and terminal fencing;
- worker leases, generations, bounded retries, durable outboxes, validators and checkpoints for staged work;
- deterministic supervisor probes that perform no model inference.

## Recovery and transient-stall boundary

A model call may fail transiently even when the same provider/model/configuration later succeeds. CogentNexus-OpenClaw treats this as a continuity problem rather than proof that a provider is permanently defective.

- model call interrupted and no durable result exists -> bounded inference recovery may be eligible only from sufficient evidence;
- durable result exists but delivery failed -> retry delivery only, never regenerate;
- a model call is merely slow/silent while provider/Gateway remain healthy -> elapsed time alone is not recovery authority;
- an external side effect may already have happened -> require idempotency/receipt/read-after-write evidence before repetition.

See [docs/TRANSIENT_STALL_RECOVERY.md](docs/TRANSIENT_STALL_RECOVERY.md).

## Installation

For public consumption, install from the exact `v0.9.5` GitHub Release assets and verify `SHA256SUMS.txt` before extraction/install.

There is intentionally no `cnxclaw.cmd install` command. Installation is performed by the repository installer from an exact verified release tree or reviewed source checkout.

```powershell
python -m pip install "PyYAML>=6.0,<7"
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
.\scripts\install.ps1 -Workspace "$HOME\.openclaw\workspace"
```

See:

- [English install guide](docs/INSTALL.md)
- [คู่มือติดตั้งภาษาไทย](docs/INSTALL.th.md)
- [คู่มือคำสั่งภาษาไทย](docs/COMMANDS.th.md)
- [Clean reinstall](docs/CLEAN_REINSTALL.md)
- [ล้างและติดตั้งใหม่แบบสะอาด](docs/CLEAN_REINSTALL.th.md)

## Everyday control

```powershell
.\cnxclaw.cmd status
.\cnxclaw.cmd provider list
.\cnxclaw.cmd check system
.\cnxclaw.cmd start
.\cnxclaw.cmd start --provider ollama
.\cnxclaw.cmd stop
.\cnxclaw.cmd restart
.\cnxclaw.cmd restart --provider ollama
.\cnxclaw.cmd gateway start
.\cnxclaw.cmd gateway stop
.\cnxclaw.cmd gateway restart
.\cnxclaw.cmd ticket list
.\cnxclaw.cmd ticket cancel <ticket-id>
.\cnxclaw.cmd session cancel <session-key>
.\cnxclaw.cmd disable
.\cnxclaw.cmd enable
.\cnxclaw.cmd reset
.\cnxclaw.cmd uninstall
```

Destructive `reset` and `uninstall` require explicit `y` confirmation and are ownership-bounded.

## Validation

```sh
python -m pip install -r requirements-dev.txt
python scripts/check_namespace_isolation.py
python scripts/check_baseline_consistency.py
python skills/cogentnexus-openclaw/scripts/validate.py --workspace-singleton
python skills/cogentnexus-openclaw/scripts/cogent.py self-test
python skills/cogentnexus-openclaw/scripts/runtime.py self-test
python skills/cogentnexus-openclaw/scripts/workflow.py self-test
python -m pytest -q

cd plugins/cogentnexus-openclaw
npm ci
npm test
npm run evaluation
npm audit --omit=dev
npm run plugin:validate
```

## Release and historical boundaries

`v0.9.5` is the current published stable baseline. The immutable release tag and GitHub Release both target merge SHA `50be0b973c30fd8d1528aaac3497c0fc3b0b4d95`.

Post-release documentation commits on `main` may clarify the current documentation surface, but they are not retroactively part of the published `v0.9.5` tag.

Historical v0.9.4/v0.9.3/v0.9.2 notes and reports remain historical evidence. They should not be rewritten merely to make their historical state descriptions look current.
