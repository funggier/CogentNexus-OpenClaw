# CNX-20260827-103 — Diagnose Live Dashboard Durable-Staging Boundary

Status: `READY_FOR_HERMES`
Execution mode: `SOURCE_AND_READ_ONLY_LIVE_DASHBOARD_STAGING_DIAGNOSIS`
Authorization: `OPERATOR_APPROVED_DIAGNOSIS_ONLY_NO_SEMANTIC_RESEND`
Owner: ChatGPT
Executor: Hermes/Codex
Date: 2026-08-27 ICT

## Goal

Identify the exact failing boundary that allowed Task 102 to visibly deliver one correct Dashboard answer while producing zero durable `cnx_assistant_delivery` rows.

This task is diagnosis-only. Do not repair product source and do not send any new semantic message.

## Accepted predecessor evidence

Task 102 report commit:

`4d23875f4c402cf47109439ebd6b6b5eb72e131b`

Independent Task 102 disposition:

`ACCEPT_BLOCKER_LIVE_DURABLE_PAYLOAD_STAGING_REPRODUCED_AFTER_REPAIR`

Task 102 proved:

- authenticated Dashboard target and input path are usable;
- exactly one semantic Send occurred;
- exactly one new Ticket was accepted and routed;
- exactly one correlated normal `ollama/qwen3.5:9b` Direct inference occurred;
- the exact nonce rendered visibly once;
- `response_ready_at` was recorded;
- `delivery_confirmed_at` remained `null`;
- `cnx_assistant_delivery` remained `0`;
- no `delivery_confirmed` or `completed` event occurred;
- no semantic resend or duplicate provider effect occurred.

Task-102 semantic artifacts are retired evidence. Do not reuse or repair them.

## Accepted live baseline

Exact installed source:

`32212a4331e1f32b5a130bd30d271d4cbc56f6c1`

Exact installed plugin fingerprint:

`df2600da3ae78e1613793b4a7e5d1ebe61f66f71f0903e1d5d2cd5f0d5f4f4b4`

Expected live state remains MANAGED generation 24 with accepted startup/Supervisor/Gateway/SQLite/Ollama health.

## Primary hypotheses

Prove or eliminate each hypothesis with evidence. Do not jump directly to a fix.

### H1 — installed/runtime payload mismatch

The source contains the Task-093 registration repair, but the loaded `dist`/release entry/runtime payload is not the same implementation actually executing live.

### H2 — verified-delivery installer is not registered in the active runtime

`v091-release-entry` is loaded, but `installV091DashboardVerifiedDelivery(api, config)` is not reached or is suppressed before its `reply_dispatch` registration.

### H3 — real Dashboard final delivery does not emit `reply_dispatch`

OpenClaw 2026.7.1-2 visibly delivers Dashboard output through a path that bypasses the hook assumed by the verified-delivery implementation.

### H4 — `reply_dispatch` emits, but real callback shape differs from the test model

Examples include:

- run correlation is not at `event.runId` or `ctx.runId`;
- `ctx.dispatcher` is absent or different;
- `appendBeforeDeliver` is unavailable at that callback;
- final payload/cardinality data differs from the unit-test assumption.

### H5 — hook receives the callback but intentionally skips the final payload

Examples include:

- `info.kind` differs from `final`;
- queued final count is not exactly one;
- payload text is represented somewhere other than `payload.text`;
- media/cardinality filter rejects the payload;
- Dashboard Ticket/session correlation cannot be resolved at staging time.

### H6 — staging is attempted but fails before durable commit

The callback reaches `stageDashboardDirectResult`, but session authority, schema/state validation, SQLite write, or another exact pre-commit boundary throws or returns non-staged.

## Hard fence

During Task 103:

- no new semantic nonce;
- no Dashboard semantic Send;
- no sent sentinel;
- no Task-102 nonce/session/run/Ticket reuse for mutation or replay;
- no direct Ollama/provider probe;
- no synthetic Ticket inserted into live SQLite;
- no live SQLite/config/runtime mutation;
- no product-source fix;
- no maintained product test/source edit;
- no install/install-over/uninstall/reset/cleanup;
- no session cleanup/normalization;
- no model/provider/timeout change;
- no Gateway/Supervisor restart or reboot;
- no credential/token/password read, request, copy, print, log, or re-entry;
- no merge/tag/release/force push.

Read-only inspection of live logs, installed files, process metadata, SQLite and OpenClaw runtime/package source is allowed.

Ephemeral diagnostic scripts/harnesses are allowed only outside maintained product source or as untracked disposable files in an isolated worktree. They must not be committed.

## Phase A — execution and baseline fence

Before diagnosis:

1. fetch/reset the coordination branch to remote without force-pushing;
2. record exact execution HEAD;
3. prove Task-102 report and independent review are ancestors;
4. verify no Task-103 report exists yet;
5. verify accepted installed source/fingerprint and MANAGED generation;
6. verify Gateway/Supervisor/SQLite health read-only;
7. snapshot Ticket/event/outbox/assistant-delivery counts and the exact Task-102 Ticket state;
8. prove no active semantic/provider work attributable to this task.

If the live baseline has materially drifted, stop with:

`BLOCKED_TASK103_BASELINE_DRIFT`

## Phase B — source → package → dist → installed-runtime parity

Trace the exact installed execution chain, not only repository source.

At minimum prove:

1. repository `v091-release-entry.ts` calls `installV091DashboardVerifiedDelivery(api, config)` after legacy registration;
2. repository `v091-dashboard-verified-delivery.ts` contains the Task-093 separated prototype/API-registration lifetime repair (`REGISTERED_APIS`/equivalent);
3. built `dist` contains the same effective registration logic;
4. package manifest/files include the relevant runtime artifacts;
5. installed live plugin path contains byte/content-equivalent effective logic covered by the accepted payload fingerprint;
6. the active OpenClaw plugin entry resolves to that installed runtime artifact, not an older shadow copy.

Record exact paths and hashes where practical without exposing secrets.

If parity fails, classify the first mismatch and stop diagnosis there with:

`ROOT_CAUSE_INSTALLED_RUNTIME_PAYLOAD_MISMATCH`

Do not repair it in this task.

## Phase C — exact OpenClaw 2026.7.1-2 hook contract

Inspect the exact installed OpenClaw 2026.7.1-2 runtime/package/type declarations read-only.

Determine from executable/source evidence:

- whether `reply_dispatch` exists in this exact build;
- where it is emitted;
- which Dashboard/native-delivery paths emit it;
- exact callback event fields;
- exact callback context fields;
- whether `ctx.dispatcher` exists;
- whether `appendBeforeDeliver` exists and at what lifecycle point;
- actual final payload representation (`payload.text` or another shape);
- actual final-kind/cardinality semantics;
- whether the hook occurs before visible Dashboard delivery.

Do not rely on current unit-test mocks as authority. Compare the exact installed OpenClaw contract against the mock assumptions line by line.

If the exact build proves Dashboard bypasses `reply_dispatch`, classify:

`ROOT_CAUSE_DASHBOARD_BYPASSES_REPLY_DISPATCH`

If it emits but the callback contract differs materially, classify:

`ROOT_CAUSE_REPLY_DISPATCH_CONTEXT_CONTRACT_MISMATCH`

## Phase D — Task-102 live evidence correlation

Use only existing Task-102 logs/state and read-only queries.

Correlate the Task-102 session/Ticket/run/time window with:

- plugin startup/registration logs;
- OpenClaw hook or delivery logs if present;
- Gateway logs around final response dispatch;
- plugin diagnostic/error messages around staging;
- Task-102 Ticket/event timeline;
- any evidence that `reply_dispatch` handler ran, skipped, or threw.

Do not infer absence of execution merely from absence of a log line unless the code guarantees that log line.

Produce a boundary table in the report:

| Boundary | Expected | Observed | Proven/Unproven |
| --- | --- | --- | --- |
| release entry active | installer reachable | ... | ... |
| hook registered | one runtime API registration | ... | ... |
| `reply_dispatch` emitted | final Dashboard response | ... | ... |
| run correlation | Task-102 run | ... | ... |
| dispatcher available | `appendBeforeDeliver` callable | ... | ... |
| final payload filter | one text final | ... | ... |
| stage function entered | exact run/text | ... | ... |
| durable write | one pending delivery row | zero | ... |

## Phase E — production-shaped source-only reproduction

Use an isolated worktree or disposable harness. Do not edit maintained product source.

The reproduction must exercise the real release registration boundary rather than calling `installV091DashboardVerifiedDelivery()` directly as the primary path.

Required properties:

1. load/register the real release entry used by the package;
2. use the exact installed OpenClaw 2026.7.1-2 plugin API/type/runtime behavior where feasible;
3. capture which hooks the release entry actually registers;
4. drive only synthetic in-memory/temp-directory delivery state, never live SQLite;
5. compare a test-shaped `reply_dispatch` callback against the real installed OpenClaw callback contract found in Phase C;
6. show the smallest condition that changes staging from one durable row to zero.

If a fully executable real-runtime reproduction cannot be constructed without causing live semantic/provider effects, stop at the strongest safe source/runtime contract proof and state the exact unproven boundary. Do not weaken the fence to get a reproduction.

## Phase F — root-cause decision

The task succeeds only if it identifies one first failing boundary with evidence strong enough to prescribe a bounded successor repair.

Preferred result tokens:

- `ROOT_CAUSE_INSTALLED_RUNTIME_PAYLOAD_MISMATCH`
- `ROOT_CAUSE_VERIFIED_DELIVERY_INSTALLER_NOT_REGISTERED`
- `ROOT_CAUSE_DASHBOARD_BYPASSES_REPLY_DISPATCH`
- `ROOT_CAUSE_REPLY_DISPATCH_CONTEXT_CONTRACT_MISMATCH`
- `ROOT_CAUSE_FINAL_PAYLOAD_FILTER_MISMATCH`
- `ROOT_CAUSE_DASHBOARD_STAGE_CORRELATION_REJECTED`
- `ROOT_CAUSE_DASHBOARD_STAGE_WRITE_FAILURE`

If evidence cannot select one root cause safely:

`BLOCKED_ROOT_CAUSE_NOT_YET_ISOLATED`

The report must explicitly eliminate or leave open H1-H6.

## No-fix rule

Even after a root cause is proven, do not modify product source in Task 103.

Instead report the minimal successor repair design:

- exact component/file boundary to change;
- behavior before/after;
- required RED reproduction;
- required GREEN regression proof;
- required install/fingerprint impact;
- whether a later live semantic retest will need operator assistance.

Any implementation is a separate approved task.

## Operator-assistance contract

No operator action is expected in Task 103.

If an unexpected diagnostic step would require the operator to click, focus, authenticate, send, restart, or approve a mutation, stop before that step and report exactly what operator action would be required. Do not improvise around the operator.

## Verification and publication

Before reporting:

- confirm live counts/state were not mutated by Task 103;
- confirm no new semantic/provider effect occurred;
- confirm product source/maintained tests are unchanged;
- confirm credentials were not accessed;
- `git diff --check` for any coordination/report artifact;
- publish exactly one report-only commit after any ephemeral diagnostic material is removed/untracked.

Report path:

`docs/operations/coordination/reports/CNX-20260827-103-diagnose-live-dashboard-staging-boundary.md`

The report must include:

- execution HEAD and report HEAD;
- source/dist/installed parity evidence;
- exact OpenClaw 2026.7.1-2 hook contract evidence;
- Task-102 live correlation evidence;
- boundary table;
- production-shaped reproduction evidence or explicit safe limitation;
- H1-H6 disposition;
- exact root-cause token or blocker token;
- minimal successor repair design;
- proof of zero semantic/provider/product mutation;
- publication-fence proof.

Task 103 does not authorize implementation or a new semantic acceptance run.