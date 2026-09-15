# CNX-352 — Runtime Registration Observation Boundary

## Status
READY_FOR_HERMES

## Baseline
Parent baseline: `b4552f48fd733814afdf0523234103a158f7ac82`

## Objective
Find the smallest read-only observation boundary that can attribute CogentNexus plugin registration to the already-running OpenClaw Gateway process and distinguish registration completion from installed-plugin inventory.

Target chain:

```text
Gateway process
  -> plugin entry invocation
  -> releaseEntry.register(api)
  -> legacy register(runtimeApi)
  -> before_agent_run registration
  -> effective hook registry
```

## Required investigation

1. Verify GitHub remote branch and that baseline `b4552f48fd733814afdf0523234103a158f7ac82` is an ancestor before work. Local-only state is not evidence.
2. Inspect existing repository and OpenClaw read-only lifecycle/diagnostic seams for plugin registration invocation, runtime API identity, hook registration, registration counts, handler identity, effective hook registry, startup diagnostics, and lifecycle callbacks.
3. Trace these boundaries without modifying production behavior: A=`releaseEntry.register` entered; B=legacy `register(runtimeApi)` invoked; C=`before_agent_run` registration executed; D=`installManagedRuntimeGuards` completed; E=effective registry contains the CNX handler.
4. Investigate the Promise-returning branch in `v091-release-entry.ts` and whether registration visibility can be observed before/after Promise completion using an existing safe lifecycle seam.
5. Any process evidence must be tied to the actual OpenClaw Gateway process. Do not infer process binding from `openclaw plugins list --json`, file hashes, static imports, synthetic harnesses, or `hookCount=0`.
6. Use only read-only diagnostics and test-only adapters around existing seams. Do not add production instrumentation in CNX-352.
7. Record exact commands and outputs/errors. Do not install dependencies just to obtain a green test result.

## Classification

### D PROVEN
Only when an exact process-scoped observation demonstrates that the running Gateway loaded a stale/different CogentNexus module identity.

### E PROVEN
Only when exact runtime evidence demonstrates Dashboard/WebChat provider execution without invocation of `before_agent_run`.

### UNRESOLVED
Use when the required process-scoped boundary remains unavailable. Observability limitation is not a production defect.

## Hard fences
No production behavior changes, plugin install/reinstall, Gateway restart, provider invocation, provider-routing change, runtime/config/database mutation, Dashboard/WebChat UI interaction, CNX-344 replay/resend, change to `durableAdmissionEligible`, timeout authority, or admission ownership, v0.9.5 history/tag mutation, force-push/history rewrite, or self-acceptance.

## Final report
Create `docs/operations/coordination/reports/CNX-20260915-352-runtime-registration-observation-boundary-report.md` containing the exact starting remote HEAD, exact final GitHub HEAD, ancestry, seams inspected, exact commands/results, process-scoped observations, async-registration findings, D/E/UNRESOLVED classification, production-change declaration, hard-fence verification, and smallest next probe if unresolved.

## Completion
Commit and push the final report to this branch, independently verify the remote branch tip from GitHub, and read the report back from GitHub remote before declaring CNX-352 complete.
