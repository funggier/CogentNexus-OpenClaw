# Coordination Channel Status

**State:** `READY_FOR_CODEX`  
**Updated:** 2026-08-24 18:58 ICT  
**Transport:** GitHub repository history  
**Human authority:** operator approved Task 049 backup/removal-to-fresh design with response `1`  
**Execution trigger:** manual only; scheduled execution remains disabled by operator

## Task 048 disposition

Task `CNX-20260824-048` is reviewed `ACCEPT_BOUNDED_NONREPRODUCTION` with result:

`BLOCKED_INSUFFICIENT_EVIDENCE`

The earlier timeout did not reproduce. Native registry inspection returned valid JSON in 16.378 seconds; native plugin list returned valid JSON for 72 plugins in 4.785 seconds; lifecycle trace completed normally. The legacy plugin is natively owned as `cogentnexus-rotation` / `openclaw-plugin-cogentnexus-rotation` v0.9.1. No live repair or mutation occurred.

## Active Task 049

Task `CNX-20260824-049` is ready for the operator's manual Codex signal.

Goal: create a verified external backup, remove only proven legacy CogentNexus, reach the current installation classifier result `mode=fresh`, and stop before installing the current CogentNexus-OpenClaw.

## Required sequence

1. Prove exact coordination/source/collision/legacy ownership and current runtime sentinels.
2. Run the now-proven native inventory command once.
3. If it fails again, back up first, then use at most one registry refresh and one `doctor --fix`, with bounded retries.
4. Create and independently verify the external legacy/config/SQLite/scheduler/plugin backup.
5. Invoke legacy `cnx.cmd disable` once and prove PASSTHROUGH/native health.
6. Preview and invoke the exact native plugin uninstall once.
7. Remove only the exact legacy supervisor task, launcher, skill, state, owned plugin residue, and exact config/load-path/install-record residue.
8. Gracefully restart Gateway once only if required to unload the removed plugin.
9. Prove OpenClaw registry health and CogentNexus classifier `mode=fresh` separately.
10. Verify unrelated systems/data and publish a report-only commit.

## Mandatory stop-before-install gate

Task 049 must not invoke or download/run:

- `scripts/install.ps1`;
- `clean-reinstall.ps1`;
- any current Release installer;
- any equivalent current-product installation path.

It must not create `cnxclaw.cmd`, `skills\cogentnexus-openclaw`, `.cogentnexus-openclaw`, or the current plugin/controller/scheduler.

Installation requires Task 049 report review, a successor task, and new explicit operator approval.

## Stop gates

Stop and report on backup failure, ownership drift, native repair failure, handoff failure, unsafe plugin removal, locked/unowned legacy cleanup, fresh-classification failure, preservation failure, or unsafe publication. Do not auto-restore.

## Exclusions

No OpenClaw upgrade/downgrade/reinstall, manual SQLite edit, Ollama/model change, broad cleanup, wildcard/parent deletion, force kill, primary-repository Git mutation, HermesAgent, Ecosystem, staged-capability-loop, Procmon/Task 027/038, merge, tag, Release, or archive action.

Report meaningful progress approximately every 3 minutes and at every backup/repair/handoff/removal/fresh-classification/safety transition.
