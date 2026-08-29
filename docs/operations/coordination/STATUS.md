# Coordination Channel Status

**State:** `READY_FOR_HERMES`  
**Execution mode:** `REPOSITORY_SOURCE_TDD_REPAIR`  
**Updated:** 2026-08-29 ICT  
**Transport:** GitHub repository history  
**Human authority:** operator authorized continued stabilization; Task 132 authorizes repository/source/test/CI/package repair only  
**Execution trigger:** manual Hermes/Codex continuation; scheduled execution remains disabled

## Active work

Task:

[`tasks/CNX-20260829-132-provider-to-operator-recovery-suite-sequencing-contract-repair.md`](tasks/CNX-20260829-132-provider-to-operator-recovery-suite-sequencing-contract-repair.md)

Task ID:

`CNX-20260829-132`

## Task 131 accepted live result

Report:

`docs/operations/coordination/reports/CNX-20260829-131-v093-real-windows-recovery-reacceptance-authoritative-root.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260829-131-v093-real-windows-recovery-reacceptance-authoritative-root-review.md`

Accepted classification:

- authoritative-root preflight PASS;
- baseline PASS;
- gateway-crash PASS;
- provider-crash PASS under the fail-closed provider incident exception;
- operator-stop not reached;
- full suite FAIL at `operator-before` because the just-accepted provider incident intentionally remained open and therefore recovery was `READY_WITH_WARNINGS`, while `Assert-Baseline` requires strict `READY`;
- this boundary is a harness sequencing contradiction, not a new provider-recovery runtime failure.

Task-131 suite ledger is consumed `1 / 1` and must not be replayed.

## Why Task 132 is repository-only

The provider recovery policy deliberately closes incidents only on stable model success or a verified manual transition. A successful automatic provider restart does not prove stable model completion and does not close the incident.

Task 131 showed the repaired provider-crash convergence contract working as designed: the provider listener returned, circuit remained closed, and the only recovery warning was the expected open provider incident. The next suite scenario then rejected that same state before it could exercise operator-stop.

Therefore Task 132 repairs only the harness scenario boundary.

## Required sequencing contract

Standalone `operator-stop` remains strict `READY`.

If `operator-stop` immediately follows a provider-crash PASS in the same harness process, the pre-operator gate may accept the carried prior incident only when:

- exact same incident ID;
- one incident row only;
- status WARN;
- `incidentOpen=true`;
- `circuitOpen=false`;
- recovery verdict `READY_WITH_WARNINGS`;
- exactly one WARN total, the provider incident;
- all other checks PASS;
- provider event adapter exactly one PASS row with `expected=false`;
- managed mode and Ollama selected in both host/provider views;
- Gateway and Ollama listeners healthy.

Reject standalone/stale/different/missing/duplicate incident, extra warning, circuit-open, FAIL/INDETERMINATE, adapter mismatch, listener loss, provider mismatch, or non-managed state.

Do not manufacture model completion or lifecycle normalization before operator-stop. Existing harness-owned stop/start behavior remains the operation under test, and post-start convergence remains strict `READY`.

## TDD / validation gate

Before modifying the harness:

- behavioral RED must execute the real PowerShell 5.1 harness `-ContractSelfTest` path and reproduce the Task-131 provider→operator sequence rejection;
- grep/source-text assertions and duplicated Python predicates do not satisfy RED.

Then require focused GREEN, full Python, PowerShell parse/self-test, plugin/evaluation/audit gates, `git diff --check`, dedicated exact-SHA PS5.1 Recovery V3 Smoke, established candidate workflows, and fresh package proof.

Relevant current files:

- `scripts/test-v093-ollama-recovery-windows-v3.ps1`;
- `tests/test_recovery_harness_contract.py`;
- `.github/workflows/v093-ollama-recovery-v3-smoke.yml`.

Previous candidate/harness are historical baseline only:

- source `1b922bf400fdbccb1f9c7019b89b69fd67f44070`;
- harness blob `622f70b339fea0f2ef7c564253aa3c6bf90ffc97`.

Task 132 must produce a new exact candidate and harness blob.

## Historical live ledger

Consumed/closed:

- install-over `1 / 1`;
- Task-124 reset/uninstall/fresh reinstall/standalone stop/start/restart `1 / 1` each;
- Task-125 old-harness recovery suite `1 / 1`;
- Task-128 suite `0 / 1`, closed blocked;
- Task-131 suite `1 / 1` consumed;
- Task-131 gateway-crash PASS;
- Task-131 provider-crash PASS;
- Task-131 operator-stop `0`.

Task 132 authorizes **zero live lifecycle/recovery operations**.

## Prohibited

No live recovery suite/crash injection, install/install-over/reset/uninstall/reinstall, live start/stop/restart/enable/disable, provider/OpenClaw/model/config mutation, process kill, task/service mutation, cleanup/normalization, reboot, credential/secret access, Dashboard semantic Send, merge/tag/release, or force push.

## Required output

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260829-132-provider-to-operator-recovery-suite-sequencing-contract-repair.md`

Then stop for independent ChatGPT review. Final Dashboard durable-delivery acceptance remains unopened and prohibited.
