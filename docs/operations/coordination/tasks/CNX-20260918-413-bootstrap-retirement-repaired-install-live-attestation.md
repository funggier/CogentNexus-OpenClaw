# CNX-20260918-413 — Bootstrap Marker Retirement, Exact Repaired Install-Over, and Live Runtime Attestation

Status: `READY_FOR_HERMES`

## Authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Parent: `CNX-20260918-412`
- Executor: `Hermes`
- Reviewer: `ChatGPT`
- Human final authority: `Operator`
- Parent review: `docs/operations/coordination/reviews/CNX-20260918-412-chatgpt-review.md`
- Parent report: `docs/operations/coordination/reports/CNX-20260918-412-maintenance-convergence-repair-local-validation-report.md`
- Exact repaired production candidate: `368073d67e75cc89b9b04b21b0ee002e76f7e82f`

GitHub remote is authoritative for coordination state.

The product/source candidate is frozen at `368073d67e75cc89b9b04b21b0ee002e76f7e82f`.

## Objective

Resolve the one-time bootstrap deadlock left by the pre-CNX-411 production runtime, then install the exact repaired candidate and perform one read-only live hook attestation.

The sequence is:

```text
re-prove exact stale healthy-runtime marker
    ->
one narrow old-runtime lifecycle start
(no --provider; exactly once)
    ->
require recovery READY
    ->
install exact repaired candidate
    ->
require natural managed convergence
    ->
call cogentnexus.runtimeAttestation exactly once
    ->
stop
```

No semantic/model/provider request is authorized.

## Why bootstrap retirement is necessary

CNX-410 found an active `healthy-runtime` maintenance marker while Gateway/runtime health was already good.

CNX-411 repaired the automatic Supervisor convergence defect, but that repair is not yet installed.

Therefore production cannot use the new repair to retire the already-existing marker until installation occurs, while the install hazard gate correctly refuses installation while the marker remains.

This task may break that bootstrap deadlock using only the existing supported old-runtime lifecycle verification primitive.

Manual marker deletion/editing is forbidden.

## Phase A — fresh authority and exact source binding

Before live mutation:

1. fetch the current coordination branch;
2. re-read ACTIVE, STATUS, CNX-412 report/review, and this task;
3. require CNX-413 is still `READY_FOR_HERMES`;
4. verify exact candidate `368073d67e75cc89b9b04b21b0ee002e76f7e82f` is an ancestor of current remote HEAD;
5. compare candidate -> current HEAD;
6. require all post-candidate drift to be coordination/report/review documentation only;
7. if any product/source/test/install-script drift exists after the candidate, stop as `BLOCKED_PREFLIGHT_DRIFT`;
8. create/use a fresh disposable checkout pinned exactly to the candidate SHA;
9. prove detached exact HEAD and clean checkout;
10. resolve `scripts/install.ps1` from this exact candidate.

Do not install from a mutable worktree.

## Phase B — read-only production bootstrap preflight

Capture exact current production state before any mutation:

- OpenClaw version;
- Gateway health, PID, port, process identity;
- controller mode/cnxMode, desired Gateway, generation;
- supervisor installed/state/health snapshot;
- installed CogentNexus plugin identity/version/path/source;
- installed release-entry hash;
- current runtime/skill path and installed `runtime.py` path;
- maintenance marker contents;
- recovery check;
- delivery check;
- pending outbox count;
- provider recovery incident state;
- SQLite read-only integrity;
- bounded durable-state counts sufficient to detect unexpected mutation;
- current provider/model selection only as read-only invariance evidence;
- no secrets/tokens/credentials printed.

### Required exact bootstrap state

Proceed to Phase C only if all are true:

- Gateway healthy/reachable;
- controller active/managed;
- desired Gateway = running;
- maintenance marker active;
- marker `recoveryPolicy = healthy-runtime`;
- marker reason matches the existing recoverable Gateway-restart lineage, not a new manual-maintenance reason;
- pending outbox = 0;
- no active provider recovery incident;
- SQLite integrity = OK;
- no actionable durable delivery/recovery work that could be replayed by a lifecycle operation.

If marker is already absent and recovery is `READY`, skip Phase C and record `BOOTSTRAP_ALREADY_CONVERGED`.

If marker is active but has `recoveryPolicy != healthy-runtime`, stop:

`BLOCKED_BOOTSTRAP_MARKER_POLICY`

If durable recovery/delivery is unsafe or ambiguous, stop:

`BLOCKED_DELIVERY_HAZARD`

## Phase C — one-time supported bootstrap marker retirement

This phase is authorized only for the exact stale `healthy-runtime` marker from Phase B.

Use the **currently installed production runtime primitive**, not the candidate checkout, and invoke exactly:

```text
<canonical-installed-python> <installed-runtime.py> --root <production-cnx-root> lifecycle start
```

Requirements:

- no `--provider`;
- no public `cnxclaw start` wrapper;
- no candidate script;
- exactly one invocation;
- retry count = 0.

Reason for using the narrow runtime primitive:

- it verifies Gateway health;
- when Gateway is already healthy it does not need a Gateway start;
- without `--provider` provider health is not a convergence requirement;
- successful health verification retires the maintenance marker through the existing supported `clear_maintenance` contract;
- it avoids Host-level terminal/session/direct-recovery reconciliation that is unnecessary for this bootstrap cleanup.

### Required post-bootstrap evidence

Immediately after the one permitted call, require:

- command exit code = 0;
- Gateway remains healthy;
- Gateway process identity is recorded; no unexplained manual process boundary;
- maintenance marker absent;
- recovery verdict = `READY`;
- delivery verdict = `READY`;
- pending outbox = 0;
- no new active provider incident;
- SQLite integrity = OK;
- bounded durable-state counts unchanged except non-semantic runtime ledger/maintenance bookkeeping explicitly attributable to lifecycle verification;
- provider/model selection unchanged.

If the command fails or the marker remains:

`FAIL_BOOTSTRAP_CONVERGENCE`

Stop. Do not retry, do not delete/edit the marker manually, and do not install.

## Phase D — exact repaired install-over

Only after the hazard gate is fully clean.

Install from the fresh detached checkout pinned to:

`368073d67e75cc89b9b04b21b0ee002e76f7e82f`

Use the repository's established ownership-safe Windows installer:

`scripts/install.ps1`

Do not use:

- `-SkipPlugin`
- `-SkipGatewayRestart`
- `-SkipAgentsPolicy`
- `-LinkPlugin`

If elevation requires the already-established Scheduled Task pattern, use that exact pattern. Do not invent a second install mechanism.

### Installer cardinality

- installer starts: max 1;
- installer invocation after process start: exactly 1;
- installer retries: 0;
- manual plugin copy/replace: 0;
- manual Gateway repair/restart after installer: 0;
- manual maintenance-marker edit/delete: 0;
- manual Ticket/outbox/recovery/SQLite mutation: 0.

If installer terminates unsuccessfully, stop:

`FAIL_INSTALLER_TERMINAL`

## Phase E — installed identity and convergence

After installer success, verify exact installed candidate identity.

At minimum:

- installed plugin id/version/path/source coherent;
- OpenClaw remains `2026.7.1-2`;
- candidate `host_v091.py` SHA-256 computed from detached source equals installed production `host_v091.py` SHA-256;
- installed runtime-attestation module exists;
- installed release-entry contains/registers `cogentnexus.runtimeAttestation`;
- RPC scope remains `operator.read`;
- provider/model configuration remains unchanged;
- no duplicate CogentNexus plugin generation is active.

The TypeScript/plugin surfaces did not change between the CNX-409 qualified attestation candidate and CNX-411; if prior deterministic emitted hashes remain applicable, record whether they still match, but bind acceptance primarily to exact source candidate + installed file hashes computed during this task.

### Natural post-install convergence

Do not issue any manual lifecycle repair after installer execution.

Poll read-only health/recovery/delivery state until either:

A. convergence is proven:
- Gateway healthy;
- controller active/managed;
- maintenance marker absent;
- recovery `READY`;
- delivery `READY`;
- pending outbox 0;
- SQLite integrity OK;

or

B. the bounded observation fuse expires / state becomes unsafe.

The new CNX-411 repair must be allowed to own any `healthy-runtime` marker retirement created by the normal runtime flow.

If convergence does not occur without manual repair:

`FAIL_POST_INSTALL_CONVERGENCE`

Stop.

## Phase F — one-shot live runtime attestation

Only after Phase E is fully GREEN, invoke exactly once:

```text
openclaw gateway call cogentnexus.runtimeAttestation --params '{}' --json
```

Record:

- exact UTC time;
- Gateway PID;
- command;
- exit code;
- stdout/stderr;
- installed candidate hashes;
- full non-secret response.

Expected fields:

- `schemaVersion`
- `pluginId`
- `hookName`
- `runnerReady`
- `globalHookCount`
- `latestRegistryPluginHookCount`
- `classification`

### Result handling

If `classification = PRESENT`:

`PASS_REPAIRED_RUNTIME_ATTESTATION_PRESENT`

Then stop.

If `classification = ABSENT`:

`FAIL_LIVE_RUNTIME_ATTESTATION_ABSENT`

Then stop.

If `classification = AMBIGUOUS`:

`BLOCKED_LIVE_RUNTIME_ATTESTATION_AMBIGUOUS`

Then stop.

If `classification = RUNNER_UNAVAILABLE`:

`FAIL_LIVE_RUNTIME_ATTESTATION_RUNNER_UNAVAILABLE`

Then stop.

If RPC is unavailable despite exact installed identity:

`FAIL_LIVE_RUNTIME_ATTESTATION_RPC_UNAVAILABLE`

Then stop.

Attestation retries: 0.

## Hard fences

- Web Chat semantic submissions: 0.
- Ollama semantic/model requests: 0.
- OpenAI semantic/model requests: 0.
- Any model/provider semantic request: 0.
- Provider/model selection changes: 0.
- Provider credential/auth mutation: 0.
- Public `cnxclaw start` bootstrap call: 0.
- Bootstrap runtime lifecycle-start calls: max 1.
- Bootstrap lifecycle retry: 0.
- Manual maintenance marker edit/delete: 0.
- Manual Ticket/outbox/recovery/SQLite mutation: 0.
- Manual durable delivery/replay: 0.
- Installer starts: max 1.
- Installer retry after start: 0.
- Manual plugin copy/replace: 0.
- Manual Gateway restart/repair after installer: 0.
- OpenClaw dependency patch/version change: 0.
- Release/tag/main: 0.
- Force push/history rewrite: 0.
- Do not create/start CNX-414 yourself.

## Allowed classifications

- `PASS_REPAIRED_RUNTIME_ATTESTATION_PRESENT`
- `BOOTSTRAP_ALREADY_CONVERGED` only as an intermediate Phase-C note, not final if installation proceeds
- `BLOCKED_PREFLIGHT_DRIFT`
- `BLOCKED_BOOTSTRAP_MARKER_POLICY`
- `BLOCKED_DELIVERY_HAZARD`
- `FAIL_BOOTSTRAP_CONVERGENCE`
- `FAIL_INSTALLER_TERMINAL`
- `FAIL_INSTALLED_CANDIDATE_IDENTITY`
- `FAIL_POST_INSTALL_CONVERGENCE`
- `FAIL_LIVE_RUNTIME_ATTESTATION_ABSENT`
- `BLOCKED_LIVE_RUNTIME_ATTESTATION_AMBIGUOUS`
- `FAIL_LIVE_RUNTIME_ATTESTATION_RUNNER_UNAVAILABLE`
- `FAIL_LIVE_RUNTIME_ATTESTATION_RPC_UNAVAILABLE`
- `BLOCKED_EVIDENCE`

## Required report

Publish:

`docs/operations/coordination/reports/CNX-20260918-413-bootstrap-retirement-repaired-install-live-attestation-report.md`

Include:

- fresh GitHub authority;
- exact source binding;
- candidate -> current drift classification;
- preflight marker and hazard state;
- exact bootstrap runtime command/cardinality/result;
- pre/post bootstrap marker/recovery/delivery/SQLite evidence;
- installer attempt ledger;
- exact installer source/path/result;
- installed source/artifact hashes;
- post-install natural-convergence observations;
- one-shot runtime attestation command/result;
- semantic/model/provider request count explicitly zero;
- provider/model selection invariance;
- final classification.

Then:

1. set ACTIVE.md = `WAITING_FOR_CHATGPT_REVIEW`;
2. set STATUS.md = `WAITING_FOR_CHATGPT_REVIEW`;
3. verify local HEAD == remote HEAD;
4. verify clean worktree;
5. stop;
6. do not create/start CNX-414.
