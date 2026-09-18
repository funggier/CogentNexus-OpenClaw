# CNX-20260918-406 — ChatGPT Review

## Decision

`ACCEPTED`

Accepted classification:

`OLLAMA_VERTICAL_SLICE_MAPPED_READY_FOR_RED_TEST`

## Review basis

Independent review re-read the authoritative CNX-406 task, report, current branch state, and the critical repository boundaries named by the report.

Verified directly:

- `v090-model-selection-boundary.test.ts` passes `sessions.patch { key, model }` through the CNX runtime-safety proxy and explicitly verifies that model changes do not create or mutate CNX Ticket state.
- `v091-release-entry.ts` keeps provider routing outside CogentNexus, installs the CNX continuity/recovery observers only after Host authority is accepted, and exports `hooks.allowConversationAccess: true`.
- `v091-direct-model-call-lease.ts` observes `model_call_started`, `model_call_ended`, and `agent_end`, recording provider/model metadata without becoming a provider router.
- `cnx374-registry-wiring.test.ts` proves only plugin-side registration through a mocked `api.on` surface. It does not prove membership in the real OpenClaw composed live hook registry.

The report correctly distinguishes:

1. OpenClaw-native provider/model/session routing, which should be reused;
2. CogentNexus continuity/admission, whose live registration/composed-registry boundary remains the practical defect;
3. live qualification items that were deliberately not exercised under CNX-406 hard fences.

No provider router should be added to CogentNexus.

## Review correction / refinement

The report's proposed two-turn `sessions.patch` / Agent Core continuity test is useful, but it is one layer above the earliest already-proven defect.

The first successor RED characterization should target the narrower boundary:

```text
CogentNexus plugin definition/register(api)
    -> OpenClaw plugin loader / host registry
    -> composed hook registry
    -> hasHooks("before_agent_run")
```

The test must distinguish:

- plugin code calling `api.on("before_agent_run", ...)`;
- host acceptance of that hook;
- final visibility to the composed/global hook runner.

A mocked `api.on` array is insufficient because CNX-374 already proves that local registration call path.

Once this boundary is RED/GREEN, the two-turn same-session model-switch continuity test becomes the next repository integration layer, followed by explicitly authorized live Web Chat qualification.

## Successor direction

The next bounded task should be repository-first and avoid production semantic traffic.

Priority order:

1. obtain/reuse an OpenClaw 2026.7.1-2 loader/registry integration seam;
2. add a failing integration characterization proving whether the exported CogentNexus entry becomes visible to the composed hook registry as `before_agent_run`;
3. if reproducible in repository tests, make the smallest CogentNexus-side repair that preserves OpenClaw ownership and turns the test GREEN;
4. run focused/full plugin validation and exact-SHA CI where available;
5. defer live Gateway/Dashboard proof to a separately authorized local/live task.

If the real composed registry cannot be represented through repository-accessible public/test APIs, stop the repository task with an exact evidence packet for a narrow Hermes live-runtime task rather than inventing an approximation.

## Hard-boundary carry-forward

- No new CNX provider router.
- No OpenClaw dependency patch unless separately authorized.
- No production Gateway/provider/config mutation in the repository task.
- No live semantic request in the repository task.
- No release/tag/main.

## Reviewer

ChatGPT

Human final authority: Operator


## Historical reconciliation after initial review

A full read-back of CNX-380 through CNX-405 materially changes the successor recommendation and prevents duplicate work.

The following boundaries are already established:

- CNX-380 executed the exact isolated OpenClaw loader and queried the real global hook runner.
- CNX-381 proved repeated `api.on("before_agent_run", ...)` calls reached the real host registration path and can be rejected by the host policy gate.
- CNX-385 subsequently proved that `plugins.entries.<id>.hooks.allowConversationAccess=true` is a supported host configuration contract and is preserved by normalization.
- CNX-391 replayed a production-shaped true-policy configuration through the exact installed loader and proved that `before_agent_run` is accepted into the real registry; its false-policy control omitted it.
- CNX-394/CNX-395 proved that `plugins list --json hookCount/hookNames` is an installed-index/status projection and is not reliable evidence of the live Gateway typed-hook registry.
- CNX-399/CNX-400/CNX-401 proved cache/repeated-registration/registry-replacement mechanisms but not their production occurrence.
- CNX-404/CNX-405 exhausted the available read-only production correlation without obtaining per-invocation cache/registry/acceptance identity.

Therefore the initial review suggestion to create another basic loader/composed-registry RED test would duplicate stronger historical evidence and is superseded by this reconciliation.

## Revised successor direction

The next bounded work should stop treating registry lifecycle forensics as the primary path.

Before any new live semantic requalification, perform an exact-version architecture review of OpenClaw's available pre-inference typed-hook boundaries and select the narrowest supported, provider-independent boundary for CogentNexus Ticket-first admission.

The review must compare at least:

- `before_agent_run`;
- `before_agent_reply`;
- `before_prompt_build`;
- `before_model_resolve`;
- `inbound_claim` where relevant to Web Chat ingress;
- any exact selection-runner / Agent Core pre-model boundary in OpenClaw 2026.7.1-2.

The decision must be based on exact source ownership, dispatch coverage, ordering relative to provider/model resolution and inference, fail-closed semantics, context/session identity availability, and provider/runtime independence.

Do not migrate hooks merely because `before_agent_run` has been difficult to observe. If the exact source proves it is still the correct boundary, retain it and define the next smallest proof/repair. If another supported boundary is strictly better for the product invariant, document the migration cost and compatibility implications before implementation.

This is architecture-level reasoning and should use a stronger reasoning model rather than a lightweight worker model.
