# CNX-20260904-243 — Task-242 Hardened Scheduled Runner Harness Qualification

## Disposition

`PASS_HARDENED_RUNNER_HARNESS_QUALIFIED`

This is an operator-tooling qualification only. It does **not** authorize another installer attempt.

## Fresh authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`
- Fresh authority HEAD before Phase D and before publication: `8df79e1d3121b5bc659a9f3b0b3b212a4ee1ff2a`
- Task: `CNX-20260904-243`
- Parent: `CNX-20260904-242`
- Reviewed Task-242 report HEAD: `1420fb8ae3c53deb0f99e1ce20c5192822ae91ba`
- Exact executable candidate remains `18a51b15768fb3d2196e65f1ef470c34aeef7f36`
- Candidate plugin fingerprint remains `1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`

`ACTIVE.md` and `STATUS.md` remained `READY_FOR_HERMES` for Task 243. No Task-243 report existed before this publication.

## Phase A — retained Task-241 weakness

The retained Task-241 runner was not modified. It remains at:

```text
C:/Users/CDQ-P/AppData/Local/Temp/cnx241-installer-runner.ps1
```

- size: `879` bytes
- SHA-256: `fca3d96a6152dde72d35ff240d8ad71df28838e29a2452b977a07e54d886cbaa`

The Task-242 evidence showed no durable pre-child marker, no explicit transcript/fallback log, result write only after child return, and no `finally` result path. No fresh Task-241 child installer invocation was inferred.

## Phase B — new disposable harness

New Task-243-only path:

```text
C:/Users/CDQ-P/AppData/Local/Temp/cnx243-harness-20260904T
```

Hardened runner:

```text
C:/Users/CDQ-P/AppData/Local/Temp/cnx243-harness-20260904T/hardened-runner.ps1
```

The runner creates and probes the evidence root, writes `runner-started.json` before child launch, records runner path, child path, argument line, working directory, identity, PID, UTC timestamp, and artifact paths; captures stdout/stderr; distinguishes child nonzero exit from launch exception; writes transcript or fallback evidence; always attempts `runner-result.json` in `finally`; and returns the child exit code after durable capture.

The disposable harness was corrected once after the first direct invocation exposed a PowerShell 5.1 argument-binding issue: array arguments were replaced by an explicit argument line using `ProcessStartInfo.Arguments`. No repository or product file was changed.

## Phase C — direct qualification

### C1: synthetic child nonzero

Evidence path:

```text
.../cnx243-harness-20260904T/direct-nonzero/
```

Observed:

- `runner-started.json`: present
- stdout marker `CNX243_STDOUT_MARKER`: present
- stderr marker `CNX243_STDERR_MARKER`: present
- `runner-transcript.txt`: present
- `runner-result.json`: present
- outcome: `child_nonzero_exit`
- `childStarted`: `true`
- child exit code: `37`
- runner exit code: `37`

### C2: synthetic child launch exception

Evidence path:

```text
.../cnx243-harness-20260904T/direct-launch-exception/
```

Observed:

- `runner-started.json`: present
- outcome: `child_launch_exception`
- `childStarted`: `false`
- child exit code: unavailable/null
- exception type: `System.Management.Automation.MethodInvocationException`
- exception message captured: system could not find the specified file
- `runner-result.json`: present from `finally`
- `runner-fallback.log`: present
- no product command invoked

Both direct cases passed after the disposable PowerShell 5.1 argument correction.

## Phase D — scheduled harmless qualification

The first registration method failed before task creation with Windows error `0x80070057` for the short user ID. A read-only check proved `TaskPresent=false`. One materially different registration method was then used with explicit principal `CDQ-P\\CDQ-P`. This is recorded as one permitted pre-start registration correction; no installer task was involved.

Successful scheduled canary:

- task: `CogentNexus-OpenClaw-Task243-Harness-Canary-1`
- successful registration: `1`
- start: `1`
- starts after first start: `0`
- retries after start: `0`
- terminal state: `Ready`
- `LastTaskResult`: `37`
- principal readback: `CDQ-P`, Interactive, Limited
- action: `C:/Windows/System32/WindowsPowerShell/v1.0/powershell.exe`
- entry: `.../cnx243-harness-20260904T/scheduled-entry.ps1`
- execution time limit: `PT10M`

Scheduled evidence path:

```text
.../cnx243-harness-20260904T/scheduled-nonzero/
```

Required evidence was present:

- `runner-started.json` — 1,038 bytes
- `child-stdout.txt` — 22 bytes, known stdout marker
- `child-stderr.txt` — 22 bytes, known stderr marker
- `runner-transcript.txt` — 74 bytes
- `runner-result.json` — 1,036 bytes

The scheduled `runner-result.json` records outcome `child_nonzero_exit`, `childStarted=true`, and child exit code `37`; scheduler `LastTaskResult=37` coherently matches it. Durable identity, CWD, timestamps, source, argument line, transcript path, fallback path, and result paths are recorded.

## Phase E — live-state preservation

Fresh read-only checks after qualification returned `READY`, exit code `0`, and `stateChanged=false` for:

```text
gateway
provider
model
storage
recovery
delivery
```

Status remained:

```text
controller mode = passthrough
controller generation = 39
selected provider = ollama
```

No candidate installation was performed or authorized. Task-237/Task-241/Task-242 evidence was not cleaned or mutated.

## Product and semantic zero-effect ledger

```text
scripts/install.ps1 invocations: 0
installer Scheduled Task registrations: 0
installer Scheduled Task starts: 0
rollover-prepare/finalize: 0
openclaw plugins install: 0
plugin mutation: 0
controller/Gateway/lifecycle mutation: 0
manual Ticket/outbox/recovery/SQLite writes: 0
Dashboard semantic submissions: 0
Discord semantic submissions: 0
direct Discord/API sends: 0
semantic retries: 0
recovery replay/resend: 0
provider/model substitution: 0
process termination: 0
historical evidence cleanup: 0
force-push/history rewrite: 0
```

Harmless harness ledger:

```text
pre-start registration correction: 1 (first attempt proved TaskPresent=false)
successful canary registration: 1
scheduled canary starts: 1
scheduled canary retries after start: 0
direct C1/C2 synthetic qualification: completed; no product calls
```

## Actions state

Fresh GitHub query at publication time, all bound to SHA `8df79e1d3121b5bc659a9f3b0b3b212a4ee1ff2a`:

- PS5.1 Acceptance Smoke `33868999901`: `completed / success`
- Windows Installer Pack Smoke `33868999911`: `completed / success`
- Validate `33868999909`: `in_progress`

The Validate watcher reached its local 420-second observation timeout, but a subsequent direct GitHub query confirmed the run remained genuinely `in_progress`; this is reported separately and is not treated as a product or harness failure.

## Recommendation and stop gate

The hardened disposable runner is qualified for evidence-channel use. A separate reviewed successor may decide whether to use it for another bounded installer attempt. Task 243 itself does not authorize that attempt.

STOP for independent ChatGPT review.
