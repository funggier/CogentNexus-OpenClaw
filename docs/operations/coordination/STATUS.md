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

## Source repair lineage through Task 086

Task 084 established source fingerprint attestation and reviewed rollover plan/apply binding.

Task 085 corrected the attested classification and lifecycle truth tables.

Task 086 independently repaired production install/rollover gate nesting and was accepted at source:

`71f48c1a134ee9b2646b4cc7f077abe9cae59ebb`

Its production AST regression proves package creation is under `installPlugin`, rollover is under `rolloverPlugin` but not `installPlugin`, and rollover precedes strict `resolve-plugin`.

## Task 087 live result

Task 087 used exact accepted source `71f48c1a...` for one supported live recovery attempt.

Report:

`88917b48b812e86a8e7dafb1c70b6cf04f98e91f`

Reported token:

`BLOCKED_SUPPORTED_PENDING_RECOVERY_INSTALL_OVER`

Independent decision:

`ACCEPT`

Disposition:

`ACCEPT_BLOCKER_ACTION_RESOLVER_PARAMETER_SPLATTING_BOUNDARY`

Publication fence is valid: report-only, one commit from execution HEAD `e55414f690046f4562aaae148b1c4d0339756d38`.

## Task 087 evidence

Pre-mutation attestation and classification passed exactly:

- PASSTHROUGH generation 13;
- exactly two canonical generations;
- old manifest-owned generation `g-5593cbcfff5b35d5`;
- active disabled source-exact replacement `g-7257c4555ca8ad21`;
- replacement fingerprint == exact source fingerprint;
- `mode=upgrade`;
- `pendingRollover=true`;
- `pluginAlreadyExact=false`;
- direct resolver truth table = `installPlugin=false`, `rolloverPlugin=true`.

The one supported installer invocation failed before rollover because `install.ps1` passed its resolver arguments through array splatting:

```powershell
$actionArgs = @("-Mode", [string]$classification.mode)
...
& $actionResolver @actionArgs
```

PowerShell binds array-splat elements positionally, so the literal string `-Mode` became the value of the resolver's `Mode` parameter and failed its ValidateSet.

The command was not retried. No manual repair, third generation, semantic message or provider probe occurred.

## Current live baseline

The preserved fail-closed live topology remains:

- controller PASSTHROUGH generation 13;
- startup disabled;
- Supervisor absent;
- AGENTS managed markers absent;
- manifest -> `g-5593cbcfff5b35d5`;
- active disabled source-exact replacement -> `g-7257c4555ca8ad21`;
- exactly two canonical generations;
- no third generation;
- Gateway healthy from accepted Task-087 post-failure evidence;
- zero Task-087 semantic/provider activity.

Do not manually normalize this state.

## Active Task 088

[`tasks/CNX-20260827-088-repair-action-resolver-parameter-splatting-boundary.md`](tasks/CNX-20260827-088-repair-action-resolver-parameter-splatting-boundary.md)

Status: `READY_FOR_HERMES`

Authorization: `TASK087_ACTION_RESOLVER_BOUNDARY_REPAIR_AUTHORIZED`

Execution mode: `SOURCE_TDD_POWERSHELL_ACTION_RESOLVER_BOUNDARY_REPAIR`

Task 088 must:

- RED-reproduce the Task-087 PowerShell 5.1 array-splat failure with the real resolver;
- prove proper named invocation succeeds;
- replace the installer caller with safe named-parameter transport, preferably hashtable splatting;
- exercise every lifecycle truth-table row through the corrected boundary;
- add production installer boundary/AST coverage so string-token array splatting cannot regress;
- preserve Task-086 independent install/rollover gates and ordering;
- preserve all Task-084/085 attestation/classification/security/atomicity behavior;
- preserve Task-082 npm-pack and Task-078/079/080 semantic/delivery behavior;
- keep plugin payload source unchanged;
- run full Python/npm11/npm12/PowerShell/installer/baseline verification.

## Hard live fence

Task 088 is source/test-only. No live installer/install-over/uninstall/reset/cleanup, generation mutation, ownership/controller/startup/Supervisor/AGENTS/config/runtime/SQLite/session mutation, Dashboard/WebChat/CLI semantic message, direct Ollama probe, provider/model/timeout change, restart/reboot, merge, tag or release.

## Successor logic

Only independent acceptance of:

`PASS_ACTION_RESOLVER_PARAMETER_BOUNDARY_REPAIRED`

may authorize another one-shot supported live recovery attempt against the preserved two-generation state.

Final semantic acceptance remains separate and is not authorized until live recovery, parity, MANAGED health, five natural no-flash ticks and Dashboard owner-surface readiness all pass independently.
