# Coordination Channel Status

**State:** `READY_FOR_HERMES`  
**Execution mode:** `REPOSITORY_SOURCE_TDD_REPAIR`  
**Updated:** 2026-08-29 ICT  
**Transport:** GitHub repository history  
**Human authority:** operator authorized continued stabilization; Task 126 authorizes repository/source TDD repair and read-only retained-evidence diagnosis only  
**Execution trigger:** manual Hermes/Codex continuation; scheduled execution remains disabled

## Active work

Task:

[`tasks/CNX-20260829-126-provider-crash-recovery-convergence-root-cause-repair.md`](tasks/CNX-20260829-126-provider-crash-recovery-convergence-root-cause-repair.md)

Task ID:

`CNX-20260829-126`

## Task 125 independent review

Task-125 report:

`docs/operations/coordination/reports/CNX-20260829-125-v093-recovery-reality-interactive-confirmation-acceptance.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260829-125-v093-recovery-reality-interactive-confirmation-acceptance-review.md`

Verdict:

`ACCEPTED FAIL — GATEWAY-CRASH RECOVERY PASSED, BUT PROVIDER-CRASH RECOVERY FAILED TO REACH THE REVIEWED DURABLE-READY CONTRACT WITHIN 420 SECONDS; SOURCE/HARNESS ROOT-CAUSE DIAGNOSIS IS REQUIRED BEFORE ANY REPLAY.`

Task 125 established a valid live failure boundary:

- true interactive confirmation passed;
- gateway crash recovery passed;
- provider crash was injected;
- the complete durable READY predicate was not observed inside 420 seconds;
- operator-stop was not reached;
- harness cleanup returned the machine to healthy managed state;
- no recovery replay and no Dashboard semantic Send occurred.

## Consumed live-operation ledger

Do not replay during Task 126:

- install-over `1 / 1`;
- reset `1 / 1`;
- uninstall `1 / 1`;
- fresh reinstall `1 / 1`;
- stop `1 / 1`;
- start `1 / 1`;
- restart `1 / 1`;
- Task-125 recovery suite `1 / 1`;
- gateway-crash `1 / 1 PASS`;
- provider-crash `1 / 1 FAIL`;
- operator-stop `0`, not reached.

## Task 126 diagnosis and TDD contract

Use retained Task-125 JSON/log evidence read-only. Before any source edit, extract the complete `converge-provider-after` observation series and identify which exact predicate fields remained unsatisfied.

Correlate the observations with the owning provider recovery, incident/circuit, event-adapter, supervisor, host-state, and recovery-verdict logic.

Then:

1. add a focused RED regression test that reproduces the evidence-derived failure;
2. apply the smallest responsibility-local source or harness-contract fix at the actual owning layer;
3. run focused and full test suites/static checks/plugin validation/evaluation/audit;
4. push an exact repaired candidate;
5. require exact-SHA CI and package proof;
6. publish the Task-126 report and stop for ChatGPT review.

Do not assume in advance whether the defect is product recovery logic or the reviewed acceptance predicate. Do not simply lengthen the 420-second fuse without evidence.

## Prohibited during Task 126

- live provider crash/recovery replay;
- install/install-over/reset/uninstall/reinstall;
- stop/start/restart;
- live provider/OpenClaw mutation;
- process kill/reboot;
- manual cleanup/normalization;
- credential/secret access;
- Dashboard semantic Send;
- merge/tag/release/force push.

## Required output

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260829-126-provider-crash-recovery-convergence-root-cause-repair.md`

After publishing, stop for independent ChatGPT review. Do not automatically open a new live Windows acceptance task.