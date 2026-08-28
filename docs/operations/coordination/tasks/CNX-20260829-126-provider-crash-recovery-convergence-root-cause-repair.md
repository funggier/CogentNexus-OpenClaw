# CNX-20260829-126 — Provider-Crash Recovery Convergence Root-Cause Repair

- Status: `READY_FOR_HERMES`
- Execution mode: `REPOSITORY_SOURCE_TDD_REPAIR`
- Owner / independent reviewer: ChatGPT
- Executor: Hermes/Codex after operator continuation
- Date: 2026-08-29 ICT
- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`

## Purpose

Diagnose and repair the exact provider-crash durable-convergence failure proven by Task 125.

This task is repository/source/test/CI work plus read-only inspection of retained Task-125 evidence. It authorizes **no live Windows lifecycle or recovery disruption**.

## Accepted failure boundary

Task-125 report:

`docs/operations/coordination/reports/CNX-20260829-125-v093-recovery-reality-interactive-confirmation-acceptance.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260829-125-v093-recovery-reality-interactive-confirmation-acceptance-review.md`

Accepted verdict:

`ACCEPTED FAIL — GATEWAY-CRASH RECOVERY PASSED, BUT PROVIDER-CRASH RECOVERY FAILED TO REACH THE REVIEWED DURABLE-READY CONTRACT WITHIN 420 SECONDS; SOURCE/HARNESS ROOT-CAUSE DIAGNOSIS IS REQUIRED BEFORE ANY REPLAY.`

Task-125 exact evidence:

- log: `C:\Users\CDQ-P\Downloads\CNXCLAW_V093_OLLAMA_RECOVERY_V3_20260829-062300.txt`;
- JSON: `C:\Users\CDQ-P\Downloads\CNXCLAW_V093_OLLAMA_RECOVERY_V3_20260829-062300.json`;
- exact frozen source candidate: `01d08cd7c82f542c821e3a60f7fffa036efb1d75`;
- exact recovery harness blob: `80da4a2a23f5b5e936d725dcbd695a631bad1cb6`.

## Fixed facts

Task 125 proved:

- true PTY and interactive confirmation were correct;
- `explicit-disruptive-confirmation=PASS`;
- recovery harness prechecks passed;
- `gateway-crash` scenario passed;
- `provider-crash` was injected;
- provider recovery did not satisfy durable convergence within `420` seconds;
- harness-owned cleanup subsequently restored healthy managed state;
- operator-stop did not run;
- no recovery replay occurred.

Do not reclassify this as the old `$args`, TUI, UTF-16, or confirmation problem.

## Durable convergence predicate to diagnose

For provider-crash, the exact harness requires all of these simultaneously:

1. host mode == `managed`;
2. host selected provider == `ollama`;
3. provider status selected provider == `ollama`;
4. recovery verdict == `READY`;
5. exactly one `Provider event adapter` check row and `details.expected == false`;
6. Gateway listener present;
7. Ollama listener present;
8. exactly one `Provider recovery incident` row and `details.circuitOpen == false`.

The retained observation series is authoritative. Identify exactly which field(s) failed and how they evolved over time.

## Phase A — fresh repository and evidence reconciliation

Before source edits:

- fetch current branch HEAD and `ACTIVE.md` / `STATUS.md`;
- confirm Task 126 remains authoritative;
- confirm no new live acceptance/recovery task supersedes it;
- preserve the Task-125 one-shot ledger;
- read the retained Task-125 JSON/log **read-only**;
- do not invoke `cnxclaw` lifecycle commands, recovery disruption, process kill, provider mutation, or cleanup.

A read-only current-status probe is allowed only if necessary to confirm the harness cleanup left a safe state; it must not be used to normalize or repair anything.

## Phase B — exact observation-series diagnosis

From the Task-125 JSON, extract and report:

- first `converge-provider-after` observation;
- last observation;
- every change-point where any predicate field changed;
- count/duration of each distinct non-ready state;
- Gateway and Ollama listener/PID changes;
- provider incident row across the window;
- provider event-adapter row across the window;
- recovery verdict across the window;
- host/provider selected state across the window.

Explicitly answer:

- Did the Ollama listener recover before durable convergence polling? 
- Did Gateway remain/recover healthy?
- Did provider selection return to Ollama?
- Was the provider recovery incident absent, duplicated, circuit-open, or stale?
- Was `Provider event adapter.details.expected` stale or incorrect?
- Was `recovery.verdict` blocked by another check not represented in the harness predicate?
- Did the system eventually recover only after the 420-second fuse / cleanup-start, and if so what transition caused it?

Do not infer from the final cleanup state what happened inside the failed 420-second window.

## Phase C — source authority trace

Trace the exact owning code for every failed predicate through the frozen/current source, including as applicable:

- provider crash detection / process-health observation;
- provider restart/recovery scheduling;
- provider recovery incident persistence and circuit state;
- provider event adapter expected/actual semantics;
- recovery-check verdict composition;
- supervisor/host state transitions;
- stale incident/event clearing after successful provider restart;
- timing/backoff/fuse logic.

Apply the responsibility-locality invariant: fix the layer that owns the stale/incorrect state. Do not move provider policy into installer or unrelated layers.

## Phase D — TDD RED

Before production-source modification, add the smallest deterministic regression test that reproduces the Task-125 evidence-derived failure.

Requirements:

- RED must fail against the current product/source contract for the same reason observed live;
- the test must assert the state transition/postcondition, not merely grep source text;
- do not encode an arbitrary 420-second sleep;
- model the relevant crash/restart/recovery sequence deterministically with fake time/process/listener/provider state where practical;
- if the defect is in the recovery harness predicate rather than product state, the RED test must demonstrate that the harness rejects a state that the product contract defines as recovered;
- capture RED commit SHA and exact failing output in the report.

Do **not** simply increase `RecoveryFuseSeconds` unless retained evidence proves the product contract intentionally converges later and the reviewed timeout alone is incorrect.

## Phase E — minimal responsibility-local repair

Apply the smallest root-cause fix.

Possible categories are illustrative, not assumptions:

- clear/close a provider recovery incident when actual provider recovery succeeds;
- update event-adapter expected state when the provider returns;
- repair supervisor convergence/state reconciliation;
- repair recovery verdict composition;
- repair the reviewed recovery harness predicate if product state is actually coherent and the predicate is stale/incorrect.

Do not make broad refactors unrelated to the evidence.

## Phase F — validation

At minimum run:

- the new focused regression test;
- all provider/recovery/supervisor/check-system focused tests;
- full Python test suite;
- PowerShell syntax/AST checks for any modified `.ps1`;
- `sh -n` for any modified shell scripts;
- `python -m compileall` for modified Python surfaces;
- `git diff --check`;
- plugin tests;
- plugin validation/pack proof;
- evaluation suite;
- npm audit according to repository contract.

Require GREEN before candidate advancement.

## Phase G — exact-SHA CI and package proof

Push the repaired source candidate and require the repository's exact-SHA workflows to pass, including the established validation, installer pack smoke, PS5.1 acceptance smoke, and any recovery-specific smoke affected by this change.

Record:

- exact source SHA;
- all relevant workflow run IDs/conclusions;
- artifact ID/name/digest;
- package ZIP/tar.gz hashes;
- payload count;
- payload/plugin fingerprint.

If CI/package proof is not complete: `BLOCKED`, not candidate-ready.

## Phase H — report and stop

Publish exactly:

`docs/operations/coordination/reports/CNX-20260829-126-provider-crash-recovery-convergence-root-cause-repair.md`

Report must include:

- retained Task-125 evidence analysis;
- exact failed predicate(s) and change-point timeline;
- deepest proven root cause;
- owning source files/functions;
- RED commit/output;
- repair commit(s);
- focused/full test results;
- exact final candidate SHA;
- exact-SHA CI runs;
- package proof/hashes/fingerprint;
- explicit statement that no live lifecycle/recovery replay occurred;
- verdict `PASS`, `FAIL`, or `BLOCKED`.

Then stop for independent ChatGPT review. Do not auto-open a new live Windows acceptance task.

## Hard fence

Task 126 does **not** authorize:

- any live provider crash injection;
- any recovery-suite replay;
- install/install-over/reset/uninstall/reinstall;
- standalone stop/start/restart;
- live provider/OpenClaw configuration changes;
- process kill/reboot;
- manual cleanup/normalization of the Windows machine;
- credential/secret access;
- Dashboard semantic Send;
- merge/tag/GitHub Release;
- force push.

The final Dashboard durable-delivery acceptance remains prohibited until a repaired exact candidate later passes real-Windows recovery acceptance.