# CNX-20260917-377 — Composed Hook Registry Wiring Repair

## Purpose

Resolve the concrete gap proven by CNX-376:

`plugin api.on("before_agent_run") registration`
→ **missing host composed-registry visibility**
→ `hasHooks("before_agent_run") === false`
→ Dashboard dispatch skipped

CNX-374 repaired the conversation-hook access gate. CNX-376 proved that the repaired hook registration still does not become visible to the host composed registry consumed by the Dashboard selection runner.

## Parent

`CNX-20260917-376`

## Branch

`cnx-357-openai-dashboard-ticket-first-requalification-v2`

## Executor / Reviewer

Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`

## Starting authority

Begin from the authoritative branch HEAD and re-read `ACTIVE.md`, `STATUS.md`, this task, CNX-376 report, and CNX-374 report.

Before runtime conclusions, re-verify the effective installed artifact SHA-256 directly. CNX-376 report contains an artifact hash inconsistent with the previously verified CNX-374/CNX-375 repaired artifact identity; do not propagate that typo as evidence.

## Objective

Trace and repair the registry-composition lifecycle so dynamically registered plugin conversation hooks become visible to the same composed registry used by `getGlobalHookRunner()` and the Dashboard selection runner.

Required flow:

`OpenClaw loader`
→ `createApi(... hookPolicy ... )`
→ `plugin api.on()`
→ `plugin/host registry storage`
→ `initializeGlobalHookRunner(registry)`
→ `createComposedHookRegistryFacade(state)`
→ `getGlobalHookRunner()`
→ `hasHooks("before_agent_run")`

## Required investigation

Determine which concrete mechanism explains CNX-376's observed divergence:

1. registry instance mismatch;
2. registry replacement/reset after plugin registration;
3. composed facade excludes dynamically registered plugin hooks;
4. initialization/recomposition ordering;
5. plugin records are stored in a different registry collection;
6. another concrete host-side lifecycle mechanism.

Do not assume the two hypotheses from CNX-376. Prove the mechanism from source and, where possible, supported runtime evidence.

## Repair authority

A minimal source repair is authorized **only after** the causal registry-composition mechanism is proven.

The repair must:

- preserve OpenClaw's existing registry architecture;
- make the already-authorized `before_agent_run` registration visible to the composed runner registry;
- avoid changing TicketStore, admission semantics, provider/auth/routing, or Dashboard UI;
- avoid introducing a second admission path;
- avoid broad refactors.

## TDD / verification

Before the implementation fix:

- create or adapt a focused regression that reproduces the composed-registry failure;
- establish RED where practical;
- implement the smallest fix;
- establish GREEN.

Then run the relevant plugin tests/build/validation.

If runtime activation is required, restart only after the source/build evidence is green.

Do not perform Dashboard semantic requalification in this task by default.

## Semantic traffic

No Dashboard semantic request is authorized by default.

A semantic request may be used only if:

- the repaired registry composition cannot be verified by supported read-only/runtime diagnostics; and
- a single semantic probe is specifically justified in the report to confirm `hasHooks("before_agent_run")`/dispatch behavior.

Maximum: **1** additional Dashboard semantic request.

No retry and no second semantic request.

## Hard fences

- No provider/auth/routing/model changes.
- No TicketStore redesign.
- No admission redesign.
- No Dashboard UI/provider-layer changes.
- No controller normalization.
- No speculative patch.
- No broad refactor.
- No unrelated runtime mutation.
- No release/tag/main.
- No force-push/history rewrite.
- No historical edits to CNX-360 through CNX-376.
- Do not start CNX-378 yourself.

## Required report

Create:

`docs/operations/coordination/reports/CNX-20260917-377-composed-registry-wiring-repair-report.md`

Include:

- authoritative starting/final HEAD
- verified effective artifact hash
- exact source/line ranges
- proven root cause
- registry instance/composition lineage
- RED/GREEN regression evidence
- build/validation results
- runtime activation evidence if used
- semantic request count (0 or 1) and purpose
- classification:
  - `COMPOSED_REGISTRY_REPAIRED`
  - `INCONCLUSIVE`
  - `REPAIR_BLOCKED`
- remaining uncertainty
- hard-fence compliance

After report publication, set `ACTIVE.md` and `STATUS.md` to `WAITING_FOR_CHATGPT_REVIEW` and stop.
