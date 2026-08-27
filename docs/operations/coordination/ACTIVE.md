# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `SOURCE_TDD_POWERSHELL_ACTION_RESOLVER_BOUNDARY_REPAIR`
Current authorization: `TASK087_ACTION_RESOLVER_BOUNDARY_REPAIR_AUTHORIZED`
Task ID: `CNX-20260827-088`
Updated: 2026-08-27 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260827-088-repair-action-resolver-parameter-splatting-boundary.md`](tasks/CNX-20260827-088-repair-action-resolver-parameter-splatting-boundary.md)

## Task 087 accepted blocker

Task 087 reported:

`BLOCKED_SUPPORTED_PENDING_RECOVERY_INSTALL_OVER`

Report HEAD:

`88917b48b812e86a8e7dafb1c70b6cf04f98e91f`

Independent review:

Decision: `ACCEPT`

Disposition:

`ACCEPT_BLOCKER_ACTION_RESOLVER_PARAMETER_SPLATTING_BOUNDARY`

Review path:

[`reviews/CNX-20260827-087-live-attested-pending-rollover-recovery-and-parity.md`](reviews/CNX-20260827-087-live-attested-pending-rollover-recovery-and-parity.md)

Publication fence is accepted: Task 087 is one report-only commit from execution HEAD `e55414f690046f4562aaae148b1c4d0339756d38` and contains no product source changes.

## Task 087 live evidence preserved

The one authorized supported installer invocation was executed exactly once and was not retried.

Pre-mutation evidence passed:

- controller PASSTHROUGH generation 13;
- exactly two canonical generations;
- manifest -> prior `g-5593cbcfff5b35d5`;
- active disabled replacement -> `g-7257c4555ca8ad21`;
- replacement fingerprint equals exact source fingerprint;
- attested classification = `upgrade + pendingRollover=true + pluginAlreadyExact=false`;
- direct lifecycle decision = `installPlugin=false + rolloverPlugin=true`;
- Gateway healthy;
- no semantic/provider run active.

The installer then failed before rollover at the action-resolver call boundary with:

`Cannot validate argument on parameter 'Mode': argument "-Mode" is not in fresh,legacy,upgrade`.

After failure:

- no retry occurred;
- canonical generation count remains 2;
- no third generation was created;
- manifest/controller remained unchanged;
- AGENTS remains absent and Supervisor absent;
- zero semantic messages and zero provider probes were generated.

## Exact root cause

Accepted source `71f48c1a134ee9b2646b4cc7f077abe9cae59ebb` constructs `$actionArgs` as an array containing strings such as `"-Mode"` and then array-splats it into the PowerShell resolver.

Array splatting passes positional values; it does not reinterpret `"-Mode"` as named-parameter syntax. The resolver therefore receives the literal string `-Mode` as the value of its positional `Mode` parameter and its ValidateSet rejects it.

This is the only current blocker carried into Task 088. The Task-084/085/086 attestation, classification, lifecycle truth table and independent rollover gate remain preserved.

## Current live state remains read-only

The Task-083/087 two-generation PASSTHROUGH topology remains the accepted baseline. Do not manually normalize it.

No live install/install-over/uninstall/reset/cleanup or manual rollover is authorized in Task 088.

## Task 088 requirements

Task 088 is source/test-only and must:

1. RED-reproduce the exact PowerShell 5.1 array-splat failure against the production resolver.
2. Prove the resolver itself works with correct named parameters.
3. Replace the installer caller with a PowerShell-5.1-safe named-parameter mechanism, preferably hashtable splatting.
4. Exercise fresh, legacy, ordinary upgrade, pending recovery, already-exact, SkipPlugin and impossible pending+exact rows through the corrected boundary.
5. Add production-boundary/AST coverage proving the installer no longer uses a string-token array for resolver arguments.
6. Preserve Task-086 sibling install/rollover gates and ordering before strict `resolve-plugin`.
7. Preserve all ownership/security/atomicity/npm-pack/semantic regressions.
8. Keep zero diff under `plugins/cogentnexus-openclaw/**`.
9. Run full Python/npm11/npm12/PowerShell/installer/baseline gates.

## Hard live and semantic fence

Task 088 sends zero semantic messages and performs zero provider probes.

No live installer, generation mutation, ownership/controller/startup/Supervisor/AGENTS/config/runtime/SQLite/session mutation, Dashboard/WebChat/CLI send, direct Ollama call, provider/model/timeout change, restart/reboot, merge, tag or release.

## Successor gate

Only an independently accepted:

`PASS_ACTION_RESOLVER_PARAMETER_BOUNDARY_REPAIRED`

may authorize another single supported live recovery attempt against the preserved two-generation topology.
