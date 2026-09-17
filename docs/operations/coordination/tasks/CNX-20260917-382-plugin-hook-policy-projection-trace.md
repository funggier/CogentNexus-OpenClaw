# CNX-20260917-382 — Plugin Hook Policy Projection Trace

## Purpose

Trace the exact OpenClaw `2026.7.1-2` loader path that turns the loaded CogentNexus plugin definition/manifest metadata into the `hookPolicy` supplied to `createApi(...)` and ultimately consumed by `registerTypedHook(...)`.

CNX-381 proved in an exact isolated lifecycle that:

`plugin definition load`
→ `register(api)`
→ `api.on("before_agent_run")`
→ real host `registerTypedHook`
→ **host rejects the hook because effective non-bundled hook policy is not true**

At the same time, the effective CogentNexus artifact contains:

`hooks: { allowConversationAccess: true }`

Therefore the next investigation boundary is the **policy projection/metadata propagation path**, not registry composition.

## Parent

`CNX-20260917-381`

## Branch

`cnx-357-openai-dashboard-ticket-first-requalification-v2`

## Executor / Reviewer

Executor: Hermes
Reviewer: ChatGPT
Human final authority: Operator

## Starting authority

Begin from authoritative branch HEAD and re-read:

- `ACTIVE.md`
- `STATUS.md`
- this task
- CNX-381 report
- CNX-380 report
- CNX-378 report
- CNX-374 report

Before runtime conclusions, directly verify the effective artifact SHA-256:

`2841b704ad1c923ba643ca885eaf1d34e2f9565350d501c9d4895746d56c2d95`

Do not use the known CNX-376 typo as evidence.

## Objective

Determine exactly where:

`hooks.allowConversationAccess = true`

present on the exported CogentNexus plugin definition becomes absent/false by the time OpenClaw calls:

`createApi(..., hookPolicy, ...)`

and reaches the `registerTypedHook` conversation-hook gate.

## Required trace

Trace the real OpenClaw `2026.7.1-2` module graph in a disposable isolated process.

Required chain:

`plugin source/exported definition`
→ `definePluginEntry` result
→ plugin discovery/manifest metadata
→ loader plugin record
→ `loadPlugin` / plugin activation record
→ `createApi(...)`
→ `hookPolicy: entry?.hooks`
→ API registration closure
→ `api.on()`
→ `registerTypedHook(..., hookPolicy)`
→ conversation-hook gate

At every boundary record whether the following exact property exists and what its value is:

`hooks.allowConversationAccess`

## Identity and projection matrix

Produce a matrix similar to:

| Boundary | Value present? | Value | Object/token | Notes |
|---|---:|---:|---|---|
| exported plugin definition | yes/no | true/false/undefined | P1 | ... |
| definePluginEntry result | yes/no | ... | P2 | ... |
| discovered plugin metadata | yes/no | ... | P3 | ... |
| loader entry record | yes/no | ... | P4 | ... |
| createApi hookPolicy | yes/no | ... | P5 | ... |
| api.on registration context | yes/no | ... | P6 | ... |
| registerTypedHook policy | yes/no | ... | P7 | ... |
| conversation-hook gate | yes/no | ... | P8 | ... |

Also record object identity/equality where possible. Do not assume metadata objects are the same object as the exported definition.

## Critical questions

Answer these explicitly:

1. Does `definePluginEntry(...)` preserve `hooks.allowConversationAccess`?
2. Does the real loader retain the `hooks` field when creating its plugin/entry record?
3. Is the `hookPolicy` passed to `createApi` actually `entry.hooks` from the same record that was loaded?
4. Is `entry?.hooks` empty/undefined by the time `createApi` executes?
5. Is `pluginConfig.hooks` incorrectly being treated as policy, or vice versa?
6. Does a non-bundled plugin take a different loader path that strips/normalizes `hooks`?
7. Is there a manifest/discovery schema that omits `hooks` even though the executable definition contains it?
8. Is there a compatibility adapter that reconstructs the plugin entry without preserving `hooks`?
9. Does the CNX-374 repair alter the executable exported object but fail to affect the metadata object consumed by `createApi`?

## TDD / repair

**No repair is authorized in CNX-382.**

Do not change source, dependency, config, artifact, or production runtime.

No permanent instrumentation.

Temporary instrumentation is allowed only in disposable isolated copies and must be deleted after evidence capture.

The purpose is to identify the exact projection boundary so that a separate successor task can perform the minimal repair.

## Production boundary

Production runtime must remain untouched.

Do not restart or reload production Gateway.

Do not attach debugger to production.

Do not send Dashboard semantic/model requests.

Production facts may be referenced only as previously established evidence:

- PID `27372`
- OpenClaw `2026.7.1-2`
- effective artifact SHA above
- plugin loaded
- production `hookCount=0`, `hookNames=[]`

Do not claim that the isolated policy projection is production root cause unless the relevant loader path and metadata structure are proven to be the same mechanism.

## Hard fences

- No production Gateway restart/reload.
- No production configuration mutation.
- No OpenClaw dependency patch.
- No CogentNexus source patch.
- No artifact rebuild.
- No semantic/model/provider requests.
- No TicketStore/admission/provider/auth/routing/Dashboard UI changes.
- No speculative repair.
- No permanent instrumentation.
- No committed disposable instrumentation.
- No broad refactor.
- No release/tag/main.
- No force-push/history rewrite.
- No historical edits to CNX-360 through CNX-381.
- Do not start CNX-383 yourself.

## Required report

Create:

`docs/operations/coordination/reports/CNX-20260917-382-plugin-hook-policy-projection-trace-report.md`

Include:

- authoritative starting/final HEAD
- exact OpenClaw version/module hashes
- effective plugin artifact path and SHA-256
- disposable process identity
- exported definition evidence
- definePluginEntry evidence
- discovery/manifest evidence
- loader record evidence
- createApi hookPolicy evidence
- registerTypedHook policy evidence
- object identity/projection matrix
- exact first loss/alteration boundary
- comparison with CNX-374 and CNX-381
- production vs isolated evidence separation
- remaining uncertainty
- hard-fence compliance

## Classification

Choose one:

`HOOK_POLICY_PROJECTION_LOSS_PROVEN`

`HOOK_POLICY_PROJECTION_PRESERVED_GATE_SOURCE_MISMATCH`

`HOOK_POLICY_PROJECTION_PATH_NOT_REPRODUCED`

`HOOK_POLICY_PROJECTION_DIAGNOSTICALLY_UNRESOLVED`

Do not claim repair success in CNX-382.

## Closeout

After report publication:

- set `ACTIVE.md` to `WAITING_FOR_CHATGPT_REVIEW`
- set `STATUS.md` to `WAITING_FOR_CHATGPT_REVIEW`
- stop immediately
- do not start CNX-383
