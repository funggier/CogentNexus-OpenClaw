# Coordination Channel Status

**State:** `READY_FOR_HERMES`
**Updated:** 2026-08-27 ICT
**Transport:** GitHub repository history
**Human authority:** operator authorized definitive repair through final live/semantic acceptance and approved heavy comprehensive work while Hermes/Codex budget is available
**Execution trigger:** manual Hermes continuation; scheduled execution remains disabled

## Accepted semantic/delivery lineage

Tasks 078/079/080 remain accepted candidate behavior covering owner/session delivery security, admission/routing idempotency, timeout recovery authority, direct model-call lease ordering, direct lifecycle convergence, workflow delivery atomicity, crash-safe completion-lock publication and exact workflow/Ticket delivery-run fencing.

Task 082 remains accepted for the Windows/npm 11/npm 12 `npm pack --json` installer boundary.

Task 084/085/086 established and repaired source-attested same-version rollover, classification truth tables and independent production install/rollover gates. Task 086 accepted source remains:

`71f48c1a134ee9b2646b4cc7f077abe9cae59ebb`

Provider readiness remains:

`PROVIDER_READY_WITH_FRESH_OWNER_SESSION`

No additional direct Ollama probe is authorized.

## Task 087 accepted blocker

Task 087 used one supported live recovery attempt and stopped on the PowerShell action-resolver array-splat boundary.

Accepted disposition:

`ACCEPT_BLOCKER_ACTION_RESOLVER_PARAMETER_SPLATTING_BOUNDARY`

The live topology remains the two-generation PASSTHROUGH state with no third generation, no retry, no semantic message and no provider probe.

## Task 088 reported result

Task 088 report:

`657e0552dbeddd9608b44c7e3845f48533e178a2`

Reported token:

`PASS_ACTION_RESOLVER_PARAMETER_BOUNDARY_REPAIRED`

Reported implementation:

`93854acb3e4fae63abcd52ac85799a77d67498c6`

Independent decision:

`REWORK`

Disposition:

`REWORK_EVIDENCE_PUBLICATION_UNSAFE`

Review:

`docs/operations/coordination/reviews/CNX-20260827-088-repair-action-resolver-parameter-splatting-boundary.md`

## Task-088 publication failure

Fresh repository verification found:

- branch/report HEAD `657e0552...` directly parents execution HEAD `08f74896...`;
- execution -> report is exactly one report-only commit;
- reported implementation `93854ac...` is not repository-resolvable;
- production `scripts/install.ps1` at the report HEAD still has:

```powershell
$actionArgs = @("-Mode", [string]$classification.mode)
...
& $actionResolver @actionArgs
```

Therefore the tested caller fix described by the report is not part of coordination source ancestry and cannot authorize another live attempt.

## Provisional Task-088 evidence preserved

The report records useful evidence that may be reused only after correct source publication:

- RED reproduction of `Mode="-Mode"` under Windows PowerShell 5.1;
- successful named/hashtable invocation of the production resolver;
- intended minimal hashtable-splat caller change;
- focused/full Python, npm 11/npm 12, PowerShell and baseline verification;
- zero plugin-payload and live mutation claims.

Independent acceptance is withheld until implementation is published and reverified.

## Current live baseline

Keep read-only:

- controller PASSTHROUGH generation 13;
- startup disabled;
- Supervisor absent;
- AGENTS managed markers absent;
- ownership manifest -> prior `g-5593cbcfff5b35d5`;
- active disabled source-exact replacement -> `g-7257c4555ca8ad21`;
- exactly two canonical generations;
- no third generation;
- Gateway healthy from accepted Task-087 evidence;
- no semantic/provider activity.

Do not manually normalize the topology.

## Active Task 089

[`tasks/CNX-20260827-089-recover-and-publish-task088-implementation.md`](tasks/CNX-20260827-089-recover-and-publish-task088-implementation.md)

Status: `READY_FOR_HERMES`

Authorization: `TASK088_PUBLICATION_RECOVERY_AUTHORIZED`

Execution mode: `SOURCE_TDD_PUBLICATION_RECOVERY_ACTION_RESOLVER`

Task 089 must:

- start from current coordination HEAD in a fresh isolated worktree;
- recover local `93854ac...` only if its exact diff is available and safe, otherwise recreate the two-file repair with fresh RED/GREEN;
- publish the PowerShell-5.1-safe named-parameter caller into repository ancestry;
- preserve the Task-086 production AST install/rollover sibling gates;
- preserve all attestation/classification/security/atomicity/npm-pack/semantic regressions;
- keep plugin payload source unchanged;
- rerun full Python/npm11/npm12/PowerShell/installer/baseline verification;
- publish implementation first and verify execution->implementation compare;
- publish the Task-089 report as a separate report-only commit and verify implementation->report compare.

## Hard live fence

Task 089 is source/test-only. No live install/install-over/uninstall/reset/cleanup, generation mutation, ownership/controller/startup/Supervisor/AGENTS/config/runtime/SQLite/session mutation, Dashboard/WebChat/CLI semantic message, direct Ollama probe, provider/model/timeout change, restart/reboot, merge/tag/release or force-push.

## Successor logic

Only independent acceptance of:

`PASS_ACTION_RESOLVER_BOUNDARY_PUBLISHED_SAFE`

may authorize another one-shot supported live recovery attempt against the preserved two-generation state.

Final semantic acceptance remains separate until live recovery, exact parity, MANAGED health, five natural no-flash ticks and authenticated Dashboard owner-surface readiness all pass independently.
