# Coordination Channel Status

**State:** `READY_FOR_CODEX`  
**Updated:** 2026-08-24 12:34 ICT  
**Transport:** GitHub repository history  
**Human authority:** operator; Task 045 explicitly authorized by reply `1`  
**Execution trigger:** manual only; scheduled execution remains disabled by operator

## Task 044 disposition

Task `CNX-20260824-044` is reviewed `ACCEPT`.

Accepted implementation commit:

`4c825f8ec1ed6b43a419ad52e0bb85cee28007c1`

## Active Task 045

Task `CNX-20260824-045` is ready for the operator's manual Codex signal.

Purpose: live Windows clean-reinstall acceptance using the reviewed default external backup path, exact ownership gates, one destructive invocation maximum, fresh v0.9.3 installation, and post-install/side-effect proof.

## Mandatory pre-mutation classification gate

Only an exact coherent v0.9.3 `upgrade` may proceed.

The task must stop read-only if the live machine is:

- legacy CogentNexus requiring migration;
- fresh with product plugin/task/service residue;
- mixed, partial, ambiguous, or unowned;
- missing exact manifest/plugin/launcher/artifacts;
- affected by source drift, command collision, unsafe backup boundary, or insufficient preflight conditions.

Legacy migration is not included in the current authorization.

## Authorized destructive boundary

If every preflight gate passes, Codex may invoke the reviewed `scripts/clean-reinstall.ps1` exactly once with only the live workspace argument and default backup behavior.

No retry, `-NoBackup`, custom backup root, linked plugin, manual substitute deletion, automatic restore, or broader force action is authorized.

## Failure behavior

On any failure, stop, preserve backup and recovery evidence, publish one report, and request a new human decision. Do not manually finish or repeat installation.

## Paused/excluded work

`CogentNexus-HermesAgent`, `CogentNexus-Ecosystem`, `staged-capability-loop`, Procmon/Task 027/038 evidence, merge, tag, Release, and archive remain excluded.

Report meaningful progress approximately every 3 minutes and at every safety transition.
