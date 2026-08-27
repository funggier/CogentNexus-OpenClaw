# CogentNexus-OpenClaw

CogentNexus-OpenClaw is a durable Host/control layer for OpenClaw. It keeps accepted user intent outside the lifetime of a single model call, OpenClaw session, Gateway process, delivery attempt, or context window.

## Current status

- **Development line:** v0.9.3
- **Core / Bridge version:** 0.9.3
- **Validated OpenClaw baseline:** `2026.7.1-2`
- **Managed provider:** **Ollama only**
- **Published historical release:** v0.9.2
- **v0.9.3 release status:** development candidate; not yet published as a GitHub Release
- **Accepted Recovery Core checkpoint:** `eadb89099637d24f96e265a500d66c577aa939a3`

v0.9.3 narrows the current managed provider surface to Ollama while retaining older v0.9.2 compatibility modules in-tree for migration/native-restore compatibility. Those historical modules are not a current LM Studio management contract.

> **Continuity invariant:** once eligible work is durably accepted, it must not silently disappear. It must eventually become delivered/completed, cancelled, or explicitly failed with durable evidence.

See [docs/CURRENT_STATE.md](docs/CURRENT_STATE.md) for the exact accepted/deferred boundary.

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
  - Ollama lifecycle/recovery ownership
  - CPU-only deterministic supervision
  - cancellation / generation fences
      |
      v
OpenClaw Gateway + Ollama
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

CogentNexus-OpenClaw v0.9.3 manages **Ollama only**.

```powershell
.\cnxclaw.cmd start
.\cnxclaw.cmd start --provider ollama
.\cnxclaw.cmd check provider
.\cnxclaw.cmd check provider ollama
```

LM Studio support belongs to the frozen v0.9.2 historical provider layer. v0.9.3 may retain compatibility code needed for migration or restoration, but current operator-facing v0.9.3 commands do not select, start, stop, probe, or manage LM Studio.

See [docs/PROVIDERS.md](docs/PROVIDERS.md).

## Core capabilities

- durable SQLite Ticket admission before inference for eligible managed owner messages;
- lightweight DIRECT work without forcing every message into a heavyweight workflow;
- external Host Controller with persisted desired runtime state;
- Ollama lifecycle and recovery control;
- Gateway lifecycle control and deliberate-stop fencing;
- read-only component/system pre-flight checks;
- Direct Recovery for genuinely pre-response interrupted work;
- original provider/model provenance fencing during recovery;
- single-owner recovery across OpenClaw native restart behavior;
- transient SQLite BUSY tolerance at the authority-read boundary;
- recursive/self-intake suppression for recovery continuations;
- response-ready immutability and one durable `direct_result`;
- delivery confirmation and exactly-once-ish CNXCLAW delivery semantics;
- ticket/session cancellation and terminal fencing;
- worker leases, generations, duplicate suppression, bounded retries, durable outboxes;
- verified STAGED workflows, artifact hashes, validators, bounded repair and checkpoints;
- deterministic supervisor probes that perform no model inference.

## Recovery boundary

- model call interrupted and no durable result exists -> bounded inference recovery may be eligible;
- durable result exists but delivery failed -> retry delivery only, never regenerate;
- an external side effect may already have happened -> require idempotency/receipt/read-after-write evidence before doing anything again.

## Install during v0.9.3 development

There is no published v0.9.3 GitHub Release yet. Repository stabilization and real-machine acceptance must complete before publication is considered.

From a reviewed v0.9.3 source/development candidate checkout on Windows:

```powershell
.\scripts\install.ps1 -Provider ollama
```

Do not treat an arbitrary moving branch checkout as a frozen release candidate. The final acceptance process records an exact commit, payload fingerprint, file count, archive SHA256, and GitHub Actions evidence before installation on the real machine.

See:

- [English install guide](docs/INSTALL.md)
- [คู่มือติดตั้งภาษาไทย](docs/INSTALL.th.md)
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

## Historical boundary

v0.9.2 is a frozen historical release. Its release notes and historical acceptance evidence may legitimately describe provider-neutral Ollama/LM Studio work. Those records must not be rewritten to pretend history was different, and they must not be used as current v0.9.3 operator guidance.

A successful repository stabilization and later real-Windows acceptance do not automatically publish v1.0.0; final release promotion remains a separate human decision.
