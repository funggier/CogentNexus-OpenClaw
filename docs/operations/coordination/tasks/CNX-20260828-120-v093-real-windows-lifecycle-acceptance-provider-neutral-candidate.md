# CNX-20260828-120 — v0.9.3 Real-Windows Lifecycle Acceptance — Provider-Neutral Candidate

- Status: `READY_FOR_HERMES`
- Execution mode: `LIVE_WINDOWS_ACCEPTANCE`
- Owner / independent reviewer: ChatGPT
- Executor: Hermes/Codex after operator continuation
- Date: 2026-08-28 ICT
- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`

## Purpose

Run the bounded real-Windows lifecycle acceptance against the newly accepted provider-neutral installer candidate after Tasks 117–119.

This is a **new acceptance task**, not a replay or continuation of Task 116. Task 116 remains historical failure evidence only.

## Exact frozen candidate

Use exactly:

- source SHA: `01d08cd7c82f542c821e3a60f7fffa036efb1d75`;
- package version: `0.9.3`;
- GitHub Actions artifact ID: `9691451156`;
- artifact name: `cogentnexus-openclaw-v0.9.3-package-proof-01d08cd7c82f542c821e3a60f7fffa036efb1d75`;
- GitHub artifact digest: `sha256:9db9290e14646575586a42160b79cfea691e35f3a0ca7d294f7f941dcae0c87a`;
- package ZIP SHA256: `8e06b186e425170a22bfce06fa3505a7cdac3b097d4bfdc4ccc4d810d502cac1`;
- package tar.gz SHA256: `6a14cb665ca6148ce2912970df62027533aef34fb0c871a2e542d1b149e94f31`;
- payload file count: `178`;
- payload V2 fingerprint: `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`.

Exact-SHA CI already independently accepted:

- Validate `33185349482` — success;
- Windows Installer Pack Smoke `33185349413` — success;
- PS5.1 Acceptance Smoke `33185349400` — success.

Do not substitute a newer branch checkout, a repacked worktree, or a different artifact.

## Architectural boundary

Installation is provider-neutral.

The Windows installer command for this task is exactly:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1 -Workspace "$HOME\.openclaw\workspace"
```

Do **not** pass `-Provider`.

Provider/runtime readiness is a separate runtime postcondition. Current v0.9.3 runtime policy may still be Ollama-aware where runtime/recovery actually owns that behavior. Do not interpret provider-neutral installation as multi-provider runtime support.

## Non-negotiable execution rules

1. Fresh read-only reconciliation **before any live mutation**.
2. Every disruptive phase is attempted at most once.
3. Stop immediately on the first non-zero exit, failed postcondition, ambiguous ownership/classification, or evidence mismatch.
4. Do not manually normalize/clean residue in order to continue.
5. Do not replay a completed disruptive phase because a watcher/session/task restarts.
6. Preserve all post-failure evidence before stopping.
7. No Dashboard semantic message/nonce/Send in this task.

## Phase 0 — exact artifact provenance, no live mutation

Create a fresh external acceptance-evidence root under the existing CogentNexus-OpenClaw acceptance evidence boundary.

Download/reuse only artifact `9691451156` and verify before touching live state:

- artifact ID/name;
- artifact/source SHA binding;
- artifact digest where available;
- package ZIP/tar.gz SHA256;
- `PACKAGE_IDENTITY.json`;
- `PAYLOAD_IDENTITY.json`;
- `SHA256SUMS.txt`;
- package version;
- payload count/fingerprint;
- packaged `scripts/install.ps1` has no `Provider` parameter/default/ValidateSet, no provider executable prerequisite, and no provider-bearing lifecycle handoff;
- packaged `scripts/install.sh` is likewise provider-neutral;
- packaged/current install docs contain provider-free Windows/POSIX source-install commands.

Record a fresh provenance file before machine mutation.

If identity differs in any way: `BLOCKED`, no mutation.

## Phase 1 — fresh read-only machine reconciliation

Do not assume Task-116 state is still current.

Capture fresh read-only evidence for at least:

- current timestamp and PowerShell version;
- OpenClaw version — expected exact baseline `2026.7.1-2`;
- current CNX status/check-system output if launcher exists;
- current runtime/provider status as a **separate runtime fact**;
- Gateway status;
- SQLite `PRAGMA integrity_check` for owned Ticket/runtime databases as applicable;
- supervisor/service/task state;
- ownership manifest contents/verification;
- exact current OpenClaw plugin inventory JSON;
- current plugin root/generation and load/config paths;
- legacy generic namespace inventory: `cnx.cmd`, `cnx`, `skills/cogentnexus`, `.cogent`, `cogentnexus-rotation`;
- current `.cogentnexus-openclaw` staging/backup/transaction/rollover residue;
- any prior Task-107/116 transaction residue still present.

Then run the **pinned candidate's** read-only classifier:

```powershell
python .\skills\cogentnexus-openclaw\scripts\namespace_ownership.py classify-install --workspace "$HOME\.openclaw\workspace" --app-data "$env:LOCALAPPDATA\CogentNexus-OpenClaw"
```

Use the correct path inside the verified extracted candidate if the relative path differs.

Expected historical shape may still resemble interrupted upgrade/re-entry, but **do not require stale Task-116 values**. Accept only a classification that is coherent with fresh evidence and supported by the current classifier contract.

If classification is ambiguous, legacy/current namespaces are mixed unexpectedly, ownership cannot be proven, SQLite is not `ok`, OpenClaw baseline differs, or runtime state is unsafe: `BLOCKED`, no mutation.

## Phase 2 — install-over exactly once

Only after Phases 0–1 pass.

From the verified candidate extraction, execute exactly once:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1 -Workspace "$HOME\.openclaw\workspace"
```

No `-Provider` argument.

Record stdout/stderr/exit code and post-install read-only evidence.

Required postconditions include:

- installer completed successfully;
- current ownership manifest verifies;
- current plugin registration/root is coherent and unique;
- no active conflicting product wrapper/generation;
- no unsafe legacy namespace adoption;
- CNX runtime reaches its expected managed/ready state;
- configured runtime/provider state is coherent and no installer-level provider selection occurred;
- Gateway is healthy;
- SQLite integrity remains `ok`;
- external OpenClaw/provider runtime/data remain present.

If any condition fails: stop. Do not retry install-over.

## Phase 3 — reset exactly once

Run the installed current launcher reset once using the normal confirmation path:

```powershell
.\cnxclaw.cmd reset
```

Provide exactly one normal `y` confirmation when prompted.

Do not pass a provider argument.

Verify reset reconstructs fresh CNX-owned state while preserving external OpenClaw, provider runtime/models/data, and unrelated workspace namespaces.

If non-zero/ambiguous: stop; no retry.

## Phase 4 — uninstall exactly once

Run:

```powershell
.\cnxclaw.cmd uninstall
```

Provide exactly one normal `y` confirmation.

Required uninstall proof:

- current CogentNexus-OpenClaw-owned launchers/state/skill/plugin/service/task surfaces are removed according to contract;
- no active current product registration remains;
- generic historical names are not left as ambiguous owned residue;
- external OpenClaw remains installed and version `2026.7.1-2`;
- external provider runtime/models/data remain intact;
- unrelated workspace/user data remain intact;
- no manual cleanup is required to claim success.

If non-zero/ambiguous: stop; do not retry or manually clean.

## Phase 5 — fresh reinstall from the same exact artifact exactly once

Use a clean extraction of the **same verified artifact** or otherwise prove the extracted source still matches the pinned candidate before execution.

Execute exactly once:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1 -Workspace "$HOME\.openclaw\workspace"
```

No provider argument.

Verify fresh ownership, plugin uniqueness, launcher/state/skill installation, runtime readiness, Gateway readiness, SQLite integrity, and preservation of external dependencies/data.

If non-zero/ambiguous: stop; no retry.

## Phase 6 — lifecycle controls once each

With the freshly installed exact candidate, run once each in this order:

```powershell
.\cnxclaw.cmd stop
.\cnxclaw.cmd start
.\cnxclaw.cmd restart
```

No provider argument.

After each command, capture state and verify the requested transition completed without duplicate ownership/effects.

Stop on first failure; do not replay any completed transition.

## Phase 7 — recovery reality harness exactly once

This is a **runtime/recovery** phase, where provider-specific knowledge is legitimate because the current v0.9.3 runtime/recovery implementation is Ollama-based.

Run the reviewed recovery harness exactly once:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\test-v093-ollama-recovery-windows-v3.ps1 -Scenario all -RunDisruptive
```

Use the harness from the exact candidate. Do not modify its scenarios or rerun failed scenarios manually.

Require its normal acceptance postconditions and preserve full output/evidence.

If it fails: stop; no rerun.

## Phase 8 — final read-only acceptance snapshot

Capture final evidence for:

- exact installed candidate/source identity;
- CNX status/check system;
- ownership manifest verify;
- exact OpenClaw plugin inventory/root uniqueness;
- no legacy/conflicting namespace;
- SQLite integrity `ok`;
- supervisor/service state;
- Gateway health;
- runtime/provider readiness as separate runtime evidence;
- OpenClaw remains exactly `2026.7.1-2`;
- external provider runtime/models/data preserved;
- no unexpected staging/transaction/rollover residue;
- no pending/duplicate lifecycle effect attributable to this task.

## Phase 9 — report and stop

Publish exactly:

`docs/operations/coordination/reports/CNX-20260828-120-v093-real-windows-lifecycle-acceptance-provider-neutral-candidate.md`

Report must include:

- exact candidate/artifact identity and all verified hashes;
- fresh pre-mutation machine classification;
- exact commands, timestamps, exit codes, and evidence paths for every phase;
- explicit proof each disruptive phase ran no more than once;
- install-over result;
- reset result;
- uninstall preservation/removal result;
- fresh reinstall result;
- stop/start/restart result;
- recovery harness result;
- final ownership/plugin/SQLite/Gateway/runtime snapshot;
- confirmation no Dashboard semantic Send occurred;
- verdict `PASS`, `FAIL`, or `BLOCKED`;
- first failure boundary/root cause if not PASS.

Then stop for independent ChatGPT review.

Do **not** automatically create or execute the final Dashboard durable-delivery task.

## Hard fence

This task does not authorize:

- any package/candidate substitution;
- source edits or ad-hoc repair on the live machine;
- retry/replay of a failed or completed disruptive phase;
- manual cleanup/normalization to force continuation;
- OpenClaw update/downgrade/reinstall/uninstall/rebaseline;
- provider runtime update/reinstall/reconfiguration;
- provider/model/endpoint/timeout changes;
- unrelated plugin/workspace mutation;
- credential/token/password access or re-entry;
- Dashboard semantic nonce/message/Send;
- reboot;
- generic process-tree kill;
- merge/tag/GitHub Release/force push.
