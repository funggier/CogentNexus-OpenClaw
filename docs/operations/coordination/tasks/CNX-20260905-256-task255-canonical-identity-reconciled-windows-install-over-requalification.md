# CNX-20260905-256 — Canonical-Identity-Reconciled Exact-Candidate Windows Install-Over Requalification

Status: `READY_FOR_HERMES`
Executor: Hermes / authenticated Windows operator
Coordinator / independent reviewer: Musethree (independent review of Task255)
Parent task: `CNX-20260905-255`
Parent review: `docs/operations/coordination/reviews/CNX-20260905-255-task254-streaming-runner-exact-candidate-windows-install-over-requalification-review.md`
Parent umbrella: `CNX-20260831-188`

## Objective

Perform exactly one live Windows install-over requalification of the Task254
exact candidate with the reconciled canonical installer identity. This is a new
authority — not a retry of Task255. Task255 preflight is consumed and closed.

## Reconciled identities (authoritative)

Required executable candidate:

`6822af464fe7a5cb3f93305d0263dfc86b56ac68`

Required streaming runner (`scripts/manifest-streaming-runner.ps1`), canonical bytes:

`729fba4552e28cd6f53e62f10c8f3bd098d5ca5dfb8d0e3bf4ba3ba1a6250f3e`

Required installer (`scripts/install.ps1`), canonical Git bytes ONLY:

`9d53a42794e0052a817a9f7dd60d0e5895b75882f62261e08427ee414e17b57b`

Known CRLF-materialized digest of the same file (diagnosis only, NEVER a gate):

`c0779d9bae69d850a44073134e7799a48a1856935b09aae1ae8c7da9f57e0629`

Expected candidate plugin fingerprint:

`1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`

Public `v0.9.3` must remain immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

## Required fresh authority and preflight

Before any Windows write or Scheduled Task registration:

1. fetch fresh GitHub branch authority;
2. require Task256 is still active and `READY_FOR_HERMES`;
3. verify public tag identity;
4. verify exact candidate Actions remain terminal SUCCESS for Validate, Windows
   Installer Pack Smoke, and PS5.1 Acceptance Smoke;
5. create a fresh disposable detached checkout of exact `6822af4` under
   `%LOCALAPPDATA%\Temp` with `core.autocrlf=false`;
6. prove detached exact HEAD, clean working tree, no relevant untracked files,
   `VERSION=0.9.3`;
7. triple-proof installer bytes: `git show 6822af4:scripts/install.ps1` SHA-256,
   detached working-tree SHA-256, and raw GitHub bytes SHA-256 must ALL equal
   `9d53a427...e17b57b`; record the CRLF-materialized digest separately and
   require it NOT be used as the gate;
8. prove runner SHA-256 equals `729fba45...a6250f3e`;
9. recompute/prove candidate plugin fingerprint rather than assuming it;
10. perform read-only live preflight of installed fingerprint/version, controller
    mode/generation, Gateway, Ollama, Delivery, Recovery, SQLite, pending
    rollover state, and installer classification;
11. preserve Task248/251 retained forensic evidence and existing rollover
    backups/transactions without modification.

If live state already proves the exact candidate plugin is installed and the
system is already converged because of external drift, STOP without invoking the
installer and report `BLOCKED_PREFLIGHT_DRIFT_CANDIDATE_ALREADY_INSTALLED`.

Any other authority or identity mismatch: `BLOCKED_PREFLIGHT_DRIFT`. Do not
substitute the CRLF digest to pass, do not switch candidates, do not add
installer parameters.

## Durable evidence root

Create and use a non-temp evidence root from the beginning:

`%LOCALAPPDATA%\CogentNexus-OpenClaw\forensics\CNX-20260905-256`

Before Scheduled Task start, preserve at minimum: exact checkout HEAD proof,
runner bytes/SHA-256 (canonical + materialized note), installer bytes/SHA-256
(canonical triple proof + materialized note), plugin fingerprint proof, launch
manifest bytes/SHA/readback, Scheduled Task XML/action/principal/settings
readback, preflight runtime state, pre-start effect ledger. Do not rely on
`%TEMP%` as the sole copy.

## Launch topology — mandatory

```text
Windows Task Scheduler
-> Windows PowerShell 5.1
-> exact candidate scripts/manifest-streaming-runner.ps1
-> frozen launch manifest
-> Windows PowerShell 5.1 target process
-> exact candidate scripts/install.ps1
```

The Scheduled Task action MUST contain only the runner invocation and its
manifest/evidence-root arguments. It MUST NOT embed the installer argument
vector as nested Scheduler quoting.

The frozen launch manifest must identify `childExecutable` (Windows PowerShell
5.1 executable), `childArguments` (exact vector with one `-File` followed by the
exact detached candidate `scripts/install.ps1` path), `workingDirectory` (exact
detached checkout root), and `evidenceRoot` (Task256 durable root).

Do not pass nonexistent parameters such as `--install-source-commit` /
`-InstallSourceCommit`. Do not use installer skip switches or `LinkPlugin`.

Before start, parse/read back the frozen manifest and prove:

```text
runner SHA (canonical) = 729fba4552e28cd6f53e62f10c8f3bd098d5ca5dfb8d0e3bf4ba3ba1a6250f3e
installer SHA (canonical triple-proven) = 9d53a42794e0052a817a9f7dd60d0e5895b75882f62261e08427ee414e17b57b
exact candidate HEAD = 6822af464fe7a5cb3f93305d0263dfc86b56ac68
manifest -File occurrence = exactly 1
manifest target after -File = exact detached candidate scripts/install.ps1
```

## Scheduled Task contract

Use the previously qualified interactive scheduler identity unless fresh
read-only evidence proves required identity drift. Record
principal/user/SID/logon/run-level explicitly.

Required settings:

```text
ExecutionTimeLimit = PT45M
AllowHardTerminate = true
```

Do not increase `ExecutionTimeLimit` in this task. Pre-start readback must prove
task action, runner path, manifest path, evidence root, principal, and `PT45M`
settings exactly. Any discrepancy: STOP before start.

## Cardinality / retry gate

Strict live budget:

```text
successful installer Scheduled Task registrations <= 1
installer Scheduled Task starts <= 1
actual scripts/install.ps1 target starts <= 1
installer retries after start = 0
```

If task registration fails before a task exists, prove `TaskPresent=false` and
STOP; do not attempt a second registration in this task. Once the Scheduled
Task is started, the retry gate is permanently closed regardless of outcome. Do
not manually start a second installer process.

## Execution observation

After the single start, observation is read-only. Retain while the target is
still running where possible: `runner-started.json`, `child-started.json` with
actual target PID, incremental `child-stdout.txt` / `child-stderr.txt`, runner
transcript/fallback/result, Scheduled Task status and final `LastTaskResult`,
timestamps for installer-owned backup/staging/transaction artifacts. Do not
manually terminate the child merely because it runs long; at `PT45M`, allow the
Scheduler contract to determine terminal state and preserve all evidence.

## Outcome branches

### A. Installer succeeds

Require one-shot exit/result success, then prove postflight convergence: exact
candidate plugin installed, fingerprint `1ff69c45...babb5f`, rollover
prepare/finalize consistent, no unresolved pending transaction, controller in
expected managed mode, startup/adapter healthy, Ollama selected/healthy,
Gateway healthy on expected loopback, Delivery READY with pending understood,
Recovery READY, SQLite integrity `ok`, zero attributable semantic messages.

Disposition: `PASS_EXACT_CANDIDATE_INSTALL_OVER_REQUALIFIED`.

### B. Installer exits nonzero

STOP. Do not retry. Preserve streaming stdout/stderr, runner result, actual
target PID, Scheduled Task result, installer-owned residue. If
`plugin-rollover-prepare` reports `pre-install backup project-tree attestation
mismatch`, preserve the Task250 `diagnostic=` payload exactly, including
source/backup hash-input snapshots and per-path delta. Do not weaken attestation.

Disposition: `FAIL_INSTALLER_TERMINAL_STREAMING_EVIDENCE_PRESERVED`.

### C. Scheduler reaches PT45M / 0x41306 or equivalent

STOP. Do not retry, do not increase timeout. Identify the last proven installer
output/stage and actual target PID from durable streams. Record absent terminal
runner result if the outer process was killed. Correlate installer-owned residue
read-only.

Disposition: `BLOCKED_SCHEDULER_LIMIT_STREAMING_STAGE_EVIDENCE_PRESERVED`.

### D. Runner/target launch failure before installer starts

Prove no installer target process started and no installer-owned live mutation
occurred. STOP without re-registering/restarting.

Disposition: `BLOCKED_RUNNER_OR_TARGET_LAUNCH_PRESTART`.

## Semantic hard fence

Installer/runtime qualification only. No Dashboard/Discord/API semantic
acceptance.

```text
Dashboard semantic sends = 0
Discord semantic sends = 0
direct API semantic sends = 0
recovery replay/resend = 0
```

## Other hard fences

- no force push/history rewrite;
- no release/tag mutation;
- no manual deletion/repair of retained rollover evidence;
- no manual weakening of ownership/attestation checks;
- no DB mutation outside installer-owned behavior;
- no manual Gateway/controller/provider/model lifecycle mutation outside
  installer-owned behavior;
- no second installer execution.

## Required report

Publish:

`docs/operations/coordination/reports/CNX-20260905-256-task255-canonical-identity-reconciled-windows-install-over-requalification.md`

Include: fresh GitHub authority and exact candidate proof; canonical triple proof
plus CRLF-materialized note; checkout path/HEAD/cleanliness; runner/installer/
plugin fingerprints; frozen manifest bytes/SHA/readback; Scheduled Task
action/principal/settings/XML proof; preflight live state; registration/start/
target-start cardinality; streaming evidence identities/timestamps; terminal
task/result/exit evidence; exact last proven stage; rollover/backup/transaction
evidence; Task250 `diagnostic=` verbatim if attestation recurs; postflight
evidence if success; semantic-zero/effect ledger; public tag immutability; final
disposition.

Then STOP for independent review. Even on installer PASS, do not perform
semantic acceptance until a separate successor task is authorized.
