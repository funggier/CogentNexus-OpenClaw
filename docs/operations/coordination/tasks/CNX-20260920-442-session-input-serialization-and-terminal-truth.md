# CNX-20260920-442 — Session Input Serialization and Terminal Truth

Status: `SOURCE_QUALIFIED`

State: `SOURCE_QUALIFIED_READY_FOR_LIVE_INSTALL`

Parent: `CNX-20260920-427`

Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`

Executor: `ChatGPT via LConnect`

Reviewer: `ChatGPT`

Human final authority: `Operator`

## Trigger

A live Discord turn on channel `1391855033993138217` exposed a same-session transcript race.

User turn:

`@Ce ช่วยดูหน่อยครับว่าวันนี้เป็นข้างขึ้นข้างแรม`

Authoritative run:

`673cb634-58e2-4706-94d8-0a45e7740784`

CNX Ticket:

`CNXT-8e762028-d5af-4ad9-a56d-8aae89600a9b`

Physical session:

`06e736f1-01e5-45b7-8c0b-bbaa9ed6f700`

The first model call completed and invoked `exec` successfully. During the second model call, native
`/context` mutated the same session transcript. OpenClaw terminated the run with:

`SQLite transcript changed while preparing rewrite for 06e736f1-01e5-45b7-8c0b-bbaa9ed6f700`

No final assistant answer was delivered.

CNX nevertheless recorded the Ticket as `completed`, exposing a terminal-truth mismatch.

Two native command Tickets were also incorrectly admitted and left `accepted`:

- `CNXT-7b523819-6b36-4c83-8ec7-8186e60417cc` — `/context`
- `CNXT-738a99f9-2619-4d50-a574-6b13aa6d1471` — `/context detail`

## Primary goal

Make every owner conversational session safe under concurrent human input while preserving Ticket-first durability.

This contract is **surface-independent**. It applies to Discord, WebChat/Dashboard, and any other supported OpenClaw owner ingress that enters the same reply/session pipeline. Discord is only the reproducing surface; it is not the scope boundary.

Required semantics:

1. Native slash commands handled by OpenClaw must not create CNX conversational Tickets on any supported owner ingress.
2. A new ordinary user turn arriving through any supported owner ingress while another run owns the session must be durably accepted without mutating the active run's transcript.
3. Ordinary queued user turns must preserve FIFO order and idempotency.
4. CNX must not classify a Ticket `completed` until the authoritative host run terminal outcome is known.
5. Host-level failure after model-call completion must settle the owning CNX Ticket as non-success, never completed.
6. Existing CNX-427/CNX-440 Ticket-first and durable Discord settlement guarantees must remain intact.

## Desired serialization

```text
User A
  -> Ticket A -> RUNNING
  -> User B arrives -> durable queue / Ticket B -> QUEUED
  -> User C arrives -> durable queue / Ticket C -> QUEUED
  -> Run A terminal
  -> Ticket A terminal
  -> dequeue B -> Run B
  -> dequeue C -> Run C
```

Native informational commands such as `/context` should stay in OpenClaw's command lane and must not enter
the CNX conversational Ticket pipeline.

Control commands whose purpose is to cancel/reset execution must retain native control semantics rather than
being silently converted into queued conversation.

## Status UI

Status/progress UI work is explicitly out of scope for CNX-442 by operator decision on 2026-09-20.
Decorative host phrases such as `Cracking…` or `Shelling…` are not modified by this task.

## TDD plan

### RED-A — Native command bypass

Prove `/context` and `/context detail` do not create CNX Tickets across representative owner surfaces while ordinary conversational text still does.

### RED-B — Same-session concurrent human turn

Reproduce one active run followed by a second ordinary user message across representative owner surfaces. Prove the second input is durably queued
and cannot mutate the active transcript before the first run reaches terminal state.

### RED-C — Terminal truth

Reproduce the observed ordering where model-call activity completes but the host run later ends in error.
Prove the Ticket cannot reach `completed` before authoritative run terminal success.

## Constraints

- Do not patch installed OpenClaw core files directly unless a supported plugin boundary is proven insufficient and separately escalated.
- Do not manually mutate OpenClaw session SQLite to simulate queueing.
- Do not directly edit live CNX Ticket rows before migration/repair behavior is source-tested.
- Preserve `ollama/qwen3.8:27b` at context `24576` and keep-alive `2h`.
- Source tests first; no live reinstall until the affected regression surface is GREEN.

## Surface-independence requirement

The repair must not special-case Discord for admission, queueing, or terminal truth.

Representative qualification surfaces:

- Discord owner channel;
- WebChat / Dashboard owner session;
- generic owner reply-dispatch context used by other supported OpenClaw ingress paths.

The implementation should prefer host-generic session/reply primitives. Channel-specific code is allowed only where transport semantics truly differ, such as Discord receipt settlement.

Queue policy should therefore be expressed at the OpenClaw messages/session layer rather than only under a Discord adapter.

## Source qualification

Implementation is source-qualified and ready for one supported live install-over.

Implemented boundaries:

- host-native command bypass at `reply_dispatch` using OpenClaw command facts/detection;
- surface-independent owner-session serialization through OpenClaw's supported session API with `queueMode=followup`;
- authoritative terminal reconciliation from exact `trajectory_runtime_events.session.ended` evidence in the owning agent's `openclaw-agent.sqlite`;
- silent successful runs complete only after authoritative Host success without duplicating `response_ready`;
- Host terminal failure clears unconfirmed response-ready state and atomically creates Direct Recovery;
- confirmed/transport-accepted delivery evidence remains fail-closed and is never silently rewritten.

Validation:

- CNX-442 focused suite: 13/13 PASS;
- CNX-440 + Discord/WebChat durable delivery: 11/11 PASS;
- CNX-427 + reply-dispatch/Ticket-first admission: 22/22 PASS;
- Host claim/session ingress fences: 8/8 PASS;
- `src/index.test.ts`: 42/42 PASS;
- v0.9.5 behavior/delivery/session/no-reply matrix: 21/21 PASS;
- total core targeted/integration regression count: **120 PASS**;
- `npm run plugin:validate`: PASS;
- package verification: PASS, 280 packed files;
- mixed-plugin artifact/schema verification: PASS;
- Ticket DB bootstrap: PASS;
- `git diff --check`: PASS;
- TypeScript/plugin build: PASS.

Status/progress UI is not part of this task and is intentionally unchanged.

Next gate:

1. freeze exact candidate commit and push;
2. run one supported `scripts/install.ps1 -Workspace C:\Users\CDQ-P\.openclaw\workspace` install-over;
3. verify live plugin/runtime health, session queue policy, command bypass behavior, and Host-terminal reconciliation without sending a semantic Discord message on the operator's behalf.

## Historical native-command retirement

Live preflight found the two reproducing command Tickets still stranded as `accepted`:

- `CNXT-7b523819-6b36-4c83-8ec7-8186e60417cc` — `/context`;
- `CNXT-738a99f9-2619-4d50-a574-6b13aa6d1471` — `/context detail`.

Both have zero Direct model-call rows, zero inference-attempt rows, zero assistant-delivery rows, and zero Direct-recovery rows.

CNX-442 now includes a bounded startup retirement migration. It retires only an old accepted Direct Ticket when:

- OpenClaw's own command detector recognizes the stored prompt as a native/control command;
- the Ticket is older than the bounded minimum age;
- response/delivery are still absent;
- no model-call, inference, delivery, or recovery evidence exists.

The migration preserves history by terminally cancelling the stranded Ticket and appending `native_command_ticket_retired`. It does not rewrite Tickets that have execution/delivery evidence.

Migration regression coverage: 3/3 PASS.

Additional release/authority wiring qualification after the migration was wired: 8/8 PASS.
