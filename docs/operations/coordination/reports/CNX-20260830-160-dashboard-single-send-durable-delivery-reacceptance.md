# CNX-20260830-160 — Dashboard Single-Send Durable-Delivery Reacceptance

## Disposition

`FAIL`

The mandatory pre-Send gate passed and exactly one semantic Dashboard Send was performed. The accepted installed candidate produced one durable Ticket and one completed model call with `response_ready`, but no visible Dashboard final response and no durable `cnx_assistant_delivery` row. The Ticket then entered the product's permanent failure path with `failure_delivery_suppressed`. This proves a Dashboard/durable-delivery product failure on the one authorized Send. No semantic retry or second Send was performed.

## Authority and provenance

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`
- Fresh authoritative remote HEAD used: `fcfc2ce5c44fb8b7ae8af70aca6c69b666093a8c`
- ACTIVE/STATUS: `READY_FOR_HERMES`, `LIVE_DASHBOARD_SINGLE_SEND_DURABLE_DELIVERY_REACCEPTANCE`
- Task: `CNX-20260830-160`
- Accepted Dashboard repair: `1ec8cfc81b8a21a178200c33816427f9abfd31b9`
- Accepted installer observability repair: `2e8ff49da2573d87236fa7a004bc156d8c94b880`
- Fresh isolated source checkout: `C:\Users\CDQ-P\AppData\Local\Temp\cnx160-dashboard-20260830T100616Z\source`
- Fresh checkout HEAD: `fcfc2ce5c44fb8b7ae8af70aca6c69b666093a8c`
- Production-path diff from accepted installer-observability repair to current HEAD: empty (`plugins`, `skills`, `scripts`, `package.json`, `package-lock.json`)
- Required report was absent at preflight.

## Evidence root

`C:\Users\CDQ-P\AppData\Local\Temp\cnx160-dashboard-20260830T100616Z\`

All evidence below was retained outside product deletion roots. Hashes are SHA-256 of the exact local evidence files.

## Pre-Send gate

Preflight completed at approximately `2026-08-30T10:09:38Z` UTC and passed:

- Installed launcher: `C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd`
- Launcher SHA-256: `f53df28f2a7ee7fc43c65ba2c48770ed9b7ed3e7b14d3c762f957bd017b90f10`
- Authoritative state root: `C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw`
- Installed plugin root: `C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw`
- Ownership verification: exit `0`, `OWNERSHIP_PRESENT`
- Installed version: `0.9.3`
- Installed fingerprint: `07ac85dcc4eddca65d2107bac9123bedaf14751bedc66d2e8c5a12d88cf82d96`
- Installed fingerprint matched the Task-159 accepted candidate provenance.
- Plugin inventory: `cogentnexus-openclaw`, `enabled=true`, `status=loaded`, entrypoint `dist/v091-release-entry.js`
- Controller: `mode=managed`, desired Gateway/provider `running`, selected provider `ollama`, generation `24`
- Gateway: OpenClaw `2026.7.1-2`, loopback `127.0.0.1:18789`, reachable/healthy
- Ollama: reachable/healthy/ready at `127.0.0.1:11434`; four models reported
- Startup adapter: installed, `State=Ready`, `Enabled=true`, `LastTaskResult=0`
- `check delivery --json`: `READY`, pending `0`, `readOnly=true`, `stateChanged=false`
- `check recovery --json`: `READY`, no active incident/maintenance, `readOnly=true`, `stateChanged=false`
- `check system`: `SYSTEM READINESS: READY`, no state changed
- SQLite: opened with `mode=ro`; `integrity_check=ok`
- No concurrent installer process was present.
- No pre-existing active/ambiguous semantic operation blocked unique correlation.

Evidence files:

| Evidence | SHA-256 |
|---|---|
| `a01-status.txt` | `07fe8507e73626232a9baf26b95ec6116f1d0efa2c0043e4604a8152b29c3aea` |
| `a02-delivery.json` | `2c4408d9ec3d9fc574c2a4429a6b131d5e72fede25ec8b2ae198ad5dd008a0a1` |
| `a03-recovery.json` | `dc331d93112f88afe522cf947642be818a87303526f353701426809fba0e38d6` |
| `a04-system.txt` | `a91c148378a671965734b82190641b525b7a250febe441631efd28c0ce325e94` |
| `a05-cnx.txt` | `8cc2298a8df7cdc61f038e88295ce5ec6c14657172b9f945390adbdda2472f6b` |
| `a06-ownership-verify.txt` | `5d33595e26c7eaceba0f2a07e4e2757c3dcaf7ac10c3c8f6f973c3ca8933c609` |
| `a07-installed-fingerprint.txt` | `bb2b703b36f1c9e16a22f3d1beded1048a621fc1eabbfef8564a8e5a5d12b19e` |
| `a08-recovery-preflight.txt` | `2c4ba6f711a37799b269fde691e939ea8fe42488e0ca8a8ba506bac548b443fe` |

## Dashboard interaction

- Browser: Firefox, real OpenClaw Control Dashboard
- Fresh session URL: `http://127.0.0.1:18789/chat?session=agent%3Amain%3Adashboard%3A357978f0-cd4f-4b13-b3c5-06dd5ccd342c`
- Session key: `agent:main:dashboard:357978f0-cd4f-4b13-b3c5-06dd5ccd342c`
- Exact input submitted: `Task 160 durable delivery check. Please reply briefly to confirm receipt.`
- Composer verification: exact text appeared once before Send; no extra text or second copy.
- Best available durable Send/accept timestamp: `2026-08-30T10:11:50.282Z` UTC (`accepted` event)
- Dashboard semantic Send count: **exactly `1`**
- Visible result: user message bubble appeared; Dashboard showed responding state, then no assistant final bubble was delivered.
- UI screenshot after the failed delivery observation: `C:\Users\CDQ-P\AppData\Local\hermes\cache\images\computer_use_116e1105867242d7a26209e9ffdf20a7.png`
- No Send button was pressed again; no Enter, reload, follow-up, alternate surface, or semantic retry was used.

## Durable correlation and result

The one Send uniquely correlated to:

- Ticket: `CNXT-cbd974c0-6084-4754-87ab-fde4bdce188b`
- Run: `b929e739-2565-495c-a685-49a27963aba4`
- Session: `agent:main:dashboard:357978f0-cd4f-4b13-b3c5-06dd5ccd342c`
- Generation: `0`
- Call ID: `b929e739-2565-495c-a685-49a27963aba4:model:1`
- Provider/model: `ollama` / `qwen3.5:9b`
- Prompt SHA-256: `82a23d07fd96b4f7ed99ecd6cdf3025f7e64cea94a1b2c303f135bd30160ee29`

Durable event order:

| Event | UTC |
|---|---|
| `accepted` | `2026-08-30T10:11:50.282Z` |
| `routed` | `2026-08-30T10:11:50.287Z` |
| `direct_model_call_started` | `2026-08-30T10:11:50.424Z` |
| `direct_model_call_ended` / outcome `completed` | `2026-08-30T10:13:19.685Z` |
| `response_ready` | `2026-08-30T10:13:19.766Z` |
| `failed` | `2026-08-30T10:15:19.842Z` |
| `failure_delivery_suppressed` | `2026-08-30T10:15:19.842Z` |

Final durable state:

- Ticket status: `failed`
- Failure class: `permanent`
- Failure message: `direct response delivery became unverifiable before the final payload was durably captured; refusing regeneration to avoid duplicate output`
- Model call: one row, `state=ended`, `outcome=completed`, `duration_ms=89261`
- `response_ready_at`: `2026-08-30T10:13:19.766Z`
- `delivery_confirmed_at`: `null`
- `cnx_assistant_delivery` rows: `0`
- `ticket_outbox` rows: `0`
- Duplicate authoritative result: none observed
- Recovery/incident rows for this operation: none observed
- SQLite integrity: exact `ok`

Read-only database evidence:

- `b01-db-after-send.json`: `1c7af713d36906edc727a67450c698b722fd530ac08645769fd30c44095f5d39`
- `b02-db-30s.json`: `8d18396dcefd043a1f7ab8579d46ddc65394bedf388a58f3bf16dc1e4957b6e5`
- `b03-observation-series.jsonl`: `61af91ecd0c367ab003854921de45971232940b82818026ed434a0f660fe87c9`
- `b04-db-after-response.json`: `517e1daee2764382313f55037ce3aa7bca9f14162b1d065f236751d5065b23a3`
- `b05-settlement-observation.jsonl`: `975ea5e4f0f481d0551af2509e78558326c146961e7c4bab4f277f2b73f3ba36`

## Visible-vs-durable reconciliation

The visible user bubble confirms the Dashboard accepted the one message. The model call completed and a durable `response_ready` event was recorded, but the Dashboard never displayed a final assistant response. The durable result explicitly records `durableDelivery=false`; no `cnx_assistant_delivery` row and no outbox row exists; the operation was terminally failed with delivery regeneration suppressed. Therefore visible and durable evidence do **not** satisfy the Task-160 PASS contract.

## Bounded logs

Original OpenClaw log:

- Path: `C:\Users\CDQ-P\AppData\Local\Temp\openclaw\openclaw-2026-08-30.log`
- Bytes at capture: `1720418`
- SHA-256 at capture: `f374fa4d81aa3d163b3746a2e8d398e93bf1f05d2b6c2e6ef5d12d4d705cd795`

Relevant bounded raw window: `2026-08-30T10:10:30Z` through `2026-08-30T10:16:30Z`

- Evidence: `b06-bounded-log-window-raw.txt`
- Bytes: `2402`
- SHA-256: `60734ef6df6dcf0f1577a2f25ac0e6f394103973bbc37d1c02b018fdc149e01e`
- Relevant records show `handler-entry` with `hasAppendBeforeDeliver=false`, followed by `handler-skip` with reason `missing-append-before-deliver`.

## Post-Send health

Read-only post-send checks completed after terminal failure:

- Controller remained `mode=managed`, selected provider `ollama`, desired Gateway/provider `running`.
- Gateway remained reachable/healthy on loopback `127.0.0.1:18789`.
- Ollama remained reachable/healthy/ready with four models.
- Plugin remained installed/enabled/loaded.
- `check delivery --json`: `READY`, pending `0`, `readOnly=true`, `stateChanged=false`.
- `check recovery --json`: `READY`, no active incident/maintenance, `readOnly=true`, `stateChanged=false`.
- Supervisor snapshot remained healthy.
- SQLite remained `integrity_check=ok`.

Evidence:

- `c01-post-status.txt`: `f79ad978ba0f6a4f5a0a7d076a37e1b8383788b45a8b28f49c02667805b2ddda`
- `c02-post-delivery.json`: `2c4408d9ec3d9fc574c2a4429a6b131d5e72fede25ec8b2ae198ad5dd008a0a1`
- `c03-post-recovery.json`: `32e3022bc9a23271175f62d387742afe452bdf1f3220dbbfdd907ea7cf86e317`

## Live-action and mutation ledger

Authorized actions performed:

- Fresh remote GitHub ref check and isolated detached clone: source/evidence only.
- Read-only installed provenance, ownership, plugin inventory, health, Gateway/provider, scheduled-task, log, and SQLite inspection.
- Dashboard navigation to a fresh session, exact message composition, and exactly one authorized Send.
- Read-only observation until the operation reached terminal failure.
- No product mutation, lifecycle command, install-over, uninstall/reinstall, reset, recovery disruption, process kill, database write, Ticket/workflow/outbox/delivery mutation, source patch, dependency upgrade, release/promotion, or force push.
- Exactly one Dashboard semantic Send; no second semantic message was submitted.

## Remaining uncertainty

The exact physical mouse-click timestamp is not independently exposed by the Dashboard; the durable `accepted` event at `2026-08-30T10:11:50.282Z` is the best available operation timestamp. The failure is not an executor timeout or harness failure: the model call completed, the product produced `response_ready`, and the product's own terminal failure/suppression path recorded the missing durable delivery. No attempt was made to repair or replay it.

## Publication

This report is the only file authorized for the report-only publication commit. The report commit SHA and remote blob must be verified after push; then Hermes must STOP for ChatGPT review.
