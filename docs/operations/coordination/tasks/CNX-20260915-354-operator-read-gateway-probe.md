# CNX-354 — Operator-Read Gateway Probe

## Status

READY_FOR_HERMES

## Repository

`funggier/CogentNexus-OpenClaw`

## Target branch

`cnx-354-operator-read-gateway-probe`

## Baseline

Parent baseline: `ad7bf9beed945d756b8d4ddbde732a2671a71432`

## Objective

Determine whether the currently available OpenClaw Gateway `operator.read` capability, if it can be used without broadening permissions or changing runtime state, exposes any trustworthy Gateway-side process-local plugin/runtime observation needed to continue the CNX-344 root-cause investigation.

CNX-353 established that `gateway call health` is Gateway-owned but coarse: it reports `plugins.loaded` without module identity, registration state, plugin-manager identity, or effective hook registry. `gateway probe` reported a read limitation due to missing `operator.read`.

The target question for CNX-354 is narrowly:

```text
Does an already-supported, read-only operator.read Gateway surface expose
process-local plugin/module/registration/hook state?
```

## Investigation boundary

Use only already-supported OpenClaw read/diagnostic mechanisms. Do not add production instrumentation, change authorization policy, create new RPCs, restart Gateway, or mutate any runtime/configuration state.

The evidence chain sought is:

```text
running Gateway PID
  -> Gateway-owned operator.read surface
  -> process-local runtime state
  -> CogentNexus module / registration state
  -> effective before_agent_run registry
```

## Required preflight

Verify GitHub remote state before any work. Local-only state is not authority.

```text
git remote -v
git fetch origin
git rev-parse origin/cnx-354-operator-read-gateway-probe
git merge-base --is-ancestor ad7bf9beed945d756b8d4ddbde732a2671a71432 origin/cnx-354-operator-read-gateway-probe
```

Record the exact results.

## Required investigation

### 1. Inspect the existing scope limitation

Re-run or inspect the existing read-only probe that reports:

```text
missing scope: operator.read
```

Identify from OpenClaw source/configuration exactly what this scope gates and whether there is an already-configured, documented way to exercise it without mutation.

Do not change scopes.

### 2. Inventory documented Gateway methods

Inspect:

```text
openclaw gateway call --help
```

and relevant OpenClaw source to determine whether any currently documented method is operator-read scoped and returns more than health/status metadata.

Do not infer capability from undocumented/private methods.

### 3. Search for existing operator-read implementation

Inspect OpenClaw code paths for terms such as:

```text
operator.read
operatorRead
scope
permission
authorization
gateway call
health
status
diagnostic
plugin
hook
runtime
registry
```

Classify each candidate as:

- Gateway-owned and process-local
- Gateway-owned but persisted/config-derived
- CLI-local inspection
- unsupported/private/internal

Only the first category can satisfy the process-local objective.

### 4. Test only an already-supported read path

If an operator-read path is already authorized and documented in the current environment, exercise it read-only.

The test must not:

- broaden permissions;
- edit config;
- issue a restart;
- install/reinstall plugins;
- invoke providers;
- interact with Dashboard/WebChat;
- mutate databases.

If the environment cannot exercise `operator.read`, record the exact denial/error and classify the limitation. Do not attempt privilege escalation or permission modification.

### 5. Process attribution

Any useful response must be attributable to the running Gateway process identified by OpenClaw, currently expected to be PID `17080`.

A response that does not carry Gateway process identity or clearly documents Gateway ownership is insufficient for D/E proof.

### 6. Registration state

Where possible, look specifically for:

```text
plugin registration invocation
loaded module URL/path
module/cache identity
plugin-manager instance
registration owner
registration count
before_agent_run hook identity
priority
registry membership
```

Do not accept:

```text
plugins list --json
plugins inspect --runtime
static source
installed file hashes
synthetic tests
```

as process-scoped evidence unless the implementation proves that the data comes from the running Gateway process.

## Classification rules

### OPERATOR-READ BOUNDARY FOUND

Use this only if a supported read-only operator-scoped Gateway surface is demonstrably Gateway-owned and exposes useful process-local runtime/plugin state.

This is an observability result, not a repair.

### D PROVEN

Only if an exact process-scoped observation shows that the running Gateway loaded a stale/different CogentNexus module identity from the expected identity.

### E PROVEN

Only if exact Gateway-side runtime evidence demonstrates Dashboard/WebChat provider execution without invocation of `before_agent_run`.

### UNRESOLVED / BLOCKED

Use when `operator.read` cannot be exercised safely in the current environment, or when available Gateway methods remain too coarse to expose process-local plugin state.

A missing permission or missing observability surface is not itself a production defect.

## Test constraint

A focused repository test may be attempted only if the existing environment already supports it. Record exact errors. Do not install dependencies just to manufacture a passing test.

## Hard fences

No production behavior changes; no production instrumentation; no install/reinstall; no Gateway restart/stop/start; no provider call; no provider-routing change; no permission/scope broadening; no runtime/configuration mutation; no database mutation; no Dashboard/WebChat UI interaction; no semantic request; no CNX-344 replay/resend; no `durableAdmissionEligible` change; no timeout-authority change; no new admission owner; no v0.9.5 tag/history mutation; no force-push; no history rewrite; no self-acceptance.

## Required final report

Create:

`docs/operations/coordination/reports/CNX-20260915-354-operator-read-gateway-probe-report.md`

The report must contain:

- exact starting remote HEAD;
- parent baseline and ancestry verification;
- exact final GitHub HEAD;
- Gateway PID/process identity;
- `operator.read` scope/authorization observation;
- documented and implemented Gateway methods inspected;
- exact commands and outputs/errors;
- any qualifying Gateway-owned process-local observation;
- D/E/OPERATOR-READ-BOUNDARY-FOUND/UNRESOLVED classification;
- production-change declaration;
- hard-fence verification;
- smallest next probe.

## Completion contract

Commit and push the final report to the target branch. Independently verify the branch tip from GitHub and read the final report back from GitHub remote before declaring CNX-354 complete.
