# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `SOURCE_REPAIR_TDD_RECOVERY_PREFLIGHT_SEMANTICS`
Current authorization: `RECOVERY_PREFLIGHT_CORRECTION_AUTHORIZED`
Task ID: `CNX-20260826-073`
Updated: 2026-08-26 18:29 ICT
Owner: ChatGPT
Executor: Hermes after the operator's continuation signal

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260826-073-correct-clean-fresh-recovery-preflight.md`](tasks/CNX-20260826-073-correct-clean-fresh-recovery-preflight.md)

## Task 072 review

Task 072 reported:

`PASS_FRESH_INSTALL_OWNED_RUNTIME_NO_FLASH_VERIFIED`

Install source:

`9df671670908241486afe2badf8a7f221410c6f8`

Report HEAD:

`19d3ae6bf090e58aaf9b45da52fe3ae6f4f7d11a`

Independent review decision:

`ACCEPT`

Disposition:

`ACCEPT_LIVE_INSTALL_OWNED_RUNTIME_NO_FLASH_WITH_PREFLIGHT_FOLLOWUP`

Review commit:

`9811272b8826ade6bf3d12f6091d2fcb8ff044ab`

## Accepted Task-072 live state

- one-time Task-066 residue cleanup completed within the exact two authorized roots;
- one normal fresh install completed from exact accepted source;
- controller is MANAGED and Gateway/Ollama/plugin/ownership/AGENTS/SQLite health passed;
- launcher and Supervisor bind to CogentNexus-owned runtime under `%LOCALAPPDATA%\CogentNexus-OpenClaw\runtime\python` with no durable Hermes/Codex/temp dependency;
- five natural PT1M ticks passed with `NO_FLASH_MULTI_TICK_PROVEN`;
- no product semantic LLM smoke was performed.

## Follow-up defect discovered during independent review

Task-072's install log emitted a recovery-preflight error even after the pre-marker residue had already been removed.

Root cause in accepted production source:

1. `recovery_preflight()` raises whenever there is no marker before distinguishing clean fresh inventory from unmarked partial residue.
2. `install.ps1` does not explicitly stop when `recovery-preflight` exits nonzero; it proceeds to `classify-install`.

This did not invalidate Task-072 runtime/no-flash acceptance, but it is a known installer correctness gap and must be corrected before final release/source parity and semantic acceptance.

## Authorized Task 073 operation

Source/tests only. Correct clean-fresh recovery semantics and make installer recovery-preflight errors fail closed before classification/mutation. Preserve unmarked-residue safety, incomplete-transaction recovery, owned-install behavior, fresh transaction ordering, upgrade/legacy isolation, npm 11/12 reproducibility, and all accepted runtime ownership design.

## Live hard fence

Do not mutate the healthy Task-072 live installation: no install/install-over/uninstall/reset/lifecycle action, Scheduled Task/Gateway/Ollama/plugin/config/AGENTS/SQLite mutation, process termination, reboot, HermesAgent mutation, merge/tag/release, or semantic LLM smoke.

## Pre-authorized successor

If Task 073 is independently accepted, Task 074 may perform one supported install-over from the accepted correction onto the current MANAGED installation and re-prove source/live parity, owned runtime, MANAGED health, and >=3 natural PT1M no-flash ticks. Final semantic acceptance moves to Task 075.