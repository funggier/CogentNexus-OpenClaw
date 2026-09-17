# CNX-20260917-385 — Normalized Hook Policy Input Path Diagnosis

## Purpose

Determine why `normalized.entries[pluginId]?.hooks` is absent in the exact OpenClaw runtime path even when the configured plugin entry is intended to carry `hooks.allowConversationAccess=true`, and whether an existing supported plugin/config contract can preserve that field without patching OpenClaw or adding a new dependency architecture.

## Parent

`CNX-20260917-384`

## Branch

`cnx-357-openai-dashboard-ticket-first-requalification-v2`

## Executor / Reviewer

Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`

## Evidence baseline

CNX-382 proved the executable definition contains `hooks.allowConversationAccess=true`, while the loader passes `normalized.entries[pluginId]?.hooks` to `createApi(... hookPolicy ...)`.

CNX-381 proved the real `api.on("before_agent_run")` path reaches `registerTypedHook` and is rejected by the host conversation-hook policy gate.

CNX-383/384 established that the plugin repository does not own the normalization/projection implementation and has no existing tracked host-dependency patch mechanism.

CNX-373 previously established that the live runtime configuration includes `plugins.entries.cogentnexus-openclaw.hooks.allowConversationAccess=true` before the failing registration path.

## Objective

Trace the exact path:

`raw OpenClaw config`
→ config/schema validation
→ normalization
→ `normalized.entries[pluginId]`
→ `entry.hooks`
→ `createApi(hookPolicy)`

Determine exactly where the configured `hooks.allowConversationAccess` is retained, stripped, transformed, or rejected.

Then determine whether an **existing supported contract already available to the plugin** can make the field survive normalization.

This is diagnosis only. No repair is authorized.

## Required investigation

1. Identify the exact config object used by the loader before normalization.
2. Identify the schema/parser/normalizer that constructs `normalized.entries`.
3. Trace `plugins.entries.<id>.hooks` through validation and normalization.
4. Determine whether `hooks` is intentionally schema-filtered, renamed, defaulted, or omitted.
5. Compare the raw config path with the manifest/discovery path and executable definition path.
6. Determine whether `hooks.allowConversationAccess` has a documented/supported host configuration contract distinct from the executable definition.
7. Determine whether the plugin manifest (`openclaw.plugin.json`) or another existing plugin metadata surface can legitimately declare this policy.
8. Determine whether an existing install/bootstrap/configuration writer in this repository can populate the required normalized field without inventing a new dependency architecture.
9. Determine whether the normalization behavior differs between bundled and non-bundled/global plugins.
10. Identify the smallest **existing** supported extension point, if any, that can carry this policy to `createApi` without modifying OpenClaw itself.

## TDD / repair boundary

No source repair in this task.

A focused diagnostic/regression may be added only if it helps prove the normalization boundary. Any temporary instrumentation must be disposable and uncommitted.

Do not modify production configuration or installed dependencies.

## Hard fences

- No production Gateway restart/reload.
- No production configuration mutation.
- No OpenClaw dependency patch.
- No CogentNexus source repair.
- No artifact rebuild for deployment purposes.
- No Dashboard semantic/model/provider requests.
- No TicketStore/admission/provider/auth/routing/model/Dashboard UI changes.
- No speculative workaround.
- No new dependency architecture.
- No permanent or committed instrumentation unless it is a focused repository regression required to document the proven boundary.
- No release/tag/main.
- No force-push/history rewrite.
- No historical edits to CNX-360 through CNX-384.
- Do not start CNX-386 yourself.

## Required report

Create:

`docs/operations/coordination/reports/CNX-20260917-385-normalized-hook-policy-input-path-diagnosis-report.md`

Include:

- authoritative starting/final HEAD
- exact OpenClaw version and relevant module hashes
- exact raw config field/value
- schema/normalizer source and line ranges
- normalization before/after representation
- `normalized.entries[pluginId]` evidence
- `entry.hooks` evidence
- `createApi(hookPolicy)` evidence
- bundled vs non-bundled comparison if relevant
- existing supported extension points considered
- explicit answer whether a plugin-owned repair path exists without host patching
- production vs isolated evidence separation
- remaining uncertainty
- hard-fence compliance

## Classification

Use one:

`NORMALIZED_HOOK_POLICY_STRIPPING_PROVEN`

`NORMALIZED_HOOK_POLICY_PRESERVED_HOST_CONTRACT_FOUND`

`NORMALIZED_HOOK_POLICY_INPUT_PATH_UNRESOLVED`

`NORMALIZED_HOOK_POLICY_DIAGNOSTICALLY_BLOCKED`

Do not claim repair success.

## Closeout

After report publication, set `ACTIVE.md` and `STATUS.md` to `WAITING_FOR_CHATGPT_REVIEW` and stop.
