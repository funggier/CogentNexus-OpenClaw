# Coordination Channel Status

**State:** `READY_FOR_HERMES`  
**Execution mode:** `LIVE_WINDOWS_REDIRECTED_STDIN_UNINSTALL_AND_FRESH_REINSTALL_ACCEPTANCE`  
**Updated:** 2026-08-30 ICT  
**Transport:** GitHub repository history  
**Human authority:** operator requested continuation; Task 146 controlled failure was executor stdin/PTY plumbing before any destructive mutation, so one new harness-qualified lifecycle attempt is authorized  
**Execution trigger:** manual Hermes/Codex continuation; scheduled execution remains disabled

## Active work

Task:

[`tasks/CNX-20260830-147-redirected-stdin-product-uninstall-and-fresh-reinstall-retry.md`](tasks/CNX-20260830-147-redirected-stdin-product-uninstall-and-fresh-reinstall-retry.md)

Task ID:

`CNX-20260830-147`

## Task-146 accepted evidence

Report:

`docs/operations/coordination/reports/CNX-20260830-146-product-uninstall-and-clean-fresh-reinstall-acceptance.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260830-146-product-uninstall-and-clean-fresh-reinstall-acceptance-review.md`

Disposition: **ACCEPT** as controlled evidence; lifecycle objective remains unproven.

Task 146 established:

- safe coherent preflight;
- real installed launcher reached the real confirmation prompt;
- executor did not deliver stdin and the process failed at Python `input()` with bad file descriptor;
- uninstall mutation did not begin;
- no `y`, retry, cleanup or fresh install occurred;
- post-state remained coherent MANAGED with exact accepted candidate, healthy Gateway/Ollama/recovery/delivery/SQLite and Dashboard Sends `0`.

This is classified as an executor harness failure, not a demonstrated product uninstall defect. No source repair is authorized from Task-146 evidence.

## Task-147 authority

Before product mutation, Hermes/Codex must qualify deterministic redirected-stdin process plumbing on a harmless `input()` child using the same mechanism intended for uninstall. Qualification must prove exactly one `y` line was delivered and exit/stdout/stderr are preserved.

Only a qualified harness may invoke the installed `cnxclaw.cmd uninstall` exactly once. If uninstall succeeds, product-owned cleanup must reach clean native state without manual deletion before one fresh accepted-candidate install is allowed.

Accepted production implementation SHA remains:

`fb5781c1abd68280760bd5b3b4a65fabd8a60e58`

## Semantic fence

Task 147 authorizes **zero Dashboard semantic Sends** and no manual Ticket/workflow/outbox/delivery/recovery/database mutation.

## Prohibited

No reset; no Dashboard Send/resend; no crash/recovery injection; no manual plugin lifecycle; no manual CNX live-file deletion; no clean-reinstall helper; no second uninstall attempt; no fresh-install retry; no manual controller/ownership normalization; no unrelated process/service/task mutation; no reboot; no credentials/secrets; no merge/tag/GitHub Release; no force push.

## Required output

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260830-147-redirected-stdin-product-uninstall-and-fresh-reinstall-retry.md`

Then stop for independent ChatGPT review.
