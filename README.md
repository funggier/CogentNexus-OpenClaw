# CogentNexus-OpenClaw

CogentNexus-OpenClaw is a durable Host/control layer for OpenClaw. It keeps accepted user intent outside the lifetime of a single model call, OpenClaw session, Gateway process, delivery attempt, or context window.

## Current status

- **Release line:** v0.9.3
- **Core / Bridge version:** 0.9.3
- **Validated OpenClaw baseline:** `2026.7.1-2 (0790d9f)`
- **Managed provider:** **Ollama only**
- **Frozen repaired product candidate:** `050ab53f4b593ab538143084d6bbdbf7e1672e34`
- **Accepted active facade SHA-256:** `aa747f8f30080ef839a8d2cbf5758f9981a007ca01f41a988576f42edea8682f`
- **Package payload-v2:** `b1ca9f3b42009cf4b1ae0a04f0e75add8d2ff9bd5dc97fce4040dc4753562d93` / `186` files
- **Installed skill-tree identity:** `a1e873ba404205507a1623961b49f1b1a0689f9f`
- **Executable skill scripts tree:** `3d9d323ba19443d46e970b87cef52ce878da274f`
- **Repaired Dashboard delivery source blob:** `aa97d7a5411f799c612cd0aeece050085298a8bb`

The v0.9.3 implementation completed the bounded real-Windows lifecycle acceptance sequence through install-over/provenance, reset, uninstall with external preservation, fresh reinstall, and final Dashboard semantic/durable-delivery testing. Task 188 then corrected stale documentation-bearing product bytes. A subsequent real Dashboard requalification exposed a narrow `NO_REPLY` integration defect: CogentNexus could marker-stage OpenClaw's bare silent sentinel into a visible durable result.

Task 191 repaired that boundary with TDD. Task 192 then installed the exact repaired candidate on the accepted Windows host and proved the normal real-runtime shape:

```text
1 human Send
-> 1 Ticket
-> 1 logical OpenClaw run
-> 1 Ollama model call
-> 1 durable assistant delivery
-> 1 logical visible Dashboard assistant result
```

The accepted Task-192 turn returned the requested visible nonce on the first natural final, required no sentinel revision, created no duplicate or Direct Recovery row, left pending outbox at zero, and showed no bare `NO_REPLY` in durable/UI output.

Public release availability is authoritative on GitHub Releases/tags. A branch checkout or this README is never proof that v0.9.3 has been published.

> **Continuity invariant:** once eligible work is durably accepted, it must not silently disappear. It must eventually become delivered/completed, cancelled, or explicitly failed with durable evidence.

See [docs/CURRENT_STATE.md](docs/CURRENT_STATE.md) for the current acceptance/publication boundary.

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

The installer itself remains provider-neutral. Historical LM Studio support belongs to the frozen v0.9.2 provider layer and may remain in compatibility/migration history, but current v0.9.3 operator commands do not manage LM Studio.

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
- delivery confirmation and duplicate suppression;
- direct-Dashboard silent-sentinel fencing so bare `NO_REPLY` is never promoted into durable visible content;
- at most one same-run OpenClaw finalization revision for the exact bounded sentinel case;
- ticket/session cancellation and terminal fencing;
- worker leases, generations, bounded retries, durable outboxes, validators and checkpoints for staged work;
- deterministic supervisor probes that perform no model inference.

## Recovery and transient-stall boundary

A model call may fail transiently even when the same provider/model/configuration later succeeds. CogentNexus treats this as a continuity problem rather than proof that a provider is permanently defective.

- model call interrupted and no durable result exists -> bounded inference recovery may be eligible only from sufficient evidence;
- durable result exists but delivery failed -> retry delivery only, never regenerate;
- a model call is merely slow/silent while provider/Gateway remain healthy -> elapsed time alone is not recovery authority;
- an external side effect may already have happened -> require idempotency/receipt/read-after-write evidence before repetition.

See [Transient Model-Call Stall Recovery](docs/TRANSIENT_STALL_RECOVERY.md) for the observed failure shapes and evidence hierarchy.

## Installation status

There is intentionally no `cnxclaw.cmd install` command. Installation is performed from a reviewed source/archive through the repository installer.

For pre-publication validation, use an exact reviewed candidate rather than a moving branch. For a published release, use the exact release archive and verify it against `SHA256SUMS.txt`.

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

v0.9.2 is a frozen historical release. Historical release notes and acceptance evidence may legitimately describe LM Studio/provider-neutral behavior when that is what actually occurred; those records must not be rewritten as current v0.9.3 promises.

The earlier Windows implementation candidate `f6392da3e4112ce441526d5ef19925c90a872b0b` and documentation-corrected candidate `604569c286e930f1a596362ab926b065b56d486e` remain immutable historical evidence. Task 191/192 supersede them for publication with repaired candidate `050ab53f4b593ab538143084d6bbdbf7e1672e34`.
