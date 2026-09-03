# CNX-20260903-234 — Dashboard-Origin Discord-Session Durable Staging TDD Repair Review

Disposition: `REJECT_PASS_TDD_EVIDENCE_INCOMPLETE__FUNCTIONAL_REPAIR_GREEN__EXACT_TOPOLOGY_HARDENING_REQUIRED`
Reviewer: ChatGPT independent coordination review
Date: 2026-09-03 ICT

## Scope

Independently review Task 234 after Task 233 proved a real durable-delivery failure for a Dashboard-origin turn whose owner session remained:

`agent:main:discord:channel:1531199905673252946`

Task-234 report:

`docs/operations/coordination/reports/CNX-20260903-234-dashboard-origin-discord-session-durable-staging-tdd-repair.md`

Report HEAD:

`71ed478c6a403361510a06c83b0844fe2fc44f3e`

Candidate repair HEAD:

`43fd1d6f988431c7a94d24abc8a6811de46f78fa`

Candidate plugin payload fingerprint:

`964d471f9e330cfeffd270f2200d563dea8c3e7b9252409660df96f1173f58b7`

Public `v0.9.3` remains immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

## Findings

### 1. Functional root-cause direction is accepted

The Task-233 failure shape is consistent with the pre-repair staging scope mismatch:

- `before_agent_finalize` could correlate a Discord-associated owner;
- the later Dashboard durable staging path re-entered Dashboard-only ticket classification;
- the Dashboard-visible answer therefore could exist without a durable `direct_result`;
- Task 233 then reached `direct_redelivery_timeout`.

The Task-234 production change preserves owner identity and carries a trusted ingress-surface classification through the native transcript candidate instead of broadening `isDashboardSession()` globally.

The candidate repair also keeps a real Discord-origin context off the Dashboard staging path.

Result: `FUNCTIONAL_ROOT_CAUSE_AND_REPAIR_DIRECTION_ACCEPTED`.

### 2. The chosen ingress context has legitimate framework support

Task 234 identifies OpenClaw hook context fields including `messageProvider`, `channel`, and `channelId` as the framework-level surface metadata. Independent review of OpenClaw hook documentation also confirms that channel-originated runs expose provider-surface identity in `ctx.channel` / `ctx.messageProvider`, with `ctx.channelId` carrying the conversation target when available.

This is materially stronger than inferring ingress from prompt text, browser state, `@Ce`, or session-key syntax.

However, Task 235 must capture the exact installed `2026.7.1-2` contract/source or type definition used by the live runtime so the final accepted repair is tied to that exact version rather than only current documentation.

Result: `INGRESS_SIGNAL_DIRECTION_ACCEPTED__EXACT_VERSION_PROOF_REQUIRED`.

### 3. Exact repair SHA is cleanly GREEN in GitHub Actions

Fresh independent check of exact candidate SHA `43fd1d6f...` confirms:

- Validate `33760819493` — SUCCESS
- Windows Installer Pack Smoke `33760819324` — SUCCESS
- PS5.1 Acceptance Smoke `33760819312` — SUCCESS

The historical Task-233 Windows/Python 3.14 timeout therefore did not reproduce on this candidate tree.

Result: `CI_GREEN_EXACT_CANDIDATE`.

### 4. Repair scope is narrow

Task-234 branch lineage from the Task-234 opening authority contains three product/test commits:

1. `6b1e496fa67b0f09678268ba918a98a824610286` — new Task-234 test file only;
2. `278a235fa9df75990a3ea7f1a8e3930441ead76b` — ingress-aware production repair plus corrections to the new regression harness;
3. `43fd1d6f988431c7a94d24abc8a6811de46f78fa` — one TypeScript candidate annotation.

The production implementation change is confined to:

`plugins/cogentnexus-openclaw/src/v091-dashboard-verified-delivery.ts`

The new regression is:

`plugins/cogentnexus-openclaw/src/task234-dashboard-discord-ingress.test.ts`

The report commit after `43fd1d6f...` adds only the Task-234 report file.

Result: `SCOPE_NARROW_AND_TRACEABLE`.

### 5. The committed RED does not fully satisfy the Task-234 genuine-RED contract

Commit `6b1e496...` is test-only, which is good. However, the final working regression differs materially from that committed RED because harness corrections were committed together with the production repair in `278a235...`.

Those corrections include at least:

- initializing `sessionAuthority(...)` / delivery schema;
- awaiting the finalize hook;
- correcting the run/fixture shape used by the test.

Task-234 itself required a committed test-only RED that deterministically failed for the intended staging/ingress reason while the paired Discord-origin negative case remained valid.

Because the corrected harness and production repair landed in the same commit, the branch history does not independently prove that the **corrected production-shaped test** failed against predecessor production before the repair.

This is a TDD evidence/provenance gap, not evidence that the candidate repair is wrong.

Result: `TDD_RED_PROVENANCE_INCOMPLETE`.

### 6. The new production-shaped regression stops before exact-topology settlement

The final Task-234 test proves for Dashboard-origin + Discord-associated owner:

- marker-bearing message is returned;
- one `cnx_assistant_delivery` `direct_result` row exists;
- row is `pending` with the expected text.

It also proves a real Discord-origin context on the same owner does not create Dashboard staging.

But the Task-234 task required the production-shaped Dashboard-origin topology to continue through the native transcript authority boundary and prove:

- marker-bearing native transcript update;
- durable row becomes `delivered`;
- Ticket becomes `completed`;
- exactly one `delivery_confirmed` event;
- no `direct_redelivery_timeout` eligibility;
- recovery cannot regenerate the exact result;
- owner remains the Discord-associated key.

Existing `v162-dashboard-transcript-authority.test.ts` proves those downstream mechanics only with an ordinary `agent:main:dashboard:*` owner. It does not prove them on the newly authorized Discord-associated owner topology.

The production implementation appears capable of settling by run/idempotency marker without a Dashboard-only owner recheck, but this must be locked by a direct regression before live use.

Result: `EXACT_TOPOLOGY_SETTLEMENT_TEST_GAP`.

### 7. Ambiguous ingress context needs an explicit fail-closed contract

Current candidate helper logic checks `webchat` before `discord`. Therefore a contradictory context such as:

```text
messageProvider=discord
channel=webchat
```

would currently classify as Dashboard.

Task 234 required missing/ambiguous ingress identity to fail closed rather than grant the new cross-surface exception. If exact OpenClaw `2026.7.1-2` guarantees these fields are consistent provider-surface aliases, contradictory values are invalid framework state and should not authorize Dashboard staging. If the two fields have different exact semantics in that version, Task 235 must document the authoritative precedence instead of guessing.

Result: `AMBIGUOUS_INGRESS_CONTRACT_UNPROVEN`.

### 8. Live-system fences were preserved

Task 234 reports zero:

- Dashboard/Discord semantic Sends;
- semantic retries;
- recovery replay/resend;
- manual Ticket/outbox/recovery/SQLite writes;
- live install/plugin/lifecycle mutations;
- provider/model substitutions;
- process termination;
- historical Task-223/Task-233 evidence mutation;
- Release/tag/asset mutation;
- force push.

No evidence reviewed contradicts that ledger.

Result: `LIVE_FENCES_PRESERVED`.

## Independent disposition

`REJECT_PASS_TDD_EVIDENCE_INCOMPLETE__FUNCTIONAL_REPAIR_GREEN__EXACT_TOPOLOGY_HARDENING_REQUIRED`

This review does **not** reject the functional repair direction. `43fd1d6f...` is a strong GREEN candidate, but it is not yet accepted as live-install authority because the exact TDD/settlement evidence required by Task 234 is incomplete.

A bounded successor must:

1. capture the exact OpenClaw `2026.7.1-2` hook-context contract;
2. reconstruct the corrected regression against predecessor production in a disposable checkout and prove the intended genuine RED without product mutation;
3. strengthen the current regression through exact native transcript settlement on the Discord-associated owner;
4. define/test unknown and contradictory ingress contexts fail-closed according to the exact framework contract;
5. make no production change unless a newly added test exposes a real defect;
6. if a defect is exposed, follow a fresh test-only RED -> minimal repair -> GREEN sequence;
7. obtain full validation and exact-SHA Actions GREEN;
8. stop before live install or semantic requalification.

No live installation or semantic test is authorized by this review.
