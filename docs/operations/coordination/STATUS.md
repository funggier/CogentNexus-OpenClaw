# Coordination Channel Status

**State:** `READY_FOR_HERMES`  
**Execution mode:** `LIVE_WINDOWS_REPAIRED_CANDIDATE_INSTALL_OVER_HEALTH_PROOF`  
**Updated:** 2026-08-30 ICT  
**Transport:** GitHub repository history  
**Human authority:** operator explicitly approved opening the next Hermes Task for the necessary live Windows checkpoint  
**Execution trigger:** operator instructs Hermes to execute Task 157 on the real Windows/OpenClaw environment

## Active work

Task:

[`tasks/CNX-20260830-157-repaired-candidate-windows-install-over-health-proof.md`](tasks/CNX-20260830-157-repaired-candidate-windows-install-over-health-proof.md)

Task ID:

`CNX-20260830-157`

Owner / coordinator / reviewer: ChatGPT  
Executor: Hermes

## Authorization basis

Task 155 repaired the public-hook duplicate durable-authority defect and has been reviewed `ACCEPT`.

Accepted production repair:

`1ec8cfc81b8a21a178200c33816427f9abfd31b9`

Task-155 acceptance checkpoint commit:

`d4a4d6b0b14d18eee47d608edd66917eb27b9a68`

The next required Phase-P checkpoint is live deployment proof of the repaired candidate before any Dashboard semantic reacceptance.

## Task-157 gate

Hermes is authorized only to:

- capture pre-state and candidate/package provenance;
- perform repaired-candidate **install-over** using the established process;
- perform the minimum lifecycle actions necessary for install-over and health proof;
- inspect installed identity, provenance, status, health, relevant logs, loader/plugin state;
- publish the Task-157 evidence report.

Candidate provenance must be established before live install-over. If it cannot be established, stop `BLOCKED` before mutation.

## Required output

Hermes must publish:

`docs/operations/coordination/reports/CNX-20260830-157-repaired-candidate-windows-install-over-health-proof.md`

Then stop. ChatGPT will fresh-read and review the durable report before authorizing any successor Task.

## Live / semantic fence

Phase P remains pending/FAIL until later acceptance completes.

Task 157 does **not** authorize Dashboard semantic Send, Dashboard click/focus/type/paste for semantic testing, a new semantic user message, manual Ticket/workflow/outbox/delivery/database mutation, reset, clean uninstall/fresh reinstall, arbitrary live-state deletion, production/source patching, OpenClaw source patching, dependency upgrade, Phase Q, merge, tag, GitHub Release, package publication/promotion, or force push.

A separate explicit coordination Task is required before Dashboard durable-delivery reacceptance.
