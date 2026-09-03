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

Repair the Task-233 durable semantic staging failure with root-cause-first TDD.

Task 233 proved this live topology:

```text
human Dashboard-origin message
on owner session agent:main:discord:channel:1531199905673252946
-> accepted Direct Ticket
-> OpenClaw run
-> Ollama/model activity
-> native Dashboard assistant content visible
-> response_ready
-> NO cnx_assistant_delivery direct_result
-> NO durable delivery confirmation
-> direct_redelivery_timeout
```

Task-233 review disposition:

`ACCEPT_FAIL_DURABLE_SEMANTIC_TRACE__DASHBOARD_ORIGIN_ON_DISCORD_ASSOCIATED_SESSION_STAGING_SCOPE_DEFECT_PROVISIONALLY_PROVEN__TDD_REPAIR_REQUIRED`

The task must determine and repair the exact production contract without changing real Discord-origin routing semantics.

## Published / source authority

Public `v0.9.3` must remain immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

Accepted pre-Task-234 production repair authority:

`9a8510f1317c8e53c01c233b080ec20357cd22df`

Accepted pre-Task-234 plugin payload fingerprint:

`e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386`

Task-233 exact failure lineage:

```text
Ticket: CNXT-57ab3fb4-930e-43a6-bd16-90f5b84620e3
run:    e225362a-8872-45f8-a914-c90d835880c0
owner:  agent:main:discord:channel:1531199905673252946
```

## Source hypothesis that must be independently verified

Accepted source currently has an apparent scope mismatch:

1. `isDashboardSession()` accepts only `agent:<agent>:dashboard:*`.
2. `before_agent_finalize` in `v091-dashboard-verified-delivery.ts` can recognize a Discord-associated owner via `discordOwnerTicket(...)` and record a native transcript candidate.
3. `before_message_write` routes the candidate through `stageDashboardDirectResult(...)`.
4. `stageDashboardDirectResult(...)` re-resolves only through `dashboardTicket(...)`.
5. Therefore the Task-233 owner key can be accepted as a candidate but rejected at durable staging.
6. `v092-durable-delivery-boundary.ts` later fails closed because `response_ready` exists without a durable direct-result row.

This is a **hypothesis to prove against exact live/runtime evidence**, not permission to make a broad session-key change.

## Critical cross-surface invariant

The environment intentionally supports both:

```text
Dashboard-origin turn on Discord-associated owner session -> Dashboard-visible/native result
Discord-origin turn on that Discord owner session           -> Discord result / external-channel delivery semantics
```

The following shortcuts are forbidden:

- treating every `agent:*:discord:channel:*` key as Dashboard;
- broadening `isDashboardSession()` to all Discord owner keys;
- inferring ingress from `@Ce`;
- inferring ingress solely from prompt text;
- inferring ingress solely from current browser URL;
- changing owner session key just to force Dashboard behavior;
- routing a Dashboard-origin turn to Discord;
- routing a Discord-origin turn through Dashboard native-delivery settlement.

The owner session key remains ownership identity. The repair must use a trustworthy ingress-surface/correlation contract if distinct behavior depends on ingress.

## Semantic and live-mutation budget

Task 234 is repository/root-cause repair only.

```text
Dashboard semantic Sends: 0
Discord-origin semantic Sends: 0
direct operator Discord/API Sends: 0
recovery replay/resend: 0
manual Ticket/outbox/recovery/SQLite writes: 0
installer/reset/uninstall/reinstall: 0
manual lifecycle/Gateway mutations: 0
plugin install/enable/disable/uninstall: 0
provider/model substitution: 0
process termination: 0
Release/tag/asset mutation: 0
force push/history rewrite: 0
```

Read-only live evidence collection is authorized.

## Retry policy

The user's bounded tooling-retry policy remains active.

Authorized:

- up to 2 additional attempts per logical read-only evidence/tool operation;
- CI/test retry only when evidence indicates runner/tooling/timing failure rather than deterministic product failure;
- each retry must materially change method or address the observed failure;
- record every retry in the attempt ledger.

Not authorized:

- semantic resend;
- hiding a deterministic RED/GREEN failure by repeated reruns;
- retrying a production write after uncertain state without first proving repository authority and exact diff.

Required final retry classification:

- `RETRY_POLICY_EFFECTIVE`
- `RETRY_POLICY_NOT_NEEDED`
- `RETRY_POLICY_EXHAUSTED_WITHOUT_RECOVERY`
- `RETRY_POLICY_STOPPED_BY_PRODUCT_BOUNDARY`

## Phase A — fresh repository / CI authority

Before source work:

1. fetch fresh branch HEAD;
2. verify Task 234 is active and `READY_FOR_HERMES`;
3. verify `9a8510f...` remains an ancestor;
4. compare `9a8510f... -> HEAD` and classify every changed product/source/test/workflow file;
5. verify public `v0.9.3` remains `26ce64a...`;
6. verify Task-233 report HEAD remains `827577a...` unless superseded by explicit coordination authority;
7. inspect Task-233 report-head workflow state.

Task-233 report-head CI must be recorded accurately:

- Windows Installer Pack Smoke: success;
- PS5.1 Acceptance Smoke: success;
- Validate `33706153188`: failure isolated to Windows/Python 3.14 `npm test`, where `v093-response-ready-boundary.test.ts` timed out at 15 seconds while other matrix jobs passed.

Do not call this GREEN. Do not automatically label it product regression either. Reproduce/recheck as part of Task-234 validation.

Unexpected unrelated source drift:

`BLOCKED_PREFLIGHT_DRIFT`

## Phase B — exact Task-233 read-only live correlation

Without any semantic Send or mutation, inspect the exact Task-233 lineage and available runtime logs/telemetry.

At minimum correlate:

```text
Ticket CNXT-57ab3fb4-930e-43a6-bd16-90f5b84620e3
run e225362a-8872-45f8-a914-c90d835880c0
owner agent:main:discord:channel:1531199905673252946
```

Prove/read:

- accepted/routed/direct-model events;
- `response_ready`;
- absence of attributable `cnx_assistant_delivery direct_result`;
- `direct_redelivery_timeout`;
- no attributable Discord response;
- current Ticket/recovery state without modifying it;
- relevant `CogentNexus-OpenClaw delivery-observe` telemetry for the run/correlation if retained.

Specifically search for evidence such as:

```text
handler-entry
handler-skip
public-hook-fallback-armed
stage-attempt
stage-not-staged
stage-staged
```

If `stage-not-staged` is present, record its exact reason. A `not-dashboard-direct` result would strongly confirm the source hypothesis.

If logs are no longer available, do not invent them. Continue from durable/source evidence and mark the missing telemetry explicitly.

## Phase C — trusted ingress-surface contract investigation

Before writing a regression or production fix, inspect the exact installed/source OpenClaw `2026.7.1-2` hook contracts used at Ticket intake and the relevant post-model hooks.

Find whether a trustworthy field/API distinguishes at least:

```text
Dashboard/WebChat-origin user turn
Discord-origin user turn
```

while both may share the same owner session key.

Candidate evidence may come from trusted OpenClaw event/context/runtime metadata, but it must be demonstrated from actual source/API shape or a production-shaped harness.

Unacceptable discriminators:

- user-controlled prompt content;
- mention text;
- assumptions from session-key syntax alone;
- browser state alone;
- heuristics that would change if a user copied the same text across surfaces.

If no trustworthy discriminator exists at the required boundary, STOP without guessing:

`BLOCKED_INGRESS_SURFACE_CONTRACT`

The report must state exactly what signal is missing and where the current OpenClaw contract loses ingress identity.

## Phase D — TDD RED

Only after Phase C establishes a viable trusted contract, add the smallest production-shaped regression test(s) **before production repair**.

The RED suite must prove the real topology that existing tests miss.

Required behaviors:

### D1 — Dashboard-origin on Discord-associated owner

Use an owner key matching the real shape:

`agent:main:discord:channel:<id>`

and explicitly mark/provide the trusted Dashboard-origin signal established in Phase C.

Require:

- exactly one accepted/correlated Direct Ticket;
- visible final candidate can be captured;
- exact final text is durably staged into one `cnx_assistant_delivery` `direct_result` before native append/settlement authority;
- marker-bearing native message is produced when the native transcript path is used;
- native transcript settlement produces exactly one `delivery_confirmed` and terminal completion;
- no legacy `direct_redelivery_timeout` is eligible for that result;
- owner session remains the Discord-associated owner key.

Against predecessor production code, this must fail for the intended reason.

### D2 — real Discord-origin on the same owner key remains external-channel behavior

Provide the trusted Discord-origin signal on the same owner-key shape.

Require:

- it is **not** claimed by Dashboard native durable staging;
- Dashboard marker/native-transcript settlement is not injected into the Discord path;
- existing receipt-confirmed/external-channel behavior remains authoritative;
- no cross-surface Dashboard-only side effect occurs.

### D3 — ordinary Dashboard session behavior unchanged

Existing `agent:main:dashboard:*` native transcript/durable staging must remain correct.

### D4 — existing safety boundaries remain intact

At minimum keep coverage for:

- duplicate same-text final;
- changed-text duplicate fail-closed behavior;
- `NO_REPLY` visible-final boundary;
- owner-generation/session authority;
- durable response-ready immutability;
- no regeneration while exact durable result is pending.

## Genuine RED requirement

Commit the test-only RED separately.

Required proof:

- production file(s) unchanged from predecessor at RED commit;
- targeted new regression fails deterministically for the expected staging/ingress reason;
- unrelated existing targeted tests stay green where possible.

Allowed RED disposition:

`RED_CONFIRMED_DASHBOARD_ORIGIN_DISCORD_OWNER_STAGING_GAP`

If the new test passes before repair, the hypothesis/test is wrong. Do not manufacture a repair; return to root-cause analysis.

## Phase E — minimal production repair

After genuine RED, implement the smallest repair that satisfies the trusted ingress contract.

Preferred design properties:

- preserve owner session identity exactly;
- separate ownership identity from ingress/delivery-surface identity;
- keep Dashboard durable staging available for Dashboard-origin turns even when owner session key is Discord-associated;
- keep real Discord-origin turns on Discord/external-channel delivery semantics;
- maintain idempotency key uniqueness and owner-generation fencing;
- preserve native transcript marker settlement and no-regeneration boundaries;
- avoid new global mutable routing state unless the proven OpenClaw hook contract requires bounded run-scoped correlation;
- fail closed when ingress identity is missing/ambiguous rather than guessing cross-surface delivery.

Do not broaden behavior beyond what the RED requires.

## Phase F — targeted GREEN

At minimum run and record:

- new Task-234 regression(s);
- `v162-dashboard-transcript-authority.test.ts`;
- `v091-dashboard-verified-delivery.test.ts`;
- `v154-dashboard-public-hook-fallback.test.ts`;
- `v207-direct-discord-no-reply.test.ts`;
- `v090-dashboard-delivery.test.ts`;
- `v093-response-ready-boundary.test.ts`;
- any intake/provenance test directly affected by the ingress signal.

All must pass after minimal repair.

## Phase G — full repository GREEN

Run the full relevant validation on the exact repair tree:

- full plugin `npm test`;
- plugin build/evaluation;
- `npm audit --omit=dev`;
- plugin validation;
- representative/full Python validation as required by current workflow;
- PowerShell/POSIX syntax and acceptance checks;
- package dry-run/provenance validation;
- `git diff --check`;
- Validate workflow;
- Windows Installer Pack Smoke;
- PS5.1 Acceptance Smoke.

The exact repair tree must be cleanly reproducible.

### Task-233 CI timeout handling

The prior Windows/Python 3.14 `v093-response-ready-boundary` timeout must be re-evaluated.

If it passes on the repair tree without source/test changes to that timing contract, record it as non-reproduced timing anomaly.

If it reproduces deterministically, diagnose it separately/root-cause-first. Do not increase timeouts blindly to obtain GREEN.

## Phase H — source/provenance review

Record:

- genuine RED commit SHA;
- minimal production repair commit SHA;
- exact changed production/test files;
- diff stats;
- exact plugin payload fingerprint after repair;
- whether package/plugin identity changed and why;
- exact CI run IDs and conclusions;
- compare against predecessor accepted repair/source authority;
- confirmation that public `v0.9.3` was not mutated.

No force push.

## Live system fence

Even after repository GREEN, Task 234 must **not** install the repair on the live Windows runtime and must not perform another Dashboard/Discord semantic acceptance.

The live Task-233 failed Ticket/recovery evidence is retained as forensic authority. Do not manually settle, delete, replay, or clean it in this task.

A successor live-install/requalification task requires independent ChatGPT review first.

## Allowed final dispositions

Use one primary disposition:

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

Do not automatically install/retest live, send Dashboard/Discord semantic traffic, clean Task-233/Task-223 evidence, mutate Release/tag/assets, or begin another acceptance turn.
