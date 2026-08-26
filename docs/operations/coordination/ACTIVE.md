# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `LIVE_BOUNDED_RESIDUE_CLEANUP_FRESH_INSTALL_OWNED_RUNTIME_NO_FLASH`
Current authorization: `BOUNDED_RESIDUE_CLEANUP_AND_FRESH_INSTALL_LIVE_ACCEPTANCE_AUTHORIZED`
Task ID: `CNX-20260826-072`
Updated: 2026-08-26 17:21 ICT
Owner: ChatGPT
Executor: Hermes after the operator's continuation signal

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260826-072-bounded-cleanup-fresh-install-owned-runtime-live-acceptance.md`](tasks/CNX-20260826-072-bounded-cleanup-fresh-install-owned-runtime-live-acceptance.md)

## Task 071 review

Task 071 reported:

`PASS_UPGRADE_LEGACY_MODE_ISOLATION_PROVEN`

Production candidate HEAD:

`9df671670908241486afe2badf8a7f221410c6f8`

Test-only implementation HEAD:

`7a55980e662b50f2d2979eb77a3ac1f89da7912f`

Report HEAD:

`d1c8382690d1e06e60ef335e26ba19cdde9152df`

Independent review decision:

`ACCEPT`

Disposition:

`ACCEPT_UPGRADE_LEGACY_MODE_ISOLATION_PROVEN`

Review commit:

`3943fb9988c44fecf407b5cb2375bc9adcaf5746`

## Accepted source for live install

Task 072 MUST install exact production commit:

`9df671670908241486afe2badf8a7f221410c6f8`

Task-071 commits after this point are tests/report only.

Accepted source properties include:

- reproducible npm 11/npm 12 lock with OpenClaw exactly `2026.7.1-2`;
- fresh transaction begin/record/commit/recovery contract;
- exact application-data authority and record-time path rejection;
- attempt-scoped supported plugin inverse;
- shared-parent deletion safety;
- fresh caught-failure rollback coverage;
- restored upgrade/legacy reachability and non-fresh rollback isolation;
- CogentNexus-owned runtime authority design from Tasks 063-065.

## Current live baseline to re-prove

Task 066 accepted blocker ended with:

- no Supervisor task;
- no launcher/plugin registration;
- AGENTS managed block absent;
- native OpenClaw Gateway healthy;
- Ollama healthy with four models;
- no ownership manifest;
- exactly two unowned failed-install residue roots:
  - `<workspace>\.cogentnexus-openclaw`
  - `<workspace>\skills\cogentnexus-openclaw`

Task 072 must re-prove this live state before any deletion.

## Authorized Task 072 operation

1. Re-prove exact Task-066 residue and preservation baselines.
2. Delete exactly those two residue roots once, only after attribution/safety proof.
3. Perform one normal fresh install from exact `9df6716...` with no skip/link shortcuts.
4. Prove launcher and Scheduled Task bind to `%LOCALAPPDATA%\CogentNexus-OpenClaw\runtime\python\Scripts\python.exe/pythonw.exe`, with no Hermes/Codex/temp durable path.
5. Observe at least three natural PT1M supervisor ticks and prove no causal conhost/console-python trampoline.
6. Finish final non-semantic MANAGED/Gateway/Ollama/plugin/config/ownership/AGENTS/SQLite health acceptance.

## Live hard fences

- Do not uninstall again.
- Do not repeat a completed cleanup/install after session interruption; inspect live state first.
- No reboot/power cycle.
- No source edits.
- No provider/model changes or Ollama pulls/removals.
- No broad cleanup outside the two proven residue roots.
- No HermesAgent mutation.
- No merge/tag/release.
- No real user-message/LLM semantic smoke in Task 072.

## Pre-authorized successor

If Task 072 is independently accepted, Task 073 may perform the separate bounded semantic flow:

`user message -> durable Ticket -> Ollama LLM -> durable result/delivery -> user-visible response`.
