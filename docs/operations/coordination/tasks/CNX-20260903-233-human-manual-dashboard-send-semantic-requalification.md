# CNX-20260903-233 — Human-Manual Dashboard Send Semantic/Durable Requalification

Status: `WAITING_FOR_USER_MANUAL_SEND`
Date: 2026-09-03 ICT
Parent: `CNX-20260903-232`
Installer-requalification parent: `CNX-20260902-230`
Repair parent: `CNX-20260902-226`
Failure lineage: `CNX-20260902-223`
Parent umbrella: `CNX-20260831-188`
UI actuator: User, manual mouse action only
Post-send observer: Hermes / authenticated Windows operator, read-only
Coordinator / final reviewer: ChatGPT

## Purpose

Change only the failed UI actuation method from Task 232.

Task 232 issued one automated/native click toward the Dashboard Send control, but application/runtime acceptance was not proven:

```text
draft remained visible
new Ticket = 0
new model-call lineage = 0
new durable semantic/result lineage = 0
new Dashboard result = 0
```

Independent review therefore treats Task 232 as a UI/tool automation boundary failure, not a CogentNexus/OpenClaw semantic-processing failure.

Task 233 authorizes one **human manual mouse click** on the existing Dashboard Send button and then read-only correlation of the resulting semantic lineage.

## Accepted parent review

Task-232 review:

`docs/operations/coordination/reviews/CNX-20260903-232-existing-session-dashboard-semantic-durable-requalification-review.md`

Accepted verdict:

`REJECT_PRODUCT_SEMANTIC_FAILURE__ACCEPT_FAIL_CLOSED_UI_AUTOMATION_BOUNDARY__RUNTIME_SUBMISSION_UNPROVEN__MANUAL_HUMAN_SEND_RETRY_AUTHORIZED`

Accepted repaired source:

`9a8510f1317c8e53c01c233b080ec20357cd22df`

Accepted plugin fingerprint:

`e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386`

Public `v0.9.3` must remain unchanged at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

## Intended existing Dashboard session

Use exactly the existing session:

```text
agent:main:discord:channel:1531199905673252946
```

Expected URL:

```text
http://127.0.0.1:18789/chat?session=agent%3Amain%3Adiscord%3Achannel%3A1531199905673252946
```

Existing history is valid.

`New session` must not be clicked.

## Exact message

The composer must contain exactly:

`ช่วยสรุปงานที่ฉันควรโฟกัสวันนี้จาก context ล่าสุด และบอกเหตุผลสั้น ๆ`

No `@Ce` prefix. No added/removed text.

Task 232 reported that this exact draft remained visible after its failed automated actuation.

Fresh visible UI state wins.

## Phase U1 — user visual gate

Before clicking anything, the user must visually confirm all of the following:

1. the Dashboard is still on session `agent:main:discord:channel:1531199905673252946`;
2. the composer still contains the exact authorized message;
3. no new assistant result for that message has already appeared;
4. the draft has not disappeared or materially changed.

If any item is false, **do not click Send**. Report the observed state to ChatGPT.

## Phase U2 — exactly one human manual Send

If Phase U1 passes, the user may use their normal physical mouse/pointer to click the visible Dashboard `Send message` control exactly once.

Immediately after the one physical click:

`SEMANTIC_RETRY_GATE=CLOSED`

The user must not:

- click Send a second time;
- press Enter/Ctrl+Enter as a fallback;
- retype/resubmit the message;
- send the same message from Discord;
- use any API/alternate transport;
- trigger recovery/replay.

Even if the UI appears slow or ambiguous, do not submit again.

After the one manual click, the user should tell ChatGPT simply that the manual Send was performed. The coordinator will then move Task 233 to post-send observation without authorizing another semantic action.

## Manual actuation budget

```text
human manual Dashboard Send clicks: 1 maximum
automated/native/computer-use Send clicks: 0
Enter-key submissions: 0
Discord-origin test submissions: 0
direct Discord/API Sends: 0
semantic resubmissions after manual click: 0
```

## Routing invariant

For this environment:

```text
Dashboard-origin turn -> Dashboard result
Discord-origin turn   -> Discord result
```

Task 233 therefore expects:

```text
one runtime-accepted Dashboard human submission
one Ticket lineage
one OpenClaw session/run lineage
one Ollama/model-call lineage
one durable semantic/result lineage
one logical Dashboard assistant result
zero Discord replies attributable to this Dashboard-origin turn
```

Discord channel `1531199905673252946` remains read-only negative control.

## Accepted pre-send durable baseline from Task 232

Task-232 postflight reported:

```text
controller mode: managed
generation: 38
Gateway: healthy
provider: ollama
Delivery: READY, pending=0
Recovery: READY
SQLite integrity: ok
tickets: 12
ticket_events: 94
cnx_direct_model_call: 12
cnx_assistant_delivery: 8
cnx_sessions: 20
ticket_outbox: 0
```

This is a comparison baseline, not a value to force. Fresh post-send evidence is authoritative.

## Phase H — post-send Hermes observation

This phase is **not active until the user reports that the single manual Send was performed and ChatGPT changes coordination state to post-send observation**.

Hermes then performs read-only evidence collection only.

Required proof:

- exact current GitHub/coordination authority;
- current managed runtime health;
- exactly one new Ticket attributable to the exact Dashboard text;
- exact durable payload/provenance fields proving human/channel payload semantics;
- exactly one attributable OpenClaw session/run lineage;
- exactly one attributable Ollama/model-call lineage;
- exactly one durable semantic/result lineage;
- exactly one logical Dashboard assistant result;
- zero attributable Discord reply;
- zero recovery duplicate/resend;
- pending `ticket_outbox` returns to 0;
- SQLite integrity remains `ok`;
- plugin/repair/ownership provenance remains coherent;
- Task-223 historical evidence remains unchanged.

Read-only observer/tool retries may use up to 2 additional evidence-driven attempts per logical observation. Each retry must materially change method or address the observed failure and must be recorded.

## Human semantic provenance contract

Prove the current-schema equivalent of:

```text
source = openclaw
payload_source = channel_payload
payload_author_kind = human
subject derives from exact user message
body derives conservatively from distinct body candidate or no-body fallback
```

No invented `@Ce` control token may enter human semantic content.

## Hard fences

Task 233 does not authorize:

- automated Send actuation;
- second human Send;
- Enter-key fallback;
- `New session`;
- Discord-origin acceptance turn;
- direct Discord/API Send;
- installer/reset/uninstall/reinstall;
- manual lifecycle/Gateway repair;
- plugin mutation;
- manual Ticket/outbox/recovery/SQLite write;
- recovery replay/resend;
- provider/model substitution;
- process termination;
- stale Task-223 evidence cleanup/finalization/edit/move/delete;
- product/source/test/workflow edit;
- Release/tag/asset mutation;
- force push/history rewrite.

## Required final ledger

```text
human manual Dashboard Send clicks
automated Send clicks
runtime-accepted Dashboard human submissions
new Ticket lineages
new OpenClaw session/run lineages
new Ollama/model-call lineages
new durable semantic/result lineages
new logical Dashboard assistant results
Discord replies attributable to Dashboard turn
direct operator Discord/API Sends
semantic resubmissions
recovery replay/resend
manual product/data/lifecycle mutations
```

Expected PASS shape:

```text
human manual Dashboard Send clicks: 1
automated Send clicks: 0
runtime-accepted Dashboard human submissions: 1
new Ticket lineage: 1
new session/run lineage: 1
new Ollama/model-call lineage: 1
new durable semantic/result lineage: 1
new logical Dashboard assistant result: 1
Discord replies attributable to Dashboard turn: 0
direct operator Discord/API Sends: 0
semantic resubmissions: 0
recovery replay/resend: 0
manual product/data/lifecycle mutations: 0
```

## Allowed final dispositions

- `PASS_HUMAN_MANUAL_DASHBOARD_SEMANTIC_DURABLE_REQUALIFIED`
- `BLOCKED_USER_VISUAL_GATE`
- `FAIL_MANUAL_DASHBOARD_TURN`
- `FAIL_DURABLE_SEMANTIC_TRACE`
- `FAIL_PAYLOAD_PROVENANCE`
- `FAIL_OLLAMA_LINEAGE`
- `FAIL_DASHBOARD_NO_RESULT`
- `FAIL_DASHBOARD_DUPLICATE_RESULT`
- `FAIL_UNEXPECTED_DISCORD_CROSS_SURFACE_DELIVERY`
- `FAIL_POST_TURN_HEALTH`
- `BLOCKED_EVIDENCE`

## Current stop boundary

Current state is `WAITING_FOR_USER_MANUAL_SEND`.

Do not start Hermes post-send semantic observation until the user confirms the one manual Send action to ChatGPT.
