# CNX-20260917-380 — Exact Isolated OpenClaw Registry Trace

## Purpose

Resolve the contradiction left by CNX-378 and CNX-379 by executing the exact OpenClaw `2026.7.1-2` loader/module graph and the effective CogentNexus plugin artifact in a **non-production isolated process** with temporary instrumentation.

The objective is diagnosis only. Do not patch production or claim a production root cause from a synthetic model.

## Parent

`CNX-20260917-379`

## Branch

`cnx-357-openai-dashboard-ticket-first-requalification-v2`

## Executor / Reviewer

Executor: Hermes
Reviewer: ChatGPT
Human final authority: Operator

## Starting authority

Begin from authoritative branch HEAD. Re-read:

- `ACTIVE.md`
- `STATUS.md`
- this task
- CNX-379 report
- CNX-378 report
- CNX-376 report

Re-verify the effective installed CogentNexus artifact SHA-256 directly before using it as evidence. Expected previously verified value:

`2841b704ad1c923ba643ca885eaf1d34e2f9565350d501c9d4895746d56c2d95`

Do not use the CNX-376 typo as evidence.

## Objective

Run the **actual installed OpenClaw module graph** corresponding to production OpenClaw `2026.7.1-2` in an isolated process/environment, loading the effective CogentNexus artifact without connecting to the production Gateway.

Instrument the exact runtime references along this path:

`loader`
→ `createPluginRegistry`
→ plugin load / `createApi`
→ `api.on("before_agent_run")`
→ registration target
→ `activatePluginRegistry`
→ `setActivePluginRegistry`
→ `initializeGlobalHookRunner(registry)`
→ `state.registry`
→ `collectLivePluginRegistries()`
→ `createComposedHookRegistryFacade(state)`
→ `getGlobalHookRunner()`
→ `hasHooks("before_agent_run")`

The trace must use the real OpenClaw functions/modules, not a reimplementation of their semantics.

## Isolation requirements

- Must not attach to or mutate production PID `27372`.
- Must not restart or reload production Gateway.
- Must not change production config.
- Use a temporary directory/process and disposable configuration/state.
- Temporary instrumentation may be applied to a disposable copy of installed OpenClaw or through a controlled preload/loader shim, provided the exact module graph and real functions execute.
- Do not modify the repository source permanently.
- Do not commit instrumentation.

## Required evidence

Capture:

1. Exact OpenClaw package version and module file hashes used by the harness.
2. Exact CogentNexus artifact path and SHA-256.
3. Process PID for the isolated run.
4. Stable WeakMap identity tokens for each actual registry object encountered.
5. Hook counts before/after `api.on` registration.
6. Identity equality checks between registration registry, initialized registry, `state.registry`, live registry collection members, and composed facade inputs.
7. Retirement state and ownership/filter state where applicable.
8. `hasHooks("before_agent_run")` result at the exact real runner.
9. Any inventory projection produced by the real OpenClaw loader in the isolated run, if available.
10. Exact ordering/timestamps sufficient to establish whether reset/replacement/recomposition occurs.

## Root-cause decision

Only classify a production mechanism as proven when the exact isolated execution reproduces the observed CNX-376 condition (`hook registration occurred` while the real runner/inventory reports no visible hook) and the trace identifies the concrete transition causing it.

Potential outcomes include:

- registry instance mismatch;
- registry replacement/reset;
- collection/composition exclusion;
- ownership/filter rejection;
- initialization ordering/recomposition;
- inventory projection differs from actual runner registry;
- another concretely observed mechanism.

If exact isolated execution still does not reproduce the condition, classify the contradiction as unresolved rather than inventing a cause.

## Repair authority

**No repair is authorized in CNX-380.**

Even if the exact mechanism is discovered, stop after evidence capture unless the task explicitly reaches the documented handoff point and receives a new authorization in a successor task.

## Semantic traffic

No Dashboard semantic request.
No production model request.

## Hard fences

- No production Gateway restart/reload.
- No production config mutation.
- No OpenClaw dependency patch in production.
- No CogentNexus source patch.
- No TicketStore/admission/provider/model/auth/routing/Dashboard UI changes.
- No semantic request.
- No speculative repair.
- No permanent instrumentation.
- No broad refactor.
- No release/tag/main.
- No force-push/history rewrite.
- No historical edits to CNX-360 through CNX-379.
- Do not start CNX-381 yourself.

## Required report

Create:

`docs/operations/coordination/reports/CNX-20260917-380-exact-isolated-openclaw-registry-trace-report.md`

Include:

- authoritative starting/final HEAD;
- exact isolated process identity;
- OpenClaw package/module identities and hashes;
- CogentNexus artifact identity/hash;
- instrumentation method;
- real registry identity matrix;
- real hook-count transitions;
- real composition/runner observation;
- inventory projection if available;
- exact causal transition if reproduced;
- production-vs-isolated evidence boundary;
- remaining uncertainty;
- hard-fence compliance.

Classification must be one of:

`EXACT_REGISTRY_LIFECYCLE_CAUSE_REPRODUCED`

`EXACT_LIFECYCLE_STILL_CONTRADICTORY`

`EXACT_ISOLATION_NOT_ACHIEVED`

After report publication, set `ACTIVE.md` and `STATUS.md` to `WAITING_FOR_CHATGPT_REVIEW` and stop.
