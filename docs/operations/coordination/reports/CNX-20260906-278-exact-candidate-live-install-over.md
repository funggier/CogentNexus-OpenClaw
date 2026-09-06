# CNX-20260906-278 — Exact Candidate Live Install-Over

## Disposition

`BLOCKED_EVIDENCE__INSTALLER_TERMINAL_UNPROVEN__PARTIAL_INSTALL_STATE__WAITING_FOR_CHATGPT_REVIEW`

Task278 authorized exactly one supported install-over of the exact candidate. That one installer invocation was consumed. The terminal tool timed out at approximately 420 seconds before the installer emitted a final exit code or completion line. Per the safety contract, the installer was not retried, no process was killed, and no manual repair or lifecycle command was run.

## Candidate binding

- Candidate SHA: `36cd4c800ded28bdb7165fcad6e0bfb48b4e933b`
- Exact detached checkout: `C:\Users\CDQ-P\AppData\Local\Temp\cnx-task278-candidate-36cd4c8`
- Checkout HEAD: exact candidate SHA
- Checkout worktree: clean before execution
- Installer: `C:\Users\CDQ-P\AppData\Local\Temp\cnx-task278-candidate-36cd4c8\scripts\install.ps1`
- Candidate plugin fingerprint from repository helper: `79e9c2a32bea5eaade3a7b30efaeb2584b1e3a3972a4a8a93e8425ffc27160cc`
- Candidate validation: `npm ci`, `npm run plugin:validate`, package contents verification all passed; packed file count `202`
- Recovery preflight: `OWNERSHIP_PRESENT`
- Lifecycle resolver: `mode=upgrade`, `installPlugin=true`, `rolloverPlugin=true`

## One-shot installer evidence

Transcript: `C:\Users\CDQ-P\AppData\Local\Temp\cnx-task278-installer-transcript.txt`

Completed stages, each with installer-reported `exit_code=0`:

- `ticket-db-bootstrap`: `94ms`
- `plugin-npm-pack`: `533ms`
- `plugin-rollover-prepare`: `214157ms`
- `plugin-install-local-package`: `38843ms`
- `plugin-disable-post-install`: `5638ms`
- `plugin-rollover-finalize`: `3247ms`
- `owned-runtime-ensure`: `141ms`

The transcript ends after `owned-runtime-ensure` and the launcher write. It contains no later `CNXCLAW_INSTALL_STAGE_COMPLETE`, no `CogentNexus-OpenClaw v0.9.3 installation completed successfully`, and no reliable installer process exit code. No Task278 `runner-result.json` or equivalent complete terminal artifact was found. The timeout is therefore an evidence blocker, not a successful installer result.

The installer did perform supported installer-owned mutations before the evidence boundary: plugin rollover/install, plugin disable, runtime ownership preparation, and launcher/ownership state writes. These are recorded as observed partial state; they were not manually repeated or repaired.

## Installed payload and runtime readback

Fresh readback after the timeout:

- Installed root: `C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw`
- Installed version: `0.9.3`
- Installed fingerprint via repository helper: `79e9c2a32bea5eaade3a7b30efaeb2584b1e3a3972a4a8a93e8425ffc27160cc`
- Candidate/installed fingerprint: **exact match**
- Raw OpenClaw plugin inventory: plugin present, `enabled=false`, `status=disabled`, source `dist/v091-release-entry.js`
- Host controller: `mode=passthrough`, `desiredGateway=running`, `desiredProvider=unchanged`, generation `57`
- Host controller update: `2026-09-06T12:59:22.533169+00:00`
- Ownership manifest installedAt: `2026-09-06T12:59:20.537180+00:00`
- Install transaction readback: existing transaction state `committed`; this is not treated as proof of this one-shot's terminal success

Because the installer did not reach a proven terminal result and the plugin remains disabled/passthrough, managed activation is **not proven** and is not claimed.

## Gateway/provider/host health

Fresh read-only probes:

- `GET http://127.0.0.1:18789/health`: HTTP `200`, `{"ok":true,"status":"live"}`
- Gateway listener: `127.0.0.1:18789`
- Ollama listener: `127.0.0.1:11434`
- Ollama `/api/tags`: HTTP `200`; configured model `qwen3.5:9b` present
- Gateway process was observed listening after the installer-owned transition
- Exact `\\CogentNexus-OpenClaw-Supervisor` task lookup returned no matching current task entry in the readback; historical similarly named tasks remain and were not changed
- Persisted health JSON says `healthy`, but its timestamp `2026-09-06T04:06:23.539638+00:00` is stale relative to the fresh HTTP probes and is treated as historical support only
- OpenClaw status had `gateway.reachable=true` but lacked `operator.read` scope; this is an observability limitation, not proof of failure or success

## Durable-state preservation (read-only)

SQLite opened with `mode=ro`:

- `pragma integrity_check`: `ok`
- Ticket counts: `accepted=2`, `cancelled=2`, `completed=11`
- Pending outbox: `0`
- Direct recovery: `pending=2`, `cancelled=1`

Protected old Ticket remained unchanged:

- `CNXT-dc11c9a0-8a89-4df5-9c48-345260725be4`
- status `accepted`
- failure class `interrupted`
- `delivery_confirmed_at=null`

Task272 sacrificial lineage remained non-clean and was not disposed:

- setup-related accepted/interrupted Ticket still has no durable delivery confirmation
- completed Ticket in the same session remains completed with its prior confirmation
- no Delete, reset, cancellation, replay, redelivery, or manual disposition was performed

## Hard-fence ledger

- supported installer/install-over: `1` (this Task278 one-shot; terminal evidence incomplete)
- live semantic Discord/Dashboard sends: `0`
- OpenClaw session Delete/reset: `0`
- manual Ticket/SQLite/session mutation: `0`
- recovery/replay/redelivery/disposition: `0`
- ad-hoc process kill: `0`
- Scheduled Task mutation outside installer: `0`
- release/tag/default-branch promotion: `0`
- force push/history rewrite: `0`

## Required review decision

Do not retry the installer or invoke `enable`, Gateway restart, session Delete/reset, recovery, redelivery, or semantic send from this report. ChatGPT review must adjudicate the partial install state and missing terminal evidence. Any further live action requires a separately named successor authority; Task272's parked Delete/test-message authority remains separate and unconsumed.
