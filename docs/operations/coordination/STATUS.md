# Coordination Channel Status

**State:** `READY_FOR_HERMES`  
**Execution mode:** `LIVE_WINDOWS_RECOVERY_ACCEPTANCE_ONLY`  
**Updated:** 2026-08-29 ICT  
**Transport:** GitHub repository history  
**Human authority:** operator authorized continued stabilization; Task 131 grants one new exact repaired-harness real-Windows recovery-suite execution only  
**Execution trigger:** manual Hermes/Codex continuation; scheduled execution remains disabled

## Active work

Task:

[`tasks/CNX-20260829-131-v093-real-windows-recovery-reacceptance-authoritative-root.md`](tasks/CNX-20260829-131-v093-real-windows-recovery-reacceptance-authoritative-root.md)

Task ID:

`CNX-20260829-131`

## Task 129/130 accepted forensic closure

Task-130 report:

`docs/operations/coordination/reports/CNX-20260829-130-task129-readonly-evidence-publication-closeout.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260829-130-task129-readonly-evidence-publication-closeout-review.md`

Accepted result:

- Task 128's `passthrough` / null-provider / missing-SQLite preflight was a false blocker caused by using `--root C:\Users\CDQ-P\.openclaw\workspace`;
- installed launcher authority is `C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd`;
- that launcher explicitly uses `C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw` as state root;
- direct installed-launcher probes show `managed`, provider `ollama`, recovery `READY`;
- authoritative SQLite exists below that root and read-only `PRAGMA integrity_check` is `ok`;
- Supervisor task independently references the same installed state root;
- no authoritative managed-state drift was accepted.

Classification:

`LAUNCHER_OR_ROOT_MISMATCH` + `SQLITE_PATH_OR_STATUS_PROBE_DEFECT` limited to Task-128 preflight.

## Accepted candidate

Task-127 candidate remains:

`1b922bf400fdbccb1f9c7019b89b69fd67f44070`

Exact repaired recovery harness:

- `scripts/test-v093-ollama-recovery-windows-v3.ps1`;
- Git blob `622f70b339fea0f2ef7c564253aa3c6bf90ffc97`.

Package proof:

- artifact `9706878201`;
- digest `sha256:c5dcbda0858a08362daa3218c2912ddd4a36c259e61a05be28d7b1d4114b104c`;
- payload count `178`;
- fingerprint `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`.

## Task 131 corrected preflight requirement

Before any disruption, all authoritative CNX preflight commands must be invoked through the explicit installed launcher path. The executor must freshly parse that launcher's owned Python, installed CLI, explicit `.cogentnexus-openclaw` root, and `%*` forwarding.

The workspace parent must never be substituted as controller root.

Require a fresh already-safe baseline: managed/Ollama/recovery `READY`, ownership/fingerprint exact, OpenClaw exact, one current plugin, Gateway/Ollama healthy, and authoritative SQLite read-only integrity exactly `ok`. If unsafe, stop BLOCKED without lifecycle repair or normalization.

If safe, run exactly one repaired-harness suite in a true interactive PowerShell PTY:

`-Scenario all -RunDisruptive`

Enter exactly one lowercase `y` only after `Type y to continue:` appears. No suite/scenario rerun is permitted once launched.

## Ledger

Historical operations remain consumed. Task 128 closed with suite `0 / 1 launched`.

Task 131 creates a new one-shot ledger:

- repaired-harness suite: maximum `1 / 1`;
- confirmation: maximum one lowercase `y` after prompt;
- baseline/gateway-crash/provider-crash/operator-stop only inside the exact harness.

## Prohibited

No install/install-over/reset/uninstall/reinstall, no standalone lifecycle outside the exact harness, no source/harness edits, no alternate confirmation, no provider/OpenClaw/model/config mutation, no manual cleanup/normalization, no reboot, no generic process-tree kill, no credentials/secrets, no Dashboard semantic Send, no merge/tag/release, and no force push.

## Required output

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260829-131-v093-real-windows-recovery-reacceptance-authoritative-root.md`

Then stop for independent ChatGPT review. Dashboard durable-delivery acceptance remains unopened and prohibited.
