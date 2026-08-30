# Execution Ownership and Escalation Policy

Updated: 2026-08-31 ICT

## Purpose

Use an executor-heavy, reviewer-light workflow that preserves strong evidence while reducing duplicated analysis and ChatGPT context consumption.

Standing role model:

- Hermes/Codex is the default primary technical investigator and implementer for delegated tasks.
- ChatGPT is the coordinator, acceptance-contract author, evidence reviewer, and final disposition owner.
- The human operator remains final authority.

See also:

- `EXECUTOR_ANALYSIS_REVIEW_MODEL.md`
- `EXECUTOR_REPORT_CONTRACT.md`

## Default delegated lane: Hermes/Codex owns the technical loop

When ChatGPT publishes a delegated task, Hermes/Codex should normally execute the full authorized technical loop, including both repository and local/live work as applicable:

- fresh remote-state synchronization;
- source/repository/upstream investigation;
- root-cause analysis;
- TDD RED -> minimal fix -> GREEN;
- source/test/configuration/installer/CI repair within task scope;
- targeted and full validation;
- exact-SHA GitHub Actions inspection;
- package/build/plugin/schema evidence;
- local Windows/runtime/lifecycle/GUI proof when explicitly authorized;
- risk and residual-uncertainty analysis;
- detailed report publication under `reports/` using `EXECUTOR_REPORT_CONTRACT.md`.

Repository/source/test/CI work is no longer reserved for ChatGPT by default once a task is delegated.

## ChatGPT lane: framing, targeted review, and disposition

ChatGPT normally performs:

- task framing from operator intent;
- success criteria and evidence requirements;
- hard fences and irreversible-action gates;
- selection of accepted candidate/parent state;
- targeted review of the executor report and verification packet;
- independent spot-checks of critical claims;
- deeper source/diff/CI reconstruction only when evidence quality, contradiction, or risk requires it;
- ACCEPT / REWORK / BLOCKED review publication;
- successor-task selection;
- standing coordination-policy changes.

ChatGPT may still perform direct repository work when the operator explicitly requests it, when executor capability is unavailable, or when a narrow reviewer-side probe is cheaper and safer than a new executor cycle. This is an exception rather than the standing default for delegated technical work.

## No reconstruction by default

A compliant executor report is a structured claim set, not an instruction for ChatGPT to repeat the entire investigation.

ChatGPT should begin with:

1. task/lineage/acceptance-contract check;
2. verification-packet spot checks;
3. targeted inspection of high-impact or uncertain claims.

Full reconstruction is required only when the report is insufficient, contradictory, implausible, or safety-critical evidence cannot otherwise be established.

## Review identity

For delegated tasks, Hermes/Codex executes and ChatGPT reviews, naturally creating cross-actor separation.

Reviewer identity separation itself is not evidence. Acceptance still depends on exact commits, tests, workflow runs, artifact hashes, machine observations, and task-specific proof.

If ChatGPT directly executes a task and later reviews it, the durable review must say `ChatGPT self-review`; it must never be described as independent.

## Local/live authority

Hermes/Codex may perform real-machine or semantic actions only when the active task explicitly authorizes them.

Examples requiring explicit live authority include:

- install/install-over/update/uninstall/reset/clean-reinstall;
- Gateway/Ollama/provider/controller/service/process restart or mutation outside installer-owned transitions;
- crash/recovery/reboot acceptance;
- Dashboard/browser/GUI semantic interaction;
- semantic Send/ack/delivery side effects;
- local filesystem/state mutation beyond the task's repository/worktree operations;
- manual database or durable runtime-state mutation;
- hardware/device/permission changes.

Repository delegation does not implicitly authorize live side effects.

## Executor autonomy inside the hard fence

Hermes/Codex may determine the investigation sequence, inspect additional relevant source, add narrowly necessary regression coverage, and choose safe implementation details needed to satisfy the task.

It must not broaden into unrelated product changes, destructive/live actions, dependency upgrades, OpenClaw upgrades/patches, releases, default-branch merges, force pushes, or successor tasks unless the active task explicitly authorizes them.

If broader authority is required, report `BLOCKED` or `REWORK_REQUIRED` with the exact needed scope.

## Existing task ownership and race prevention

When a Hermes/Codex task is active:

- Hermes/Codex owns production/source implementation for that task unless the task says otherwise;
- ChatGPT must not make overlapping production/source changes concurrently;
- ChatGPT may perform read-only review, coordination updates, and non-overlapping policy/documentation work with fresh HEAD checks;
- if ChatGPT must take over implementation, ownership must first be changed explicitly in durable coordination state;
- before every push/write, the executor must fetch/race-check the remote branch and preserve normal fast-forward history;
- never force-push to solve coordination drift.

## Remote authority and local checkout freshness

The current remote working branch named by coordination is authoritative.

Hermes/Codex must:

1. fetch/synchronize the named branch;
2. verify remote HEAD;
3. read remote `ACTIVE.md`, `STATUS.md`, active task, and report state;
4. compare local checkout/worktree against remote HEAD;
5. prefer a fresh clone/worktree if local state is stale or uncertain;
6. never reset away unknown local work merely to synchronize.

A stale local checkout cannot override remote coordination truth.

## Evidence ownership

Hermes/Codex owns the primary technical evidence package for delegated tasks:

- implementation commits;
- test output summaries;
- workflow run IDs;
- artifact hashes/fingerprints;
- local evidence paths and hashes;
- machine observations;
- risk/uncertainty analysis;
- acceptance matrix;
- verification packet;
- final matching `reports/*.md` file.

ChatGPT owns the durable review/disposition and successor authorization.

Contrary real-machine evidence outranks repository hypotheses and triggers review/rework rather than improvisation.

## Human role

The human operator should not be used as a courier for logs, task bodies, or routine synchronization. The operator primarily provides intent, approves policy or disruptive boundaries when required, triggers authorized executors, and remains final authority.

## Core operating principle

```text
ChatGPT defines what must be proven and what must not be crossed.
Hermes/Codex performs the deep technical work and packages the evidence.
ChatGPT verifies the critical claims instead of rebuilding the investigation.
Escalate review depth only when evidence or risk requires it.
```
