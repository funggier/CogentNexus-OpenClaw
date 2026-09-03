# Active Coordination Task

Status: `WAITING_FOR_USER_MANUAL_SEND`
Execution mode: `TASK233_HUMAN_MANUAL_DASHBOARD_SEND_SEMANTIC_REQUALIFICATION`
Current disposition: `TASK232_UI_AUTOMATION_BOUNDARY_ACCEPTED__PRODUCT_SEMANTIC_FAILURE_REJECTED__MANUAL_HUMAN_SEND_AUTHORIZED`
Task ID: `CNX-20260903-233`
Parent task: `CNX-20260903-232`
Installer-requalification parent: `CNX-20260902-230`
Repair parent: `CNX-20260902-226`
Failure lineage: `CNX-20260902-223`
Parent umbrella: `CNX-20260831-188`
Updated: 2026-09-03 ICT
UI actuator: User, manual mouse action only
Post-send observer: Hermes / authenticated Windows operator, read-only
Coordinator / final reviewer: ChatGPT

## Published authority

Public `v0.9.3` remains immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

Accepted repaired source:

`9a8510f1317c8e53c01c233b080ec20357cd22df`

Accepted plugin payload fingerprint:

`e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386`

No Release/tag/asset mutation is authorized.

## Task 232 review result

Task-232 report disposition `FAIL_DASHBOARD_TURN` is not accepted as a CogentNexus/OpenClaw semantic-processing failure.

Independent review:

`reviews/CNX-20260903-232-existing-session-dashboard-semantic-durable-requalification-review.md`

Verdict:

`REJECT_PRODUCT_SEMANTIC_FAILURE__ACCEPT_FAIL_CLOSED_UI_AUTOMATION_BOUNDARY__RUNTIME_SUBMISSION_UNPROVEN__MANUAL_HUMAN_SEND_RETRY_AUTHORIZED`

Accepted evidence from Task 232:

```text
automated Send-control actuation attempts: 1
runtime-accepted Dashboard human submissions proven: 0
new Ticket lineage: 0
new model-call lineage: 0
new durable semantic/result lineage: 0
new Dashboard result: 0
Discord reply attributable to turn: 0
operator Discord/API Sends: 0
```

The exact draft remained visible and durable counts were unchanged after the automation attempt. Runtime health remained coherent.

Task-232 report recorded a stale authority SHA (`e7cfe086...`) even though Task 232 opened at `9a33dfe...`; this is retained as a reporting/provenance defect. The successor performs from fresh current authority.

## Active Task 233

Execute:

`tasks/CNX-20260903-233-human-manual-dashboard-send-semantic-requalification.md`

Intended session:

```text
agent:main:discord:channel:1531199905673252946
```

Expected URL:

```text
http://127.0.0.1:18789/chat?session=agent%3Amain%3Adiscord%3Achannel%3A1531199905673252946
```

Exact draft, with no `@Ce` prefix:

`ช่วยสรุปงานที่ฉันควรโฟกัสวันนี้จาก context ล่าสุด และบอกเหตุผลสั้น ๆ`

## Current user action gate

Before any click, the user must visually verify:

1. the intended existing session is still open;
2. the composer still contains exactly the authorized message;
3. no new assistant result for that message is already present;
4. the draft has not disappeared or changed.

If any check fails, do not Send and report the visible state.

If all checks pass, the user is authorized to use their normal physical mouse/pointer to click the visible Dashboard `Send message` control **exactly once**.

After that one physical click:

`SEMANTIC_RETRY_GATE=CLOSED`

The user must not click Send again, press Enter as fallback, retype/resubmit, use Discord ingress, or use alternate API transport.

After the single click, the user should tell ChatGPT that the manual Send was performed. ChatGPT will then activate Task-233 post-send read-only Hermes observation.

## Send / routing budgets

```text
human manual Dashboard Send clicks: 1 maximum
automated/native/computer-use Send clicks: 0
Enter-key submissions: 0
Discord-origin semantic messages: 0
direct operator Discord/API Sends: 0
semantic resubmissions after click: 0
```

Expected routing:

```text
Dashboard-origin -> Dashboard result
Discord-origin   -> Discord result
```

Discord channel `1531199905673252946` remains read-only negative control. An attributable Discord reply from this Dashboard-origin turn is failure.

## Expected PASS shape after post-send observation

```text
human manual Dashboard Send clicks: 1
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

## Hard fences

No automated Send, second manual Send, Enter fallback, `New session`, Discord-origin acceptance turn, direct Discord/API Send, installer/reset/uninstall/reinstall, manual lifecycle/Gateway repair, plugin mutation, manual Ticket/outbox/recovery/SQLite write, recovery replay, provider/model substitution, process kill, stale Task-223 evidence cleanup/finalization, product/source/test/workflow edit, Release/tag/asset mutation, or force push is authorized.

## Current stop boundary

Wait for the user's one manual Dashboard Send confirmation.

Hermes post-send observation is not active until ChatGPT changes coordination state after that confirmation.
