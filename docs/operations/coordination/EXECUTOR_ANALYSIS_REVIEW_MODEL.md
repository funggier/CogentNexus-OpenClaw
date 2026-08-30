# Executor-Heavy Analysis and Reviewer-Light Coordination Model

Updated: 2026-08-31 ICT

## Purpose

Reduce ChatGPT coordination-context consumption without reducing evidence quality or safety. Hermes/Codex becomes the default primary technical investigator and implementer for delegated CogentNexus-OpenClaw tasks. ChatGPT remains coordinator, authority-boundary designer, evidence reviewer, and final disposition owner.

This policy applies to future delegated work after its publication. It does not retroactively redefine evidence already produced by historical tasks.

## Core model

```text
Human intent
    -> ChatGPT frames objective / acceptance contract / safety boundary
    -> Hermes/Codex performs primary investigation + implementation + validation
    -> Hermes/Codex publishes evidence-rich report + verification packet
    -> ChatGPT performs targeted evidence review, not full reconstruction by default
    -> ACCEPT / REWORK / BLOCKED + successor task
```

The goal is not to reduce rigor. The goal is to move first-pass technical depth to the executor and make the reviewer consume a compact, auditable interface.

## Default technical ownership

For a delegated task, Hermes/Codex should normally own the complete technical loop that the task authorizes:

- fresh remote-state synchronization and authority verification;
- repository/source inspection;
- root-cause investigation;
- external/upstream source inspection when relevant;
- alternative evaluation and technical recommendation;
- TDD RED -> minimal fix -> GREEN when production/source changes are required;
- repository tests, build/package/plugin validation;
- CI/workflow triggering and exact-SHA evidence collection;
- machine/local/live execution when authorized;
- risk, crash-window, compatibility, and residual-uncertainty analysis;
- production/source commits and normal pushes within task scope;
- a detailed completion report that is sufficient for reviewer verification.

ChatGPT does not need to repeat those activities merely because it is the final reviewer.

## ChatGPT ownership

ChatGPT normally owns:

- converting human intent into a bounded task;
- defining success criteria, hard fences, irreversible-action gates, and evidence expectations;
- selecting the executor and setting task scope;
- reading the executor's final report and verification packet;
- checking current remote GitHub state before review/disposition;
- targeted verification of critical claims and any claims with high uncertainty or high impact;
- expanding review depth only when report quality, contradiction, risk, or evidence gaps require it;
- publishing ACCEPT / REWORK / BLOCKED reviews;
- defining and opening successor tasks;
- changing standing coordination policy.

ChatGPT may still execute technical work directly when the human explicitly requests it, when executor access is unavailable, or when a narrow reviewer-side probe is cheaper than a rework cycle. Direct execution is an exception, not the default lane for a delegated technical task.

## No-reconstruction-by-default rule

If the executor report satisfies `EXECUTOR_REPORT_CONTRACT.md`, ChatGPT should not reconstruct the entire investigation from scratch.

Reviewer depth should escalate progressively:

1. **Level 1 — Contract review:** verify task identity, lineage, disposition, acceptance matrix, residual uncertainty, and hard-fence statement.
2. **Level 2 — Targeted evidence verification:** independently inspect the critical claims listed in the verification packet using exact commits, diffs, workflow runs, hashes, logs, or other durable evidence.
3. **Level 3 — Focused technical expansion:** inspect surrounding implementation/source only where a claim is surprising, high-risk, weakly evidenced, or contradictory.
4. **Level 4 — Full reconstruction:** repeat the broader investigation only when the report cannot support a safe disposition, contradictory evidence appears, or the failure mode is severe enough to justify it.

Do not jump to Level 4 merely because source and CI are accessible to ChatGPT.

## Evidence-rich, reasoning-light reporting

Executors must provide technical rationale sufficient to audit decisions, but must not dump private chain-of-thought. Reports should state:

- facts observed;
- evidence references;
- causal conclusions;
- alternatives materially considered;
- why the chosen action was preferred;
- uncertainty and risk;
- what remains unproven.

This gives ChatGPT enough information to validate the conclusion without requiring the executor's hidden reasoning trace.

## Review trust model

An executor report is not accepted merely because Hermes/Codex says PASS. The report is a structured claim set.

ChatGPT must independently verify at least the task's critical claims, including as applicable:

- authoritative branch/HEAD lineage;
- exact production/source changes;
- RED/GREEN evidence;
- exact-SHA CI results;
- immutable artifact/package provenance;
- live-machine state when acceptance depends on it;
- absence of prohibited semantic or destructive side effects;
- any claim whose failure could cause duplicate output, data loss, unsafe lifecycle mutation, or invalid release acceptance.

The reviewer verifies claims, not every intermediate action.

## Executor autonomy inside a task

Within the task's hard fence, Hermes/Codex may investigate more deeply than the initial task wording anticipated when required to reach a justified disposition. It may add narrowly necessary tests/evidence and may choose among safe implementation details.

It must not broaden authority into:

- unrelated product changes;
- new destructive/live actions;
- semantic sends not explicitly authorized;
- dependency/OpenClaw upgrades unless explicitly authorized;
- release/promotion/default-branch operations;
- a successor task.

If resolving a problem requires broader authority, report `BLOCKED` or `REWORK_REQUIRED` with the exact requested scope expansion.

## Task-writing rule

Future tasks should avoid prescribing every investigation step when the executor can safely determine those steps itself. Each task should instead emphasize:

- objective;
- accepted starting state/candidate;
- success criteria;
- hard fences;
- mandatory evidence;
- task-specific high-risk invariants;
- required report path.

The standing report contract supplies the general analysis/report requirements, reducing repeated task text.

## Context-efficiency rule

Do not copy large source excerpts, logs, workflow outputs, or historical narratives into coordination files unless they are required to establish a claim. Prefer:

- exact SHA/run/artifact identifiers;
- concise summaries;
- line/function/file pointers;
- hashes;
- compact acceptance matrices;
- local evidence path + hash when raw evidence cannot be committed.

Reports may be detailed, but should be information-dense and reviewer-oriented rather than chronological transcripts.

## Failure handling

A report must not convert uncertainty into PASS.

Use:

- `PASS` when all required acceptance criteria are evidenced;
- `FAIL` when a defect or violated criterion is demonstrated;
- `BLOCKED` when required proof/action cannot be obtained within authority;
- `REWORK_REQUIRED` when the task can continue safely but the current implementation/evidence is insufficient and a repair iteration is required.

ChatGPT maps those results to the durable review state and next task.

## Relationship to existing coordination files

This document is the standing role model. It is complemented by:

- `EXECUTION_OWNERSHIP.md` — ownership, escalation, race prevention, remote authority;
- `EXECUTOR_REPORT_CONTRACT.md` — mandatory executor analysis/report interface;
- `CODEX_BOOTSTRAP.md` — Hermes/Codex startup behavior;
- `README.md` — coordination overview;
- `ACTIVE.md` / `STATUS.md` — current task authority only.

When older language conflicts with this policy after this policy's publication, the executor-heavy/reviewer-light model governs future delegated tasks unless an active task explicitly overrides it.
