# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `SOURCE_TEST_VERIFICATION_MODE_SPECIFIC_NONFRESH_ISOLATION`
Current authorization: `MODE_SPECIFIC_NONFRESH_VERIFICATION_AUTHORIZED`
Task ID: `CNX-20260826-071`
Updated: 2026-08-26 16:19 ICT
Owner: ChatGPT
Executor: Hermes after the operator's continuation signal

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260826-071-prove-upgrade-legacy-mode-isolation.md`](tasks/CNX-20260826-071-prove-upgrade-legacy-mode-isolation.md)

## Task 070 review

Task 070 reported:

`PASS_INSTALLER_MODE_ISOLATION_RESTORED`

Implementation HEAD:

`9df671670908241486afe2badf8a7f221410c6f8`

Report HEAD:

`573ca752e1c257a071d9a56b4206039c911b3b56`

Independent review decision:

`REWORK`

Disposition:

`REWORK_MODE_SPECIFIC_UPGRADE_LEGACY_EVIDENCE_MISSING`

Review commit:

`3b3cea20d02e66e34704bd3ee8d1ed79f1610b79`

## Accepted Task 070 candidate behavior

Preserve unless a new executable proof fails:

- Task-069 synthetic non-fresh abort sentinel is removed;
- one shared installer body serves fresh/upgrade/legacy;
- fresh rollback is gated by `$isFreshTransaction` in the catch;
- non-fresh failures rethrow without fresh rollback;
- fresh transaction begin remains fresh-only;
- commit remains after ownership create + verify;
- Task-067–069 npm/transaction/application-data/plugin-inverse/shared-parent safety remains intact;
- publication fence passed.

## Blocking evidence gap

Task 070 did not implement the required mode-specific executable M4/M5 proofs:

1. no coherent production `upgrade` classification fixture proves no fresh transaction marker is created;
2. no valid production `legacy` ownership/classification fixture proves migration/native-handoff reachability and no fresh marker;
3. the published M1/M2 harnesses mirror `$isFreshTransaction=$false` but do not distinguish or drive actual `upgrade` and `legacy` classification contracts.

## Current live condition

Preserve the accepted Task-066 native baseline:

- no CogentNexus Supervisor task;
- no launcher/plugin registration;
- AGENTS managed block absent;
- OpenClaw Gateway native/healthy;
- Ollama healthy;
- Task-066 partial unowned workspace residue remains untouched;
- no valid ownership manifest.

## Authorized Task 071 operation

Source/tests verification only. Build real production-facing coherent upgrade and valid legacy fixtures, prove both classifications and no fresh marker/rollback behavior, re-run fresh rollback and full regression gates. Prefer test-only changes; do not alter production code unless a new failing executable test proves a defect.

## Live hard fence

No live residue cleanup, install/uninstall/reset/lifecycle operation, Scheduled Task mutation, Gateway/Ollama/plugin/config/AGENTS/SQLite mutation, process termination, reboot, primary workspace mutation, HermesAgent mutation, merge/tag/release.

## Pre-authorized successor

If Task 071 is independently accepted, Task 072 may perform bounded one-time Task-066 residue cleanup and fresh install, then exact owned-runtime/no-Hermes binding, at least three natural PT1M no-flash ticks, and final MANAGED health acceptance without another confirmation.
