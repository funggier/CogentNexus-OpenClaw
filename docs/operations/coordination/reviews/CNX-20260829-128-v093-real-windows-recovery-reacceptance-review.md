# CNX-20260829-128 — Independent Review

## Verdict

**ACCEPTED BLOCKED — Task 128 stopped at the required read-only safety fence before launching the newly authorized recovery suite. No Task-128 disruptive scenario, lifecycle replay, confirmation input, provider mutation, or Dashboard semantic Send occurred. The observed PASSTHROUGH/null-provider state is a precondition failure requiring separate read-only state-root/authority diagnosis; it is not a recovery-product failure.**

## Reviewed inputs

- Task: `docs/operations/coordination/tasks/CNX-20260829-128-v093-real-windows-recovery-reacceptance.md`
- Report: `docs/operations/coordination/reports/CNX-20260829-128-v093-real-windows-recovery-reacceptance.md`
- Accepted Task-127 candidate: `1b922bf400fdbccb1f9c7019b89b69fd67f44070`
- Recovery harness: `scripts/test-v093-ollama-recovery-windows-v3.ps1`
- Harness Git blob: `622f70b339fea0f2ef7c564253aa3c6bf90ffc97`
- Package proof artifact: `9706878201`
- Expected payload fingerprint: `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`
- Task-128 report commit: `b341b2f44da58df502dffeb05c3b4d0d13de1fa9`

## Findings

### 1. Task 128 correctly honored the Phase-0 hard fence

The required live precondition was not proven safe:

- reported host mode: `passthrough`, not `managed`;
- reported host selected provider: `null`, not `ollama`;
- provider status selected provider: `null`;
- recovery verdict was warning-bearing rather than a coherent managed pre-disruption baseline;
- supervisor health snapshot was not established;
- SQLite integrity `ok` was not proven because the status-reported database path did not exist under the probe used.

The Task-128 contract explicitly required `BLOCKED` rather than using `start`, `restart`, install, reset, provider selection, or manual normalization to manufacture a precondition. The executor followed that rule.

### 2. No Task-128 recovery authorization was consumed

Accepted ledger:

- Task-128 recovery suite: `0 / 1 launched`;
- interactive confirmation prompt: not reached;
- lowercase `y`: not entered;
- baseline: `0`;
- gateway-crash: `0`;
- provider-crash: `0`;
- operator-stop: `0`.

Therefore a future task may separately authorize one recovery execution after the precondition problem is independently resolved. Task 128 itself remains closed and must not be resumed ad hoc.

### 3. No new live mutation is evidenced

The report records no install/install-over, reset, uninstall/reinstall, standalone stop/start/restart, provider/model/config mutation, process kill, cleanup/normalization, reboot, or Dashboard semantic Send. The report commit is coordination/report-only relative to the Task-128 activation head.

### 4. The PASSTHROUGH observation is not yet classified as genuine product state drift

The accepted installer constructs the installed `cnxclaw.cmd` launcher to invoke the installed `skills\cogentnexus-openclaw\scripts\cnxclaw_v093.py` and explicitly supplies `--root <workspace>\.cogentnexus-openclaw`. The v0.9.3 facade preserves that global root parsing and the accepted backend reads controller/provider/check state from the supplied root.

Consequently, current working directory alone should not cause a wrong-root status when the installed launcher is actually used. However, the Task-128 report does not preserve the literal preflight launcher path/command or launcher bytes/target, so it does not independently prove that the status/provider/recovery observations came through the intended installed launcher-to-root chain.

This is an evidence gap, not evidence that Task 128 should have proceeded. The safe decision remains BLOCKED.

### 5. Historical state makes read-only diagnosis mandatory before any re-entry

Task 125's exact harness built-in `cleanup-start` and cleanup baseline had returned the system to a healthy managed state after the old-harness provider-convergence failure. Task 126 classified the live provider recovery itself as coherent. Task 128 later observed PASSTHROUGH/null provider while ownership, exact plugin fingerprint, OpenClaw, Gateway, Ollama, models, and scheduled tasks were still present/healthy.

That discontinuity must be explained before any command is allowed to re-enter managed mode. A blind `start`/`restart` could erase the evidence needed to distinguish:

1. genuine authoritative controller/state drift;
2. launcher/target/root mismatch;
3. alternate/stale CNX state root;
4. status/SQLite path interpretation defect;
5. an authorized or autonomous transition after Task 125.

## Required successor

Open a **read-only managed-state / state-root authority diagnosis** only.

The successor must not run the recovery suite and must not use install, reset, uninstall/reinstall, start, stop, restart, enable/disable, provider selection, process kill, cleanup, normalization, or Dashboard Send.

It should establish, with literal paths and hashes:

- the exact installed `cnxclaw.cmd` bytes and its Python/CLI/root target;
- the explicit installed-launcher status/provider/recovery outputs;
- exact controller/state/runtime/ownership/SQLite paths under the launcher-supplied root;
- any other `.cogentnexus-openclaw` roots and their provenance/mtime/generation without modifying them;
- scheduled-task/service executable, arguments, working directory, and state-root authority;
- relevant non-secret environment path overrides;
- controller generation/mode/provider transition history available from durable files/logs;
- comparison against Task-125 final cleanup evidence;
- whether the missing SQLite probe was pointed at the authoritative installed database path.

Only after independent review of that diagnosis may a later task authorize a controlled managed-state re-entry or a new recovery acceptance execution.

## Dashboard gate

Final Dashboard durable-delivery acceptance remains prohibited.
