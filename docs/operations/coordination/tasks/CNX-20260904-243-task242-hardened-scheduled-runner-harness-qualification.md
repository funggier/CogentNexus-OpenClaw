# CNX-20260904-243 — Hardened Scheduled Runner Harness Qualification

## Status

`READY_FOR_HERMES`

## Purpose

Qualify a hardened one-off Windows Scheduled Task runner/evidence harness before any further live installer attempt.

Task 242 proved that the general Scheduled Task -> Windows PowerShell 5.1 -> script -> durable file channel works. Task 241 remains unclassifiable because its operator runner had no durable pre-child marker, no transcript/fallback log, and no `finally` result path.

This task repairs and qualifies **operator tooling only**. It does not modify or execute the CogentNexus-OpenClaw installer or product runtime.

## Authority

Repository: `funggier/CogentNexus-OpenClaw`

Branch: `agent/v0.9.3-full-stabilization`

Parent Task: `CNX-20260904-242`

Installer parent: `CNX-20260904-241`

Candidate-validation parent: `CNX-20260904-240`

Parent umbrella: `CNX-20260831-188`

Accepted Task-242 review verdict:

`ACCEPT_PASS_HARMLESS_CANARY_PROVES_EXECUTION_CHANNEL__TASK241_SPECIFIC_RUNNER_CHILD_BOUNDARY_UNRESOLVED__HARDENED_RUNNER_HARNESS_QUALIFICATION_REQUIRED`

Reviewed Task-242 report HEAD:

`1420fb8ae3c53deb0f99e1ce20c5192822ae91ba`

Exact executable candidate remains:

`18a51b15768fb3d2196e65f1ef470c34aeef7f36`

Candidate plugin fingerprint remains:

`1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`

No candidate install is authorized in this task.

## Fresh-authority rule

Before each phase and before any repository write:

1. Fetch current branch HEAD, `ACTIVE.md`, `STATUS.md`, this task, Task-242 report/review, and relevant Actions fresh from GitHub.
2. Fresh GitHub/repository evidence supersedes older prose.
3. If unexpected product/source/test/workflow drift appears, stop `BLOCKED_PREFLIGHT_DRIFT`.
4. Do not force-push or rewrite history.

## Preserved live boundary

Fresh Windows read-only evidence wins. Expected retained boundary is:

```text
controller = passthrough
generation = 39
candidate plugin not installed
Gateway = READY
provider/model/storage/recovery/delivery = READY
pending outbox = 0
SQLite integrity = ok
```

Retained Task-237 backup token:

`c6aaf93db7c34f718d01302477a292e1`

Do not clean or mutate historical Task-237/241/242 evidence.

## Phase A — Reconstruct Task-241 harness defect precisely

Read-only inspect the retained Task-241 runner and Task-242 forensic evidence.

Confirm the observed weakness:

```text
no durable runner-started artifact before child call
no explicit transcript/fallback log
result artifact only written after child returns
no finally fallback result
child invocation itself not durably recorded before launch
```

Record retained runner SHA/path and do not modify the Task-241 runner in place.

## Phase B — Build a new hardened disposable harness

Create a **new unique temp path** for Task 243. Do not overwrite Task-241/242 artifacts.

The hardened PowerShell 5.1 runner must, before invoking any child:

1. create the evidence root;
2. verify it is writable;
3. record a durable `runner-started.json` (or equivalent) containing:
   - schema/version marker;
   - runner SHA/path;
   - child executable/source path;
   - full ordered argument vector;
   - effective working directory;
   - Windows identity;
   - process ID;
   - UTC timestamp;
4. create/declare explicit transcript and fallback log paths.

Child execution requirements:

- capture stdout and stderr durably;
- preserve the exact child exit code when a child process launches and returns;
- distinguish a child-launch exception from a child nonzero exit;
- always enter a `finally` path that attempts to write `runner-result.json`;
- `runner-result.json` must include start/end timestamps, outcome category, child exit code if available, exception type/message if applicable, artifact paths, and whether transcript/fallback writes succeeded;
- propagate the intended terminal exit code to Task Scheduler **after** durable result capture.

Do not depend on the current working directory. Use absolute paths throughout.

The harness may be generated in temp by Hermes. Do not add it to production source in this task.

## Phase C — Direct harmless qualification

Before any Scheduled Task execution, validate the new runner with harmless synthetic child fixtures only.

At minimum prove these two direct cases:

### C1 — Child nonzero exit

Use a synthetic child that:

```text
writes a known stdout marker
writes a known stderr marker
exits with a known nonzero code (recommended 37)
```

Prove the runner records both streams, records exit code 37, writes `runner-result` from `finally`, and itself exits 37 only after artifacts are durable.

### C2 — Child launch exception

Use a deliberately nonexistent synthetic executable/path or equivalent harmless launch-failure fixture.

Prove:

```text
runner-started exists
outcome = child_launch_exception (or equivalent explicit category)
exception type/message captured
runner-result exists from finally
no product command was invoked
```

Do not interpret this case as a product failure; it is harness qualification only.

## Phase D — One scheduled failure-path canary maximum

Only after Phase C passes, register **one** harmless Scheduled Task using the hardened runner and a synthetic child fixture. Prefer the controlled nonzero child case because it verifies the critical failure path while still producing deterministic output.

Maximum budget:

```text
Task-243 harmless Scheduled Task registrations: 1
Task-243 harmless Scheduled Task starts: 1
Task-243 Scheduled Task retries after start: 0
```

Required scheduled proof:

```text
runner-started artifact exists before/independent of child completion
stdout marker captured
stderr marker captured
runner-result exists
child exit code preserved (e.g. 37)
Task Scheduler LastTaskResult coherently reflects the runner terminal code
transcript/fallback artifact exists or an explicit recorded transcript-write failure exists
identity/CWD/timestamps/source/args are durable
```

The canary must not invoke:

- `scripts/install.ps1`;
- any CogentNexus/OpenClaw CLI/runtime command;
- Gateway/provider/model operations;
- network calls;
- SQLite/Ticket/outbox/recovery writes;
- semantic messages.

## Phase E — Live-state preservation proof

After qualification, perform read-only health/state checks sufficient to prove the live boundary was not changed.

Expected:

```text
controller remains passthrough generation 39
candidate plugin remains not installed
Gateway/provider/model/storage/recovery/delivery remain READY
SQLite integrity remains ok
no new semantic lineage
Task-237 retained evidence unchanged
```

## Product zero budget

```text
scripts/install.ps1 invocations: 0
installer Scheduled Task registrations: 0
installer Scheduled Task starts: 0
rollover-prepare/finalize: 0
openclaw plugins install: 0
plugin mutation: 0
controller/Gateway/lifecycle mutation: 0
manual Ticket/outbox/recovery/SQLite writes: 0
```

## Semantic zero budget

```text
Dashboard semantic submissions: 0
Discord semantic submissions: 0
direct Discord/API sends: 0
semantic retries: 0
recovery replay/resend: 0
```

## Repository/source hard fence

Task 243 is tooling/qualification only.

Do not modify:

- `scripts/install.ps1`;
- plugin/runtime production source;
- tests/workflows;
- release/tag/assets;
- historical evidence.

Only coordination report publication is expected on the branch.

## Retry policy

- Direct harmless qualification steps may be repeated only when needed to correct the **new Task-243 disposable harness** itself, because they cannot produce product/semantic side effects. Record each materially different correction.
- Scheduled canary start budget is exactly one. Once it starts, do not start it a second time.
- Installer retry remains unauthorized regardless of Task-243 outcome.

## Required report

Publish exactly:

`docs/operations/coordination/reports/CNX-20260904-243-task242-hardened-scheduled-runner-harness-qualification.md`

Report must include:

- fresh GitHub authority;
- retained Task-241 runner weakness confirmation;
- Task-243 runner path/SHA and concise design;
- exact `runner-started`, transcript/fallback, stdout/stderr, and `runner-result` evidence schema/paths;
- direct nonzero-child proof;
- direct child-launch-exception proof;
- scheduled canary registration/start cardinality and LastTaskResult;
- live-state preservation proof;
- zero-product/zero-semantic ledger;
- exact report commit/HEAD and Actions state.

Then STOP for independent ChatGPT review.

## Allowed final dispositions

- `PASS_HARDENED_RUNNER_HARNESS_QUALIFIED`
- `BLOCKED_PREFLIGHT_DRIFT`
- `FAIL_DIRECT_NONZERO_CAPTURE`
- `FAIL_CHILD_LAUNCH_EXCEPTION_CAPTURE`
- `FAIL_SCHEDULED_HARNESS_QUALIFICATION`
- `FAIL_EXIT_CODE_PROPAGATION`
- `FAIL_LIVE_STATE_PRESERVATION`
- `BLOCKED_EVIDENCE`

Even on PASS, Task 243 does **not** authorize another installer attempt. A separate reviewed successor is required.
