# CNX-20260905-257 — Task256 Pending-Redeliver Recovery Reconciliation

## Final disposition

`RECONCILED_PENDING_REDELIVER_STALE_OWNER__EXPLICIT_DISPOSITION_REQUIRED`

The pending row is a real, emittable `redeliver` recovery item, but current
owner intent is not provable. The owner session is marked `active` in SQLite
while its last durable update is `2026-09-01T09:23:13.389Z`; therefore it is
classified **stale-but-active**, not genuinely live on the evidence available.
The row was not cleared, cancelled, replayed, resent, or otherwise mutated.
Installer requalification remains parked.

Recommendation: keep the row untouched until a separately authorized recovery
reconciliation task proves either (a) current owner intent and a genuinely
live owner-session generation, or (b) an authoritative cancellation/disposition
from the owner. No installer task may be armed while this row satisfies the
live `dueDirectRecovery()` predicates.

## Fresh GitHub authority

Authority was re-fetched from GitHub before investigation.

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`
- Opening/final remote HEAD: `13887bc9f288cd51bf6bfbc0b2e62646e37ab65e`
- `ACTIVE.md` and `STATUS.md`: `READY_FOR_HERMES`, active Task257,
  `TASK257_TASK256_PENDING_REDELIVER_RECOVERY_RECONCILIATION_FORENSIC`
- Task file: `docs/operations/coordination/tasks/CNX-20260905-257-task256-pending-redeliver-recovery-reconciliation.md`
- Public tag: `v0.9.3 = 26ce64a624255278a3a0266ad38746e0e6ed2e31`
- Exact candidate source: `6822af464fe7a5cb3f93305d0263dfc86b56ac68`
- Candidate canonical installer identity: `9d53a427...e17b57b`
- Candidate runner identity: `729fba45...a6250f3e`

The report clone was created fresh from the branch and verified
`HEAD == remote HEAD` before publication. The tag was verified independently
with `git ls-remote`; the single-branch clone did not materialize the tag object
locally, so no local tag claim is substituted for the remote result.

## Evidence and read-only boundary

Durable evidence root:

`C:\Users\CDQ-P\AppData\Local\CogentNexus-OpenClaw\forensics\CNX-20260905-257`

- `fresh-readonly.json` — fresh SQLite schema, integrity, subject rows,
  full subject events, and table counts. Captured `2026-09-05T06:39:59.029427Z`.
  SHA-256: `6124a29f738b16623f7308e6bdd6516f5812c36bff86420b370421c11a986d07`
- `readonly-command-log.txt` — exact read-only authority/tag, process,
  gateway-status, and scheduler commands with outputs/exit evidence.
  SHA-256: `5269da51927d4c3833b872b4102070437edf5b157ea5dccf7a109d22f3d8f5ee`
- SQLite path:
  `C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw\runtime\cogentnexus-openclaw.sqlite3`
- Open mode: `file:<path>?mode=ro`; `PRAGMA integrity_check` returned `ok`.

No write-capable SQLite connection, `VACUUM`, scheduler registration/start,
installer invocation, gateway restart, semantic send, replay, or resend was
performed.

## Exact subject-row binding

Fresh read-only query at `2026-09-05T06:39:59.029427Z` returned:

```text
ticket_id        = CNXT-dc11c9a0-8a89-4df5-9c48-345260725be4
recovery mode    = redeliver
recovery state   = pending
recovery attempts= 0
active_run_id    = NULL
next_attempt_at  = 2026-09-03T01:49:59.316Z (past due)
last_error       = Direct response delivery was not confirmed before deadline
owner_generation = 1
recovery created = 2026-09-03T01:49:59.316Z
recovery updated = 2026-09-03T01:49:59.316Z

Ticket status       = accepted
Ticket run_id       = e225013e-8d50-4479-b227-ca9a10b89a46
owner_session_key   = agent:main:discord:channel:1531199905673252946
workflow_eligible   = 0
workflow_id         = NULL
response_ready_at   = NULL
delivery_confirmed_at= NULL
failure_class       = interrupted
Ticket updated       = 2026-09-03T01:49:59.316Z

Session state        = active
Session generation   = 1
Session updated      = 2026-09-01T09:23:13.389Z
Session deleted_at   = NULL

Model-call rows      = 1
Model-call state     = ended
Model-call outcome   = completed
Model-call provider  = ollama
Model-call model     = qwen3.5:9b
Model-call started   = 2026-09-03T01:46:56.358Z
Model-call ended     = 2026-09-03T01:47:59.117Z
Recovery attempts    = 0

cnx_assistant_delivery rows for Ticket = 0
Ticket outbox rows for Ticket           = 0
```

The row has the same owner generation as the session (`1`), so the generation
predicate does not protect against the stale timestamp. The live gateway was
observed running at PID `17936` on `127.0.0.1:18789` with gateway status exit
`0`, but a running gateway/Discord transport does not prove that this specific
owner session is live. The scheduler query showed no Task255/256/257 installer
registration; only older residue tasks and `OpenClaw Gateway` were present.

## Payload, redeliver mode, and transport trace

The original committed user request in `tickets.prompt` is:

```text
ช่วยสรุปงานที่ฉันควรโฟกัสวันนี้จาก context ล่าสุด และบอกเหตุผลสั้น ๆ
```

The exact candidate source implements the following redeliver behavior:

1. `v091-direct-recovery.ts:58-64` selects `ticket_id`, owner session,
   committed prompt, `mode`, attempt count, and owner generation when the row
   is pending, the Ticket is accepted, workflow admission is false, the owner
   session is active at the matching generation, the timestamp is due, and the
   model-call fence does not exclude it.
2. `v094-direct-recovery` recovery prompt construction (materialized installed
   equivalent `dist/v094-direct-recovery.js:257-272`) selects the `redeliver`
   instruction: `Reconstruct only the compact final response. Do not repeat
   external side effects.` It supplies the committed prompt plus bounded,
   read-only owner-session context, and explicitly says not to send directly.
3. The same source's `dist/v094-direct-recovery.js:496-498` reads owner-session
   messages with limit `24` before embedded execution. The embedded run is
   disabled for tools/message tool, uses the original provider/model, and is
   fenced to the recovery run.
4. On a successful result, `dist/v094-direct-recovery.js:367-408` would create
   one durable `direct_result` delivery with idempotency key
   `cnxclaw-direct-result:<ticket_id>:g1`, preserve the first
   `response_ready_at`, move recovery to `awaiting_delivery`, and record
   `deliveryMode = host-chat-inject`.
5. The transport launcher is `dist/v094-direct-recovery.js:310-324`: it prefers
   `skills/cogentnexus-openclaw/scripts/host_delivery_v092.py`, invokes
   `python ... --root <root> flush`, detaches it, and does not send directly
   from the recovery worker. The script's exact transport implementation is
   `host_delivery_v092.py:46-57`, which invokes the Node OpenClaw CLI gateway
   RPC; delivery failure bookkeeping is bounded to the durable delivery row
   (`host_delivery_v092.py:60-115`).

Thus the pending item represents a reconstruction of the original answer for
injection into the owning Discord channel, not a new user request and not an
installer or semantic-acceptance action.

## Why pending since 2026-09-03

The event sequence is exact from the subject Ticket's `ticket_events` rows:

```text
2026-09-03T01:44:25.903Z  accepted
2026-09-03T01:44:25.908Z  routed, workflowEligible=false
2026-09-03T01:44:26.020Z  direct_model_call_started, call 1
2026-09-03T01:46:04.414Z  direct_model_call_ended, completed, 98,394 ms
2026-09-03T01:46:04.932Z  direct_model_call_started, call 2
2026-09-03T01:46:30.718Z  direct_model_call_ended, completed, 25,787 ms
2026-09-03T01:46:32.489Z  direct_model_call_started, call 3
2026-09-03T01:46:56.150Z  direct_model_call_ended, completed, 23,661 ms
2026-09-03T01:46:56.358Z  direct_model_call_started, call 4
2026-09-03T01:47:59.117Z  direct_model_call_ended, completed, 62,759 ms
2026-09-03T01:47:59.256Z  response_ready
2026-09-03T01:49:59.316Z  direct_redelivery_timeout, cutoff=2026-09-03T01:47:59.316Z
```

The Ticket has `response_ready_at = NULL`, no assistant-delivery row, no outbox
row, and `delivery_confirmed_at = NULL`. The durable failure is therefore a
response-delivery confirmation timeout after completed model work. The
`direct_redelivery_timeout` event created the `pending/redeliver` recovery row
at the same timestamp with `attempt_count = 0`; no later recovery claim,
retry, or delivery attempt is present in the fresh database snapshot.

The source's event-driven service performs an immediate `run()` at service
start (`v091-direct-recovery.ts:190-251`, with the immediate call at `:250`),
then schedules future wakes using `nextDirectRecoveryWakeMs`. A due pending row
would be eligible at service start or at its scheduled wake. The available
Gateway restart log records restarts on 2026-08-16, not on or after the
2026-09-03 row creation. Current gateway status is healthy/running, but the
fresh row proves no recovery claim has occurred. Therefore the evidence
supports: model response completed, delivery confirmation timed out, recovery
was persisted, and no later qualifying service-start/wake execution has
claimed it. It does not prove the exact external reason the later service path
did not run.

## Owner-session liveness and desired intent

The durable owner key is a Discord channel session. SQLite says `active`,
generation `1`, but `updated_at` is four days older than the forensic capture.
The current Gateway and Discord process are live, yet neither establishes that
the session record is genuinely live or that the original owner still wants a
redelivery. The original prompt is a dated daily-focus request, which is
especially unsuitable for assuming current intent after the delivery timeout.

Assessment: **desired now = UNKNOWN / NOT PROVABLE**. Do not silently deliver,
clear, cancel, or replay it in this task.

## Safe disposition options (all unexecuted)

1. **Owner-authorized redelivery:** a new live task must first prove current
   owner intent, genuinely live owner session, matching generation, unchanged
   committed prompt, a pending `redeliver` row, and no active/recovering model
   call fence. It may then authorize exactly one bounded recovery execution and
   separately verify durable delivery. This task did not execute it.
2. **Authoritative cancellation:** if the owner no longer wants the dated
   response, a separately authorized disposition task may cancel the recovery
   through the product's proper cancellation authority, recording the required
   durable audit evidence. Direct SQL `UPDATE`/`DELETE` is not an acceptable
   substitute. This task did not cancel it.
3. **Continue parked:** preserve the row and require explicit operator/owner
   adjudication later. This is the recommended immediate disposition because
   intent and session liveness are unresolved. Installer requalification must
   remain parked.

No option was selected or executed here.

## Exact future `dueDirectRecovery()` gate

At exact candidate source `v091-direct-recovery.ts:50-64`, a row is due only when
all of the following are true:

```text
recovery row exists for the Ticket
r.state = 'pending'
Ticket exists and t.status = 'accepted'
t.workflow_eligible = 0
t.workflow_id IS NULL
owner session joins successfully
s.state = 'active'
s.generation = r.owner_generation
r.next_attempt_at IS NULL OR r.next_attempt_at <= current ISO timestamp
no cnx_direct_model_call row for this Ticket has state 'active' or 'recovering'
```

A safe future installer gate must require the opposite of emittability, proved
read-only immediately before any Gateway-restarting install action. At minimum:

```text
subject pending/redeliver row is absent, OR
row was cancelled by the separately authorized product operation, OR
owner/session/generation predicate is proven false (not merely inferred), OR
an explicitly authorized active/recovering model-call fence is present,
AND no pending direct_result / terminal outbox delivery for this Ticket exists,
AND current owner intent/disposition is recorded by the successor authority.
```

A healthy Gateway, a task registration readback, absence of an installer task,
or a stale process probe alone is insufficient. The future task must also
re-check the complete Ticket/recovery/session/fence/delivery/outbox tuple after
any state transition and before arming the installer.

## Zero-mutation ledger

```text
DB writes/vacuum                         = 0
recovery row clear/cancel/reset          = 0
recovery claim/attempt                   = 0
recovery replay/resend                   = 0
assistant delivery attempt               = 0
installer Scheduled Task registrations   = 0
installer Scheduled Task starts          = 0
scripts/install.ps1 starts               = 0
Gateway restart                          = 0
Dashboard/Discord/API semantic sends     = 0
release/tag mutation                     = 0
force push/history rewrite               = 0
```

The only writes were durable forensic evidence files and this report in a
separate report clone. The report publication is report-only and does not
change product/live state.

## Publication boundary

This report is the only repository path changed for Task257 publication. It is
published from a fresh clean clone of remote branch HEAD
`13887bc9f288cd51bf6bfbc0b2e62646e37ab65e`. After commit/push, the report blob,
raw GitHub bytes/hash, changed paths, local/remote HEAD, and clean worktree
must be re-verified. Then STOP for independent review. Installer
requalification and semantic acceptance remain unauthorized.
