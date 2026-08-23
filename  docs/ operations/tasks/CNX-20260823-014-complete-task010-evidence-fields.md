# CNX-20260823-014 — Complete Exact Fields for Task 010 Evidence Adjudication

Status: READY  
Owner: ChatGPT  
Executor: Codex  
Priority: current evidence completion gate  
Predecessor: `CNX-20260823-013` (`REWORK`)  
Execution mode: `AUTO`

## Objective

Complete only the exact evidence fields omitted from the Task 013 report so ChatGPT can independently adjudicate the already-existing Task 010 recovery run.

Do not repeat, extend, or inspect any live runtime action. This task is a narrow read-only extraction from the same two immutable evidence files.

## Duplicate-execution fence

Before reading local evidence, fetch the branch and check for:

`docs/operations/coordination/reports/CNX-20260823-014-complete-task010-evidence-fields.md`

If it exists, perform no local observation or other action. Stop awaiting ChatGPT review.

Confirm `ACTIVE.md` names this exact task with `READY_FOR_CODEX` and `AUTO`.

## Exact evidence in scope

Read only:

1. `C:\Users\CDQ-P\Downloads\CNX_V093_OLLAMA_RECOVERY_V3_20260823-003808.txt`
   - bytes: `1802394`
   - SHA256: `FBA88FF64D236DF58C9A287BDE7B996D9D35A1D71E3976D7FF1C177553F9705F`
2. `C:\Users\CDQ-P\Downloads\CNX_V093_OLLAMA_RECOVERY_V3_20260823-003808.json`
   - bytes: `5900085`
   - SHA256: `4F86AA70B88129E9CCB258CEB780B5243D9B0E515362BEC69A40E4F099A90D1F`

Verify both identities first. If either mismatches, report `BLOCKED` and stop. Do not search for or substitute another file.

## Required exact-field completion

Use bounded, focused, read-only extraction and record exact commands and exit codes. Do not use a broad extraction that may time out when a narrower field query is possible.

### 1. Provenance

Publish the exact recorded value or `NOT_RECORDED` for each:

- tested source HEAD;
- tested branch;
- tested CogentNexus version;
- harness physical path;
- harness Git blob;
- harness SHA256;
- harness byte size;
- suite schema/name/provider;
- invocation start, failure/completion timestamp, and duration;
- safely redacted invocation arguments proving `Scenario all`, `RunDisruptive`, output paths, and confirmation gate.

Do not expose tokens, credentials, unrelated command lines, chat text, or user data.

### 2. Exact scenario/step chronology

For every represented baseline, Gateway injection/recovery/convergence, provider injection/recovery/incident/convergence, operator stop/start, cleanup, and final-health step, publish:

- exact step identifier;
- executed, skipped, or not represented;
- exact start and end timestamp, or `NOT_RECORDED`;
- result;
- exact supporting JSON field/event or bounded TXT marker;
- listener PID before/after when recorded;
- recovery verdict sequence and observation timestamps when recorded.

Scenario names alone are not execution evidence.

### 3. Injection safety completion

For each Gateway and Ollama injection, publish the exact recorded value or `NOT_RECORDED` for:

- listener endpoint;
- target PID;
- executable/process identity;
- command-line role identity in redacted form;
- harness PID and ancestor/protected-target rejection evidence;
- active-operation/target persistence timestamp before injection;
- exact kill action;
- kill exit status;
- explicit process-tree-kill indicator;
- replacement PID and identity;
- replacement-listener observation timestamp.

Do not infer an exit status or timestamp when absent.

### 4. Provider incident chronology

Publish an exact timestamped table for:

- pre-injection health;
- listener loss;
- incident ID/classification opened;
- each recorded incident advancement/state transition;
- replacement listener;
- restored runtime health;
- every durable recovery verdict observation;
- active marker/operation state;
- stable-success observations;
- fuse expiration;
- cleanup transition;
- incident cleared or not cleared;
- final `READY`.

For any transition not recorded, write `NOT_RECORDED`.

Then classify exactly one:

- `RUNTIME_RECOVERY_FAILED`
- `RUNTIME_RECOVERED_DURABLE_STATE_STUCK`
- `HARNESS_ASSERTION_OR_TIMING_DEFECT`
- `INSUFFICIENT_EVIDENCE`

The observation fuse is not recovery authority.

### 5. Corrected gate adjudication

Return exactly one:

- `PARTIAL_RECOVERY_EVIDENCE_ACCEPTABLE`
- `NO_PROCESS_RECOVERY_SCENARIO_ACCEPTABLE`
- `SAFETY_INVARIANT_VIOLATION`
- `EVIDENCE_CORRUPT_OR_MISMATCHED`

For each gate below, return `PROVEN`, `FAILED`, `SKIPPED`, or `UNPROVEN`, citing the exact completed fields:

- healthy MANAGED/Ollama baseline;
- Gateway exact-PID crash and automatic runtime recovery;
- Gateway durable-state convergence;
- Ollama exact-PID listener crash and runtime recovery;
- provider incident lifecycle;
- provider durable-state convergence;
- intentional `cnx stop` remains stopped;
- explicit `cnx start` returns to healthy MANAGED state;
- final cleanup/health.

A gate may be `PROVEN` only when the required safety and outcome fields are published. Otherwise use `UNPROVEN` even if Task 013 called it proven.

## Prohibited actions

- no harness, scenario, parser, `-SyntaxOnly`, CI wait, preflight, confirmation, or runtime command;
- no live process, listener, service, Scheduled Task, `cnx`, OpenClaw, or Ollama inspection;
- no process kill, restart, suspend, window/app action, or process-tree operation;
- no clone/worktree/checkout inspection, creation, cleanup, repair, prune, reset, reuse, archive, rename, or deletion;
- no evidence modification, move, rename, deletion, or new evidence search;
- no chat/project/session/cache access or deletion;
- no install, reset, uninstall, reinstall, merge, tag, release, package change, or force-push.

## Acceptance criteria

PASS requires both file identities to match and every required field above to contain either the exact evidence value or `NOT_RECORDED`, with a corrected adjudication that does not overstate missing fields.

This task cannot authorize another runtime experiment.

## Report

Write only:

`docs/operations/coordination/reports/CNX-20260823-014-complete-task010-evidence-fields.md`

Include:

- Task ID, start HEAD, ACTIVE verification;
- commands/exit codes;
- evidence identity;
- exact provenance table;
- exact step chronology;
- exact injection-safety tables;
- exact provider incident chronology and classification;
- corrected primary and gate verdicts;
- safety accounting;
- remaining uncertainty;
- narrow recommended next step.

Only this matching report may change. Commit message must begin:

`report: CNX-20260823-014`

Never force-push. Stop after publishing.
