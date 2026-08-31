# CNX-20260830-149 — Proven-Launcher Product Reset Fresh-State Retry

Status: `READY_FOR_HERMES`
Execution mode: `LIVE_WINDOWS_PROVEN_LAUNCHER_RESET_FRESH_STATE_ACCEPTANCE`
Owner: ChatGPT
Executor: Hermes/Codex on the operator's real Windows machine

## Purpose

Retry the real installed `cnxclaw.cmd reset` acceptance after Task 148 proved only an executor quoting failure. This task must use the launcher invocation shape already proven by Task 147 and must not change production source.

Accepted production SHA:

`fb5781c1abd68280760bd5b3b4a65fabd8a60e58`

## Starting boundary

Task 148 post-failure proof showed no reset mutation began. Re-verify read-only before mutation:

- launcher/skill/plugin present and accepted provenance exact;
- ownership verify PASS;
- controller MANAGED with Ollama selected/running;
- Gateway/Ollama/recovery/delivery healthy, pending `0`;
- SQLite `integrity_check=ok`, semantic counts all zero;
- Dashboard semantic Sends `0`.

Capture controller and SQLite creation time, last-write time, SHA-256, size, and Windows file ID before reset. Capture launcher/plugin/helper hashes.

## Harness qualification

Qualify redirected stdin on a harmless Python child using the same `subprocess.Popen` pipe mechanism. Exactly one lowercase `y` line must be received, stdout/stderr captured, exit `0`.

If qualification fails: `BLOCKED_HARNESS`; do not invoke reset.

## Exact product invocation

Invoke the installed launcher exactly once using the Task-147-proven command shape:

```text
cmd.exe /d /c C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd reset
```

Requirements:

- no `/s`;
- no `call`;
- no manually embedded/escaped quote wrapper around the batch path;
- reset invocation count exactly `1`;
- write exactly one lowercase `y` line then close stdin;
- preserve actual stdout/stderr and exit code.

The command must visibly reach `Continue? [y/N]:` and accept the confirmation. If command resolution fails or reset exits nonzero, stop immediately; no retry, reinstall, repair, manual deletion, or normalization.

## PASS proof

After reset exit `0`, prove read-only that:

1. state root was recreated by the product;
2. controller and durable SQLite database are new reset-generation files, demonstrated by changed Windows file ID and/or creation-time evidence versus pre-reset values;
3. semantic counts remain fresh (`0` for tickets/events/model-call/recovery/delivery/outbox/sessions);
4. launcher, skill and canonical plugin remain installed;
5. plugin fingerprint and installed `namespace_ownership.py` hash remain exact accepted provenance;
6. ownership verify passes;
7. controller is fresh `MANAGED` with Ollama selected/running;
8. Gateway/OpenClaw/Ollama are healthy;
9. recovery and delivery are `READY`, read-only, pending `0`;
10. SQLite integrity is `ok`;
11. no uninstall/install/reinstall occurred;
12. Dashboard semantic Sends remain `0`.

Do not require program/plugin files to be recreated; reset is state recreation while installed release payload remains installed.

## Required report

Publish exactly:

`docs/operations/coordination/reports/CNX-20260830-149-proven-launcher-product-reset-fresh-state-retry.md`

Verdict exactly one of `PASS`, `FAIL_RESET`, `BLOCKED_HARNESS`, `BLOCKED`.

Then stop for independent ChatGPT review.

## Hard fence

No Dashboard semantic Send/resend; no Ticket/workflow/outbox/delivery/recovery manual mutation; no uninstall/install/reinstall; no manual state deletion; no manual plugin/controller/ownership normalization; no second reset; no crash/recovery injection; no unrelated process/service/task mutation; no reboot; no credentials/secrets; no merge/tag/release; no force push.
