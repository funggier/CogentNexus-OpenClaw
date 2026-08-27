# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `SOURCE_TDD_PRODUCTION_ROLLOVER_GATE_REPAIR`
Current authorization: `TASK085_NESTING_REWORK_AUTHORIZED`
Task ID: `CNX-20260827-086`
Updated: 2026-08-27 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260827-086-fix-production-pending-rollover-gate-nesting.md`](tasks/CNX-20260827-086-fix-production-pending-rollover-gate-nesting.md)

## Task 085 review

Task 085 reported:

`PASS_ATTESTED_CLASSIFICATION_AND_PENDING_ROLLOVER_CONTROL_FLOW_REPAIRED`

Implementation HEAD:

`6b5c9d56a48d4affe67c2bb718898378edee6e8a`

Report HEAD:

`d8951eb1b724fc60236e458a78da0cef2926868d`

Independent review:

Decision: `REWORK`

Disposition:

`REWORK_PENDING_ROLLOVER_STILL_NESTED_UNDER_INSTALL_GATE`

Review path:

[`reviews/CNX-20260827-085-correct-attested-classification-and-pending-rollover-control-flow.md`](reviews/CNX-20260827-085-correct-attested-classification-and-pending-rollover-control-flow.md)

Publication fence is accepted: one implementation commit followed by one report-only commit; no `plugins/cogentnexus-openclaw/**` changes.

## Task-085 evidence preserved

Do not redo unnecessarily:

- source `plugin-fingerprint` attestation;
- expected replacement fingerprint bound into rollover plan/apply;
- explicit source equality is enforced for every attested replacement;
- ordinary single-generation changed-source classification now returns `upgrade`, `pending=false`, `exact=false`;
- already-source-exact single generation returns `upgrade`, `pending=false`, `exact=true`;
- generic two-generation resolver remains ambiguous;
- executable lifecycle truth table helper returns the correct action matrix;
- Ticket DB bootstrap is outside package-install gate;
- Task-084 ownership/security/atomicity fences remain intact;
- no live mutation occurred in Task 085.

## Why Task 085 is REWORK

`scripts/install.ps1` still nests the actual upgrade rollover block inside:

`if ($actions.installPlugin) { ... }`

although the Task-085 helper correctly returns pending recovery as:

- `installPlugin=false`
- `rolloverPlugin=true`

Therefore pending recovery still cannot reach rollover-plan/apply and would later hit strict `resolve-plugin` with two canonical candidates.

This is the sole blocking production-control-flow finding currently carried into Task 086.

## Current live state remains read-only

The Task-083 two-generation partial topology remains the accepted live baseline:

- controller PASSTHROUGH generation 13;
- startup disabled;
- Supervisor absent;
- AGENTS managed block absent;
- manifest -> prior `g-5593cbcfff5b35d5`;
- active disabled replacement -> `g-7257c4555ca8ad21`;
- prior fingerprint `7e9189f8...`;
- replacement/source fingerprint `8fd911e3...`;
- Gateway/Ollama healthy from accepted evidence;
- SQLite integrity accepted, Tickets/outbox zero.

Do not manually normalize this topology.

## Task 086 requirements

Task 086 is source/test-only and must:

1. RED-prove against implementation `6b5c9d56...` that production rollover is a descendant of the `$actions.installPlugin` gate.
2. Use PowerShell 5.1 AST or equivalently exact production-script analysis against the real `scripts/install.ps1`.
3. Preserve the package-install block under `installPlugin`.
4. Move the upgrade rollover block to an independent sibling gate controlled by `rolloverPlugin`.
5. Prove pending recovery reaches rollover with install=false.
6. Prove ordinary upgrade performs install then rollover.
7. Prove already-exact performs neither.
8. Prove rollover occurs before later strict `resolve-plugin`/ownership publication.
9. Preserve all Task-084/085 classification, attestation, security and rollback behavior.
10. Keep zero diff under `plugins/cogentnexus-openclaw/**`.
11. Run full Python/npm11/npm12/PowerShell/installer/semantic/baseline verification.

## Hard live fence

Task 086 may not run live install/install-over/uninstall/reset/cleanup; may not mutate live generations, controller/startup/Supervisor/AGENTS/ownership/config/runtime/SQLite/session state; may not send Dashboard/WebChat/CLI semantic messages; may not call Ollama directly or change provider/model/timeouts; and may not restart/reboot/merge/tag/release.

## Successor gate

Only an independently accepted:

`PASS_PENDING_ROLLOVER_PRODUCTION_GATE_REPAIRED`

may authorize another live recovery attempt.

That live successor must use one supported installer invocation to complete the existing attested pending rollover without npm-pack/plugin install or a third generation, restore MANAGED/startup/Supervisor/AGENTS, prove parity/health, observe five natural no-flash ticks, and prove Dashboard/WebChat owner-surface readiness with zero semantic messages.
