# CNX-20260831-191 — NO_REPLY Direct Dashboard Semantic Repair

- **Status:** `IN_PROGRESS`
- **Date:** 2026-08-31 ICT
- **Repository:** `funggier/CogentNexus-OpenClaw`
- **Working branch:** `agent/v0.9.3-full-stabilization`
- **Parent umbrella:** `CNX-20260831-188`
- **Triggered by:** `CNX-20260831-190`
- **Executor:** ChatGPT / repository CI
- **Final live verifier:** Hermes on accepted Windows host + one genuine human Dashboard Send only after a repaired candidate is frozen
- **Coordinator / final reviewer:** ChatGPT

## Goal

Repair the direct Dashboard semantic boundary exposed by Task 190 without replaying unrelated lifecycle work.

A genuine human Dashboard request must never turn the OpenClaw silent sentinel `NO_REPLY` / `no_reply` into a durable visible CogentNexus assistant result.

For a genuine direct Dashboard turn, when the natural final assistant answer is the bare silent sentinel, CogentNexus must request at most one bounded same-run finalization revision so the model can produce a visible answer. It must not fabricate semantic content, create another Ticket, start an external recovery run, or perform another human Send.

## Evidence and root cause

Task-190 report:

`docs/operations/coordination/reports/CNX-20260831-190-task189-phase-e-human-send-orchestration-and-evidence-closure.md`

Observed accepted chain before semantic failure:

`1 human Send -> 1 Ticket -> 1 run -> 1 provider/model call -> 1 durable delivery -> 1 Dashboard bubble`

but durable and visible assistant text was exactly:

`NO_REPLY`

Task-190 therefore correctly classified `FAIL_SEMANTIC_DURABLE_DELIVERY`.

Repository investigation shows:

1. `v091-dashboard-verified-delivery.ts` takes any non-empty assistant final text and stages it as `cnx_assistant_delivery(kind='direct_result')`.
2. `before_message_write` adds a CogentNexus delivery marker to staged text.
3. For a bare `NO_REPLY`, that marker changes the payload from OpenClaw's exact silent sentinel into non-sentinel visible text, bypassing normal OpenClaw suppression.
4. OpenClaw upstream currently documents `NO_REPLY` as a background/silent sentinel and has known direct/DM cases where small/local models can still return the token on ordinary direct turns because silent-reply guidance leaks into the model prompt. CogentNexus cannot safely assume the model will never emit it on the accepted OpenClaw baseline.

## Architecture

Repair two adjacent boundaries in the existing Dashboard verified-delivery module only:

1. **Sentinel staging fence** — recognize only a *bare* case-insensitive `NO_REPLY` token after trim as silent. Never stage it, never add a delivery marker, and never settle it as a durable direct result.
2. **Bounded direct-final revision** — in `before_agent_finalize`, if and only if the current run has an accepted direct Dashboard Ticket and the natural final answer is the bare silent sentinel, return one OpenClaw `action: 'revise'` decision with an idempotency key and `maxAttempts: 1`. The instruction must require a visible answer to the user's current request and explicitly forbid `NO_REPLY` for this direct turn. Do not synthesize or infer the requested answer in CogentNexus.

OpenClaw owns the same-run revision pass. CogentNexus only supplies the bounded finalization decision.

## Global constraints

- Preserve accepted OpenClaw baseline `2026.7.1-2 (0790d9f)`.
- Preserve managed provider contract: Ollama only.
- No dependency changes.
- No workflow behavior changes unrelated to this direct semantic boundary.
- No durable-schema changes.
- No reset, uninstall, fresh reinstall, state deletion, or provider replacement during repository repair.
- No release PR/merge/tag/release publication until repaired candidate passes exact-candidate CI and bounded Windows requalification.
- No force push.
- TDD is mandatory: RED -> minimal fix -> GREEN.
- Exact bare sentinel only: mixed substantive text containing `NO_REPLY` must not be treated as silent by this repair.
- A sentinel-triggered revision is bounded to one same-run finalization revision; no external retry/recovery loop.

## Files

Primary implementation:

- `plugins/cogentnexus-openclaw/src/v091-dashboard-verified-delivery.ts`

Regression tests:

- `plugins/cogentnexus-openclaw/src/v091-dashboard-verified-delivery.test.ts`

Coordination/report files only as needed after code/test evidence exists.

## Task 1 — RED: prove bare sentinel leakage

Add a focused regression test using a direct Dashboard Ticket and the existing registered hooks.

Required assertions before production repair:

- `stageDashboardDirectResult(..., text: 'NO_REPLY')` must be expected to return `{ staged:false, reason:'silent-reply' }`.
- case/whitespace variant such as `"  no_reply  "` must have the same result.
- no `cnx_assistant_delivery` row is created for the Ticket.
- no delivery marker is added to the sentinel.
- substantive text containing the token, e.g. `"Actual answer: NO_REPLY is a sentinel"`, remains ordinary visible content and may still be staged.

Run the targeted Vitest test and record the expected RED failure against the current source before editing production code.

## Task 2 — RED: prove bounded direct revision contract

Add a focused hook-level regression test for `before_agent_finalize`.

Set up an accepted direct Dashboard Ticket for a run, install `installV091DashboardVerifiedDelivery`, capture the registered `before_agent_finalize` hook, and assert:

- natural final exactly `NO_REPLY` returns `action:'revise'`;
- retry metadata includes an idempotency key stable for that run and `maxAttempts:1`;
- instruction says the direct user request requires a visible answer and forbids bare `NO_REPLY`;
- ordinary visible assistant text returns no revision;
- a non-Dashboard or non-ticketed run returns no revision;
- mixed substantive text containing `NO_REPLY` returns no revision.

Run the targeted test and record RED before production code changes.

## Task 3 — GREEN: minimal production repair

Implement a private helper in `v091-dashboard-verified-delivery.ts` equivalent in semantics to:

```ts
function isBareSilentReply(text: string) {
  return /^NO_REPLY$/iu.test(text.trim());
}
```

Do not match token suffixes/prefixes or mixed text.

Apply the helper at the earliest durable staging boundary:

```ts
const text = input.text.trim();
if (!text) return { staged:false, reason:'empty-text' };
if (isBareSilentReply(text)) return { staged:false, reason:'silent-reply' };
```

Then extend the existing `before_agent_finalize` registration:

- resolve `runId` and `sessionKey` exactly as the current hook already does;
- if the final text is a bare sentinel and `dashboardTicket(path, runId)` confirms an accepted direct Dashboard Ticket, return:

```ts
{
  action: 'revise',
  reason: 'direct Dashboard request produced a silent sentinel',
  retry: {
    instruction: 'This is a genuine direct Dashboard user request. Produce a visible answer to the current user request. Do not return NO_REPLY/no_reply for this turn.',
    idempotencyKey: `cnxclaw-dashboard-visible-final:${runId}`,
    maxAttempts: 1,
  },
}
```

The exact final wording may be tightened, but must not copy/derive the answer itself from the user prompt.

For ordinary visible final text, preserve the existing transcript-candidate behavior unchanged.

## Task 4 — GREEN verification

Run:

- targeted `v091-dashboard-verified-delivery.test.ts`;
- plugin TypeScript/build validation;
- full plugin test suite;
- repository validation workflow(s) appropriate to a plugin production-source change.

No production success may be claimed until targeted and broader suites are green.

## Task 5 — candidate freeze and proportional Windows requalification

Because this is an executable plugin behavior change, the old product candidate `604569c286e930f1a596362ab926b065b56d486e` is superseded only after repository tests/CI are green.

Freeze a new exact candidate SHA and recompute product/package identities.

Windows requalification default scope:

1. read-only host baseline;
2. one supported install-over of the new exact candidate;
3. prove installed executable/plugin bytes match candidate;
4. prove managed Ollama/Gateway/delivery/SQLite health;
5. one genuine human Dashboard semantic turn orchestrated by Hermes;
6. prove:
   `1 human Send -> 1 Ticket -> one logical run with at most one host-owned finalization revision -> 1 durable assistant delivery -> 1 logical visible Dashboard assistant result`;
7. prove no external direct-recovery run, duplicate Ticket, duplicate durable delivery, retry Send, regeneration, or pending terminal outbox residue.

The same-run OpenClaw finalization revision, if the first natural final is bare `NO_REPLY`, is permitted and must be observable as such; it is not an external CogentNexus recovery run.

Do not repeat reset/uninstall/fresh reinstall unless new evidence shows lifecycle impact attributable to this repair.

## Stop conditions

Stop and report instead of broadening scope if:

- the repair requires OpenClaw baseline upgrade;
- a same-run bounded finalization revision cannot be expressed on `2026.7.1-2` plugin API;
- durable schema changes become necessary;
- the fix requires fabricating user-visible semantic content inside CogentNexus;
- more than one revision/retry is needed to obtain a visible direct answer;
- Windows evidence shows unrelated lifecycle drift.

## Completion disposition

Task 191 is PASS only when:

- RED evidence was observed before production edit;
- sentinel staging leakage is fixed;
- bounded direct-final revision behavior is covered by tests;
- targeted + full relevant CI are green;
- new exact product candidate is frozen;
- bounded real-Windows semantic requalification passes;
- release publication can safely resume under Task 188.
