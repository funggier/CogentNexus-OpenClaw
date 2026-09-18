# CNX-20260918-422 — Reply-Dispatch Ticket-First Repair and OpenClaw 2026.9.4 Isolated Qualification

Status: `READY_FOR_HERMES`

## Authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Parent: `CNX-20260918-421`
- Executor: `Hermes`
- Reviewer: `ChatGPT`
- Human final authority: `Operator`
- Parent report: `docs/operations/coordination/reports/CNX-20260918-421-openclaw-current-upgrade-qualification-and-harness-agnostic-ticket-first-admission-report.md`
- Parent review: `docs/operations/coordination/reviews/CNX-20260918-421-chatgpt-review.md`

GitHub remote is authoritative.

## Objective

Complete the work CNX-421 did not finish.

Prove and implement, with TDD, a harness-agnostic Ticket-first admission boundary at `reply_dispatch`, then qualify the CogentNexus plugin against OpenClaw v2026.9.4 using isolated state only.

Do not upgrade the live OpenClaw installation in this task.

## Established source facts

Treat these as hypotheses to re-verify from exact source before repair:

- `reply_dispatch` runs before ordinary model/harness dispatch;
- `reply_dispatch.event.runId` is the real dispatch run identifier;
- `reply_dispatch.event.ctx` is `FinalizedMsgContext`;
- the finalized context contains message text;
- v2026.9.4 exposes `InboundAccessAuthorized`;
- `GatewayClientScopes` remains available;
- `before_agent_run` is not universal for Codex/plugin harnesses;
- OpenClaw owns provider/model/fallback/harness selection.

Target invariant:

`NO TICKET = NO MODEL EXECUTION`

for eligible external owner turns.

## Stage 1 — authority and exact contract recheck

Verify:

- remote HEAD;
- ACTIVE/STATUS;
- CNX-421 review;
- this task is READY_FOR_HERMES;
- installed OpenClaw remains 2026.7.1-2;
- target upstream is v2026.9.4;
- no active semantic acceptance run.

Re-read exact OpenClaw source for:

- `PluginHookReplyDispatchEvent`;
- `FinalizedMsgContext`;
- `createReplyDispatchEvent`;
- dispatch ordering;
- hook takeover result semantics;
- Codex/plugin harness entry;
- embedded/Ollama entry.

## Stage 2 — define shared admission kernel

Refactor only as much as necessary to produce one deterministic admission function that accepts normalized trusted input such as:

- owner session key;
- exact run ID;
- prompt/user content;
- trust proof;
- workspace/database location;
- Ticket-first configuration;
- control-path classification.

The kernel must:

- reject missing/contradictory identity;
- exclude subagents/synthetic/control/delivery/continuation paths as intended;
- call `TicketStore.accept()` exactly once logically per semantic turn;
- route at most once;
- preserve direct vs durable behavior;
- never mutate provider/model/harness selection;
- fail closed where a Ticket is required but persistence fails.

Do not duplicate policy separately inside `reply_dispatch` and `before_agent_run`.

## Stage 3 — RED characterization suite

Before production repair, add tests that fail against the current implementation.

At minimum:

1. Dashboard/Codex-style plugin harness path must create Ticket before model/harness execution.
2. Dashboard/Ollama/embedded path remains Ticket-first.
3. Same semantic turn crossing `reply_dispatch` and later `before_agent_run` produces one Ticket only.
4. Route-event cardinality remains one.
5. Direct request remains direct and continues through OpenClaw-selected model/harness.
6. Durable request is blocked/diverted before conversational inference.
7. CogentNexus never changes provider/model/harness fields.
8. Internal delivery markers do not create ordinary owner Tickets.
9. Post-compaction continuation does not create duplicate Ticket.
10. Direct recovery does not create duplicate Ticket.
11. Subagent/synthetic sessions are excluded.
12. Missing/untrusted ingress proof cannot create a privileged Ticket.
13. v2026.9.4 `InboundAccessAuthorized=true` is accepted as trusted ingress proof for applicable external-owner dispatch.
14. contradictory trust/identity fails closed.

Record exact RED output before modifying production source.

## Stage 4 — minimal repair

Implement the smallest production change needed to make the RED suite GREEN.

Preferred structure:

`reply_dispatch adapter -> shared admission kernel`

plus:

`before_agent_run adapter -> same shared admission kernel`

for defense-in-depth/idempotency on supported runners.

Important:

- do not create a second provider router;
- do not force Ollama;
- do not force OpenAI;
- do not synthesize fake run IDs when a real one exists;
- do not bypass OpenClaw session/model authority;
- preserve existing delivery adapter behavior;
- preserve recovery/session-generation contracts.

## Stage 5 — focused GREEN

Run:

- new CNX-422 tests;
- existing `index.test.ts`;
- dashboard delivery tests;
- inference/model-call lease tests;
- direct recovery tests;
- session lifecycle/generation tests;
- Discord-specific Ticket/inference tests;
- plugin build/typecheck.

Then run the plugin's broader test suite if feasible.

Any regression must be characterized before additional source changes.

## Stage 6 — OpenClaw v2026.9.4 SDK compatibility

The plugin currently declares:

- peer dependency: `openclaw >=2026.5.17`;
- dev dependency: `openclaw 2026.7.1-2`.

Create an isolated qualification environment for v2026.9.4.

Do not blindly change the published package metadata first.

Prove:

- TypeScript compile against v2026.9.4;
- SDK imports resolve;
- `definePluginEntry` and hook typing remain compatible;
- manifest/config schema remains valid;
- hook registration succeeds;
- plugin loads without deprecated/private import breakage.

If the source repair intentionally requires v2026.9.4-only trust fields, document the new minimum supported OpenClaw version and adjust dependency metadata only when justified by tests.

## Stage 7 — isolated runtime qualification

Use non-live state/ports/processes only.

Run at least two isolated cases:

### Fresh state

- clean OpenClaw v2026.9.4 state;
- CogentNexus plugin installed from the candidate build;
- isolated Gateway starts;
- plugin loads;
- expected hooks register;
- deterministic local dispatch/hook contract tests execute without external semantic provider traffic;
- Gateway shuts down cleanly.

### Copied state

Use a copy of relevant live state, never the live files.

Characterize:

- session/transcript migration behavior;
- stale pending delivery/recovery residue behavior;
- plugin state migration;
- startup behavior;
- downgrade/rollback implications.

The old residue is test input, not permission to mutate live state.

## Stage 8 — migration and rollback decision

Document exactly:

- what v2026.9.4 changes on first start;
- whether migration is one-way;
- which files/DBs/state must be backed up;
- whether 2026.7.1-2 can reopen the migrated copy;
- required rollback procedure;
- whether CogentNexus installer/reset/uninstall assumptions need revision.

## Stage 9 — final classification

Use one:

### READY

`READY_FOR_CONTROLLED_OPENCLAW_2026_9_4_UPGRADE`

Requires:

- RED captured;
- minimal repair implemented;
- GREEN;
- plugin builds against target;
- isolated fresh-state runtime GREEN;
- copied-state migration characterized;
- rollback plan proven or bounded;
- no unresolved Ticket-first trust blocker.

### REPAIR READY, UPGRADE BLOCKED

`ADMISSION_REPAIR_READY_OPENCLAW_UPGRADE_BLOCKED`

### REPAIR BLOCKED

`BLOCKED_REPLY_DISPATCH_TICKET_FIRST_REPAIR`

### QUALIFICATION BLOCKED

`BLOCKED_OPENCLAW_2026_9_4_ISOLATED_QUALIFICATION`

## Hard fences

- semantic sends: 0;
- external provider probes: 0;
- browser mutation: 0;
- live provider/model mutation: 0;
- live OpenClaw upgrade: 0;
- live session/transcript migration: 0;
- live plugin install-over/uninstall: 0;
- live Gateway restart for upgrade: 0;
- manual mutation of live Ticket/outbox/recovery/SQLite state: 0;
- release/tag/main: 0;
- force push/history rewrite: 0.

Repository source/tests/docs changes on the working branch are authorized.

Temporary v2026.9.4 processes and copied/fresh state are authorized only when isolated from live ports/state/services.

## Required report

Publish:

`docs/operations/coordination/reports/CNX-20260918-422-reply-dispatch-ticket-first-repair-and-openclaw-2026-9-4-isolated-qualification-report.md`

Include:

- starting/ending exact HEAD;
- exact upstream source provenance;
- corrected `reply_dispatch` context analysis;
- RED evidence;
- production repair diff summary;
- GREEN evidence;
- provider/model non-mutation proof;
- trust-boundary proof;
- files/commits changed;
- v2026.9.4 build/plugin-load evidence;
- isolated fresh-state result;
- copied-state migration result;
- rollback findings;
- remaining risks;
- final classification.

Closeout:

1. publish report;
2. set ACTIVE.md and STATUS.md to `WAITING_FOR_CHATGPT_REVIEW`;
3. verify local HEAD == remote HEAD;
4. verify clean publication worktree;
5. stop;
6. do not perform the live OpenClaw upgrade;
7. do not create the live-upgrade successor task before ChatGPT review.
