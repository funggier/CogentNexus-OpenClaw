# CNX-20260906-277 — Task273-276 Live Deployment Read-Only Preflight

## Disposition

`PREFLIGHT_COMPLETE__INSTALL_AUTHORITY_REQUIRED__SACRIFICIAL_SESSION_NOT_CLEAN__WAITING_FOR_CHATGPT_REVIEW`

This task performed read-only live discovery only. No install-over, Gateway/provider mutation, semantic send, session Delete/reset, recovery/replay/redelivery, Ticket/SQLite mutation, Scheduled Task mutation, or force-push was performed.

## Authority and accepted candidate

- Task: `CNX-20260906-277`
- Parent: `CNX-20260906-276`
- Accepted source/test/CI candidate: `36cd4c800ded28bdb7165fcad6e0bfb48b4e933b`
- Current coordination remote HEAD at preflight: `869629e` (`docs(review): accept Task276 and open Task277 preflight`)
- Executor: Hermes
- Live deployment authority: **not granted by Task277**

## Installed payload identity

Installed plugin root:

`C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw`

Read-only manifest:

- id: `cogentnexus-openclaw`
- version: `0.9.3`
- runtime extension: `dist/v091-release-entry.js`

Supported artifact helper fingerprint of installed runtime `dist`:

- kind: `directory`
- digest: `f0c15e0fcb58223f40d3c329d40a4e1c9a506c4a905b6fb0780c2e4c6ba2166a`
- fileCount: `192`
- totalBytes: `1073826`

Read-only token search of installed `dist` found no Task273-275 repair markers (`owner-context-mismatch`, ambiguous Discord receipt fence, pending-direct-result timeout guard, or `channelId === webchat` compatibility token). This is supporting evidence only; the exact installed digest is the authoritative identity.

The candidate source has no source-file delta from accepted SHA `36cd4c800ded28bdb7165fcad6e0bfb48b4e933b` to the current coordination tip; the post-candidate changes are coordination docs/review/task files only. A supported local candidate build produced:

- kind: `directory`
- digest: `0891007136c454efc51fe087225055be8a6f9ab9664e76750fbec6699ac1acb9`
- fileCount: `198`
- totalBytes: `1096031`

The installed and candidate runtime fingerprints therefore **do not match**. The candidate requires a separately authorized supported install-over before it can be treated as installed. Task277 does not authorize that action.

The initial attempt to fingerprint the entire installed extension root exceeded the bounded read-only probe window because it includes dependency payloads; it was not used as evidence. The bounded runtime `dist` fingerprint above completed successfully.

## Live runtime health

Fresh live probes:

- `GET http://127.0.0.1:18789/health`: HTTP `200`, `{"ok":true,"status":"live"}`
- Gateway listen: `127.0.0.1:18789`
- Gateway process: `node.exe` PID `24992`
- Gateway status: reachable; OpenClaw runtime `2026.7.1-2`
- Gateway service: installed/loaded/managed by OpenClaw; Scheduled Task state `Ready`, last result `0`
- Ollama: HTTP `200` at `127.0.0.1:11434/api/tags`
- Available configured model: `qwen3.5:9b`, digest `6488c96fa5faab64bb65cbd30d4289e20e6130ef535a93ef9a49f42eda893ea7`
- Host health snapshot: `healthy`, but timestamp `2026-09-06T04:06:23.539638+00:00` is older than the fresh probes and is reported as a stale snapshot, not fresh proof
- Supervisor task: `\\CogentNexus-OpenClaw-Supervisor`, `Ready`, `Enabled`, last result `0`

OpenClaw status also reports `gateway.reachable=true` with connect latency `170ms`, but `operator.read` scope is missing. This is an observability-scope limitation, not evidence of Gateway failure.

The supervisor task listing also contains historical Task237/241/243/244/245/248/251 entries with old nonzero results. They were not changed or rerun; they are historical scheduler residue and separate from the current supervisor's last result `0`.

## Durable state (read-only)

SQLite path:

`C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw\runtime\cogentnexus-openclaw.sqlite3`

- SQLite `pragma integrity_check`: `ok`
- Ticket counts: `accepted=2`, `cancelled=2`, `completed=11`
- Pending `ticket_outbox`: `0`
- `cnx_assistant_delivery`: `delivered=8`, no pending assistant-delivery rows in the aggregate
- `cnx_direct_recovery`: `pending=2`, `cancelled=1`
- `cnx_sessions`: `21`

### Protected old Ticket

Protected old Ticket remains present and untouched:

- Ticket: `CNXT-dc11c9a0-8a89-4df5-9c48-345260725be4`
- owner session: `agent:main:discord:channel:1531199905673252946`
- status: `accepted`
- failure class: `interrupted`
- failure message: `Direct response delivery was not confirmed before deadline`
- `delivery_confirmed_at`: `null`

The owner session row remains active with generation `1` and `session_id=null`. It is excluded from any future disposable-session operation.

### Task272 sacrificial setup session

- session key: `agent:main:discord:channel:1366635842554036314`
- session ID: `68ad6250-1d3a-4dac-a1b1-f1da84a10cda`
- generation: `0`
- session state: `active`

Relevant durable Ticket rows on this session include:

- a completed Ticket with `delivery_confirmed_at` `2026-09-06T04:29:19.540Z`;
- a later Ticket still `accepted`, `failure_class=interrupted`, failure message `Direct response delivery was not confirmed before deadline`, and `delivery_confirmed_at=null`.

The setup session is therefore **not clean**. Its visible Discord response history does not override the unconfirmed durable Ticket state. No cleanup, replay, redelivery, cancellation, Delete, or reset was attempted.

## Decision and next action

The live host is reachable and the accepted candidate is source/test/CI-verified, but the installed runtime is not the accepted candidate and the sacrificial Task272 session remains non-clean. The exact next live action, if ChatGPT and the human later authorize deployment, is:

1. issue a new successor task explicitly authorizing one supported install-over of candidate `36cd4c800ded28bdb7165fcad6e0bfb48b4e933b`;
2. bind the installer to the exact candidate checkout/artifact and perform the task's installer-owned managed Gateway transition only;
3. re-read installed fingerprint and post-install health;
4. separately obtain explicit authority for any sacrificial-session Delete/recreation acceptance, keeping the protected old-Ticket owner excluded.

Task272's parked Delete/test-message authority does not imply install authority and remains unconsumed.

## Hard-fence ledger

- live Discord/Dashboard semantic sends: `0`
- live OpenClaw session Delete/reset: `0`
- manual live Ticket/session/SQLite mutation: `0`
- recovery replay/redelivery/disposition: `0`
- installer/install-over/uninstall/reset: `0`
- Gateway/provider/service lifecycle mutation: `0`
- Scheduled Task mutation: `0`
- release/tag/default-branch promotion: `0`
- force push/history rewrite: `0`

## Handoff

Set `ACTIVE.md` and `STATUS.md` to `WAITING_FOR_CHATGPT_REVIEW` and stop. No live action is authorized by this report.
