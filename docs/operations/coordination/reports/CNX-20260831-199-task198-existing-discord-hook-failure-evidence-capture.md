# CNX-20260831-199 — Task 198 Existing Discord Hook Failure Evidence Capture

- **Task:** CNX-20260831-199
- **Parent:** CNX-20260831-198
- **Repository:** `funggier/CogentNexus-OpenClaw`
- **Authority branch:** `agent/v0.9.3-full-stabilization`
- **Authority checkout:** `C:/Users/CDQ-P/AppData/Local/Temp/cnx-task198-authority-20260831T`
- **Evidence captured at:** `2026-08-31` (read-only collection)
- **Evidence workspace:** `C:/Users/CDQ-P/AppData/Local/Temp/cnx199-evidence-20260831T152900Z`
- **Disposition:** `EVIDENCE_CAPTURED_ROOT_CAUSE_NOT_PROVEN`

## Scope and hard fences

This task was executed as an evidence-only subtask. The following were not performed:

- no Discord message was sent, retried, regenerated, or injected;
- no reset, uninstall, reinstall, install-over, or session deletion was performed by this task;
- no source, runtime, provider, plugin, installer, or package mutation was performed;
- no workflow dispatch, release mutation, tag mutation, or force push was performed.

The only writes were evidence files under the temporary evidence workspace and this coordination report.

## Fresh authority preflight

The repository was cloned fresh from GitHub on branch `agent/v0.9.3-full-stabilization`. The coordination files identified Task 199 as the active evidence subtask under Task 198. The report was absent in the fresh checkout before this write.

The first baseline invocation used an incorrect harness root and returned `passthrough`/`generation=1`, pointing at a different runtime database. That result was preserved as a harness anomaly and was not used as product evidence. A corrected read-only invocation against the installed CogentNexus runtime root produced the live baseline. No state-changing command was run to resolve the anomaly.

## Runtime baseline

Correct-root baseline artifacts are in:

- `a09-status-correct-root.txt`
- `a10-delivery-correct-root.json`
- `a11-recovery-correct-root.json`
- `a12-gateway-correct-root.json`
- `a13-provider-correct-root.json`
- `a14-storage-correct-root.json`

The database inspected was:

```text
C:/Users/CDQ-P/.openclaw/workspace/.cogentnexus-openclaw/runtime/cogentnexus-openclaw.sqlite3
```

The database was queried read-only. SQLite integrity remained `ok` in the captured baseline.

## Session A and Session B correlation

Both sessions used the same Discord prompt and prompt SHA-256:

```text
Prompt: @Ce สวัสดีครับ
Prompt SHA-256: 129996ffe3efa4d905536e2b73077efc093f2b3a8e6aeef2c16bfeec5061b775
```

### Session A

```text
Session key: agent:main:discord:channel:1531201432861282405
Session diagnostic UUID: a42bdfa3-0616-4e5e-985e-94ff15dc4be7
Ticket: CNXT-a7b576ed-94ee-46b8-82d5-55cc7605aefd
Run: cdb5839e-b245-4098-a082-981bf99b834e
Model call: cdb5839e-b245-4098-a082-981bf99b834e:model:1
```

SQLite records show:

- ticket status: `completed`;
- `created_at`: `2026-08-31T09:48:36.684Z`;
- `response_ready_at`: `2026-08-31T10:03:29.957Z`;
- `delivery_confirmed_at`: `2026-08-31T10:03:45.853Z`;
- direct model outcome: `completed`;
- duration: `893093 ms`;
- recovery attempts: `0`;
- lifecycle events: `accepted → routed → direct_model_call_started → direct_model_call_ended → response_ready → delivery_confirmed → completed`.

Important limitation: the retained logs also contain later fail-closed hook warnings for this same Discord session key, but they do not contain a structured exception payload that can be joined unambiguously to the completed Ticket A run. Therefore the exact exception for the user-described blocked attempt is **not recoverable from retained evidence**.

The exact log messages available for the blocked path are:

```text
CogentNexus-OpenClaw delivery-observe {"event":"handler-skip","reason":"missing-run-correlation"}
before_agent_run hook failed; blocking request
```

Other retained entries show `missing-append-before-deliver` in the same runtime, but no stack trace, exception class, or structured error object is present for this task's Session A blocked path.

### Session B

```text
Session key: agent:main:discord:channel:1531199905673252946
Session diagnostic UUID: 119ef92d-271f-4d6f-ada6-ae7504bb35b3
Ticket: CNXT-50d93e89-a04b-421d-bad2-b2c747f646da
Run: 65f3abad-9817-4c7a-aeb7-1feeafda5213
Model call: 65f3abad-9817-4c7a-aeb7-1feeafda5213:model:1
```

SQLite records show:

- ticket status: `completed`;
- `created_at`: `2026-08-31T14:41:20.843Z`;
- `response_ready_at`: `2026-08-31T14:56:33.668Z`;
- `delivery_confirmed_at`: `2026-08-31T14:56:49.816Z`;
- direct model outcome: `completed`;
- duration: `912602 ms`;
- recovery attempts: `0`;
- lifecycle events: `accepted → routed → direct_model_call_started → direct_model_call_ended → response_ready → delivery_confirmed → completed`.

The user separately confirmed the Discord answer was visible. That proves the user-visible surface outcome for B, but it does not by itself prove the native durable delivery table.

## Durable delivery and native Discord evidence

For both exact tickets, the read-only SQLite query returned:

```text
cnx_assistant_delivery: []
ticket_outbox: []
```

This means the following are present:

- Ticket-level `delivery_confirmed_at`;
- lifecycle `delivery_confirmed` event;
- lifecycle `completed` event;

but the corresponding `cnx_assistant_delivery` durable rows are absent for both A and B.

A search across the retained OpenClaw logs, temporary observer output, and available JSONL ledger material did not find a native `message_sent`, `confirmDirectDelivery`, or `reply_dispatch` record that can be joined to either exact run. This is recorded as **NOT FOUND**, not as proof that Discord did not send the message.

## Session-generation and deletion-barrier evidence

For Session A, retained logs show session deletion-barrier completions at generations `1`, `2`, `3`, and `4`, each reporting `tickets=0` and `assistantSuppressed=0` at the barrier log point. Two deletion attempts also returned:

```text
errorCode=INVALID_REQUEST
errorMessage=Session agent:main:discord:channel:1531201432861282405 changed before deletion. Retry.
```

These entries demonstrate session lifecycle churn and optimistic-concurrency rejection around deletion. They do **not** prove that deletion caused the hook failure, and this report makes no such root-cause claim.

## Findings

1. Session A is not accurately classified as “no Ticket ever existed.” A completed Ticket/run exists for the same session key and prompt.
2. The user-described blocked path is evidenced by `missing-run-correlation` followed by `before_agent_run hook failed; blocking request`, but the exact underlying exception is absent from retained logs.
3. Session B has the same successful Ticket/model/lifecycle shape as Session A.
4. Both A and B lack a corresponding `cnx_assistant_delivery` row, so durable native delivery accounting is unproven for both.
5. No exact native Discord `message_sent` correlation record was found in the retained evidence set.
6. Session A has generation/deletion-barrier churn, including two `changed before deletion` errors, but causal attribution is not proven.
7. The incorrect-root baseline and unmatched-file shell summary are harness/collection anomalies only; they did not mutate runtime state or determine the product outcome.

## Acceptance disposition

```text
EVIDENCE_CAPTURED_ROOT_CAUSE_NOT_PROVEN
```

This report supplies the evidence requested by Task 199 and stops at the authorized boundary. Root-cause analysis, invariant definition, and any TDD/source change decision remain for the Task 198 coordinator and are not claimed here.

## Evidence manifest

```text
a01-status.txt
 a02-check-delivery.json
 a03-check-recovery.json
 a06-cnxclaw-help.txt
 a07-cnxclaw-check-help.txt
 a08-recovery-preflight-help.txt
 a09-status-correct-root.txt
 a10-delivery-correct-root.json
 a11-recovery-correct-root.json
 a12-gateway-correct-root.json
 a13-provider-correct-root.json
 a14-storage-correct-root.json
b01-sqlite-correlated.json
b02-openclaw-2026-08-31.log.json
c01-openclaw-2026-08-30.log.jsonl
c01-openclaw-2026-08-31.log.jsonl
c01-ledger.jsonl.jsonl
c02-A-B-records.json
c04-relevant-log-lines.json
```

Secrets, credentials, tokens, and connection strings were not recorded.
