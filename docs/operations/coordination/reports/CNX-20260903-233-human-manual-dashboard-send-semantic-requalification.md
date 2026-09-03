# CNX-20260903-233 — Human-Manual Dashboard Send Semantic/Durable Requalification

- **Task:** `CNX-20260903-233`
- **Parent:** `CNX-20260903-232`
- **Primary disposition:** `FAIL_DURABLE_SEMANTIC_TRACE`
- **Retry classification:** `RETRY_POLICY_EFFECTIVE`
- **UI actuator:** User manual mouse only
- **Post-send observer:** Hermes, read-only
- **Execution date:** 2026-09-03 ICT
- **Semantic retry gate:** `CLOSED` after the one manual Send confirmation

## Fresh authority

The coordination branch was fetched before post-send observation and again before report preparation.

```text
REMOTE_HEAD=7de9e248de86758f62340e456c2dd836ad9f5ab6
TASK233_ACTIVE=true
HAS_SUCCESSOR=false
```

Accepted repaired source remained an ancestor:

```text
9a8510f1317c8e53c01c233b080ec20357cd22df
```

Accepted plugin fingerprint remained:

```text
e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386
```

Public `v0.9.3` remained immutable at:

```text
26ce64a624255278a3a0266ad38746e0e6ed2e31
```

No source/product/test/workflow, Release, tag, asset, stale-evidence, lifecycle, installer, plugin, process, provider, model, recovery, SQLite, or Discord mutation was performed by Hermes.

## Manual Send boundary

The user confirmed the one physical Dashboard Send action with `ส่งแล้ว`. Prior fresh UI evidence showed the intended existing session and exact authorized composer text. Hermes did not click Send, did not press Enter, did not retype, and did not use an alternate transport.

Manual action ledger:

```text
human manual Dashboard Send clicks: 1
automated/native/computer-use Send clicks: 0
Enter-key submissions: 0
Discord-origin test submissions: 0
direct operator Discord/API Sends: 0
semantic resubmissions: 0
```

Immediate post-send capture showed the exact user message in the intended session and the Dashboard assistant processing/result surface. A later capture showed assistant content rendered in the Dashboard. The UI also showed the existing warning:

```text
Exec failed: pty · `check git status (in C:UsersCDQ-P.openclawworkspace)`
```

The UI-visible response is recorded as presentation evidence only; it is not treated as durable delivery evidence.

## Durable lineage

The exact new Ticket was:

```text
ticket_id: CNXT-dc11c9a0-8a89-4df5-9c48-345260725be4
run_id: e225013e-8d50-4479-b227-ca9a10b89a46
owner_session_key: agent:main:discord:channel:1531199905673252946
prompt: ช่วยสรุปงานที่ฉันควรโฟกัสวันนี้จาก context ล่าสุด และบอกเหตุผลสั้น ๆ
authoritative prompt_sha256: 76818536ffea3287fef5b48b26164bc288ff2e7665a7bd1ffd561fae6808cc02
created_at: 2026-09-03T01:44:25.903Z
```

This proves one runtime-accepted Dashboard-origin human Ticket with the exact prompt and intended session. The durable Ticket did not reach a successful terminal delivery state:

```text
status: accepted
failure_class: interrupted
failure_message: Direct response delivery was not confirmed before deadline
response_ready_at: null
delivery_confirmed_at: null
delivery_last_error: Direct response delivery was not confirmed before deadline
```

The durable event order was:

```text
95 accepted
96 routed
97 direct_model_call_started (ollama / qwen3.5:9b)
98 direct_model_call_ended (completed)
99 direct_model_call_started (ollama / qwen3.5:9b)
100 direct_model_call_ended (completed)
101 direct_model_call_started (ollama / qwen3.5:9b)
102 direct_model_call_ended (completed)
103 direct_model_call_started (ollama / qwen3.5:9b)
104 direct_model_call_ended (completed)
105 response_ready
106 direct_redelivery_timeout
```

The four model-call attempts are internal runtime behavior within the one attributable run; Hermes performed no model retry or recovery replay.

Model proof:

```text
provider: ollama
model: qwen3.5:9b
final call state: ended
final call outcome: completed
final call duration_ms: 62759
recovery_attempt_count: 0
```

Durable delivery proof failed:

```text
cnx_assistant_delivery rows for Ticket: 0
ticket_outbox rows for Ticket: 0
response_ready_at: null
delivery_confirmed_at: null
direct_redelivery_timeout: present
```

Thus the model lineage exists and completed, but the durable semantic/result delivery lineage required by Task 233 is absent. The UI-visible assistant content cannot override this durable failure.

## Post-send health

Read-only post-send checks remained healthy:

```text
mode=managed
generation=38
Gateway=healthy
provider=ollama
Delivery=READY, pending=0
Recovery=READY
SQLite integrity=ok
```

Final database totals were:

```text
tickets: 13
ticket_events: 106
cnx_direct_model_call: 13
cnx_assistant_delivery: 8
cnx_sessions: 20
cnx_direct_recovery: 1
ticket_outbox: 0
```

The new Ticket is the thirteenth Ticket and the new model-call lineage is the thirteenth model-call record; no new assistant-delivery row was created. No attributable Discord reply was observed. The Dashboard showed the user message and assistant content, but the durable delivery contract did not settle.

## Retry/observation ledger

| Logical operation | Attempt | Method | Result | Product/semantic state could have changed? | Remaining budget / rationale |
|---|---:|---|---|---|---|
| Fresh authority gate | 1 | Remote fetch and ACTIVE/task read | Task 233 active; no successor | No | No retry needed |
| Immediate post-send observation | 1 | Read-only status, delivery/recovery, SQLite snapshot, Firefox capture | New Ticket/model call observed; model active; UI responding | Yes, already caused by user Send | Semantic gate closed; no resend |
| Passive observation | 1 | Background observer polling read-only SQLite every 5 seconds | Recorded 174 samples; call lineage progressed to completion; delivery remained absent | No new action | Continued observation only |
| Observer wait | 1 | Foreground process wait | Tool wait timed out at 420 seconds while observer remained read-only | No | No semantic retry; poll/log inspection used |
| Durable event correlation | 1 | Direct read-only SQLite query by exact Ticket ID | Accepted → four Ollama calls → response_ready → redelivery timeout | No | No retry allowed |
| Post-health/provenance | 1 | Read-only launcher checks, SQLite, canonical backup hash, Firefox AX capture | Health remained coherent; historical evidence unchanged | No | No retry needed |

`RETRY_POLICY_EFFECTIVE` applies only to the observer/tool timeout handling. No semantic, model, Ticket, delivery, or recovery retry occurred.

## Required final ledger

```text
human manual Dashboard Send clicks: 1
automated Send clicks: 0
runtime-accepted Dashboard human submissions: 1
new Ticket lineages: 1
new OpenClaw session/run lineages: 1 attributable run
new Ollama/model-call lineages: 1 attributable run containing 4 internal call records
new durable semantic/result lineages: 0
new logical Dashboard assistant results: UI-visible content present; durable delivery not proven
product/runtime Discord replies attributable to Dashboard turn: 0
direct operator Discord/API Sends: 0
semantic resubmissions: 0
recovery replay/resend: 0
manual product/data/lifecycle mutations: 0
process terminations: 0
provider/model substitutions: 0
stale-evidence mutations: 0
installer/plugin/rollover actions: 0
```

## Historical evidence preservation

Task-223 retained evidence remained unchanged:

```text
transaction SHA-256:
ec1b32ec2813e1b4e2c220679f39c6922789b7d77e88ec9ca4ad6ba82ccac510

inventory SHA-256:
1a7299f926cda4e3f936577204c50059e0e4e716f8594535d4b3c40c40e51477

backup tree SHA-256:
7394401cb0ae9791c1c9b98661a9bf9df47ecb83c0b139b46cd742b17ee7342a

backup fingerprint:
f82674172a3946e00ddcb3a94fd14c8476bf91abc11ed7d44b5fa53acb74eaf1
```

No stale transaction/inventory/backup cleanup or finalization was attempted.

## Evidence paths

```text
C:/Users/CDQ-P/AppData/Local/Temp/cnx233-preflight-20260903T/
C:/Users/CDQ-P/AppData/Local/Temp/cnx233-postsend-20260903T/
C:/Users/CDQ-P/AppData/Local/Temp/cnx233-observer.py
C:/Users/CDQ-P/AppData/Local/hermes/cache/images/computer_use_fc43b816469c419da419b3974e94a321.png
C:/Users/CDQ-P/AppData/Local/hermes/cache/images/computer_use_38744a33bb524b96b2fe699880984eac.png
C:/Users/CDQ-P/AppData/Local/hermes/cache/computer_use/elements_de1f1e5ba1ee4b4d829b7bf8d38b21c6.json
```

## Final decision

Task 233 successfully proves the user’s single manual Dashboard Send entered the runtime and created one exact Ticket/run lineage using Ollama. It does **not** pass the semantic/durable acceptance: the runtime produced a `response_ready` event after four completed Ollama call records, but durable delivery was not confirmed, no durable assistant-delivery row exists, no outbox row exists, and the Ticket ended with `Direct response delivery was not confirmed before deadline` / `direct_redelivery_timeout`.

The Dashboard-visible assistant content is preserved as UI-visible evidence only and cannot be promoted to durable PASS. No resend, recovery replay, second click, Enter fallback, or Discord test is permitted. Execution stops after this report for independent review.
