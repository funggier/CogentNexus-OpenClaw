# CNX-20260917-383 — Hook Policy Projection Repair

## Purpose

Repair the proven hook-policy projection defect established by CNX-382:

`releaseEntry.hooks.allowConversationAccess = true`
→ executable definition contains the policy
→ `definePluginEntry` does not preserve `hooks`
→ loader `entry = normalized.entries[pluginId]`
→ `createApi(... hookPolicy = entry?.hooks)`
→ `registerTypedHook` receives no `allowConversationAccess=true`
→ non-bundled `before_agent_run` hooks are rejected before registry storage

This task is the first authorized repair following the diagnosis chain CNX-381 → CNX-382.

## Authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Executor: Hermes
- Reviewer: ChatGPT
- Human final authority: Operator
- Parent report: `docs/operations/coordination/reports/CNX-20260917-382-plugin-hook-policy-projection-trace-report.md`

## Starting authority

Begin from authoritative branch HEAD and re-read:

- `ACTIVE.md`
- `STATUS.md`
- this task
- CNX-382 report
- CNX-381 report
- CNX-374 report

Before runtime conclusions, direct-hash the effective installed CogentNexus artifact. Expected known repaired artifact SHA lineage before this repair:

`2841b704ad1c923ba643ca885eaf1d34e2f9565350d501c9d4895746d56c2d95`

Do not assume any new artifact is active until it is directly hashed from the effective runtime path.

## Objective

Make the smallest justified source change so that the conversation-hook policy already declared by the executable plugin definition reaches the host `hookPolicy` consumed by `registerTypedHook` for the non-bundled plugin path.

The repair must preserve existing OpenClaw registry architecture and must not add a second registration/admission path.

## Repair constraints

The repair must be driven directly by CNX-382's proven mechanism.

Preferred repair direction, to be evaluated rather than assumed:

- preserve the plugin-definition hook policy through the plugin entry representation actually consumed by the loader; or
- explicitly project the already-declared executable definition hook policy into the host hook-policy input at the narrowest correct boundary.

Do not patch around the gate by bypassing `registerTypedHook`.

Do not disable the conversation-hook gate.

Do not duplicate `before_agent_run` registration.

Do not modify TicketStore or admission semantics.

## TDD requirement

Before source repair:

1. Add or adapt a focused regression reproducing CNX-382's exact failure.
2. Establish RED.
3. Implement the minimal justified repair.
4. Establish GREEN.

The regression must verify both:

- `hooks.allowConversationAccess=true` is preserved/projected into the policy path; and
- the non-bundled `before_agent_run` registration is accepted into the typed hook registry rather than merely returning `undefined`.

Prefer a unit/integration test at the narrowest host/plugin boundary that reproduces the actual loader/API policy projection.

## Validation

After GREEN:

- run the focused CNX-382/383 regression;
- run relevant existing CNX-374 regression;
- run relevant plugin test suite;
- run plugin build;
- run validation/lint/type checks relevant to changed code;
- ensure no unrelated source files changed.

Only after source/build validation is GREEN may runtime activation occur.

## Runtime activation

Runtime activation is authorized only to verify the repaired artifact.

If activation is required:

1. capture pre-activation PID and effective artifact SHA;
2. activate/restart only the required runtime;
3. capture post-activation PID;
4. directly hash effective installed artifact;
5. verify OpenClaw plugin inventory;
6. verify hook visibility (`before_agent_run`) through supported/read-only diagnostics where possible.

A semantic Dashboard request is **not authorized by default**.

At most **one** controlled Dashboard semantic probe may be used only if:

- source tests/build pass;
- runtime activation is proven;
- supported diagnostics still cannot determine whether `before_agent_run` is visible/dispatchable; and
- the report explicitly justifies why the probe is necessary.

No retry and no second semantic request.

## Success target

The repair is considered technically repaired only when evidence establishes:

`releaseEntry.hooks.allowConversationAccess=true`
→ loader/API policy path carries the value
→ `registerTypedHook` accepts the non-bundled conversation hook
→ `before_agent_run` becomes visible in the relevant registry/runner

Then a separate follow-up task may perform full Dashboard Ticket-first semantic requalification.

Do not collapse semantic requalification into this repair unless the single authorized probe is strictly required for runtime visibility verification.

## Hard fences

- No provider/auth/routing/model changes.
- No TicketStore redesign.
- No admission redesign.
- No Dashboard UI changes.
- No controller normalization.
- No speculative patch.
- No broad refactor.
- No bypass of the host conversation-hook policy gate.
- No second registration path.
- No unrelated runtime mutation.
- No release/tag/main.
- No force-push/history rewrite.
- No historical edits to CNX-360 through CNX-382.
- Do not start CNX-384 yourself.

## Required report

Create:

`docs/operations/coordination/reports/CNX-20260917-383-hook-policy-projection-repair-report.md`

Include:

- authoritative starting/final HEAD
- exact source files and line ranges changed
- root cause reference to CNX-382
- RED regression evidence
- exact minimal repair
- GREEN regression evidence
- relevant test/build/validation results
- pre/post runtime identity if activated
- direct effective artifact SHA-256
- plugin inventory/hook visibility
- semantic request count and justification if used
- mutation counts
- hard-fence compliance
- remaining uncertainty
- classification

## Classification

Use one of:

- `HOOK_POLICY_PROJECTION_REPAIRED`
- `HOOK_POLICY_PROJECTION_REPAIR_BLOCKED`
- `HOOK_POLICY_PROJECTION_REPAIR_INCONCLUSIVE`

Do not claim Dashboard semantic requalification success solely from source/build/runtime hook registration evidence.

## Closeout

After report publication:

- set `ACTIVE.md` to `WAITING_FOR_CHATGPT_REVIEW`
- set `STATUS.md` to `WAITING_FOR_CHATGPT_REVIEW`
- stop

Do not create CNX-384 yourself.
