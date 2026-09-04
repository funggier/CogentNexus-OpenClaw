# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `TASK253_TASK252_STREAMING_DIAGNOSTIC_RUNNER_TDD_QUALIFICATION`
Current disposition: `TASK252_ACCEPTED_BLOCKED__SCHEDULER_TIMEOUT_AND_BUFFERED_RUNNER_EVIDENCE_LOSS_PROVEN__STREAMING_RUNNER_TDD_REQUIRED`
Task ID: `CNX-20260905-253`
Parent task: `CNX-20260905-252`
Parent umbrella: `CNX-20260831-188`
Updated: 2026-09-05 ICT
Executor: Hermes / repository-capable implementation agent
Coordinator / independent reviewer: ChatGPT

## Accepted Task-252 result

Independent review verdict:

`ACCEPT_BLOCKED_TASK251_CHILD_STAGE_UNPROVEN__SCHEDULER_TIMEOUT_AND_BUFFERED_RUNNER_EVIDENCE_LOSS_PROVEN__STREAMING_DIAGNOSTIC_RUNNER_TDD_REQUIRED`

Reviewed Task-252 report HEAD:

`c1649f064e22492ac324a1f137fc109cff680c62`

Independent review commit:

`9318008a9549a264aa28491b0d4d264750a9e168`

Task252 proved:

```text
Task251 scheduler termination = PT45M execution limit + AllowHardTerminate + 0x41306
Task251 runner evidence loss = buffered ReadToEnd()/post-completion writes
Task251 runner SHA-256 = 0c2da0cb5877ca9493e4921c3a7b5492dd884841a2bd68c3fb63032b6e42eb98
last installer stage = unproven
underlying child stall cause = unproven
Task252 live/product/semantic mutations = 0
```

The Task251 installer MUST NOT be retried from this evidence. Increasing `ExecutionTimeLimit` is not authorized as a fix.

## Active Task 253

Execute:

`docs/operations/coordination/tasks/CNX-20260905-253-task252-streaming-diagnostic-runner-tdd-qualification.md`

Required flow:

```text
fresh GitHub authority
-> inspect retained buffered-runner contract and repo conventions
-> TEST-ONLY RED
-> prove live stdout/stderr visibility requirement while synthetic child is still alive
-> prove forced outer-runner termination must preserve already-emitted output
-> minimal repository-owned Windows PowerShell 5.1 streaming runner
-> focused GREEN for streaming/nonzero/launch-failure/argument-binding cases
-> full GREEN
-> exact final candidate + runner SHA + installer SHA + plugin fingerprint
-> exact-SHA Actions GREEN
-> report
-> STOP for independent review
```

Preferred production path:

`scripts/manifest-streaming-runner.ps1`

Task253 is repository/test-only. Synthetic child processes are allowed only for runner qualification and MUST NOT call the installer, OpenClaw/CogentNexus product runtime, Gateway, or production databases.

## Hard fences

```text
live scripts/install.ps1 invocations = 0
live installer Scheduled Task registrations/starts = 0
rollover prepare/finalize invocations = 0
live plugin/retired-tree/rollover-backup mutation = 0
controller/Gateway/provider/model/DB mutation = 0
Dashboard/Discord/API semantic sends = 0
recovery replay/resend = 0
release/tag mutation = 0
force push/history rewrite = 0
```

Repository source/test edits limited to the streaming diagnostic runner and its qualification coverage are authorized.

## Stop boundary

Hermes must publish:

`docs/operations/coordination/reports/CNX-20260905-253-task252-streaming-diagnostic-runner-tdd-qualification.md`

Then STOP for independent ChatGPT review. Even on PASS, live installer retry and semantic acceptance remain unauthorized until a separate successor task.
