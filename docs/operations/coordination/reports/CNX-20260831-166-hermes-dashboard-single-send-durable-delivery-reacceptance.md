# CNX-20260831-166 — Hermes Dashboard Single-Send Durable-Delivery Reacceptance Report

## Disposition

**FAIL**

The authorized one-shot Dashboard send executed exactly once. The model completed and the Dashboard displayed exactly one correct assistant reply, but the repaired native-transcript delivery path did not durably settle the exact result. The native assistant transcript record lacked the CogentNexus delivery marker and assistant idempotency identity; no `cnx_assistant_delivery` row was staged; the Ticket ultimately failed closed with `durableDelivery:false` and no `delivery_confirmed_at`.

This is an executed acceptance failure, not a blocked test. No retry, second send, recovery injection, manual mutation, source repair, reinstall, or runtime restart was performed.

## Scope and authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Working branch: `agent/v0.9.3-full-stabilization`
- Fresh remote execution HEAD: `aab5ab2507ca76fa43070014afc559138bd59332`
- Task: `docs/operations/coordination/tasks/CNX-20260831-166-hermes-dashboard-single-send-durable-delivery-reacceptance.md`
- Predecessor review read from that HEAD: `docs/operations/coordination/reviews/CNX-20260830-165-hermes-windows-install-over-provenance-health-review.md`
- Task state at the one-shot race gate: `READY_HERMES`
- Task-166 report path at the one-shot race gate: absent
- Exact pre-send remote race check: `2026-08-30T18:20:55Z`
- Remote HEAD at that gate: `aab5ab2507ca76fa43070014afc559138bd59332`

The current HEAD contains accepted Task-164 repair commit `80b87dfbe0d9176e421f3748b4cee0827db12d0c` as an ancestor. A path-scoped diff from that repair through the Task-166 execution HEAD was empty for `plugins`, `scripts`, `skills`, `package.json`, and `package-lock.json`.

## Installed candidate provenance

- Plugin ID: `cogentnexus-openclaw`
- Display name: `CogentNexus-OpenClaw Bridge`
- Installed version: `0.9.3`
- Installed state before send: `enabled=true`, `status=loaded`
- Installed source: `C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw\dist\v091-release-entry.js`
- Accepted/installed plugin fingerprint: `5b23040f26ab1148c44647429cc5eff0ef89505e2f068b72d41d9a5fb0ee02e5`
- Ownership verification before send: exit `0`
- OpenClaw version: `2026.7.1-2`

The installed fingerprint matched the Task-165 accepted candidate, and no product-path drift existed on the Task-166 execution HEAD.

## Preflight health and baseline

Read-only preflight snapshot timestamp: `2026-08-30T18:17:51.829776+00:00`.

All fifteen read-only checks exited `0`:

1. `cnxclaw status`
2. `cnxclaw check system`
3. `cnxclaw check provider`
4. `cnxclaw check cogentnexus-openclaw`
5. `cnxclaw check gateway`
6. `cnxclaw check model`
7. `cnxclaw check storage`
8. `cnxclaw check recovery`
9. `cnxclaw check delivery`
10. `cnxclaw check resources`
11. `cnxclaw provider status`
12. `openclaw --version`
13. `openclaw gateway status`
14. `openclaw plugins list --json`
15. installed `namespace_ownership.py verify`

Additional baseline:

- SQLite `PRAGMA integrity_check`: `ok`
- `tickets`: `2`
- `ticket_events`: `14`
- `cnx_direct_model_call`: `2`
- `cnx_direct_recovery`: `0`
- `cnx_assistant_delivery`: `0`
- `ticket_outbox`: `0`
- `cnx_sessions`: `4`
- Gateway connectivity: healthy
- Provider/model: `ollama` / `qwen3.5:9b`
- No pending terminal deliveries or outbox work

## Exact one-shot Dashboard interaction

### Session and nonce

- Dashboard session key: `agent:main:dashboard:13b27c98-c09c-431e-928f-446175ed1937`
- Native transcript file selected by runtime: `C:\Users\CDQ-P\.openclaw\agents\main\sessions\7d2ca55f-ecda-4e24-b924-5f61e75a13b3.jsonl`
- Nonce: `T166-20260830T181855Z-3D954CC9`
- Exact prompt:

```text
CNX-166 acceptance T166-20260830T181855Z-3D954CC9. Reply with exactly: CNX-166-ACK-T166-20260830T181855Z-3D954CC9
```

- Expected exact answer:

```text
CNX-166-ACK-T166-20260830T181855Z-3D954CC9
```

### Send accounting

- Semantic Dashboard Send activations: **1**
- Semantic retry Sends: **0**
- Second prompt submissions: **0**
- Manual recovery/resume actions: **0**

Before the one semantic Send, background desktop input could not establish the composer focus and was verified to have left the composer empty. Firefox was then explicitly focused; a DPI/multi-monitor coordinate mismatch was corrected while the composer still remained empty. The exact complete prompt was visually verified in the composer before the single Send button activation. These pre-submit focus/type transport attempts created no chat message and did not activate Send.

The one-shot Send produced one user bubble and transitioned to `Assistant is responding…`. No Send/Enter/click retry occurred after that point.

## Observed first response

The first and only assistant bubble displayed:

```text
CNX-166-ACK-T166-20260830T181855Z-3D954CC9
```

- UI first-response minute: `2026-08-31 01:22` local time (`UTC+07:00`)
- Exact assistant response matched expected: yes
- Visible assistant semantic result bubbles: `1`
- Visible duplicate result bubbles: `0`
- Visible recovery/failure injection: `0`
- Visible retry: `0`

Final UI evidence screenshot:

- Path: `C:\Users\CDQ-P\AppData\Local\hermes\cache\images\computer_use_48e37d24a2b6490e9262d33192a67fdc.png`
- SHA-256: `303ebd278e861cfd9d18c385fad59b646c618f1d53c5564d371c2b645acdfc22`

The expected answer appears twice in the full UI accessibility inventory because the user prompt itself quotes the expected answer and the assistant bubble contains the result. Native transcript role-aware parsing confirms exactly one assistant result record.

## Exact durable correlation

### Ticket identity

- Ticket ID: `CNXT-1fb84cef-19d1-485e-a032-991da12aa770`
- Run ID: `2f9ea54b-e9e3-4e50-b012-9ad35b24b778`
- Model call ID: `2f9ea54b-e9e3-4e50-b012-9ad35b24b778:model:1`
- Request key: `e8859f165d50dcf02f2ac29f013e0c5620e08b0a2a53fb76a1e2c381d42281b9`
- Prompt SHA-256: `7df6c3e85f7ed46ca69970bd09b38f5c6caf4dfa4c6b2de6aa0b136beb165ec7`
- Owner session key: `agent:main:dashboard:13b27c98-c09c-431e-928f-446175ed1937`

### Model execution

- Provider/model: `ollama` / `qwen3.5:9b`
- Model call start: `2026-08-30T18:21:12.170Z`
- Model call end: `2026-08-30T18:22:54.232Z`
- Duration: `102064 ms`
- Model outcome: `completed`
- Recovery attempt count: `0`

The model completed exactly once; no second inference or recovery model call was observed.

### Ticket events

The exact Ticket event sequence was:

1. `accepted` — `2026-08-30T18:21:12.028Z`
2. `routed` — `2026-08-30T18:21:12.032Z`
3. `direct_model_call_started` — `2026-08-30T18:21:12.170Z`
4. `direct_model_call_ended` — `2026-08-30T18:22:54.232Z`, outcome `completed`
5. `response_ready` — `2026-08-30T18:22:54.323Z`, `durableDelivery:false`
6. `failed` — `2026-08-30T18:24:54.380Z`
7. `failure_delivery_suppressed` — `2026-08-30T18:24:54.380Z`

Final Ticket fields:

- `status=failed`
- `failure_class=permanent`
- `response_ready_at=2026-08-30T18:22:54.323Z`
- `delivery_confirmed_at=null`
- `result_json={"runId":"2f9ea54b-e9e3-4e50-b012-9ad35b24b778","direct":true,"expectsDelivery":true,"durableDelivery":false}`
- `attempt_count=0`
- `worker_id=null`
- `lease_token=null`

Exact failure message:

```text
direct response delivery became unverifiable before the final payload was durably captured; refusing regeneration to avoid duplicate output
```

The terminal-failure path removed one pending failure delivery and emitted:

```json
{"reason":"direct response delivery became unverifiable before the final payload was durably captured; refusing regeneration to avoid duplicate output","removed":1,"policy":"non-inference-terminal-failure"}
```

This fail-closed behavior prevented a duplicate visible failure or regenerated answer, but it does not satisfy durable delivery acceptance.

## Native transcript authority evidence

The native session transcript changed from one session header record to six total records. Role-aware parsing found:

- User records containing the nonce: `1`
- Assistant records containing the nonce: `1`
- Assistant records exactly equal to the expected response: `1`
- Assistant delivery-marker records: `0`

Exact relevant native records:

- User record ID: `a662bbe7`
- User timestamp: `2026-08-30T18:21:12.147Z`
- User idempotency key: `2f9ea54b-e9e3-4e50-b012-9ad35b24b778:user`
- Assistant record ID: `f6b6563b`
- Assistant timestamp: `2026-08-30T18:22:54.245Z`
- Assistant content: exact expected answer
- Assistant idempotency key: `null`
- Assistant delivery marker: absent

Final transcript:

- Size: `1488` bytes
- SHA-256: `d6aae2670e8e598045da1775360b82735f4ddf2ab03b859f1f957936394d39c9`

The assistant message was natively persisted, but the installed repaired plugin did not bind the durable identity/marker needed for post-persistence settlement. Therefore transcript existence alone cannot be reported as confirmed delivery under the Task-164/Task-166 invariant.

## Delivery, outbox, and recovery rows

Final scoped rows for this execution:

- `cnx_assistant_delivery`: `0`
- `ticket_outbox`: `0`
- `cnx_direct_recovery`: `0`
- Claim token: no delivery row existed
- Claim expiry: no delivery row existed
- Delivered timestamp: no delivery row existed

No competing delivery, outbox retry, recovery injection, or second inference occurred.

## Post-settlement health

Final read-only post-settlement snapshot timestamp: `2026-08-30T18:31:18.914838+00:00`.

- All fifteen health/provenance commands listed in preflight still exited `0`
- SQLite integrity: `ok`
- Plugin: `0.9.3`, enabled and loaded
- Ownership verification: exit `0`
- Gateway/provider/model/storage checks: ready
- Delivery/recovery command checks: exit `0`
- `cnx_direct_recovery`: `0`
- `ticket_outbox`: `0`

The system remained operational after the acceptance failure. Generic readiness does not override the exact Ticket's failed durable-delivery state.

## Exact-SHA workflow context

GitHub Actions on the exact Task-166 execution HEAD `aab5ab2507ca76fa43070014afc559138bd59332` were all successful before the live send:

- PS5.1 Acceptance Smoke `33327287052`: `success`
- Windows Installer Pack Smoke `33327287008`: `success`
- Validate `33327287107`: `success`

These workflow results establish repository/package health but do not supersede the failed live durable-delivery acceptance.

## Evidence artifacts

Read-only evidence root:

```text
C:\Users\CDQ-P\AppData\Local\Temp\cnx-next-20260830T181656Z
```

Key files:

- `preflight.json` — pre-send health, database rows/schema, and transcript snapshot
- `nonce.json` — frozen nonce and exact prompt/expected answer
- `send-ledger.json` — one-shot semantic Send accounting
- `mid-observation-1.json` — Ticket correlation while the model was running
- `postflight.json` — immediate post-response snapshot
- `durable-observation.json` — final Ticket/events/failure state and exact-ID log search
- `postsettlement.json` — final health and database snapshot
- `uniqueness-evidence.json` — role-aware transcript uniqueness and evidence hashes
- `capture_state.py` — read-only snapshot collector

No credentials or secrets are included in this report.

## Hard-fence compliance

- Exactly one authorized Dashboard semantic Send: yes
- Retry after Send: no
- Second nonce/prompt: no
- Source repair: no
- Test modification: no
- OpenClaw source patch: no
- Dependency upgrade: no
- Install-over/uninstall/reinstall/reset: no
- Gateway/provider/supervisor restart or mutation: no
- Manual Ticket/workflow/result/outbox/delivery/database mutation: no
- Manual recovery/resume: no
- Release/tag/package publication: no
- Merge to default/release branch: no
- Force push: no

Repository change for this task is limited to this matching report.

## Why the disposition is FAIL

Task-166 required all of the following together:

1. one authorized Dashboard Send;
2. exactly one visible assistant result;
3. exactly one model call;
4. a durable exact-result row with stable identity;
5. native transcript receipt carrying the marker/identity;
6. transcript-confirmed settlement to delivered;
7. no retry, recovery injection, second inference, or duplicate.

Criteria 1, 2, 3, and 7 passed. Criteria 4, 5, and 6 failed:

- no durable assistant-delivery row was created;
- the native assistant transcript lacked the delivery marker and idempotency identity;
- the Ticket never received `delivery_confirmed_at` and finalized as permanent failure with `durableDelivery:false`.

Therefore the only evidence-supported disposition is **FAIL**.

## Review boundary

Hermes stops after publishing this Task-166 report. Any root-cause investigation, source repair, TDD cycle, reinstall, or second live Dashboard acceptance attempt requires a separate ChatGPT review and a new explicitly authorized task. The Task-166 nonce must not be reused.
