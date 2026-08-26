# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `SOURCE_TDD_CRASH_SAFE_DELIVERY_FENCING`
Current authorization: `CRASH_SAFE_DELIVERY_FENCING_REPAIR_AUTHORIZED`
Task ID: `CNX-20260826-080`
Updated: 2026-08-26 23:20 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260826-080-close-crash-safe-lock-and-exact-delivery-run-fencing.md`](tasks/CNX-20260826-080-close-crash-safe-lock-and-exact-delivery-run-fencing.md)

## Task 079 report/review

Task 079 reported:

`PASS_WORKFLOW_DELIVERY_ATOMICITY_CLOSED`

Implementation/test HEADs:

- `3c5c637d7299435bd1fef614d399f9a7017cb358`
- `ef22d03ae2b2cc68da76640c2108944d01bc9524`

Report HEAD:

`a5228f65cf5da0b40831703d49e234ae585d5fde`

Independent review:

Decision: `REWORK`

Disposition:

`REWORK_CRASH_SAFE_LOCK_PUBLICATION_AND_EXACT_RUN_FENCING`

Review path:

[`reviews/CNX-20260826-079-finish-workflow-delivery-atomicity.md`](reviews/CNX-20260826-079-finish-workflow-delivery-atomicity.md)

## Accepted Task-078/079 candidate evidence to preserve

Do not redo unless a focused regression proves otherwise:

- owner/session-bound delivery-marker fail-closed behavior;
- repeated owner Ticket admission/routing idempotency;
- one Ticket/Host timeout-recovery authority;
- direct model-call lease/Host ordering coverage with no production lease fix required;
- direct semantic lifecycle `accepted -> routed -> response_ready -> delivery_confirmed -> completed` and negative owner/CLI/subagent coverage;
- provider disposition `PROVIDER_READY_WITH_FRESH_OWNER_SESSION` from the two already-consumed Task-078 direct Ollama probes;
- stale workflow schedule-failure rollback CAS;
- workflow scheduling/binding/settlement serialization;
- same-run bind idempotency and different-bound-run rejection;
- repeated scheduling/rollback/retry convergence;
- complete well-formed dead-PID lock recovery and live-PID non-steal behavior;
- full npm/Python/baseline verification reported green.

No further Ollama probe is authorized or required.

## Why Task 080 exists

Independent review found two remaining fail-closed gaps:

1. current completion lock creates the canonical `.lock` file before writing complete owner metadata. A process death in that tiny acquisition window can leave an empty/partial canonical lock; `readCompletionLock()` then cannot classify it and every future acquisition returns without recovery, violating the crash-liveness invariant;
2. workflow and Ticket settlement with a supplied run id can still accept an unbound durable record. Workflow settlement rejects only a different existing run, and Ticket outbox SQL currently allows `delivery_run_id IS NULL OR delivery_run_id=?`. Durable settlement must require the exact prior run binding when a run identity is supplied.

Task 080 must RED/GREEN only these final delivery-fencing gaps, preserve all accepted predecessor behavior, and rerun the complete semantic/recovery/security regression gates.

## Hard live fence

No OpenClaw semantic/user message, no Dashboard/WebChat live turn, no `openclaw agent` semantic test, no direct Ollama probe, no live Ticket/session/SQLite mutation, no install/install-over/uninstall/reset/cleanup, no provider/model/config/plugin/AGENTS change, no restart/reboot, no merge/tag/release. Source work must use a fresh isolated worktree.

Accepted live production remains:

`79b51ed06363f6e8862c491ee0a313ddb412c806`

Task-078/079/080 candidate source remains non-live until supported install-over parity is independently authorized and accepted.

## Successor gate

If Task 080 passes independent review, the next task is supported install-over/source-live parity/health/no-flash using the combined accepted Task-078/079/080 implementation. That live task may prepare/verify a fresh authenticated Dashboard/WebChat owner session but must not send the final semantic nonce.