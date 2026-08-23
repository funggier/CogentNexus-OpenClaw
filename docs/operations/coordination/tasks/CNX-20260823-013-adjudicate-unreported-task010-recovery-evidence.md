# CNX-20260823-013 — Adjudicate Existing Unreported Task 010 Recovery Evidence

Status: READY  
Owner: ChatGPT  
Executor: Codex  
Priority: current evidence gate  
Predecessor: `CNX-20260823-012` (`ACCEPT`)  
Execution mode: `AUTO`

## Objective

Adjudicate the already-existing Task 010 v3 recovery TXT/JSON evidence without repeating or extending any runtime action.

Determine exactly which baseline, Gateway-crash, Ollama/provider-crash, and intentional stop/start steps actually executed; which passed, failed, or were skipped; whether every disruptive target satisfied exact-PID safety; and what the provider durable-`READY` convergence timeout proves.

This is offline evidence review only. It does not authorize a harness, scenario, confirmation, process query, process kill, CogentNexus/OpenClaw/Ollama command, checkout operation, cleanup, install, reset, uninstall, or reinstall.

## Duplicate-execution fence

Before any local evidence read, fetch the branch and check for:

`docs/operations/coordination/reports/CNX-20260823-013-adjudicate-unreported-task010-recovery-evidence.md`

If it exists, perform no local observation or other action. Stop awaiting ChatGPT review.

Confirm `ACTIVE.md` names this exact task with `READY_FOR_CODEX` and `AUTO`.

## Exact evidence in scope

Read only these two already-hashed files:

1. `C:\Users\CDQ-P\Downloads\CNX_V093_OLLAMA_RECOVERY_V3_20260823-003808.txt`
   - expected SHA256: `FBA88FF64D236DF58C9A287BDE7B996D9D35A1D71E3976D7FF1C177553F9705F`
   - expected bytes: `1802394`
2. `C:\Users\CDQ-P\Downloads\CNX_V093_OLLAMA_RECOVERY_V3_20260823-003808.json`
   - expected SHA256: `4F86AA70B88129E9CCB258CEB780B5243D9B0E515362BEC69A40E4F099A90D1F`
   - expected bytes: `5900085`

First verify path, byte size, and SHA256 byte-for-byte. If either differs, report `BLOCKED` and stop without substituting another evidence file.

The Task 010 collision directories and report worktree are out of scope. Do not inspect them again.

## Required read-only adjudication

Record exact evidence-reading commands and exit codes. Parse only task-relevant fields and matching log passages.

### Provenance and invocation

Record:

- evidence schema version;
- suite start/completion/failure timestamps and duration;
- exact tested source HEAD, branch, version, harness path, harness Git blob/SHA256/bytes when recorded;
- invocation arguments in a safe redacted form sufficient to prove `Scenario all`, `RunDisruptive`, output paths, and explicit confirmation;
- whether lowercase `y` was entered and at what gate;
- final suite result and exact error class/message.

Do not expose credentials, tokens, unrelated command lines, chat content, or user data.

### Scenario/step matrix

For every baseline, Gateway-crash, provider-crash, operator-stop, operator-start, cleanup, and final-health step present in the evidence, record:

- executed, skipped, or not represented;
- start/end timestamps;
- PASS/FAIL/BLOCKED result;
- exact durable evidence fields supporting the result;
- listener PIDs before/after where recorded;
- recovery verdict progression where recorded;
- whether a later cleanup action changed state after the scenario failure.

Do not infer PASS from a scenario name merely appearing in the JSON.

### Exact-PID and no-tree-kill safety

For every recorded disruptive injection, determine from the evidence:

- listener endpoint and resolved target PID;
- validated executable/process identity;
- harness PID/ancestor/protected-process rejection gates;
- persisted active-operation/target evidence before injection;
- exact kill command/action and exit status;
- explicit absence or presence of a process-tree kill;
- replacement listener PID and identity when observed.

If the evidence cannot prove a safety gate, mark it unproven; do not fill gaps from prior reports.

### Provider incident and convergence

For the Ollama/provider scenario, record the exact timeline and distinguish:

- listener crash and replacement;
- provider incident opened/advanced/cleared state;
- runtime/listener health;
- durable recovery verdict and active marker/operation;
- stable-success observations;
- timeout fuse;
- final cleanup and final `READY` state.

Classify the provider failure as exactly one:

- `RUNTIME_RECOVERY_FAILED`
- `RUNTIME_RECOVERED_DURABLE_STATE_STUCK`
- `HARNESS_ASSERTION_OR_TIMING_DEFECT`
- `INSUFFICIENT_EVIDENCE`

Explain the evidence boundary. A timeout is an observation fuse, not recovery authority.

### Overall adjudication

Return exactly one primary adjudication:

- `PARTIAL_RECOVERY_EVIDENCE_ACCEPTABLE`: one or more scenarios are independently proven, while later failure/skips remain;
- `NO_PROCESS_RECOVERY_SCENARIO_ACCEPTABLE`: evidence cannot safely prove any scenario;
- `SAFETY_INVARIANT_VIOLATION`: any process-tree kill, invalid target, protected target, missing required pre-kill persistence, or unsafe action is proven;
- `EVIDENCE_CORRUPT_OR_MISMATCHED`: expected identity/hash/size differs.

List each process-recovery gate separately as `PROVEN`, `FAILED`, `SKIPPED`, or `UNPROVEN`:

- healthy MANAGED/Ollama baseline;
- Gateway exact-PID crash and automatic runtime recovery;
- Gateway durable-state convergence;
- Ollama exact-PID listener crash and runtime recovery;
- provider incident lifecycle;
- provider durable-state convergence;
- intentional `cnx stop` remains stopped;
- explicit `cnx start` returns to healthy MANAGED state;
- final cleanup/health.

## Prohibited actions

- no recovery harness, scenario, parser, `-SyntaxOnly`, CI wait, or Windows preflight;
- no confirmation input;
- no live process enumeration, kill, suspend, restart, window close, or app restart;
- no `cnx`, OpenClaw, Ollama, network-listener, service, or Scheduled Task command;
- no clone/worktree/checkout creation, inspection, cleanup, repair, prune, reset, reuse, archive, rename, or deletion;
- no evidence move, rename, deletion, modification, or new evidence search;
- no chat/project/session/cache access or deletion;
- no install, reset, uninstall, reinstall, merge, tag, release, package change, or force-push.

## Acceptance criteria

PASS requires:

- byte-for-byte evidence identity verification;
- complete provenance/invocation accounting;
- a step-by-step scenario matrix that does not convert skipped or merely named scenarios into PASS;
- exact-PID/no-tree-kill safety accounting for every recorded injection;
- provider incident/convergence classification;
- one primary overall adjudication;
- explicit proven/failed/skipped/unproven gate list;
- explicit remaining uncertainty and narrow recommended next step.

This task may accept existing partial evidence but may not authorize or perform another disruptive run.

## Report

Write only:

`docs/operations/coordination/reports/CNX-20260823-013-adjudicate-unreported-task010-recovery-evidence.md`

Include:

- Task ID, start HEAD, ACTIVE verification;
- exact commands and exit codes;
- evidence identity table;
- provenance/invocation table;
- scenario/step matrix;
- exact-PID safety table;
- provider incident/convergence timeline and classification;
- primary overall adjudication;
- gate-by-gate verdicts;
- safety accounting;
- unproven items;
- narrow recommended next step.

Only this matching report may change. Commit message must begin:

`report: CNX-20260823-013`

Never force-push. Stop after publishing the report.
