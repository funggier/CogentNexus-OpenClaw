# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `SOURCE_TDD_WORKFLOW_DELIVERY_ATOMICITY_REPAIR`
Current authorization: `WORKFLOW_DELIVERY_ATOMICITY_REPAIR_AUTHORIZED`
Task ID: `CNX-20260826-079`
Updated: 2026-08-26 22:49 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260826-079-finish-workflow-delivery-atomicity.md`](tasks/CNX-20260826-079-finish-workflow-delivery-atomicity.md)

## Task 078 report/review

Task 078 reported:

`PASS_SEMANTIC_P1S_REPAIRED_PROVIDER_READY`

Implementation HEAD:

`e25fbd5ab0c2773ee65d98782ecba942cbe36d58`

Final report HEAD reviewed:

`b934eea6a9df91e1aa6602730c00c66d995ff62e`

Independent review:

Decision: `REWORK`

Disposition:

`REWORK_WORKFLOW_DELIVERY_ATOMICITY_INCOMPLETE`

Review path:

[`reviews/CNX-20260826-078-close-semantic-p1s-and-provider-readiness.md`](reviews/CNX-20260826-078-close-semantic-p1s-and-provider-readiness.md)

## Accepted Task-078 evidence to preserve

Do not redo unless a regression is independently demonstrated:

- delivery-marker fail-closed owner/run fencing on the registered hook path;
- repeated Ticket admission/routing idempotency;
- one Ticket/Host timeout recovery authority for Ticketed direct runs;
- direct model-call lease/Host interleaving tests and no-production-fix disposition;
- registered direct lifecycle `accepted -> routed -> response_ready -> delivery_confirmed -> completed` with duplicate convergence and negative owner/CLI/subagent coverage;
- full plugin/Python/baseline verification reported green;
- provider disposition `PROVIDER_READY_WITH_FRESH_OWNER_SESSION` from exactly two already-consumed direct Ollama probes (TTFT approximately 7.7 s and 0.2 s).

No additional provider probe is authorized or required in Task 079.

## Why Task 079 exists

Task-078 Gate W is incomplete in three atomicity/crash-recovery areas:

1. scheduling-failure rollback still writes a stale notice without atomic re-read and can overwrite a newer `delivered` state;
2. workflow delivery-run binding is still an unlocked read/write and can race settlement;
3. the new exclusive `.lock` file has no bounded abandoned-lock recovery and can permanently suppress delivery after process death.

Task 079 must RED/GREEN these exact gaps and strengthen repeated/concurrent retry convergence while preserving all accepted Task-078 semantic/provider results.

## Hard live fence

No OpenClaw semantic/user message, no Dashboard/WebChat live turn, no `openclaw agent` semantic test, no direct Ollama probe, no live Ticket/session/SQLite mutation, no install/install-over/uninstall/reset/cleanup, no provider/model/config/plugin/AGENTS change, no restart/reboot, no merge/tag/release. Source work must use a fresh isolated worktree.

Accepted live production remains:

`79b51ed06363f6e8862c491ee0a313ddb412c806`

Task-078/079 candidate source is not live until a later supported install-over/source-live parity gate.

## Successor gate

If Task 079 is independently accepted, the next task is supported install-over/source-live parity/health/no-flash using the combined accepted Task-078/079 implementation. It may prepare a fresh authenticated Dashboard/WebChat owner session but must not send the final semantic nonce.
