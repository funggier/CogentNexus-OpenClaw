# CNX-20260829-131 — v0.9.3 Real-Windows Recovery Re-Acceptance with Authoritative Root

- Status: `READY_FOR_HERMES`
- Execution mode: `LIVE_WINDOWS_RECOVERY_ACCEPTANCE_ONLY`
- Owner / independent reviewer: ChatGPT
- Executor: Hermes/Codex after operator continuation
- Date: 2026-08-29 ICT
- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`

## Purpose

Run one new real-Windows recovery-reality acceptance against the independently accepted Task-127 repaired harness, after Task 129/130 proved that Task 128 was blocked by an executor/preflight root mismatch rather than authoritative managed-state drift.

This task creates a **new one-shot recovery-suite authorization**. It does not resume Task 128, does not reuse Task 128's execution context, and does not authorize replay of the already-passed installer/lifecycle acceptance phases.

## Accepted repository candidate and harness

Accepted Task-127 source candidate:

`1b922bf400fdbccb1f9c7019b89b69fd67f44070`

Exact repaired recovery harness:

- path: `scripts/test-v093-ollama-recovery-windows-v3.ps1`
- Git blob: `622f70b339fea0f2ef7c564253aa3c6bf90ffc97`

Exact package proof:

- artifact ID: `9706878201`
- artifact name: `cogentnexus-openclaw-v0.9.3-package-proof-1b922bf400fdbccb1f9c7019b89b69fd67f44070`
- artifact digest: `sha256:c5dcbda0858a08362daa3218c2912ddd4a36c259e61a05be28d7b1d4114b104c`
- payload count: `178`
- payload/plugin fingerprint: `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`
- tar.gz SHA256: `9a4634e41d21271b92d0c6ce69f4931bca11455808a9e1b8567e48db85bb432d`
- ZIP SHA256: `526ca264db77b960d2d81d3f6cf7c100e8c45f2d6243eaab00801da9ee293c3e`

Task-127 exact-SHA workflows passed:

- Validate `33226001453`;
- PS5.1 v0.9.3 Ollama Recovery V3 Smoke `33226001456`;
- PS5.1 Acceptance Smoke `33226001472`;
- Windows Installer Pack Smoke `33226001471`.

## Accepted Task-129/130 forensic result

Task-130 independent review:

`docs/operations/coordination/reviews/CNX-20260829-130-task129-readonly-evidence-publication-closeout-review.md`

Accepted classification:

- `LAUNCHER_OR_ROOT_MISMATCH`;
- `SQLITE_PATH_OR_STATUS_PROBE_DEFECT`, limited to the Task-128 external preflight layer.

Accepted installed launcher authority:

`C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd`

Task-130 retained launcher SHA256:

`f53df28f2a7ee7fc43c65ba2c48770ed9b7ed3e7b14d3c762f957bd017b90f10`

Accepted parsed state root:

`C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw`

Accepted authoritative SQLite path:

`C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw\runtime\cogentnexus-openclaw.sqlite3`

Task 130 demonstrated read-only:

- authoritative mode `managed`;
- selected provider `ollama`;
- recovery `READY`;
- provider incident closed/circuit closed;
- SQLite `PRAGMA integrity_check = ok`;
- Supervisor scheduled task resolves to the same installed script/root.

These are prior forensic facts only. Task 131 must still perform a fresh safe preflight immediately before any disruption.

## Why no reinstall is authorized

The Task-127 accepted candidate changed recovery acceptance harness/test/workflow/coordination surfaces, not the installed runtime/provider/plugin implementation requiring redeployment for this recovery test. Installed plugin fingerprint remained exact during Task 129/130.

Task 131 therefore does not authorize install/install-over. If fresh Git/source identity review contradicts this assumption, stop `BLOCKED`; do not deploy anything under Task 131.

## Historical consumed ledger

Remain consumed and forbidden outside this new exact Task-131 suite:

- Task-121 install-over: `1 / 1`;
- Task-124 reset: `1 / 1`;
- Task-124 uninstall: `1 / 1`;
- Task-124 fresh reinstall: `1 / 1`;
- Task-124 standalone stop: `1 / 1`;
- Task-124 standalone start: `1 / 1`;
- Task-124 standalone restart: `1 / 1`;
- Task-125 old-harness recovery suite: `1 / 1`;
- Task-125 gateway-crash: `1 / 1 PASS`;
- Task-125 provider-crash: `1 / 1 old-harness convergence FAIL`;
- Task-128 repaired-harness suite: `0 / 1 launched`, closed without execution.

Task 131 creates a fresh ledger:

- exact repaired-harness recovery suite: maximum `1 / 1`;
- confirmation lowercase `y`: maximum `1 / 1`, only after prompt;
- baseline/gateway-crash/provider-crash/operator-stop occur only inside that one exact harness process.

No suite or scenario rerun is permitted after launch.

## Phase 0 — authority, exact candidate, and corrected read-only preflight

Before disruption:

1. Fresh-fetch GitHub coordination and confirm Task 131 remains authoritative and unsuperseded.
2. Confirm accepted candidate `1b922bf400fdbccb1f9c7019b89b69fd67f44070` and exact harness blob `622f70b339fea0f2ef7c564253aa3c6bf90ffc97`.
3. Use an isolated exact-candidate checkout/worktree or exact package extraction for the harness. Do not modify the installed runtime workspace.
4. Verify the execution-copy harness bytes exactly by Git blob/hash equivalent.
5. Confirm again from Git history that no installed runtime/plugin/installer production deployment is required.

### Mandatory root-authority correction

All external CNX preflight probes must use the **explicit installed launcher path**:

`$HOME\.openclaw\workspace\cnxclaw.cmd`

Do not invoke a candidate-checkout `cnxclaw_v093.py` for authoritative live state. Do not manually substitute `--root $HOME\.openclaw\workspace`. Do not use a generic wrapper that can drop or rewrite arguments.

Freshly read and record the installed launcher text/hash. Parse and record its:

- owned foreground Python path;
- installed `cnxclaw_v093.py` path;
- explicit `--root` path;
- `%*` forwarding.

Require the parsed root to be the installed `.cogentnexus-openclaw` state root. If the launcher/root authority is missing, changed unexpectedly, ambiguous, or inconsistent with the Supervisor task authority, stop `BLOCKED` before disruption.

### Required fresh read-only preflight

Using direct argument-safe calls through the explicit installed launcher, require:

- `cnxclaw.cmd status` => coherent `managed` state;
- host selected provider `ollama`;
- desired Gateway/provider running;
- `cnxclaw.cmd provider status --json` => selected provider `ollama`;
- `cnxclaw.cmd check recovery --json` => pre-disruption baseline exactly `READY`, no unsafe pending transition, provider incident closed/circuit closed;
- installed ownership verification passes;
- installed plugin fingerprint exactly `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`;
- OpenClaw exactly `2026.7.1-2`;
- exactly one current `cogentnexus-openclaw` plugin loaded/enabled;
- Gateway listener/process healthy;
- Ollama REST/listener healthy and version/model inventory recorded;
- authoritative SQLite path derived from the parsed installed root exists and a read-only URI-mode `PRAGMA integrity_check` returns exactly `ok`;
- relevant Supervisor/OpenClaw scheduled-task/service state recorded;
- no duplicate active recovery operation or unsafe provider transition.

Capture preflight Ollama model inventory for final comparison.

If any preflight requirement is not already safe, stop `BLOCKED`. Do not use start/restart/reset/install/provider selection/manual normalization to manufacture the precondition.

## Phase 1 — true interactive confirmation

The exact harness contains:

`Read-Host 'Type y to continue'`

Requirements:

1. Establish a real interactive PowerShell PTY/console before launching the suite.
2. Run the exact candidate harness directly, without a generic wrapper around the PowerShell command.
3. Do not pipe, redirect, synthesize, monkey-patch, or edit confirmation input.
4. Wait until the literal prompt appears.
5. Enter exactly one lowercase `y`, then Enter.
6. Require harness evidence `explicit-disruptive-confirmation = PASS`.

If true PTY input cannot be guaranteed, stop `BLOCKED` before suite launch.

## Phase 2 — exact recovery suite once

Canonical logical command:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File <EXACT-CANDIDATE-PATH>\scripts\test-v093-ollama-recovery-windows-v3.ps1 -Scenario all -RunDisruptive
```

Record the literal absolute execution path and command.

This is the only Task-131 disruptive process authorized.

The reviewed harness itself resolves:

`$HOME\.openclaw\workspace\cnxclaw.cmd`

and therefore uses the installed launcher's explicit authoritative state root. Do not edit the harness to inject an alternate root.

### Baseline

Require baseline PASS before advancing.

### Gateway-crash

Require:

- exact validated Gateway listener PID targeted;
- no process-tree kill;
- exact injected PID terminates;
- different Gateway listener PID observed after recovery;
- durable convergence PASS;
- ordinary convergence remains strict `READY`;
- scenario PASS.

### Provider-crash

Require:

- exact validated Ollama listener PID targeted;
- no process-tree kill;
- exact injected PID terminates;
- different Ollama listener PID observed after recovery;
- provider circuit remains closed after the single crash;
- durable convergence PASS under the repaired fail-closed provider-incident contract;
- if verdict is `READY_WITH_WARNINGS`, exactly one WARN is permitted and it must be the single open, circuit-closed `Provider recovery incident`; all other checks must be PASS;
- if verdict is `READY`, record the coherent incident/check state;
- scenario PASS.

Do not manufacture a model completion merely to close the incident.

### Operator-stop

Require:

- only harness-owned intentional `cnxclaw stop`;
- maintenance/stopped desired state observed;
- Gateway remains stopped during harness observation period without automatic recovery;
- only harness-owned `start-after-intentional-stop` restores managed state;
- Gateway and Ollama listeners return;
- durable convergence PASS under strict ordinary `READY` path;
- scenario PASS.

No standalone Task-124 lifecycle command may be run outside the exact harness.

## Failure rule

Once the Task-131 harness process is launched, the one-shot suite authorization is consumed.

If any phase/scenario fails:

- fail-stop immediately;
- do not rerun suite or individual scenario;
- do not substitute another harness or confirmation mechanism;
- permit only the exact harness's built-in best-effort reconciliation if it runs naturally;
- do not manually start/restart/reset/reinstall/normalize afterward under Task 131;
- preserve first-failure evidence.

Any retry would require a new diagnosis/review/task.

## Phase 3 — final deterministic read-only snapshot

Only after exact harness PASS/exit `0`, collect final read-only evidence through the same installed launcher/root authority chain.

Require:

- installed launcher/root authority unchanged;
- ownership/plugin fingerprint unchanged;
- managed state;
- provider `ollama`;
- recovery/check state coherent under the accepted incident semantics;
- no unsafe pending/duplicate recovery operation;
- OpenClaw exact `2026.7.1-2`;
- exactly one current plugin loaded/enabled;
- Gateway healthy;
- Ollama REST version/listener `/api/tags` `/api/ps` recorded;
- final model inventory matches preflight inventory;
- authoritative SQLite read-only integrity exactly `ok`;
- relevant scheduled-task/service state;
- no Dashboard semantic Send.

If final snapshot exposes inconsistency, report FAIL/BLOCKED as appropriate and do not normalize.

## Phase 4 — report and stop

Publish exactly:

`docs/operations/coordination/reports/CNX-20260829-131-v093-real-windows-recovery-reacceptance-authoritative-root.md`

Report must include:

- exact Task-127 candidate/package/harness provenance;
- fresh installed launcher SHA/text-parsed authority and explicit root;
- proof corrected preflight used the installed launcher/root, not workspace parent;
- fresh evidence root;
- preflight status/provider/recovery/ownership/plugin/OpenClaw/Gateway/Ollama/SQLite/service evidence;
- exact true PTY and confirmation evidence;
- literal recovery command and execution path;
- one-shot ledger;
- baseline result;
- gateway-crash before/after PIDs and convergence;
- provider-crash before/after PIDs, incident/circuit/warning details and convergence;
- operator-stop observation and harness-owned restore;
- harness exit/result plus JSON/log paths;
- final deterministic snapshot and model-inventory comparison;
- explicit no Dashboard semantic Send;
- final `PASS`, `FAIL`, or `BLOCKED` with exact first failure.

Then STOP for independent ChatGPT review. Do not automatically open Dashboard durable-delivery acceptance.

## Hard fence

Task 131 does **not** authorize:

- install/install-over;
- reset/uninstall/reinstall;
- standalone start/stop/restart outside the exact harness;
- enable/disable outside reviewed harness behavior;
- source/harness edits;
- alternate/piped/synthetic confirmation;
- provider/model/endpoint/configuration changes;
- OpenClaw/Ollama update/change;
- manual cleanup/normalization;
- generic process-tree kill;
- reboot;
- credentials/secrets access;
- Dashboard semantic Send;
- merge/tag/GitHub Release;
- force push.

Final Dashboard durable-delivery acceptance remains prohibited until Task 131 passes and is independently reviewed.
