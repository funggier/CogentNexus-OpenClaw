# CNX-20260831-190 — Task-189 Phase-E Human Send Orchestration and Evidence Closure

- **Disposition:** `FAIL_SEMANTIC_DURABLE_DELIVERY`
- **Date:** 2026-08-31 ICT
- **Repository:** `funggier/CogentNexus-OpenClaw`
- **Working branch:** `agent/v0.9.3-full-stabilization`
- **Remote HEAD observed at start:** `1b999491f9f2ccce0efbd5347339df81541dbf23`
- **Parent umbrella:** `CNX-20260831-188`
- **Continues:** `CNX-20260831-189`
- **Evidence root:** `C:/Users/CDQ-P/AppData/Local/Temp/cnx190-evidence-20260831T111500Z`

## Candidate and authority

Task-190 is the Phase-E continuation of Task-189. The immutable product candidate remained:

`604569c286e930f1a596362ab926b065b56d486e`

The accepted facade identity remained:

`aa747f8f30080ef839a8d2cbf5758f9981a007ca01f41a988576f42edea8682f`

The live remote `ACTIVE.md` and `STATUS.md` identified Task-190 as `READY_FOR_HERMES` and explicitly authorized only one genuine human Dashboard Send, read-only post-send evidence, and this report. No destructive lifecycle replay or product/source edit was authorized.

Task-189 report/review were read from the live remote ref. Task-189 Phases A-D were accepted; Phase E was the sole remaining boundary.

## Phase E.0 — pre-send baseline

A fresh read-only baseline was captured before the prompt was issued:

| Surface | Baseline |
|---|---:|
| `tickets` | 5 |
| `ticket_events` | 43 |
| `ticket_outbox` | 0 |
| `cnx_assistant_delivery` | 4 |
| `cnx_direct_model_call` | 5 |
| `cnx_direct_recovery` | 0 |
| `cnx_sessions` | 13 |

Additional baseline evidence:

- SQLite `PRAGMA integrity_check`: `ok`
- Gateway: healthy and listening on `127.0.0.1:18789`
- provider: managed `ollama`
- delivery check: `READY`, pending outbox `0`, `readOnly=true`, `stateChanged=false`
- OpenClaw: `2026.7.1-2 (0790d9f)`
- evidence files: `a01-host.json` through `a08-db-baseline.json`

The first baseline recovery check still reported the retained supervisor warning from the earlier install-over (`READY_WITH_WARNINGS`, stale snapshot `degraded`) while Gateway/Ollama had no active incident. This later converged to `READY` after the semantic turn without manual recovery; it did not cause a semantic retry or lifecycle action.

## Phase E.1/E.2 — one genuine human Send

Hermes generated the nonce immediately before instruction:

`CNX189-20260831T113657Z-19d2a36f`

Exact prompt given to the human Dashboard actor:

```text
ตอบกลับข้อความนี้เพียงว่า CNX189-20260831T113657Z-19d2a36f
```

The user used the normal OpenClaw Dashboard message box and later reported `ส่งแล้ว` in the Hermes conversation. Hermes did not click Send, press Enter, inject a message, retry, regenerate, or create a second semantic turn.

The single-send budget is therefore consumed: `1 / 1` human Send. No further semantic action is authorized.

## Phase E.3 — durable correlation

Final read-only SQLite correlation identified exactly one new turn:

- Ticket: `CNXT-1965a893-7100-4b0a-be7e-c27b12949319`
- request key: `e6ff771ed9d74fd4245c361844542c73b9b87e341d82da8fd3beec82c3464091`
- prompt SHA-256: `ee8502648e75626e413c7ee037bbfc2eb8034db6587163ec6487974638f47e23`
- session: `agent:main:dashboard:ab4095a0-3f46-41f5-8715-09143bb633dd`
- run: `3244b8cc-517b-4415-b272-d9a9a80ffc21`
- model call: `3244b8cc-517b-4415-b272-d9a9a80ffc21:model:1`
- provider/model: `ollama / qwen3.5:9b`
- delivery: `delivery_id=5`, `kind=direct_result`, `status=delivered`
- idempotency key: `cnxclaw-direct-result:CNXT-1965a893-7100-4b0a-be7e-c27b12949319:g0`
- Ticket status: `completed`
- `response_ready_at`: `2026-08-31T11:53:05.563Z`
- `delivery_confirmed_at`: `2026-08-31T11:53:05.572Z`

The correlated event chain contained exactly eight ordered events:

1. `accepted` — `2026-08-31T11:38:46.430Z`
2. `routed` — `2026-08-31T11:38:46.436Z`
3. `direct_model_call_started` — `2026-08-31T11:38:46.563Z`
4. `direct_model_call_ended` — `2026-08-31T11:53:05.538Z`
5. `response_ready` — `2026-08-31T11:53:05.563Z`
6. `direct_response_durable` — `2026-08-31T11:53:05.563Z`
7. `delivery_confirmed` — `2026-08-31T11:53:05.572Z`
8. `completed` — `2026-08-31T11:53:05.572Z`

Final count deltas from the pre-send baseline:

| Surface | Before | After | Delta |
|---|---:|---:|---:|
| `tickets` | 5 | 6 | +1 |
| `ticket_events` | 43 | 51 | +8 |
| `ticket_outbox` | 0 | 0 | +0 |
| `cnx_assistant_delivery` | 4 | 5 | +1 |
| `cnx_direct_model_call` | 5 | 6 | +1 |
| `cnx_direct_recovery` | 0 | 0 | +0 |
| `cnx_sessions` | 13 | 13 | +0 |

The existing session record was reused for the Dashboard session; the new run/Ticket/model-call/delivery correlation is unique.

## Failure: logical assistant content mismatch

The durable delivery row contains:

```text
text = NO_REPLY
status = delivered
```

The final Dashboard capture likewise shows one assistant bubble containing `NO_REPLY` with the CogentNexus delivery marker. It does **not** show an assistant acknowledgement containing the requested nonce. The required shape therefore fails criterion 6 of Task-190: logical assistant content must correspond to the requested nonce acknowledgement.

The durable chain is otherwise complete, but delivery confirmation alone does not upgrade the incorrect logical content to PASS. This is classified as `FAIL_SEMANTIC_DURABLE_DELIVERY`, not a UI-only uncertainty.

Evidence:

- `d01-post-send-sqlite.json`
- `d02-observation.json` — 55 read-only snapshots; observer exit code `0`
- `d03-correlation.json`
- final Dashboard screenshot: `C:/Users/CDQ-P/AppData/Local/hermes/cache/images/computer_use_7f263e47d58449a48b5f87a3397db827.png`

## Retry/recovery/duplicate checks

- human Send: exactly `1`
- Hermes Send: `0`
- Hermes Enter-as-Send: `0`
- `chat.inject`/synthetic injection: `0`
- retry/second Send: `0`
- regenerate: `0`
- direct recovery: `0`
- correlated duplicate Ticket: not found
- correlated duplicate model call: not found
- correlated duplicate delivery: not found
- pending terminal outbox: `0`
- SQLite integrity: `ok`

The bounded observer initially saw the expected in-flight state (`model call +1`, delivery unchanged), then observed terminal settlement. No retry or manual recovery was used during the wait.

## Final health

Post-settlement read-only checks:

- Gateway: healthy, `Connectivity probe: ok`, listening on `127.0.0.1:18789`
- provider: `ollama`, reachable/healthy/ready
- delivery: `READY`, pending `0`, `readOnly=true`, `stateChanged=false`
- recovery: `READY`, no maintenance marker, no active Ollama incident, recovery attempts `0`
- supervisor snapshot: `healthy` at `2026-08-31T11:53:10.017976+00:00`
- SQLite: `integrity_check=ok`

## Issue register

1. **Pre-send recovery warning:** the stale supervisor snapshot initially yielded `READY_WITH_WARNINGS`; there was no active incident and no manual recovery. It later converged to healthy automatically. Product effect: none.
2. **Slow local model settlement:** model execution lasted approximately `858.975s`. The observer waited read-only; no retry or recovery was performed. Product effect: none beyond delayed settlement.
3. **Semantic content mismatch:** both durable delivery and Dashboard showed `NO_REPLY` instead of the requested nonce acknowledgement. This is the decisive product acceptance failure and requires review; no repair or resend was authorized.
4. **Capture/assertion boundary:** Dashboard capture was used only as corroboration. Durable SQLite evidence is authoritative for cardinality and delivery state; the content mismatch is independently proven by the durable delivery `text` field.

## Fence statement

Exactly one genuine human Dashboard Send occurred. Hermes performed no Send, Enter-as-Send, injection, retry, regeneration, recovery, reset, uninstall, reinstall, state deletion, provider replacement, product/source/test/dependency/workflow edit, release action, merge, tag, GitHub Release publication, or force push.

Task-190 stops after this report is published. Any source repair, semantic retry, or expanded lifecycle requalification requires a new explicitly authorized coordination task.
