# CNX-20260917-378 — Live Registry Identity Correlation Diagnosis

## Purpose

Resolve the remaining contradiction from CNX-376 and CNX-377 by correlating the **exact live OpenClaw runtime**, the **effective loaded plugin artifact**, the **plugin load/registration event**, and the **registry object consumed by the global composed hook runner**.

Known evidence:

`CNX-376`: live Dashboard runtime reported `hookCount: 0`, `hookNames: []`, and the selection runner skipped `before_agent_run` because `hasHooks("before_agent_run")` was false.

`CNX-377`: source tracing of the currently installed OpenClaw 2026.7.1-2 dependency found a live-registry composition design in which `initializeGlobalHookRunner(registry)` stores the registry and the composed facade dynamically composes the active registry with live plugin registries. No repository-side repair could therefore be justified.

The remaining problem is not yet a proven fixable source defect. It is an **evidence correlation gap** between the exact runtime observed by CNX-376 and the source/runtime model inspected by CNX-377.

## Parent

`CNX-20260917-377`

## Branch

`cnx-357-openai-dashboard-ticket-first-requalification-v2`

## Executor / Reviewer

Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`

## Starting authority

Begin from the authoritative branch HEAD and re-read:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`
- this task
- CNX-376 report
- CNX-377 report
- CNX-374 report where artifact identity is relevant

Before any runtime conclusion, hash the effective installed plugin artifact directly from disk.

Trusted repaired artifact SHA-256 lineage:

`2841b704ad1c923ba643ca885eaf1d34e2f9565350d501c9d4895746d56c2d95`

Do not copy an artifact hash from CNX-376 or any unverified pasted output.

## Objective

Produce evidence sufficient to answer all of the following for **one exact runtime instance**:

1. Which OpenClaw process/PID is being observed?
2. Which exact OpenClaw build/module files are loaded by that process?
3. Which exact CogentNexus plugin artifact is loaded by that process?
4. Which plugin registry object receives the `api.on("before_agent_run")` registration?
5. Which registry object is stored in global hook-runner state by `initializeGlobalHookRunner(registry)`?
6. Are those registry objects the same object, distinct objects, or otherwise connected through the composition mechanism?
7. At the moment `hasHooks("before_agent_run")` is queried, which registry collection is actually being composed?
8. Can the CNX-376 `hookCount: 0` observation be reproduced against that same exact runtime/build/artifact combination?

The result must either identify a concrete mechanism or conclusively narrow the contradiction to a specific unobserved boundary.

## Required investigation

Trace and correlate the following chain with evidence:

`Gateway process`
→ `loaded OpenClaw module/build identity`
→ `plugin loader`
→ `createPluginRegistry`
→ `createApi(... hookPolicy ...)`
→ `plugin register(api)`
→ `api.on("before_agent_run")`
→ `registerTypedHook / registry mutation`
→ `activatePluginRegistry / setActivePluginRegistry`
→ `initializeGlobalHookRunner(registry)`
→ `state.registry`
→ `createComposedHookRegistryFacade(state)`
→ `getGlobalHookRunner()`
→ Dashboard selection runner
→ `hasHooks("before_agent_run")`

Use supported diagnostic mechanisms and source correlation. A process-local diagnostic technique is preferred when it can observe object identity without changing production behavior.

Potential acceptable approaches include, where supported and safe:

- Node inspector/debugger observation of a running process;
- diagnostic evaluation of loaded module state;
- a disposable reproduction using the exact installed OpenClaw package and effective plugin artifact, provided it does not masquerade as the live production runtime;
- targeted temporary instrumentation in a disposable copy/worktree, clearly separated from the actual runtime;
- runtime logs or diagnostics that expose registry lifecycle and identity.

Do not assume any one approach works. Report exactly what was observable.

## Runtime safety

- Do not modify the live OpenClaw installation merely to obtain evidence.
- Do not overwrite or replace the active plugin artifact.
- Do not alter user configuration permanently.
- Do not restart the production Gateway unless a later task explicitly authorizes it; this task is diagnosis-only by default.
- Do not send a Dashboard semantic request.
- Do not invoke a model/provider request merely as a probe.
- Do not attach a debugger in a way that mutates application state beyond passive inspection.
- Do not patch OpenClaw source or dependency code.

## TDD / repair boundary

This task is **diagnosis-only**.

No source repair is authorized unless a concrete repository-side defect is independently proven by the evidence produced in this task and the task is explicitly extended by a new authorization commit. Do not invent a RED test merely to justify a patch.

A focused regression may be added only if it documents a genuinely reproducible repository-side behavior and remains read-only/diagnostic.

## Semantic traffic

Dashboard semantic traffic: **0 authorized / 0 expected**.

No semantic probe is necessary for this task. The objective is runtime identity correlation, not end-to-end requalification.

## Hard fences

- No OpenClaw dependency patch.
- No speculative plugin patch.
- No TicketStore changes.
- No admission changes.
- No provider/auth/routing/model changes.
- No Dashboard UI/provider-layer changes.
- No controller normalization.
- No production configuration changes.
- No production Gateway restart/reload by default.
- No semantic request.
- No broad refactor.
- No release/tag/main.
- No force-push/history rewrite.
- No historical edits to CNX-360 through CNX-377.
- Do not start CNX-379 yourself.

## Required evidence

Record, at minimum:

- authoritative starting/final HEAD;
- effective plugin artifact path and freshly computed SHA-256;
- OpenClaw process/PID if a live process is inspected;
- OpenClaw package/build identity and relevant module paths/hashes;
- plugin load identity;
- registry object identity evidence, using safe object identity markers such as stable object references or equivalent supported diagnostics;
- plugin registration event evidence;
- global runner registry identity evidence;
- composed-registry membership evidence at the exact observation point;
- whether CNX-376's `hookCount: 0` can be reproduced or explained;
- explicit distinction between live-runtime evidence and disposable reproduction evidence;
- zero semantic requests;
- hard-fence compliance.

## Classification

Use exactly one:

- `LIVE_REGISTRY_IDENTITY_CORRELATED`
- `LIVE_REGISTRY_IDENTITY_CONTRADICTION_UNRESOLVED`
- `DIAGNOSTIC_ACCESS_BLOCKED`

Do not claim a source root cause or repair unless directly proven.

## Required report

Create:

`docs/operations/coordination/reports/CNX-20260917-378-live-registry-identity-correlation-diagnosis-report.md`

After report publication:

- set `ACTIVE.md` to `WAITING_FOR_CHATGPT_REVIEW`;
- set `STATUS.md` to `WAITING_FOR_CHATGPT_REVIEW`;
- stop immediately;
- do not create CNX-379.
