# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `REPOSITORY_SOURCE_TDD_REPAIR`
Current authorization: `CNX-20260829-126_PROVIDER_CRASH_RECOVERY_CONVERGENCE_ROOT_CAUSE_REPAIR`
Task ID: `CNX-20260829-126`
Updated: 2026-08-29 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260829-126-provider-crash-recovery-convergence-root-cause-repair.md`](tasks/CNX-20260829-126-provider-crash-recovery-convergence-root-cause-repair.md)

Task 126 diagnoses and repairs the **real provider-crash durable-convergence failure** proven by Task 125. It is repository/source/test/CI work plus read-only inspection of retained Task-125 evidence. It authorizes no live Windows lifecycle or recovery replay.

## Task 125 closure

Task-125 report:

`docs/operations/coordination/reports/CNX-20260829-125-v093-recovery-reality-interactive-confirmation-acceptance.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260829-125-v093-recovery-reality-interactive-confirmation-acceptance-review.md`

Review verdict:

`ACCEPTED FAIL — GATEWAY-CRASH RECOVERY PASSED, BUT PROVIDER-CRASH RECOVERY FAILED TO REACH THE REVIEWED DURABLE-READY CONTRACT WITHIN 420 SECONDS; SOURCE/HARNESS ROOT-CAUSE DIAGNOSIS IS REQUIRED BEFORE ANY REPLAY.`

Accepted Task-125 facts:

- exact candidate `01d08cd7c82f542c821e3a60f7fffa036efb1d75`;
- true PTY and exact lowercase `y` confirmation passed;
- harness prechecks passed;
- `gateway-crash` passed;
- `provider-crash` was injected;
- `converge-provider-after` did not observe the complete durable READY predicate inside `420` seconds;
- `operator-stop` did not execute because fail-stop worked;
- suite was not replayed;
- harness-owned cleanup restored healthy managed state;
- no Dashboard semantic Send occurred.

This is not the earlier `$args`, TUI, UTF-16, or confirmation defect.

## Consumed live ledger

Consumed and forbidden to replay during Task 126:

- Task-121 install-over `1 / 1`;
- Task-124 reset `1 / 1`;
- Task-124 uninstall `1 / 1`;
- Task-124 fresh reinstall `1 / 1`;
- Task-124 stop `1 / 1`;
- Task-124 start `1 / 1`;
- Task-124 restart `1 / 1`;
- Task-125 recovery suite `1 / 1`;
- Task-125 gateway-crash scenario `1 / 1 PASS`;
- Task-125 provider-crash scenario `1 / 1 FAIL at durable convergence`;
- operator-stop `0`, not reached.

## Task 126 root-cause gate

Read the retained Task-125 JSON/log read-only and identify exactly which durable-convergence predicate(s) remained false across the 420-second observation window.

The provider-crash predicate requires all of:

- host mode `managed`;
- host selected provider `ollama`;
- provider selected provider `ollama`;
- recovery verdict `READY`;
- one Provider event adapter row with `details.expected == false`;
- Gateway listener present;
- Ollama listener present;
- one Provider recovery incident row with `details.circuitOpen == false`.

Extract first/last/change-point observations before changing source.

Then trace the owning state machine/check logic, write a focused RED regression test from the actual evidence, apply the smallest responsibility-local repair, and require full GREEN + exact-SHA CI + package proof.

Do not merely increase the recovery timeout unless the retained evidence proves the timeout alone is wrong.

## Hard fence

Task 126 does not authorize:

- live provider crash injection or recovery-suite replay;
- install/install-over/reset/uninstall/reinstall;
- stop/start/restart;
- live OpenClaw/provider configuration mutation;
- process kill/reboot;
- manual Windows cleanup/normalization;
- credentials/secrets;
- Dashboard semantic Send;
- merge/tag/release/force push.

## Completion signal

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260829-126-provider-crash-recovery-convergence-root-cause-repair.md`

Then stop for independent ChatGPT review. Do not auto-open a new live Windows acceptance task.