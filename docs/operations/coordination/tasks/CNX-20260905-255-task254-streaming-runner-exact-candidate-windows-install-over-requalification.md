# CNX-20260905-255 — Task-254 Streaming-Runner Exact-Candidate Windows Install-Over Requalification

Status: `READY_FOR_HERMES`  
Executor: Hermes / authenticated Windows operator  
Coordinator / independent reviewer: ChatGPT  
Parent task: `CNX-20260905-254`  
Parent review: `docs/operations/coordination/reviews/CNX-20260905-254-task253-target-child-identity-binding-tdd-repair-review.md`  
Parent umbrella: `CNX-20260831-188`

## Objective

Perform exactly one live Windows install-over requalification of the Task254 exact candidate using the repository-owned streaming diagnostic runner as the durable evidence boundary.

This task exists because Task251 proved that the previous buffered runner could lose all child evidence when the Scheduled Task hit its `PT45M` execution limit, while Task253/254 now prove a streaming runner that:

- writes child stdout/stderr durably while the target is alive;
- binds `child-started.json.pid` to the actual manifest target process;
- leaves no target-start artifact when target launch fails;
- preserves already-emitted evidence if the outer runner is terminated.

This task MUST NOT increase the scheduler execution limit as a symptom fix. Keep the first live requalification at the known `PT45M` boundary so a repeated stall produces bounded stage evidence.

## Exact candidate identities

Required executable candidate:

`6822af464fe7a5cb3f93305d0263dfc86b56ac68`

Required streaming runner:

`scripts/manifest-streaming-runner.ps1`

Expected SHA-256:

`729fba4552e28cd6f53e62f10c8f3bd098d5ca5dfb8d0e3bf4ba3ba1a6250f3e`

Required installer SHA-256:

`c0779d9bae69d850a44073134e7799a48a1856935b09aae1ae8c7da9f57e0629`

Expected candidate plugin fingerprint:

`1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`

Public `v0.9.3` must remain immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

## Required fresh authority and preflight

Before any Windows write or Scheduled Task registration:

1. fetch fresh GitHub branch authority;
2. require Task255 is still active and `READY_FOR_HERMES`;
3. verify public tag identity;
4. verify exact candidate Actions remain terminal SUCCESS for:
   - Validate;
   - Windows Installer Pack Smoke;
   - PS5.1 Acceptance Smoke;
5. create a fresh disposable detached checkout of exact `6822af464fe7a5cb3f93305d0263dfc86b56ac68` under `%LOCALAPPDATA%\Temp`;
6. prove detached exact HEAD, clean working tree, no relevant untracked files, `VERSION=0.9.3`;
7. hash the exact checkout runner and installer and require the identities above;
8. recompute/prove candidate plugin fingerprint rather than assuming it;
9. perform read-only live preflight of current installed plugin fingerprint/version, controller mode/generation, Gateway, Ollama, Delivery, Recovery, SQLite, pending rollover state, and installer classification;
10. preserve Task248/251 retained forensic evidence and existing rollover backups/transactions without modification.

If live state already proves the exact candidate plugin is installed and the system is already converged because of external drift, STOP without invoking the installer and report `BLOCKED_PREFLIGHT_DRIFT_CANDIDATE_ALREADY_INSTALLED`.

Any other authority or identity mismatch: `BLOCKED_PREFLIGHT_DRIFT`.

## Durable evidence root

Create and use a non-temp evidence root from the beginning:

`%LOCALAPPDATA%\CogentNexus-OpenClaw\forensics\CNX-20260905-255`

Before Scheduled Task start, preserve at minimum:

- exact checkout HEAD proof;
- runner bytes/SHA-256;
- installer bytes/SHA-256;
- plugin fingerprint proof;
- launch manifest bytes/SHA-256;
- parsed manifest readback;
- Scheduled Task XML/action/principal/settings readback;
- preflight runtime state;
- pre-start effect ledger.

Do not rely on `%TEMP%` as the sole copy of execution evidence.

## Launch topology — mandatory

Use this topology only:

```text
Windows Task Scheduler
-> Windows PowerShell 5.1
-> exact candidate scripts/manifest-streaming-runner.ps1
-> frozen launch manifest
-> Windows PowerShell 5.1 target process
-> exact candidate scripts/install.ps1
```

The Scheduled Task action MUST contain only the runner invocation and its manifest/evidence-root arguments. It MUST NOT embed the installer argument vector as nested Scheduler quoting.

The frozen launch manifest must identify:

- `childExecutable`: Windows PowerShell 5.1 executable;
- `childArguments`: exact argument vector that includes one `-File` followed by the exact detached candidate `scripts/install.ps1` path;
- `workingDirectory`: exact detached checkout repository root;
- `evidenceRoot`: the durable Task255 evidence root.

Do not pass nonexistent parameters such as `--install-source-commit` / `-InstallSourceCommit`.

Do not use installer skip switches or `LinkPlugin`.

Before start, parse/read back the frozen manifest and prove:

```text
runner SHA = 729fba4552e28cd6f53e62f10c8f3bd098d5ca5dfb8d0e3bf4ba3ba1a6250f3e
installer SHA = c0779d9bae69d850a44073134e7799a48a1856935b09aae1ae8c7da9f57e0629
exact candidate HEAD = 6822af464fe7a5cb3f93305d0263dfc86b56ac68
manifest -File occurrence = exactly 1
manifest target after -File = exact detached candidate scripts/install.ps1
```

## Scheduled Task contract

Use the previously qualified interactive scheduler identity unless fresh read-only evidence proves required identity drift. Record principal/user/SID/logon/run-level explicitly.

Required settings:

```text
ExecutionTimeLimit = PT45M
AllowHardTerminate = true
```

Do not increase `ExecutionTimeLimit` in this task.

Pre-start readback must prove the task action, runner path, manifest path, evidence root, principal, and `PT45M` settings exactly. Any discrepancy: STOP before start.

## Cardinality / retry gate

Strict live budget:

```text
successful installer Scheduled Task registrations <= 1
installer Scheduled Task starts <= 1
actual scripts/install.ps1 target starts <= 1
installer retries after start = 0
```

If task registration fails before a task exists, prove `TaskPresent=false` and STOP; do not attempt a second registration in this task.

Once the Scheduled Task is started, the retry gate is permanently closed regardless of outcome.

Do not manually start a second installer process.

## Execution observation

After the single start, observation is read-only.

Use the streaming evidence to retain, while the target is still running where possible:

- `runner-started.json`;
- `child-started.json` with actual target PID;
- incremental `child-stdout.txt`;
- incremental `child-stderr.txt`;
- runner transcript/fallback/result if available;
- Scheduled Task status and final `LastTaskResult`;
- timestamps for installer-owned backup/staging/transaction artifacts.

Do not manually terminate the child merely because it runs for a long time. If it reaches the configured `PT45M` limit, allow the Scheduler contract to determine the terminal state and preserve all already-written evidence.

## Outcome branches

### A. Installer succeeds

Require one-shot exit/result success and then prove postflight convergence:

- exact candidate plugin installed;
- installed plugin fingerprint = `1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`;
- rollover prepare/finalize completed consistently;
- no unresolved pending rollover transaction;
- controller returns to expected managed mode;
- startup/adapter state healthy;
- Ollama selected/healthy;
- Gateway healthy on expected loopback endpoint;
- Delivery READY with pending count understood/expected;
- Recovery READY;
- SQLite integrity `ok`;
- no attributable semantic message emitted.

Disposition: `PASS_EXACT_CANDIDATE_INSTALL_OVER_REQUALIFIED`.

### B. Installer exits nonzero

STOP. Do not retry.

Preserve complete streaming stdout/stderr, runner result, actual target PID evidence, Scheduled Task result, and all installer-owned residue.

If `plugin-rollover-prepare` reports `pre-install backup project-tree attestation mismatch`, preserve the Task250 `diagnostic=` payload exactly, including source/backup hash-input snapshots and per-path delta. Do not weaken or bypass attestation.

Disposition: `FAIL_INSTALLER_TERMINAL_STREAMING_EVIDENCE_PRESERVED`.

### C. Scheduler reaches PT45M / 0x41306 or equivalent hard-termination boundary

STOP. Do not retry and do not increase timeout.

Use the durable stream evidence to identify the **last proven installer output/stage** and actual target PID. Record whether a terminal runner result is absent because the outer process was killed. Inspect installer-owned residue read-only to correlate the last stage.

Disposition: `BLOCKED_SCHEDULER_LIMIT_STREAMING_STAGE_EVIDENCE_PRESERVED`.

### D. Runner/target launch failure before installer actually starts

Prove no installer target process started and no installer-owned live mutation occurred. STOP without re-registering/restarting.

Disposition: `BLOCKED_RUNNER_OR_TARGET_LAUNCH_PRESTART`.

## Semantic hard fence

This task is installer/runtime qualification only. Do not perform Dashboard/Discord/API semantic acceptance.

```text
Dashboard semantic sends = 0
Discord semantic sends = 0
direct API semantic sends = 0
recovery replay/resend = 0
```

Do not consume the human Dashboard semantic budget in this task.

## Other hard fences

- no force push/history rewrite;
- no release/tag mutation;
- no manual deletion/repair of retained rollover evidence;
- no manual weakening of ownership/attestation checks;
- no DB mutation outside installer-owned behavior;
- no manual Gateway/controller/provider/model lifecycle mutation outside installer-owned behavior;
- no second installer execution.

## Required report

Publish:

`docs/operations/coordination/reports/CNX-20260905-255-task254-streaming-runner-exact-candidate-windows-install-over-requalification.md`

Include:

- fresh GitHub authority and exact candidate proof;
- exact checkout path/HEAD/cleanliness;
- runner/installer/plugin fingerprints;
- frozen manifest bytes/SHA/readback;
- Scheduled Task action/principal/settings/XML proof;
- preflight live state;
- registration/start/target-start cardinality;
- streaming evidence identities and timestamps;
- terminal task/result/exit evidence;
- exact last proven installer stage;
- rollover/backup/transaction evidence;
- Task250 `diagnostic=` payload verbatim if attestation mismatch recurs;
- postflight runtime/installed fingerprint evidence if success;
- semantic-zero/effect ledger;
- public tag immutability;
- final disposition.

Then STOP for independent ChatGPT review. Even on installer PASS, do not perform semantic acceptance until a separate successor task is authorized.
