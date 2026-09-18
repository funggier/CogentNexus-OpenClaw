# CNX-20260918-421 — OpenClaw Current Upgrade Qualification and Harness-Agnostic Ticket-First Admission

Status: `READY_FOR_HERMES`

## Authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Parent: `CNX-20260918-420`
- Executor: `Hermes`
- Reviewer: `ChatGPT`
- Human final authority: `Operator`
- Parent report: `docs/operations/coordination/reports/CNX-20260918-420-operator-fresh-session-ollama-route-ticket-first-discrimination-report.md`
- Parent review: `docs/operations/coordination/reviews/CNX-20260918-420-chatgpt-review.md`

GitHub remote is authoritative.

## Operator direction

The Operator has stated that if the newer OpenClaw structure is better for CogentNexus, moving to the current version is desirable.

Treat that as authority to qualify the current upstream generation and prepare a bounded migration candidate.

It is **not** authority to mutate the live OpenClaw installation inside this task.

## Starting facts

CNX-420 is accepted PASS for the fresh Ollama path:

`PASS_OPERATOR_FRESH_SESSION_OLLAMA_TICKET_FIRST_VERTICAL_SLICE`

CNX-419 remains valid evidence that the Codex/plugin-harness path can bypass the current CogentNexus `before_agent_run` admission boundary.

Installed/live OpenClaw baseline:

`2026.7.1-2 (0790d9f)`

Upstream qualification target:

`v2026.9.4`

Known architectural facts to verify from exact upstream source, not assumption:

- `before_agent_run` is not a universal input gate across all harnesses;
- `before_dispatch` is pre-model and carries canonical inbound identity fields but not the Dashboard run ID;
- `reply_dispatch` is pre-model and carries `replyOptions.runId`;
- Dashboard `chat.send` supplies a stable run/idempotency key into the dispatch path;
- OpenClaw v2026.8.1+ crosses a major session/transcript and Plugin SDK migration boundary;
- current OpenClaw keeps provider/model selection as host authority.

## Objective

Answer two questions with exact evidence before any live upgrade:

1. Is OpenClaw v2026.9.4 a safer/better structural baseline for CogentNexus than the installed 2026.7.1-2 baseline?
2. What exact pre-model admission seam can enforce Ticket-first across both the built-in Ollama path and the Codex/OpenAI plugin-harness path without making CogentNexus a provider router?

Produce either a qualified current-version migration path or a precise blocker.

## Required invariant

Target:

`NO TICKET = NO MODEL EXECUTION`

This invariant must be interpreted only for eligible external owner turns.

Internal delivery, continuation, recovery, subagent, lifecycle, and other explicitly excluded control paths must remain outside ordinary Ticket intake where their existing contracts require that behavior.

## Stage 1 — authority and baseline recheck

Before source changes:

- verify remote branch HEAD and clean coordination state;
- verify CNX-420 review exists and is `ACCEPTED_PASS`;
- verify this task is `READY_FOR_HERMES`;
- record installed OpenClaw version without mutation;
- record canonical CogentNexus plugin version/fingerprint where available;
- record live Gateway/controller health read-only;
- record that there is no active semantic acceptance run.

If authority has moved, stop and reconcile before changing repository source.

## Stage 2 — exact upstream contract comparison

Compare exact source/contracts for:

- installed `2026.7.1-2`;
- target `v2026.9.4`.

At minimum characterize:

### Dispatch and admission

- `before_dispatch` ordering and result semantics;
- `reply_dispatch` ordering and result semantics;
- `before_agent_run` ordering and exact runner/harness coverage;
- Dashboard `chat.send` run/idempotency propagation;
- Codex/plugin-harness entry point;
- embedded/Ollama entry point;
- model-call lifecycle hooks;
- dispatch cancellation/abort ownership;
- reply dispatcher ownership.

### Identity and trust

For each candidate seam, record whether it exposes:

- session key;
- run ID;
- message ID;
- authenticated Gateway scopes/owner identity;
- channel/account/conversation identity;
- internal-vs-owner request distinguishers.

Do not weaken the owner-trust boundary merely to gain earlier admission.

### Provider/model authority

Prove which layer owns:

- selected provider;
- selected model;
- session override;
- fallback;
- harness/runtime selection.

Required conclusion:

CogentNexus does not become a provider/model router.

### Persistence and upgrade boundary

Characterize v2026.8.1+ changes relevant to:

- session/transcript persistence;
- migration behavior;
- downgrade/rollback;
- plugin SDK exports/import paths;
- plugin manifest/config;
- hook registration;
- update/recovery behavior.

## Stage 3 — reachability matrix

Create a compact model-execution reachability matrix for at least:

1. Dashboard -> Ollama built-in/embedded;
2. Dashboard -> Codex/OpenAI plugin harness;
3. Discord owner turn;
4. internal verified-delivery turn;
5. post-compaction continuation;
6. direct recovery;
7. subagent/synthetic worker.

For every path record:

- earliest trusted owner boundary;
- first stable session identity;
- first stable run identity;
- first harness-selection point;
- earliest hook capable of handling/blocking the turn;
- whether `before_agent_run` runs;
- whether `reply_dispatch` runs;
- whether a Ticket must exist;
- expected delivery ownership.

Do not call any seam universal until this matrix proves it for the intended external-owner surfaces.

## Stage 4 — admission architecture decision

Prefer one shared admission kernel rather than duplicated policy logic.

Expected candidate shape:

`trusted owner turn -> shared Ticket admission kernel -> Ticket accept/route -> host harness/provider -> execution -> durable delivery`

For Dashboard/channel dispatch paths, characterize `reply_dispatch` as the leading run-correlated candidate.

Retain `before_agent_run` as:

- deeper defense for supported runners;
- duplicate/idempotency confirmation;
- lifecycle integrity gate where still required.

Use `before_dispatch` only where its identity/trust properties add value. Do not synthesize a fake run ID merely to use an earlier hook.

Required duplicate properties:

- one eligible semantic turn -> one Ticket;
- later deeper hook with same owner session + run ID -> no second Ticket;
- no duplicate route event;
- no duplicate model call;
- no duplicate delivery.

## Stage 5 — RED characterization tests

Before production source repair, add tests that fail for the currently missing contract.

At minimum:

- Dashboard/Codex path receives Ticket admission before plugin-harness model execution;
- Dashboard/Ollama path remains Ticket-first;
- the same turn reaching both early admission and `before_agent_run` remains one Ticket;
- direct/non-durable turn still proceeds to OpenClaw's selected harness;
- durable turn is diverted to the durable dispatcher before conversational inference;
- provider/model selection is not mutated by CogentNexus;
- internal delivery marker is excluded from ordinary admission;
- continuation/recovery path is not double-admitted;
- subagent/synthetic paths are excluded as intended;
- owner-trust failure cannot create a privileged Ticket.

Record RED evidence before repair.

## Stage 6 — bounded repository repair candidate

Only if Stages 2-5 identify a proven seam, implement the minimum repository source change needed to centralize admission and cover the missing Codex/plugin-harness path.

Constraints:

- TDD: RED -> minimal repair -> GREEN;
- do not add an independent provider router;
- do not force Ollama/OpenAI;
- preserve TicketStore idempotency semantics;
- preserve existing delivery/recovery/session-generation contracts;
- preserve CNX-420 healthy Ollama behavior;
- avoid broad unrelated refactors;
- add comments only where host-boundary rationale is non-obvious.

If no safe seam is proven:

`BLOCKED_HARNESS_AGNOSTIC_ADMISSION_SEAM`

Do not guess a repair.

## Stage 7 — isolated v2026.9.4 compatibility qualification

Use an isolated clone/worktree/temp state only.

Do **not** point v2026.9.4 at the live OpenClaw state.

Qualification must cover, as applicable:

- plugin build/typecheck;
- unit/contract tests;
- CogentNexus plugin load/registration;
- required hook registration;
- plugin SDK import compatibility;
- config/manifest compatibility;
- copied-state session/transcript migration behavior;
- clean fresh-state startup behavior;
- isolated Gateway startup/shutdown on non-live ports/state;
- rollback/downgrade implications documented from copied state;
- no live scheduled-task or service takeover.

No external semantic provider call is required in this task.

If network/model access would be required, stop at deterministic isolated qualification and report the remaining acceptance gap.

## Stage 8 — timeout-authority characterization

Without sending a new model request, inspect source/config contracts explaining how a model call with emitted `timeoutMs=900000` could complete after approximately 44m43s.

Classify whether the emitted deadline is:

- advisory/observational;
- enforced only by a runner that the Ollama path bypassed;
- superseded by another runtime timeout;
- incorrectly recorded;
- or still unresolved.

Do not change live timeout configuration in this task.

## Upgrade decision gate

Return one of:

### A — current generation qualified

`READY_FOR_CONTROLLED_OPENCLAW_2026_9_4_UPGRADE`

Requires:

- v2026.9.4 isolated compatibility GREEN;
- migration/rollback boundary understood;
- CogentNexus plugin can load on the target SDK;
- admission architecture is compatible with the target dispatch contract;
- no unresolved blocker threatens live session continuity.

### B — architecture repair valid, upgrade not yet safe

`ADMISSION_REPAIR_READY_OPENCLAW_UPGRADE_BLOCKED`

Use when the Ticket-first source candidate is sound but v2026.9.4 migration/plugin compatibility has a blocker.

### C — target structure unsuitable or insufficiently proven

`STAY_ON_OPENCLAW_2026_7_1_2_PENDING_COMPATIBILITY_REPAIR`

Use only with exact evidence.

### D — evidence incomplete

`BLOCKED_CURRENT_UPGRADE_QUALIFICATION`

## Hard fences

- semantic sends: 0;
- direct Ollama/OpenAI/provider probes: 0;
- browser mutation: 0;
- live provider/model config mutation: 0;
- live OpenClaw upgrade: 0;
- live session/transcript migration: 0;
- live plugin install-over/uninstall: 0;
- live Gateway restart for upgrade: 0;
- manual Ticket/outbox/recovery/SQLite mutation: 0;
- release/tag/main: 0;
- force push/history rewrite: 0.

Repository source/tests/docs on the working branch are allowed when required by TDD.

Temporary isolated OpenClaw v2026.9.4 state/processes are allowed only when they cannot bind to or mutate the live installation/state/ports/services.

## Required report

Publish:

`docs/operations/coordination/reports/CNX-20260918-421-openclaw-current-upgrade-qualification-and-harness-agnostic-ticket-first-admission-report.md`

Include:

- starting/ending exact HEAD;
- upstream source/tag/commit provenance;
- 7.1-2 vs 9.4 contract comparison;
- model-execution reachability matrix;
- selected admission seam and rejected alternatives;
- trust-boundary analysis;
- RED/GREEN test evidence if a repair candidate is implemented;
- files/commits changed;
- isolated v2026.9.4 qualification evidence;
- session/transcript migration and rollback findings;
- timeout-authority finding;
- exact upgrade decision classification;
- remaining risks/gaps.

Closeout:

1. set ACTIVE.md and STATUS.md to `WAITING_FOR_CHATGPT_REVIEW`;
2. verify local HEAD equals remote HEAD;
3. verify clean publication worktree;
4. stop;
5. do not perform the live upgrade or create its successor task before ChatGPT review.
