# CNX-20260904-242 — Task-241 Scheduled Runner Evidence-Channel Forensic

## Status

`READY_FOR_HERMES`

## Purpose

Determine why the Task-241 installer Scheduled Task ended with `LastTaskResult=1` while producing no fresh runner result or installer transcript artifact.

This task is **forensic/tooling-only**. It must not invoke the product installer or mutate live CogentNexus/OpenClaw runtime state.

## Authority

Repository: `funggier/CogentNexus-OpenClaw`

Branch: `agent/v0.9.3-full-stabilization`

Parent Task: `CNX-20260904-241`

Parent report:

`docs/operations/coordination/reports/CNX-20260904-241-task240-exact-candidate-windows-install-over-requalification.md`

Independent Task-241 review verdict:

`ACCEPT_BLOCKED_EVIDENCE__ONE_SHOT_BUDGET_RESPECTED__PRODUCT_FAILURE_UNCLASSIFIED__RUNNER_EXECUTION_EVIDENCE_FORENSIC_REQUIRED`

Reviewed Task-241 report HEAD:

`36490e1f70da7096054f96f33898a6d9577a9187`

Exact executable candidate remains:

`18a51b15768fb3d2196e65f1ef470c34aeef7f36`

Expected candidate plugin fingerprint remains:

`1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`

Task-237 retained evidence token remains:

`c6aaf93db7c34f718d01302477a292e1`

Do not mutate or clean historical evidence.

## Fresh-authority rule

Before every phase and every repository write:

1. Fetch branch HEAD, `ACTIVE.md`, `STATUS.md`, this task, Task-241 report/review, and relevant GitHub Actions fresh.
2. Fresh GitHub evidence wins over older prose.
3. If unreviewed product/source/test/workflow drift is present, stop `BLOCKED_PREFLIGHT_DRIFT`.
4. No force push or history rewrite.

## Preserved live boundary

Task-241 post-state was:

```text
controller = passthrough
generation = 39
candidate plugin = not installed
Gateway = READY
provider = READY
model = READY
storage = READY
recovery = READY
delivery = READY
pending outbox = 0
SQLite integrity = ok
```

Fresh read-only Windows evidence wins if newer.

## Core forensic question

Task 241 proves exactly one Scheduled Task registration and one start. The task returned:

```text
LastTaskResult = 1
```

But the expected runner result/transcript was absent. Determine which boundary failed:

```text
A. Scheduled Task action launch / command-line binding
B. PowerShell process startup
C. runner script startup
D. runner pre-installer setup / evidence-root creation
E. child-process launch boundary
F. artifact flush/write boundary
G. another specifically evidenced tooling/harness cause
```

Do not infer an installer/product defect unless new read-only evidence actually proves the child installer was invoked and reached product code.

## Phase A — Preserve and inventory Task-241 evidence read-only

Collect without mutation:

- exact Task-241 disposable task definition/XML if still present;
- action executable, arguments, working directory, principal, logon type, run level, execution-time limit and restart policy;
- Scheduled Task state and current `LastTaskResult`;
- exact runner file path used in Task 241;
- runner SHA-256, size and timestamps;
- dedicated Task-241 evidence-root existence, tree inventory, ACL/ownership, timestamps and free-space/path sanity;
- any Task Scheduler Operational/Admin/history events available for the Task-241 task name and execution window;
- any Windows PowerShell operational/event evidence relevant to the execution window;
- nearby temp/transcript files matching Task-241 runner/transcript/result naming patterns;
- process/launch evidence that can be recovered read-only from OS logs or retained files;
- Task-237 retained evidence token/inventory unchanged.

Do not delete, rename, finalize or rewrite anything.

## Phase B — Static runner reconstruction

Reconstruct the exact Task-241 launch chain from retained files and task definition:

```text
Task Scheduler
-> executable
-> argument vector / quoting
-> runner script
-> evidence root
-> child invocation command
-> transcript/result write path
```

Validate statically:

- PowerShell parser result;
- quoting/escaping of all paths containing separators/spaces;
- whether the runner depends on current working directory;
- whether any output/result path is relative rather than absolute;
- whether evidence-root creation occurs before risky operations;
- whether `try/catch/finally` can preserve a terminal result even if child launch fails;
- whether transcript setup itself can fail before durable fallback logging;
- whether the registered principal can write to the exact evidence path.

Static validation may use local PowerShell parsing and read-only filesystem probes.

## Phase C — Harmless scheduler canary

A single harmless canary Scheduled Task is authorized only if Phase A/B cannot already prove the cause.

Maximum canary budget:

```text
harmless canary task registrations: 1
harmless canary task starts: 1
canary retries after start: 0
```

The canary must:

- use an equivalent principal/logon/run-level shape to Task 241;
- use Windows PowerShell 5.1 unless evidence proves Task 241 used something else;
- exercise only scheduler -> runner -> durable artifact capture;
- write a unique canary artifact to a dedicated temp forensic directory;
- record argv/current-directory/environment/path/identity and a deterministic success marker;
- perform **no** installer call, plugin command, Gateway/controller command, database command, semantic send, network side effect, recovery action or product mutation;
- exit with a deterministic known code.

The canary may use a materially improved evidence wrapper, but its purpose is to isolate the Task-241 execution/evidence channel, not to test CogentNexus.

After the canary starts, do not start it again. Read-only observer retries are allowed if evidence-driven and side-effect free.

## Phase D — Root-cause classification

Prefer the narrowest supported classification. Examples:

- `SCHEDULER_ACTION_ARGUMENT_BINDING_DEFECT`
- `RUNNER_STARTUP_DEFECT`
- `EVIDENCE_ROOT_WRITE_PERMISSION_DEFECT`
- `TRANSCRIPT_BOOTSTRAP_FAILS_BEFORE_FALLBACK`
- `RELATIVE_PATH_OR_WORKING_DIRECTORY_DEFECT`
- `EARLY_EXCEPTION_NOT_DURABLY_CAPTURED`
- `CHILD_INVOCATION_BOUNDARY_DEFECT`
- `BLOCKED_EVIDENCE`

For the accepted classification, record the exact evidence chain and why alternatives are excluded.

## Phase E — Successor recommendation

Do not perform a new installer attempt in Task 242.

If the cause is fully localized, recommend the smallest next task needed to make the runner/evidence channel fail-closed and durable before another bounded installer requalification.

If the needed repair is only an ephemeral/operator harness change, do not modify repository product/source/test/workflow code in Task 242. Preserve the proposed correction in the report for independent review.

If a repository-owned tooling/test defect is discovered, stop and recommend a separate TDD repair task rather than editing it here.

## Product and semantic zero-effect fence

```text
scripts/install.ps1 invocations: 0
installer Scheduled Task starts: 0
rollover-prepare/finalize: 0
openclaw plugins install: 0
manual plugin mutation: 0
controller/Gateway/lifecycle mutation: 0
manual Ticket/outbox/recovery/SQLite writes: 0
Dashboard semantic submissions: 0
Discord semantic submissions: 0
direct Discord/API sends: 0
recovery replay/resend: 0
provider/model substitution: 0
process termination: 0
```

## Additional hard fences

Do not perform:

- installer retry;
- reset/uninstall/reinstall;
- managed-state normalization;
- Task-237 or Task-241 evidence cleanup;
- manual plugin copying/deletion/replacement;
- production/source/test/workflow edits;
- release/tag/asset mutation;
- force push/history rewrite.

## Required report

Publish exactly:

`docs/operations/coordination/reports/CNX-20260904-242-task241-scheduled-runner-evidence-channel-forensic.md`

The report must include:

- fresh repository authority;
- Task-241 retained evidence inventory;
- exact Scheduled Task action/principal/settings reconstruction;
- exact runner identity/hash/path;
- filesystem/ACL/path/working-directory findings;
- Scheduler/PowerShell event findings;
- canary ledger/results if used;
- root-cause classification with alternatives excluded;
- preserved live-state proof;
- zero-product/zero-semantic-effect ledger;
- retry ledger;
- exact report commit/HEAD and relevant Actions state;
- recommended successor and why.

Then STOP for independent ChatGPT review.

## Allowed final dispositions

- `PASS_RUNNER_EVIDENCE_CHANNEL_ROOT_CAUSE_LOCALIZED`
- `PASS_HARMLESS_CANARY_PROVES_EXECUTION_CHANNEL`
- `BLOCKED_EVIDENCE`
- `BLOCKED_PREFLIGHT_DRIFT`
- `FAIL_CANARY_EXECUTION_CHANNEL`
- `FAIL_FORENSIC_BOUNDARY_VIOLATION`
