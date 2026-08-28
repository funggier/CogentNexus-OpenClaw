# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `SOURCE_TDD_REPAIR`
Current authorization: `CNX-20260828-118_POSIX_INSTALLER_PROVIDER_NEUTRALITY_ALIGNMENT`
Task ID: `CNX-20260828-118`
Updated: 2026-08-28 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260828-118-posix-installer-provider-neutrality-alignment.md`](tasks/CNX-20260828-118-posix-installer-provider-neutrality-alignment.md)

Task 118 is a **source-only TDD repair** to finish provider-neutral responsibility across the installer subsystem after Task 117 repaired Windows PowerShell but left the POSIX installer provider-coupled.

## Task 117 closure

Task-117 report:

`docs/operations/coordination/reports/CNX-20260828-117-installer-provider-binding-origin-repair.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260828-117-installer-provider-binding-origin-repair-review.md`

Review verdict:

`REJECTED FOR CANDIDATE ADVANCEMENT — WINDOWS POWERSHELL REPAIR IS VALID, BUT THE INSTALLER SUBSYSTEM IS NOT YET PROVIDER-NEUTRAL`

Accepted Task-117 work:

- `scripts/install.ps1` no longer accepts/defines/validates/defaults provider;
- PowerShell installer no longer directly requires Ollama merely for installation;
- PowerShell installer uses generic runtime `enable` handoff;
- Task-116 `3D Objects` provider-binding surface is removed;
- Task-117 exact candidate CI was green;
- no live Task-116 replay occurred.

Blocking finding:

Current `scripts/install.sh` still contains `PROVIDER="ollama"`, `--provider`, direct Ollama prerequisite, provider-specific output, and `enable --provider ollama`. Current tests explicitly preserve that POSIX coupling.

## Architectural invariant

**Every subsystem defines only data genuinely required to perform or verify that subsystem's own responsibility.**

Installation does not own provider name/model/endpoint/timeout/provider executable/provider-selection policy. Both current installer entry points must therefore expose the same provider-neutral responsibility boundary.

This does not broaden runtime provider support. Provider/runtime modules remain provider-aware where provider knowledge is genuinely required.

Required Task-118 method:

`fresh reconcile -> TESTS-ONLY POSIX provider-neutral RED -> minimal install.sh boundary repair -> GREEN -> focused/full validation -> exact same-SHA CI/package proof -> report -> independent review`

## Preserved live boundary

Task 116 remains the latest authoritative live-machine evidence:

- CNX passthrough, generation 25;
- OpenClaw exactly `2026.7.1-2`;
- current runtime/provider healthy;
- Gateway healthy;
- SQLite integrity `ok`;
- interrupted-reentry classification coherent;
- no lifecycle phase beyond the failed pre-body Task-116 install-over binding executed.

Task 118 must not mutate live state.

## Hard fence

Task 118 does **not** authorize:

- live install-over/reset/uninstall/reinstall;
- live POSIX installation;
- Task-116 destructive replay;
- live stop/start/restart/recovery harness;
- manual cleanup/normalization;
- OpenClaw/provider-runtime changes;
- provider/model/endpoint/timeout changes;
- live SQLite/config/session/manifest/plugin mutation;
- credentials/secrets access;
- Dashboard semantic Send;
- reboot/process-tree kill;
- merge/tag/release/force push.

## Completion signal

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260828-118-posix-installer-provider-neutrality-alignment.md`

Then stop for independent ChatGPT review. Do not create or execute a real-Windows lifecycle retry task.
