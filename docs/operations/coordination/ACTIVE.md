# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `LIVE_WINDOWS_REDIRECTED_STDIN_UNINSTALL_AND_FRESH_REINSTALL_ACCEPTANCE`
Current authorization: `CNX-20260830-147_REDIRECTED_STDIN_PRODUCT_UNINSTALL_AND_FRESH_REINSTALL_RETRY`
Task ID: `CNX-20260830-147`
Updated: 2026-08-30 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

GitHub remote branch `agent/v0.9.3-full-stabilization` is authoritative. A stale local checkout must not be used as coordination truth.

## Active task

[`tasks/CNX-20260830-147-redirected-stdin-product-uninstall-and-fresh-reinstall-retry.md`](tasks/CNX-20260830-147-redirected-stdin-product-uninstall-and-fresh-reinstall-retry.md)

Task 147 retries the Task-146 lifecycle acceptance only after qualifying a deterministic non-PTY redirected-stdin harness with a harmless child process.

## Task-146 disposition

Task-146 report:

`docs/operations/coordination/reports/CNX-20260830-146-product-uninstall-and-clean-fresh-reinstall-acceptance.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260830-146-product-uninstall-and-clean-fresh-reinstall-acceptance-review.md`

Review disposition: **ACCEPT** as controlled execution evidence, **not** as lifecycle PASS.

Task 146 reached the real uninstall prompt but executor PTY/stdin plumbing failed with `OSError: [Errno 9] Bad file descriptor` before any `y` was delivered. Post-failure read-only proof shows no destructive mutation began and the accepted candidate remains coherent MANAGED.

No product/source defect is established by that harness failure.

Accepted implementation/deployment source remains:

`fb5781c1abd68280760bd5b3b4a65fabd8a60e58`

## Task-147 execution contract

1. Fresh remote authority and read-only live-state recheck.
2. Qualify the exact redirected-stdin child-process plumbing using a harmless Python `input()` child; it must receive exactly `y`, capture output/error and exit `0`.
3. If harness qualification fails: stop `BLOCKED_HARNESS`; do not invoke uninstall.
4. If qualified: invoke installed `cnxclaw.cmd uninstall` exactly once, write exactly one `y` line, close stdin and capture real exit/output.
5. On uninstall failure: stop, no retry/cleanup/fresh install.
6. On exit `0`: wait only for product-owned deferred cleanup and prove clean CNX-absent/native-OpenClaw/Ollama-healthy state.
7. Only then perform exactly one normal fresh `scripts/install.ps1` from exact accepted source.
8. On fresh-install failure: stop, no retry/manual repair.
9. On success: prove exact candidate provenance, new ownership, singular canonical plugin, MANAGED runtime health, genuinely fresh durable database, pending `0`, Dashboard Sends `0`.

## Required completion signal

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260830-147-redirected-stdin-product-uninstall-and-fresh-reinstall-retry.md`

Then stop for independent ChatGPT review.

## Hard fence

No Dashboard semantic Send/resend; no reset; no crash/recovery injection; no manual semantic/database mutation; no manual plugin lifecycle or CNX live-file cleanup; no clean-reinstall helper; no second uninstall; no fresh-install retry; no manual controller/ownership normalization; no unrelated process/service/task mutation; no reboot; no credentials/secrets; no merge/tag/release; no force push.
