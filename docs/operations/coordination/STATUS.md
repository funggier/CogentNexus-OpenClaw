# Coordination Channel Status

**State:** `READY_FOR_HERMES`  
**Execution mode:** `REPOSITORY_SOURCE_TDD_REPAIR`  
**Updated:** 2026-08-29 ICT  
**Transport:** GitHub repository history  
**Human authority:** operator authorized continued stabilization; Task 127 authorizes repository/source TDD repair only  
**Execution trigger:** manual Hermes/Codex continuation; scheduled execution remains disabled

## Active work

Task:

[`tasks/CNX-20260829-127-recovery-harness-failclosed-contract-and-ci-proof.md`](tasks/CNX-20260829-127-recovery-harness-failclosed-contract-and-ci-proof.md)

Task ID:

`CNX-20260829-127`

## Task 126 independent review

Task-126 report:

`docs/operations/coordination/reports/CNX-20260829-126-provider-crash-recovery-convergence-root-cause-repair.md`

Review:

`docs/operations/coordination/reviews/CNX-20260829-126-provider-crash-recovery-convergence-root-cause-repair-review.md`

Verdict:

`REJECTED CANDIDATE ADVANCEMENT — ROOT-CAUSE CLASSIFICATION IS ACCEPTED, BUT THE HARNESS REPAIR IS NOT YET FAIL-CLOSED OR BEHAVIORALLY PROVEN, AND THE AFFECTED RECOVERY-SPECIFIC SMOKE DID NOT RUN ON THE EXACT CANDIDATE SHA.`

Accepted root-cause facts:

- retained Task-125 convergence series showed coherent recovered provider/Gateway state;
- recovery verdict stayed `READY_WITH_WARNINGS` only because the provider incident intentionally remained open pending stable model-success evidence;
- provider recovery policy is correct and must not be weakened;
- the repair belongs to the acceptance harness.

Rejected candidate:

`69a3efa1feb7711f22c83055a8571035240ec81c`

Confirmed exact-SHA successes on that rejected candidate:

- Validate `33223319908` — success;
- Windows Installer Pack Smoke `33223319175` — success;
- PS5.1 Acceptance Smoke `33223319261` — success.

GitHub showed only those three runs for the SHA; the dedicated `PS5.1 v0.9.3 Ollama Recovery V3 Smoke` did not run.

## Task 127 requirements

1. Add a true behavioral RED that invokes harness-owned convergence logic, not a test-local duplicate or source-text grep.
2. Refactor minimally so `Wait-DurableConvergence` and the non-disruptive self-test share one harness-owned predicate.
3. Allow `READY_WITH_WARNINGS` only on provider-crash convergence when the sole WARN is exactly the expected open/circuit-closed `Provider recovery incident`; reject any additional/unrelated warning.
4. Keep ordinary/gateway/operator convergence strict `READY`.
5. Add/adjust the recovery-v3 workflow so direct-push candidate changes produce an exact-SHA recovery smoke run.
6. Make that smoke execute the real non-disruptive convergence contract self-test, not only parse/grep source.
7. Require full GREEN, four exact-SHA workflow successes, and fresh package proof.
8. Publish the Task-127 report and stop for independent review.

## Consumed live-operation ledger

Do not replay during Task 127:

- install-over `1 / 1`;
- reset `1 / 1`;
- uninstall `1 / 1`;
- fresh reinstall `1 / 1`;
- stop `1 / 1`;
- start `1 / 1`;
- restart `1 / 1`;
- Task-125 recovery suite `1 / 1`;
- gateway-crash `1 / 1 PASS`;
- provider-crash `1 / 1 old-harness convergence FAIL`;
- operator-stop `0`, not reached.

## Prohibited

No live provider crash/recovery replay, lifecycle mutation, provider/OpenClaw live mutation, process kill/reboot, manual cleanup/normalization, credential/secret access, Dashboard semantic Send, merge/tag/release, or force push.

## Required output

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260829-127-recovery-harness-failclosed-contract-and-ci-proof.md`

Then stop for independent ChatGPT review. Do not automatically open a live Windows acceptance task.
