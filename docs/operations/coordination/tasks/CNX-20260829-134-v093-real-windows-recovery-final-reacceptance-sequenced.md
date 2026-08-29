# CNX-20260829-134 — v0.9.3 Real-Windows Recovery Final Re-Acceptance (Sequenced Harness)

- Status: `READY_FOR_HERMES`
- Execution mode: `LIVE_WINDOWS_RECOVERY_ACCEPTANCE_ONLY`
- Owner / independent reviewer: ChatGPT
- Executor: Hermes/Codex after operator continuation
- Date: 2026-08-29 ICT
- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`

## Purpose

Run one new real-Windows recovery acceptance against the exact Task-133 accepted candidate after Task 132/133 repaired and behaviorally proved the remaining provider-crash → operator-stop sequencing defect.

This is a new one-shot authorization. It does not resume or replay Task 131's consumed suite and does not authorize installer/lifecycle phases outside the exact recovery harness.

## Accepted exact candidate

Source candidate:

`1424d6fbee2c458c8c30440616783d2fa1bc1201`

Exact recovery harness:

- path: `scripts/test-v093-ollama-recovery-windows-v3.ps1`
- Git blob: `a4138e00e2056db89b0a9eceed1b54e001c4e319`

Fresh package proof:

- artifact ID: `9709798190`
- artifact name: `cogentnexus-openclaw-v0.9.3-package-proof-1424d6fbee2c458c8c30440616783d2fa1bc1201`
- GitHub outer artifact digest: `sha256:e8dbb2f742bfeffc93a80a7cda62a8c273ced9e2b1e9b47a3962dead52ccfeef`
- payload count: `178`
- payload/plugin fingerprint: `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`
- inner tar.gz SHA256: `33be3ccea56bae7926c371d37e46f30dbec39364380b9bb5601e5d9a6e073a9a`
- inner ZIP SHA256: `cfe1c6cfccd298849b0d9c5f0a4603848f27c50c3b579629538616fd72ec81c1`

Exact-SHA workflows all passed:

- Validate `33235544556`
- PS5.1 v0.9.3 Ollama Recovery V3 Smoke `33235544569`
- PS5.1 Acceptance Smoke `33235544559`
- Windows Installer Pack Smoke `33235544603`

Task-133 independent review:

`docs/operations/coordination/reviews/CNX-20260829-133-recovery-sequencing-behavioral-matrix-and-package-proof-closeout-review.md`

Accepted verdict authorizes a new separately controlled live recovery re-acceptance only.

## Why no reinstall is authorized

Changes from the last live-tested candidate are confined to the recovery acceptance harness and its non-disruptive self-test/test proof. Installed runtime/provider/plugin production behavior was not changed.

The package payload/plugin fingerprint remains exactly:

`3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`

Use the exact candidate harness from an isolated checkout/package extraction while the harness invokes the installed `cnxclaw.cmd` for live state. Do not install or install-over.

If fresh source/history inspection contradicts this assumption, stop `BLOCKED` before disruption.

## Historical live ledger

Remain consumed/closed:

- Task-121 install-over: `1 / 1`
- Task-124 reset: `1 / 1`
- Task-124 uninstall: `1 / 1`
- Task-124 fresh reinstall: `1 / 1`
- Task-124 standalone stop/start/restart: `1 / 1` each
- Task-125 old-harness recovery suite: `1 / 1`
- Task-128 repaired-harness suite: `0 / 1`, closed blocked
- Task-131 repaired-harness suite: `1 / 1`, consumed
- Task-131 baseline: PASS
- Task-131 gateway-crash: PASS
- Task-131 provider-crash: PASS
- Task-131 operator-stop: `0`, not reached

Task 134 creates exactly one new ledger:

- exact Task-133 recovery suite: maximum `1 / 1`
- interactive confirmation: maximum one lowercase `y` after the exact prompt
- baseline/gateway-crash/provider-crash/operator-stop only inside that single harness process

No suite/scenario rerun is permitted after launch.

## Phase 0 — authority and fresh safe preflight

Before disruption:

1. Fresh-fetch branch/coordination and confirm Task 134 remains authoritative and unsuperseded.
2. Verify exact candidate `1424d6fbee2c458c8c30440616783d2fa1bc1201` and harness blob `a4138e00e2056db89b0a9eceed1b54e001c4e319`.
3. Materialize an isolated exact candidate checkout/worktree or exact package extraction. Do not modify the installed workspace.
4. Verify the execution-copy harness bytes/hash exactly.
5. Confirm no installed runtime/plugin/installer production deployment change requires reinstall.

### Authoritative root discipline

All external CNX preflight/final probes must use the explicit installed launcher:

`C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd`

Freshly read/hash/parse it and record:

- Python executable/path authority;
- installed `cnxclaw_v093.py` path;
- explicit state root;
- `%*` forwarding.

Require explicit root:

`C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw`

Never substitute the workspace parent as `--root`.

### Required already-safe preflight

Using direct argument-safe installed-launcher calls, require:

- coherent mode `managed`;
- desired Gateway/provider `running`;
- selected provider `ollama` in host/provider views;
- recovery verdict exact `READY`;
- no active unsafe provider incident/circuit/transition;
- ownership verification PASS;
- installed plugin fingerprint exact `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`;
- OpenClaw exactly `2026.7.1-2`;
- exactly one current CogentNexus-OpenClaw plugin loaded/enabled;
- Gateway listener/process healthy;
- Ollama REST/listener healthy; record version and model inventory;
- authoritative SQLite exists and read-only URI-mode `PRAGMA integrity_check` returns exactly `ok`;
- Supervisor/OpenClaw task/service state recorded;
- no duplicate active recovery operation.

If any requirement is not already safe, stop `BLOCKED`; do not manufacture preconditions with start/restart/reset/install/provider selection or normalization.

## Phase 1 — true interactive confirmation

The exact harness uses:

`Read-Host 'Type y to continue'`

Requirements:

- use a true interactive PowerShell PTY/console;
- invoke the exact harness directly;
- no generic wrapper that changes command/arguments;
- no piping/redirection/synthetic input/patching;
- wait for exact `Type y to continue:` prompt;
- enter exactly one lowercase `y` followed by Enter;
- require `explicit-disruptive-confirmation = PASS` evidence.

If a true PTY cannot be guaranteed, stop `BLOCKED` before disruptive launch.

## Phase 2 — exact one-shot suite

Canonical logical command:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File <EXACT-CANDIDATE-PATH>\scripts\test-v093-ollama-recovery-windows-v3.ps1 -Scenario all -RunDisruptive
```

Record the literal absolute command/path.

### Baseline

Require PASS with strict ordinary `READY`.

### Gateway-crash

Require:

- exact validated Gateway listener PID targeted;
- no process-tree kill;
- different recovered Gateway listener PID;
- listener healthy;
- durable convergence PASS;
- strict ordinary `READY`;
- scenario PASS.

### Provider-crash

Require:

- exact validated Ollama listener PID targeted;
- no process-tree kill;
- different recovered Ollama listener PID;
- provider circuit closed;
- durable convergence PASS under the accepted provider-incident contract;
- if `READY_WITH_WARNINGS`, exactly one WARN = the single open/circuit-closed Provider recovery incident, all other checks PASS;
- exact incident ID/classification carried by the harness when applicable;
- no artificial model completion/normalization;
- scenario PASS.

### Provider→operator sequence boundary

This is the repaired Task-132/133 acceptance target.

If provider-crash PASSed with the intentional open incident, require `operator-before` to accept **only** that exact same carried incident:

- same harness process;
- immediately preceding scenario `provider-crash`;
- exact non-empty incident ID match;
- classification match where present;
- verdict `READY_WITH_WARNINGS`;
- exactly one WARN, the Provider recovery incident;
- incident open;
- circuit closed;
- no FAIL/INDETERMINATE;
- every other recovery check PASS;
- exactly one adapter row with `expected=false`;
- managed/Ollama structural state;
- Gateway/Ollama listeners healthy.

Record carried incident ID and boundary evidence.

### Operator-stop

After the sequence-aware boundary passes, require:

- only harness-owned `cnxclaw stop`;
- maintenance state with desired Gateway/provider stopped;
- Gateway stops and remains stopped throughout intentional observation;
- no automatic recovery while intentional stop is active;
- only harness-owned `start-after-intentional-stop` restores operation;
- Gateway/Ollama listeners return;
- post-start convergence is strict ordinary `READY` with no carried-warning exception;
- scenario PASS.

### Suite result

Require process exit `0`, suite result `PASS`, and all four scenarios PASS.

## Failure rule

Once the harness process launches, Task-134 suite authorization is consumed.

On any failure:

- fail-stop;
- no suite rerun;
- no individual scenario rerun;
- no alternate harness/confirmation;
- only harness built-in best-effort reconciliation may run naturally;
- no manual start/restart/reset/install/reinstall/provider/config/state/database normalization;
- preserve first-failure evidence.

A deterministic read-only final snapshot is allowed after harness exit to preserve state evidence, but it must not mutate or normalize anything.

Any further disruptive retry requires a new task and independent diagnosis/review.

## Phase 3 — final read-only snapshot

After harness exit, collect read-only evidence through the same authoritative installed launcher/root:

- mode/desired state/provider;
- recovery verdict/checks/incident/circuit;
- no pending/duplicate recovery;
- OpenClaw exact version;
- one current plugin;
- exact installed fingerprint unchanged;
- Gateway listener/process;
- Ollama REST/listener/version/`/api/tags`/`/api/ps` and model inventory;
- final model inventory equals preflight inventory;
- SQLite `integrity_check=ok`;
- Supervisor/OpenClaw task/service state;
- outbox/status residue classification;
- no Dashboard Send.

If suite exit is PASS but final snapshot is inconsistent, verdict is FAIL/BLOCKED; do not normalize.

## Required report

Publish exactly:

`docs/operations/coordination/reports/CNX-20260829-134-v093-real-windows-recovery-final-reacceptance-sequenced.md`

Report must include:

- exact start coordination HEAD;
- exact candidate/harness/package proof identity;
- no-reinstall proof;
- preflight launcher/root authority and read-only evidence;
- PTY/prompt/one lowercase `y` evidence;
- literal suite command;
- one-shot ledger;
- baseline result;
- Gateway before/after PIDs and convergence;
- provider before/after PIDs, incident/circuit/checks and convergence;
- provider→operator carried incident ID/boundary evidence;
- intentional stop/no-auto-recovery/start/post-start strict READY evidence;
- harness exit/result/evidence paths;
- final read-only snapshot/model inventory/SQLite/task state;
- explicit no manual normalization and no Dashboard Send;
- final PASS/FAIL/BLOCKED and first failure if any.

Then STOP for independent ChatGPT review. Do not open Dashboard durable-delivery acceptance automatically.

## Hard fence

No install/install-over/reset/uninstall/reinstall; no standalone lifecycle outside the exact harness; no source/harness edit; no alternate confirmation; no provider/model/OpenClaw/config mutation; no manual normalization; no generic process-tree kill; no task/service mutation outside observation; no reboot; no credentials/secrets; no Dashboard semantic Send; no merge/tag/release; no force push.
