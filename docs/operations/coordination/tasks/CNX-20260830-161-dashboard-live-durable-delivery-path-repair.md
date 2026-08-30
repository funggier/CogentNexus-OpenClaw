# CNX-20260830-161 — Dashboard Live Durable-Delivery Path Repair

Status: `IN_PROGRESS_CHATGPT`

Execution mode: `REPOSITORY_DASHBOARD_DURABLE_DELIVERY_PATH_REPAIR`

Current authorization: `CNX-20260830-161_REPOSITORY_DASHBOARD_DURABLE_DELIVERY_PATH_REPAIR`

Task ID: `CNX-20260830-161`

Updated: 2026-08-30 ICT

Owner / coordinator / executor / reviewer: ChatGPT

Review type at completion: self-review / non-independent

## Trigger

Task 160 is durably reviewed **FAIL**.

The live single-Send acceptance established:

- installed candidate provenance and health were valid;
- exactly one authorized Dashboard semantic Send occurred;
- the model call completed and `response_ready` was committed;
- `cnx_assistant_delivery` remained empty for the tested run;
- `delivery_confirmed_at` remained null;
- the Ticket terminal-failed with the no-regeneration safety path;
- bounded logs recorded verified-delivery handler entry with `hasAppendBeforeDeliver=false` followed by `missing-append-before-deliver`;
- no semantic retry occurred.

Task-160 report:

`docs/operations/coordination/reports/CNX-20260830-160-dashboard-single-send-durable-delivery-reacceptance.md`

Task-160 review:

`docs/operations/coordination/reviews/CNX-20260830-160-dashboard-single-send-durable-delivery-reacceptance-review.md`

## Objective

Identify the exact source/control-flow reason the accepted Dashboard durable-delivery fallback failed to establish durable authority on the real OpenClaw Dashboard/webchat path, reproduce that mechanism with a valid RED regression, implement the smallest safe CogentNexus-OpenClaw repair, and prove GREEN without weakening duplicate/no-regeneration safeguards.

## Root-cause questions that must be resolved before production change

Determine from the exact installed OpenClaw source/control flow and current plugin integration whether the public fallback is:

1. not invoked on the Dashboard/webchat reply path;
2. invoked only after the CogentNexus terminal guard has already made delivery unverifiable;
3. invoked with context/payload shape that prevents authoritative durable capture; or
4. failing for another specifically evidenced reason.

Do not select a repair until the causal path is demonstrated.

## TDD contract

### RED

Add the smallest regression test that faithfully represents the demonstrated Task-160 control-flow defect.

The RED test must fail against the current accepted source for the intended reason, not because of namespace, fixture, syntax, environment, or unrelated failures.

Record exact RED commit/run/job/failure evidence before production repair.

### Minimal repair

Change only the CogentNexus-OpenClaw production surface necessary to restore durable authority for the demonstrated Dashboard/webchat path.

The repair must preserve:

- Task-155 duplicate-safe durable authority for repeated final/public callbacks;
- one authoritative durable result per tested run/generation;
- no model regeneration merely because delivery is uncertain;
- terminal failure when durable authority genuinely cannot be established;
- current Ticket/workflow/delivery ownership boundaries;
- OpenClaw source as external/upstream code (no OpenClaw source patch).

Do **not** merely delete or bypass the `missing-append-before-deliver` guard.

### GREEN

At the exact repair SHA, run and record at minimum:

- repository Validate workflow / relevant full matrix;
- Windows PowerShell 5.1 Acceptance Smoke;
- Windows Installer Pack Smoke;
- full CogentNexus-OpenClaw plugin tests;
- Task-155 duplicate public-hook regression;
- the new Task-161 regression;
- dependency audit / existing package validation required by the repository.

Any production/source change requires fresh validation after the final production SHA.

## Repository-only authorization

Authorized:

- GitHub source/history/upstream-source read-only inspection;
- repository test creation/modification;
- minimal CogentNexus-OpenClaw production repair;
- repository documentation/report/review updates;
- CI/workflow execution and log inspection.

## Hard fence

Task 161 does **not** authorize:

- any Dashboard semantic Send;
- Dashboard click/focus/type/paste for semantic testing;
- any new semantic user message through another surface;
- real Windows install-over/uninstall/reinstall/reset;
- manual Ticket/workflow/result/outbox/delivery/database mutation;
- arbitrary live-state deletion;
- OpenClaw source patch;
- dependency upgrade;
- unrelated product behavior change;
- release/tag/package publication/promotion;
- merge to default/release branch;
- force push.

## Acceptance criteria

Task 161 may be accepted only when:

1. Task-160 live failure mechanism is source/control-flow evidenced rather than guessed;
2. a valid RED test fails for that mechanism before production change;
3. a minimal safe repair makes the regression GREEN;
4. Task-155 duplicate-safety behavior remains GREEN;
5. relevant full repository/plugin/Windows validation is GREEN on the exact production repair SHA;
6. no prohibited action occurred;
7. a durable Task-161 report and explicit ChatGPT self-review are published.

## Successor gate

Even a Task-161 ACCEPT does **not** authorize another Dashboard semantic Send.

The next live step must be a separate Hermes repaired-candidate Windows install-over + provenance/health acceptance task. Only after that checkpoint is reviewed ACCEPT may a new exactly-one-Send Dashboard reacceptance task be opened.
