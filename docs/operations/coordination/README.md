# CogentNexus Coordination Layer

This directory is the GitHub-based durable handoff surface between ChatGPT, Hermes/Codex, and the human operator.

GitHub remote coordination state is authoritative. Local execution is allowed only within the exact permissions of the active task.

Standing model:

- [`EXECUTOR_ANALYSIS_REVIEW_MODEL.md`](EXECUTOR_ANALYSIS_REVIEW_MODEL.md) — executor-heavy / reviewer-light role architecture;
- [`EXECUTION_OWNERSHIP.md`](EXECUTION_OWNERSHIP.md) — ownership, authority, race prevention, and live-action boundaries;
- [`EXECUTOR_REPORT_CONTRACT.md`](EXECUTOR_REPORT_CONTRACT.md) — mandatory executor analysis/evidence interface;
- [`CODEX_BOOTSTRAP.md`](CODEX_BOOTSTRAP.md) — Hermes/Codex startup behavior;
- [`PROBLEM_LOOP.md`](PROBLEM_LOOP.md) — blocker handling;
- [`SIGNALS.md`](SIGNALS.md) — minimal operator signals;
- [`WATCH_MODE.md`](WATCH_MODE.md) — optional continuous pickup.

## Canonical current contract

- Repository: `funggier/CogentNexus-OpenClaw`
- Current stabilization branch: `agent/v0.9.3-full-stabilization`
- Active authority: current remote `ACTIVE.md` + `STATUS.md`
- Executor role: `Hermes/Codex`
- Manual trigger: `ต่อ`
- ChatGPT owns task framing, reviews, `ACTIVE.md`, `STATUS.md`, and successor authorization
- Hermes/Codex owns primary technical investigation, implementation, validation, evidence packaging, and matching delegated reports
- Human operator remains final authority

Do not rely on a historical READY-state token copied into older docs. The exact current state and execution mode come from remote `ACTIVE.md` and `STATUS.md`.

## Intended loop

```text
Human intent
    ↓
ChatGPT defines objective + accepted starting state + success criteria + hard fences
    ↓
ChatGPT publishes delegated task
    ↓
Hermes/Codex synchronizes current remote GitHub truth
    ↓
Hermes/Codex performs primary technical investigation
(source / upstream / root cause / TDD / implementation / CI / local-live proof as authorized)
    ↓
Hermes/Codex publishes evidence-rich report
+ acceptance matrix
+ reviewer verification packet
    ↓
ChatGPT verifies critical claims using targeted evidence checks
    ↓
Need deeper review?
    ├─ no  → ACCEPT / next task
    └─ yes → focused expansion or REWORK/BLOCKED
```

The default is **not** for ChatGPT to reconstruct the executor's investigation from scratch.

## Ownership model

### ChatGPT owns

- translating operator intent into a bounded task;
- accepted parent/candidate selection;
- success criteria and evidence thresholds;
- hard fences and semantic/destructive-action gates;
- `tasks/*.md`;
- `reviews/*.md`;
- `ACTIVE.md` and `STATUS.md`;
- targeted verification of critical executor claims;
- deeper reviewer investigation only when evidence or risk requires it;
- final ACCEPT / REWORK / BLOCKED / SUPERSEDED disposition;
- successor-task authorization;
- standing coordination policy.

### Hermes/Codex owns for delegated tasks

- remote-state synchronization;
- repository/source/upstream investigation;
- root-cause analysis;
- source/test/config/installer implementation within task scope;
- TDD and regression coverage;
- build/package/plugin/schema validation;
- GitHub Actions exact-SHA verification;
- Windows/local/live proof when explicitly authorized;
- risk, crash-window, compatibility, and residual-uncertainty analysis;
- implementation commits/pushes within scope;
- matching `reports/*.md` using `EXECUTOR_REPORT_CONTRACT.md`.

### Human operator

- provides intent and priorities;
- approves policy or disruptive boundaries when needed;
- triggers authorized executors;
- remains final authority.

The human should not be used as a courier for task bodies, logs, or routine synchronization.

## Reviewer-light rule

A compliant executor report should let ChatGPT begin from a small verification packet rather than rereading the entire codebase/history.

Review depth escalates only as necessary:

1. contract/lineage review;
2. critical-claim spot checks;
3. focused technical expansion;
4. full reconstruction only for insufficient/contradictory/high-risk evidence.

PASS is never accepted solely because the executor says PASS. The reviewer independently verifies the claims that determine acceptance.

## Report contract

Future delegated reports follow [`EXECUTOR_REPORT_CONTRACT.md`](EXECUTOR_REPORT_CONTRACT.md).

Required high-value elements include:

- objective and acceptance contract;
- exact starting authority/HEAD/candidate lineage;
- investigation and causal conclusion;
- material alternatives when relevant;
- implementation/action summary;
- risk and residual uncertainty;
- RED/minimal fix/GREEN or equivalent preflight/action/postflight evidence;
- criterion-by-criterion acceptance matrix;
- exact commits/runs/hashes/fingerprints/evidence paths;
- contradictions/anomalies;
- hard-fence compliance;
- residual unproven items;
- **3-10 item reviewer verification packet**;
- recommended successor without self-authorizing it.

Reports should be information-dense, not chronological transcripts. Prefer exact evidence pointers over large copied logs/source.

## Executor autonomy and hard fences

Within an authorized task, Hermes/Codex may choose the investigation sequence, inspect relevant additional source, add narrowly necessary tests, and choose safe implementation details needed to satisfy the acceptance contract.

It may not infer authority for unrelated product changes, destructive/live mutations, semantic Sends, dependency/OpenClaw upgrades, release/promotion, default-branch merge, force push, or successor tasks.

If broader authority is needed, publish a blocker/rework report stating the exact missing authorization.

## Task identity

Every delegated task has a stable ID such as:

```text
CNX-20260831-166
```

The same task identity is used across `tasks/`, `reports/`, and `reviews/`.

Historical tasks/reports remain governed by the contract under which they were produced; they do not need rewriting solely because the standing model changed.

## Handoff state model

Exact tokens may vary by active task, but the conceptual state is:

```text
READY executor handoff
    ↓ manual `ต่อ` or authorized auto pickup
EXECUTING
    ↓ matching report pushed
REPORT READY FOR REVIEW
    ↓ ChatGPT targeted review
ACCEPTED / REWORK / BLOCKED
    ↓
next authorized task or closure
```

`ACTIVE.md` is the single pointer to the current delegated executor authority.

## Remote authority rule

Hermes/Codex must re-read the current remote branch for every execution signal. A local checkout is only a working copy.

Before work and before pushes:

- verify remote HEAD;
- read current remote `ACTIVE.md`, `STATUS.md`, task, and report state;
- race-check concurrent changes;
- prefer fresh worktree/clone when local state is uncertain;
- never reset away unknown work merely to synchronize;
- never force-push coordination history.

## Minimal human signals

See [`SIGNALS.md`](SIGNALS.md).

`ต่อ` means synchronize current remote truth and execute only the exact authorized delegated task. `สถานะ` is read-only coordination status. `หยุด` means do not begin a new task.

## Problem resolution

See [`PROBLEM_LOOP.md`](PROBLEM_LOOP.md).

Do not convert a safe stop into a silent dead end. The executor should analyze the blocker, preserve evidence, state the smallest missing authority or repair needed, publish the matching report, and stop for ChatGPT review.

## Review contract

ChatGPT review files use durable dispositions such as:

```text
ACCEPT
REWORK
BLOCKED
SUPERSEDED
```

The review records reviewer identity and the exact critical evidence checked. If ChatGPT also executed the reviewed technical work, it must be labeled `ChatGPT self-review`, never independent review.

## Standing executor stop rule

After publishing the matching report, Hermes/Codex stops that run. It may recommend the next action but must not invent, open, or execute the successor task until ChatGPT publishes new authority.

## Relationship to `docs/operations`

This directory is the coordination/handoff layer. Historical evidence remains historical. Accepted technical truth comes from source, tests, immutable evidence, machine observations where required, and explicit review/acceptance gates.
