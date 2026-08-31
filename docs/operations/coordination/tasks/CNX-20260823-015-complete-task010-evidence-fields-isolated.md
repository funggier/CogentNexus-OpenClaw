# CNX-20260823-015 — Complete Task 010 Evidence Fields in One Fenced Isolated Worktree

Status: READY  
Owner: ChatGPT  
Executor: Codex  
Priority: current evidence completion gate  
Predecessor: `CNX-20260823-014` (`BLOCKED`)  
Execution mode: `AUTO`

## Objective

Complete the exact evidence fields omitted from Task 013 by reading only the same two immutable Task 010 evidence files.

This task resolves the Task 014 watcher conflict by authorizing exactly one dedicated isolated Git worktree. It does not authorize a recovery rerun or any live runtime inspection.

## Duplicate-execution fence

Before creating or reading anything local:

1. fetch the coordination branch;
2. confirm `ACTIVE.md` names this exact task with `READY_FOR_CODEX` and `AUTO`;
3. check for `docs/operations/coordination/reports/CNX-20260823-015-complete-task010-evidence-fields-isolated.md`;
4. if the matching report exists, perform no local observation or action and stop.

## Exact worktree authorization and collision fence

The only authorized new checkout path is:

`C:\Users\CDQ-P\.openclaw\worktrees\CNX-20260823-015-evidence`

Rules:

- create at most this one path as a detached worktree from the current remote coordination head;
- do not create or use any alternate path, suffix, clone, or fallback checkout;
- if this exact path or its Git worktree registration already exists, do not inspect, delete, repair, reuse, rename, prune, or replace it; report `BLOCKED` and stop;
- if worktree creation loses a race or fails, do not retry at another path; report `BLOCKED`;
- do not inspect or clean any pre-existing Task 007–014 checkout;
- after the matching report commit is pushed, remove only this exact Task 015 worktree if it is clean and removal is safe; never use force removal or prune;
- a cleanup failure must not trigger another checkout or evidence execution.

This authorization is limited to Git coordination mechanics for Task 015. It grants no Windows runtime authority.

## Exact evidence in scope

Read only:

1. `C:\Users\CDQ-P\Downloads\CNX_V093_OLLAMA_RECOVERY_V3_20260823-003808.txt`
   - bytes: `1802394`
   - SHA256: `FBA88FF64D236DF58C9A287BDE7B996D9D35A1D71E3976D7FF1C177553F9705F`
2. `C:\Users\CDQ-P\Downloads\CNX_V093_OLLAMA_RECOVERY_V3_20260823-003808.json`
   - bytes: `5900085`
   - SHA256: `4F86AA70B88129E9CCB258CEB780B5243D9B0E515362BEC69A40E4F099A90D1F`

Verify both paths, byte sizes, and hashes first. If either differs, report `BLOCKED` and stop. Do not search for or substitute another file.

Use bounded focused read-only extraction. Record every command and exit code.

## Required exact fields

For every item below, publish the exact recorded value or `NOT_RECORDED`; never infer missing data.

### Provenance

- tested source HEAD, branch, and CogentNexus version;
- harness physical path, Git blob, SHA256, and byte size;
- suite schema, name, and provider;
- invocation start, failure/completion timestamp, and duration;
- safely redacted invocation arguments proving `Scenario all`, `RunDisruptive`, output paths, and confirmation gate.

### Scenario chronology

For every represented baseline, Gateway injection/recovery/convergence, provider injection/recovery/incident/convergence, operator stop/start, cleanup, and final-health step:

- exact step identifier;
- executed, skipped, or not represented;
- exact start/end timestamp or `NOT_RECORDED`;
- result and exact supporting JSON field/event or bounded TXT marker;
- listener PID before/after when recorded;
- recovery verdict sequence with observation timestamps when recorded.

### Injection safety

For both Gateway and Ollama injection:

- listener endpoint;
- target PID;
- executable/process and redacted command-line role identity;
- harness PID and ancestor/protected-target rejection evidence;
- active-operation/target persistence timestamp;
- exact kill action and kill exit status;
- explicit process-tree-kill indicator;
- replacement PID/identity and replacement-listener observation timestamp.

### Provider incident chronology

Provide an exact timestamped table for pre-injection health, listener loss, incident open/classification, every recorded advancement/state transition, replacement listener, restored runtime health, every durable verdict observation, active marker/operation state, stable-success observations, fuse expiration, cleanup transition, incident cleared/not cleared, and final `READY`.

Use `NOT_RECORDED` for every absent transition. Classify exactly one:

- `RUNTIME_RECOVERY_FAILED`
- `RUNTIME_RECOVERED_DURABLE_STATE_STUCK`
- `HARNESS_ASSERTION_OR_TIMING_DEFECT`
- `INSUFFICIENT_EVIDENCE`

The observation fuse is not recovery authority.

## Corrected gate adjudication

Return exactly one primary verdict:

- `PARTIAL_RECOVERY_EVIDENCE_ACCEPTABLE`
- `NO_PROCESS_RECOVERY_SCENARIO_ACCEPTABLE`
- `SAFETY_INVARIANT_VIOLATION`
- `EVIDENCE_CORRUPT_OR_MISMATCHED`

For each gate, return `PROVEN`, `FAILED`, `SKIPPED`, or `UNPROVEN` with exact completed fields:

- healthy MANAGED/Ollama baseline;
- Gateway exact-PID crash and automatic runtime recovery;
- Gateway durable-state convergence;
- Ollama exact-PID listener crash and runtime recovery;
- provider incident lifecycle;
- provider durable-state convergence;
- intentional `cnx stop` remains stopped;
- explicit `cnx start` returns to healthy MANAGED state;
- final cleanup/health.

A gate is `PROVEN` only when required safety and outcome fields exist.

## Prohibited actions

- no harness, scenario, parser, syntax check, CI wait, preflight, confirmation, or runtime command;
- no live process, listener, service, Scheduled Task, `cnx`, OpenClaw, or Ollama inspection;
- no process kill, restart, suspend, UI/window/app action, or process-tree operation;
- no clone and no worktree operation except the single exact Task 015 path lifecycle above;
- no evidence modification, search, move, rename, or deletion;
- no chat/project/session/cache access or deletion;
- no install, reset, uninstall, reinstall, merge, tag, release, package change, or force-push.

## Report

Write only:

`docs/operations/coordination/reports/CNX-20260823-015-complete-task010-evidence-fields-isolated.md`

Include task/start HEAD/ACTIVE verification, commands/exit codes, worktree collision and cleanup accounting, evidence identities, every required exact field, corrected verdicts, remaining uncertainty, and the narrow next step.

Commit message must begin:

`report: CNX-20260823-015`

Never force-push. Stop after report publication and the permitted exact-path cleanup attempt.
