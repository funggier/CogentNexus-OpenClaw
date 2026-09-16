# CNX-20260916-371 — Dashboard Runner Admission Boundary Repair Report

## Disposition

**BLOCKED / DIAGNOSIS INCONCLUSIVE — NO REPAIR PERFORMED**

The exact host source path was inspected from the active installed OpenClaw `2026.7.1-2` runtime. Source evidence establishes the Dashboard gateway entrypoint and the embedded selection runner's hook-dispatch location, but the available read-only evidence does not prove the runtime condition that caused the registered CogentNexus handler not to be invoked for CNX-370. Per the task hard fence, no guessed repair, runtime mutation, or semantic request was performed.

## GitHub authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Starting remote HEAD: `418d4a8302548491f161dafd1ec19b8af2826732`
- Final remote HEAD before publication: `418d4a8302548491f161dafd1ec19b8af2826732`
- Worktree: clean before report creation; only this report and coordination-state edits are task changes.

## Diagnosis evidence

### Dashboard entrypoint

The installed runtime's `message-handler-CzwI6JjW.js` dispatches the Gateway `agent` request and passes `isWebchatConnect` and the request context into the agent handler. The installed `agent-D6kiZtPt.js` defines the `agent` handler and starts the Gateway agent execution asynchronously. The Dashboard's WebChat/control-UI request therefore enters through the Gateway `agent` handler, not through the CLI runner.

Installed source hashes:

| Artifact | SHA-256 |
|---|---|
| `message-handler-CzwI6JjW.js` | `ce8653d5e612bb6b3ec28eb57b9762303de4ca3eeee8b41397d76e77604ef121` |
| `agent-D6kiZtPt.js` | `06a0b478abf02cdb542cc14a3641b57def58677d8d6eadd0ffe58ac063f940df` |
| `selection-JInn13lc.js` | `ccff13111aa60369ac9d88b526a58a7df1f733f1d99d205c01c6186036957e66` |

### Runner path

The active Dashboard execution path reaches the embedded selection runner in `selection-JInn13lc.js` (`runEmbeddedAttempt`). That runner records `prompt.submitted` immediately before calling `promptActiveSession(...)` and records model completion downstream. The installed source contains a `before_agent_run` dispatch block immediately before that prompt submission:

- `selection-JInn13lc.js:13922-13968`: conditional `hookRunner?.hasHooks("before_agent_run")`, then `hookRunner.runBeforeAgentRun(...)`, then block handling.
- `selection-JInn13lc.js:13969+`: prompt submission/model execution continues only when the gate did not block.

The normal CLI runner independently dispatches the same hook in `cli-runner-DE2P2Dy_.js:773-...`, confirming that hook dispatch is runner-specific rather than universally applied by the Gateway request entrypoint.

### Registration versus invocation

The repository's active plugin source registers `before_agent_run` through `api.on` in `plugins/cogentnexus-openclaw/src/index.ts:752-753`, guarded only by `config.preInferenceAdmission !== false`. The existing CNX-368/CNX-369 evidence proves registration/activation. The installed selection runner source proves that its code has a dispatch site, but CNX-370 proves no invocation trace for the Dashboard request.

The remaining unresolved boundary is therefore the runtime state of the selection runner's `hookRunner` at `selection-JInn13lc.js:13922`: whether the runner received the global hook registry and whether that registry reported the CogentNexus handler at the exact Dashboard execution boundary. Static source alone cannot distinguish `hookRunner` absent, `hasHooks("before_agent_run") === false`, or a different request/runner path that produced the observed trajectory. No runtime instrumentation or mutation was authorized merely to guess among these cases.

### First divergence

Observed CNX-370 first divergence remains after `prompt.submitted`: no `before_agent_run`, no `admission.trace.*`, and direct model completion. The source path has a dispatch opportunity before model execution, but the supplied runtime evidence does not identify which condition prevented the invocation.

## Root cause classification

**Inconclusive host-runner hook-registry boundary.** It is not justified to classify this as embedded-runner bypass, app-server bypass, selection-runner bypass, or plugin-registration loss without a runtime observation of the selected runner and its hook registry at the dispatch boundary.

## Source changes and hashes

No production source files were changed. No regression test was added because the concrete failing boundary is not yet identified and adding a test for an assumed condition would violate the evidence-first gate.

Repository source hashes at final pre-publication verification:

| File | SHA-256 |
|---|---|
| `plugins/cogentnexus-openclaw/src/index.ts` | `352c323ac75b8eb8a190b5fe3cda1e644679525b44f3f034e4622e07b67fe5ba` |
| `plugins/cogentnexus-openclaw/src/v091-release-entry.ts` | `f033b4a588421da097d3db0f8247e741c1de5cf8782cadcbfb2db993840e6a9a` |
| `plugins/cogentnexus-openclaw/src/v091-final-entry.ts` | `7b20c7e8a1eea08cc260350a31e883f69cf543da03f480ff5970050cf998e947` |

Before/after production hash delta: **none**.

## RED/GREEN and validation

- Focused RED regression: **NOT RUN** — no proven repair target exists.
- GREEN regression: **NOT RUN**.
- Plugin test suite: **NOT RUN**; no source repair was made.
- Full test suite: **NOT RUN**.
- Build: **NOT RUN**.
- Plugin validation/static checks: source inspection only; no repair claim.
- Runtime activation/reload: **0**.
- Semantic Dashboard request: **0**.

## Runtime activation and semantic evidence

No process was restarted or reloaded. No artifact was installed or changed. No semantic request was sent. CNX-370 remains the latest semantic evidence and remains `FAIL / NOT_REQUALIFIED`.

## Hard-fence compliance

- No provider, auth, routing, model, or semantic-contract changes.
- No Dashboard-only admission path and no duplicated Ticket path.
- No manual controller normalization.
- No unrelated Dashboard traffic.
- No historical CNX-360–CNX-370 edits.
- No release/tag/main change.
- No force-push or history rewrite.
- No broad refactor.
- No claim that Ticket-first was restored.
- No CNX-372 or semantic requalification started.

## Remaining uncertainty and required next evidence

A supported, read-only runtime observation is required at the selection runner dispatch boundary, capturing: selected runner identity, `hookRunner` presence, `hasHooks("before_agent_run")`, plugin ID/registration snapshot, and the exact request/run correlation. Until that evidence is available, the smallest justified repair cannot be selected safely.

## Recommended next state

`WAITING_FOR_CHATGPT_REVIEW`

*Report generated by Hermes Agent for CNX-20260916-371. Diagnosis stopped at the hard fence because the concrete runtime cause was not proven.*
