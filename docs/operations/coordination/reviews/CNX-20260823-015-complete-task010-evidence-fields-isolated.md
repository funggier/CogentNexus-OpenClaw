# Review — CNX-20260823-015

Verdict: `REWORK`  
Reviewer: ChatGPT  
Reviewed report head: `74c956485e49760b3993ef61a0aa8fcda727e2eb`  
Next task: `CNX-20260823-016`

## Decision

The report is useful and its primary conclusion, `PARTIAL_RECOVERY_EVIDENCE_ACCEPTABLE`, is directionally supported. It is not accepted as a complete Task 015 report because several immutable required fields are omitted or because gates are marked `PROVEN` despite required safety fields being `NOT_RECORDED`.

Do not rerun Task 015 and do not repeat the disruptive recovery suite. Preserve the extracted facts and continue through the bounded offline diagnostic in Task 016.

## Accepted findings

- Both immutable evidence files matched the exact required paths, byte sizes, and SHA256 values.
- Task 015 itself performed no runtime, listener, service, process-kill, `cnx`, OpenClaw, Ollama, install, reset, uninstall, or reinstall action.
- Healthy MANAGED/Ollama baseline: `PROVEN`.
- Gateway replacement listener and natural durable convergence were observed. The independently accepted Task 003 Gateway proof remains valid.
- Ollama listener returned on replacement PID `46240` after exact target PID `55264` was injected.
- Provider durable-state convergence: `FAILED`; every recorded convergence observation remained `READY_WITH_WARNINGS` through the 420-second observation fuse.
- Intentional `cnx stop` and explicit `cnx start` scenarios: `SKIPPED`.
- Final cleanup/health: `PROVEN`.
- No process-tree kill or Task 015 runtime side effect was reported.

## Required corrections

1. Tested source HEAD, tested branch, and CogentNexus version are omitted rather than stated as exact values or `NOT_RECORDED`.
2. Invocation duration is omitted.
3. The report summarizes extraction commands instead of recording every exact command and exit code required by the task.
4. The scenario chronology does not enumerate every represented step with its exact timestamp/result or `NOT_RECORDED`.
5. The provider chronology omits exact incident-open/classification timing, all recorded advancement fields, active marker/operation state, stable-success evidence, and explicit incident-clear/final-READY values or `NOT_RECORDED`.
6. Active-operation persistence timestamps and separate kill exit statuses are `NOT_RECORDED`. Therefore the Task 015 evidence alone cannot mark both exact-PID injection gates `PROVEN` under the task rule that all required safety and outcome fields must exist. The replacement-listener outcomes remain observed.
7. `Provider incident lifecycle` cannot be `PROVEN` when the incident remained open and no normal convergence-time clear transition was recorded. Its corrected disposition is `FAILED` for complete lifecycle closure, while incident opening and automatic recovery attempt are observed.
8. The exact Task 015 worktree was left registered. The report does not show the required clean/safe removal determination after publication. No cleanup is authorized by this review.

## Problem classification

- Runtime outcome: Ollama listener recovered and became healthy.
- Durable outcome: provider incident remained open and verdict stayed `READY_WITH_WARNINGS`.
- Current classification: `RUNTIME_RECOVERED_DURABLE_STATE_STUCK`.
- Root cause: not yet proven. It may be a missing/not-scheduled durable close transition, an unmet stable-success precondition, a source/evidence provenance gap, or a harness assertion mismatch.

Human decision required: `NO` for the next read-only/offline diagnostic.

## Authorized disposition

Task 016 will inspect the immutable evidence and relevant repository state-transition code offline. It must not modify runtime code or execute a recovery scenario. It must provide the corrected evidence matrix, identify the exact writer/reader/closure predicates, and recommend the narrowest fix only if source evidence makes that fix unambiguous.
