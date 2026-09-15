# CNX-356 — Effective Admission Boundary Feasibility

Status: `READY_FOR_HERMES`
Execution mode: `READ_ONLY_RUNTIME_FEASIBILITY_SPIKE`
Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`
Parent: `CNX-355`
Base: `main`

## Objective

Determine whether the currently installed OpenClaw Gateway exposes an already-supported, authenticated read-only method that can observe the effective plugin hook registry from inside the Gateway process sufficiently to close the CNX-355 Level-3 observability gap.

Do not repair production behavior. This task is a feasibility probe only.

## Key source finding to verify at runtime

Current public OpenClaw source contains a `hooks.status` Gateway handler. That handler reads the request's live plugin registry via `getPluginRuntimeGatewayRequestScope()?.pluginRegistry ?? getActivePluginRegistry()` and builds a hook status report from `registry.hooks`. The report includes `name`, `source`, `pluginId`, `filePath`, `handlerPath`, `hookKey`, `events`, `loadable`, and plugin-management metadata.

This source finding is not sufficient by itself because CNX-355 observed an installed OpenClaw `2026.7.1-2` Gateway whose exposed CLI help only advertised `health/status/system-presence/cron.*`. The installed build must be tested directly before treating `hooks.status` as available.

## Hard fences

- No CogentNexus production source changes.
- No OpenClaw source changes.
- No new Gateway RPC/method.
- No undocumented method probing.
- No permission or scope broadening.
- No token/password/credential extraction, display, or persistence.
- No Gateway restart/stop/start/reload.
- No plugin install/enable/disable.
- No provider/model/auth/routing mutation.
- No semantic Dashboard/provider request.
- No CNX-344 replay/resend.
- No Ticket/SQLite/session/transcript/delivery mutation.
- No v0.9.5 tag/history mutation.
- No force-push/history rewrite.

## Required execution

1. Verify this branch descends directly from current `main` and record the starting HEAD.
2. Verify current Gateway process identity using already-supported read-only status surfaces only.
3. Using the existing paired/authenticated Control UI or other already-supported Gateway client boundary, determine whether the installed Gateway advertises `hooks.status` as a supported read-only method.
4. If `hooks.status` is advertised, invoke only `hooks.status` with the minimum valid parameters needed to select the active agent/workspace. Do not call any other new method merely because it exists.
5. Record whether the returned report contains the live CogentNexus plugin hook and the minimum fields needed for CNX-344 causality:
   - pluginId/source;
   - hook name/key/events;
   - loadable/enabled state;
   - effective handler/file identity where exposed;
   - whether the CogentNexus `before_agent_run` registration is represented.
6. Compare the result only against the known canonical CogentNexus invariant:
   - hook name `before_agent_run`;
   - priority `2000` is still not expected to be present in `hooks.status` unless the installed implementation exposes it elsewhere. Do not infer priority from absence.
7. If `hooks.status` is unavailable on the installed version, classify `UNRESOLVED / BLOCKED` and stop. Do not implement a replacement diagnostic.
8. If `hooks.status` is available and proves live Gateway plugin-hook membership, classify `BOUNDARY_CLOSED` only for the facts it actually exposes; do not claim priority/causality unless directly evidenced.
9. Publish a report at:
   `docs/operations/coordination/reports/CNX-20260915-356-effective-admission-boundary-feasibility-report.md`
10. Verify the final remote branch tip and report blob from GitHub after publication.
11. Stop for independent ChatGPT review.

## Decision rules

### `BOUNDARY_CLOSED`
Use only when a supported authenticated Gateway read method executes in the actual Gateway process and returns direct live plugin-hook registry facts for CogentNexus.

### `UNRESOLVED / BLOCKED`
Use when the installed Gateway does not support `hooks.status`, the authenticated client cannot invoke it within existing authority, or the result is still CLI-local/coarse and does not expose effective plugin-hook membership.

### `DEFECT`
Do not use this spike to declare a production defect. A production defect requires direct evidence of a mismatch between intended and effective runtime behavior. Any repair requires a separate successor task.

## Required report contents

- exact starting and final remote SHAs;
- exact branch and parent ancestry;
- installed Gateway/process identity;
- supported method inventory relevant to this probe;
- whether `hooks.status` exists in the installed Gateway;
- redacted live result fields;
- explicit distinction between hook membership evidence and priority/causality evidence;
- no-secret accounting;
- hard-fence accounting;
- changed-path list;
- final classification;
- next recommended authority, if blocked.
