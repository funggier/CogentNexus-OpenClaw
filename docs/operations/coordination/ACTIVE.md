# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `REPOSITORY_SOURCE_TDD_REPAIR`
Current authorization: `CNX-20260829-132_PROVIDER_TO_OPERATOR_RECOVERY_SUITE_SEQUENCING_CONTRACT_REPAIR`
Task ID: `CNX-20260829-132`
Updated: 2026-08-29 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260829-132-provider-to-operator-recovery-suite-sequencing-contract-repair.md`](tasks/CNX-20260829-132-provider-to-operator-recovery-suite-sequencing-contract-repair.md)

Task 132 is repository/source TDD repair only. It diagnoses and repairs the remaining recovery-v3 harness scenario-sequencing contradiction proven by Task 131. It authorizes no live recovery or lifecycle mutation.

## Task 131 closure

Task-131 report:

`docs/operations/coordination/reports/CNX-20260829-131-v093-real-windows-recovery-reacceptance-authoritative-root.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260829-131-v093-real-windows-recovery-reacceptance-authoritative-root-review.md`

Accepted verdict:

`ACCEPTED FAIL — authoritative-root preflight passed, gateway-crash recovery passed, and provider-crash recovery passed under the repaired fail-closed incident contract; full-suite acceptance failed before operator-stop because the harness requires strict READY at operator-before even though the immediately preceding provider-crash contract intentionally permits the same open, circuit-closed provider incident to remain READY_WITH_WARNINGS. This is a harness scenario-sequencing defect, not a new provider-recovery product failure. Operator-stop remains unproven.`

Accepted Task-131 live results:

- corrected authoritative preflight PASS;
- baseline PASS;
- gateway-crash PASS;
- provider-crash PASS;
- provider post-crash convergence `READY_WITH_WARNINGS` with exactly one open/circuit-closed provider incident WARN and all other checks PASS;
- operator-stop `0`, not reached;
- Task-131 suite `1 / 1` consumed;
- no rerun/manual normalization/Dashboard Send.

## Task 132 repair boundary

The product recovery policy is not the repair target. Preserve the event-driven invariant:

- automatic provider restart success does not close an incident;
- stable model success or verified manual transition closes it.

Repair only the recovery harness sequencing so that:

- standalone operator-stop still requires strict `READY`;
- when operator-stop immediately follows a provider-crash PASS in the same harness process, `operator-before` may accept only the exact same carried provider incident identity/state previously accepted by provider-crash;
- the exception remains fail-closed: one WARN only, exact incident ID, incident open, circuit closed, all other checks PASS, adapter correct, managed/Ollama/listeners healthy;
- different/stale/missing/duplicate incident, extra WARN, circuit-open, structural failure, or standalone open incident is rejected;
- no artificial model completion or normalization is inserted;
- post-operator-start convergence remains strict `READY`.

## TDD requirement

Before harness production modification, create a deterministic behavioral RED through the real Windows PowerShell harness-owned `-ContractSelfTest` path that reproduces the Task-131 sequence contradiction.

Do not count grep/source-text checks or duplicated Python predicate logic as the behavioral RED.

Then apply the smallest harness-local repair, run focused/full validation, exact-SHA Recovery V3 Smoke, established candidate workflows, and fresh package proof.

Existing relevant files:

- `scripts/test-v093-ollama-recovery-windows-v3.ps1`
- `tests/test_recovery_harness_contract.py`
- `.github/workflows/v093-ollama-recovery-v3-smoke.yml`

## Current repository baseline

Previous accepted candidate used by Task 131:

`1b922bf400fdbccb1f9c7019b89b69fd67f44070`

Previous harness blob:

`622f70b339fea0f2ef7c564253aa3c6bf90ffc97`

Task 132 must produce and report a new exact candidate/harness blob before any future live authorization.

## Historical live ledger

Remain consumed/closed:

- Task-121 install-over `1 / 1`;
- Task-124 reset/uninstall/fresh reinstall/standalone stop/start/restart `1 / 1` each;
- Task-125 old-harness recovery suite `1 / 1`;
- Task-128 suite `0 / 1`, closed blocked;
- Task-131 repaired-harness suite `1 / 1` consumed;
- Task-131 gateway-crash PASS;
- Task-131 provider-crash PASS;
- Task-131 operator-stop `0`, not reached.

Task 132 authorizes zero live operations.

## Completion signal

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260829-132-provider-to-operator-recovery-suite-sequencing-contract-repair.md`

Then stop for independent ChatGPT review. Do not open a live recovery task automatically.

## Hard fence

No live recovery suite/crash injection, no install/install-over/reset/uninstall/reinstall, no live start/stop/restart/enable/disable, no live provider/OpenClaw/model/config mutation, no process kill, no task/service mutation, no cleanup/normalization, no reboot, no credentials/secrets, no Dashboard semantic Send, no merge/tag/release, and no force push.
