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
