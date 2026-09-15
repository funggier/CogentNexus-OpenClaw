# CNX-352 — Runtime Registration Observation Boundary

## Status

READY_FOR_HERMES

## Repository

`funggier/CogentNexus-OpenClaw`

## Target branch

`cnx-352-runtime-registration-observation-boundary`

## Baseline

- Parent baseline: `cnx-351-process-scoped-runtime-introspection`
- Starting HEAD: `b4552f48fd733814afdf0523234103a158f7ac82`

## Objective

Continue the CNX-351 investigation by finding the smallest **read-only, process-relevant observation boundary** for CogentNexus registration inside the already-running OpenClaw Gateway.

The target evidence chain is:

```text
OpenClaw Gateway process
  -> plugin entry invocation
  -> releaseEntry.register(api)
  -> legacy register(runtimeApi)
  -> before_agent_run registration
  -> effective hook registry
```

CNX-351 established that the Windows process can be identified as Gateway PID `17080`, while JavaScript module identity, live registration invocation, and effective hook registry remain unobservable through the currently available external surfaces.

## Source seam to investigate

`plugins/cogentnexus-openclaw/src/v091-release-entry.ts`

Relevant behavior:

1. `releaseEntry.register(api)` checks Host authority.
2. It resolves the legacy `register` function from `v091-final-entry.js`.
3. It builds the fenced `runtimeApi`.
4. It calls `const registered = register(runtimeApi)`.
5. `installV097DirectRecoveryStartupLiveness(api, config)` runs during registration.
6. If `registered` is Promise-like, `installManagedRuntimeGuards` is deferred until resolution.
7. Otherwise `installManagedRuntimeGuards` executes immediately.

## Required investigation

### 1. GitHub-first verification

Verify the remote branch and ancestry before any work. Local-only state is not evidence.

```text
git fetch origin
git rev-parse origin/cnx-352-runtime-registration-observation-boundary
git merge-base --is-ancestor b4552f48fd733814afdf0523234103a158f7ac82 origin/cnx-352-runtime-registration-observation-boundary
```

### 2. Identify existing observation seams

Search the repository and installed OpenClaw surfaces for already-supported, read-only mechanisms exposing any of:

- plugin registration invocation
- plugin runtime API identity
- hook registration return values
- handler identity
- registration count
- effective hook registry
- startup/plugin lifecycle diagnostics
- runtime debug/inspection endpoints
- logger output already emitted during registration
- OpenClaw plugin lifecycle callbacks

Do not add instrumentation until existing seams have been exhausted.

### 3. Trace the real registration lifecycle

Determine, from source and existing runtime diagnostics, whether the following events can be distinguished:

```text
A = releaseEntry.register entered
B = legacy register(runtimeApi) invoked
C = before_agent_run registration executed
D = installManagedRuntimeGuards completed
E = effective hook registry contains CNX handler
```

Explicitly separate static source evidence from process-scoped runtime evidence.

### 4. Async registration boundary

Pay particular attention to the Promise branch:

```text
const registered = register(runtimeApi)
if (registered && typeof (registered as Promise<void>).then === "function") {
  return Promise.resolve(registered).then(installManagedRuntimeGuards)
}
installManagedRuntimeGuards()
```

Determine whether the available OpenClaw plugin lifecycle can observe Promise-returning registration and whether hook visibility can be sampled before and after completion without changing behavior.

Do not alter this code in CNX-352.

### 5. Process-scoped attribution

Any useful observation must be tied to the actual Gateway process. Do not infer process binding from installed plugin inventory, file hashes, static `register()` paths, synthetic harnesses, or `hookCount=0` from `openclaw plugins list --json`.

### 6. Test strategy

Allowed:

- read-only source tests
- test-only loader/adapter around an existing registration seam
- existing runtime diagnostics

Not allowed:

- production behavior changes
- OpenClaw restart
- plugin install/reinstall
- provider calls
- Dashboard/WebChat semantic requests
- database mutation
- config/runtime mutation

If testing is blocked, record the exact command and error. Do not install dependencies merely to force a green result.

## Classification rules

### D PROVEN

Only if an exact process-scoped observation shows the running Gateway loaded a stale/different CogentNexus module identity than expected.

### E PROVEN

Only if an exact runtime observation proves Dashboard/WebChat can reach provider execution while `before_agent_run` was not invoked.

### UNRESOLVED

Use when the required process-scoped observation boundary remains unavailable.

Do not convert an observability limitation into a production defect.

## Hard fences

Do not modify production runtime behavior, install/reinstall the plugin, restart OpenClaw, invoke a provider, change provider routing, mutate runtime/configuration or databases, interact with Dashboard/WebChat UI, replay/resend CNX-344, change `durableAdmissionEligible`, change timeout authority, create another admission owner, mutate the v0.9.5 tag/history, force-push, rewrite history, or self-accept the task.

## Required final report

Create:

`docs/operations/coordination/reports/CNX-20260915-352-runtime-registration-observation-boundary-report.md`

The report must include exact starting remote HEAD, exact final GitHub HEAD, parent baseline and ancestry verification, source seams inspected, runtime/diagnostic seams inspected, exact commands/results, Gateway process identity if revalidated, process-scoped registration observations, effective hook registry observations, async registration findings, D/E/UNRESOLVED classification, production-change declaration, hard-fence verification, and the smallest next probe if unresolved.

## Completion contract

Task is not complete until the final report is committed, pushed, and read back from GitHub remote. The GitHub branch tip must be independently verified after publication.
