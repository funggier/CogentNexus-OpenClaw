# CNX-20260917-379 — Disposable Registry Trace Harness

## Purpose

Resolve the contradiction left by CNX-378 without mutating the production OpenClaw runtime.

Known facts:

`PID 27372 / OpenClaw 2026.7.1-2 / effective CogentNexus artifact`
→ loaded plugin record reports `hookCount: 0`, `hookNames: []`

while the inspected OpenClaw source model indicates:

`api.on()`
→ registry mutation
→ `initializeGlobalHookRunner(registry)`
→ live composed facade
→ `hasHooks("before_agent_run")`

and therefore should expose dynamically registered hooks.

CNX-378 proved the contradiction remains correlated to one live runtime, but supported diagnostics cannot expose JavaScript object identity. No causal mechanism has therefore been proven.

## Parent

`CNX-20260917-378`

## Branch

`cnx-357-openai-dashboard-ticket-first-requalification-v2`

## Executor / Reviewer

Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`

## Objective

Build and run a **disposable, non-production diagnostic reproduction** that can directly observe registry object identity and hook flow at the following boundaries:

`plugin api.on()`
→ `registerTypedHook()`
→ plugin/host registry object
→ `initializeGlobalHookRunner(registry)` argument
→ `state.registry`
→ `collectLivePluginRegistries()`
→ `createComposedHookRegistryFacade()` getter
→ composed hook collection
→ `hasHooks("before_agent_run")`

The harness must determine whether the observed `hookCount: 0` is explained by:

1. distinct registry object instances;
2. registry replacement/reset;
3. registration into a collection excluded from composition;
4. plugin ownership/filtering exclusion;
5. initialization ordering/recomposition;
6. inventory projection differing from actual runner registry;
7. another concrete, directly observed mechanism.

## Required identity evidence

For every relevant registry/collection observed, record a stable diagnostic identity within the harness, such as:

- generated object token / WeakMap-assigned ID;
- creation site / lifecycle label;
- hook count before and after registration;
- plugin ownership metadata relevant to composition;
- whether the object is retired/replaced;
- identity equality comparisons between each lifecycle boundary.

The final report must provide an explicit identity matrix, for example:

| Boundary | Identity | Same as active registry? | Hook count | Notes |
|---|---|---:|---:|---|
| plugin registration target | R1 | yes/no | N | ... |
| initializeGlobalHookRunner arg | R2 | yes/no | N | ... |
| state.registry | R3 | yes/no | N | ... |
| collected live plugin registry | R4 | yes/no | N | ... |
| composed facade input | R5 | yes/no | N | ... |
| hasHooks query result | — | — | N | ... |

## Harness constraints

The reproduction must be clearly separated from the production gateway.

Preferred order:

1. copy/clone the exact OpenClaw installation/runtime files into a temporary disposable directory;
2. add temporary instrumentation only inside that disposable copy;
3. load the same effective CogentNexus artifact or a minimal fixture that performs the same `api.on("before_agent_run")` registration;
4. execute the relevant lifecycle in an isolated process;
5. remove/discard the temporary instrumented environment after collecting evidence.

Do not write instrumentation into the live installed OpenClaw tree.
Do not alter the production gateway process.
Do not restart/reload the production gateway.
Do not alter production configuration.

If an exact isolated reproduction cannot be built safely, stop at the point of failure and classify the diagnostic access limitation instead of patching production.

## Repository / source rules

No permanent source repair is authorized by this task.

Temporary harness code may be created under an explicitly disposable location only if it is not committed. No production OpenClaw dependency source may be changed in the repository or installed runtime.

Do not modify CogentNexus source except for a temporary fixture that is not committed and is clearly marked disposable.

Do not infer the production cause from an unvalidated synthetic fixture. The report must distinguish:

- directly observed production facts;
- isolated-harness facts;
- conclusions that are supported by both.

## Semantic traffic

No Dashboard semantic request.

No production model request.

No production Gateway restart/reload.

## TDD / validation

This is a diagnosis harness, not a repair task.

Required checks:

1. prove the harness itself can observe a known registry mutation and distinguish object identity;
2. run the exact or closest possible lifecycle under the isolated environment;
3. capture the identity matrix and hook visibility at each boundary;
4. compare harness results with CNX-376/CNX-378 production observations.

No speculative source fix is permitted.

## Hard fences

- No TicketStore/admission changes.
- No provider/model/auth/routing changes.
- No Dashboard UI/provider-layer changes.
- No production Gateway restart/reload.
- No production configuration changes.
- No production OpenClaw dependency patch.
- No permanent CogentNexus source patch.
- No semantic request.
- No broad refactor.
- No release/tag/main.
- No force-push/history rewrite.
- No historical edits to CNX-360 through CNX-378.
- Do not start CNX-380 yourself.

## Required report

Create:

`docs/operations/coordination/reports/CNX-20260917-379-disposable-registry-trace-harness-report.md`

Include:

- authoritative starting/final HEAD;
- production runtime identity reused from CNX-378;
- exact disposable environment and dependency identities;
- instrumentation points;
- complete registry identity matrix;
- hook counts at each boundary;
- plugin ownership/filter observations;
- direct evidence for or against each candidate mechanism;
- comparison with CNX-376 and CNX-378;
- explicit separation of production facts vs harness facts;
- classification:
  - `REGISTRY_LIFECYCLE_CAUSE_PROVEN`
  - `REGISTRY_INVENTORY_PROJECTION_CONTRADICTION_PROVEN`
  - `DIAGNOSTIC_HARNESS_INSUFFICIENT`

No repair classification is allowed in CNX-379.

After report publication, set `ACTIVE.md` and `STATUS.md` to `WAITING_FOR_CHATGPT_REVIEW` and stop.
