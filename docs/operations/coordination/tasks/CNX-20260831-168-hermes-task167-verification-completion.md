# CNX-20260831-168 — Hermes/Codex Task-167 Verification Completion

Status: `READY_HERMES`

Execution mode: `REPOSITORY_TASK167_VERIFICATION_COMPLETION_HERMES`

Current authorization: `CNX-20260831-168_HERMES_TASK167_VERIFICATION_COMPLETION`

Task ID: `CNX-20260831-168`

Updated: 2026-08-31 ICT

Executor: Hermes/Codex

Coordinator / final reviewer: ChatGPT

Review model: `executor-heavy / reviewer-light`

## Purpose

Complete the mandatory validation and evidence package for the Task-167 repository repair without changing the product candidate by default.

Task 167 produced repair SHA:

`231761fca24c315e90536955d3e384f55e2e232e`

and proposed root cause: the prior delivery path learned the final candidate at `before_agent_finalize` after the native `before_message_write` opportunity had already occurred. The Task-167 report supplied a production-shaped RED/GREEN regression, but its acceptance evidence did not yet satisfy the mandatory report contract.

Task-167 ChatGPT review:

`docs/operations/coordination/reviews/CNX-20260831-167-hermes-native-delivery-staging-root-cause-repair-review.md`

Disposition:

`REWORK_REQUIRED — EVIDENCE_CONTRACT_INCOMPLETE`

This is an evidence-completion task, not a new repair task.

## Standing policy

Read and obey:

- `docs/operations/coordination/EXECUTOR_ANALYSIS_REVIEW_MODEL.md`
- `docs/operations/coordination/EXECUTION_OWNERSHIP.md`
- `docs/operations/coordination/EXECUTOR_REPORT_CONTRACT.md`
- `docs/operations/coordination/CODEX_BOOTSTRAP.md`
- Task 167, Task-167 report, and Task-167 ChatGPT review.

Hermes/Codex owns the primary verification and evidence packaging. ChatGPT will review the resulting verification packet rather than reconstructing Task 167 from scratch.

## Authoritative product candidate

Exact Task-167 repair SHA:

`231761fca24c315e90536955d3e384f55e2e232e`

Pinned OpenClaw remains:

`0790d9f593ad30c940ed93b5872a8cf6d6f3cf8c` (`2026.7.1-2`).

Later coordination-only commits must not be treated as product changes.

Before validation, verify that the product/test diff from Task-167 base `5b481ff1c5d64e40f9a87ff792599c63cfcf84a9` to repair SHA `231761fc...` is limited to the intended Task-167 source/test/report surface and that no dependency/OpenClaw/product-adjacent drift occurred beyond what the report claims.

## Objectives

Provide enough exact evidence for ChatGPT to decide whether Task 167 can be accepted without repeating the executor's investigation.

At minimum:

1. verify exact candidate lineage and changed-file scope;
2. complete all missing required local validation against exact product repair SHA `231761fc...` using a clean/fresh checkout or equivalent immutable worktree;
3. inspect all required exact-SHA GitHub workflows and record final IDs/results;
4. re-evaluate the Task-167 root-cause/repair claim against validation results and note any contradiction;
5. produce the mandatory acceptance matrix;
6. produce the mandatory Reviewer Verification Packet;
7. make no live Windows/runtime/semantic mutation.

## Required local validation

Run and record, at minimum, on exact repair SHA `231761fca24c315e90536955d3e384f55e2e232e`:

1. Task-167 production-faithful regression;
2. Task-162 native transcript authority regression;
3. v091 Dashboard verified-delivery regression set;
4. duplicate/no-regeneration/recovery coverage relevant to the boundary;
5. full plugin test suite;
6. TypeScript/no-emit validation where part of current repository practice;
7. `npm run build`;
8. `npm run plugin:validate`;
9. `python scripts/check_baseline_consistency.py` or the current authoritative baseline-consistency command if repository naming has changed;
10. package/installer validation appropriate to the plugin source change, including the repository's normal packed-package verification path.

If the exact command differs because the repository has moved, record the actual current command and why it is authoritative.

Do not substitute a narrower command for a required validation without explaining the equivalence.

## Exact-SHA workflow requirement

Inspect final outcomes for Task-167 repair SHA `231761fca24c315e90536955d3e384f55e2e232e`:

- Validate run `33330458434`;
- Windows Installer Pack Smoke run `33330458470`;
- PS5.1 Acceptance Smoke run `33330458475`.

At the Task-167 review snapshot, PS5.1 had already succeeded while Validate and Windows Installer Pack Smoke were still running. Task 168 must record their **final** states and must not claim PASS while any required exact-SHA run is pending, cancelled, skipped unexpectedly, or failed.

If a required workflow fails, analyze the failure enough to classify whether it invalidates the repair. Do not modify production source inside Task 168 merely to turn CI green; report `FAIL`/`REWORK_REQUIRED` and stop for ChatGPT disposition unless the task is explicitly superseded with repair authorization.

## Required risk and safety analysis

The report must explicitly analyze, at minimum:

- why session-key fallback cannot bind the assistant write to the wrong Ticket;
- behavior when zero or more than one eligible accepted direct Dashboard Ticket exists;
- crash window after staging/claim but before native append;
- crash window after native append but before transcript-update settlement;
- interaction with host recovery and marker/history dedupe;
- whether `before_agent_finalize` can overwrite, delete, or otherwise perturb already-settled state after the earlier pre-write path;
- whether existing Task-155/Task-162 duplicate/no-regeneration guarantees remain intact;
- any liveness tradeoff introduced by the repair.

Do not invent certainty where tests/evidence do not prove it. Record residual uncertainty explicitly.

## Report contract

Create:

`docs/operations/coordination/reports/CNX-20260831-168-hermes-task167-verification-completion.md`

The report must comply fully with `EXECUTOR_REPORT_CONTRACT.md` and include:

1. disposition;
2. objective and acceptance contract;
3. exact authority/start state;
4. candidate lineage and changed-file scope;
5. concise Task-167 root-cause/repair summary;
6. alternatives/hypotheses/contradictions relevant to final confidence;
7. exact local validation commands and results;
8. exact workflow IDs/final results;
9. risk/crash-window/duplicate-safety analysis;
10. acceptance matrix covering every Task-167 and Task-168 requirement;
11. anomalies and residual uncertainty;
12. hard-fence compliance;
13. **Reviewer Verification Packet** with 3–10 critical claims, each containing:
    - claim;
    - exact evidence pointer;
    - why the evidence supports it;
    - narrowest independent ChatGPT check;
14. recommended successor gate.

## Hard fence

Task 168 is repository verification-only by default.

Do **not**:

- perform any Dashboard semantic Send;
- use another live semantic OpenClaw surface;
- use `chat.inject`;
- install-over, uninstall, reinstall, or reset the Windows installation;
- restart/mutate live Gateway, Ollama, Supervisor, or OpenClaw runtime;
- manually mutate live Ticket/workflow/result/outbox/delivery/database/transcript state;
- modify production source or Task-167 regression merely to improve acceptance results;
- patch/upgrade OpenClaw;
- upgrade dependencies;
- perform unrelated repair;
- release/tag/promote/merge default branch;
- force push.

Documentation/report-only commits are allowed after race-checking the remote branch.

If validation proves the repair itself still needs source changes, report `FAIL` or `REWORK_REQUIRED` with evidence. A separate source-repair task must then be opened by ChatGPT.

## Successor gate

Even Task-168 `PASS` does not authorize install-over or Dashboard semantic testing.

ChatGPT must review the Task-168 verification packet. If Task-167 is then accepted, the next authorized step is a separate Windows install-over/provenance/health checkpoint for the exact repaired candidate. Only after that checkpoint is accepted may a later exactly-one-Send Dashboard reacceptance be opened.
