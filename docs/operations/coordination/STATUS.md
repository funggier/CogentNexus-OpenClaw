# Coordination Channel Status

**State:** `READY_FOR_CODEX`  
**Updated:** 2026-08-24 15:02 ICT  
**Transport:** GitHub repository history  
**Human authority:** operator; Task 046 destructive design explicitly approved and reconfirmed `1`  
**Execution trigger:** manual only; scheduled execution remains disabled by operator

## Task 045 disposition

Task `CNX-20260824-045` is reviewed `ACCEPT_SAFE_PREMUTATION_STOP` with result:

`BLOCKED_LEGACY_MIGRATION_NOT_AUTHORIZED`

It proved a managed legacy installation and performed zero destructive invocations.

## Active Task 046

Task `CNX-20260824-046` is ready for the operator's manual Codex signal.

Goal: remove only classifier/proof-bound legacy CogentNexus, then fresh-install the reviewed current CogentNexus-OpenClaw v0.9.3 once.

## Required sequence

1. Re-prove legacy ownership, hashes, plugin inventory, collision-free state, source integrity, and unrelated sentinels.
2. Create one external backup and verify source/destination counts, bytes, and hashes.
3. Invoke exact legacy `cnx.cmd disable` once if required and prove PASSTHROUGH/native health.
4. Uninstall/remove only exact `cogentnexus-rotation`, exact legacy config/load paths, exact `CogentNexus Supervisor`, `cnx.cmd`, `skills\cogentnexus`, `.cogent`, and exact proven plugin residue.
5. Require classifier result `fresh`.
6. Invoke current `scripts/install.ps1` once with only the workspace argument.
7. Exact-verify `cnxclaw.cmd`, new skill/state/ownership/plugin/scheduler, Gateway/Ollama, backup, legacy absence, and unrelated data.

## Stop gates

Stop before removal if native plugin inventory still times out, source/ownership/backup/handoff is unproved, or state is mixed/unowned.

If removal or fresh installation fails, preserve backup/recovery evidence and stop. No retry, automatic restore, manual broad cleanup, clean reinstall, or install-over migration.

## Exclusions

No OpenClaw user-data reset, Ollama model/provider change, HermesAgent, Ecosystem, staged-capability-loop, Procmon/Task 027/038, primary-repository Git mutation, merge, tag, Release, or archive action.

Report meaningful progress approximately every 3 minutes and at every safety transition.
