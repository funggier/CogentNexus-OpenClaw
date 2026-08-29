# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `LIVE_WINDOWS_PRODUCT_RESET_FRESH_STATE_ACCEPTANCE`
Current authorization: `CNX-20260830-148_PRODUCT_RESET_FRESH_STATE_ACCEPTANCE`
Task ID: `CNX-20260830-148`
Updated: 2026-08-30 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

GitHub remote branch `agent/v0.9.3-full-stabilization` is authoritative. A stale local checkout must not be used as coordination truth.

## Active task

[`tasks/CNX-20260830-148-product-reset-fresh-state-acceptance.md`](tasks/CNX-20260830-148-product-reset-fresh-state-acceptance.md)

Task 148 is the real-Windows acceptance of the installed operator-facing `cnxclaw.cmd reset` command. It must prove CNX state is recreated as fresh-install MANAGED while installed program/skill/plugin accepted provenance remains installed and exact.

## Task-147 disposition

Task-147 report:

`docs/operations/coordination/reports/CNX-20260830-147-redirected-stdin-product-uninstall-and-fresh-reinstall-retry.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260830-147-redirected-stdin-product-uninstall-and-fresh-reinstall-retry-review.md`

Review disposition: **ACCEPT**.

Task 147 proved the real operator-facing lifecycle:

- qualified non-PTY confirmation harness;
- one `cnxclaw.cmd uninstall` + one `y`, exit `0`;
- product-owned cleanup reached CNX-absent/native-OpenClaw healthy state;
- one normal fresh install from exact accepted SHA, exit `0`;
- new canonical MANAGED installation with fresh zero-row durable DB;
- Dashboard semantic Sends `0`.

Accepted production implementation remains:

`fb5781c1abd68280760bd5b3b4a65fabd8a60e58`

## Task-148 execution contract

Before reset, re-prove live state read-only and capture durable DB/controller creation-time/file-identity evidence plus installed program/plugin hashes.

Qualify redirected stdin again with a harmless `input()` child. Only then invoke installed `cnxclaw.cmd reset` exactly once with exactly one lowercase `y` line.

If reset fails, stop with no retry or repair.

If reset succeeds, prove:

- CNX state/durable DB was recreated using changed file identity and/or creation-time evidence;
- launcher, skill and canonical plugin remain installed;
- plugin fingerprint/helper hash remain exact accepted candidate;
- ownership verify passes;
- controller is fresh MANAGED with Ollama selected/running;
- Gateway/Ollama/recovery/delivery/SQLite healthy, pending `0`;
- semantic counts `0`;
- no install/uninstall occurred;
- Dashboard semantic Sends `0`.

## Required completion signal

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260830-148-product-reset-fresh-state-acceptance.md`

Then stop for independent ChatGPT review.

## Hard fence

No Dashboard semantic Send/resend; no Ticket/workflow/outbox/delivery/recovery semantic mutation; no uninstall/install/reinstall; no manual state deletion; no manual plugin/controller/ownership normalization; no reset retry; no crash/recovery injection; no unrelated process/service/task mutation; no reboot; no credentials/secrets; no merge/tag/release; no force push.
