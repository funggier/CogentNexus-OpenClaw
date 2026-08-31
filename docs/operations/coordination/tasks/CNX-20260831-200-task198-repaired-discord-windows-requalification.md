# CNX-20260831-200 — Task 198 Repaired Discord Windows Requalification

Status: `READY_FOR_HERMES`
Date: 2026-08-31 ICT
Parent: `CNX-20260831-198`
Executor: Hermes / authenticated Windows operator
Coordinator / final reviewer: ChatGPT

## Purpose

Perform the minimum live Windows requalification required after the Task-198 production repair changed plugin bytes.

This task validates the repaired Discord/native Direct surface on the real Windows/OpenClaw/Ollama host. It does **not** repeat the broader reset/uninstall/fresh-install lifecycle acceptance and does **not** modify the already-published v0.9.3 Release.

## Immutable repair candidate

Use exactly:

`9f4eaa429b2540540e7d6f6c2af99067960e45fb`

Do not substitute branch HEAD after coordination-only commits.

Package proof authority:

- version: `0.9.3`
- payload file count: `190`
- payload-v2 fingerprint:
  `db5fbd96630ac3685c0588e3d5009dce68e0052bc03f8dab5fdb29577410b27d`
- package-proof artifact ID: `9766213750`
- artifact digest:
  `f8190f9a1fe347be47c69fb9d9a6df2ade2edf8666fd25bfe57efff233f109d7`
- tar.gz SHA-256:
  `379f0b4a7c12d4f350e0d3065dd25c7ab2bde80089adb16bfa64d6bbc673cdfb`
- zip SHA-256:
  `07bcdc45810c86efb5535075e1e560f9477e65a1f72e5299d75dea6dbc542d3e`

Repository gates already GREEN at this exact candidate:

- Validate `33413832703`: `completed/success`
- Windows Installer Pack Smoke `33413832709`: `completed/success`
- PS5.1 Acceptance Smoke `33413832777`: `completed/success`

## Repair under test

Task 198 proved that a transient SQLite writer lock slightly longer than the base five-second busy timeout could escape Ticket-first `before_agent_run` admission as:

```text
ERR_SQLITE_ERROR
errcode: 5
database is locked
```

OpenClaw treats `before_agent_run` exceptions as fail-closed and blocks the request.

The repaired candidate retries `TicketStore.accept()` exactly once only for that exact transient SQLite BUSY/LOCKED error class. Persistent contention still fails closed. No provider, delivery, recovery, authorization, or lifecycle semantics were intentionally changed.

**Do not artificially lock the production SQLite database in this task.** The deterministic repository integration test already proves the contention behavior. This live task checks installation/runtime/Discord regression only.

## Phase A — read-only pre-state

Before installation, capture without mutation:

1. current date/time;
2. current installed CogentNexus/OpenClaw product/provenance identity;
3. OpenClaw version — expected accepted baseline `2026.7.1-2 (0790d9f)`;
4. Host mode — expected `managed`;
5. selected provider/model readiness — managed provider must remain Ollama;
6. Gateway status/listen health;
7. SQLite `PRAGMA integrity_check` — expected `ok`;
8. Ticket/delivery/recovery/outbox counts and pending-state summary;
9. relevant Discord session state for the known healthy room used in Task 196:
   `agent:main:discord:channel:1531199905673252946`.

Do not delete/reset/recreate the Discord session merely to simplify the test.

## Phase B — one supported install-over

Perform exactly one supported install-over from the exact frozen candidate:

`9f4eaa429b2540540e7d6f6c2af99067960e45fb`

Use the repository-supported installer path/archive mechanism. Do not use a nonexistent `cnxclaw install` command.

Capture:

- exact source/candidate provenance;
- installer exit code;
- installed package/plugin identity;
- installed repair files/compiled payload evidence sufficient to prove the Task-198 bytes are active;
- post-install Host/Gateway/Ollama health;
- post-install SQLite integrity;
- durable counts before the human send.

No reset, uninstall, fresh reinstall, provider replacement, or state deletion is authorized.

## Phase C — prepare exactly one human Discord Send

Use the known healthy Discord room/session:

`agent:main:discord:channel:1531199905673252946`

Hermes must generate a fresh nonce that has not appeared in prior transcripts or logs, for example in this shape:

`CNX200-<UTC timestamp>-<short random suffix>`

Hermes then tells the user the **exact single Discord message** to send manually in the normal Discord UI. Use a compact direct request such as:

`ตอบกลับข้อความนี้เพียงว่า <NONCE>`

Do not have Hermes, a bot, CLI, API, `chat.inject`, or any automation send the human message.

After giving the exact prompt, Hermes must stop and wait for the user to say:

`ส่งแล้ว`

### Single-send budget

- human Discord Send: exactly `1 / 1`
- Hermes/bot/API Send: `0`
- retry: `0`
- regenerate: `0`
- second room/message: `0`
- injection: `0`

If the one human Send fails visibly, do not send a second message under this task. Capture evidence and report the failure.

## Phase D — durable correlation after `ส่งแล้ว`

Immediately correlate the one human message through durable state and retained logs.

Required accepted shape:

`1 human Discord Send -> 1 Ticket -> 1 Direct model call -> response_ready -> 1 native visible Discord assistant result -> delivery_confirmed -> completed`

Capture at minimum:

- human prompt/nonce hash or safely bounded exact nonce;
- Discord owner session key;
- Ticket ID;
- Ticket request key / prompt SHA-256 if available;
- run ID;
- model call ID;
- provider/model;
- ordered Ticket events;
- `response_ready_at`;
- `delivery_confirmed_at`;
- terminal Ticket status;
- Ticket/outbox/recovery deltas;
- relevant OpenClaw/CogentNexus logs around the run;
- user-visible Discord evidence or authoritative channel-delivery evidence.

### Required negative checks

For this tested send:

- `before_agent_run hook failed` must **not** occur;
- no duplicate Ticket;
- no duplicate model call;
- no Direct Recovery attempt;
- no regenerated assistant response;
- no pending Ticket outbox residue;
- no stuck/pending assistant-delivery residue attributable to the tested send;
- no provider substitution.

### Important observer semantics

Do **not** fail the test solely because a redacted Dashboard observer logs:

`missing-run-correlation`

or

`missing-append-before-deliver`

Those diagnostics were proven non-blocking observer skips on non-Dashboard transports.

Do **not** require a `cnx_assistant_delivery` row for this native Discord Direct result. The accepted native external-channel contract may terminal through Ticket-level `message_sent` / `confirmDirectDelivery` evidence. Record whether such a row exists, but absence alone is not failure.

## Phase E — post-state health

After the single send settles, capture:

- Gateway health;
- managed Ollama/provider readiness;
- Host/recovery state;
- SQLite integrity;
- pending outbox/recovery/delivery counts;
- exact installed provenance.

No cleanup that deletes evidence is authorized.

## Acceptance criteria

PASS requires all of the following:

1. exact candidate `9f4eaa...` installed successfully through one supported install-over;
2. active installed plugin identity proves the repaired candidate bytes;
3. OpenClaw/Gateway/managed Ollama/SQLite remain healthy;
4. exactly one genuine human Discord Send was used;
5. exactly one Ticket and one model call correlate to that Send;
6. the requested nonce is returned as one native visible Discord assistant result;
7. Ticket reaches `response_ready -> delivery_confirmed -> completed`;
8. no retry/recovery/duplicate/outbox residue;
9. no `before_agent_run hook failed` for the tested send;
10. no destructive lifecycle or publication action occurred.

## Failure / stop rules

Stop and report without another human send if any of these occur:

- install-over failure;
- candidate/provenance mismatch;
- Gateway/provider/SQLite health failure;
- the one human Discord Send is blocked or produces wrong semantic output;
- duplicate Ticket/model/reply;
- recovery becomes active;
- `before_agent_run hook failed` occurs for the tested run;
- evidence cannot safely correlate the one Send.

Do not repair source under Task 200. Any new product defect returns to ChatGPT for a new repository task.

## Hard fence

No force push, no tag/Release mutation, no v0.9.3 republish, no reset, no uninstall, no fresh reinstall, no state deletion, no artificial SQLite lock, no provider/model replacement, no synthetic human send, no retry/regenerate/second Discord send, and no product/source/test/workflow edits.

## Report

Publish when terminal:

`docs/operations/coordination/reports/CNX-20260831-200-task198-repaired-discord-windows-requalification.md`

Final disposition must be one of:

- `PASS`
- `FAIL_INSTALL_OVER`
- `FAIL_PROVENANCE`
- `FAIL_DISCORD_BEFORE_AGENT`
- `FAIL_DISCORD_SEMANTIC_DELIVERY`
- `FAIL_DURABLE_CORRELATION`
- `FAIL_HEALTH`
- `BLOCKED_EVIDENCE`

Then stop for ChatGPT review.