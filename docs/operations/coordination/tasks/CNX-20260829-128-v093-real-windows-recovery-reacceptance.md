# CNX-20260829-128 — v0.9.3 Real-Windows Recovery Re-Acceptance

- Status: `READY_FOR_HERMES`
- Execution mode: `LIVE_WINDOWS_RECOVERY_ACCEPTANCE_ONLY`
- Owner / independent reviewer: ChatGPT
- Executor: Hermes/Codex after operator continuation
- Date: 2026-08-29 ICT
- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`

## Purpose

Run one new, separately authorized real-Windows recovery-reality acceptance against the repaired Task-127 harness contract.

This task exists because Task 125 consumed the previous recovery-suite execution under the old harness, Task 126 proved that failure was an acceptance-harness contract mismatch, and Task 127 repaired and independently validated that harness contract on an exact candidate SHA.

Task 128 authorizes **one new recovery-suite execution only**. It does not authorize replay of the already-passed installer/lifecycle acceptance phases.

## Accepted repository candidate

Independent Task-127 review:

`docs/operations/coordination/reviews/CNX-20260829-127-recovery-harness-failclosed-contract-and-ci-proof-review.md`

Accepted exact source candidate:

`1b922bf400fdbccb1f9c7019b89b69fd67f44070`

Exact repaired recovery harness:

- path: `scripts/test-v093-ollama-recovery-windows-v3.ps1`
- Git blob: `622f70b339fea0f2ef7c564253aa3c6bf90ffc97`

Exact package proof:

- artifact ID: `9706878201`
- artifact name: `cogentnexus-openclaw-v0.9.3-package-proof-1b922bf400fdbccb1f9c7019b89b69fd67f44070`
- artifact digest: `sha256:c5dcbda0858a08362daa3218c2912ddd4a36c259e61a05be28d7b1d4114b104c`
- package version: `0.9.3`
- payload file count: `178`
- payload/plugin fingerprint: `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`
- tar.gz SHA256: `9a4634e41d21271b92d0c6ce69f4931bca11455808a9e1b8567e48db85bb432d`
- ZIP SHA256: `526ca264db77b960d2d81d3f6cf7c100e8c45f2d6243eaab00801da9ee293c3e`

Task-127 exact-SHA workflows all passed:

- Validate `33226001453`
- PS5.1 v0.9.3 Ollama Recovery V3 Smoke `33226001456`
- PS5.1 Acceptance Smoke `33226001472`
- Windows Installer Pack Smoke `33226001471`

## Why no reinstall is authorized

The repaired candidate changes the recovery acceptance harness/test/workflow/coordination surfaces, not the installed CogentNexus runtime/provider implementation that already passed Task-124 lifecycle acceptance and Task-123/124 deterministic installed-state checks.

Before disruption, the executor must verify from Git history that the accepted candidate introduces no installed runtime/plugin/installer production change requiring deployment for this recovery re-acceptance. If that statement is false, ambiguous, or cannot be proven, stop `BLOCKED` before any disruption; do not install or install-over.

The installed plugin fingerprint is expected to remain:

`3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`

## Consumed historical ledger

The following old authorizations remain consumed and must never be replayed under Task 128:

- Task-121 install-over: `1 / 1`;
- Task-124 reset: `1 / 1`;
- Task-124 uninstall: `1 / 1`;
- Task-124 fresh reinstall: `1 / 1`;
- Task-124 standalone stop: `1 / 1`;
- Task-124 standalone start: `1 / 1`;
- Task-124 standalone restart: `1 / 1`;
- Task-125 recovery suite: `1 / 1` under the old harness;
- Task-125 gateway-crash: `1 / 1 PASS` under the old harness;
- Task-125 provider-crash: `1 / 1 old-harness convergence FAIL`;
- Task-125 operator-stop: `0`, not reached.

Task 128 creates a **new one-shot ledger** solely because the accepted candidate contains a repaired recovery acceptance harness:

- Task-128 exact recovery suite: maximum `1 / 1`;
- within that one suite, the reviewed scenarios are `baseline`, `gateway-crash`, `provider-crash`, `operator-stop` exactly as implemented by the exact harness.

No scenario or suite rerun is permitted inside Task 128 after the harness process is launched.

## Phase 0 — authority, candidate, and read-only safety fence

Before any disruptive command:

1. Fresh-fetch GitHub coordination and confirm Task 128 remains authoritative and is not superseded.
2. Confirm accepted source candidate remains `1b922bf400fdbccb1f9c7019b89b69fd67f44070`.
3. Materialize/use an isolated exact-candidate checkout/worktree or exact package extraction without modifying the installed runtime workspace.
4. Verify the harness bytes are exact: `git hash-object scripts/test-v093-ollama-recovery-windows-v3.ps1` must equal `622f70b339fea0f2ef7c564253aa3c6bf90ffc97` when using a Git checkout. If using the package proof, establish equivalent exact source provenance and record it.
5. Confirm no source/harness edits exist in the execution copy.
6. Confirm the historical consumed ledger above.

Then perform deterministic, argument-safe **read-only** preflight probes only. Do not use a generic wrapper that can drop arguments.

Required preflight evidence:

- installed CogentNexus state is coherent/managed;
- `check recovery --json` is safe for the pre-disruption baseline and there is no unsafe pending lifecycle/recovery transition;
- installed ownership verification passes;
- installed plugin fingerprint is exactly `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`;
- OpenClaw is exactly `2026.7.1-2`;
- exactly one current `cogentnexus-openclaw` plugin is loaded/enabled;
- Gateway listener/process is healthy;
- Ollama REST/listener is healthy and version/model inventory is recorded;
- SQLite integrity is exactly `ok`;
- relevant supervisor/OpenClaw service or scheduled-task state is recorded;
- no unsafe pending provider transition or duplicate active recovery operation exists.

Capture the preflight Ollama model inventory and compare it against the final snapshot; Task 128 authorizes no model/configuration change.

If the preflight is not already safe, stop `BLOCKED`. Do **not** use start/restart/reset/install or manual normalization to manufacture the precondition.

## Phase 1 — true interactive confirmation gate

The exact harness contains:

`Read-Host 'Type y to continue'`

Task 128 requires a true interactive PowerShell TTY/console session capable of satisfying that prompt normally.

Rules:

1. Establish before launching the suite that the executor channel is an actual interactive PTY/console suitable for `Read-Host`.
2. Run the exact harness directly from the verified exact-candidate execution copy.
3. Do not use a generic executor wrapper around the PowerShell command.
4. Do not pipe `y`, redirect stdin, synthesize host input, monkey-patch `Read-Host`, edit the harness, or create a replacement harness.
5. Wait until the exact prompt appears.
6. Enter exactly one lowercase `y`, then Enter.
7. Require harness evidence step `explicit-disruptive-confirmation = PASS` before accepting any disruptive scenario result.

If a true interactive channel is unavailable, stop `BLOCKED` **before launching the disruptive suite**.

## Phase 2 — exact recovery suite, once

Canonical logical command:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File <EXACT-CANDIDATE-PATH>\scripts\test-v093-ollama-recovery-windows-v3.ps1 -Scenario all -RunDisruptive
```

Use the actual verified absolute path to the exact candidate harness. Record the literal command and execution path.

This is the only Task-128 recovery-suite execution authorized.

### Baseline

Require baseline PASS before any crash scenario advances.

### Gateway-crash

Require:

- exact validated OpenClaw Gateway listener PID targeted;
- no process-tree kill;
- injected exact PID terminates;
- a different Gateway PID is observed after recovery;
- durable convergence passes;
- Gateway/ordinary convergence remains strict `READY` under the repaired harness;
- scenario records PASS.

### Provider-crash

Require:

- exact validated Ollama listener PID targeted;
- no process-tree kill;
- injected exact PID terminates;
- a different Ollama listener PID is observed after recovery;
- provider recovery circuit remains closed after the single injected crash;
- durable convergence passes under the repaired fail-closed provider-incident contract;
- if convergence is `READY_WITH_WARNINGS`, the retained observation must show exactly one WARN and it must be the single open, circuit-closed `Provider recovery incident`; every other recovery check must be PASS;
- if convergence reaches exact `READY`, record the incident/check state that made that verdict coherent;
- scenario records PASS.

Do not create an artificial model completion merely to close the incident. The purpose is to validate recovery after an idle provider crash under the real contract.

### Operator-stop

Require:

- the harness's intentional `cnxclaw stop` transition only;
- maintenance/stopped desired state is observed;
- Gateway remains stopped for the harness observation period with no automatic recovery;
- only the harness's reviewed `start-after-intentional-stop` is used to restore the managed state;
- Gateway and Ollama listeners return;
- durable convergence passes under the ordinary strict-READY path;
- scenario records PASS.

No standalone Task-124 stop/start/restart command may be replayed outside the exact harness.

## Failure rule

Once the Task-128 harness process is launched, the one-shot suite authorization is consumed.

If any phase/scenario fails:

- fail-stop immediately;
- do not rerun the suite;
- do not rerun an individual crash scenario;
- do not switch to a different harness or confirmation mechanism;
- allow only the exact harness's built-in best-effort reconciliation behavior if it executes naturally;
- do not manually start/restart/reset/reinstall/normalize afterward under Task 128;
- preserve evidence and classify the first failure.

A later retry would require a new independent diagnosis/review and explicit new task/candidate authorization.

## Phase 3 — final deterministic read-only snapshot

Only after the exact harness returns PASS / exit `0`, collect a final read-only snapshot without lifecycle repair commands.

Require and record:

- installed plugin fingerprint/ownership unchanged;
- CogentNexus managed state;
- provider selection `ollama`;
- recovery/check state and any intentionally open/closed incident semantics after the suite;
- no unsafe pending or duplicate recovery operation;
- OpenClaw exact `2026.7.1-2`;
- exactly one current plugin loaded/enabled;
- Gateway listener/process healthy;
- Ollama REST version, listener PID, `/api/tags`, `/api/ps`, and model inventory;
- final model inventory matches the preflight inventory;
- SQLite integrity exactly `ok`;
- supervisor/OpenClaw service/scheduled-task state;
- namespace/residue classification;
- no Dashboard semantic Send.

If the final read-only snapshot itself exposes an inconsistency, report FAIL/BLOCKED as appropriate. Do not normalize it with lifecycle commands.

## Phase 4 — report and stop

Publish exactly:

`docs/operations/coordination/reports/CNX-20260829-128-v093-real-windows-recovery-reacceptance.md`

The report must include:

- exact Task-127 candidate and package proof;
- exact harness path and blob/provenance;
- proof that no reinstall was needed/used;
- fresh preflight evidence root;
- exact interactive PTY/confirmation evidence;
- literal recovery-suite command;
- one-shot execution ledger;
- baseline result;
- gateway-crash before/after PIDs, convergence verdict, scenario result;
- provider-crash before/after PIDs, recovery incident/circuit/check details, convergence verdict, scenario result;
- operator-stop observation and harness-owned restore result;
- harness exit code/result and evidence log/JSON paths;
- final deterministic snapshot;
- explicit no Dashboard Send;
- verdict `PASS`, `FAIL`, or `BLOCKED` and exact first failure if not PASS.

Then stop for independent ChatGPT review. **Do not automatically open the Dashboard durable-delivery acceptance task.**

## Hard fence

Task 128 does **not** authorize:

- install or install-over;
- reset/uninstall/reinstall;
- standalone stop/start/restart outside the exact harness scenario;
- source/harness edits;
- alternate/piped/synthesized confirmation;
- manual cleanup/normalization;
- candidate substitution;
- provider/model/endpoint/configuration changes;
- OpenClaw update/change;
- credential/secret access;
- Dashboard semantic Send;
- reboot;
- generic process-tree kill;
- merge/tag/GitHub Release;
- force push.

Final Dashboard durable-delivery acceptance remains prohibited until Task 128 passes and is independently reviewed.