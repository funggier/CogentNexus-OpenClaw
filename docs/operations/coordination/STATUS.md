# Coordination Channel Status

**State:** `READY_FOR_HERMES`
**Updated:** 2026-08-26 23:20 ICT
**Transport:** GitHub repository history
**Human authority:** operator authorized definitive repair through final live/semantic acceptance and approved heavy comprehensive source work while Hermes/Codex budget is available
**Execution trigger:** manual Hermes continuation; scheduled execution remains disabled

## Accepted live baseline

Task 075 remains the accepted live baseline source:

`79b51ed06363f6e8862c491ee0a313ddb412c806`

The live product remains MANAGED with previously accepted Gateway/Ollama health, CogentNexus-owned runtime, one canonical v0.9.3 plugin generation and no-flash operation. Task-078/079 source has not been installed live.

## Semantic/provider lineage preserved

Task 076's single CLI-targeted semantic run is retired and its nonce must not be reused. It established that CLI session-key targeting is not an authenticated owner surface. Dashboard/WebChat remains the required future trusted owner surface.

Task 078 materially repaired/proved:

- delivery marker owner/session fail-closed behavior;
- repeated admission/routing idempotency;
- one Ticket/Host timeout recovery authority;
- direct model-call lease ordering;
- direct registered lifecycle and duplicate convergence;
- owner/CLI/subagent negative security behavior;
- provider readiness `PROVIDER_READY_WITH_FRESH_OWNER_SESSION` using exactly two bounded direct Ollama probes already consumed.

Task 079 materially repaired:

- stale schedule-failure rollback CAS;
- workflow bind/schedule/settle serialization;
- repeated scheduling/retry convergence;
- well-formed dead-PID lock recovery and live-lock non-steal behavior.

## Task 079 independent review

Task 079 implementation/test HEADs:

- `3c5c637d7299435bd1fef614d399f9a7017cb358`
- `ef22d03ae2b2cc68da76640c2108944d01bc9524`

Report HEAD:

`a5228f65cf5da0b40831703d49e234ae585d5fde`

Independent decision:

`REWORK`

Disposition:

`REWORK_CRASH_SAFE_LOCK_PUBLICATION_AND_EXACT_RUN_FENCING`

The remaining gaps are narrow but still affect crash-safe durable delivery:

1. canonical completion lock is created before complete owner metadata is written; a process death between these operations can leave an unparsable product lock that later acquisitions will never recover;
2. workflow settlement with a supplied run id accepts the state when no `deliveryRunId` has ever been bound;
3. Ticket outbox settlement has the analogous `(delivery_run_id IS NULL OR delivery_run_id=?)` run fence.

## Active Task 080

[`tasks/CNX-20260826-080-close-crash-safe-lock-and-exact-delivery-run-fencing.md`](tasks/CNX-20260826-080-close-crash-safe-lock-and-exact-delivery-run-fencing.md)

Status: `READY_FOR_HERMES`

Authorization: `CRASH_SAFE_DELIVERY_FENCING_REPAIR_AUTHORIZED`

Execution mode: `SOURCE_TDD_CRASH_SAFE_DELIVERY_FENCING`

Task 080 must use strict RED/GREEN TDD to:

- eliminate the malformed canonical-lock publication crash window with an atomic complete-record create-if-absent protocol;
- preserve live-lock safety and valid dead-owner recovery;
- require exact prior `deliveryRunId` binding for workflow settlement when a run id is supplied;
- require exact prior run binding for Ticket outbox run-bound success/failure settlement;
- preserve all accepted Task-078/079 security/recovery/idempotency behavior;
- rerun npm 11/12, plugin validate/tests, full Python and baseline gates.

No additional provider probe is authorized.

## Hard live fence

No OpenClaw semantic message, Dashboard/WebChat live turn, CLI semantic test, direct Ollama probe, live Ticket/session/SQLite mutation, install/install-over/uninstall/reset/cleanup, provider/model/config/plugin/AGENTS change, restart/reboot, merge/tag/release. Implementation must use a fresh isolated worktree.

## Successor logic

If Task 080 passes independent review, the combined Task-078/079/080 candidate must first undergo supported install-over/source-live parity/health/no-flash acceptance. That live parity gate may prepare a fresh authenticated Dashboard/WebChat owner session but cannot consume the final semantic nonce. A separate final semantic task will authorize exactly one real owner message afterward.