# CNX-341 — Live Timeout Authority Provenance Diagnostic

- Parent: `CNX-340F`
- Branch: `agent/v0.9.6-live-timeout-authority-diagnostic`
- Executor: `Hermes`
- Reviewer: `ChatGPT`
- Human final authority: `Operator`
- Source failure under investigation: CNX-340F `FAIL — LEGACY_TIMEOUT_AUTHORITY_REMAINS`
- Known real call session: `agent:main:dashboard:945504d3-42f1-497a-b635-9975561e4bd5`

## Objective

Determine **why the live runtime direct-model-call lease produced `timeoutMs=900000`** during CNX-340F even though the repaired source in CNX-340A resolves runtime timeout authority and the reported artifact SHA was `c15b2f61a1596f301510e9cd392851ef99427c6c129d653d2d336cfefa79b3a8`.

This is a provenance diagnostic, not a repair and not a semantic requalification. The primary goal is to identify the exact runtime value/source that caused `900000`, and distinguish among:

1. stale installed artifact,
2. installed artifact mismatch despite matching reported hash,
3. Gateway loading a different file/path than expected,
4. runtime restart/load boundary not refreshed,
5. `event.timeoutMs` / `event.timeoutSeconds` or context timeout overriding config,
6. `api.config` / provider configuration shape differing from the expected runtime configuration,
7. another concrete runtime authority or wrapper supplying 900s.

Do not infer the cause from filenames, branch names, or report text. Prove it from live/read-only evidence wherever possible.

## Known source behavior to reconcile

The CNX-340A repair added `runtimeModelCallTimeoutMs(api, event, ctx)` to the `model_call_started` handler. Its precedence is:

1. `event.timeoutMs`
2. `event.timeoutSeconds`
3. `ctx.timeoutMs`
4. `ctx.timeoutSeconds`
5. `api.config.agents.defaults.timeoutSeconds`
6. `api.config.models.providers.<event.provider>.timeoutSeconds`
7. plugin config `timeoutSeconds`
8. legacy fallback `DIRECT_MODEL_CALL_TIMEOUT_MS = 900000`

The current repaired source on branch `agent/v0.9.6-direct-model-call-timeout-authority-repair` must be treated as reference evidence, not as proof that the live Gateway loaded it.

## Hard fences

- Read-only diagnostic by default.
- No new Dashboard session.
- Do not click `New session`.
- Do not send a semantic request.
- Do not perform another live model call.
- No retry, resend, recovery, fallback, or manual dispatch.
- No provider/model/config/timeout/controller/database mutation.
- No installation or Gateway restart during this task unless a later explicit successor task authorizes it.
- No production code or test changes.
- Do not modify `v0.9.5` or published history.
- Do not overwrite, force-push, or rewrite existing branches.
- If evidence is unavailable or contradictory, report `BLOCKED` rather than guessing.

## Required questions to answer

### A. What exact plugin artifact is loaded by the running Gateway?

Read-only establish:

- installed plugin path
- exact `v091-release-entry.js` path actually loaded, if observable
- exact SHA-256 of the file on disk
- plugin/package metadata and version
- any generated/build provenance available
- whether the file contains the repaired `runtimeModelCallTimeoutMs` implementation and the `timeoutMs: runtimeModelCallTimeoutMs(api,event,ctx)` call site

Do not treat the filename or package version as sufficient evidence.

### B. Was the Gateway process started before or after the repaired artifact existed?

Without restarting anything, capture what can be proven read-only about:

- active Gateway process identity
- process start time, if available
- plugin load/startup evidence, if available
- installed artifact modification time, if available
- relationship between process start and artifact installation/build timestamps

Do not infer causality solely from timestamps; state the evidence and remaining uncertainty.

### C. What timeout values are actually visible at the model-call hook boundary?

Use non-semantic instrumentation/diagnostic facilities already present in the repository/runtime if available. The objective is to identify, for the failing live path or an equivalent non-production diagnostic path, the values visible at the resolver boundary:

- `event.timeoutMs`
- `event.timeoutSeconds`
- `ctx.timeoutMs`
- `ctx.timeoutSeconds`
- `api.config.agents.defaults.timeoutSeconds`
- `api.config.models.providers.ollama.timeoutSeconds`
- plugin/runtime config timeout fields used by the resolver
- final value returned by `runtimeModelCallTimeoutMs()`

Do not add persistent production instrumentation. Prefer existing logging, read-only process/runtime inspection, or an isolated diagnostic harness that does not mutate production state.

### D. Reconcile the 900000ms outcome

Determine the narrowest proven explanation for:

`actual durable timeoutMs = 900000`

Classify the result as one of:

- `ROOT_CAUSE_PROVEN — STALE_RUNTIME_ARTIFACT`
- `ROOT_CAUSE_PROVEN — RUNTIME_LOAD_BOUNDARY`
- `ROOT_CAUSE_PROVEN — LIVE_TIMEOUT_INPUT_OVERRIDE`
- `ROOT_CAUSE_PROVEN — RUNTIME_CONFIG_SHAPE`
- `ROOT_CAUSE_PROVEN — OTHER_RUNTIME_AUTHORITY`
- `ROOT_CAUSE_NOT_PROVEN — EVIDENCE_INSUFFICIENT`

Do not use `STALE_RUNTIME_ARTIFACT` merely because the local repo branch differs from the task branch.

## Required evidence package

Publish a report containing:

- exact inspected branch/commit references
- installed plugin path and exact file SHA(s)
- source snippet/evidence for repaired resolver on the repair branch
- any observable Gateway process/load evidence
- all timeout inputs that could be observed
- exact resolver output if directly observed
- correlation to CNX-340F's `900000` lease
- explicit distinction between proven facts and hypotheses
- recommended next action, limited to the evidence-backed action

## Success criteria

### PASS

PASS only if the diagnostic identifies a concrete, evidence-backed cause for `900000` sufficient to select the next repair/requalification action without guessing.

### BLOCKED

BLOCKED if the runtime cannot expose enough evidence to distinguish the plausible causes safely. In that case, stop without semantic traffic or mutation and state the minimum evidence needed for the next task.

## Expected disposition

No code change is expected from CNX-341. If a code or configuration repair is indicated, document it as the next successor task rather than implementing it inside this diagnostic.

Publish:

`docs/operations/coordination/reports/CNX-20260914-341-live-timeout-authority-provenance-diagnostic-report.md`

Stop for independent ChatGPT review. Do not self-accept CNX-341.
