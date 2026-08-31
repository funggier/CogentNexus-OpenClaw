# CNX-20260830-153 — Task-152 Redacted Delivery-Hook Evidence Collection

Status: `READY_FOR_HERMES`
Execution mode: `READ_ONLY_WINDOWS_TASK152_DELIVERY_HOOK_EVIDENCE_COLLECTION`
Executor: Hermes/Codex

## Objective

Collect the already-existing redacted `CogentNexus-OpenClaw delivery-observe` evidence for the single Task-152 Dashboard run so ChatGPT can identify the first internal durable-capture boundary before any source repair.

This task is **read-only evidence collection only**. It authorizes no new semantic action and no runtime mutation.

## Authority

Task-152 report:

`docs/operations/coordination/reports/CNX-20260830-152-final-dashboard-durable-delivery-operator-mouse-gates.md`

Task-152 independent review:

`docs/operations/coordination/reviews/CNX-20260830-152-final-dashboard-durable-delivery-operator-mouse-gates-review.md`

Review disposition: `ACCEPT` as controlled `FAIL_DURABLE_CAPTURE` evidence. Phase P remains FAIL.

Accepted installed production source remains:

`fb5781c1abd68280760bd5b3b4a65fabd8a60e58`

No source change is authorized by this task.

## Why this evidence is required

The Task-152 report proves:

- one real operator Send;
- one Ticket accepted before inference;
- one completed direct model call;
- one visible exact ACK;
- `response_ready` exists;
- zero `cnx_assistant_delivery` rows;
- no delivery confirmation/completion;
- terminal `failure_delivery_suppressed`.

But `response_ready` alone does not prove the final dispatcher callback/staging path executed, because the installed source may create `response_ready` through `markDashboardAwaiting` when no durable result is owned.

The installed source already emits privacy-bounded events such as:

- `hook-registered`
- `handler-entry`
- `handler-skip`
- `callback-registered`
- `callback-entry`
- `filter-skip`
- `stage-attempt`
- `stage-not-staged`
- `stage-exception`
- `stage-staged`

Task 153 must locate the existing Task-152 event sequence and report the first missing/failing boundary.

## Phase A — fresh authority and read-only identity

1. Fetch the remote branch fresh.
2. Verify `ACTIVE.md`/`STATUS.md` still authorize Task 153 and no matching report/review/successor supersedes it.
3. Verify the matching Task-153 report is absent before collection.
4. Do not open, edit, focus, type into, or Send from the Dashboard.
5. Use read-only database/log inspection only.

You may locally read the Task-152 Ticket/model timestamps and raw correlation identifiers only as necessary to identify the correct existing log window. **Do not reproduce raw Ticket IDs, run IDs, session IDs, nonce, prompt, response text, credentials, or tokens in the report.**

## Phase B — locate existing Task-152 log window

Use the existing OpenClaw log files that cover Task 152. Do not restart or rotate logs.

Establish the narrow window from existing durable timestamps around:

- Task-152 Ticket `accepted`;
- `direct_model_call_started` / `direct_model_call_ended`;
- `response_ready`;
- terminal `failure_delivery_suppressed`.

Report timestamps may be included. Raw semantic identifiers must be redacted or replaced by a stable digest.

## Phase C — extract redacted delivery-observe sequence

From existing logs only, collect lines with prefix/content equivalent to:

`CogentNexus-OpenClaw delivery-observe`

For the Task-152 correlation/window, report the ordered sequence of event names and only the source-approved bounded fields, including when present:

- `event`
- `reason`
- `hasEventRunId`
- `hasContextRunId`
- `hasDispatcher`
- `hasAppendBeforeDeliver`
- `kind`
- `alreadyOwned`
- `finalCount`
- `hasText`
- `hasMedia`
- `registrationCount`
- `ownerGeneration`
- bounded exception category
- correlation digest only, never raw run/session identifiers.

Explicitly answer presence/absence for each relevant boundary:

1. `hook-registered`
2. `handler-entry`
3. `handler-skip`
4. `callback-registered`
5. `callback-entry`
6. `filter-skip`
7. `stage-attempt`
8. `stage-not-staged`
9. `stage-exception`
10. `stage-staged`

If multiple correlations exist in the same window, distinguish them by safe digest and explain which one aligns temporally with Task 152 without revealing raw identifiers.

## Phase D — registration/reload context if the handler is absent

Only if Task-152 `handler-entry` is absent, inspect existing structural plugin/startup/reload log evidence around the same runtime generation to determine whether:

- `hook-registered` existed after the latest plugin/runtime activation;
- the plugin loaded successfully;
- a later reload/API registration boundary may have occurred.

Use only structural/redacted lines. Do not include semantic content.

## Required classification

Report exactly the first proven internal boundary, choosing the narrowest supported classification, for example:

- `HANDLER_NOT_ENTERED`
- `HANDLER_SKIPPED_MISSING_CORRELATION`
- `HANDLER_SKIPPED_MISSING_DISPATCHER`
- `HANDLER_SKIPPED_MISSING_APPEND_BEFORE_DELIVER`
- `CALLBACK_NOT_INVOKED`
- `FILTER_SKIPPED_<REASON>`
- `STAGE_NOT_ATTEMPTED`
- `STAGE_NOT_STAGED_<REASON>`
- `STAGE_EXCEPTION_<CATEGORY>`
- `STAGE_STAGED_DB_ABSENT`
- `UNRESOLVED_FROM_EXISTING_LOGS`

Do not infer beyond the first proven boundary.

## Hard fence

- No Dashboard click/focus/typing/paste/Send.
- No new semantic nonce/prompt.
- No API/CLI/Gateway semantic transport.
- No Ticket/workflow/outbox/delivery/recovery/database writes.
- No start/stop/restart/enable/disable/reset/uninstall/install/reinstall.
- No process/service/task mutation or kill.
- No plugin/config/controller/ownership mutation.
- No log deletion/rotation.
- No reboot.
- No credentials/secrets disclosure.
- No source edit.
- No merge/tag/release/force push.

## Required report

Publish exactly:

`docs/operations/coordination/reports/CNX-20260830-153-task152-redacted-delivery-hook-evidence-collection.md`

The report must contain:

- exact GitHub authority;
- evidence sources/time window without secrets;
- ordered redacted `delivery-observe` event sequence;
- explicit presence/absence matrix for the ten boundaries above;
- first proven boundary classification;
- statement that no semantic or runtime mutation occurred.

Then stop for independent ChatGPT review. Do not patch source and do not create another live acceptance task.
