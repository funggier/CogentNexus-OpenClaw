# CNX-20260904-248 — Task-247 Repaired-Candidate Windows Install-Over Requalification

## Disposition

`FAIL_INSTALLER_TERMINAL_DIAGNOSTIC_PRESERVED`

The exact Task-247 repaired candidate was invoked once through a fresh manifest-bound Windows PowerShell 5.1 runner. The repaired capture preserved the complete bounded diagnostic and exact failing invariant. The installer terminated at `plugin-rollover-prepare` with child exit `1`. No retry, repair, semantic action, or second invocation was performed.

## Authority and candidate

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`
- Fresh authority before execution: `e70a0fcb63cd4619b66e29020687e4fee970e53a`
- Task: `CNX-20260904-248`
- Parent: `CNX-20260904-247`
- Exact candidate: `6c11a5e8f417300835e85441b88e0f37e3897353`
- Expected plugin fingerprint: `1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`
- Public tag `v0.9.3` was not changed

Task-247 exact-SHA Actions were accepted GREEN before this task:

```text
PS5.1 Acceptance Smoke        33884732550 = SUCCESS
Windows Installer Pack Smoke 33884732528 = SUCCESS
Validate                      33884732569 = SUCCESS on attempt 2, same SHA
```

## Fresh source and preflight

Fresh detached source:

```text
C:/Users/CDQ-P/AppData/Local/Temp/cnx248-exact-source-20260904T
```

Source gates passed:

```text
HEAD = 6c11a5e8f417300835e85441b88e0f37e3897353
VERSION = 0.9.3
worktree = clean
Task-247 Invoke-NativeInstallerDiagnostic = present
```

Exact source installer SHA-256:

```text
c0779d9bae69d850a44073134e7799a48a1856935b09aae1ae8c7da9f57e0629
```

Plugin-local validation passed:

```text
mixed-plugin artifact verification: PASS (45 config properties, 5 tools)
ticket DB bootstrap: PASS (9 required tables + v095 registration fence)
packedFileCount: 196
```

Plugin fingerprint computed from the detached source matched the expected fingerprint exactly:

```text
1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f
```

Fresh preflight was read-only. Controller was `passthrough`, generation `39`, selected provider `ollama`; the canonical installed plugin was the disabled predecessor fingerprint. Gateway, provider, model, storage, recovery, delivery, and CogentNexus-OpenClaw checks were all `READY` with `stateChanged=false`; SQLite integrity was `ok`; delivery pending count was `0`.

## Runner, manifest, and binding

Durable evidence root:

```text
C:/Users/CDQ-P/AppData/Local/CogentNexus-OpenClaw/forensics/CNX-20260904-248
```

Fresh frozen runner:

```text
C:/Users/CDQ-P/AppData/Local/CogentNexus-OpenClaw/forensics/CNX-20260904-248/runner/manifest-runner.ps1
```

Runner SHA-256:

```text
0c2da0cb5877ca9493e4921c3a7b5492dd884841a2bd68c3fb63032b6e42eb98
```

PowerShell parser: `PASS`.

Direct harmless qualification passed before registration:

- synthetic child exit `37`: stdout, stderr, transcript, started/result artifacts persisted;
- launch exception: `child_launch_exception`, fallback and final result persisted.

Frozen manifest:

```text
C:/Users/CDQ-P/AppData/Local/CogentNexus-OpenClaw/forensics/CNX-20260904-248/launch-manifest.json
```

Manifest SHA-256:

```text
818ae0a811f73d8764fa21056a89524486913048e23e029f70642e46efc1424f
```

The manifest contained exactly one `-File`, bound to:

```text
C:/Users/CDQ-P/AppData/Local/Temp/cnx248-exact-source-20260904T/scripts/install.ps1
```

The pre-start recheck proved source HEAD, runner hash, manifest hash, task action, working directory, and manifest binding. The Scheduled Task action carried only the simple runner/manifest/evidence-root vector; installer arguments were not nested in the task action.

## Scheduled Task execution

Task:

```text
CogentNexus-OpenClaw-Task248-Installer-1
```

- registration: `1`
- starts: `1`
- child installer invocations: `1`
- retries after start: `0`
- second start: `0`
- second installer invocation: `0`
- principal: `CDQ-P`, Limited, Interactive
- action executable: Windows PowerShell 5.1
- pre-start state: `Ready`
- terminal state: `Ready`
- terminal `LastTaskResult`: `1`

Start timestamp:

```text
2026-09-04T15:34:42.0554329Z
```

The first inline readback attempt was malformed by Git Bash variable expansion. It occurred after registration and before start, did not alter the task, and was replaced with a file-based readback. No registration retry was performed.

## Complete repaired diagnostic

Runner evidence:

```text
runner-started.json
runner-result.json
runner-transcript.txt
child-stdout.txt
child-stderr.txt
```

Runner result:

```text
outcome = child_nonzero_exit
childStarted = true
childExitCode = 1
transcriptWriteSucceeded = true
fallbackWriteSucceeded = false
```

Installer stage order:

```text
ticket-db-bootstrap: exit 0
plugin-npm-pack: exit 0
plugin-rollover-prepare: exit 1
```

The repaired bounded diagnostic preserved the complete traceback and exact invariant:

```text
File "C:\Users\CDQ-P\.openclaw\workspace\skills\cogentnexus-openclaw\scripts\namespace_ownership.py", line 909, in prepare_plugin_rollover_transaction
    raise RuntimeError("pre-install backup project-tree attestation mismatch")
RuntimeError: pre-install backup project-tree attestation mismatch
```

The PowerShell wrapper also recorded its own capture boundary at `install.ps1:75` and the fail-closed installer throw at `install.ps1:433`. The Python exception is therefore proven as:

```text
exception type: RuntimeError
exception message: pre-install backup project-tree attestation mismatch
function: prepare_plugin_rollover_transaction
source line: namespace_ownership.py:909
```

No stronger underlying cause is claimed. The available evidence proves the attestation mismatch was raised at the tree-equality check; it does not prove whether the mismatch was caused by an historical concurrent content change, filesystem timing, or another lower-level factor.

## Installer-owned partial state

The installer created a workspace skill backup:

```text
C:/Users/CDQ-P/.openclaw/workspace/.cogentnexus-openclaw/install-backups/cogentnexus-openclaw-20260904-223654
```

The installer also created an external rollover-generation backup:

```text
C:/Users/CDQ-P/AppData/Local/CogentNexus-OpenClaw/plugin-generation-rollover-backups/cogentnexus-openclaw-fc6fb357dd4a4c9688e4eb0116c10033
```

External backup tree hash after failure:

```text
900ac13f85a6de75e40a632a534f2b0ceef53def1e8387fc3530c02a7413de58
```

The current retired tree was also read-only hashed to the same value, with zero current path-level differences. This current equality is recorded only as post-failure state; it is not used to infer historical equality at the instant of the failed attestation.

No new Task-248 transaction JSON was persisted. The staging directory still contains only historical transaction/inventory files for tokens `0473c508...`, `844361ed...`, `8469daf...`, and `930460...`; no Task-248 transaction was observed.

The installer-created workspace backup was distinct from the external generation-rollover backup. Neither backup domain was manually modified or cleaned.

## Postflight

Read-only postflight results:

- Gateway: `READY`, exit `0`, `stateChanged=false`
- Provider: `READY`, exit `0`, `stateChanged=false`
- Model: `READY`, exit `0`, `stateChanged=false`
- Storage: `READY`, exit `0`, SQLite `integrity_check=ok`, `stateChanged=false`
- Recovery: `READY`, no active maintenance/replay/incident, `stateChanged=false`
- Delivery: `READY`, pending terminal deliveries `0`, `stateChanged=false`
- CogentNexus-OpenClaw: `READY`, controller `passthrough`, selected provider `ollama`
- Scheduled Task: `Ready`, `LastTaskResult=1`
- canonical installed plugin: version `0.9.3`, predecessor fingerprint `e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386`, disabled

The candidate was not installed as the canonical extension, rollover finalization was not reached, and managed convergence did not occur. No PASS is claimed.

## Effect ledger

```text
installer task registrations = 1
installer task starts = 1
scripts/install.ps1 child invocations = 1
installer retries after start = 0
manual installer invocations = 0
manual plugin install/copy/delete/rename = 0
manual rollover prepare/finalize = 0
manual controller/Gateway/lifecycle repair = 0
manual Ticket/outbox/recovery/SQLite mutation = 0
Dashboard semantic submissions = 0
Discord semantic submissions = 0
direct API sends = 0
semantic retries = 0
recovery replay/resend = 0
process termination = 0
historical evidence cleanup = 0
release/tag/asset mutation = 0
force-push/history rewrite = 0
```

Installer-owned writes inside the one authorized invocation were limited to the observed workspace backup, external rollover backup, plugin staging/build artifacts, and the failed installer path. No manual repair was performed.

## Conclusion and stop gate

Task 247's repaired native-stderr boundary successfully exposed the exact terminal failure that Task 245 could not preserve:

```text
RuntimeError: pre-install backup project-tree attestation mismatch
```

The failure is localized to the pre-install backup tree attestation at `namespace_ownership.py:909`. Task 248 permits no retry or repair after this terminal result. A separately reviewed successor is required for any diagnosis, cleanup, recovery, or new installer attempt.

Semantic acceptance remains unauthorized.

STOP for independent ChatGPT review.
