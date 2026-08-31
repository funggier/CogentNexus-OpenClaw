# CNX-20260828-122 — Post-Install Verification Recovery and Lifecycle Continuation

- Status: `READY_FOR_HERMES`
- Execution mode: `LIVE_WINDOWS_ACCEPTANCE_CONTINUATION`
- Owner / independent reviewer: ChatGPT
- Executor: Hermes/Codex after operator continuation
- Date: 2026-08-28 ICT
- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`

## Purpose

Recover the missing **read-only post-install proof** from Task 121 without replaying install-over, then continue only the still-unconsumed lifecycle phases if the installed state is proven coherent.

Task 121 already consumed the single authorized install-over attempt and it returned exit code `0`. Task 122 therefore starts from the resulting installed machine state.

## Exact candidate

Retain exactly:

- source SHA `01d08cd7c82f542c821e3a60f7fffa036efb1d75`;
- artifact ID `9691451156`;
- artifact digest `sha256:9db9290e14646575586a42160b79cfea691e35f3a0ca7d294f7f941dcae0c87a`;
- ZIP SHA256 `8e06b186e425170a22bfce06fa3505a7cdac3b097d4bfdc4ccc4d810d502cac1`;
- tar.gz SHA256 `6a14cb665ca6148ce2912970df62027533aef34fb0c871a2e542d1b149e94f31`;
- payload count `178`;
- payload fingerprint `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`.

## Task-121 accepted boundary

Independent review verdict:

`ACCEPTED INCOMPLETE — INSTALL-OVER SUCCEEDED ONCE; POST-INSTALL VERIFICATION HARNESS FAILED; PRODUCT FAILURE NOT PROVEN; INSTALL-OVER IS CONSUMED AND MUST NOT BE REPLAYED`

Consumed attempts:

- install-over: **1 / 1**.

Still unconsumed:

- reset: `0`;
- uninstall: `0`;
- fresh reinstall after uninstall: `0`;
- stop: `0`;
- start: `0`;
- restart: `0`;
- recovery harness: `0`.

## Non-negotiable rules

1. **Never run install-over in Task 122.**
2. Begin with read-only post-install reconciliation only.
3. Every probe must be explicit and non-interactive; no bare `python`, `openclaw`, or `ollama` invocation.
4. Use fully resolved script/executable paths where ambiguity is possible.
5. Bound every probe and capture stdout/stderr/exit code separately.
6. If current installed state cannot be proven coherent, stop with zero new mutation.
7. No manual cleanup, normalization, manifest editing, plugin moving, or ad-hoc live repair.
8. Each remaining disruptive phase may execute at most once.
9. Stop on first non-zero, failed postcondition, ambiguity, or integrity mismatch.
10. No Dashboard semantic Send in this task.

## Phase 0 — fresh branch/task/artifact reconciliation

Before touching live state:

- fetch current branch HEAD and coordination files;
- confirm Task 122 is still active and not superseded;
- confirm no candidate/source substitution;
- confirm Task-121 report/review and the consumed install-over ledger;
- create a new external Task-122 evidence root.

No live mutation.

## Phase 1 — recover post-install proof using non-interactive probes only

Capture the current machine state produced by Task 121.

### 1A — installed CNX state

Use the installed launcher explicitly:

```powershell
cd "$HOME\.openclaw\workspace"
.\cnxclaw.cmd status
.\cnxclaw.cmd check system
.\cnxclaw.cmd check provider
```

These probes must be read-only. Record each separately with exit code.

### 1B — ownership verification

Resolve the installed ownership script path explicitly, e.g.:

```powershell
$OwnershipScript = "$HOME\.openclaw\workspace\skills\cogentnexus-openclaw\scripts\namespace_ownership.py"
python $OwnershipScript verify `
  --root "$HOME\.openclaw\workspace\.cogentnexus-openclaw" `
  --workspace "$HOME\.openclaw\workspace"
```

Do not call bare `python`. First prove the script path exists. Record JSON/output and exit code.

### 1C — OpenClaw/plugin/Gateway proof

Use explicit non-TUI commands only:

```powershell
openclaw --version
openclaw plugins list --json
openclaw gateway status
```

Never call bare `openclaw`.

Require:

- OpenClaw exactly `2026.7.1-2`;
- one coherent current CogentNexus-OpenClaw plugin registration/root;
- no conflicting current generation/wrapper;
- Gateway healthy.

### 1D — runtime/provider preservation

Use explicit non-interactive runtime commands only:

```powershell
ollama --version
ollama list
ollama ps
```

Never call bare `ollama`.

Provider/runtime evidence is a runtime postcondition, not installer policy. Do not change provider/model/endpoint/timeout.

### 1E — SQLite integrity

Use explicit `python -c` or an existing known read-only checker. Never call bare `python`.

Run `PRAGMA integrity_check` on each applicable CNX-owned SQLite database and require exactly `ok`.

### 1F — residue/ownership inventory

Capture read-only:

- ownership manifest contents;
- installed skill/launcher/plugin roots;
- service/task state;
- `.cogentnexus-openclaw` staging/backup/transaction/rollover surfaces;
- legacy generic names (`cnx.cmd`, `cnx`, `skills/cogentnexus`, `.cogent`, `cogentnexus-rotation`);
- current plugin inventory JSON.

Do not delete or normalize anything.

### Phase-1 gate

Proceed only if the current post-install state is coherently proven:

- Task-121 exact candidate is installed/owned;
- ownership verification passes;
- CNX status/checks are coherent;
- plugin root/registration is unique;
- Gateway healthy;
- SQLite integrity `ok`;
- OpenClaw baseline preserved;
- provider runtime/models/data preserved;
- no unsafe mixed ownership or ambiguous active residue.

If not proven: `BLOCKED`, zero new mutations, publish report and stop.

## Phase 2 — reset exactly once

Only after Phase 1 passes.

Run:

```powershell
cd "$HOME\.openclaw\workspace"
.\cnxclaw.cmd reset
```

Provide exactly one normal `y` confirmation. No provider argument.

Verify fresh CNX-owned state is reconstructed while OpenClaw, provider runtime/models/data, and unrelated workspace data remain intact.

Stop on failure; no retry.

## Phase 3 — uninstall exactly once

Run:

```powershell
.\cnxclaw.cmd uninstall
```

Provide exactly one normal `y` confirmation.

Verify only CogentNexus-OpenClaw-owned surfaces are removed; external OpenClaw/provider/unrelated data remain intact. No manual cleanup may be required to claim success.

Stop on failure; no retry.

## Phase 4 — fresh reinstall same artifact exactly once

After successful uninstall only, use the same exact verified artifact and run the canonical provider-neutral installer exactly once:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1 -Workspace "$HOME\.openclaw\workspace"
```

This is the **fresh reinstall** phase, not a replay of Task-121 install-over.

Verify ownership/plugin/runtime/Gateway/SQLite readiness and external-data preservation with the same non-interactive probe discipline.

Stop on failure; no retry.

## Phase 5 — lifecycle controls once each

Run once each in order:

```powershell
.\cnxclaw.cmd stop
.\cnxclaw.cmd start
.\cnxclaw.cmd restart
```

Capture state after each transition. Stop on first failure; do not replay completed transitions.

## Phase 6 — recovery reality harness exactly once

Run exactly once from the exact candidate:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\test-v093-ollama-recovery-windows-v3.ps1 -Scenario all -RunDisruptive
```

Do not alter or manually rerun scenarios.

## Phase 7 — final read-only acceptance snapshot

Capture final proof for:

- exact installed candidate identity;
- CNX status/check-system;
- ownership verification;
- plugin inventory/root uniqueness;
- SQLite integrity `ok`;
- supervisor/task state;
- Gateway health;
- runtime/provider readiness separately;
- OpenClaw exactly `2026.7.1-2`;
- provider runtime/models/data preserved;
- no unexpected transaction/staging/rollover residue;
- no duplicate/pending effect attributable to Tasks 121–122.

## Phase 8 — report and stop

Publish exactly:

`docs/operations/coordination/reports/CNX-20260828-122-post-install-verification-recovery-and-lifecycle-continuation.md`

Report must include:

- fresh evidence root;
- explicit proof Task-121 install-over was **not replayed**;
- every post-install read-only probe command/output/exit code;
- Phase-1 coherence verdict;
- reset/uninstall/fresh-reinstall/stop/start/restart/recovery results and attempt counts;
- final ownership/plugin/SQLite/Gateway/runtime snapshot;
- confirmation no Dashboard semantic Send occurred;
- verdict `PASS`, `FAIL`, or `BLOCKED`;
- first failure boundary if not PASS.

Then stop for independent ChatGPT review. Do not auto-open the final Dashboard durable-delivery task.

## Hard fence

Task 122 does not authorize:

- replay of Task-121 install-over;
- candidate/artifact substitution;
- source edits or ad-hoc live repair;
- manual cleanup/normalization;
- replay of any completed remaining lifecycle phase;
- OpenClaw update/downgrade/reinstall/uninstall/rebaseline;
- provider runtime update/reinstall/reconfiguration;
- provider/model/endpoint/timeout changes;
- unrelated plugin/workspace mutation;
- credential/token/password access;
- Dashboard semantic nonce/message/Send;
- reboot;
- generic process-tree kill;
- merge/tag/GitHub Release/force push.
