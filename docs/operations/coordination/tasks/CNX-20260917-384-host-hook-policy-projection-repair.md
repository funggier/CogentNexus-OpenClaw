# CNX-20260917-384 — Host Hook Policy Projection Repair

## Purpose

Repair the proven OpenClaw host-side hook-policy projection boundary identified by CNX-382 and blocked under the plugin-only fence in CNX-383.

Proven chain:

`releaseEntry.hooks.allowConversationAccess=true`
→ OpenClaw loader uses `normalized.entries[pluginId]`
→ `createApi(... hookPolicy: entry?.hooks)`
→ `registerTypedHook`
→ non-bundled conversation-hook policy rejects `before_agent_run` before registry storage.

## Parent

`CNX-20260917-383`

## Branch

`cnx-357-openai-dashboard-ticket-first-requalification-v2`

## Executor / Reviewer

Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`

## Starting authority

Begin from authoritative branch HEAD and re-read `ACTIVE.md`, `STATUS.md`, this task, CNX-383 report, CNX-382 report, CNX-381 report, and CNX-374 report.

Known effective artifact identity remains:

`2841b704ad1c923ba643ca885eaf1d34e2f9565350d501c9d4895746d56c2d95`

Do not infer a changed artifact until directly hashed.

## Objective

Implement the smallest reproducible host-side repair that causes the already-authorized CogentNexus hook policy to reach the existing OpenClaw `hookPolicy` parameter without bypassing the conversation-hook gate.

The repair must preserve OpenClaw's existing policy semantics and must not create a second hook registration path.

## Required first decision

Confirm whether the repository can own this repair reproducibly through an existing supported mechanism, such as:

1. a supported loader/config projection extension point;
2. a reproducible dependency patch mechanism already accepted by this repository's build/install workflow;
3. a controlled OpenClaw fork/vendor path already compatible with the project's packaging model.

If none exists, do not improvise a new dependency-management architecture. Report the exact blocker.

## Repair scope

A host-side OpenClaw dependency change is explicitly authorized for this task **only at the proven projection boundary**.

The allowed semantic change is narrow:

- preserve/project `allowConversationAccess` from the authoritative plugin hook-policy declaration into the `hookPolicy` consumed by `registerTypedHook`;
- or, if repository architecture requires it, make the runtime configuration normalization preserve the existing `plugins.entries.<id>.hooks.allowConversationAccess` value already used by the host contract.

The gate itself must remain intact.

## Required TDD

### RED

Create or adapt a focused regression at the exact host boundary proving:

- plugin definition declares `allowConversationAccess=true`;
- current loader/API policy path does not carry it into `registerTypedHook`;
- `before_agent_run` is rejected;
- another ordinary typed hook remains accepted.

The failure must be caused by the projection defect, not by path, dependency-installation, or fixture errors.

### Repair

Implement the smallest host-side change justified by the proven owner.

Do not change unrelated loader behavior.

### GREEN

The focused regression must prove:

- `allowConversationAccess=true` reaches the actual `hookPolicy` object;
- `registerTypedHook` accepts `before_agent_run` under the existing gate;
- the hook is present in the typed registry afterward;
- ordinary typed hooks remain unaffected.

## Dependency reproducibility

Because the proven owner is outside plugin source, the repair must be reproducible from a clean checkout.

If changing OpenClaw dependency code:

- identify exact OpenClaw version/base;
- record exact changed module(s);
- use a repository-tracked reproducible mechanism;
- ensure `npm ci` / clean install reproduces the patched dependency;
- do not rely on hand-editing `node_modules` only;
- verify lockfile/package metadata as appropriate.

Do not silently convert this project into an OpenClaw fork unless explicitly required by the existing architecture and documented.

## Runtime activation

Allowed only after focused RED→GREEN and clean-install/build validation succeed.

When activation is necessary:

- record pre-activation PID;
- activate only the resulting validated artifact/runtime;
- directly hash the effective installed CogentNexus artifact;
- record post-activation PID;
- verify plugin inventory and hook visibility.

No Dashboard semantic request is required by default.

One semantic probe may be used only if supported runtime hook visibility remains unavailable after validated activation, and the report must explain why. Maximum 1; no retry.

## Hard fences

- No bypass of `registerTypedHook` policy gate.
- No hardcoded acceptance inside the gate.
- No second `before_agent_run` registration path.
- No TicketStore redesign.
- No admission redesign.
- No provider/auth/routing/model changes.
- No Dashboard UI changes.
- No controller normalization.
- No unrelated OpenClaw changes.
- No broad refactor.
- No speculative patch outside proven boundary.
- No force-push/history rewrite.
- No release/tag/main.
- No historical edits to CNX-360 through CNX-383.
- Do not start CNX-385 yourself.

## Required report

Create:

`docs/operations/coordination/reports/CNX-20260917-384-host-hook-policy-projection-repair-report.md`

Include:

- authoritative starting/final HEAD
- exact OpenClaw version and changed modules
- dependency repair/reproducibility mechanism
- RED evidence
- exact minimal change
- GREEN evidence
- clean-install validation
- build/plugin validation
- runtime activation evidence if used
- effective artifact SHA-256 from disk
- hook inventory / typed registry evidence
- semantic request count
- mutation counts
- hard-fence compliance
- remaining uncertainty

## Classification

Use one:

`HOST_HOOK_POLICY_PROJECTION_REPAIRED`
`HOST_HOOK_POLICY_REPAIR_BLOCKED`
`HOST_HOOK_POLICY_REPAIR_INCONCLUSIVE`

Do not claim Dashboard Ticket-first semantic success in this task.

## Closeout

After report publication, set `ACTIVE.md` and `STATUS.md` to `WAITING_FOR_CHATGPT_REVIEW` and stop.
