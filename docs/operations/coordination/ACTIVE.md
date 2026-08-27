# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `SOURCE_TDD_PUBLICATION_RECOVERY_ACTION_RESOLVER`
Current authorization: `TASK088_PUBLICATION_RECOVERY_AUTHORIZED`
Task ID: `CNX-20260827-089`
Updated: 2026-08-27 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260827-089-recover-and-publish-task088-implementation.md`](tasks/CNX-20260827-089-recover-and-publish-task088-implementation.md)

## Task 088 review

Task 088 reported:

`PASS_ACTION_RESOLVER_PARAMETER_BOUNDARY_REPAIRED`

Report HEAD:

`657e0552dbeddd9608b44c7e3845f48533e178a2`

Reported implementation HEAD:

`93854acb3e4fae63abcd52ac85799a77d67498c6`

Independent review:

Decision: `REWORK`

Disposition:

`REWORK_EVIDENCE_PUBLICATION_UNSAFE`

Review path:

[`reviews/CNX-20260827-088-repair-action-resolver-parameter-splatting-boundary.md`](reviews/CNX-20260827-088-repair-action-resolver-parameter-splatting-boundary.md)

## Why Task 088 is REWORK

The report claims source/tests were committed before the report, but fresh GitHub verification shows:

- Task-088 report HEAD `657e0552...` is one report-only commit directly on execution HEAD `08f74896...`;
- the reported implementation `93854ac...` is not resolvable from the repository;
- execution -> report contains only the Task-088 report file;
- production `scripts/install.ps1` at report HEAD still contains the broken array-splat boundary:

```powershell
$actionArgs = @("-Mode", [string]$classification.mode)
...
& $actionResolver @actionArgs
```

Therefore the Task-088 tested fix is not published as accepted source and no live successor is authorized.

## Preserved Task-088 evidence

The Task-088 report may be reused as provisional executor evidence after source publication is repaired:

- exact RED reproduction of Task-087 `Mode="-Mode"` failure;
- named/hashtable resolver invocation succeeds;
- intended minimal caller fix is understood;
- focused/full Python, npm 11/npm 12, PowerShell and baseline evidence was reported;
- no plugin payload change or live mutation was reported.

These facts do not release a source candidate until repository ancestry is corrected and independently reverified.

## Current live baseline remains read-only

Preserve the Task-087 fail-closed topology:

- controller PASSTHROUGH generation 13;
- startup disabled;
- Supervisor absent;
- AGENTS managed markers absent;
- manifest -> prior `g-5593cbcfff5b35d5`;
- active disabled source-exact replacement -> `g-7257c4555ca8ad21`;
- exactly two canonical generations;
- no third generation;
- no semantic/provider activity.

Do not manually normalize this state.

## Task 089 requirements

Task 089 is source/test-only and must:

1. start from the current coordination HEAD in a fresh isolated worktree;
2. recover local commit `93854ac...` only if it exists and its diff is exactly the intended Task-088 source/test delta; otherwise recreate the fix through fresh RED/GREEN;
3. replace the array-splat action-resolver caller with PowerShell-5.1-safe named parameter transport;
4. exercise all lifecycle rows through the production-shaped boundary;
5. preserve Task-086 sibling install/rollover gates and AST ordering;
6. preserve Task-084/085 attestation/classification/security/atomicity, Task-082 npm-pack and Task-078/079/080 semantic/delivery behavior;
7. keep zero diff under `plugins/cogentnexus-openclaw/**`;
8. rerun full Python/npm11/npm12/PowerShell/installer/baseline gates;
9. publish source/tests first into GitHub-resolvable ancestry;
10. publish the Task-089 report only after implementation compare is verified.

## Hard live fence

No live installer/install-over/uninstall/reset/cleanup, generation mutation, ownership/controller/startup/Supervisor/AGENTS/config/runtime/SQLite/session mutation, Dashboard/WebChat/CLI semantic message, direct Ollama probe, provider/model/timeout change, restart/reboot, merge/tag/release or force-push.

## Successor gate

Only independent acceptance of:

`PASS_ACTION_RESOLVER_BOUNDARY_PUBLISHED_SAFE`

may authorize another single supported live recovery attempt.
