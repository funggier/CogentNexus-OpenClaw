# CNX-20260918-416 — Repaired Installer Re-entry and Live Runtime Attestation

Status: `READY_FOR_HERMES`

## Authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Parent: `CNX-20260918-415`
- Executor: `Hermes`
- Reviewer: `ChatGPT`
- Human final authority: `Operator`
- Parent review: `docs/operations/coordination/reviews/CNX-20260918-415-chatgpt-review.md`
- Parent report: `docs/operations/coordination/reports/CNX-20260918-415-ticket-db-native-stderr-repair-local-validation-report.md`
- Exact product/source candidate: `c1baa815d6894f0d619d4d3695c61a442e206e38`

GitHub remote is authoritative for coordination state.

The production/source candidate is frozen at:

`c1baa815d6894f0d619d4d3695c61a442e206e38`

## Objective

Starting from the safe partial production state left by CNX-413, prove that the current ownership state is a supported non-fresh installer re-entry shape, then perform exactly one repaired install-over from the frozen candidate.

After successful natural convergence, invoke the read-only runtime attestation exactly once.

No semantic/model/provider request is authorized.

## Accepted current production state from CNX-413

Expected before-state:

- controller: passthrough / cnxMode disabled;
- generation: 106;
- plugin: disabled;
- Gateway: healthy;
- stale `healthy-runtime` marker: already retired;
- Recovery: READY;
- Delivery: READY;
- pending outbox: 0;
- SQLite integrity: OK;
- provider/model: unchanged at `ollama/qwen3.8:27b`;
- durable counts unchanged by the failed installer;
- no manual repair occurred after CNX-413.

This expected state must be re-proven. Do not assume it.

## Phase A — fresh authority and exact candidate binding

1. Fetch the current coordination branch.
2. Re-read ACTIVE, STATUS, this task, CNX-415 review/report, CNX-413 report.
3. Require CNX-416 remains `READY_FOR_HERMES`.
4. Verify candidate `c1baa815d6894f0d619d4d3695c61a442e206e38` is an ancestor of current remote HEAD.
5. Compare candidate -> current HEAD.
6. Require all post-candidate product-source drift to be absent. Test-only and coordination/report/review changes are allowed.
7. Create/use a fresh disposable checkout pinned exactly to the candidate.
8. Prove detached exact HEAD and clean worktree.
9. Bind `scripts/install.ps1` hash from that exact checkout.

If product/source/install-script drift exists after the candidate:

`BLOCKED_PREFLIGHT_DRIFT`

## Phase B — read-only production safety preflight

Capture:

- exact UTC time;
- OpenClaw version;
- Gateway health/PID/port/process identity;
- controller state/generation;
- Supervisor status/snapshot;
- plugin inventory and enabled/loaded/source/path state;
- current installed release-entry hash;
- installed skill `host_v091.py` hash;
- maintenance marker state;
- Recovery verdict;
- Delivery verdict;
- pending outbox count;
- provider recovery incident state;
- SQLite `PRAGMA integrity_check`;
- bounded durable table/status counts;
- current provider/model selection;
- relevant process residue;
- ownership manifest/transaction/staging residue inventory.

Do not print secrets or credentials.

### Required safety gate

Before any installer invocation require:

- Gateway healthy;
- controller is passthrough/disabled;
- maintenance marker absent;
- Recovery = READY;
- Delivery = READY;
- pending outbox = 0;
- no active provider recovery incident;
- SQLite integrity = OK;
- no actionable durable recovery/delivery work;
- provider/model unchanged;
- no live installer/rollover/lifecycle mutation process currently running.

If unsafe or ambiguous:

`BLOCKED_DELIVERY_HAZARD`

## Phase C — exact read-only ownership/re-entry classification

Use the exact candidate's ownership tooling.

### Candidate fingerprint

Compute the exact candidate plugin fingerprint using the frozen candidate root and record it.

### Live plugin inventory

Capture:

`openclaw plugins list --json`

to a read-only evidence file.

### Production-equivalent classifier

Run the exact candidate classifier read-only with the live inventory and expected replacement fingerprint:

```text
python <candidate>\skills\cogentnexus-openclaw\scripts\namespace_ownership.py classify-install
  --workspace <production workspace>
  --app-data <production app-data root>
  --plugin-inventory-json <captured live inventory>
  --expected-replacement-fingerprint <candidate plugin fingerprint>
```

Record exact command, exit code, and full non-secret classification output.

### Supported re-entry gate

Proceed only if the exact classifier proves a coherent supported non-fresh state.

Required minimum:

- classifier exit code = 0;
- mode is a supported upgrade/non-fresh mode;
- `pendingRollover=false`;
- no mixed/foreign/shared/ambiguous ownership;
- no unresolved transaction requiring explicit attested rollover recovery;
- current disabled plugin state and ownership manifest are coherent with upgrade re-entry.

`pluginAlreadyExact` may be true or false; record and let the installer's action resolver decide the supported path.

If `pendingRollover=true`:

`BLOCKED_PENDING_ROLLOVER_TRANSACTION`

If ownership is partial/mixed/foreign/mismatched:

`BLOCKED_PARTIAL_OWNERSHIP`

If classification is not sufficient to prove safe re-entry:

`BLOCKED_INDETERMINATE_REENTRY`

Do not use manual file edits, plugin enable, transaction deletion, or recovery flags to force a passing classification.

## Phase D — one repaired installer invocation

Only after Phase C is GREEN.

Use the exact detached candidate:

`c1baa815d6894f0d619d4d3695c61a442e206e38`

Run the ownership-safe Windows installer:

`scripts/install.ps1 -Workspace <production workspace>`

Do not use:

- `-SkipPlugin`
- `-SkipGatewayRestart`
- `-SkipAgentsPolicy`
- `-LinkPlugin`
- rollover recovery flags unless Phase C explicitly proves an existing supported rollover transaction and ChatGPT separately authorizes it — CNX-416 does not pre-authorize those flags.

Because the pre-state is already passthrough/disabled, the installer should not need a second public disable/handoff mutation beyond its normal supported logic.

### Installer cardinality

- installer invocations: max 1;
- installer successful process starts: max 1;
- retry count after process start: 0;
- manual plugin copy/replace: 0;
- manual Gateway repair/restart: 0;
- manual lifecycle repair: 0;
- manual Ticket/outbox/recovery/SQLite repair: 0.

### Observer requirement

Do not use a short terminal timeout as completion evidence.

Historical accepted Windows install-over execution has exceeded 800 seconds.

Use a detached/retained wrapper or equivalent established project pattern that:

- persists installer PID/start time;
- captures stdout/stderr/transcript durably;
- persists terminal exit code and end time;
- allows read-only PID observation;
- uses an observation fuse comfortably greater than historical successful duration (minimum 1200 seconds unless existing project evidence requires longer);
- does not kill or retry merely because an interactive caller times out.

A missing terminal result is not success.

### Ticket DB repair acceptance

At `ticket-db-bootstrap`, record:

- stage START;
- captured Node warning/output if present;
- stage COMPLETE;
- native exit code.

Node SQLite warning on stderr with child exit 0 must not terminate PowerShell before classification.

If ticket DB child exit is truly nonzero, installer must fail closed.

## Phase E — post-install exact identity and natural convergence

Only if installer terminal exit = 0.

Verify:

- exact installer terminal success;
- plugin id/version/path/source coherent;
- plugin enabled and loaded as intended;
- installed `host_v091.py` hash equals candidate source;
- installed release-entry and runtime-attestation emitted module belong to the exact candidate build lineage;
- `cogentnexus.runtimeAttestation` is present with `operator.read`;
- OpenClaw remains `2026.7.1-2`;
- provider/model selection unchanged;
- no duplicate CogentNexus generation/root active;
- controller converges to active/managed expected v0.9.5 state;
- Gateway healthy;
- maintenance marker absent after natural convergence;
- Recovery READY;
- Delivery READY;
- pending outbox 0;
- SQLite integrity OK.

Do not issue manual lifecycle or enable repair after installer execution.

If convergence requires manual repair:

`FAIL_POST_INSTALL_CONVERGENCE`

## Phase F — one-shot live runtime attestation

Only after Phase E is fully GREEN.

Invoke exactly once:

```text
openclaw gateway call cogentnexus.runtimeAttestation --params '{}' --json
```

Record:

- exact UTC time;
- Gateway PID;
- command;
- exit code;
- stdout/stderr;
- installed hashes;
- full non-secret response.

### Result classification

If `classification = PRESENT`:

`PASS_REPAIRED_INSTALL_RUNTIME_ATTESTATION_PRESENT`

Then stop.

If `classification = ABSENT`:

`FAIL_LIVE_RUNTIME_ATTESTATION_ABSENT`

If `classification = AMBIGUOUS`:

`BLOCKED_LIVE_RUNTIME_ATTESTATION_AMBIGUOUS`

If `classification = RUNNER_UNAVAILABLE`:

`FAIL_LIVE_RUNTIME_ATTESTATION_RUNNER_UNAVAILABLE`

If the RPC is unavailable despite exact installed identity:

`FAIL_LIVE_RUNTIME_ATTESTATION_RPC_UNAVAILABLE`

Attestation retries: 0.

Even on PRESENT, do not send semantic traffic in this task.

## Hard fences

- Web Chat semantic submissions: 0.
- Ollama semantic/model requests: 0.
- OpenAI semantic/model requests: 0.
- Any provider/model semantic request: 0.
- Provider/model selection changes: 0.
- Provider credential/auth mutation: 0.
- Manual maintenance marker mutation: 0.
- Manual Ticket/outbox/recovery/SQLite mutation: 0.
- Manual durable replay/delivery: 0.
- Manual plugin enable/disable/copy/replace/remove: 0.
- Installer starts: max 1.
- Installer retries: 0.
- Manual Gateway restart/repair after installer: 0.
- Manual lifecycle repair after installer: 0.
- Attestation RPC calls: max 1.
- Attestation retries: 0.
- OpenClaw dependency patch/version change: 0.
- Release/tag/main: 0.
- Force push/history rewrite: 0.
- Do not create/start CNX-417 yourself.

## Allowed final classifications

- `PASS_REPAIRED_INSTALL_RUNTIME_ATTESTATION_PRESENT`
- `BLOCKED_PREFLIGHT_DRIFT`
- `BLOCKED_DELIVERY_HAZARD`
- `BLOCKED_PENDING_ROLLOVER_TRANSACTION`
- `BLOCKED_PARTIAL_OWNERSHIP`
- `BLOCKED_INDETERMINATE_REENTRY`
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

`docs/operations/coordination/reports/CNX-20260918-416-repaired-installer-reentry-live-runtime-attestation-report.md`

Include:

- fresh GitHub authority;
- exact candidate/source binding;
- candidate -> HEAD drift classification;
- read-only production preflight;
- exact candidate fingerprint;
- live plugin inventory;
- exact `classify-install` output;
- installer attempt/observer ledger;
- ticket-db stage stderr/exit evidence;
- terminal installer result;
- installed identity;
- natural convergence evidence;
- one-shot attestation result if reached;
- semantic/model/provider request counts explicitly zero;
- final classification.

Then:

1. set ACTIVE.md = `WAITING_FOR_CHATGPT_REVIEW`;
2. set STATUS.md = `WAITING_FOR_CHATGPT_REVIEW`;
3. verify local HEAD == remote HEAD;
4. verify clean worktree;
5. stop;
6. do not create/start CNX-417.
