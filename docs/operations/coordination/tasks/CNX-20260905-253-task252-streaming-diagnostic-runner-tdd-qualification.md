# CNX-20260905-253 — Task-252 Streaming Diagnostic Runner TDD Qualification

Status: `READY_FOR_HERMES`  
Executor: Hermes / repository-capable implementation agent  
Coordinator / independent reviewer: ChatGPT  
Parent task: `CNX-20260905-252`  
Parent review commit: `9318008a9549a264aa28491b0d4d264750a9e168`  
Parent review verdict: `ACCEPT_BLOCKED_TASK251_CHILD_STAGE_UNPROVEN__SCHEDULER_TIMEOUT_AND_BUFFERED_RUNNER_EVIDENCE_LOSS_PROVEN__STREAMING_DIAGNOSTIC_RUNNER_TDD_REQUIRED`  
Parent umbrella: `CNX-20260831-188`

## Objective

Replace the disposable buffered diagnostic-runner pattern used by Task 251 with a reusable, repository-owned Windows PowerShell 5.1 compatible **streaming diagnostic runner** and prove its behavior with test-first qualification only.

This task exists because Task 252 proved:

```text
Task251 scheduler termination mechanism = PT45M hard execution limit
Task251 terminal result = 0x41306
Task251 runner evidence-loss mechanism = buffered ReadToEnd()/post-completion writes
Task251 last installer stage = unproven
Task251 underlying child stall cause = unproven
```

The runner must preserve child output durably while the child is still executing, so a later hard termination cannot erase all evidence emitted before termination.

Task 253 is repository/test-only. It MUST NOT run the live installer, register/start a live installer Scheduled Task, invoke rollover prepare/finalize, mutate runtime/product state, or submit semantic messages.

## Fresh authority

Before implementation:

1. fetch current `agent/v0.9.3-full-stabilization` HEAD;
2. re-read Task252 report/review and ACTIVE/STATUS;
3. require Task253 remains the active task before source/test changes;
4. verify no unexpected product/source/test/workflow drift since this task publication;
5. verify public `v0.9.3` remains `26ce64a624255278a3a0266ad38746e0e6ed2e31`.

Unexpected authority drift: `BLOCKED_PREFLIGHT_DRIFT`.

## Design boundary

This is a bounded operational-tooling change, not an installer semantic change.

Preferred production location:

`scripts/manifest-streaming-runner.ps1`

If an existing repository location is demonstrably more appropriate, document the reason and keep the change equally narrow.

Preferred regression location:

`tests/test_task253_manifest_streaming_runner.py`

The exact test filename may differ if repository conventions require it, but the RED commit must remain test-only.

Do NOT modify `scripts/install.ps1`, `namespace_ownership.py`, plugin payload/source, lifecycle/provider/model logic, ownership/backup/transaction semantics, or Dashboard delivery code in this task.

## Required runner contract

The runner must remain manifest-bound and deterministic. It must accept:

```text
-LaunchManifest <path>
-EvidenceRoot <path>
```

The launch manifest must continue to identify an exact child executable plus argument vector without Scheduler-side nested installer quoting.

Required durable artifacts/semantics:

### Before child launch

- create evidence root if needed;
- write `runner-started.json` before child launch;
- create/open `child-stdout.txt` and `child-stderr.txt` before or immediately at child launch;
- avoid waiting for child completion before those files exist.

### Immediately after successful child launch

Write durable child-start metadata containing at minimum:

- UTC timestamp;
- child PID;
- executable identity/path;
- manifest SHA-256 or equivalent frozen identity;
- runner SHA-256 or equivalent source identity where practical.

### While child is running

- stdout bytes/lines emitted by the child must become visible in `child-stdout.txt` before child exit;
- stderr bytes/lines emitted by the child must become visible in `child-stderr.txt` before child exit;
- writes must be incrementally flushed/durable, not retained only in PowerShell memory until `ReadToEnd()`/`WaitForExit()` returns;
- the runner MUST NOT require a later re-scan/reconstruction to recover already-emitted child output.

A heartbeat/progress metadata file is optional. Do not add it unless it materially improves the minimum contract and is behavior-tested.

### Normal terminal completion

On ordinary child completion, record a terminal `runner-result.json` with:

- child exit code;
- start/completion timestamps;
- normal-vs-launch-failure classification;
- stdout/stderr artifact identities/paths;
- manifest/runner identity sufficient for evidence binding.

The runner process exit code should preserve the intended child success/nonzero contract used by the existing harness.

### Child-launch failure

A failure to create/start the child process must be distinguishable from a child that launched and exited nonzero. Preserve bounded launch exception evidence and terminal runner result where the outer runner remains alive.

### Forced outer-runner termination

The design must explicitly tolerate this evidence shape:

```text
runner-started = present
child-started = present
partial child stdout/stderr = present and durable
runner-result = possibly absent because the outer process was killed
```

A missing terminal result after a hard outer kill is acceptable. Losing already-emitted stdout/stderr is not.

## TDD topology — mandatory

Use RED -> minimal implementation -> GREEN.

### Phase 1 — test-only RED

The first implementation-related commit MUST modify/add test/harness fixtures only. It must not add or edit the production streaming runner.

The RED must prove the current repository lacks the required streaming contract. The failure must be attributable to the missing/incorrect streaming behavior, not a malformed test environment.

At minimum, the RED suite must specify these behavioral cases:

1. **live stdout/stderr visibility** — synthetic child emits stdout marker A and stderr marker B, flushes, then remains alive; test requires both markers to be observable in evidence files while child is still running;
2. **forced outer termination preservation** — after markers are durably observed, terminate only the disposable runner under test and prove the already-emitted markers remain in the evidence files;
3. **normal nonzero completion** — synthetic child emits stdout/stderr then exits with a known code such as `23`; runner result preserves that exact exit code and both streams;
4. **launch failure distinction** — deliberately invalid child executable/path produces launch-failure classification rather than masquerading as child exit `23` or success;
5. **manifest argument binding** — arguments containing spaces/quotes or representative installer-style paths arrive at the synthetic child exactly as intended.

The behavioral PowerShell tests must run on Windows PowerShell 5.1 where the contract is Windows-specific. Cross-platform test collection must skip capability-dependently rather than hard-failing because `powershell.exe` is absent.

Capture the exact RED command and failure output in the report.

### Phase 2 — minimal production implementation

Only after RED is proven, add the minimum runner implementation required by the tests.

Do not copy the old buffered `ReadToEnd()` design and merely add periodic copies. Prefer an actual streaming/file-redirection mechanism whose behavior is deterministic under Windows PowerShell 5.1.

Implementation must not execute CogentNexus/OpenClaw product operations by itself. It is a generic manifest-bound child runner.

### Phase 3 — focused GREEN

Run the Task253 behavioral suite. Require all cases above to pass.

For the forced-termination test, preserve proof that the child markers were on disk **before** the outer runner was terminated and remain afterward.

### Phase 4 — full GREEN

Run repository validations appropriate to the changed files, including at minimum:

- full Python test suite;
- plugin tests/validation where repository policy requires them;
- PowerShell/Windows acceptance coverage relevant to the new runner;
- production npm audit per existing validation policy.

Do not hide unrelated failures. Classify genuine infrastructure/network anomalies separately and use only bounded same-SHA retry if justified by existing retry policy.

## Exact candidate and deployment gates

At the end of Task253, record the final candidate SHA and SHA-256 of the streaming runner file.

Because this runner will be the evidence boundary for any later live installer attempt, the final candidate must have terminal SUCCESS for:

```text
Validate
Windows Installer Pack Smoke
PS5.1 Acceptance Smoke
```

on the exact candidate SHA before a future live successor may be authorized.

If the runner-only change leaves plugin payload unchanged, recompute/prove the plugin fingerprint rather than assuming it. Expected unchanged value from Task250 is:

`1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`

Also record whether `scripts/install.ps1` SHA-256 remains the Task250 candidate value:

`c0779d9bae69d850a44073134e7799a48a1856935b09aae1ae8c7da9f57e0629`

Any installer/source semantic drift outside the new runner/test scope requires independent review before live work.

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

Repository source/test edits for the streaming runner and ordinary CI are authorized.

Synthetic local/CI child processes used only for the runner tests are authorized. They MUST NOT invoke `scripts/install.ps1`, OpenClaw, CogentNexus runtime commands, Gateway, or production databases.

## Required report

Publish:

`docs/operations/coordination/reports/CNX-20260905-253-task252-streaming-diagnostic-runner-tdd-qualification.md`

The report must include:

- fresh opening authority;
- final test-only RED commit and proof it changes no production runner/source;
- exact RED failure reason/output;
- minimal implementation commit/diff summary;
- focused GREEN evidence for all five behavioral cases;
- forced-termination pre-kill and post-kill evidence identities;
- full validation results/counts;
- final candidate SHA;
- streaming runner SHA-256;
- installer SHA-256 and plugin fingerprint proof;
- exact-SHA Actions status/run IDs;
- hard-fence/effect ledger;
- public tag immutability;
- final disposition.

Allowed dispositions:

- `PASS_STREAMING_DIAGNOSTIC_RUNNER_TDD_QUALIFIED`
- `FAIL_STREAMING_RUNNER_CONTRACT`
- `FAIL_TDD_EVIDENCE`
- `BLOCKED_PLATFORM_CAPABILITY`
- `BLOCKED_CI_GATE`
- `BLOCKED_PREFLIGHT_DRIFT`

Then STOP for independent ChatGPT review.

Even on PASS, do not run the installer or perform Dashboard/Discord semantic acceptance. A separate live successor is required.
