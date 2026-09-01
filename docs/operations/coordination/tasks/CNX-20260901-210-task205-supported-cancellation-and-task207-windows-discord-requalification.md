# CNX-20260901-210 — Task-205 Supported Cancellation + Task-207 Windows Discord Requalification

Status: `READY_FOR_HERMES`
Date: 2026-09-01 ICT
Parent: `CNX-20260901-209`
Repair parent: `CNX-20260831-198`
Executor: Hermes / authenticated Windows operator
Coordinator / final reviewer: ChatGPT

## Purpose

Resolve the one proven executable historical Task-205 recovery using the product's supported exact-run session-boundary cancellation semantics, prove that the old recovery can no longer emit output, then continue directly into the deferred exact Task-207 Windows install-over and one-send Discord visible-final requalification.

This task deliberately combines cleanup and requalification only because Task 209 proved that the target Discord owner session has no unrelated same-session nonterminal/emittable work.

## Immutable authority

Published `v0.9.3` remains immutable:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

Do not retarget, republish, overwrite, or mutate that Release/tag/assets.

Repository-GREEN Task-207 candidate:

`27fe0181b3b65d555a3b0cc8354f6f7945c21c0b`

Validated package proof:

```text
artifact ID: 9790881384
artifact digest: sha256:1733897690890f9adcb12176b79db2b43e27799a4022743c4597fad44d2d5a34
payload-v2 fingerprint: d0677581d60d3d5535c65e3261dae6f50d7aeb245b8680adac0cace4c040643b
payload files: 192
tar.gz SHA-256: 0ab3884621a518b4cfd46949e3c8e3e7f9f52995bee257743960dd7636794dcf
zip SHA-256: 0321028fc6214e18dbc965ad79a6d04328a05a84dce6a9efc058fb1122237986
```

Exact-head CI authority:

```text
Validate: 33483589170 success
Windows Installer Pack Smoke: 33483589124 success
PS5.1 Acceptance Smoke: 33483589138 success
```

Accepted OpenClaw baseline:

`2026.7.1-2 (0790d9f)`

Target Discord identity:

```text
channel ID: 1531199905673252946
owner session: agent:main:discord:channel:1531199905673252946
```

## Historical Task-205 identity

```text
Ticket: CNXT-f23e2c11-e630-4319-84c2-c57ed7e7edf6
run: b79dbb65-15eb-4b3e-8ffb-4084125e6cb5
nonce: CNX205-20260831T190442Z-8cdbed
owner session: agent:main:discord:channel:1531199905673252946
```

Task 209 fresh evidence at `2026-09-01T08:57:10.821Z` proved:

```text
Ticket status: accepted
workflow_eligible: 0
workflow_id: null
session: active / generation 0
recovery: redeliver / pending
recovery owner_generation: 0
attempt_count: 0
active_run_id: null
due_by_time: true
active/recovering model calls: 0
production-equivalent scheduler selection: exact Task-205 Ticket selected
same-session unrelated emittable residue: none
SQLite integrity: ok
```

## Supported cancellation authority

The currently installed pre-Task-207 product lineage exports:

`cancelSessionTickets(path,{runId,...})`

from the installed compiled `dist/v090.js` module.

The same exported semantics are present at the currently installed repaired lineage `9f4eaa429b2540540e7d6f6c2af99067960e45fb` and at Task-207 source. The function resolves owner session from the exact supplied run ID and delegates to the normal session-boundary cancellation path; that path increments session generation, cancels nonterminal Tickets for that exact owner session, and cancels direct-recovery state without raw/manual SQLite edits.

Task 210 authorizes exactly one invocation of this supported function for the exact historical run ID after a fresh scope gate.

Raw `UPDATE`/`DELETE` SQLite statements are forbidden.

## Phase A — fresh pre-cancellation read-only gate

Create a fresh evidence directory under:

`%LOCALAPPDATA%\Temp\cnx210-*`

Capture fresh UTC timestamp and read-only runtime state:

- OpenClaw exact baseline;
- Host mode;
- startup adapter;
- Gateway;
- Ollama/provider/model visibility;
- delivery/recovery checks;
- SQLite integrity;
- installed plugin root and current installed product identity/fingerprint;
- lifecycle/recovery process residue.

Then reproduce the Task-209 same-session inventory immediately before mutation.

Cancellation is allowed only if all are still true:

```text
owner session state = active
historical Ticket status = accepted
historical recovery state = pending
historical recovery is still the exact one selected by production-equivalent scheduler query
same-session nonterminal Tickets = exactly 1 and it is the historical Task-205 Ticket
same-session nonterminal/emittable direct recoveries = exactly 1 and it belongs to that Ticket
same-session pending assistant deliveries = 0
same-session pending outbox rows = 0
same-session active/recovering model calls = 0
no unrelated same-session workflow
SQLite integrity = ok
```

If any inventory has changed, STOP before cancellation with:

`BLOCKED_CANCELLATION_SCOPE_CHANGED`

Do not try to normalize the state.

## Phase B — resolve installed cancellation module

Resolve the actual currently installed CogentNexus-OpenClaw plugin root from live ownership/OpenClaw authority. Do not guess from a stale temp path.

Require:

- installed plugin root exists;
- compiled module `dist/v090.js` exists under that installed plugin root;
- the module exports `cancelSessionTickets` as a function;
- the Ticket database path is the current workspace default:
  `<workspace>/.cogentnexus-openclaw/runtime/cogentnexus-openclaw.sqlite3`, unless live plugin config explicitly proves another path;
- the database is the same live database observed in Phase A.

A read-only module-load/export check is allowed. Do not invoke cancellation during the check.

If the supported function cannot be resolved from the installed product, STOP:

`BLOCKED_SUPPORTED_CANCELLATION_SURFACE_UNAVAILABLE`

Do not fall back to raw SQLite mutation.

## Phase C — one exact-run supported cancellation

Create an ephemeral evidence-harness `.mjs` outside repository/product directories. The harness may only:

1. import the installed `dist/v090.js`;
2. call `cancelSessionTickets` exactly once;
3. pass the exact live DB path;
4. pass exact run ID:
   `b79dbb65-15eb-4b3e-8ffb-4084125e6cb5`;
5. use a bounded reason such as:
   `explicit user stop: Task 205 stale recovery cleanup`;
6. print the returned result as JSON.

No second invocation is authorized.

Expected result if prestate remains generation 0:

```text
ownerSessionKey = agent:main:discord:channel:1531199905673252946
generation = 1
cancelled = [CNXT-f23e2c11-e630-4319-84c2-c57ed7e7edf6]
workflowIds = []
assistantSuppressed = 0
outboxTags = []
```

If the prestate generation is not 0 but all scope gates remain valid, require exactly `new_generation = old_generation + 1`; do not hard-fail solely because the absolute number differs.

If returned owner session or cancelled Ticket set contains anything unexpected, STOP immediately:

`FAIL_SUPPORTED_CANCELLATION_SCOPE`

Do not compensate with a second cancellation.

## Phase D — post-cancellation proof

Immediately verify read-only:

- owner session remains `active`;
- session generation advanced exactly once;
- historical Task-205 Ticket status is `cancelled`;
- historical Task-205 recovery state is `cancelled`;
- `active_run_id` cleared;
- `next_attempt_at` cleared;
- exact production-equivalent scheduler query no longer selects Task-205;
- no nonterminal same-session Ticket remains;
- no pending/running/awaiting-delivery recovery remains for the session;
- no pending assistant delivery;
- no pending outbox;
- no active/recovering model call;
- SQLite integrity `ok`;
- no user-visible Discord output was produced by cancellation.

If these fail, STOP before install-over:

`FAIL_CANCELLATION_POSTSTATE`

## Phase E — exact Task-207 artifact verification

Use the retained exact Task-207 package proof. Verify artifact/archive/provenance hashes before executing anything from it.

Require exact:

```text
sourceCommit = 27fe0181b3b65d555a3b0cc8354f6f7945c21c0b
packageVersion = 0.9.3
payloadV2Fingerprint = d0677581d60d3d5535c65e3261dae6f50d7aeb245b8680adac0cace4c040643b
payloadFileCount = 192
zip SHA-256 = 0321028fc6214e18dbc965ad79a6d04328a05a84dce6a9efc058fb1122237986
```

Do not publish this archive as `v0.9.3`; public `v0.9.3` is immutable and points to older code.

## Phase F — one supported install-over

Run exactly one install-over of Task-207 candidate.

Do not reset, uninstall, fresh reinstall, or issue a second install command.

Avoid the Task-200 ambiguous parent-shell shape. Launch installer as a standalone explicit child process equivalent to:

```text
powershell.exe -NoProfile -ExecutionPolicy Bypass -File <exact Task-207 install.ps1>
```

Capture:

- PID;
- creation time;
- full command line;
- stdout/stderr;
- terminal exit/disappearance using bounded polling;
- exact exit code if directly available;
- final installer completion line.

Do not infer success from intermediate diagnostic stages.

If original installer remains genuinely stuck, STOP without retry:

`BLOCKED_INSTALLER_TERMINAL`

## Phase G — installed provenance + managed-health gate

After terminal installer success prove:

- installed product/package corresponds exactly to Task-207 candidate `27fe0181...`;
- Task-207 production bytes are present;
- ownership verify passes;
- Host is `managed`;
- startup adapter enabled/Ready;
- plugin enabled and loaded without error;
- Gateway healthy;
- Ollama ready and accepted model visible;
- delivery READY, pending 0;
- recovery READY and no Task-205 recovery resurrected;
- SQLite integrity `ok`;
- no lifecycle residue;
- no unexpected Ticket/model/recovery/delivery/outbox delta caused by install-over.

If any fail, STOP before Discord:

`BLOCKED_INSTALL_OR_HEALTH_GATE`

## Phase H — exact Discord room gate

Prove the operator acceptance surface is numeric channel ID exactly:

`1531199905673252946`

Owner session must be:

`agent:main:discord:channel:1531199905673252946`

Do not rely on room name or window title alone. No probe message is allowed.

If exact numeric identity cannot be proven, STOP before nonce generation.

## Phase I — one new human Discord Send

Task-210 live acceptance budget:

`0 / 1 consumed; 1 / 1 available`

Generate one fresh nonce only after all prior gates pass:

`CNX210-<UTCSTAMP>-<RANDOM>`

Ask the user to manually send exactly once in channel `1531199905673252946`:

`@Ce ตอบกลับข้อความนี้เพียงว่า <NONCE>`

Then wait for user to say `ส่งแล้ว`.

No Hermes/API/bot/injected Send, no probe, no second nonce, no retry, no regenerate, no second room, no second human Send.

## Phase J — Task-207 visible-final proof

Correlate the fresh nonce to exactly one new Ticket and owner run.

Allowed inference shape:

- one normal direct model call;
- at most one additional same-run finalization revision if the first natural final is exact bare `NO_REPLY`/`no_reply`.

### Case A — natural visible final

If the first final is already visible substantive text, no revision is required. Continue to native delivery settlement proof.

### Case B — first final is bare `NO_REPLY`

Require one Task-207 bounded revision with:

```text
idempotency key: cnxclaw-discord-visible-final:<runId>
maxAttempts: 1
```

Then require revised final to be visible and not bare `NO_REPLY`.

If the guard is not invoked when required:

`FAIL_TASK207_NO_REPLY_GUARD_NOT_EFFECTIVE`

If one revision is exhausted and final is still bare `NO_REPLY`:

`FAIL_TASK207_REVISION_EXHAUSTED_NO_VISIBLE_FINAL`

No second Send.

## Phase K — native Discord delivery + durable settlement

Require one native visible Discord assistant result corresponding to the fresh Task-210 Send.

Capture if available:

- visible returned nonce semantics;
- native Discord message ID;
- `reply_dispatch` hook/event context;
- `reply_payload_sending` evidence;
- `message_sent` event fields;
- sessionKey/runId/messageId availability;
- dispatcher failed/cancelled counts;
- Ticket/run selected for settlement.

PASS chain:

```text
1 human Send
-> 1 Ticket
-> 1 owner run
-> 1 normal model call (+ at most 1 same-run finalization revision when required)
-> response_ready
-> 1 visible native Discord reply
-> delivery_confirmed
-> completed
```

Require no duplicate Ticket, no second visible reply, no unrelated Direct Recovery, no pending outbox, no provider substitution.

If a visible native Discord reply definitely appears but Ticket remains unconfirmed/not completed, STOP:

`FAIL_VISIBLE_REPLY_UNSETTLED__CORRELATION_DEFECT_CONFIRMED`

Do not repair `reply_dispatch`/`message_sent` in this live task.

If a visible final payload exists but native Discord send itself fails before user-visible delivery:

`FAIL_NATIVE_DISCORD_DELIVERY`

## Phase L — final health

Capture final:

- Host managed;
- startup/plugin healthy;
- Gateway healthy;
- Ollama/provider healthy;
- delivery/recovery verdicts;
- SQLite integrity;
- lifecycle residue;
- exact Task-210 Ticket/event/model/recovery/delivery/outbox deltas;
- historical Task-205 Ticket/recovery remain cancelled and inert.

## Hard fences

- exactly one supported cancellation invocation;
- no raw/manual SQLite mutation;
- no session reset/delete;
- no Gateway restart unless the supported installer itself performs its normal lifecycle actions;
- no installer retry;
- no reset/uninstall/fresh reinstall;
- no provider/model substitution;
- no source/test/workflow mutation;
- no Release/tag/asset mutation;
- no force push;
- no Discord probe/API/bot/injected Send;
- no second human Discord Send;
- no delivery-correlation repair in the live task.

## Evidence/report

Store bounded evidence under fresh `%LOCALAPPDATA%\Temp\cnx210-*`.

Publish:

`docs/operations/coordination/reports/CNX-20260901-210-task205-supported-cancellation-and-task207-windows-discord-requalification.md`

Allowed terminal dispositions include:

- `PASS_TASK207_WINDOWS_DISCORD_REQUALIFICATION`
- `BLOCKED_CANCELLATION_SCOPE_CHANGED`
- `BLOCKED_SUPPORTED_CANCELLATION_SURFACE_UNAVAILABLE`
- `FAIL_SUPPORTED_CANCELLATION_SCOPE`
- `FAIL_CANCELLATION_POSTSTATE`
- `BLOCKED_INSTALLER_TERMINAL`
- `BLOCKED_INSTALL_OR_HEALTH_GATE`
- `FAIL_TASK207_NO_REPLY_GUARD_NOT_EFFECTIVE`
- `FAIL_TASK207_REVISION_EXHAUSTED_NO_VISIBLE_FINAL`
- `FAIL_VISIBLE_REPLY_UNSETTLED__CORRELATION_DEFECT_CONFIRMED`
- `FAIL_NATIVE_DISCORD_DELIVERY`
- another precise evidence-backed blocker.

Stop after publishing the report for ChatGPT review. Do not self-repair a newly discovered delivery-correlation defect.
