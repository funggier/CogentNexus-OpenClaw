# Independent Review — CNX-20260829-124 v0.9.3 Remaining Real-Windows Lifecycle Acceptance

## Verdict

**ACCEPTED PARTIAL PASS — RESET / UNINSTALL / FRESH REINSTALL / STOP / START / RESTART PASSED ONCE; RECOVERY PRODUCT BEHAVIOR WAS NOT TESTED BECAUSE THE EXACT HARNESS CANCELLED AT ITS UNSATISFIED INTERACTIVE CONFIRMATION GATE.**

Task 124 respected the one-shot/fail-stop contract. The lifecycle phases before recovery are accepted. The recovery-harness exit code `1` is not accepted as product failure evidence because the exact candidate source proves that execution stopped in `Confirm-Disruptive` before the first disruptive scenario.

## Reviewed source and report

Task report:

`docs/operations/coordination/reports/CNX-20260829-124-v093-remaining-real-windows-lifecycle-acceptance.md`

Frozen candidate:

- source SHA `01d08cd7c82f542c821e3a60f7fffa036efb1d75`;
- artifact ID `9691451156`;
- payload/plugin fingerprint `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`.

Exact recovery harness:

`scripts/test-v093-ollama-recovery-windows-v3.ps1`

Candidate blob:

`80da4a2a23f5b5e936d725dcbd695a631bad1cb6`

The source contains:

```powershell
$answer=Read-Host 'Type y to continue'
if($answer -cne 'y'){throw 'Disruptive suite cancelled.'}
```

The Task-124 authorized command supplied `-Scenario all -RunDisruptive` but did not define an interactive confirmation channel. Therefore the cancellation was an acceptance-invocation defect, not a failed gateway/provider/operator-stop recovery scenario.

## Accepted lifecycle evidence

The following phases each executed exactly once and passed their deterministic postconditions:

1. `reset` — exit `0`, one literal `y`, reset PASS, deterministic post-reset state coherent.
2. `uninstall` — exit `0`, one literal `y`, uninstall PASS; OpenClaw/Ollama/Gateway preservation proof passed and CNX-owned surfaces were absent as expected. The PowerShell evidence encoding/decoding issue was evidence representation only; it did not change live state or invalidate the successful preservation proof.
3. fresh reinstall — exact same frozen candidate, exact provider-neutral command, exit `0`, installed fingerprint/ownership/readiness/SQLite proof passed.
4. `stop` — exit `0`, coherent stopped/maintenance state with expected listeners absent.
5. `start` — exit `0`, Gateway/Ollama and managed readiness restored.
6. `restart` — exit `0`, healthy final managed state.

No completed lifecycle phase was replayed.

## Recovery boundary

Task-124 recovery invocation count:

- exact harness process invocation: **1**;
- explicit disruptive confirmation PASS steps: **0**;
- `gateway-crash` scenario executions: **0**;
- `provider-crash` scenario executions: **0**;
- `operator-stop` scenario executions: **0**.

The harness prechecks passed, then `Confirm-Disruptive` cancelled because no answer was supplied. Best-effort cleanup/start restored a healthy managed state. No recovery scenario result can be inferred from this cancellation.

## Carried one-shot ledger

Consumed and forbidden to replay in successors:

- Task-121 install-over: `1 / 1`;
- Task-124 reset: `1 / 1`;
- Task-124 uninstall: `1 / 1`;
- Task-124 fresh reinstall: `1 / 1`;
- Task-124 stop: `1 / 1`;
- Task-124 start: `1 / 1`;
- Task-124 restart: `1 / 1`.

Task-124's recovery-harness invocation is also consumed under Task 124. However, because no disruptive scenario began, a **new separately authorized successor task** may execute the exact recovery suite once with the exact confirmation contract satisfied. This is a new acceptance authorization, not permission to replay any completed lifecycle phase.

## Successor requirement

A successor may do only:

`fresh deterministic read-only fence -> exact recovery harness in a true interactive TTY -> exactly one literal y at the exact Read-Host prompt -> recovery scenarios -> final deterministic read-only snapshot -> report`

It must not run reset, uninstall, reinstall, stop, start, or restart as setup/cleanup. It must not modify the exact harness or automate around `Read-Host` with source edits, pipeline tricks, or a new generic wrapper.

If the executor cannot provide a real interactive confirmation channel, the successor must stop `BLOCKED` without invoking the disruptive suite.

## Dashboard boundary

No Dashboard semantic Send is authorized until recovery reality acceptance passes and receives a separate independent review.
