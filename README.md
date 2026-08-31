# CogentNexus-OpenClaw

CogentNexus-OpenClaw is a durable Host/control layer for OpenClaw. It keeps accepted user intent outside the lifetime of a single model call, OpenClaw session, Gateway process, delivery attempt, or context window.

## Current status

- **Release line:** v0.9.3
- **Core / Bridge version:** 0.9.3
- **Validated OpenClaw baseline:** `2026.7.1-2 (0790d9f)`
- **Managed provider:** **Ollama only**
- **Previously accepted implementation candidate:** `f6392da3e4112ce441526d5ef19925c90a872b0b`
- **Accepted active facade SHA-256:** `aa747f8f30080ef839a8d2cbf5758f9981a007ca01f41a988576f42edea8682f`
- **Task-188 package payload-v2 identity:** `408167da1bfba7fa9723d1bd557f29d516ed27c27398b4e48abf9a4f294e6b5b` / `184` files
- **Task-188 installed skill-tree identity:** `a1e873ba404205507a1623961b49f1b1a0689f9f`
- **Executable scripts tree:** unchanged from the accepted implementation baseline (`3d9d323ba19443d46e970b87cef52ce878da274f`)

The v0.9.3 implementation completed the bounded real-Windows lifecycle/semantic acceptance sequence: install-over/provenance, reset, uninstall with external preservation, fresh reinstall, and one final Dashboard semantic/durable-delivery turn. Task 188 subsequently corrected stale current-facing documentation inside the npm package and installed skill surface without changing executable/runtime source. Because those documentation bytes are part of product identity, publication is allowed only from an exact candidate that carries the corrected identities above and passes the proportional changed-surface requalification defined by Task 188.

Public release availability is authoritative on the repository's GitHub Releases/tags. A branch checkout by itself is never proof that a release has been published.

> **Continuity invariant:** once eligible work is durably accepted, it must not silently disappear. It must eventually become delivered/completed, cancelled, or explicitly failed with durable evidence.

See [docs/CURRENT_STATE.md](docs/CURRENT_STATE.md) for the exact accepted/deferred/publication boundary.

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

LM Studio support belongs to the frozen v0.9.2 historical provider layer. v0.9.3 may retain compatibility code needed for migration or native restoration, but current operator-facing v0.9.3 commands do not select, start, stop, probe, or manage LM Studio.

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

## Installation status

There is intentionally no `cnxclaw.cmd install` command. Installation is performed from a reviewed source/archive through the repository installer.

For pre-publication or source-based validation, use an exact reviewed candidate rather than a moving branch. For a published release, use the exact release archive and verify it against `SHA256SUMS.txt`. The package payload and installed skill identities above distinguish the documentation-corrected v0.9.3 artifact from the earlier Windows-accepted implementation baseline while executable/runtime source remains unchanged.

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

## Historical boundary

v0.9.2 is a frozen historical release. Its release notes and historical acceptance evidence may legitimately describe provider-neutral Ollama/LM Studio work. Those records must not be rewritten to pretend history was different, and they must not be used as current v0.9.3 operator guidance.

The Windows evidence for `f6392da3...` is also immutable exact-artifact history. Task 188 carries forward only unchanged-surface claims that are proven by byte identity and requires proportional requalification for the documentation-bearing surface that changed.
