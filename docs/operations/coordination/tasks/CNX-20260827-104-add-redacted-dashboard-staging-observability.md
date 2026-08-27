# CNX-20260827-104 — Add Redacted Dashboard Staging Observability

Status: `READY_FOR_HERMES`
Execution mode: `SOURCE_TDD_REDACTED_DASHBOARD_STAGING_OBSERVABILITY`
Authorization: `OPERATOR_APPROVED_BOUNDED_OBSERVABILITY_IMPLEMENTATION_NO_LIVE_INSTALL`
Owner: ChatGPT
Executor: Hermes/Codex
Date: 2026-08-27 ICT

## Goal

Add narrowly scoped, redacted observability around the live Dashboard verified-delivery boundary so a later single live semantic retest can identify the first failing boundary among `reply_dispatch` handler entry, dispatcher/correlation availability, `appendBeforeDeliver` callback execution, final-payload filtering, `stageDashboardDirectResult` result, and durable transaction outcome.

This task changes observability only. It must not change the delivery decision logic, retry semantics, Ticket state machine, provider path, payload contents, staging ownership rules, or native delivery behavior.

## Accepted predecessor

Task 103 report:

`6e271242318db90b6ad1d27cca35971e40a065e4`

Independent Task-103 disposition:

`ACCEPT_BLOCKER_LIVE_HOOK_BOUNDARY_REQUIRES_REDACTED_OBSERVABILITY`

Task 103 proved:

- repository source, dist, package manifest, installed plugin and active runtime entry are in parity;
- the active release boundary registers the verified-delivery `reply_dispatch` handler in a production-shaped disposable harness;
- the exact OpenClaw `2026.7.1-2 (0790d9f)` runtime contract supports `reply_dispatch`, `runId`, dispatcher and `appendBeforeDeliver`;
- the production-shaped harness stages successfully when driven with the modeled callback shape;
- Task-102 live evidence still cannot distinguish H3/H4/H5/H6 because no guaranteed live boundary telemetry exists.

No Task-103 product mutation or semantic/provider effect occurred.

## Scope classification

This is a bounded change to an existing verified-delivery flow. Do not redesign the subsystem.

Expected maintained product files are limited primarily to:

- `plugins/cogentnexus-openclaw/src/v091-dashboard-verified-delivery.ts`
- its focused test file(s)
- generated/built `dist` artifacts required by the repository build

If implementation requires unrelated product modules or changes behavior outside this boundary, stop and report scope expansion before continuing.

## Hard invariants

The implementation must preserve all current semantic behavior.

It must not:

- change whether `reply_dispatch` claims/handles an event;
- change hook priority or registration lifetime unless necessary only to expose diagnostics and proven behavior-equivalent;
- change `appendBeforeDeliver` ordering;
- change final-kind/cardinality/media acceptance rules;
- change run/session correlation rules;
- change the text passed to `stageDashboardDirectResult`;
- change `stageDashboardDirectResult` staging decisions;
- change SQLite schema;
- change transaction isolation/commit behavior;
- change delivery marker construction;
- change `response_ready`, settlement or recovery semantics;
- add retries;
- add provider/model calls;
- log prompt text, answer text, semantic nonce, delivery text, credential values, auth token, password, provider payload or unredacted session/run identifiers.

## Redacted observability contract

Diagnostics must be structured enough to distinguish the first failing boundary in one later live run.

Use stable event/reason names. Exact names may differ if needed for repository conventions, but the report must map them one-to-one to the following boundaries.

### 1. Installer/API registration

Record an observation when the verified-delivery runtime API hook is registered.

Allowed fields:

- event/reason enum;
- process-local registration sequence/count;
- booleans only for relevant capability presence.

Do not log pluginConfig values or paths containing secrets.

### 2. `reply_dispatch` handler entry

Record that the verified handler was invoked.

Allowed fields:

- `hasEventRunId: boolean`
- `hasContextRunId: boolean`
- `hasDispatcher: boolean`
- `hasAppendBeforeDeliver: boolean`
- optional short SHA-256 correlation digest derived from run ID/session key, truncated to a fixed small length; never log the raw identifier.

If no usable run ID exists or dispatcher capability is absent, emit a deterministic skip reason before returning.

### 3. `appendBeforeDeliver` registration and callback entry

Record separately:

- callback registered;
- callback invoked.

Allowed callback fields:

- `kind` as bounded enum/string category;
- queued final count as integer;
- `hasText: boolean`
- `hasMedia: boolean`
- `alreadyOwned: boolean`

Never log text length if it can leak meaningful prompt/response characteristics unless there is a strong need; prefer only `hasText`.

### 4. Filter decision

Every early return from the verified `appendBeforeDeliver` callback must produce exactly one deterministic non-secret reason, for example:

- `not-final`
- `already-owned`
- `empty-text`
- `media-present`
- `final-count-not-one`

If there are other existing early-return boundaries, assign explicit reasons.

### 5. Stage attempt/result

Before calling `stageDashboardDirectResult`, record `stage-attempt` with only hashed correlation/boolean metadata.

After return, record either:

- `stage-staged` plus non-secret owner generation / boolean marker state where useful; or
- `stage-not-staged` plus the exact existing reason enum returned by `stageDashboardDirectResult`.

Do not log staged text, native text, idempotency key or marker.

### 6. Transaction/stage exception boundary

If staging throws, emit one redacted diagnostic containing:

- event `stage-exception`;
- exception class/name if available;
- a normalized error category safe for logs.

Do not log full raw exception messages if they may contain paths, text, SQLite data or identifiers. If exact error text is necessary for development tests, keep it test-local and not in production telemetry.

Where practical, add internal diagnostic callbacks or narrow instrumentation around transaction begin/commit so a later live run can distinguish:

- stage function not entered;
- stage function entered and returned non-staged;
- transaction started but exception occurred;
- commit completed.

Do not alter transaction behavior to achieve this.

### 7. Settlement observation

Existing successful staging/settlement behavior may keep current logs. If adding observations around `waitForIdle`/settlement, they must remain redacted and behavior-neutral. This is secondary to the pre-staging boundary and must not expand scope unnecessarily.

## Logging channel

Prefer the existing plugin logger with one stable prefix such as:

`CogentNexus-OpenClaw delivery-observe`

or an equivalent repository-consistent prefix.

Diagnostics must be easy to grep in a later Task-105 live report.

Do not write new durable SQLite diagnostic rows or mutate Ticket/event tables solely for observability. The observability in this task should live in normal runtime logs unless a pre-existing non-semantic diagnostics mechanism already exists and is clearly safer.

## TDD — mandatory RED → GREEN

No production observability code before failing tests.

### RED tests

Add focused tests that fail on the current source and demonstrate at minimum:

1. release registration emits/captures the verified registration diagnostic without exposing raw identifiers;
2. handler invocation with missing run correlation emits the exact skip reason;
3. handler invocation with missing dispatcher/`appendBeforeDeliver` emits the exact capability skip reason;
4. callback entry produces deterministic filter reasons for `not-final`, `empty-text`, media and final-count mismatch;
5. successful modeled Dashboard staging emits `stage-attempt` then `stage-staged` while still inserting exactly one durable row;
6. an existing non-staged `stageDashboardDirectResult` outcome emits `stage-not-staged` with its reason;
7. a forced disposable staging exception emits `stage-exception` without leaking response text, raw run/session keys or secrets;
8. a legitimate second runtime API registration still receives diagnostics/hook registration, preserving the Task-093 `REGISTERED_APIS` fix.

For each RED test:

- run the focused test command;
- capture that it fails for the expected missing-observability reason, not syntax/setup failure;
- record RED evidence in the report.

### GREEN implementation

Implement the minimum code needed to satisfy the RED tests while preserving all existing behavior.

Then run:

- the focused verified-delivery test file(s);
- the full plugin test suite;
- build/typecheck/lint commands used by this repository;
- any Python/installer regression suite that is required because built/package fingerprints are affected.

Record exact commands and pass/fail counts.

### Behavior-equivalence assertions

Tests must prove observability does not change:

- staged row count/content semantics;
- native returned payload behavior;
- pending/delivered states;
- direct recovery behavior;
- duplicate registration behavior;
- non-Dashboard behavior;
- rich/multi-final bypass behavior if already covered.

## Production-shaped release-path verification

After GREEN, run a disposable harness through the real release registration path, not only direct calls to `installV091DashboardVerifiedDelivery`.

The harness must prove:

- the release entry registers the observability-enabled verified handler;
- a modeled successful callback emits the expected redacted sequence;
- a modeled skip callback emits one deterministic reason;
- no raw run/session/text/credential values appear in captured diagnostics;
- staging semantics remain exactly one row for the successful modeled path.

Use temp SQLite/state only. Never touch live SQLite.

## Secret-leak test

Include explicit automated or scripted verification that captured diagnostics do not contain known synthetic values supplied by the test for:

- response text;
- prompt text if present in harness;
- raw run ID;
- raw session key;
- synthetic token/password marker.

Hash/digest output is allowed only if one-way and truncated.

## Build, package and fingerprint impact

Because runtime source/dist changes are installable payload changes:

1. build the plugin from the implementation commit;
2. prove `package.json.files` installable set remains valid;
3. compute the complete v2 installable-payload fingerprint using the accepted Task-094/095 algorithm;
4. record new fingerprint and file count;
5. verify no reparse/symlink/path safety regression;
6. do **not** install it live in Task 104.

The report must identify the exact implementation commit that a later install task may deploy if independently accepted.

## Live-state fence

Task 104 authorizes source/test/build/package work in an isolated worktree only.

It does not authorize:

- Dashboard semantic Send;
- sent sentinel;
- direct provider probe;
- live SQLite/config/runtime mutation;
- live plugin install/install-over/uninstall/reset;
- Gateway/Supervisor restart;
- session cleanup;
- credential access/re-entry;
- model/provider/timeout change;
- merge/tag/release/force push.

Read-only live baseline checks are allowed only if needed to ensure no unexpected drift, but Task 104 should not depend on live interaction.

## Operator assistance

No operator action is expected during Task 104.

If an unexpected step would require manual focus/click/authentication/send/restart/install authorization, stop before it and report exactly what the operator would need to do.

## Success criteria

Task 104 succeeds only if all of the following are true:

- RED tests were observed failing for the intended missing telemetry;
- minimal GREEN implementation passes focused and full regressions;
- observability covers handler entry through stage result/exception with deterministic redacted reasons;
- secret-leak checks pass;
- production-shaped release-path harness emits the expected diagnostic sequence;
- semantic behavior is unchanged;
- build/package verification passes;
- new installable payload fingerprint is computed;
- no live install or semantic/provider effect occurred;
- implementation and report publication fences are valid.

Preferred success token:

`PASS_REDACTED_DASHBOARD_STAGING_OBSERVABILITY_READY_FOR_LIVE_INSTALL`

If observability cannot be added without changing semantic behavior, stop with:

`BLOCKED_OBSERVABILITY_WOULD_CHANGE_DELIVERY_SEMANTICS`

If a secret-safety requirement cannot be satisfied, stop with:

`BLOCKED_OBSERVABILITY_SECRET_SAFETY`

If tests/build/package verification fail, report the exact blocker rather than weakening the contract.

## Publication fence

Use an isolated worktree.

Publication should identify:

- execution coordination HEAD;
- implementation commit HEAD;
- report commit HEAD.

The final report delta from implementation HEAD to report HEAD must be report-only.

Report path:

`docs/operations/coordination/reports/CNX-20260827-104-add-redacted-dashboard-staging-observability.md`

The report must include:

- RED evidence;
- GREEN evidence;
- changed files and implementation commit;
- exact diagnostics/reason taxonomy;
- proof semantic behavior is unchanged;
- release-path harness evidence;
- secret-leak evidence;
- build/package/fingerprint evidence;
- zero-live-mutation proof;
- recommended exact successor: independent review, then one bounded install-over task, then one operator-assisted single semantic live diagnostic retest only after install acceptance.
