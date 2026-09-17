# CNX-20260917-387 — Production Hook-Gate Outcome Correlation

## Purpose

Determine, using read-only production evidence, whether the live CogentNexus `before_agent_run` registration was:

1. rejected by the existing host conversation-hook policy gate,
2. accepted into the plugin registry but later absent from the composed registry view, or
3. not observably completed because the production evidence boundary ends earlier.

CNX-385 proved the normalization path preserves `allowConversationAccess=true`.
CNX-386 could not prove that the running production loader's in-memory effective config at registration time contained that value.

This task therefore uses the strongest remaining **non-invasive observable evidence**: production startup/registration logs and supported plugin inventory, correlated to the same gateway process and effective plugin artifact.

## Parent

`CNX-20260917-386`

## Branch

`cnx-357-openai-dashboard-ticket-first-requalification-v2`

## Executor / Reviewer

Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`

## Starting authority

Begin from the authoritative branch HEAD and re-read:

- `ACTIVE.md`
- `STATUS.md`
- this task
- CNX-386 report
- CNX-385 report
- CNX-382 report
- CNX-381 report
- CNX-380 report
- CNX-378 report
- CNX-376 report

Current authoritative branch head must be recorded in the report.

Known production baseline:

- OpenClaw `2026.7.1-2`
- gateway PID `27372` (re-correlate; do not assume unchanged)
- gateway `127.0.0.1:18789`
- effective CogentNexus artifact SHA:
  `2841b704ad1c923ba643ca885eaf1d34e2f9565350d501c9d4895746d56c2d95`

Re-hash the effective artifact if the live runtime is still running before relying on the value.

## Objective

Correlate the exact production lifecycle around plugin startup and `before_agent_run` registration using existing logs and supported read-only commands.

The decisive question is:

> Do production logs contain evidence that the host `registerTypedHook` conversation-access gate rejected `before_agent_run`, or evidence that the hook registration passed the gate and was subsequently lost/excluded by registry composition?

## Required investigation

1. Re-correlate the live gateway process:
   - PID
   - start/last-run time
   - OpenClaw version
   - gateway endpoint
   - effective CogentNexus artifact path and SHA

2. Identify the exact gateway log file used by this process.

3. Search the relevant startup/registration window for the exact host policy diagnostic:

   `typed hook "before_agent_run" blocked because non-bundled plugins must set plugins.entries.cogentnexus-openclaw.hooks.allowConversationAccess=true`

   Record whether it exists, its timestamp, and the surrounding lifecycle events.

4. Search for CogentNexus plugin startup/registration events, including existing `hook-registered` delivery-observe events.

5. Correlate the order of observable events where possible:

   `plugin discovery`
   → `plugin load/start`
   → `hook registration attempt`
   → `host policy rejection` OR absence of rejection
   → `gateway ready`
   → `plugin inventory`

6. Compare the log evidence with supported `openclaw plugins list --json` output for the same live process/runtime.

7. Determine whether the exact host policy rejection message is present.

8. If the rejection message is present, determine whether its timing and surrounding evidence are sufficient to classify gate rejection as the production boundary.

9. If the rejection message is absent but a reliable plugin-side registration event exists, determine whether that is enough to move the likely boundary downstream to registry composition. Do not treat plugin-side `hook-registered` alone as proof that `registerTypedHook` accepted the hook.

10. Inspect for any other host diagnostics emitted by `registerTypedHook`, registry insertion, registry composition, or `hasHooks` that can be correlated without invasive inspection.

11. Keep these evidence classes separate:
   - production log evidence;
   - supported inventory evidence;
   - source-trace evidence from exact OpenClaw `2026.7.1-2`;
   - conclusions/inferences.

12. Do not reopen normalization analysis unless a new log fact directly contradicts CNX-385.

13. Do not attach a debugger, restart the gateway, mutate configuration, patch dependencies, or modify production files.

## Important interpretation rules

- Absence of a warning is **not** proof that the gate passed.
- A plugin-side `hook-registered` event is **not** by itself proof that `registerTypedHook` inserted the hook into the host registry.
- `hookCount=0` / `hookNames=[]` is a downstream observation, not proof of where the hook disappeared.
- Do not claim `allowConversationAccess=true` reached the production gate unless directly evidenced.
- Do not claim registry composition failure unless the evidence distinguishes it from gate rejection.
- Do not claim Dashboard Ticket-first semantic success.

## Runtime restrictions

Production is strictly read-only.

Forbidden:

- Gateway restart/reload
- production configuration mutation
- installed dependency mutation
- OpenClaw dependency patch
- CogentNexus source repair
- artifact deployment/rebuild
- debugger/inspector attachment
- semantic/model/provider request
- Dashboard request
- TicketStore/admission/routing/auth changes
- any retry or second semantic probe

Read-only log inspection and supported diagnostics are authorized.

## Required classification

Use exactly one:

`PRODUCTION_HOOK_GATE_REJECTION_CORRELATED`

`PRODUCTION_HOOK_GATE_PASS_WITH_DOWNSTREAM_REGISTRY_LOSS_CORRELATED`

`PRODUCTION_HOOK_REGISTRATION_OUTCOME_UNRESOLVED`

`PRODUCTION_HOOK_REGISTRATION_DIAGNOSTICALLY_BLOCKED`

## Required report

Create:

`docs/operations/coordination/reports/CNX-20260917-387-production-hook-gate-outcome-correlation-report.md`

Include:

- authoritative starting/final HEAD
- live PID/version/start time
- effective CogentNexus artifact path and SHA
- exact production log path
- exact log timestamps and relevant surrounding events
- presence/absence of host policy rejection diagnostic
- plugin-side registration events
- supported plugin inventory
- event-order correlation
- explicit distinction between direct evidence and inference
- relationship to CNX-385 normalization proof
- relationship to CNX-386 config-provenance uncertainty
- whether registry-composition investigation remains justified
- semantic request count = 0
- production mutation count = 0
- hard-fence compliance
- remaining uncertainty

## Closeout

After report publication:

- set `ACTIVE.md` to `WAITING_FOR_CHATGPT_REVIEW`
- set `STATUS.md` to `WAITING_FOR_CHATGPT_REVIEW`
- stop
- do not create/start CNX-388
- do not modify historical CNX-360 through CNX-386
- do not modify `main`, tags, or releases
