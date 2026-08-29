# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `LIVE_WINDOWS_PROVEN_LAUNCHER_RESET_FRESH_STATE_ACCEPTANCE`
Current authorization: `CNX-20260830-149_PROVEN_LAUNCHER_PRODUCT_RESET_FRESH_STATE_RETRY`
Task ID: `CNX-20260830-149`
Updated: 2026-08-30 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

GitHub remote branch `agent/v0.9.3-full-stabilization` is authoritative. A stale local checkout must not be used as coordination truth.

## Active task

[`tasks/CNX-20260830-149-proven-launcher-product-reset-fresh-state-retry.md`](tasks/CNX-20260830-149-proven-launcher-product-reset-fresh-state-retry.md)

Task 149 retries reset acceptance using the exact launcher command form already proven by Task 147. No production source repair is authorized from Task 148.

## Task-148 disposition

Task-148 report:

`docs/operations/coordination/reports/CNX-20260830-148-product-reset-fresh-state-acceptance.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260830-148-product-reset-fresh-state-acceptance-review.md`

Review disposition: **ACCEPT** as controlled evidence; reset lifecycle remains unproven.

Task 148 never reached the product launcher because executor `cmd.exe` quoting was malformed. Post-failure file IDs, timestamps, hashes, state generation, runtime health and semantic counts were unchanged, proving reset mutation did not begin.

Accepted production implementation remains:

`fb5781c1abd68280760bd5b3b4a65fabd8a60e58`

## Task-149 execution contract

Recheck live state read-only, qualify redirected stdin harmlessly, then use exactly:

`cmd.exe /d /c C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd reset`

No `/s`, no `call`, no manual embedded quote escaping. Invoke reset once, send one lowercase `y`, and stop on first failure.

PASS must prove product-owned state/DB recreation by changed file identity/creation evidence while launcher/skill/plugin accepted provenance remains installed and exact, with fresh MANAGED Ollama operation, healthy Gateway/recovery/delivery/SQLite, pending `0`, semantic counts `0`, and Dashboard Sends `0`.

## Required completion signal

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260830-149-proven-launcher-product-reset-fresh-state-retry.md`

Then stop for independent ChatGPT review.

## Hard fence

No Dashboard semantic Send/resend; no uninstall/install/reinstall; no manual semantic/database mutation; no manual state deletion; no manual plugin/controller/ownership normalization; no second reset; no crash/recovery injection; no unrelated process/service/task mutation; no reboot; no credentials/secrets; no merge/tag/release; no force push.
