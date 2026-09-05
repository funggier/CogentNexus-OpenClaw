# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `TASK254_TASK253_TARGET_CHILD_IDENTITY_BINDING_TDD_REPAIR`
Current disposition: `TASK253_PASS_REJECTED__DURABLE_STREAMING_PROVEN__TARGET_CHILD_PID_BINDING_CONTRACT_NOT_MET__TDD_REPAIR_REQUIRED`
Task ID: `CNX-20260905-254`
Parent task: `CNX-20260905-253`
Parent umbrella: `CNX-20260831-188`
Updated: 2026-09-05 ICT
Executor: Hermes / repository-capable implementation agent
Coordinator / independent reviewer: ChatGPT

## Reviewed Task-253 result

Reviewed report HEAD:

`92870320e10f2a53f477561f5c4c4d24e6439875`

Independent review commit:

`1674407f0cd3e0b7a77cf0a40cc41a5ae29ab7a8`

Independent review verdict:

`REJECT_PASS_STREAMING_RUNNER_TARGET_PID_CONTRACT_NOT_MET__DURABLE_STREAMING_PROVEN__TDD_IDENTITY_BINDING_REPAIR_REQUIRED`

Accepted Task253 evidence:

```text
durable stdout/stderr while target alive = proven
pre-kill stream bytes survive outer-runner termination = proven
normal exit 23 = proven
basic invalid-target terminal classification = proven
exact candidate CI gates = green
live prohibited effects = 0
```

Blocking defect:

```text
child-started.json.pid = cmd.exe launcher PID, not actual manifest target PID
child-started.json.executable = target executable
invalid target can still create child-started.json before cmd.exe returns 9009
```

Therefore Task253 is not authorized as the live forensic boundary.

## Active Task 254

Execute:

`docs/operations/coordination/tasks/CNX-20260905-254-task253-target-child-identity-binding-tdd-repair.md`

Required flow:

```text
fresh GitHub authority
-> TEST-ONLY RED for actual target PID binding + invalid-target no-child-start evidence
-> preserve durable streaming + forced-termination behavior
-> minimal target-identity production repair
-> focused GREEN including quoting edge + deterministic synthetic cleanup
-> full GREEN
-> final runner SHA + installer SHA + plugin fingerprint
-> exact-SHA Actions GREEN
-> report
-> STOP for independent review
```

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

Repository source/test edits limited to the streaming runner and its qualification coverage are authorized.

## Stop boundary

Hermes must publish:

`docs/operations/coordination/reports/CNX-20260905-254-task253-target-child-identity-binding-tdd-repair.md`

Then STOP for independent ChatGPT review. Even on PASS, live installer retry and semantic acceptance remain unauthorized until a separate successor task.
