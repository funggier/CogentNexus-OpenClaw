# CNX-20260916-372 — Selection Runner Hook Registry Runtime Observation

## Task identity

- **Task ID:** CNX-20260916-372
- **Parent:** CNX-20260916-371
- **State:** `CNX372_SELECTION_RUNNER_HOOK_REGISTRY_RUNTIME_OBSERVATION`
- **Executor:** Hermes
- **Reviewer:** ChatGPT
- **Human final authority:** Operator
- **Branch:** `cnx-357-openai-dashboard-ticket-first-requalification-v2`

## Objective

Resolve the remaining CNX-371 uncertainty with a supported, bounded, read-only runtime observation at the exact Dashboard selection-runner hook dispatch boundary.

CNX-371 established from installed OpenClaw `2026.7.1-2` source that the Dashboard reaches the embedded selection runner and that the runner contains a `before_agent_run` dispatch site immediately before prompt/model execution. CNX-370 established that the live Dashboard request produced no `before_agent_run` evidence. CNX-371 could not distinguish among:

1. `hookRunner` absent/null at the dispatch boundary;
2. `hookRunner` present but `hasHooks("before_agent_run") === false`;
3. a different execution path/runner being used at runtime despite the static path inspection;
4. another concrete host condition preventing the registered handler from being invoked.

This task exists to distinguish those cases using runtime evidence, without modifying production source or changing application behavior.

## Required preflight

1. Synchronize with remote branch before any action.
2. Confirm `ACTIVE.md`, `STATUS.md`, this task, and CNX-371 report authorize this exact task.
3. Confirm current Gateway process identity and that no unrelated activation is occurring.
4. Confirm the installed OpenClaw version remains `2026.7.1-2`.

## Required observation

Obtain a process-scoped, read-only observation at the actual selection runner dispatch boundary, correlated to a controlled Dashboard execution context without performing a semantic Dashboard request unless absolutely necessary.

The observation must capture, where technically exposed:

- selected runner identity;
- exact `runEmbeddedAttempt` invocation context;
- `hookRunner` presence/type;
- `hasHooks("before_agent_run")` result;
- the registered hook/plugin identity or registry snapshot at that boundary;
- whether `runBeforeAgentRun(...)` is called;
- the call's return/decision if observable;
- exact session/run/trace correlation;
- process identity and artifact identity;
- timestamps sufficient to establish ordering.

Prefer supported Node/host diagnostics, debugger/inspector read-only inspection, existing diagnostic hooks, or other non-mutating runtime introspection. Do not inject persistent monkey patches or alter production behavior merely to expose the answer.

## No-semantic-default rule

A Dashboard semantic request is **not authorized by default** in CNX-372. The task is observation-only.

If the available supported observation mechanism cannot attach without a live execution context, one single minimum-necessary controlled request may be used solely to trigger the already-observed boundary, provided the report explicitly records why it was required. Do not use the request as a semantic requalification and do not judge Ticket-first behavior in this task.

## Decision criteria

Classify the boundary only from evidence:

- **REGISTRY_ABSENT:** selected runner has no usable hook registry at the dispatch site.
- **HOOK_NOT_REGISTERED:** registry exists but `hasHooks("before_agent_run") === false` for the active plugin state.
- **RUNNER_PATH_MISMATCH:** observed runtime executes a different runner/path than the inspected selection path.
- **DISPATCH_SUPPRESSED:** registry reports the hook but runtime does not invoke `runBeforeAgentRun(...)` under the observed conditions.
- **DISPATCH_REACHED:** `runBeforeAgentRun(...)` is actually invoked; if so, collect the returned decision/handler effects to identify the next boundary.
- **INCONCLUSIVE:** evidence cannot distinguish the cases; stop without repair.

Do not collapse registration and invocation into one conclusion.

## Hard fences

- Read-only diagnosis only; no source changes.
- No provider/auth/routing/model changes.
- No configuration redesign or controller normalization.
- No plugin reinstall/reload/restart unless a supported diagnostic attachment intrinsically requires it; if so, it must be separately justified and recorded.
- No semantic requalification.
- No repeated Dashboard requests.
- No historical edits CNX-360 through CNX-371.
- No release/tag/main changes.
- No force-push or history rewrite.
- No guessed repair.
- Do not modify the Dashboard UI or provider layer.

## Reporting

Publish:

`docs/operations/coordination/reports/CNX-20260916-372-selection-runner-hook-registry-runtime-observation-report.md`

Report must include exact evidence, process/artifact identity, observation method, correlation IDs, boundary classification, remaining uncertainty, and hard-fence compliance.

If and only if the evidence proves a repair target that should be handled by a separate task, state the exact repair target; do not implement it here.

After publishing the report, transition coordination to `WAITING_FOR_CHATGPT_REVIEW` and stop. Do not start a repair or semantic requalification task yourself.
