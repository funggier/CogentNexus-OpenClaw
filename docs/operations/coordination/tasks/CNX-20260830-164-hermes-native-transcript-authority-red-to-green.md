# CNX-20260830-164 — Hermes Native Transcript Authority RED-to-GREEN Repair

Status: `READY_HERMES`

Execution mode: `REPOSITORY_DASHBOARD_NATIVE_TRANSCRIPT_AUTHORITY_REPAIR_HERMES`

Current authorization: `CNX-20260830-164_HERMES_REPOSITORY_DASHBOARD_NATIVE_TRANSCRIPT_AUTHORITY_REPAIR`

Task ID: `CNX-20260830-164`

Updated: 2026-08-30 ICT

Executor: Hermes

Coordinator / final reviewer: ChatGPT

Review type at completion: ChatGPT review required before successor authorization

## Purpose

Transfer the active Dashboard final-delivery authority repair to a fresh Hermes session after ChatGPT reached its practical context boundary.

Task 164 continues the parent Task-162 objective from an already committed and CI-proven production-faithful RED state. Hermes does **not** need to rediscover the entire Task-160/161/162 investigation from scratch, but must independently verify current GitHub state and exact source before changing production code.

Parent repair objective:

`docs/operations/coordination/tasks/CNX-20260830-162-dashboard-final-delivery-authority-repair-continuation.md`

Hermes Task-163 attempt and ChatGPT review:

- `docs/operations/coordination/reports/CNX-20260830-163-hermes-dashboard-final-delivery-authority-repair.md`
- `docs/operations/coordination/reviews/CNX-20260830-163-hermes-dashboard-final-delivery-authority-repair-review.md`

The Task-163 `BLOCKED` conclusion was **not accepted** because it omitted a public trusted-plugin runtime event that exists on the exact installed OpenClaw target:

`api.runtime.events.onSessionTranscriptUpdate(...)`

## Authoritative repository state at task creation

Repository:

`funggier/CogentNexus-OpenClaw`

Working branch:

`agent/v0.9.3-full-stabilization`

Exact RED checkpoint immediately before opening Task 164:

`61218ca6cc13a5c0312829abd72bcdb524944d12`

Commit message:

`test: add Task 162 native transcript authority RED`

This SHA is a handoff checkpoint only. Hermes must fetch GitHub immediately before starting and before every write. GitHub remote state is authoritative.

Exact upstream OpenClaw target remains read-only:

- version: `v2026.7.1-2`
- commit: `0790d9f593ad30c940ed93b5872a8cf6d6f3cf8c`

Do not patch, fork, vendor, or upgrade OpenClaw.

## Required reading before work

Read these first from the current GitHub branch:

1. `docs/operations/coordination/ACTIVE.md`
2. `docs/operations/coordination/STATUS.md`
3. this Task 164 file
4. `docs/operations/coordination/tasks/CNX-20260830-162-dashboard-final-delivery-authority-repair-continuation.md`
5. `docs/operations/coordination/reviews/CNX-20260830-163-hermes-dashboard-final-delivery-authority-repair-review.md`
6. `docs/operations/coordination/reports/CNX-20260830-160-dashboard-single-send-durable-delivery-reacceptance.md`
7. `plugins/cogentnexus-openclaw/src/v162-dashboard-transcript-authority.test.ts`
8. current production `plugins/cogentnexus-openclaw/src/v091-dashboard-verified-delivery.ts`
9. recovery authority in `skills/cogentnexus-openclaw/scripts/host_delivery.py`

Then inspect exact upstream OpenClaw source at the pinned commit for every primitive relied on by the repair.

## Proven source ordering and authority candidate

ChatGPT review of exact upstream `v2026.7.1-2` established the composite candidate:

1. the terminal assistant result is available on the post-model path;
2. `before_message_write` is invoked synchronously on the native SessionManager persistence path before the session JSONL write;
3. native `SessionManager.originalAppend(...)` then commits the message;
4. only after that native append, OpenClaw emits a session transcript update;
5. trusted native plugins can subscribe through:
   `api.runtime.events.onSessionTranscriptUpdate(...)`;
6. the transcript update exposes the persisted message plus native transcript/session/message identity;
7. therefore CogentNexus can bind a stable durable-delivery marker before native persistence, hold native-write ownership against recovery, and settle delivery only after observing the post-persistence transcript event.

The required conceptual order is:

`terminal assistant candidate -> before_message_write(marker + native claim) -> SessionManager originalAppend -> onSessionTranscriptUpdate(post-persistence receipt) -> CogentNexus delivery settlement`

Recovery injection must remain fenced while native-write ownership is active and must have no pending row to claim after native persistence is settled.

## Exact RED state already committed

Test-only RED commit:

`61218ca6cc13a5c0312829abd72bcdb524944d12`

New regression:

`plugins/cogentnexus-openclaw/src/v162-dashboard-transcript-authority.test.ts`

The test requires production wiring for:

- `reply_dispatch` production fact: no `appendBeforeDeliver` on the pre-model abort-aware wrapper;
- post-model terminal assistant correlation;
- `before_message_write` marker binding;
- a durable native-write claim that blocks Host recovery before native append;
- `runtime.events.onSessionTranscriptUpdate` subscription;
- no delivery confirmation before native persistence;
- post-persistence durable settlement after the transcript update;
- no pending recovery row after native persistence;
- no duplicate `delivery_confirmed` event;
- no second inference/regeneration.

### CI RED evidence

GitHub Actions at RED SHA:

- Validate run: `33318911825` — `FAILURE` as expected for RED
- PS5.1 Acceptance Smoke run: `33318911867` — `SUCCESS`
- Windows Installer Pack Smoke run: `33318911864` — `SUCCESS`

Validate failed consistently in the matrix at `npm test` because the new regression failed while the pre-existing suites remained green.

Observed failing test:

`src/v162-dashboard-transcript-authority.test.ts`

Observed first failing assertion:

`v162-dashboard-transcript-authority.test.ts:61`

`expect(beforeAgentFinalize).toBeTypeOf("function")`

Actual failure:

`expected undefined to be type of 'function'`

This is expected on pre-repair production code because `installV091DashboardVerifiedDelivery(...)` has not yet wired the composite native transcript authority path required by the new RED.

Hermes must preserve this RED commit in history. Do not rewrite, squash away, or replace the test-only RED checkpoint.

## Objective

Implement the smallest CogentNexus-OpenClaw production repair that makes the committed Task-162 regression GREEN while preserving all previously accepted duplicate/no-regeneration and recovery guarantees.

Do not weaken the regression merely to make it pass. If fresh exact-source inspection disproves an assumption in the committed test, stop and report the discrepancy before production mutation rather than silently changing the authority contract.

## Required production investigation before edit

Before changing production code, verify on the pinned OpenClaw source:

1. exact public registration surface and event shape for `before_agent_finalize`;
2. exact public registration surface and synchronous semantics for `before_message_write`;
3. exact `PluginRuntime.events.onSessionTranscriptUpdate` API/event fields on `v2026.7.1-2`;
4. exact ordering proving the transcript update occurs after `SessionManager.originalAppend`;
5. whether the event carries enough session/message identity to correlate only the exact marker-bearing assistant row;
6. whether any paths can emit transcript updates for non-assistant/tool/user messages that require filtering;
7. whether compaction/redaction/message rewriting can alter or remove the marker before the post-persistence event;
8. how listener lifecycle/unsubscribe should be owned by the plugin without leaks or duplicate registration;
9. how the native-write claim interacts with current `host_delivery.py` claim expiry and recovery predicates;
10. how crash windows behave:
   - before `before_message_write`;
   - after native claim but before `originalAppend`;
   - after `originalAppend` but before transcript event handling;
   - after transcript event but before CogentNexus DB settlement.

The repair must remain safe across those windows. Liveness recovery may be conservative, but duplicate semantic assistant output is prohibited.

## Minimal repair constraints

Production changes should be limited to the smallest necessary CogentNexus surfaces, expected primarily around:

`plugins/cogentnexus-openclaw/src/v091-dashboard-verified-delivery.ts`

and only if actually required, narrowly scoped durable-store/recovery support already owned by CogentNexus.

Do not perform unrelated refactors.

The repair must preserve:

- Task-155 duplicate public-hook safety;
- exactly one authoritative assistant result per run/generation;
- no re-inference after an assistant result exists;
- no native-send + recovery-inject duplicate;
- fail-closed behavior when persistence cannot be proven;
- existing Ticket/workflow/delivery ownership boundaries;
- current host recovery fencing semantics;
- OpenClaw as read-only external code.

## RED -> minimal fix -> GREEN contract

### Phase A — verify existing RED

Hermes must first confirm the branch still contains the test-only RED commit and that the failure remains attributable to missing production wiring, not unrelated drift.

Do not create a new replacement RED unless the existing test is proven invalid.

### Phase B — minimal production repair

After verifying the RED, implement only the smallest repair required by the production-faithful contract.

Production implementation must not settle CogentNexus delivery at `before_message_write`; that hook is pre-persistence. It may bind identity/marker and establish a bounded native-write ownership claim, but final success must wait for the post-persistence transcript update.

Do not treat `reply_payload_sending`, transport broadcast, text equality alone, or `chat.inject` as native persistence authority.

### Phase C — GREEN validation

At the exact final production repair SHA, run and record at minimum:

1. targeted `v162-dashboard-transcript-authority.test.ts`;
2. full CogentNexus-OpenClaw plugin tests;
3. Task-155 duplicate/no-regeneration regression;
4. repository `Validate` workflow full matrix;
5. Windows PowerShell 5.1 Acceptance Smoke;
6. Windows Installer Pack Smoke;
7. repository package/plugin validation and dependency audit required by the current workflow.

Any production/source change after a validation run invalidates that run for final acceptance and requires fresh validation on the new exact SHA.

## Repository-only authorization

Hermes is authorized to:

- inspect GitHub repository state/history;
- inspect pinned upstream OpenClaw source read-only;
- verify the existing Task-162 RED;
- make the minimal CogentNexus-OpenClaw production repair;
- add narrowly necessary regression coverage if the repair exposes an adjacent case, while preserving the original RED;
- run repository-local tests;
- trigger/inspect repository CI/workflows;
- commit/push only to `agent/v0.9.3-full-stabilization` with normal non-force history;
- publish the required Task-164 report.

## Hard fence — prohibited actions

Hermes must NOT:

- send any semantic Dashboard message;
- click/focus/type/paste into Dashboard for semantic testing;
- send semantic user input through any other live OpenClaw surface;
- install-over, uninstall, reinstall, or reset the real Windows candidate;
- restart/mutate live Gateway, Ollama, Supervisor, or OpenClaw runtime;
- manually edit Ticket/workflow/result/outbox/delivery/database live state;
- delete arbitrary live state;
- patch OpenClaw source;
- upgrade dependencies;
- change unrelated product behavior;
- publish a release/tag/package;
- merge to default/release branch;
- force push.

Hosted repository CI is allowed. Real-machine lifecycle or semantic acceptance is not.

## Coordination ownership

While Task 164 is active, Hermes is the executor. ChatGPT remains coordinator/final reviewer.

Hermes should work continuously through repository investigation, minimal repair, and GREEN validation without asking for routine confirmation.

Hermes must not open a live-successor task or perform a Dashboard Send on its own.

At completion, publish a report with one disposition:

- `PASS` — RED preserved, minimal production repair GREEN, required validation GREEN;
- `FAIL` — repair or validation is demonstrably incorrect;
- `BLOCKED` — exact source disproves the composite authority path or another external constraint prevents a safe repair.

Do not convert uncertainty into PASS.

## Required completion report

Create:

`docs/operations/coordination/reports/CNX-20260830-164-hermes-native-transcript-authority-red-to-green.md`

The report must include:

1. exact starting HEAD;
2. verification of the inherited RED commit and CI failure;
3. exact upstream source evidence for all public hooks/runtime events used;
4. crash-window and duplicate-safety argument;
5. production repair commit(s);
6. files changed;
7. targeted and full tests;
8. workflow run IDs / job results;
9. exact final HEAD;
10. hard-fence compliance statement;
11. PASS / FAIL / BLOCKED;
12. recommended next action for ChatGPT review.

## Acceptance gate

Task 164 itself does not authorize any new Dashboard Send or live Windows mutation, even if Hermes reports PASS.

ChatGPT must review the report, exact diff, tests, and final GitHub state first.

Only after explicit ChatGPT acceptance may coordination advance to a separate repaired-candidate Windows install-over + provenance/health checkpoint. Only after that later checkpoint is accepted may an exactly-one-Send Dashboard reacceptance task be considered.
