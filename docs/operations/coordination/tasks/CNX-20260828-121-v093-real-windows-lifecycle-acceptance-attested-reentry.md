# CNX-20260828-121 — v0.9.3 Real-Windows Lifecycle Acceptance — Attested Re-entry

- Status: `READY_FOR_HERMES`
- Execution mode: `LIVE_WINDOWS_ACCEPTANCE`
- Owner / independent reviewer: ChatGPT
- Executor: Hermes/Codex after operator continuation
- Date: 2026-08-28 ICT
- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`

## Purpose

Retry the bounded real-Windows lifecycle acceptance using the same exact provider-neutral candidate as Task 120, but correct the read-only ownership-classification preflight so it mirrors the candidate's production attestation contract.

Task 120 performed **zero destructive mutations** and stopped because its acceptance task invoked `classify-install` without the plugin inventory and candidate plugin fingerprint needed for interrupted-rollover/re-entry classification.

Task 121 is a new explicit authorization. It is not permission to replay the incomplete Task-120 classifier blindly or to normalize the live machine manually.

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

Exact-SHA CI already accepted:

- Validate `33185349482` — success;
- Windows Installer Pack Smoke `33185349413` — success;
- PS5.1 Acceptance Smoke `33185349400` — success.

Do not substitute a newer checkout, repack the source, or use another artifact.

## Accepted Task-120 review finding

Task-120 report:

`docs/operations/coordination/reports/CNX-20260828-120-v093-real-windows-lifecycle-acceptance-provider-neutral-candidate.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260828-120-v093-real-windows-lifecycle-acceptance-provider-neutral-candidate-review.md`

Accepted verdict:

`ACCEPTED BLOCKED — HARD FENCE WORKED; BLOCK WAS CAUSED BY AN INCOMPLETE ACCEPTANCE-CLASSIFIER INVOCATION, NOT BY A PROVEN LIVE OWNERSHIP FAILURE`

No install-over/reset/uninstall/reinstall/lifecycle/recovery phase ran in Task 120.

## Architectural boundary

Installation remains provider-neutral. The installer command is exactly:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1 -Workspace "$HOME\.openclaw\workspace"
```

No installer `-Provider` argument is allowed.

Runtime/provider readiness remains a separate runtime postcondition.

## Non-negotiable execution rules

1. Fresh exact-artifact provenance before live mutation.
2. Fresh read-only machine reconciliation before live mutation.
3. The read-only classifier must use production-equivalent attestation inputs.
4. Every disruptive phase is attempted at most once in Task 121.
5. Stop immediately on first non-zero exit, failed postcondition, ambiguous classification, or evidence mismatch.
6. Do not manually edit/move/delete/normalize ownership, plugin, state, manifest, transaction, backup, or staging residue to continue.
7. Do not replay a completed disruptive phase because a watcher/session restarts.
8. Preserve post-failure evidence before stopping.
9. No Dashboard semantic message/nonce/Send in this task.

## Phase 0 — exact artifact provenance, no live mutation

Create a new Task-121 acceptance-evidence root.

Verify the exact pinned artifact/source identity again, including:

- artifact ID/name/digest;
- source SHA and package version;
- ZIP/tar.gz hashes;
- package/payload identities;
- payload count/fingerprint;
- packaged provider-neutral PowerShell/POSIX installers;
- packaged canonical install docs.

If any identity differs: `BLOCKED`, no live mutation.

## Phase 1 — fresh read-only machine reconciliation

Capture fresh read-only evidence for at least:

- timestamp / Windows / PowerShell;
- OpenClaw exact version, expected `2026.7.1-2`;
- CNX status and `check system` if launcher exists;
- runtime/provider health as a separate runtime fact;
- Gateway status;
- SQLite `PRAGMA integrity_check` on applicable owned databases;
- supervisor/task/service state;
- raw ownership manifest contents;
- current OpenClaw plugin inventory JSON;
- plugin roots/generations/load/config paths;
- current/legacy namespace inventory;
- `.cogentnexus-openclaw` backup/staging/transaction/rollover residue.

No live state mutation is permitted in this phase.

### Phase 1A — production-equivalent candidate plugin attestation

Inside the **verified extracted candidate boundary only** (not the live OpenClaw plugin root), prepare the candidate plugin exactly as the installer does before classification:

```powershell
Push-Location .\plugins\cogentnexus-openclaw
npm ci
npm run plugin:validate
Pop-Location
```

This may modify only the isolated verified candidate extraction (`node_modules`/npm preparation). It must not modify the live OpenClaw workspace/plugin registration/runtime.

Then compute the exact candidate plugin fingerprint using the candidate ownership tool, e.g.:

```powershell
python .\skills\cogentnexus-openclaw\scripts\namespace_ownership.py plugin-fingerprint --plugin-root .\plugins\cogentnexus-openclaw --version 0.9.3
```

Require a 64-hex fingerprint and record the full JSON output. Do not substitute the repository payload-v2 fingerprint for this plugin fingerprint unless the command itself proves they are equal.

### Phase 1B — current OpenClaw inventory attestation

Capture current inventory read-only:

```powershell
openclaw plugins list --json
```

Write the exact JSON to a Task-121 evidence file without editing it.

### Phase 1C — attested `classify-install`

Run the exact candidate's classifier with **both** attestation inputs:

```powershell
python .\skills\cogentnexus-openclaw\scripts\namespace_ownership.py classify-install `
  --workspace "$HOME\.openclaw\workspace" `
  --app-data "$env:LOCALAPPDATA\CogentNexus-OpenClaw" `
  --plugin-inventory-json <TASK121_EXACT_PLUGIN_INVENTORY_JSON> `
  --expected-replacement-fingerprint <TASK121_CANDIDATE_PLUGIN_FINGERPRINT>
```

Use paths inside the verified candidate extraction.

The classification must be coherent with the fresh manifest, filesystem, and OpenClaw inventory. An interrupted-rollover/re-entry result is acceptable only when the classifier itself proves it through this attested path.

Do **not** manually infer or force `upgrade`, `pluginAlreadyExact`, `pendingRollover`, or `interruptedRolloverReentry` values.

If classification remains non-zero/ambiguous, or any ownership/integrity/baseline fact is unsafe: `BLOCKED`, no mutation.

## Phase 2 — install-over exactly once

Only after Phase 0 and the complete Phase-1 attested gate pass.

Execute from the verified candidate extraction exactly once:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1 -Workspace "$HOME\.openclaw\workspace"
```

No `-Provider` argument.

Record exact stdout/stderr/exit code and post-install read-only evidence.

Required postconditions:

- installer success;
- ownership manifest verifies after convergence;
- plugin registration/root coherent and unique;
- no conflicting current product generation/wrapper;
- no unsafe legacy namespace adoption;
- CNX reaches expected managed/ready runtime state;
- configured runtime/provider remains coherent as a runtime fact;
- Gateway healthy;
- SQLite integrity `ok`;
- external OpenClaw/provider runtime/data preserved.

Stop on first failure; no retry.

## Phase 3 — reset exactly once

Run:

```powershell
.\cnxclaw.cmd reset
```

Provide exactly one normal `y` confirmation.

No provider argument.

Verify CNX-owned fresh-state reconstruction while preserving OpenClaw, provider runtime/models/data, and unrelated workspace data.

Stop on first failure; no retry.

## Phase 4 — uninstall exactly once

Run:

```powershell
.\cnxclaw.cmd uninstall
```

Provide exactly one normal `y` confirmation.

Verify only CogentNexus-OpenClaw-owned surfaces are removed and external OpenClaw/provider/unrelated data remain intact. No manual cleanup may be required to claim success.

Stop on first failure; no retry.

## Phase 5 — fresh reinstall same artifact exactly once

Using the same verified artifact (clean extraction or re-proven exact extraction), run exactly once:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1 -Workspace "$HOME\.openclaw\workspace"
```

No provider argument.

Verify ownership/plugin/runtime/Gateway/SQLite readiness and external-data preservation.

Stop on first failure; no retry.

## Phase 6 — lifecycle controls once each

Run once each, in order:

```powershell
.\cnxclaw.cmd stop
.\cnxclaw.cmd start
.\cnxclaw.cmd restart
```

No provider argument.

Capture and verify each transition before proceeding.

Stop on first failure; do not replay completed transitions.

## Phase 7 — recovery reality harness exactly once

Provider-specific knowledge is legitimate here because this is runtime/recovery behavior.

Run exactly once:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\test-v093-ollama-recovery-windows-v3.ps1 -Scenario all -RunDisruptive
```

Use the exact candidate harness. Do not modify or manually rerun scenarios.

Stop on failure.

## Phase 8 — final read-only acceptance snapshot

Capture final proof for:

- installed exact candidate identity;
- CNX status/check-system;
- ownership manifest verification;
- plugin inventory/root uniqueness;
- no conflicting/legacy current namespace;
- SQLite integrity `ok`;
- supervisor/service/task state;
- Gateway health;
- runtime/provider readiness separately;
- OpenClaw exactly `2026.7.1-2`;
- provider runtime/models/data preserved;
- no unexpected transaction/staging/rollover residue;
- no pending/duplicate effect attributable to Task 121.

## Phase 9 — report and stop

Publish exactly:

`docs/operations/coordination/reports/CNX-20260828-121-v093-real-windows-lifecycle-acceptance-attested-reentry.md`

The report must include:

- exact candidate/artifact identity/hashes;
- fresh pre-mutation evidence root;
- candidate plugin fingerprint command/output;
- exact plugin inventory evidence file;
- full attested classifier command/output;
- exact classification fields;
- exact commands/timestamps/exit codes for every phase;
- proof each disruptive phase ran no more than once;
- install-over/reset/uninstall/reinstall/lifecycle/recovery results;
- final ownership/plugin/SQLite/Gateway/runtime snapshot;
- confirmation no Dashboard semantic Send occurred;
- verdict `PASS`, `FAIL`, or `BLOCKED`;
- first failure boundary/root cause if not PASS.

Then stop for independent ChatGPT review.

Do not create or execute the final Dashboard durable-delivery task automatically.

## Hard fence

Task 121 does not authorize:

- candidate/artifact substitution;
- source edits or ad-hoc live repair;
- manual manifest/plugin/state cleanup or normalization;
- replay of failed/completed disruptive phases;
- OpenClaw update/downgrade/reinstall/uninstall/rebaseline;
- provider runtime update/reinstall/reconfiguration;
- provider/model/endpoint/timeout changes;
- unrelated plugin/workspace mutation;
- credential/token/password access or re-entry;
- Dashboard semantic nonce/message/Send;
- reboot;
- generic process-tree kill;
- merge/tag/GitHub Release/force push.
