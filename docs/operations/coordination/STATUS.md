# Coordination Channel Status

**State:** `READY_FOR_HERMES`  
**Execution mode:** `SOURCE_TDD_REPAIR`  
**Updated:** 2026-08-28 ICT  
**Transport:** GitHub repository history  
**Human authority:** operator authorized continued stabilization; Task 118 authorizes source/test/CI/package repair only  
**Execution trigger:** manual Hermes/Codex continuation; scheduled execution remains disabled

## Active work

Task:

[`tasks/CNX-20260828-118-posix-installer-provider-neutrality-alignment.md`](tasks/CNX-20260828-118-posix-installer-provider-neutrality-alignment.md)

Task ID:

`CNX-20260828-118`

## Task 117 independent review

Task-117 report:

`docs/operations/coordination/reports/CNX-20260828-117-installer-provider-binding-origin-repair.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260828-117-installer-provider-binding-origin-repair-review.md`

Verdict:

`REJECTED FOR CANDIDATE ADVANCEMENT — WINDOWS POWERSHELL REPAIR IS VALID, BUT THE INSTALLER SUBSYSTEM IS NOT YET PROVIDER-NEUTRAL`

Task 117 successfully removed provider ownership from `scripts/install.ps1` and eliminated the Task-116 PowerShell `Provider` binding surface. Its exact candidate CI was green and no live mutation was replayed.

The independent review found a remaining repository-level architecture conflict: current `scripts/install.sh` still defines/selects/validates Ollama at installation time, requires the Ollama executable, emits provider-specific install output, and passes `enable --provider ollama`. Existing tests intentionally preserve this behavior.

## Task 118 responsibility-locality gate

Task 118 must complete provider-neutrality across the installer subsystem while preserving provider policy in runtime/configuration layers where it is actually required.

Required result:

- no POSIX installer `PROVIDER` variable/default;
- no `--provider` installation API;
- no provider validation/selection in install.sh;
- no direct provider executable prerequisite merely because runtime uses it;
- no provider-specific install/success output;
- no provider-specific lifecycle handoff from installer;
- provider-free canonical POSIX install command;
- accepted Task-117 PowerShell provider-neutral repair remains intact;
- no expansion of runtime provider support.

Required order:

`fresh reconcile -> TESTS-ONLY RED -> minimal install.sh repair -> GREEN -> focused/full validation -> exact candidate CI/package proof -> report`

## Live mutation fence

Task 118 does not authorize any live lifecycle mutation:

- no Task-116 install-over replay;
- no reset/uninstall/reinstall;
- no live POSIX install;
- no live stop/start/restart or recovery harness;
- no manual cleanup/normalization;
- no OpenClaw/provider-runtime changes;
- no provider/model/endpoint/timeout changes;
- no live SQLite/manifest/plugin/session mutation;
- no credential/secret access;
- no Dashboard semantic Send.

The latest authoritative live-machine boundary remains Task 116 post-failure coherent state.

## Required output

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260828-118-posix-installer-provider-neutrality-alignment.md`

After publishing, stop for independent ChatGPT review. A new real-Windows lifecycle retry may be opened only after Task 118 passes independent review on a newly frozen exact candidate.
