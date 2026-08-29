# Execution Ownership and Escalation Policy

Updated: 2026-08-30 ICT

## Purpose

Use the smallest execution surface that can produce trustworthy evidence. Do not involve the operator's real machine when repository, GitHub, source, tests, or CI are sufficient. Escalate to Hermes/Codex only when the required proof genuinely depends on local or live environment state.

## Default lane: ChatGPT executes repository-capable work directly

ChatGPT should directly perform work that can be completed and verified through the GitHub coordination/source surface, including:

- reading and reviewing repository source, documentation, reports, reviews, commits, diffs, and workflow evidence;
- root-cause analysis when durable repository evidence is sufficient;
- source, test, documentation, configuration, and CI repair that does not require machine-local state;
- TDD through repository commits and GitHub Actions: genuine RED -> minimal production fix -> GREEN;
- exact-SHA GitHub Actions inspection across available Windows/Linux/macOS runners;
- package/build/plugin validation available in CI;
- coordination task/review/status updates;
- independent review and successor-task selection.

Repository-only work does not need to be delegated to Hermes/Codex merely because an executor exists. Git commits, exact-SHA CI, and durable review/coordination records are the proof surface for this lane.

## Escalation lane: create a Hermes/Codex task only when local/live proof is necessary

A dedicated executor task is appropriate when evidence or action requires one or more of the following:

- the operator's real Windows machine or its current filesystem/runtime state;
- real OpenClaw, Ollama, Gateway, provider, controller, service, Scheduled Task, process, or port state;
- supported live install/install-over/update/uninstall/reset/clean-reinstall behavior;
- live recovery, crash, restart, lifecycle, process, service, or reboot behavior;
- real Dashboard/browser/GUI interaction or a semantic Send/ack/delivery side effect;
- local credentials, permissions, OS policy, device, hardware, capture source, or machine-specific integration;
- filesystem behavior that CI cannot prove adequately against the required real topology;
- evidence that must be captured from the actual installation rather than a fixture or CI runner.

The task must authorize only the narrow local action/evidence that cannot be obtained safely from GitHub/CI.

## Handoff rule

Before creating an executor task, ChatGPT should ask internally:

1. Can the question be answered from repository evidence already present?
2. Can a deterministic test reproduce it in CI?
3. Can GitHub Actions provide the required OS/platform proof?
4. Is real-machine state or a real side effect essential to acceptance?

If 1-3 are sufficient, keep the work in the ChatGPT/GitHub lane. If 4 is true, create the narrowest safe Hermes/Codex task.

## Existing task ownership and race prevention

When a Hermes/Codex task is already active and an executor may be working on it:

- do not make overlapping production/source changes for the same task from ChatGPT at the same time;
- ChatGPT may continue read-only review, CI inspection, reasoning, and non-overlapping coordination work;
- if ChatGPT must take over implementation, first make the ownership transition explicit in durable coordination state or supersede/rework the active task;
- documentation-only policy work may be appended only with fresh HEAD checks and fast-forward history, without changing the implementation candidate under test;
- after an executor report appears, ChatGPT independently reviews it before authorizing a successor.

## Remote authority and local checkout freshness

The authoritative revision is the current remote working branch named by coordination, not an arbitrary local checkout.

Hermes/Codex must, before treating coordination gates as current:

1. fetch/synchronize the named working branch from GitHub;
2. verify the remote branch HEAD;
3. read `ACTIVE.md`, `STATUS.md`, the active task, report state, and safety gates from that remote revision;
4. compare any local checkout/worktree against the remote HEAD.

A stale local checkout must never be used to claim that remote coordination is stale or missing.

If the local checkout contains uncommitted or uncertain work, do not reset or overwrite it merely to synchronize. Prefer a fresh clone/worktree from the verified remote HEAD. Never force-push to resolve a freshness problem.

## Evidence ownership

- ChatGPT direct lane: commits, exact-SHA CI runs, durable reviews, coordination records, and final summaries are the evidence.
- Hermes/Codex local lane: the matching `reports/*.md` file records commands/actions, observed machine evidence, side effects, hashes/commits, and remaining uncertainty.
- Contrary real-machine evidence outranks repository hypotheses and triggers review/rework rather than improvisation.

## Human role

The human operator remains final authority, but should not be used as a courier for logs, task bodies, or routine synchronization. The operator should primarily approve/trigger genuinely local or disruptive actions when required.

## Core operating principle

```text
Do everything safely possible in GitHub/CI first.
Escalate only the irreducibly local/live remainder.
Use the real machine for proof, not as the default development surface.
```
