# CNX-20260906-279 — Managed Re-entry After Partial Install

## Disposition

`PASS_MANAGED_REENTRY_EXACT_PAYLOAD_PRESERVED__WAITING_FOR_CHATGPT_REVIEW`

Task279 used the smallest supported recovery action. The exact-candidate reinstall fallback was not used. The one supported `cnxclaw.cmd enable` attempt completed with exit code `0`; no retry was performed.

## Authority and candidate

- Task: `CNX-20260906-279`
- Parent: `CNX-20260906-278`
- Executor: Hermes
- Accepted candidate: `36cd4c800ded28bdb7165fcad6e0bfb48b4e933b`
- Human-authorized scope: one managed re-entry; reinstall only if proven necessary
- Reinstall fallback: **not consumed**

## Pre-action proof

Immediately before the action:

- installed plugin fingerprint matched candidate: `79e9c2a32bea5eaade3a7b30efaeb2584b1e3a3972a4a8a93e8425ffc27160cc`
- installed ownership `verify` passed against canonical plugin/skill/launcher
- plugin was disabled and Host controller was `passthrough`
- Gateway health endpoint returned HTTP `200`, `{"ok":true,"status":"live"}`
- Ollama endpoint returned HTTP `200`
- SQLite `pragma integrity_check`: `ok`
- Ticket counts were `accepted=2`, `cancelled=2`, `completed=11`
- pending outbox was `0`; direct recovery was `pending=2`, `cancelled=1`
- protected old Ticket remained `accepted/interrupted` with `delivery_confirmed_at=null`
- Task272 sacrificial lineage remained active/non-clean and was not selected for mutation

## Supported action

Exact command, invoked once:

`C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd enable`

Transcript:

`C:\Users\CDQ-P\AppData\Local\Temp\cnx-task279-enable-transcript.txt`

Terminal result:

`ENABLE_EXIT_CODE=0`

The command reported:

- `result=ok`, `action=enable`, provider `ollama`
- Host `mode=managed`
- authority commit `mode=managed`, generation `58`, `linearizedBeforePluginReload=true`
- policy changed and enabled
- supervisor adapter installed, `State=Ready`, `Enabled=true`, `LastTaskResult=0`
- Gateway reload requested and completed with `ok=true`, `exitCode=0`
- Ollama lifecycle `ok=true`, `skipped=true`, reason `already healthy`
- route `committed=true`, model `ollama/qwen3.5:9b`
- no recovered Tickets and no post-commit recovery error
- transactional result `true`

The later readback controller generation was `61`, reflecting supported managed lifecycle/supervisor progression; no semantic Ticket action was performed.

## Post-action verification

Fresh read-only checks after enable:

- Installed fingerprint: `79e9c2a32bea5eaade3a7b30efaeb2584b1e3a3972a4a8a93e8425ffc27160cc`
- Candidate/installed fingerprint: **exact match**
- Ownership verification: **PASS**
- Plugin inventory: version `0.9.3`, `enabled=true`, `status=loaded`
- Canonical plugin root: `C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw`
- Host controller: `mode=managed`, `desiredGateway=running`, `desiredProvider=running`, generation `61`
- Gateway: HTTP `200`, `{"ok":true,"status":"live"}`
- Ollama: HTTP `200`, configured model `qwen3.5:9b` present
- Supervisor: `\\CogentNexus-OpenClaw-Supervisor`, `Ready`, last result `0`
- SQLite integrity: `ok`
- Ticket counts unchanged: `accepted=2`, `cancelled=2`, `completed=11`
- pending outbox: `0`
- direct recovery unchanged: `pending=2`, `cancelled=1`

## Durable-state preservation

Protected old Ticket remained unchanged:

- Ticket: `CNXT-dc11c9a0-8a89-4df5-9c48-345260725be4`
- status: `accepted`
- failure class: `interrupted`
- failure message: `Direct response delivery was not confirmed before deadline`
- `delivery_confirmed_at=null`

Task272 sacrificial session remained untouched:

- session key: `agent:main:discord:channel:1366635842554036314`
- session ID: `68ad6250-1d3a-4dac-a1b1-f1da84a10cda`
- generation: `0`
- state: `active`
- setup-related Ticket remained `accepted/interrupted` with no durable delivery confirmation
- no Delete/reset/cancellation/replay/redelivery/manual disposition occurred

The protected old owner session remained active and excluded from any deletion operation.

## Hard-fence ledger

- supported `cnxclaw.cmd enable`: `1`
- fallback reinstall/install-over: `0`
- semantic Discord/Dashboard sends: `0`
- OpenClaw session Delete/reset: `0`
- manual Ticket/SQLite/session mutation: `0`
- recovery/replay/redelivery/disposition: `0`
- ad-hoc process kill: `0`
- Scheduled Task mutation outside the supported managed command: `0`
- release/tag/default-branch promotion: `0`
- force push/history rewrite: `0`

## Boundary

Task279 is complete and handed to ChatGPT review. Task272 Delete/recreation acceptance remains a separate later authority and was not resumed. Conditional final release direction is not consumed by Task279; release requires a later bounded task after independent final acceptance.
