# CNX-20260830-160 — Dashboard Single-Send Durable-Delivery Reacceptance

Status: `READY_FOR_HERMES`

Execution mode: `LIVE_DASHBOARD_SINGLE_SEND_DURABLE_DELIVERY_REACCEPTANCE`

Current authorization: `CNX-20260830-160_DASHBOARD_SINGLE_SEND_DURABLE_DELIVERY_REACCEPTANCE`

Task ID: `CNX-20260830-160`

Updated: 2026-08-30 ICT

Owner / coordinator / reviewer: ChatGPT

Executor: Hermes on the operator's real Windows/OpenClaw environment

## Purpose

Perform the final, separate live Dashboard durable-delivery reacceptance checkpoint on the repaired CogentNexus-OpenClaw candidate that Task 159 proved installed and healthy on the real Windows/OpenClaw environment.

This task authorizes **exactly one semantic Dashboard Send**. It does not authorize a second Send, a retry, repair work, release work, or any additional live semantic experiment.

## Accepted prerequisite lineage

Accepted Dashboard durable-authority production repair:

`1ec8cfc81b8a21a178200c33816427f9abfd31b9`

Accepted installer observability production repair:

`2e8ff49da2573d87236fa7a004bc156d8c94b880`

Task-159 report/evidence publication commit:

`5615b8beda31ba4da0636f4cde7a51a2e197afc9`

Task-159 review:

`docs/operations/coordination/reviews/CNX-20260830-159-windows-diagnostic-install-over-retry-review.md`

Task-159 review commit:

`138b5d3f9509ec42ec00b6fa701a7c2b02e2ab3f`

Task-159 review disposition: `ACCEPT`.

Task 159 proved the accepted candidate installed with matching fingerprint and healthy managed/plugin/gateway state. Dashboard semantic Sends remained `0` through that checkpoint.

Task-160 coordination commits after the accepted installed candidate are documentation/coordination only. Before the Send, Hermes must fresh-check that no unreviewed production/source delta has been introduced and that the installed live candidate still reconciles with the Task-159 accepted provenance.

## Objective

Using the real Dashboard and the already-installed accepted candidate, Hermes must:

1. capture fresh pre-state and provenance without semantic mutation;
2. verify the live environment is still healthy enough to run the acceptance check;
3. submit exactly one benign semantic Dashboard message;
4. observe the resulting Dashboard response without submitting another message;
5. correlate that single Send to its durable Ticket/run/generation/result/delivery evidence using established read-only tooling;
6. reconcile the visible Dashboard result with the durable authoritative result rather than accepting UI appearance alone;
7. verify no duplicate or ambiguous durable completion is present for the tested run;
8. capture post-send health and relevant logs;
9. publish the Task-160 report/evidence and STOP for ChatGPT review.

## Mandatory pre-Send gate

Before interacting with the Dashboard input, record and verify at minimum:

- current date/time, Windows and PowerShell context;
- repository branch and current coordination HEAD;
- no unreviewed production/source delta since the Task-159 accepted installed candidate;
- currently installed CogentNexus-OpenClaw/plugin identity or fingerprint still matches the accepted candidate provenance;
- CogentNexus controller/mode is `managed` or otherwise exactly in the accepted expected operational state;
- CogentNexus-OpenClaw plugin is enabled/loaded;
- OpenClaw gateway is healthy/reachable;
- established non-semantic status/health checks do not expose a relevant unresolved failure;
- no pre-existing semantic operation is actively ambiguous in a way that would prevent unique correlation of the new Send.

If provenance or required health cannot be established, **STOP `BLOCKED` with Dashboard semantic Sends = `0`**. Do not use the one authorized Send merely to diagnose a broken pre-state.

## Exactly-one semantic Send authorization

Task 160 authorizes exactly one semantic user-message submission through the real Dashboard.

Use this exact benign test input unless the Dashboard itself requires a mechanically equivalent harmless formatting adjustment:

`Task 160 durable delivery check. Please reply briefly to confirm receipt.`

Record the exact text actually submitted.

The semantic input must not request filesystem, shell, network, external-service, account, package, source-control, system-management, or other irreversible/tool side effects. It is a pure conversational delivery check.

### Send-count rule

The total semantic Dashboard Send count for this task must be exactly `1` if the pre-Send gate passes, otherwise `0`.

After the one Send occurs:

- do **not** press Send again;
- do **not** press Enter again in a way that submits another message;
- do **not** reload/replay/re-submit the semantic input;
- do **not** send a correction, follow-up, probe, or confirmation message;
- do **not** intentionally trigger a duplicate public-hook callback;
- do **not** use a second semantic message to diagnose timeout, failure, ambiguity, or missing UI output.

If the single Send fails, times out, becomes ambiguous, or produces unexpected behavior, preserve evidence and classify the checkpoint `FAIL` or `BLOCKED` as appropriate. **No semantic retry is authorized.**

## Required evidence for the one Send

The report must preserve enough evidence to correlate the single visible Dashboard interaction to the durable system-of-record state.

Record at minimum, where exposed by the established product/tooling:

### Dashboard interaction

- exact semantic input text;
- exact or best-available Send timestamp;
- semantic Send count;
- visible final Dashboard response text;
- any visible delivery/terminal indicator relevant to the tested interaction;
- screenshots or faithful UI evidence when useful, without substituting screenshots for durable state.

### Correlation identifiers

Record every available identifier needed to prove that the durable evidence belongs to the one Send, such as:

- Ticket ID;
- workflow ID;
- run ID;
- generation;
- result/delivery/outbox identifier;
- relevant event sequence identifiers or timestamps.

Do not invent identifiers that the product does not expose.

### Durable authority / result

Using established **read-only** commands/queries/log inspection, establish where available:

- committed Ticket corresponding to the Send;
- relevant workflow/run state and event history;
- durable result row/state for the same run/generation;
- durable/native result payload or authoritative text;
- delivery/outbox/settlement state;
- terminal state and validators applicable to this path;
- whether exactly one durable authoritative result exists for the tested run/generation;
- whether any duplicate/mismatch/fallback safety condition fired;
- whether visible Dashboard output reconciles with the durable authoritative result.

The Task-155 repair specifically restored durable authority for repeated public-hook finals. Task 160 does not need to manufacture a repeated callback; it must instead verify normal live delivery and inspect the evidence for duplicate/mismatch anomalies if they occurred naturally.

### Logs

Capture the relevant bounded log window around the one Send, including timestamps and complete relevant warnings/errors for:

- CogentNexus delivery handling;
- Dashboard/public-hook or reply dispatch path when observable;
- Ticket/workflow/result/delivery transition evidence;
- OpenClaw/plugin/gateway failure evidence if any.

Prefer faithful durable text evidence when the relevant log window is reasonably sized. Record original local log path and SHA-256 when a raw file is used as review evidence.

### Post-state

After the one interaction reaches a trustworthy terminal/settled state or becomes conclusively failed/blocked, record:

- CogentNexus mode/status;
- plugin loaded/enabled status;
- gateway health;
- relevant Ticket/workflow/result/delivery terminal state;
- whether any delivery remains unresolved;
- whether the tested Send created any duplicate durable result or inconsistent authority state.

## Durable-success acceptance contract

Task 160 may be `PASS` only when the evidence jointly establishes all of the following:

1. pre-Send candidate provenance and live health were valid;
2. semantic Dashboard Sends performed = exactly `1`;
3. the one Send can be uniquely correlated to its durable Ticket/run/generation evidence;
4. a visible Dashboard final response was delivered for that Send;
5. the corresponding durable authoritative result is committed/persisted and terminal as required by the established delivery model;
6. the visible result reconciles with the durable authoritative/native result rather than contradicting it;
7. delivery/outbox/settlement evidence reaches the accepted terminal/settled condition for the same semantic operation;
8. no duplicate authoritative result, durable-text mismatch, or unhandled delivery ambiguity remains for that tested run/generation;
9. relevant logs do not expose an unhandled delivery/runtime failure that contradicts success;
10. post-send CogentNexus/plugin/gateway health remains acceptable;
11. every action stayed inside Task-160 authorization.

Do not declare PASS from the visible chat bubble alone and do not declare PASS from a terminal Ticket/workflow state alone. Reconcile the visible response, durable state, delivery state, and logs.

## Disposition rules

Use:

- `PASS` only when the entire durable-success acceptance contract above is proven;
- `FAIL` when the accepted installed candidate exhibits a proven Dashboard/durable-delivery product failure on the single authorized Send;
- `BLOCKED` when environment/tool/UI/evidence limitations prevent a trustworthy conclusion without proving a product defect.

If the single Send has occurred, both `FAIL` and `BLOCKED` still require semantic Send count = `1`; do not retry to improve evidence.

## Authorized live actions

Only these actions are authorized:

- read-only status/provenance/health/log/database/Ticket/workflow/result/delivery inspection using established tooling;
- normal Dashboard navigation/focus/type needed to prepare the one authorized input;
- **one** semantic Dashboard submission;
- waiting/observing the resulting UI and existing system state;
- read-only evidence capture after the Send;
- writing/pushing Task-160 report/evidence files to GitHub.

## Hard fence

Task 160 does **not** authorize:

- a second semantic Dashboard Send or semantic retry;
- another semantic user message through any alternate OpenClaw/CogentNexus surface;
- manual creation or mutation of Ticket/workflow/run/result/outbox/delivery/database semantic state;
- manually forcing/replaying delivery or settlement;
- manual injection of a duplicate callback/event;
- reset;
- install-over;
- clean uninstall;
- fresh reinstall;
- arbitrary live-state deletion;
- source or production patching on the Windows machine;
- dependency upgrade;
- OpenClaw source patch;
- new CogentNexus product/runtime behavior;
- retry/timeout/rollback/process-kill redesign;
- merge to default/release branch;
- tag/GitHub Release/package publication/promotion;
- force push.

If a new defect is discovered, capture evidence and stop. Repair requires a new durable coordination task.

## Required report

Hermes must publish exactly:

`docs/operations/coordination/reports/CNX-20260830-160-dashboard-single-send-durable-delivery-reacceptance.md`

The report must include:

- `PASS`, `FAIL`, or `BLOCKED` disposition;
- exact source/installed candidate provenance;
- complete pre-Send health/provenance gate evidence;
- exact semantic input and Send timestamp;
- exact semantic Dashboard Send count;
- Dashboard response evidence;
- all available correlation IDs;
- durable Ticket/workflow/run/result/delivery evidence;
- visible-vs-durable reconciliation;
- relevant bounded logs/evidence artifact paths and hashes when applicable;
- post-send state and health;
- every live action/mutation performed;
- explicit confirmation that no second semantic message was submitted;
- remaining uncertainty;
- exact report/evidence commit SHA after push.

## Stop condition

After the Task-160 report/evidence is committed and pushed, **STOP**.

Do not continue into release, Phase Q, another Dashboard interaction, repair work, or any other live mutation.

ChatGPT must fresh-read and review Task-160 durable evidence before Phase P can be declared accepted or any successor is authorized.
