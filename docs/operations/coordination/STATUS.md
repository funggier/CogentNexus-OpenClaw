# Coordination Channel Status

**State:** `READY_FOR_HERMES`  
**Execution mode:** `TASK253_TASK252_STREAMING_DIAGNOSTIC_RUNNER_TDD_QUALIFICATION`  
**Updated:** 2026-09-05 ICT  
**Transport:** GitHub repository / Actions authoritative; Task253 is repository/test-only streaming-runner TDD; live installer retry and semantic acceptance remain unauthorized  
**Active task:** `CNX-20260905-253`  
**Parent:** `CNX-20260905-252`  
**Parent umbrella:** `CNX-20260831-188`  
**Disposition:** `TASK252_ACCEPTED_BLOCKED__SCHEDULER_TIMEOUT_AND_BUFFERED_RUNNER_EVIDENCE_LOSS_PROVEN__STREAMING_RUNNER_TDD_REQUIRED`

## Accepted Task-252 result

Reviewed report HEAD:

`c1649f064e22492ac324a1f137fc109cff680c62`

Independent review commit:

`9318008a9549a264aa28491b0d4d264750a9e168`

Independent review verdict:

`ACCEPT_BLOCKED_TASK251_CHILD_STAGE_UNPROVEN__SCHEDULER_TIMEOUT_AND_BUFFERED_RUNNER_EVIDENCE_LOSS_PROVEN__STREAMING_DIAGNOSTIC_RUNNER_TDD_REQUIRED`

Task252 established four separate causal layers:

```text
scheduler termination mechanism = proven: PT45M + AllowHardTerminate + LastTaskResult 0x41306
runner evidence-loss mechanism = proven: ReadToEnd()/WaitForExit() + post-completion artifact writes
last installer stage = unproven beyond child-start boundary
underlying child stall cause = unproven
```

Retained Task251 runner SHA-256:

`0c2da0cb5877ca9493e4921c3a7b5492dd884841a2bd68c3fb63032b6e42eb98`

The runner can lose all child stdout/stderr if the outer PowerShell process is hard-terminated before child completion. Task252 made no live product/source/test/workflow mutation and does not authorize an installer retry or timeout increase.

Public `v0.9.3` remains immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

## Active Task 253

Execute:

`docs/operations/coordination/tasks/CNX-20260905-253-task252-streaming-diagnostic-runner-tdd-qualification.md`

Task253 must use TDD to create and qualify a repository-owned Windows PowerShell 5.1 manifest streaming runner whose emitted child output is durable while the child is still alive.

Mandatory behavior includes:

```text
runner-start marker before child launch
child-start/PID evidence immediately after launch
stdout/stderr files visible and flushed while child is alive
forced outer-runner termination preserves already-emitted output
known nonzero child exit preserved on normal completion
launch failure distinct from child nonzero
manifest arguments preserved exactly
```

Required topology:

```text
fresh authority
-> test-only RED
-> minimal streaming runner implementation
-> focused GREEN
-> full GREEN
-> exact candidate + runner SHA + installer SHA + plugin fingerprint proof
-> exact-SHA Validate / Windows Installer Pack Smoke / PS5.1 Acceptance Smoke SUCCESS
-> report
-> STOP for independent review
```

Preferred production location:

`scripts/manifest-streaming-runner.ps1`

Do not modify installer/ownership/plugin/lifecycle/dashboard semantics as part of Task253.

## Hard fences

```text
live scripts/install.ps1 = 0
live installer task registration/start = 0
live rollover prepare/finalize = 0
live plugin/retired-tree/rollover-backup mutation = 0
controller/Gateway/provider/model/DB mutation = 0
Dashboard/Discord/API semantic sends = 0
recovery replay/resend = 0
release/tag mutation = 0
force push/history rewrite = 0
```

Repository source/test edits for the streaming runner and ordinary CI are authorized. Synthetic test children must not call product/runtime surfaces.

## Stop boundary

Hermes must publish:

`docs/operations/coordination/reports/CNX-20260905-253-task252-streaming-diagnostic-runner-tdd-qualification.md`

Then STOP for independent ChatGPT review. Live installer requalification and semantic acceptance require separate successor authority even if Task253 passes.
