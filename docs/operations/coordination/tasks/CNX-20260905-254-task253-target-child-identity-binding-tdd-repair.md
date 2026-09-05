# CNX-20260905-254 — Task-253 Target Child Identity Binding TDD Repair

Status: `READY_FOR_HERMES`  
Executor: Hermes / repository-capable implementation agent  
Coordinator / independent reviewer: ChatGPT  
Parent task: `CNX-20260905-253`  
Parent review commit: `1674407f0cd3e0b7a77cf0a40cc41a5ae29ab7a8`  
Parent review verdict: `REJECT_PASS_STREAMING_RUNNER_TARGET_PID_CONTRACT_NOT_MET__DURABLE_STREAMING_PROVEN__TDD_IDENTITY_BINDING_REPAIR_REQUIRED`  
Parent umbrella: `CNX-20260831-188`

## Objective

Repair the repository-owned PowerShell 5.1 streaming diagnostic runner so its durable child-start evidence binds to the **actual manifest target process**, not an intermediate `cmd.exe` launcher, while preserving the durable stdout/stderr behavior proven by Task253.

Task254 is repository/test-only. It MUST NOT execute the live installer, register/start a live installer Scheduled Task, invoke rollover prepare/finalize, mutate live runtime/product/database state, or send semantic messages.

## Accepted Task253 evidence

The following Task253 results are accepted and MUST be preserved unless a more exact test requires a minimal implementation change:

```text
test-only RED commit = bb66b67ff9fe5dec344a59b4d130e0d2a55988d2
Task253 candidate = cc35ce506b6a9ffee3223ec79ddb0373a898e4a5
durable stdout/stderr while target alive = proven
pre-kill stream bytes survive outer-runner termination = proven
normal exit 23 propagation = proven
basic invalid-target classification = proven
space-containing argument delivery = proven
plugin fingerprint = 1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f
scripts/install.ps1 SHA-256 = c0779d9bae69d850a44073134e7799a48a1856935b09aae1ae8c7da9f57e0629
```

Task253 is NOT accepted as a live forensic boundary because:

```text
child-started.json.pid = cmd.exe launcher PID
child-started.json.executable = manifest target executable
invalid target can still cause child-started.json to be written before cmd.exe returns 9009
```

That artifact therefore does not prove the actual target child identity.

## Fresh authority

Before implementation:

1. fetch current `agent/v0.9.3-full-stabilization` HEAD;
2. re-read Task253 report, Task253 independent review, ACTIVE, STATUS, and this Task254;
3. require Task254 remains active;
4. verify no unexpected product/source/test/workflow drift since Task254 publication;
5. verify public `v0.9.3` remains `26ce64a624255278a3a0266ad38746e0e6ed2e31`.

Unexpected authority drift: `BLOCKED_PREFLIGHT_DRIFT`.

## Design boundary

This is a bounded correction to:

`scripts/manifest-streaming-runner.ps1`

and its focused regression coverage.

Do NOT modify:

- `scripts/install.ps1`;
- ownership/backup/transaction semantics;
- plugin payload/source;
- controller/Gateway/provider/model lifecycle;
- Dashboard/Discord delivery semantics;
- release/tag state.

A different transport primitive is allowed only if required to obtain deterministic target-process identity while retaining incremental file-backed stdout/stderr on Windows PowerShell 5.1.

Prefer direct target-process creation over shell indirection if it satisfies the existing streaming/argument contract. If a launcher remains necessary, target identity must still be independently and deterministically proven before writing target child-start evidence.

## Mandatory TDD topology

Use strict RED -> minimal implementation -> GREEN.

### Phase 1 — test-only RED

First commit MUST change test/harness code only. It must not edit `scripts/manifest-streaming-runner.ps1`.

Extend the Task253 regression suite with the following behavior tests.

### A. Actual target PID binding

The synthetic target must write its own `$PID` to a durable sidecar while it remains alive.

Require:

```text
child-started.json exists only after the target is known to have started
child-started.json.pid == synthetic target's self-reported PID
child-started.json executable identity == manifest target executable
```

If launcher metadata exists, require a distinct field/artifact such as `launcherPid`; it must not be used as `pid` for the target child.

### B. Invalid target must not claim child start

Use a definitely missing executable.

Require terminal result:

```text
outcome = child_launch_exception
childStarted = false
```

and require that no target `child-started.json` exists claiming successful child launch.

If implementation chooses to retain transport-launch evidence, it must use separately named launcher/transport metadata that cannot be confused with target-child evidence.

### C. Durable streaming remains intact

Preserve Task253 tests proving both stdout and stderr markers are visible on disk while the target is still alive.

### D. Forced outer-runner termination remains intact

After markers and actual target PID are durably proven, terminate only the disposable outer runner and prove already-emitted stdout/stderr remain on disk.

The test harness MUST then deterministically clean up the synthetic target/launcher process tree using the proven target PID so Task254 leaves no orphan synthetic processes.

### E. Exit and launch classifications remain exact

Preserve:

- normal nonzero target exit `23`;
- success exit `0` where useful;
- launch failure distinct from a started target that exits nonzero.

### F. Argument-vector binding hardening

Preserve the existing path-with-spaces case and add at least one argument containing a literal quote or another Windows quoting edge that would expose accidental `cmd.exe`/string-flattening corruption.

The synthetic target must record received arguments and the test must compare the exact intended values.

The RED must fail for the Task253 candidate specifically because target-process identity/launch evidence is wrong, not because of a malformed environment or capability skip.

Capture exact RED command and failure output.

## Phase 2 — minimal production repair

Only after RED is proven, make the smallest production change to satisfy the target identity contract.

Required semantics:

1. `runner-started.json` is written before target launch attempt;
2. stdout/stderr files are created/opened before or at launch;
3. `child-started.json` is written only after the manifest target is actually started;
4. `child-started.json.pid` is the actual target PID;
5. executable identity in the same artifact refers to that target;
6. incremental stdout/stderr remain durable while the target is alive;
7. normal child exit code and terminal classification remain exact;
8. target launch failure cannot leave target child-start evidence;
9. hard outer-runner termination may omit terminal result but must not erase already-emitted streams or the already-proven target-start artifact;
10. no installer/product semantics are added to the runner.

Do not solve this by merely renaming the current launcher PID field. The actual target PID must be proven.

## Phase 3 — focused GREEN

Run the Task254 behavioral suite on Windows PowerShell 5.1.

Require all target identity, launch-failure, streaming, forced-termination, exit-code, cleanup, and argument-binding cases to pass.

Preserve evidence identities for at least:

- self-reported target PID artifact;
- `child-started.json`;
- pre-kill stdout/stderr;
- post-kill stdout/stderr;
- invalid-target result;
- argument-binding result.

## Phase 4 — full GREEN

Run repository validation appropriate to the changed runner/tests, including at minimum:

- full Python suite;
- PowerShell parser/Windows-specific checks;
- plugin validation required by repository policy;
- production npm audit;
- `git diff --check`.

Do not hide unrelated failures. Use only evidence-driven bounded CI retry for infrastructure anomalies under the existing retry policy.

## Exact candidate gates

Record and prove:

```text
final candidate SHA
scripts/manifest-streaming-runner.ps1 SHA-256
scripts/install.ps1 SHA-256
plugin fingerprint
public v0.9.3 target
```

Expected unchanged installer SHA unless unrelated authority drift is detected:

`c0779d9bae69d850a44073134e7799a48a1856935b09aae1ae8c7da9f57e0629`

Expected unchanged plugin fingerprint:

`1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`

Before any future live successor may be authorized, exact final candidate SHA must have terminal SUCCESS for:

```text
Validate
Windows Installer Pack Smoke
PS5.1 Acceptance Smoke
```

Record correct workflow run IDs and check/job IDs; do not conflate Validate and PS5.1 run IDs.

## Hard fences / effect budget

```text
live scripts/install.ps1 invocations = 0
live installer Scheduled Task registrations = 0
live installer Scheduled Task starts = 0
rollover prepare/finalize invocations = 0
live plugin install/copy/delete/rename = 0
retired-project/rollover-backup mutation = 0
controller/Gateway/provider/model lifecycle mutation = 0
Ticket/outbox/recovery/SQLite mutation = 0
Dashboard semantic sends = 0
Discord semantic sends = 0
direct API semantic sends = 0
recovery replay/resend = 0
release/tag mutation = 0
force push/history rewrite = 0
```

Repository source/test edits limited to the streaming runner and qualification tests are authorized.

Synthetic local/CI processes are authorized only for the Task254 runner tests and MUST NOT invoke `scripts/install.ps1`, OpenClaw, CogentNexus runtime commands, Gateway, or production databases.

## Required report

Publish:

`docs/operations/coordination/reports/CNX-20260905-254-task253-target-child-identity-binding-tdd-repair.md`

Report must include:

- fresh opening authority;
- test-only RED commit and changed-files proof;
- exact RED output/failure reason;
- minimal production repair commit/diff summary;
- actual-target PID binding evidence;
- invalid-target no-child-start evidence;
- streaming and forced-termination preservation evidence;
- synthetic process cleanup proof;
- argument-vector hardening evidence;
- focused/full GREEN results;
- final candidate SHA and streaming-runner SHA-256;
- installer SHA-256 and plugin fingerprint;
- exact-SHA Actions run/job IDs and terminal statuses;
- hard-fence ledger;
- public tag immutability;
- final disposition.

Allowed dispositions:

- `PASS_TARGET_CHILD_IDENTITY_BINDING_TDD_REPAIRED`
- `FAIL_TARGET_CHILD_IDENTITY_CONTRACT`
- `FAIL_STREAMING_REGRESSION`
- `FAIL_TDD_EVIDENCE`
- `BLOCKED_PLATFORM_CAPABILITY`
- `BLOCKED_CI_GATE`
- `BLOCKED_PREFLIGHT_DRIFT`

Then STOP for independent ChatGPT review.

Even on PASS, do not run the live installer or perform Dashboard/Discord semantic acceptance. A separate live successor is required.
