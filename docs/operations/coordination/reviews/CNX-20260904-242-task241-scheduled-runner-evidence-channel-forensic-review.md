# CNX-20260904-242 — Independent Review

## Reviewed authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`
- Task: `CNX-20260904-242`
- Task authority before execution: `76976b744dcc9985db27b9e67f4359dd467ad68d`
- Report commit / reviewed HEAD: `1420fb8ae3c53deb0f99e1ce20c5192822ae91ba`
- Report path: `docs/operations/coordination/reports/CNX-20260904-242-task241-scheduled-runner-evidence-channel-forensic.md`

Fresh compare from Task-242 authority to report HEAD is one report-only commit. No product/source/test/workflow drift was introduced by Task 242.

## Verdict

`ACCEPT_PASS_HARMLESS_CANARY_PROVES_EXECUTION_CHANNEL__TASK241_SPECIFIC_RUNNER_CHILD_BOUNDARY_UNRESOLVED__HARDENED_RUNNER_HARNESS_QUALIFICATION_REQUIRED`

## Independent findings

### 1. Scheduler-to-PowerShell-to-artifact channel is proven functional

The authorized harmless canary used one Scheduled Task registration and one start with zero retry, then produced:

```text
LastTaskResult = 0
marker = CNX242_CANARY_SUCCESS
PowerShell = 5.1.19041.6456
identity = CDQ-P\CDQ-P
cwd = C:\Windows\system32
artifact = present
```

This excludes a general Scheduled Task launch failure, general Windows PowerShell 5.1 startup failure, the forward-slash absolute-path style as a sufficient cause, and inability of the task principal to write to the dedicated temp evidence root.

### 2. Task-241 remains unclassifiable as a product installer failure

Task 241 has retained proof of one Scheduled Task start and terminal `LastTaskResult=1`, but no durable `runner-started`, child invocation, transcript, or `runner-result` record. The child installer invocation therefore remains unproven.

It would be unsound to infer `FAIL_INSTALLER_TERMINAL`, `FAIL_ROLLOVER_PREPARE`, or any later product stage from `LastTaskResult=1` alone.

### 3. The Task-241 operator runner has a real evidence-harness weakness

The retained runner writes its only result after the child process returns. It has no durable pre-child marker, no explicit transcript/fallback log, and no `finally` result path. An early child-launch exception or host/runner termination can therefore produce exactly the observed zero-artifact state.

This is a harness/observability weakness in the one-off operator runner, not evidence of a defect in `scripts/install.ps1`.

### 4. Product/live fences were preserved

Task 242 performed:

```text
scripts/install.ps1 invocations = 0
installer Scheduled Task starts = 0
rollover-prepare/finalize = 0
openclaw plugins install = 0
plugin mutation = 0
controller/Gateway/lifecycle mutation = 0
semantic submissions = 0
recovery replay/resend = 0
manual DB/Ticket/outbox writes = 0
```

The live boundary remained `passthrough`, generation `39`, candidate not installed, runtime checks READY, and retained Task-237 evidence unchanged.

### 5. Report-head Validate failure is external and unrelated to Task 242

For report HEAD `1420fb8...`:

- PS5.1 Acceptance Smoke `33837768138` = SUCCESS
- Windows Installer Pack Smoke `33837767959` = SUCCESS
- Validate `33837767905` = FAILURE

The failed Validate matrix job was macOS/Python 3.14 and all repository tests/build/evaluation steps before `npm audit --omit=dev` passed, including Python `480 passed, 33 skipped, 4 subtests passed` and plugin `58 files / 284 tests`. The failure was a five-minute npm registry audit endpoint network timeout. Other matrix jobs passed. This does not alter the Task-242 forensic verdict.

## Successor authority

A new installer attempt is **not** authorized by this review.

The next task should qualify a hardened one-off operator runner/evidence harness using harmless synthetic child commands only. It must prove that, under the same Scheduled Task / PowerShell 5.1 context used for the installer, the harness durably records:

1. evidence-root creation and writability before child execution;
2. `runner-started` before any child call;
3. exact child executable/source/argument vector, CWD, identity, and timestamps;
4. stdout and stderr capture;
5. child exit status;
6. a `runner-result` written from `finally` even when the child returns nonzero or child launch throws;
7. an explicit transcript/fallback log;
8. propagation of the intended terminal exit code to Task Scheduler without losing the durable artifacts.

The qualification task must remain installer-free and product/semantic side-effect free. Only after independent review of a qualified harness may a separate successor authorize another one-shot installer execution.
