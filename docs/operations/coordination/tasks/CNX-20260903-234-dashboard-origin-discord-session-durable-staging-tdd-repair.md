# CNX-20260903-234 — Dashboard-Origin Discord-Session Durable Staging TDD Repair

Status: `READY_FOR_HERMES`
Date: 2026-09-03 ICT
Parent: `CNX-20260903-233`
Installer-requalification parent: `CNX-20260902-230`
Accepted repair parent: `CNX-20260902-226`
Failure lineage: `CNX-20260902-223`
Parent umbrella: `CNX-20260831-188`
Executor: Hermes / authenticated Windows + repository operator
Coordinator / independent reviewer: ChatGPT

## Purpose

Repair the Task-233 durable semantic staging failure with root-cause-first TDD, without changing real Discord-origin routing semantics.

Task-233 review disposition:

`ACCEPT_FAIL_DURABLE_SEMANTIC_TRACE__DASHBOARD_ORIGIN_ON_DISCORD_ASSOCIATED_SESSION_STAGING_SCOPE_DEFECT_PROVISIONALLY_PROVEN__TDD_REPAIR_REQUIRED`

## Exact Task-233 authority

Task-233 report HEAD:

`827577a053979517a46f419a6f63564bd7420570`

Exact live failure lineage:

```text
Ticket: CNXT-dc11c9a0-8a89-4df5-9c48-345260725be4
run:    e225013e-8d50-4479-b227-ca9a10b89a46
owner:  agent:main:discord:channel:1531199905673252946
prompt: ช่วยสรุปงานที่ฉันควรโฟกัสวันนี้จาก context ล่าสุด และบอกเหตุผลสั้น ๆ
```

Observed topology:

```text
one human Dashboard-origin Send
-> one accepted Direct Ticket / one attributable run
-> four internal Ollama qwen3.5:9b call records in that run
-> response_ready
-> native Dashboard assistant content visible
-> NO cnx_assistant_delivery direct_result for Ticket
-> NO ticket_outbox row for Ticket
-> NO delivery_confirmed_at
-> direct_redelivery_timeout
```

The four internal model-call records are runtime behavior inside the one attributable run; they are not user/Hermes semantic retries.

## Published / source authority

Public `v0.9.3` must remain immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

Accepted pre-Task-234 production repair authority:

`9a8510f1317c8e53c01c233b080ec20357cd22df`

Accepted pre-Task-234 plugin payload fingerprint:

`e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386`

## Source hypothesis to prove

Accepted source appears to contain this scope mismatch:

1. `isDashboardSession()` accepts only `agent:<agent>:dashboard:*`.
2. `before_agent_finalize` in `v091-dashboard-verified-delivery.ts` can recognize a Discord-associated owner through `discordOwnerTicket(...)` and retain a native transcript candidate.
3. `before_message_write` sends that candidate into `stageDashboardDirectResult(...)`.
4. `stageDashboardDirectResult(...)` re-resolves through `dashboardTicket(...)`.
5. `dashboardTicket(...)` rejects `agent:*:discord:channel:*` owner keys.
6. The Dashboard-native result can therefore be visible while durable `direct_result` staging is absent.
7. `v092-durable-delivery-boundary.ts` later fails closed because `response_ready` remains unconfirmed.

This is a hypothesis to verify against the **exact Ticket/run above** and retained telemetry, not permission to make a broad session-key change.

## Critical cross-surface invariant

The environment intentionally supports:

```text
Dashboard-origin turn on Discord-associated owner -> Dashboard/native result
Discord-origin turn on same Discord owner         -> Discord/external-channel result
```

Forbidden repair shortcuts:

- treat every `agent:*:discord:channel:*` owner as Dashboard;
- broaden `isDashboardSession()` to all Discord owners;
- infer ingress from `@Ce`;
- infer ingress from prompt text;
- infer ingress from browser URL alone;
- infer ingress from owner-session syntax alone;
- change owner session identity merely to force Dashboard staging;
- route a real Discord-origin turn through Dashboard native settlement;
- route Dashboard-origin output to Discord.

A trustworthy ingress-surface/correlation contract is required.

## Semantic / live mutation budget

Task 234 is repository/root-cause repair only.

```text
Dashboard semantic Sends: 0
Discord-origin semantic Sends: 0
direct operator Discord/API Sends: 0
semantic resubmissions: 0
recovery replay/resend: 0
manual Ticket/outbox/recovery/SQLite writes: 0
installer/reset/uninstall/reinstall: 0
manual lifecycle/Gateway mutations: 0
live plugin install/enable/disable/uninstall: 0
provider/model substitution: 0
process termination: 0
Task-223/Task-233 forensic evidence mutation: 0
Release/tag/asset mutation: 0
force push/history rewrite: 0
```

Read-only live evidence plus repository source/test/CI repair are authorized.

## Retry policy

Authorized:

- up to 2 additional attempts per logical read-only evidence/tool operation;
- CI/test retry only when evidence points to runner/tooling/timing failure;
- each retry must materially change method or address the observed failure;
- every retry must be recorded.

Not authorized:

- semantic retry;
- recovery replay;
- hiding deterministic RED/GREEN failure by repeated reruns;
- increasing a test timeout merely to force GREEN without root cause.

Required final retry classification:

- `RETRY_POLICY_EFFECTIVE`
- `RETRY_POLICY_NOT_NEEDED`
- `RETRY_POLICY_EXHAUSTED_WITHOUT_RECOVERY`
- `RETRY_POLICY_STOPPED_BY_PRODUCT_BOUNDARY`

## Phase A — fresh repository / CI authority

Before source work:

1. fetch fresh branch HEAD;
2. verify Task 234 is active and `READY_FOR_HERMES`;
3. verify accepted repair `9a8510f...` remains an ancestor;
4. compare accepted repair -> HEAD and classify all product/source/test/workflow drift;
5. verify `v0.9.3` remains `26ce64a...`;
6. verify no newer coordination task supersedes Task 234;
7. inspect Task-233 report-head Actions.

Task-233 report-head CI authority:

- Windows Installer Pack Smoke — SUCCESS;
- PS5.1 Acceptance Smoke — SUCCESS;
- Validate `33706153188` — FAILURE isolated to Windows/Python 3.14 `npm test`, where `v093-response-ready-boundary.test.ts` timed out at 15 seconds; other matrix jobs passed.

Do not call Task-233 report HEAD GREEN. Do not automatically call this timeout a source regression either; Task-233 report commit is docs-only. Reproduce/recheck during Task-234 validation.

Unexpected unrelated drift:

`BLOCKED_PREFLIGHT_DRIFT`

## Phase B — exact Task-233 read-only correlation

Without semantic Send or mutation, correlate only the exact lineage:

```text
CNXT-dc11c9a0-8a89-4df5-9c48-345260725be4
e225013e-8d50-4479-b227-ca9a10b89a46
agent:main:discord:channel:1531199905673252946
```

Prove/read:

- accepted/routed events;
- four internal Ollama call records and final completion;
- `response_ready`;
- absence of attributable `cnx_assistant_delivery direct_result`;
- absence of attributable `ticket_outbox`;
- `direct_redelivery_timeout`;
- no attributable Discord response;
- current failed/recovery state without modifying it;
- retained `CogentNexus-OpenClaw delivery-observe` telemetry if available.

Search retained telemetry for exact run/correlation evidence such as:

```text
handler-entry
handler-skip
public-hook-fallback-armed
stage-attempt
stage-not-staged
stage-staged
```

If `stage-not-staged` exists, record its exact reason. `not-dashboard-direct` would strongly support the source hypothesis.

If logs are unavailable, say so; never invent them.

## Phase C — trusted ingress-surface contract investigation

Inspect the exact OpenClaw `2026.7.1-2` hook/event/context contract used at Ticket intake and relevant post-model/native-write hooks.

Identify a trustworthy signal that can distinguish:

```text
Dashboard/WebChat-origin human turn
Discord-origin human turn
```

while both can share the same owner session key.

The signal must be demonstrated from actual source/API shape or a production-shaped harness and must not depend on user-controlled text or UI heuristics.

If no trustworthy discriminator survives across the required correlation boundary, STOP:

`BLOCKED_INGRESS_SURFACE_CONTRACT`

Report exactly where ingress identity is lost and what contract is missing. Do not guess.

## Phase D — TDD RED before production repair

Only after Phase C proves a usable contract, add the smallest production-shaped regression tests.

### D1 — Dashboard-origin on Discord-associated owner

Use owner shape:

`agent:main:discord:channel:<id>`

with the trusted Dashboard-origin signal.

Require:

- one accepted/correlated Direct Ticket;
- exact final can be captured;
- one `cnx_assistant_delivery direct_result` is durably staged before native settlement authority;
- marker-bearing native append is produced where the native transcript path owns delivery;
- transcript settlement confirms delivery exactly once and terminally settles the Ticket;
- no legacy `direct_redelivery_timeout` becomes eligible;
- owner remains the Discord-associated key.

This test must genuinely fail against predecessor production for the intended staging/ingress reason.

### D2 — real Discord-origin on same owner-key shape

With the trusted Discord-origin signal require:

- Dashboard native durable staging does not claim the turn;
- no Dashboard marker/native transcript settlement is injected;
- existing Discord/external-channel receipt semantics remain authoritative;
- no cross-surface Dashboard-only effect occurs.

### D3 — ordinary Dashboard behavior unchanged

`agent:main:dashboard:*` native transcript/durable staging remains correct.

### D4 — safety contracts unchanged

Keep coverage for duplicate same-text, changed-text fail-closed duplicate, NO_REPLY, owner generation/session authority, response-ready immutability, and no-regeneration while a durable result is pending.

## Genuine RED authority

Commit test-only RED separately.

Required proof:

- predecessor production files unchanged in RED commit;
- new regression fails deterministically for expected reason;
- unrelated targeted tests remain green where possible.

Expected RED disposition:

`RED_CONFIRMED_DASHBOARD_ORIGIN_DISCORD_OWNER_STAGING_GAP`

If the new test passes before repair, return to root-cause analysis. Do not manufacture a production change.

## Phase E — minimal production repair

After genuine RED, make the smallest change that satisfies the trusted ingress contract.

Required properties:

- preserve owner session identity;
- separate owner identity from ingress/delivery-surface identity;
- allow Dashboard durable staging for Dashboard-origin turns on Discord-associated owners;
- keep real Discord-origin turns on Discord/external-channel semantics;
- preserve idempotency and generation fencing;
- preserve native marker settlement and no-regeneration boundaries;
- fail closed when ingress identity is missing/ambiguous;
- avoid broad unrelated refactor/churn.

## Phase F — targeted GREEN

At minimum run:

- new Task-234 regression(s);
- `v162-dashboard-transcript-authority.test.ts`;
- `v091-dashboard-verified-delivery.test.ts`;
- `v154-dashboard-public-hook-fallback.test.ts`;
- `v207-direct-discord-no-reply.test.ts`;
- `v090-dashboard-delivery.test.ts`;
- `v093-response-ready-boundary.test.ts`;
- intake/provenance tests affected by the ingress signal.

All must be GREEN.

## Phase G — full repository GREEN

Run and record on exact repair tree:

- full plugin `npm test`;
- plugin build/evaluation;
- `npm audit --omit=dev`;
- plugin validation;
- current full Python validation;
- PowerShell/POSIX checks;
- package dry-run/provenance validation;
- `git diff --check`;
- Validate workflow;
- Windows Installer Pack Smoke;
- PS5.1 Acceptance Smoke.

Re-evaluate the Task-233 Windows/Python 3.14 `v093-response-ready-boundary` timeout. If it passes without timing-contract changes, record non-reproduction. If it reproduces deterministically, root-cause it separately; do not blindly raise timeout.

## Phase H — provenance/report

Record:

- genuine RED commit;
- minimal repair commit;
- exact changed production/test files and diff stats;
- plugin payload fingerprint after repair;
- whether package identity changed and why;
- targeted/full test results;
- exact workflow run IDs/conclusions;
- compare against accepted predecessor repair;
- public tag immutability;
- retry attempt ledger.

No force push.

## Live-system stop fence

Even after repository GREEN, Task 234 must not install the candidate live and must not perform another Dashboard/Discord semantic turn.

Do not settle/delete/replay/clean the failed Task-233 Ticket or Task-223 forensic evidence.

A successor live-install/requalification requires independent ChatGPT review.

## Allowed final dispositions

- `PASS_DASHBOARD_ORIGIN_DISCORD_SESSION_DURABLE_STAGING_REPAIR_GREEN`
- `BLOCKED_PREFLIGHT_DRIFT`
- `BLOCKED_INGRESS_SURFACE_CONTRACT`
- `FAIL_ROOT_CAUSE_HYPOTHESIS`
- `FAIL_RED_NOT_GENUINE`
- `FAIL_TARGETED_GREEN`
- `FAIL_FULL_VALIDATION`
- `BLOCKED_EVIDENCE`

## Required report

Publish:

`docs/operations/coordination/reports/CNX-20260903-234-dashboard-origin-discord-session-durable-staging-tdd-repair.md`

Then stop for independent ChatGPT review.

Do not automatically live-install/retest, send semantic traffic, replay/settle Task 233, clean historical evidence, mutate Release/tag/assets, or begin another acceptance turn.
