# Review — CNX-20260827-087 Live Attested Pending-Rollover Recovery and Parity

Decision: `ACCEPT`

Disposition: `ACCEPT_BLOCKER_ACTION_RESOLVER_PARAMETER_SPLATTING_BOUNDARY`

Reviewed report HEAD:

`88917b48b812e86a8e7dafb1c70b6cf04f98e91f`

Execution coordination HEAD:

`e55414f690046f4562aaae148b1c4d0339756d38`

Exact source used by the live attempt:

`71f48c1a134ee9b2646b4cc7f077abe9cae59ebb`

## Publication fence

Accepted.

`e55414f... -> 88917b4...` is exactly one report-only commit adding the Task-087 report. No product source change was published by Task 087.

## Live execution disposition

The executor correctly re-proved the required Task-083 residue before mutation:

- controller PASSTHROUGH generation 13;
- exactly two canonical generations;
- manifest-owned prior generation `g-5593cbcfff5b35d5`;
- active disabled replacement `g-7257c4555ca8ad21`;
- replacement fingerprint equals exact accepted source fingerprint;
- attested classification = `upgrade + pendingRollover=true + pluginAlreadyExact=false`;
- lifecycle decision, when invoked directly, = `installPlugin=false + rolloverPlugin=true`;
- Gateway healthy and no semantic/provider run active.

The one authorized installer command was invoked exactly once, returned nonzero, and was not retried. No manual repair, cleanup, rollover, uninstall/reset, semantic message, provider probe or third generation followed. This is the correct fail-closed behavior for Task 087.

## Root cause

The failure is a production PowerShell invocation-boundary defect, not a failure of the accepted Task-084/085/086 rollover/classification logic.

The accepted source constructs:

```powershell
$actionArgs = @("-Mode", [string]$classification.mode)
if ($pendingRollover) { $actionArgs += "-PendingRollover" }
if ($pluginAlreadyExact) { $actionArgs += "-PluginAlreadyExact" }
if ($SkipPlugin) { $actionArgs += "-SkipPlugin" }
$actionsJson = (& $actionResolver @actionArgs | Out-String)
```

Array splatting passes array elements as positional argument values. It does not reinterpret the string element `"-Mode"` as named-parameter syntax for the called script. Consequently `"-Mode"` is bound as the value of the first positional parameter `Mode`, and the resolver's `ValidateSet('fresh','legacy','upgrade')` rejects it.

The live error is therefore expected from the exact source:

`Cannot validate argument on parameter 'Mode'. The argument "-Mode" does not belong to the set "fresh,legacy,upgrade".`

## Preserved evidence

Do not redesign the accepted logic unnecessarily. The following remain accepted as source-side behavior:

- source-derived plugin fingerprint attestation;
- expected fingerprint bound through rollover plan/apply;
- explicit source equality for attested replacements;
- ordinary upgrade / pending recovery / already-exact classification truth table;
- lifecycle action resolver truth table;
- independent production install and rollover gates from Task 086;
- production AST regression proving rollover is outside `installPlugin` and before strict `resolve-plugin`;
- Task-082 npm-pack parser repair;
- Task-078/079/080 semantic/delivery/security lineage.

## Required successor direction

A source/test-only successor must repair only the PowerShell resolver invocation boundary before another live attempt is authorized.

Required behavior:

1. RED-reproduce the exact array-splat failure under Windows PowerShell 5.1 using the production resolver and production-shaped classification values.
2. Replace the fragile array-of-parameter-token invocation with a PowerShell-5.1-safe named-parameter mechanism, preferably hashtable splatting or an equally explicit named call.
3. Prove the production installer uses that corrected boundary.
4. Execute all lifecycle rows through the corrected boundary:
   - fresh -> install only;
   - legacy -> install only;
   - ordinary upgrade -> install + rollover;
   - pending upgrade -> rollover only;
   - already exact -> neither;
   - SkipPlugin -> neither;
   - pending+exact impossible -> fail closed.
5. Preserve Task-086 sibling gate and ordering AST invariants.
6. Preserve zero diff under `plugins/cogentnexus-openclaw/**`.
7. Run full Python/npm11/npm12/PowerShell/installer/semantic/baseline verification.

## Live state

The accepted live baseline remains the same bounded two-generation PASSTHROUGH topology. No further live installer attempt is authorized until the successor source repair is independently accepted.
