# Review — CNX-20260827-088 Repair Action-Resolver Parameter-Splatting Boundary

Decision: `REWORK`

Disposition: `REWORK_EVIDENCE_PUBLICATION_UNSAFE`

Reviewed report HEAD:

`657e0552dbeddd9608b44c7e3845f48533e178a2`

Reported implementation HEAD:

`93854acb3e4fae63abcd52ac85799a77d67498c6`

Execution coordination HEAD:

`08f748965450e1ab9e77de8ead9fcd3c2e726fb0`

## Publication fence — FAILED

The Task-088 report claims a source/tests implementation commit followed by a separate report-only commit, but the published GitHub lineage does not contain that implementation.

Fresh repository verification shows:

- branch/report HEAD `657e0552...` has parent `08f74896...` directly;
- `08f74896... -> 657e0552...` is exactly one commit;
- that commit adds only:
  - `docs/operations/coordination/reports/CNX-20260827-088-repair-action-resolver-parameter-splatting-boundary.md`;
- the reported implementation commit `93854acb3e4fae63abcd52ac85799a77d67498c6` cannot be resolved/compared from the repository;
- therefore the implementation is not an ancestor of the report HEAD and is not available as accepted source on the coordination branch.

This alone blocks acceptance even if the executor's local test evidence is otherwise accurate.

## Independent branch-source verification

The production source at published Task-088 report HEAD still contains the Task-087 defect:

```powershell
$actionArgs = @("-Mode", [string]$classification.mode)
if ($pendingRollover) { $actionArgs += "-PendingRollover" }
if ($pluginAlreadyExact) { $actionArgs += "-PluginAlreadyExact" }
if ($SkipPlugin) { $actionArgs += "-SkipPlugin" }
$actionsJson = (& $actionResolver @actionArgs | Out-String)
```

Thus the coordination branch still passes literal parameter-looking strings through array splatting and would reproduce the same PowerShell 5.1 `Mode="-Mode"` ValidateSet failure seen live in Task 087.

The source repair described by the report is not actually present on the branch.

## Report evidence preserved provisionally

The report contains useful executor evidence that may be reused only after publication is repaired and independently reverified:

- exact RED reproduction of the Task-087 array-splat failure;
- successful direct/hashtable named-parameter invocation of the real resolver;
- intended minimal caller fix using a named hashtable;
- focused boundary regression results;
- full Python, npm 11/npm 12, PowerShell and baseline results;
- zero plugin-payload diff;
- zero live mutation by Task 088.

These are not sufficient to release a source candidate because the tested implementation is not published in repository ancestry.

## Required successor direction

The successor must be source/test-only and operate from the current coordination HEAD.

1. Recover the exact Task-088 implementation if the local Git object/worktree still exists, but do not rewrite or force-push branch history.
2. If recovered, verify its diff is limited to the intended Task-088 production caller fix and focused tests before reapplying/cherry-picking onto a fresh worktree based on current coordination HEAD.
3. If the local implementation object is unavailable, RED-reproduce the same array-splat defect from current published source and recreate the minimal named-parameter hashtable fix under TDD.
4. Re-run the focused production-boundary regression, Task-086 AST/control-flow regression, Task-085 lifecycle truth table, full Python, npm 11/npm 12, PowerShell 5.1, baseline and `git diff --check` gates.
5. Keep `plugins/cogentnexus-openclaw/**` byte-unchanged.
6. Commit source/tests first on top of the current coordination execution HEAD.
7. Publish the successor report in a separate final report-only commit whose parent is the implementation commit.
8. Do not run live recovery while source publication remains unresolved.

## Live disposition

No further live install-over is authorized from branch/report HEAD `657e0552...`.

The accepted Task-087 two-generation PASSTHROUGH state remains the live baseline and must not be manually normalized.

Final semantic acceptance remains blocked.
