# Coordination Channel Status

**State:** `READY_FOR_HERMES`  
**Execution mode:** `TASK254_TASK253_TARGET_CHILD_IDENTITY_BINDING_TDD_REPAIR`  
**Updated:** 2026-09-05 ICT  
**Transport:** GitHub repository / Actions authoritative; Task254 is repository/test-only; live installer retry and semantic acceptance remain unauthorized  
**Active task:** `CNX-20260905-254`  
**Parent:** `CNX-20260905-253`  
**Parent umbrella:** `CNX-20260831-188`  
**Disposition:** `TASK253_PASS_REJECTED__DURABLE_STREAMING_PROVEN__TARGET_CHILD_PID_BINDING_CONTRACT_NOT_MET__TDD_REPAIR_REQUIRED`

## Reviewed Task-253 result

Reviewed report HEAD:

`92870320e10f2a53f477561f5c4c4d24e6439875`

Independent review commit:

`1674407f0cd3e0b7a77cf0a40cc41a5ae29ab7a8`

Independent review verdict:

`REJECT_PASS_STREAMING_RUNNER_TARGET_PID_CONTRACT_NOT_MET__DURABLE_STREAMING_PROVEN__TDD_IDENTITY_BINDING_REPAIR_REQUIRED`

Task253 successfully proved the durable streaming objective that Task252 required, and its exact implementation candidate `cc35ce506b6a9ffee3223ec79ddb0373a898e4a5` had terminal-success validation gates. However, its `child-started.json` binds `pid` to the `cmd.exe` redirection launcher while `executable` names the manifest target. The runner also writes that child-start artifact before it knows whether the target executable actually launched; an invalid target can later become `child_launch_exception` even though `child-started.json` already exists.

This violates the required actual-child identity contract and prevents use of the runner as the next live forensic boundary.

Nonblocking Task253 reporting gaps also recorded by review:

```text
final streaming-runner SHA-256 omitted from report
PS5.1 serializer job 101231503736 belongs to run 33938651865, not 33938651855
```

Public `v0.9.3` remains immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

## Active Task 254

Execute:

`docs/operations/coordination/tasks/CNX-20260905-254-task253-target-child-identity-binding-tdd-repair.md`

Task254 must use strict TDD to bind durable child-start evidence to the actual manifest target process. Required regressions include:

```text
synthetic target self-reports PID
child-started.json.pid equals that exact target PID
child-started executable identity matches the same target
invalid executable leaves no target child-start artifact
launcher metadata is separate if retained
stdout/stderr remain durable while target is alive
forced outer-runner termination preserves emitted output
test cleans up target/launcher process tree deterministically
exit 23 and launch-failure classification remain exact
argument vector includes a quoting edge, not only spaces
```

Do not modify `scripts/install.ps1`, ownership/backup/transaction semantics, plugin payload, lifecycle/provider/model logic, or Dashboard/Discord delivery semantics.

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

Repository source/test edits for the streaming runner and ordinary CI are authorized.

## Stop boundary

Hermes must publish:

`docs/operations/coordination/reports/CNX-20260905-254-task253-target-child-identity-binding-tdd-repair.md`

Then STOP for independent ChatGPT review. Live installer requalification and semantic acceptance require separate successor authority even if Task254 passes.
