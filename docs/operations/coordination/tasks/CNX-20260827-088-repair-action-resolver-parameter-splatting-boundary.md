# CNX-20260827-088 — Repair Action-Resolver Parameter Splatting Boundary

Status: `READY_FOR_HERMES`

Execution mode: `SOURCE_TDD_POWERSHELL_ACTION_RESOLVER_BOUNDARY_REPAIR`

Current authorization: `TASK087_ACTION_RESOLVER_BOUNDARY_REPAIR_AUTHORIZED`

Owner: ChatGPT

Executor: Hermes/Codex after operator continuation

## Goal

Repair the exact Windows PowerShell invocation boundary that blocked Task 087, while preserving the accepted classification, lifecycle truth table, independent install/rollover gates and plugin payload fingerprint.

The defect to repair is limited to how `scripts/install.ps1` passes `Mode` and switch values into `scripts/resolve-plugin-lifecycle-actions.ps1`.

This task is source/test only. Do not mutate the current live two-generation PASSTHROUGH installation.

## Predecessor evidence

Task 087 report:

`docs/operations/coordination/reports/CNX-20260827-087-live-attested-pending-rollover-recovery-and-parity.md`

Report HEAD:

`88917b48b812e86a8e7dafb1c70b6cf04f98e91f`

Independent review:

Decision: `ACCEPT`

Disposition:

`ACCEPT_BLOCKER_ACTION_RESOLVER_PARAMETER_SPLATTING_BOUNDARY`

Task 086 accepted source used by the failed live attempt:

`71f48c1a134ee9b2646b4cc7f077abe9cae59ebb`

## Exact root cause

Production currently builds an array containing strings that look like PowerShell parameter tokens:

```powershell
$actionArgs = @("-Mode", [string]$classification.mode)
if ($pendingRollover) { $actionArgs += "-PendingRollover" }
if ($pluginAlreadyExact) { $actionArgs += "-PluginAlreadyExact" }
if ($SkipPlugin) { $actionArgs += "-SkipPlugin" }
$actionsJson = (& $actionResolver @actionArgs | Out-String)
```

With array splatting, `"-Mode"` is passed as a positional argument value rather than parsed as a named parameter. The resolver therefore receives `Mode="-Mode"` and fails its ValidateSet before the live pending rollover can execute.

Do not alter the resolver truth table to accommodate `"-Mode"`; fix the caller boundary.

## Preserved live baseline — READ ONLY

Task 087 stopped without retry. The live product remains:

- controller PASSTHROUGH generation 13;
- startup disabled;
- Supervisor absent;
- AGENTS managed markers absent;
- manifest -> prior `g-5593cbcfff5b35d5`;
- active disabled source-exact replacement -> `g-7257c4555ca8ad21`;
- exactly two canonical generations;
- old fingerprint `7e9189f8...`;
- replacement/source fingerprint `8fd911e3...`;
- no third generation;
- Gateway healthy from Task-087 post-failure evidence;
- zero Task-087 semantic/provider activity.

Do not normalize this state during Task 088.

## Critical payload-preservation fence

Do not modify any file under:

`plugins/cogentnexus-openclaw/**`

Do not bump v0.9.3.

Expected production change is limited to `scripts/install.ps1` unless a focused RED proves a tiny adjacent PowerShell helper/test support change is required.

## Absolute live fence

Task 088 is source/test only.

Do NOT run live install/install-over/uninstall/reset/cleanup; do not mutate live generations, controller/startup/Supervisor/AGENTS/ownership/config/runtime/SQLite/session state; do not send Dashboard/WebChat/CLI semantic messages; do not call Ollama directly; do not change provider/model/timeouts; do not restart/reboot/merge/tag/release.

Use a fresh isolated worktree from the current coordination execution HEAD.

---

# Gate R — mandatory RED against exact Task-086 source

Before production edits, reproduce the exact failure under Windows PowerShell 5.1.

Use the real production resolver:

`scripts/resolve-plugin-lifecycle-actions.ps1`

and the production-shaped invocation semantics from `scripts/install.ps1`.

Required RED fixture for pending recovery:

- classification mode = `upgrade`;
- pendingRollover = true;
- pluginAlreadyExact = false;
- SkipPlugin = false.

Using the predecessor array-splat construction must fail with the same parameter-boundary class as Task 087: `Mode` receives `-Mode` or equivalent ValidateSet failure.

Record the exact command, exit status and error. The RED must not depend on live OpenClaw state.

Also demonstrate that directly calling the resolver with proper named parameters succeeds, isolating the defect to caller argument transport rather than resolver business logic.

---

# Gate F — minimal production fix

Use one PowerShell-5.1-safe named-parameter mechanism.

Preferred implementation:

```powershell
$actionArgs = @{
    Mode = [string]$classification.mode
}
if ($pendingRollover) { $actionArgs.PendingRollover = $true }
if ($pluginAlreadyExact) { $actionArgs.PluginAlreadyExact = $true }
if ($SkipPlugin) { $actionArgs.SkipPlugin = $true }
$actionsJson = (& $actionResolver @actionArgs | Out-String)
```

Equivalent explicit named invocation is acceptable if it does not duplicate the lifecycle truth table or introduce branching inconsistencies.

Requirements:

- never pass literal `"-Mode"` as an array member to the resolver;
- resolver remains unchanged unless a focused independent defect is proven;
- impossible `pending=true + exact=true` still fails closed;
- resolver JSON parse remains explicit and checked;
- no broad installer refactor.

---

# Gate B — real production-boundary regression

Add tests that would fail on exact source `71f48c1a...` and pass only with the corrected installer caller.

Required coverage:

1. PowerShell 5.1 production-shaped pending invocation returns:
   - `installPlugin=false`
   - `rolloverPlugin=true`.
2. Ordinary upgrade returns true/true.
3. Already exact returns false/false.
4. Fresh and legacy return install-only.
5. SkipPlugin returns false/false.
6. pending+exact fails nonzero.
7. Production installer source/AST proves the splatted argument object is a named-parameter hashtable or otherwise proves no string-token array is used.
8. Production installer still consumes the same action resolver output for `$actions.installPlugin` and `$actions.rolloverPlugin`.
9. Preserve Task-086 AST invariants:
   - package creation remains below installPlugin;
   - rollover remains below rolloverPlugin;
   - rollover has no installPlugin ancestor;
   - rollover precedes strict resolve-plugin.

Do not satisfy this with a test-only copy of the caller logic.

---

# Gate P — preserved source semantics

Re-run and preserve:

- source fingerprint attestation;
- explicit expected replacement equality;
- single-old normal upgrade classification;
- pending two-generation classification;
- already-exact classification;
- generic two-generation ambiguity;
- rollover plan/apply inventory/manifest/wrapper/tree/plan-hash fences;
- atomic retirement/rollback;
- npm-pack parser boundary;
- Task-078/079/080 semantic/delivery/security suites.

No plugin payload source changes are authorized.

---

# Full verification

After GREEN, record fresh evidence for:

1. focused Task-088 PowerShell boundary RED/GREEN tests;
2. Task-086 AST/control-flow regression;
3. Task-085 classification/action truth-table tests;
4. full installer transaction/recovery/npm-pack suites;
5. full Python suite with zero failures;
6. PowerShell 5.1 syntax for modified scripts;
7. Node 24/npm 11 clean plugin suite + validation/package/bootstrap gates;
8. Node 22/npm 12 clean plugin suite + validation/package/bootstrap gates;
9. baseline consistency;
10. `git diff --check`;
11. clean final worktree;
12. zero diff under `plugins/cogentnexus-openclaw/**` relative to `71f48c1a...`.

## Publication fence

Commit source/tests first. Publish the report in a separate final report-only commit:

`docs/operations/coordination/reports/CNX-20260827-088-repair-action-resolver-parameter-splatting-boundary.md`

Required final result tokens:

- `PASS_ACTION_RESOLVER_PARAMETER_BOUNDARY_REPAIRED`
- `BLOCKED_ACTION_RESOLVER_BOUNDARY`
- `BLOCKED_INSTALLER_CONTROL_FLOW_REGRESSION`
- `BLOCKED_SECURITY_REGRESSION`
- `BLOCKED_TEST_OR_VALIDATION_FAILURE`
- `BLOCKED_EVIDENCE_PUBLICATION_UNSAFE`

## Successor gate

Only independently accepted `PASS_ACTION_RESOLVER_PARAMETER_BOUNDARY_REPAIRED` may authorize another live recovery installer attempt.

That successor must re-prove the preserved two-generation topology and use exactly one supported install-over from the accepted Task-088 implementation source. It remains separate from final semantic acceptance.
