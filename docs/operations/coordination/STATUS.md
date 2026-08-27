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

## Task 083 live blocker baseline

Task 083 made one supported live recovery attempt and stopped fail-closed, leaving the accepted two-generation PASSTHROUGH topology:

- controller PASSTHROUGH generation 13;
- manifest-owned prior `g-5593cbcfff5b35d5`;
- active disabled source-exact replacement `g-7257c4555ca8ad21`;
- startup disabled;
- Supervisor absent;
- AGENTS managed markers absent;
- Gateway/Ollama healthy from accepted evidence;
- SQLite integrity accepted, Tickets/outbox zero.

Do not manually normalize this state.

## Task 084 preserved attestation repair

Implementation:

`0847a260d6f689f364bb096bd7857bb1dd4d58e1`

Task 084 introduced sound source-attestation primitives, expected-fingerprint plan/apply binding and pending classification foundations, but was REWORK because classification and production lifecycle behavior were incomplete.

## Task 085 result and independent review

Implementation:

`6b5c9d56a48d4affe67c2bb718898378edee6e8a`

Report:

`d8951eb1b724fc60236e458a78da0cef2926868d`

Reported token:

`PASS_ATTESTED_CLASSIFICATION_AND_PENDING_ROLLOVER_CONTROL_FLOW_REPAIRED`

Independent decision:

`REWORK`

Disposition:

`REWORK_PENDING_ROLLOVER_STILL_NESTED_UNDER_INSTALL_GATE`

Publication fence is valid and no plugin payload source changed.

## Task-085 evidence accepted

- single old generation different from expected source now classifies as normal upgrade (`pending=false`, `exact=false`);
- already-source-exact generation classifies `exact=true`;
- explicit expected source fingerprint is enforced against the active replacement regardless of retired/replacement equivalence;
- the lifecycle action helper correctly returns:
  - fresh/legacy -> install only;
  - ordinary upgrade -> install + rollover;
  - pending recovery -> rollover only;
  - already exact -> neither;
- generic ambiguous resolution remains strict;
- Task-084 plan/apply, atomicity and rollback fences remain intact;
- live state was not mutated.

## Remaining blocker

The production `scripts/install.ps1` still places the rollover block inside the outer:

`if ($actions.installPlugin)`

Consequently pending recovery has the correct helper tuple `install=false, rollover=true` but the actual rollover remains unreachable.

The existing tests prove the helper truth table but do not prove production caller nesting.

## Active Task 086

[`tasks/CNX-20260827-086-fix-production-pending-rollover-gate-nesting.md`](tasks/CNX-20260827-086-fix-production-pending-rollover-gate-nesting.md)

Status: `READY_FOR_HERMES`

Authorization: `TASK085_NESTING_REWORK_AUTHORIZED`

Execution mode: `SOURCE_TDD_PRODUCTION_ROLLOVER_GATE_REPAIR`

Task 086 must:

- RED-prove the real production nesting against Task-085 implementation;
- add PowerShell 5.1 AST/control-flow coverage of `scripts/install.ps1` itself;
- keep package installation controlled by `installPlugin`;
- make upgrade rollover an independent sibling controlled by `rolloverPlugin`;
- prove pending recovery reaches rollover without package installation;
- prove ordinary upgrade install -> rollover ordering;
- prove already-exact reaches neither;
- prove rollover precedes strict unique `resolve-plugin` and ownership publication;
- preserve all attestation/classification/security/atomicity behavior;
- preserve zero diff under `plugins/cogentnexus-openclaw/**`;
- rerun full Python/npm11/npm12/PowerShell/installer/semantic/baseline gates.

## Hard live fence

Task 086 is source/test-only. No live install/install-over/uninstall/reset/cleanup, generation mutation, ownership/controller/startup/Supervisor/AGENTS/config/runtime/SQLite/session mutation, Dashboard/WebChat/CLI semantic message, direct Ollama probe, provider/model/timeout change, restart/reboot, merge, tag or release.

## Successor logic

Only after independent acceptance of:

`PASS_PENDING_ROLLOVER_PRODUCTION_GATE_REPAIRED`

may one supported live recovery install-over be authorized against the existing Task-083 two-generation state.

That live task must complete the pending attested rollover without package installation or a third generation, restore MANAGED/startup/Supervisor/AGENTS, prove exact source/live parity and owned runtime health, observe five natural PT1M no-flash ticks, and prove Dashboard/WebChat owner-surface readiness without sending a semantic message.
