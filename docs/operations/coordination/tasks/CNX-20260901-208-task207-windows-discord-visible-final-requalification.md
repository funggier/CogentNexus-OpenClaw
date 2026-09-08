# CNX-20260901-208 — Task 207 Windows Discord Visible-Final Requalification

Status: `READY_FOR_HERMES`
Date: 2026-09-01 ICT
Parent: `CNX-20260901-207`
Repair parent: `CNX-20260831-198`
Executor: Hermes / authenticated Windows operator
Coordinator / final reviewer: ChatGPT

## Purpose

Requalify the exact repository-GREEN Task-207 candidate on the accepted real Windows/OpenClaw host with one correctly targeted human Discord Send.

This task tests two boundaries in order:

1. Task-207 visible-final repair: a genuine direct Discord owner Ticket must not terminate as bare `NO_REPLY` without one bounded same-run revision;
2. only after a visible native payload exists, determine whether native delivery settlement reaches `delivery_confirmed -> completed` or whether the previously separate correlation risk is real.

No second Send is authorized.

## Immutable authority

Published `v0.9.3` remains immutable:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

Task-207 exact candidate:

`27fe0181b3b65d555a3b0cc8354f6f7945c21c0b`

Validated package proof:

```text
artifact ID: 9790881384
artifact digest: sha256:1733897690890f9adcb12176b79db2b43e27799a4022743c4597fad44d2d5a34
payload-v2: d0677581d60d3d5535c65e3261dae6f50d7aeb245b8680adac0cace4c040643b
payload files: 192
tar.gz SHA-256: 0ab3884621a518b4cfd46949e3c8e3e7f9f52995bee257743960dd7636794dcf
zip SHA-256: 0321028fc6214e18dbc965ad79a6d04328a05a84dce6a9efc058fb1122237986
```

CI authority for the exact candidate:

```text
Validate: 33483589170 success
Windows Installer Pack Smoke: 33483589124 success
PS5.1 Acceptance Smoke: 33483589138 success
```

Target Discord identity:

```text
channel ID: 1531199905673252946
owner session: agent:main:discord:channel:1531199905673252946
```

## Historical Task-205 identity — pre-existing recovery fence

Before any install-over or new human Send, inspect the old failed Task-205 Ticket and direct-recovery state:

```text
Ticket: CNXT-f23e2c11-e630-4319-84c2-c57ed7e7edf6
run: b79dbb65-15eb-4b3e-8ffb-4084125e6cb5
old nonce: CNX205-20260831T190442Z-8cdbed
```

Task 206 observed a later `direct_redelivery_timeout` and a pending recovery row with `attempt_count=0`.

### Mandatory safety gate

Freshly determine whether this old recovery is now:

- absent/terminal/superseded and incapable of delayed output; or
- still `pending` / `running` / otherwise eligible to produce a delayed Discord response.

If the old recovery can still emit output, **STOP before install-over and before any new Discord Send** with disposition:

`BLOCKED_PREEXISTING_TASK205_RECOVERY`

Do not manually edit SQLite, do not force-set recovery state, and do not send a probe. Preserve evidence for coordinator review.

## Phase A — fresh read-only baseline

Capture exact prestate:

- current date/time and host identity;
- OpenClaw version exactly `2026.7.1-2 (0790d9f)`;
- current installed CogentNexus plugin/source/package fingerprint;
- `cnxclaw status` / Host mode;
- startup adapter state;
- plugin enabled/loaded state;
- Gateway health;
- Ollama health/model visibility;
- delivery/recovery verdicts;
- SQLite integrity;
- Ticket / ticket_event / direct model call / direct recovery / assistant delivery / outbox counts;
- lifecycle process residue;
- Task-205 old recovery adjudication above.

No mutation is allowed until the old recovery safety gate passes.

## Phase B — install-over exact Task-207 candidate once

Use the retained validated package proof for exact candidate `27fe018...`; verify artifact/archive hashes before executing.

Run exactly one supported install-over. Do not reset, uninstall, fresh reinstall, or use a second installer invocation.

### Windows process-exit evidence

Avoid the Task-200 ambiguous parent-shell wait shape. Launch the installer as a standalone child process with an explicit command line equivalent to:

```text
powershell.exe -NoProfile -ExecutionPolicy Bypass -File <exact install.ps1>
```

Capture:

- exact PID and creation time;
- full command line;
- stdout/stderr files;
- terminal process disappearance / exit result using the accepted bounded poll strategy;
- final installer completion line/result.

Allow a bounded observation window consistent with earlier successful install-over evidence. Do not interpret intermediate diagnostic-stage completion as terminal installer completion.

If the original invocation remains genuinely stuck, stop. Do not rerun it.

## Phase C — provenance and managed-health gate

After install-over terminal success, prove:

- installed source/package identity corresponds exactly to `27fe018...`;
- expected Task-207 production bytes are present;
- no unexpected product drift;
- Host is `managed`;
- startup adapter enabled/Ready;
- CogentNexus plugin enabled and loaded;
- Gateway healthy;
- Ollama healthy and accepted model available;
- delivery verdict READY;
- recovery verdict READY;
- SQLite integrity `ok`;
- no lifecycle residue;
- no unexpected Ticket/model/delivery/recovery/outbox deltas occurred during install-over.

If any gate fails, stop before Discord.

## Phase D — exact Discord room gate

Prove the active operator acceptance surface is numeric channel ID exactly:

`1531199905673252946`

Do not rely on room name or window title alone. No probe message is allowed.

Only after exact numeric identity is proven may Hermes generate a fresh Task-208 nonce.

## Phase E — one human Send

Human Send budget:

`0 / 1 consumed; 1 / 1 available`

Generate a fresh nonce of form:

`CNX208-<UTCSTAMP>-<RANDOM>`

Ask the user to manually send exactly once in channel `1531199905673252946`:

`@Ce ตอบกลับข้อความนี้เพียงว่า <NONCE>`

Then wait for the user to say `ส่งแล้ว`.

No Hermes/API/bot/injected Send, retry, regenerate, second room, second nonce, or second human Send.

## Phase F — run/model/finalization evidence

Correlate the new nonce to exactly one new Ticket and one owner run.

Allowed model-call shape:

- one normal direct model call; and
- **at most one additional same-run finalization revision attempt** if the first natural final was exact bare `NO_REPLY`.

Capture enough evidence to distinguish:

### Case 1 — first final already visible

No Task-207 revision is required. Continue to native delivery proof.

### Case 2 — first final is bare `NO_REPLY`

Prove the installed Task-207 `before_agent_finalize` guard returns exactly one bounded same-run revision with:

```text
idempotency key: cnxclaw-discord-visible-final:<runId>
maxAttempts: 1
```

Then prove the revised final is visible substantive text matching the requested nonce semantics and is not bare `NO_REPLY`.

### Failure cases

If bare `NO_REPLY` reaches terminal channel dispatch again without the bounded revision, stop:

`FAIL_TASK207_NO_REPLY_GUARD_NOT_EFFECTIVE`

If one revision occurs but the revised final is still bare `NO_REPLY` and no visible payload exists, stop:

`FAIL_TASK207_REVISION_EXHAUSTED_NO_VISIBLE_FINAL`

Do not send again.

## Phase G — native visible delivery and durable settlement

Require one native visible Discord assistant reply for the new human Send.

Capture, if available:

- native Discord message ID;
- `reply_dispatch` event/context run/session correlation shape;
- callback availability/registration;
- `reply_payload_sending` evidence;
- `message_sent` success/failure, sessionKey/runId/messageId fields;
- final dispatcher failed/cancelled counts;
- Ticket/run chosen for settlement.

Then inspect durable state.

### PASS chain

```text
1 human Send
-> 1 Ticket
-> 1 owner run
-> 1 normal model call (+ at most 1 same-run finalization revision if needed)
-> 1 visible native Discord reply
-> response_ready
-> delivery_confirmed
-> completed
```

No duplicate Ticket, no second user-visible reply, no duplicate delivery settlement, no unrelated recovery, no terminal outbox residue.

### Separate correlation failure

If a visible native Discord reply is definitely observed but the Ticket remains unconfirmed/not completed, stop without repair or second Send:

`FAIL_VISIBLE_REPLY_UNSETTLED__CORRELATION_DEFECT_CONFIRMED`

Retain exact hook/event shape. This is the trigger for a separate repository TDD task; do not modify `reply_dispatch`/`message_sent` in Task 208.

### Native delivery failure

If a visible final payload exists but Discord native delivery itself fails before a visible message appears, classify separately with exact retained evidence and stop without retry.

## Phase H — final health

After the single attempt, capture:

- Host managed;
- startup/plugin/Gateway/Ollama healthy;
- delivery/recovery verdicts;
- SQLite integrity;
- lifecycle residue;
- final Ticket/event/model-call/recovery/delivery/outbox deltas.

## Hard fences

- no second Discord Send;
- no probe Send;
- no API/bot/injected Send;
- no reset/uninstall/fresh reinstall;
- no installer retry;
- no provider/model replacement;
- no manual SQLite mutation;
- no process kill except an explicitly separately authorized identity-fenced cleanup after a STOP disposition;
- no source/test/workflow mutation;
- no Release/tag/asset mutation;
- no force push.

## Evidence/report

Store bounded evidence under a fresh `%LOCALAPPDATA%\Temp\cnx208-*` directory.

Report to:

`docs/operations/coordination/reports/CNX-20260901-208-task207-windows-discord-visible-final-requalification.md`

Allowed terminal dispositions include:

- `PASS_TASK207_WINDOWS_DISCORD_REQUALIFICATION`
- `BLOCKED_PREEXISTING_TASK205_RECOVERY`
- `BLOCKED_INSTALL_OR_HEALTH_GATE`
- `FAIL_TASK207_NO_REPLY_GUARD_NOT_EFFECTIVE`
- `FAIL_TASK207_REVISION_EXHAUSTED_NO_VISIBLE_FINAL`
- `FAIL_VISIBLE_REPLY_UNSETTLED__CORRELATION_DEFECT_CONFIRMED`
- `FAIL_NATIVE_DISCORD_DELIVERY`
- another precise evidence-backed blocker.

Stop after publishing the report. Do not self-repair a newly discovered correlation/native-delivery defect.
