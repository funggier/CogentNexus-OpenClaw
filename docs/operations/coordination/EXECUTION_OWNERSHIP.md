# Execution Ownership and Escalation Policy

Updated: 2026-08-30 ICT

## Purpose

Use the smallest execution surface that can produce trustworthy evidence. Do not involve the operator's real machine when repository, GitHub, source, tests, or CI are sufficient. Escalate to Hermes/Codex only when the required proof genuinely depends on local/live environment state or when the operator explicitly requests that handoff.

## Default lane: ChatGPT executes repository-capable work directly

ChatGPT should directly perform work that can be completed and verified through the GitHub coordination/source surface, including:

- reading and reviewing repository source, documentation, reports, reviews, commits, diffs, and workflow evidence;
- root-cause analysis when durable repository evidence is sufficient;
- source, test, documentation, configuration, and CI repair that does not require machine-local state;
- TDD through repository commits and GitHub Actions: genuine RED -> minimal production fix -> GREEN;
- exact-SHA GitHub Actions inspection across available Windows/Linux/macOS runners;
- package/build/plugin validation available in CI;
- coordination task/review/status updates;
- durable review checkpoints and successor-task selection, including explicitly labeled self-review when operator policy permits.

Repository-only work does not need to be delegated to Hermes/Codex merely because an executor exists. Git commits, exact-SHA CI, durable review checkpoints, and coordination records are the proof surface for this lane.

## Review identity and self-review

Reviewer identity separation is optional unless the operator or the active task explicitly requires it.

ChatGPT may execute and review the same repository-capable task when operator policy permits. In that case:

1. use a distinct durable Task/Review checkpoint rather than folding the disposition invisibly into the implementation step;
2. anchor the review to exact commits, tests, CI runs, reports, hashes, or other durable evidence sufficient for the acceptance contract;
3. identify the reviewer as `ChatGPT self-review` when ChatGPT also executed the work;
4. never describe same-actor review as `independent`;
5. do not weaken safety fences, evidence thresholds, exact-SHA requirements, acceptance criteria, or fail-closed behavior because the review is self-review;
6. use a separate reviewer whenever the active task or operator explicitly requires one.

Do not hand work to Hermes/Codex solely to manufacture reviewer separation. A different executor/reviewer identity is not itself evidence of correctness.

## Escalation lane: create a Hermes/Codex task only when local/live proof is necessary or explicitly requested

A dedicated executor task is appropriate when evidence or action requires one or more of the following:

- the operator's real Windows machine or its current filesystem/runtime state;
- real OpenClaw, Ollama, Gateway, provider, controller, service, Scheduled Task, process, or port state;
- supported live install/install-over/update/uninstall/reset/clean-reinstall behavior;
- live recovery, crash, restart, lifecycle, process, service, or reboot behavior;
- real Dashboard/browser/GUI interaction or a semantic Send/ack/delivery side effect;
- local credentials, permissions, OS policy, device, hardware, capture source, or machine-specific integration;
- filesystem behavior that CI cannot prove adequately against the required real topology;
- evidence that must be captured from the actual installation rather than a fixture or CI runner;
- an explicit operator instruction to hand the work to Hermes/Codex.

The task must authorize only the narrow local action/evidence that cannot be obtained safely from GitHub/CI, unless the operator explicitly requests a broader but still bounded handoff.

## Handoff rule

Before creating an executor task, ChatGPT should ask internally:

1. Can the question be answered from repository evidence already present?
2. Can a deterministic test reproduce it in CI?
3. Can GitHub Actions provide the required OS/platform proof?
4. Is real-machine state or a real side effect essential to acceptance?
5. Has the operator explicitly requested a Hermes/Codex handoff?

If 1-3 are sufficient and 4-5 are false, keep the work in the ChatGPT/GitHub lane. If 4 or 5 is true, create the narrowest safe Hermes/Codex task.

Reviewer separation alone is not a reason to answer yes to the handoff gate.

## Existing task ownership and race prevention

When a Hermes/Codex task is already active and an executor may be working on it:

- do not make overlapping production/source changes for the same task from ChatGPT at the same time;
- ChatGPT may continue read-only review, CI inspection, reasoning, and non-overlapping coordination work;
- if ChatGPT must take over implementation, first make the ownership transition explicit in durable coordination state or supersede/rework the active task;
- documentation-only policy work may be appended only with fresh HEAD checks and fast-forward history, without changing the implementation candidate under test;
- after an executor report appears, ChatGPT reviews it before authorizing a successor; that review is naturally cross-actor because Hermes/Codex executed the task, but cross-actor separation is not a standing requirement for ChatGPT-direct work.

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

- ChatGPT direct lane: commits, exact-SHA CI runs, durable review checkpoints, coordination records, and final summaries are the evidence.
- Hermes/Codex local lane: the matching `reports/*.md` file records commands/actions, observed machine evidence, side effects, hashes/commits, and remaining uncertainty.
- Contrary real-machine evidence outranks repository hypotheses and triggers review/rework rather than improvisation.

## Human role

The human operator remains final authority, but should not be used as a courier for logs, task bodies, or routine synchronization. The operator should primarily approve/trigger genuinely local or disruptive actions when required, and may explicitly request a Hermes/Codex handoff at any point.

## Core operating principle

```text
Do everything safely possible in GitHub/CI first.
Use durable self-review checkpoints when the same ChatGPT executor also reviews.
Escalate only the irreducibly local/live remainder or an explicit operator-requested handoff.
Use the real machine for proof, not as the default development surface.
```
