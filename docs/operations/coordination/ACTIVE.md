# Active Coordination Task

Status: `READY_FOR_CODEX`  
Execution mode: `AUTO`  
Task ID: `CNX-20260824-042`  
Updated: 2026-08-24 06:52 ICT  
Owner: ChatGPT  
Executor: Codex

## Active task

[`tasks/CNX-20260824-042-openclaw-namespace-isolation.md`](tasks/CNX-20260824-042-openclaw-namespace-isolation.md)

## Human direction

The operator accepted Task 041 bounded non-recurrence without claiming root cause and redirected current work to complete product-wide namespace isolation before install/uninstall acceptance.

Required identity and release version: `CogentNexus-OpenClaw v0.9.3`.

Examples: `cnxclaw.cmd`, `.cogentnexus-openclaw`, skill `CogentNexus-OpenClaw`, plugin `cogentnexus-openclaw`, and v0.9.3 release notes explaining the explicit naming/namespace contract.

## Purpose

Ensure a future CogentNexus-HermesAgent installation can coexist on the same machine without collisions across launchers, skills, plugins, state/config, tools, tasks/services, logs, backups, packages, reset, or uninstall.

## Safety

Repository-only implementation in one isolated full clone. No new Git worktree, Task 027/038 access, live installation, OpenClaw config mutation, runtime action, reset/uninstall, Procmon action, retained-evidence cleanup, merge, tag, or release.

Do not repeat Task 041.

## Duplicate fence

If the matching Task 042 report exists at freshly fetched HEAD, do not repeat implementation or publish a duplicate.
