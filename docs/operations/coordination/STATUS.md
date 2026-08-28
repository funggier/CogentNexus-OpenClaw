# Coordination Channel Status

**State:** `READY_FOR_HERMES`  
**Execution mode:** `SOURCE_ONLY_TDD`  
**Updated:** 2026-08-28 ICT  
**Transport:** GitHub repository history  
**Human authority:** operator authorized continued stabilization; Task 109 authorizes source/test/CI repair only  
**Execution trigger:** manual Hermes/Codex continuation; scheduled execution remains disabled

## Active work

Task:

[`tasks/CNX-20260828-109-rollover-finalize-failclosed-repair.md`](tasks/CNX-20260828-109-rollover-finalize-failclosed-repair.md)

Task ID:

`CNX-20260828-109`

## Task 108 closure

Task 108 report:

`docs/operations/coordination/reports/CNX-20260828-108-windows-plugin-rollover-transaction-repair.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260828-108-windows-plugin-rollover-transaction-repair-review.md`

Review commit:

`bd303899b9b8ca9f011923e9d4563926b4ccad8c`

Review verdict:

`REJECTED — RESIDUAL FAILURE-PATH SOURCE DEFECT`

The later CI/package evidence for `dc5e7a87867d03501b80b662e11aeaab833e0280` is valid reproducibility evidence, but it does not override the source-review rejection. No real-Windows candidate is accepted from Task 108.

## Confirmed Task-109 defect

Task 108 established the correct normal transaction shape:

`pre-install old-state proof -> exactly one external local-.tgz install -> post-install replacement proof -> durable ownership commit`

The remaining defect is specifically the failure after replacement-manifest commit has begun. Current finalization catches a final verification exception and writes `manifestBefore` back.

Because OpenClaw may already have removed the retired generation during the external install, this can reassert a durable manifest whose plugin path no longer exists. Task 108 explicitly prohibited that state.

## Authorized Task-109 sequence

Only source/test/CI work is authorized:

`reconcile remote -> RED semantic final-verification-failure regression -> minimal fail-closed repair -> GREEN targeted tests -> full validation -> exact same-source Actions/package proof -> report`

The RED must simulate external removal/replacement before an injected final ownership verification failure. A string-only assertion is insufficient.

The repaired failure path must:

- remain non-zero/fail-closed;
- not restore/rewrite normal durable ownership to a missing retired generation;
- not declare replacement ownership successful without final proof;
- preserve durable evidence sufficient for later authorized recovery;
- not rerun the external OpenClaw install;
- preserve all successful Task-108 and earlier npm12/namespace/fresh-install protections.

## Source boundary

Reviewed Task-108 CI descendant:

`dc5e7a87867d03501b80b662e11aeaab833e0280`

Task-108 production fix:

`f034cebe5cbe94116c10a81b89c2ef30de6646a8`

The delta from `f034cebe...` to `dc5e7a87...` is only the Task-108 report. Subsequent review/task/coordination commits are documentation-only at authorization time. Executor must fetch current GitHub state before editing and stop `BLOCKED` on unexplained production drift.

## Historical package proof — not live-authorized

Task-108 report-only descendant evidence:

- Validate `33158715078` — success
- PS5.1 Acceptance Smoke `33158715084` — success
- Windows Installer Pack Smoke `33158715087` — success
- artifact ID `9680707129`
- outer SHA256 `1d6a84d64bcd86e6489203d5fddfc5a0528529ce155ad4401c0a8e8174a1c0bc`
- ZIP SHA256 `cdb7f4a63fe64bba21f5ebc8b82f75cfe07071e0472d41b5cd9abf372bbddb2b`
- tar.gz SHA256 `a7c36b01b7e2ee6fbbcb454fc9ab612adda04450ebf8cceb4a98b33edc38f61e`
- payload count `178`
- payload fingerprint `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`

This artifact is historical evidence only. Task 109 must produce a new exact artifact after its repair.

## Preserved live boundary

No new live action was authorized or performed during Task 108/review. The last recorded machine boundary remains Task 107 post-failure evidence: CNX passthrough generation `25`, selected provider Ollama healthy/ready, OpenClaw `2026.7.1-2`, Gateway healthy, SQLite integrity `ok`, Supervisor absent, and retained installer backup/staging residue. This is evidence for a future acceptance task only; Task 109 must not touch it.

## Hard fence

Task 109 does **not** authorize:

- any real Windows install-over/reset/uninstall/reinstall/lifecycle/recovery action;
- replaying Task 107;
- manual live cleanup/normalization;
- Dashboard semantic Send;
- OpenClaw/Ollama update, reinstall, uninstall, stop, or rebaseline;
- provider/model/timeout changes;
- live SQLite/config/session mutation;
- credential/token/password access or re-entry;
- LM Studio management;
- process-tree kills;
- reboot;
- merge/tag/GitHub Release/force push;
- weakening ownership validation.

## Required output

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260828-109-rollover-finalize-failclosed-repair.md`

The report must include RED evidence, root cause, minimal failure-state fix, GREEN targeted/full validation, exact GREEN candidate, exact three workflow run IDs/results, and a new package-proof artifact identity/hashes/fingerprint.

After report publication, stop for independent ChatGPT review. No real-Windows lifecycle acceptance task is authorized until that review accepts a new exact candidate.
