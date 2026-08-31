# CNX-20260830-152 — Final Dashboard Durable-Delivery Acceptance With Operator Mouse Gates

## Verdict

`FAIL_DURABLE_CAPTURE`

The operator-owned Dashboard Send succeeded far enough to create one Ticket and one direct model call, and the UI displayed the expected ACK. However, the required durable direct-result delivery row and terminal delivery/completion lifecycle were not created. The product failed closed with `failure_delivery_suppressed`; no retry was performed.

## Authority and frozen provenance

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`
- Task: `CNX-20260830-152`
- Fresh authority ref inspected before execution: `2fe237c5eee4c037fa1b7e14f3932bad05170acd`
- Task status: `READY_FOR_HERMES`
- Accepted production implementation SHA: `fb5781c1abd68280760bd5b3b4a65fabd8a60e58`
- Expected installed plugin fingerprint: `12c6d1b5b6ffd938353dd60c5d6190c34a609663369f619ff4fc7cbd176119e0`
- Expected installed `namespace_ownership.py` SHA-256: `10dda985e6d4553a73a8cdd3ef7f660937482c3ef0c2d2da8d15bcbfe8d39b66`
- Installed provenance and ownership remained unchanged.

## Phase A — read-only preflight

The remote branch, `ACTIVE.md`, `STATUS.md`, Task 152, and matching report/review state were read from a fresh clone. No matching Task-152 report existed before publication.

Installed runtime preflight passed:

- controller: `managed`
- desired Gateway/provider: `running/running`
- selected provider: `ollama`
- one canonical non-reparse CNX plugin, enabled/loaded
- Gateway healthy on loopback `127.0.0.1:18789`
- Ollama healthy/ready
- recovery: `READY`, no active incident
- delivery: `READY`, pending outbox `0`
- SQLite `PRAGMA integrity_check`: `ok`
- no active direct model/recovery/delivery work before Send
- no transaction/rollover residue

Baseline durable counts:

| Table | Count |
|---|---:|
| `tickets` | 0 |
| `ticket_events` | 0 |
| `cnx_direct_model_call` | 0 |
| `cnx_direct_recovery` | 0 |
| `cnx_assistant_delivery` | 0 |
| `ticket_outbox` | 0 |
| `cnx_sessions` | 2 |

The configured route was verified from runtime/configuration metadata only: provider `ollama`, model `qwen3.5:9b`. No separate inference/provider probe was issued.

## Prepared Dashboard and operator gates

- Target: authenticated Firefox OpenClaw Dashboard
- Firefox PID: `12060`
- Firefox HWND: `328720`
- `GetForegroundWindow()` matched the target HWND before input.
- The operator-prepared session was fresh and empty, displayed `Ready to chat`, and had no Task-151 draft/message.
- The `Message Assistant` composer was empty.
- The operator manually clicked the exact composer once with the real mouse as required by Task 152.
- The executor did not use automated mouse control for either semantic mouse gate.
- After the operator composer click, foreground/session/composer state was reverified.

## Prompt composition and Send ledger

A fresh nonce was generated and verified absent from all relevant pre-existing durable content. To comply with telemetry privacy, the raw nonce is not reproduced here; its SHA-256 digest was:

`74511b1ef058af1034329018db4c886c9b8eb45a43352ba392d87100903dd511`

The exact task prompt form was used:

```text
CogentNexus final durable-delivery acceptance <NONCE>. Reply with exactly: ACK <NONCE>
```

The executor entered one complete copy after operator-established focus. A fresh capture showed the complete prompt with exactly two nonce occurrences and no Enter/Send action.

The executor explicitly authorized Send. The operator manually clicked the real Dashboard `Send message` control exactly once with the real mouse.

- Send budget: **`1 / 1 consumed`**
- Composer/Send mouse gates: operator-owned and manually executed
- No automated Send click
- No Enter-to-submit
- No second Send/resend
- No alternate Dashboard/API/CLI/Gateway semantic transport
- Nonce retired permanently after Send

## Durable lifecycle result

The read-only observation established this event sequence:

| Order | Durable boundary | Result |
|---:|---|---|
| 1 | `accepted` | present |
| 2 | `routed` | present |
| 3 | `direct_model_call_started` | present |
| 4 | `direct_model_call_ended` | present |
| 5 | `response_ready` | present |
| 6 | `cnx_assistant_delivery` direct-result row | **absent** |
| 7 | `delivery_confirmed` | absent |
| 8 | `completed` | absent |

The single direct model call used `ollama/qwen3.5:9b`, ended with outcome `completed`, and had `recovery_attempt_count=0`. The model-call duration was `855658 ms`.

The Ticket terminal result was `failed`. The final event was `failure_delivery_suppressed`. No `cnx_assistant_delivery` row, idempotency key, delivered timestamp, delivery confirmation, or completed event existed. `ticket_outbox` remained empty (`0`), which is permitted for the direct Dashboard path but does not substitute for the required durable direct-result row.

## UI result

The Firefox Dashboard displayed exactly one visible assistant reply matching the requested ACK form. This visible result does not override the durable failure: the required direct-result delivery row was absent and the Ticket was terminally failed.

The durable result is therefore classified as `FAIL_DURABLE_CAPTURE`, not PASS.

## Final read-only runtime/state checks

- Gateway: healthy, loopback listener present
- Ollama: healthy/ready with configured route available
- recovery check: `READY`, no active incident, zero recovery attempts
- delivery check: `READY`, pending `0`, `readOnly=true`, `stateChanged=false`
- SQLite integrity: `ok`
- final counts: one Ticket, seven Ticket events, one model-call row, zero recovery rows, zero assistant-delivery rows, zero outbox rows
- no duplicate model call, recovery, regeneration, or delivery

## Telemetry privacy

Only bounded categorical/status metadata and digests were used for the report. No raw prompt, raw assistant response, raw semantic nonce, raw run/session identifier, credential, token, or secret is included. The raw nonce is intentionally redacted; only its SHA-256 digest is reported.

## Hard-fence confirmation

- No automated Send click.
- No second Send/resend.
- No alternate semantic channel or synthetic semantic injection.
- No manual Ticket/workflow/outbox/delivery/recovery/database mutation.
- No reset/uninstall/install/reinstall.
- No lifecycle command.
- No crash/recovery injection.
- No manual plugin/config/controller/process/service/task normalization.
- No reboot.
- No credentials/secrets disclosure.
- No merge/tag/release or force push.

This was one operator-owned Send attempt. The first failing boundary was durable direct-result capture after `response_ready`. Stop for independent ChatGPT review; do not create Phase Q or release state.
