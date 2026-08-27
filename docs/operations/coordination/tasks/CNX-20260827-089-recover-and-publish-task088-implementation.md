# CNX-20260827-089 — Recover and Publish Task-088 Implementation Safely

Status: `READY_FOR_HERMES`

Execution mode: `SOURCE_TDD_PUBLICATION_RECOVERY_ACTION_RESOLVER`

Current authorization: `TASK088_PUBLICATION_RECOVERY_AUTHORIZED`

Owner: ChatGPT

Executor: Hermes/Codex after operator continuation

## Goal

Recover or recreate the already-understood Task-088 PowerShell action-resolver caller fix, publish it into correct Git ancestry on the coordination branch, and re-prove the focused and full verification gates before any further live recovery attempt.

This task exists because Task 088 produced a report-only commit on the coordination branch while its reported implementation commit is not present/resolvable in repository ancestry.

This task is source/test-only. It must not mutate the current live two-generation PASSTHROUGH installation.

## Predecessor review

Task-088 report HEAD:

`657e0552dbeddd9608b44c7e3845f48533e178a2`

Reported but unpublished implementation:

`93854acb3e4fae63abcd52ac85799a77d67498c6`

Independent review:

Decision: `REWORK`

Disposition:

`REWORK_EVIDENCE_PUBLICATION_UNSAFE`

Review path:

`docs/operations/coordination/reviews/CNX-20260827-088-repair-action-resolver-parameter-splatting-boundary.md`

## Confirmed published-source defect

At Task-088 report HEAD, `scripts/install.ps1` still contains:

```powershell
$actionArgs = @("-Mode", [string]$classification.mode)
if ($pendingRollover) { $actionArgs += "-PendingRollover" }
if ($pluginAlreadyExact) { $actionArgs += "-PluginAlreadyExact" }
if ($SkipPlugin) { $actionArgs += "-SkipPlugin" }
$actionsJson = (& $actionResolver @actionArgs | Out-String)
```

This is the exact Task-087 PowerShell 5.1 failure boundary.

The required repair remains the minimal caller change to named parameter transport, preferably:

```powershell
$actionArgs = @{
    Mode = [string]$classification.mode
}
if ($pendingRollover) { $actionArgs.PendingRollover = $true }
if ($pluginAlreadyExact) { $actionArgs.PluginAlreadyExact = $true }
if ($SkipPlugin) { $actionArgs.SkipPlugin = $true }
$actionsJson = (& $actionResolver @actionArgs | Out-String)
```

Do not modify the resolver truth table to accept the bad token transport.

## Preserved live baseline — READ ONLY

The Task-087 fail-closed live topology remains the accepted baseline:

- controller PASSTHROUGH generation 13;
- startup disabled;
- Supervisor absent;
- AGENTS managed markers absent;
- manifest -> prior `g-5593cbcfff5b35d5`;
- active disabled source-exact replacement -> `g-7257c4555ca8ad21`;
- exactly two canonical generations;
- no third generation;
- no semantic/provider activity from Tasks 087/088.

Do not normalize or mutate this state in Task 089.

## Critical payload fence

Do not modify any file under:

`plugins/cogentnexus-openclaw/**`

Do not bump v0.9.3.

Expected production change is only `scripts/install.ps1`; focused tests may change as needed.

## Absolute live fence

Do NOT:

- run live install/install-over/uninstall/reset/cleanup;
- manually roll over/delete/rename/enable/disable plugin generations;
- edit live controller/startup/Supervisor/AGENTS/ownership/config/runtime/launcher;
- mutate live SQLite/Ticket/session state;
- send Dashboard/WebChat/CLI semantic messages;
- call Ollama directly;
- change provider/model/timeouts;
- restart/reboot/merge/tag/release;
- force-push or rewrite coordination history.

Use a fresh isolated worktree from the exact current coordination HEAD.

---

# Phase A — execution and publication diagnosis

1. Fetch the coordination branch and record exact execution HEAD.
2. Prove Task-088 report and REWORK review are ancestors.
3. Create a fresh isolated worktree from the execution HEAD.
4. Record clean status.
5. Confirm current branch source still reproduces the array-splat defect.
6. Check whether local Git object/commit `93854acb3e4fae63abcd52ac85799a77d67498c6` is available in any local object database/worktree.

### If `93854ac...` exists locally

Before using it:

- inspect its parent;
- inspect full diff;
- require the implementation delta to be limited to the intended Task-088 caller repair and focused tests;
- require zero plugin payload changes;
- do not push it as a detached side history;
- reapply or cherry-pick the verified implementation onto the fresh current-HEAD worktree without force.

### If `93854ac...` does not exist locally

Do not block merely because the local object disappeared. Recreate the minimal fix through the RED/GREEN gates below from current published source.

---

# Gate R — fresh RED from published source

Using Windows PowerShell 5.1 and the real production resolver:

`scripts/resolve-plugin-lifecycle-actions.ps1`

reproduce the production-shaped array-splat invocation:

```powershell
$actionArgs=@('-Mode','upgrade')
$actionArgs += '-PendingRollover'
& $resolver @actionArgs
```

Required RED:

- nonzero exit;
- `Mode` receives `-Mode` or equivalent ValidateSet failure;
- direct correct named invocation succeeds and yields:
  - `installPlugin=false`
  - `rolloverPlugin=true`.

If using a recovered `93854ac...` diff, perform RED on the unmodified current branch before applying the recovered change.

---

# Gate F — minimal source fix

Apply only the caller transport correction needed to use named-parameter semantics under Windows PowerShell 5.1.

Requirements:

- no literal `"-Mode"` array member passed to the resolver;
- `Mode` is supplied as a named key/parameter;
- switches are supplied as named keys/parameters;
- resolver script business logic remains unchanged unless an independent focused RED proves a defect;
- `$actions.installPlugin` and `$actions.rolloverPlugin` remain the production decision outputs;
- Task-086 sibling install/rollover gates remain unchanged;
- no broad installer refactor.

---

# Gate B — production-boundary GREEN

Run executable Windows PowerShell 5.1 coverage through the production-shaped caller boundary for all supported rows:

1. fresh -> install=true, rollover=false;
2. legacy -> install=true, rollover=false;
3. ordinary upgrade -> install=true, rollover=true;
4. pending recovery -> install=false, rollover=true;
5. already exact -> install=false, rollover=false;
6. SkipPlugin -> install=false, rollover=false;
7. pending+exact -> fail nonzero.

Also prove against actual `scripts/install.ps1` source/AST that:

- named parameter transport is used;
- no string-token argument array remains for action resolver invocation;
- package creation remains below `$actions.installPlugin`;
- rollover remains below `$actions.rolloverPlugin`;
- rollover has no `$actions.installPlugin` ancestor;
- rollover occurs before strict `resolve-plugin`.

The regression must exercise or inspect the real production caller, not only invoke the resolver in isolation.

---

# Gate P — predecessor behavior preservation

Re-run and preserve:

- Task-085 attested classification truth table;
- Task-086 production AST/control-flow invariant;
- source fingerprint attestation;
- explicit expected replacement equality;
- pending two-generation classification;
- already-exact classification;
- generic two-generation ambiguity/fail-closed behavior;
- rollover plan/apply inventory/manifest/wrapper/tree/plan-hash fences;
- atomic retirement/rollback;
- Task-082 npm-pack parser boundary;
- Task-078/079/080 semantic/delivery/security suites.

No plugin payload source changes are authorized.

---

# Full verification

Record fresh evidence for:

1. focused Task-089 RED/GREEN parameter-boundary tests;
2. Task-086 AST/control-flow regression;
3. Task-085 action/classification regression;
4. full installer transaction/recovery/npm-pack suites;
5. full Python suite with zero failures;
6. Python compile where applicable;
7. PowerShell 5.1 syntax for modified scripts;
8. Node 24/npm 11 clean plugin suite + validation/package/bootstrap gates;
9. Node 22/npm 12 clean plugin suite + validation/package/bootstrap gates;
10. baseline consistency;
11. `git diff --check`;
12. final clean worktree;
13. zero diff under `plugins/cogentnexus-openclaw/**` relative to Task-086 accepted plugin payload.

---

# Publication fence

The publication sequence is mandatory.

1. Commit source/tests on top of the Task-089 execution HEAD.
2. Push that implementation commit so GitHub can resolve it.
3. Verify with repository compare that execution HEAD -> implementation contains only intended source/tests.
4. Only then create the Task-089 report:

`docs/operations/coordination/reports/CNX-20260827-089-recover-and-publish-task088-implementation.md`

5. Commit/push the report separately.
6. Verify implementation -> report is exactly one report-only commit.

Do not reuse the Task-088 report as proof of the repaired ancestry.

Required result tokens:

- `PASS_ACTION_RESOLVER_BOUNDARY_PUBLISHED_SAFE`
- `BLOCKED_ACTION_RESOLVER_BOUNDARY`
- `BLOCKED_INSTALLER_CONTROL_FLOW_REGRESSION`
- `BLOCKED_SECURITY_REGRESSION`
- `BLOCKED_TEST_OR_VALIDATION_FAILURE`
- `BLOCKED_EVIDENCE_PUBLICATION_UNSAFE`

## Successor gate

Only independent acceptance of:

`PASS_ACTION_RESOLVER_BOUNDARY_PUBLISHED_SAFE`

may authorize another one-shot supported live recovery attempt against the preserved two-generation PASSTHROUGH topology.

Final semantic acceptance remains separate.
