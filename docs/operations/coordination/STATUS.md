# Coordination Channel Status

**State:** `READY_FOR_HERMES`
**Updated:** 2026-08-27 ICT
**Transport:** GitHub repository history
**Human authority:** operator authorized definitive repair through final live/semantic acceptance and approved heavy comprehensive work while Hermes/Codex budget is available
**Execution trigger:** manual Hermes continuation; scheduled execution remains disabled

## Accepted semantic/delivery lineage

Tasks 078/079/080 remain accepted candidate behavior covering owner/session delivery security, admission/routing idempotency, timeout recovery authority, direct model-call lease ordering, direct lifecycle convergence, workflow delivery atomicity, crash-safe completion-lock publication and exact workflow/Ticket delivery-run fencing.

Task 082 remains accepted for the Windows/npm 11/npm 12 `npm pack --json` installer boundary.

Task 084/085/086 remain the accepted attested same-version rollover/classification/control-flow lineage.

Provider readiness remains:

`PROVIDER_READY_WITH_FRESH_OWNER_SESSION`

No additional direct Ollama probe is authorized.

## Task 087 live blocker baseline

Task 087 used one supported live recovery attempt and stopped fail-closed at the action-resolver parameter boundary. It was not retried.

Accepted live topology remains:

- controller PASSTHROUGH generation 13;
- startup disabled;
- Supervisor absent;
- AGENTS managed markers absent;
- ownership manifest -> prior `g-5593cbcfff5b35d5`;
- active disabled source-exact replacement -> `g-7257c4555ca8ad21`;
- exactly two canonical generations;
- no third generation;
- Gateway healthy from accepted evidence;
- SQLite integrity accepted, Tickets/outbox zero;
- no semantic/provider activity.

## Task 088 publication failure

Task 088 correctly understood and tested the PowerShell array-splat defect but failed publication: its report landed without its implementation in repository ancestry.

Independent disposition:

`REWORK_EVIDENCE_PUBLICATION_UNSAFE`

No live successor was authorized from Task 088.

## Task 089 acceptance

Implementation:

`d6daf8f93fcd5578f267b2017c6cc82e5de20095`

Report:

`ebd6df825f6b84e68edd2ba24869333154be48c6`

Reported token:

`PASS_ACTION_RESOLVER_BOUNDARY_PUBLISHED_SAFE`

Independent decision:

`ACCEPT`

Disposition:

`ACCEPT_ACTION_RESOLVER_BOUNDARY_PUBLISHED_SAFE`

Review:

`docs/operations/coordination/reviews/CNX-20260827-089-recover-and-publish-task088-implementation.md`

Fresh repository verification confirms:

- execution `25d6c673...` -> implementation `d6daf8f9...` is one commit changing exactly `scripts/install.ps1` and `tests/test_installer_transaction_wiring.py`;
- implementation -> report is one report-only commit;
- implementation is repository-resolvable and in direct ancestry;
- plugin payload source diff is zero.

## Accepted Task-089 source behavior

Production action-resolver invocation now uses PowerShell 5.1-safe named hashtable splatting.

The literal string-token array form that caused Task 087 to bind `Mode="-Mode"` is absent from accepted source.

Preserved Task-086 invariants remain:

- package install is controlled by `installPlugin`;
- rollover is independently controlled by `rolloverPlugin`;
- rollover is not nested under `installPlugin`;
- rollover occurs before strict `resolve-plugin`.

Executor fresh verification reported:

- focused boundary/lifecycle: `42 passed`;
- Python `374 passed, 2 skipped, 4 subtests passed`;
- npm 11 plugin suite `49 files, 257 tests passed` plus validation/package/bootstrap gates;
- npm 12 plugin suite `49 files, 257 tests passed` plus validation/package/bootstrap gates;
- PowerShell 5.1 syntax/AST regression, baseline and `git diff --check` passed.

## Active Task 090

[`tasks/CNX-20260827-090-live-pending-rollover-recovery-retry-after-published-boundary-fix.md`](tasks/CNX-20260827-090-live-pending-rollover-recovery-retry-after-published-boundary-fix.md)

Status: `READY_FOR_HERMES`

Authorization: `ONE_SUPPORTED_PENDING_RECOVERY_RETRY_AFTER_PUBLISHED_FIX_AUTHORIZED`

Execution mode: `LIVE_SUPPORTED_PENDING_ROLLOVER_RECOVERY_RETRY`

Exact source:

`d6daf8f93fcd5578f267b2017c6cc82e5de20095`

Task 090 must re-prove the preserved Task-087 two-generation topology before mutation and require:

- replacement fingerprint == exact source fingerprint;
- `mode=upgrade`;
- `pendingRollover=true`;
- `pluginAlreadyExact=false`;
- `installPlugin=false`;
- `rolloverPlugin=true`;
- production named caller no longer reproduces the Task-087 parameter error.

Exactly one supported normal installer invocation is authorized. Nonzero exit means stop without retry.

For the pending path it must prove:

- no `npm pack`/artifact install/`openclaw plugins install`;
- no third generation;
- reviewed rollover-plan/apply uses exact expected source fingerprint and fresh inventory;
- old generation is retired;
- canonical generations converge 2 -> 1;
- existing source-exact replacement survives as the unique canonical generation.

After successful installer completion it must prove:

- MANAGED/startup/Supervisor/AGENTS restoration;
- exact source/live skill and plugin parity;
- product-owned runtime/launcher/Supervisor bindings;
- ownership/Gateway/Ollama/SQLite health;
- exact accepted four-model inventory unchanged;
- five natural PT1M ticks with `NO_FLASH_MULTI_TICK_PROVEN`;
- read-only `DASHBOARD_OWNER_SURFACE_READY` with zero semantic messages.

## Hard semantic and mutation fence

No Dashboard/WebChat send, `chat.send`, `openclaw agent`, `sessions_send`, channel message, final nonce, direct Ollama call, synthetic Ticket mutation, provider/model/timeout change, uninstall/reset/manual cleanup/manual rollover, reboot, merge, tag or release.

Outside installer-supported behavior, do not manually repair controller/startup/Supervisor/AGENTS/ownership/config/runtime/plugin state.

## Final semantic successor

Only independent acceptance of:

`PASS_LIVE_PENDING_RECOVERY_PARITY_NO_FLASH_OWNER_SURFACE_READY`

may authorize exactly one fresh authenticated Dashboard/WebChat owner message for final semantic acceptance.

That final message must prove:

`owner message -> durable Ticket accepted before correlated provider inference -> exactly one route -> response_ready -> exact owner/run delivery_confirmed -> completed -> exactly one visible nonce response`.

The Task-076 nonce/session remain permanently retired.
