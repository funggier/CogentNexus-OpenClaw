# Coordination Channel Status

**State:** `READY_FOR_HERMES`
**Updated:** 2026-08-27 ICT
**Transport:** GitHub repository history
**Human authority:** operator authorized definitive repair through final live/semantic acceptance and approved heavy comprehensive work while Hermes/Codex budget is available
**Execution trigger:** manual Hermes continuation; scheduled execution remains disabled

## Accepted semantic/delivery lineage

Tasks 078/079/080 remain accepted candidate behavior covering owner/session delivery security, admission/routing idempotency, single timeout recovery authority, direct model-call lease ordering, direct lifecycle convergence, workflow delivery atomicity, crash-safe completion-lock publication, and exact workflow/Ticket delivery-run fencing.

Task 082 remains accepted for the Windows/npm 11/npm 12 `npm pack --json` installer boundary.

Provider readiness remains:

`PROVIDER_READY_WITH_FRESH_OWNER_SESSION`

No additional direct Ollama probe is authorized.

## Accepted live blocker baseline from Task 083

The current live installation remains the bounded two-generation PASSTHROUGH topology created by Task 083:

- controller PASSTHROUGH generation 13;
- ownership manifest points to prior generation `g-5593cbcfff5b35d5`;
- prior fingerprint `7e9189f8...`;
- active disabled source-exact replacement is `g-7257c4555ca8ad21`;
- replacement/source fingerprint `8fd911e3...`;
- startup disabled;
- Supervisor absent;
- AGENTS managed markers absent;
- Gateway/Ollama healthy from accepted evidence;
- SQLite integrity accepted, Tickets/outbox zero.

Do not manually normalize, delete or rewrite this topology.

## Task 084/085 repair lineage

Task 084 established the source-attestation and rollover plan/apply primitives but was reworked for classification/control-flow gaps.

Task 085 corrected:

- ordinary changed-source vs already-exact classification;
- explicit expected-source equality for every attested replacement;
- lifecycle action truth table.

Task 085 remained REWORK only because the production rollover block was still nested under `installPlugin`.

## Task 086 acceptance

Implementation:

`71f48c1a134ee9b2646b4cc7f077abe9cae59ebb`

Report:

`1430d0a23ee2c477fdb5c2015f262c9df09c83df`

Reported token:

`PASS_PENDING_ROLLOVER_PRODUCTION_GATE_REPAIRED`

Independent decision:

`ACCEPT`

Disposition:

`ACCEPT_PENDING_ROLLOVER_PRODUCTION_GATE_REPAIRED`

Review:

`docs/operations/coordination/reviews/CNX-20260827-086-fix-production-pending-rollover-gate-nesting.md`

Publication fence is accepted: one implementation commit then one report-only commit; no plugin payload source changed.

Independent source review confirms production `scripts/install.ps1` now has sibling lifecycle gates:

- package creation/installation remains beneath `$actions.installPlugin`;
- upgrade rollover is controlled independently by `$actions.rolloverPlugin`;
- rollover occurs before later strict `resolve-plugin` / ownership publication.

The new PowerShell AST regression analyzes the actual production script and proves rollover commands have a `rolloverPlugin` ancestor but no `installPlugin` ancestor.

Fresh executor verification reported:

- Python `373 passed, 2 skipped, 4 subtests passed`;
- npm 11 plugin suite `49 files, 257 tests passed` plus validation/package/bootstrap gates;
- npm 12 plugin suite `49 files, 257 tests passed` plus validation/package/bootstrap gates;
- PowerShell 5.1 syntax/AST regression passed;
- baseline and `git diff --check` passed;
- plugin payload diff zero.

## Active Task 087

[`tasks/CNX-20260827-087-live-attested-pending-rollover-recovery-and-parity.md`](tasks/CNX-20260827-087-live-attested-pending-rollover-recovery-and-parity.md)

Status: `READY_FOR_HERMES`

Authorization: `ONE_SUPPORTED_PENDING_RECOVERY_INSTALL_OVER_AUTHORIZED`

Execution mode: `LIVE_SUPPORTED_ATTESTED_PENDING_ROLLOVER_RECOVERY`

Exact source:

`71f48c1a134ee9b2646b4cc7f077abe9cae59ebb`

Task 087 must re-prove the exact Task-083 two-generation topology and explicit source attestation before mutation.

Required pre-install decision:

- `mode=upgrade`;
- `pendingRollover=true`;
- `pluginAlreadyExact=false`;
- `installPlugin=false`;
- `rolloverPlugin=true`.

The one supported installer invocation must:

- execute no `npm pack`/artifact install/`openclaw plugins install` on this pending path;
- create no third generation;
- complete the attested rollover against the existing source-exact replacement;
- converge canonical generations 2 -> 1;
- restore MANAGED/startup/Supervisor/AGENTS through supported behavior only;
- prove exact source/live skill and plugin parity;
- prove ownership/runtime/Gateway/Ollama/SQLite health;
- observe five natural PT1M ticks with `NO_FLASH_MULTI_TICK_PROVEN`;
- prove `DASHBOARD_OWNER_SURFACE_READY` read-only.

## Hard semantic fence

Task 087 sends zero semantic messages and zero provider probes.

No Dashboard/WebChat send, `chat.send`, `openclaw agent`, `sessions_send`, channel message, direct Ollama call, provider/model/timeout change, synthetic Ticket mutation, uninstall/reset/manual cleanup/manual rollover, reboot, merge, tag or release.

The installer may be invoked exactly once. Any nonzero result must stop the task without retry.

## Final semantic successor

Only independent acceptance of:

`PASS_LIVE_ATTESTED_PENDING_RECOVERY_PARITY_NO_FLASH_OWNER_SURFACE_READY`

may authorize one fresh authenticated Dashboard/WebChat owner message for final semantic acceptance.

That final message must prove:

`owner message -> Ticket accepted before provider -> correlated Ollama inference -> response_ready -> exact owner/run delivery_confirmed -> completed -> exactly one visible nonce response`.

The Task-076 nonce remains permanently retired.
