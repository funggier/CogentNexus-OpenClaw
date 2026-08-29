# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `LIVE_WINDOWS_PRODUCT_UNINSTALL_AND_CLEAN_FRESH_REINSTALL_ACCEPTANCE`
Current authorization: `CNX-20260830-146_PRODUCT_UNINSTALL_AND_CLEAN_FRESH_REINSTALL_ACCEPTANCE`
Task ID: `CNX-20260830-146`
Updated: 2026-08-30 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

GitHub remote branch `agent/v0.9.3-full-stabilization` is authoritative. A stale local checkout must not be used as coordination truth.

## Active task

[`tasks/CNX-20260830-146-product-uninstall-and-clean-fresh-reinstall-acceptance.md`](tasks/CNX-20260830-146-product-uninstall-and-clean-fresh-reinstall-acceptance.md)

Task 146 is the controlled real-Windows acceptance of the actual operator-facing `cnxclaw.cmd uninstall` command followed, only after proven clean native state, by one normal fresh install from the exact accepted pre-release candidate.

## Task-145 disposition

Task-145 report:

`docs/operations/coordination/reports/CNX-20260830-145-accepted-candidate-partial-install-reentry-and-health-proof.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260830-145-accepted-candidate-partial-install-reentry-and-health-proof-review.md`

Review disposition: **ACCEPT**.

Accepted implementation/deployment source:

`fb5781c1abd68280760bd5b3b4a65fabd8a60e58`

Task 145 proved one supported installer re-entry from the preserved partial state completed successfully with exact candidate provenance, refreshed ownership, MANAGED runtime health, preserved durable history, pending `0`, and zero Dashboard semantic Sends.

## Preserved live-state boundary

Task 145 last observed:

- controller `managed`;
- one canonical direct plugin, enabled and loaded;
- plugin fingerprint `12c6d1b5b6ffd938353dd60c5d6190c34a609663369f619ff4fc7cbd176119e0`;
- installed ownership-helper hash `10dda985e6d4553a73a8cdd3ef7f660937482c3ef0c2d2da8d15bcbfe8d39b66`;
- ownership verify PASS with refreshed manifest;
- Gateway/OpenClaw/Ollama healthy;
- recovery/delivery READY, pending `0`;
- SQLite `ok`;
- semantic counts unchanged from the pre-reentry boundary;
- Dashboard semantic Send count `0`.

Task 146 must re-verify this read-only. It is not permission to normalize drift.

## Task-146 execution contract

1. Use fresh GitHub authority and a fresh detached exact accepted source `fb5781c1...`.
2. Capture safe read-only pre-uninstall ownership/runtime/provider/database state and external test evidence.
3. Execute the installed `cnxclaw.cmd uninstall` exactly once and feed exactly one explicit `y` confirmation.
4. On any uninstall failure: stop, no reinstall/retry/manual cleanup.
5. After exit `0`, wait only for product-owned Windows deferred cleanup and prove CNX is absent while native OpenClaw remains healthy and Ollama/provider installation is unchanged.
6. Only after that clean/native proof, execute exactly one normal `scripts/install.ps1` from exact accepted source.
7. On fresh-install failure: stop, no retry/manual repair.
8. On success, prove exact candidate provenance, new ownership, canonical singular plugin, MANAGED health, fresh durable database, pending `0`, and Dashboard Sends `0`.

Do not use `scripts/clean-reinstall.ps1`; this task intentionally tests the public lifecycle command itself.

## Required completion signal

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260830-146-product-uninstall-and-clean-fresh-reinstall-acceptance.md`

Then stop for independent ChatGPT review.

## Hard fence

No Dashboard semantic Send/resend; no reset; no manual Ticket/workflow/outbox/delivery/recovery/database mutation; no crash/recovery injection; no manual plugin lifecycle or CNX live-file cleanup; no manual controller/ownership normalization; no clean-reinstall helper; no retry after failure; no alternate installer; no unrelated process/service/task mutation; no reboot; no credentials/secrets; no merge/tag/release; no force push.
