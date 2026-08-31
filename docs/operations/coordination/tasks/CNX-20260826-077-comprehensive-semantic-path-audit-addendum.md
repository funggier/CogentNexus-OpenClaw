# CNX-20260826-077 — Comprehensive Semantic-Path Audit Addendum

Status: `READY_FOR_HERMES`

Applies to active Task: `CNX-20260826-077`

Execution mode extension: `SOURCE_COMPREHENSIVE_SEMANTIC_PATH_DIAGNOSTIC_TDD`

Authorization extension: `COMPREHENSIVE_SEMANTIC_PATH_DIAGNOSIS_AND_PROVEN_BLOCKER_REPAIR_AUTHORIZED`

This addendum extends, but does not replace, `CNX-20260826-077-diagnose-owner-entry-semantic-admission-contract.md`.

## Operator intent

Use the available Hermes/Codex budget to perform one broad, evidence-driven audit of the entire semantic acceptance path before authorizing another live acceptance message. The objective is to avoid fixing only the first visible owner-entry issue and then discovering an adjacent blocker on the next live run.

The audit remains bounded to the CogentNexus/OpenClaw semantic path. Previously accepted installer, ownership, runtime, no-flash and source/live parity areas are not to be redesigned unless a new directly relevant defect is independently proven.

## Absolute live fence remains unchanged

This addendum does **not** authorize another live semantic message.

Do not:

- send any OpenClaw user/semantic message;
- resend or reuse the Task-076 nonce;
- call Ollama directly for a semantic test;
- mutate live Ticket/session/SQLite state;
- install/install-over/uninstall/reset/cleanup;
- change model/provider/plugin/config/AGENTS;
- restart Gateway/Ollama/Supervisor merely for diagnosis;
- reboot;
- merge/tag/release;
- implement in the primary workspace.

Allowed live activity is read-only inspection of exact installed OpenClaw `2026.7.1-2`, the loaded CogentNexus v0.9.3 plugin generation, current configuration, logs, process/provider state and preserved Task-076 evidence.

All source/test work must remain in a fresh isolated worktree.

## Comprehensive audit objective

Trace the complete intended path:

`real owner user surface`
`-> OpenClaw transport/session identity`
`-> plugin hook registration/loading`
`-> before_agent_run metadata`
`-> durable owner eligibility`
`-> Ticket accept/accepted event`
`-> direct routing`
`-> conversational provider start`
`-> Ollama inference or provider failure`
`-> agent_end response_ready`
`-> reply_dispatch/message_sent delivery confirmation`
`-> completed/idempotent terminal state`
`-> recovery behavior when inference or delivery fails`

For every boundary, identify:

1. exact production source entry point;
2. exact runtime metadata in/out;
3. trust/security invariant;
4. durable state expected before crossing the boundary;
5. all early-return/bypass/failure conditions;
6. existing executable coverage;
7. whether Task-076 evidence exercised or bypassed it;
8. whether a defect can block the next live acceptance.

## Audit Area A — exact OpenClaw user-entry surface matrix

Inspect exact local OpenClaw `2026.7.1-2` implementation, not documentation assumptions.

Build a matrix for every relevant supported surface available in this build, including at minimum where present:

- `openclaw agent --session-key ...`;
- Dashboard/WebChat user turn;
- direct control-UI/session send API used by Dashboard/WebChat;
- channel-originated owner turns such as configured Discord owner/direct-message path if applicable;
- scheduled/session workflow turns, explicitly classifying them as internal continuation rather than fresh owner input where appropriate;
- any distinct Gateway RPC path used by interactive user turns.

For each surface record:

- authentication/authorization origin;
- session key before and after normalization;
- `senderIsOwner` derivation and default behavior;
- channel/trigger/surface metadata;
- whether `before_agent_run` is invoked;
- whether the same path reaches normal `agent_end`, `reply_dispatch`, and `message_sent` hooks;
- whether final output is actually user-visible;
- whether current CogentNexus policy should admit or reject it.

Do not infer owner trust merely because a command can target `agent:main:main`.

## Audit Area B — loaded plugin and hook-registration reality

Prove the runtime is loading the expected canonical CogentNexus plugin generation and that the relevant hooks are registered in the exact installed package.

Read-only verify:

- canonical active plugin generation path/version;
- package/entrypoint identity;
- configured enabled state;
- source/hash relationship where available;
- actual registration of `before_agent_run`, `agent_end`, `reply_dispatch`, `message_sent`, and any recovery/session hooks relied upon by semantic acceptance;
- no stale generation or alternate plugin copy is winning module resolution;
- no hook is conditional on a trigger/channel/config field absent from the intended owner surface.

If source/live plugin code differs from the accepted source in a way not already covered by Task 075, report it as a blocker; do not silently repair live state.

## Audit Area C — every Ticket-admission bypass and early return

Trace the production `before_agent_run` handler completely from hook entry to `TicketStore.accept()`.

Enumerate every condition that can cause a prompt to reach inference without a Ticket, including but not limited to:

- missing/unsupported session key;
- subagent/internal continuation detection;
- `senderIsOwner` handling;
- dashboard fallback logic;
- `ticketFirst`, `preInferenceAdmission`, enforced-mode/config gates;
- prompt normalization/empty prompt/internal marker rules;
- run/request identity availability;
- store/open/database failures;
- deduplication paths;
- any exception handling that fails open;
- hook return semantics that OpenClaw interprets differently than expected.

For each path classify:

- intended security behavior;
- intended internal-continuation behavior;
- potentially unsafe fail-open behavior;
- next-live-test relevance.

The invariant to protect is: **every eligible real owner turn must durably commit its Ticket before normal inference can proceed**.

## Audit Area D — production-facing owner/Ticket integration matrix

Strengthen executable tests beyond `durableAdmissionEligible()` unit tests.

Use exact OpenClaw-2026.7.1-2-compatible hook metadata fixtures or the closest production integration boundary available.

At minimum prove with isolated temp state:

1. legitimate Dashboard/WebChat owner metadata creates exactly one Ticket before provider continuation;
2. any other legitimate owner surface identified in Area A does the same;
3. `openclaw agent` metadata from Task 076 is either correctly rejected or, only if proven owner-authenticated, correctly admitted;
4. subagent metadata creates no Ticket;
5. untrusted channel/CLI metadata creates no Ticket;
6. internal scheduled continuation metadata does not create an unintended second owner Ticket;
7. provider continuation cannot be invoked by the harness until Ticket commit and `accepted` event are observable;
8. repeated hook invocation for the same production request/run identity converges without duplicate Ticket creation.

If exact OpenClaw metadata shape is uncertain, derive it from installed source before writing fixtures.

## Audit Area E — direct-lane lifecycle after admission

Trace and test the simple direct lane beyond admission so the next live attempt does not stop at a later untested boundary.

Prove in source/integration tests where possible:

- `accepted -> routed(workflowEligible=false)` ordering;
- run/session/Ticket correlation survives through agent completion;
- successful `agent_end` records `response_ready` exactly once;
- direct result metadata is durable;
- `reply_dispatch`/`message_sent` correlation targets the same Ticket;
- successful final delivery records `delivery_confirmed` and `completed` exactly once;
- direct lane does not require an outbox row when confirmed delivery is intentionally direct;
- duplicate hook callbacks do not duplicate delivery/completion;
- a different session/run cannot accidentally complete another Ticket.

Use stubs/fakes only at provider/transport boundaries; do not bypass the production TicketStore/direct-delivery logic being accepted.

## Audit Area F — provider timeout and timeout hierarchy

Investigate the Task-076 ~245.7 s provider-stage timeout more deeply, read-only.

Trace exact timeout layers and effective values in OpenClaw 2026.7.1-2 and current config:

- CLI/RPC timeout;
- embedded agent run timeout;
- model idle timeout;
- provider request timeout;
- Ollama request/model-load behavior;
- CogentNexus timeout/recovery settings if they interact with direct inference;
- any heartbeat/token-stream condition that resets or fails to reset idle timeout.

Use Task-076 correlated logs and existing Ollama/OpenClaw logs to distinguish:

- model load delay;
- inference producing no tokens;
- resource contention;
- OpenClaw timeout policy;
- provider connection stall;
- Hermes/Codex activity unrelated to product traffic;
- insufficient evidence.

Do not change timeout/model/provider values in Task 077.

Determine whether the provider timeout is likely to block the next semantic attempt even after entry-path correction. If so, treat it as an adjacent semantic acceptance blocker requiring a source/config design recommendation, but no live config mutation is authorized here.

## Audit Area G — failure/recovery/idempotency semantics

Inspect what should happen if a Ticket **has** been admitted and then the provider times out, the agent fails, or final delivery fails.

Prove source/tests for the relevant direct-lane behavior:

- admitted Ticket never disappears on provider failure;
- terminal/interrupted state is explicit and recoverable according to current product contract;
- auto-resume/recovery does not create a second Ticket for the original owner turn;
- recovery/internal continuation messages are not re-admitted as new owner Tickets;
- response-ready without confirmed delivery remains distinguishable from completed;
- delivery retry/convergence cannot emit duplicate final user-visible effects;
- no fail-open path marks completed without evidence.

Flag any proven defect that would make the next real semantic acceptance unsafe or ambiguous.

## Audit Area H — semantic security invariants

Perform a focused negative-security review around the exact admission change surface.

Preserve at least:

- subagents cannot impersonate the owner;
- arbitrary CLI invocation cannot become trusted merely by selecting an owner-looking session key;
- arbitrary channel senders cannot become owner via session-key pattern alone;
- Dashboard fallback is limited to the exact authenticated control-UI invariant proven from OpenClaw source;
- scheduled/internal continuation turns cannot create unintended new owner Tickets;
- no user-controlled metadata field alone grants owner admission;
- deduplication keys cannot collide across unrelated sessions/runs in a way that loses intent.

Any source repair must remain least privilege.

## Audit Area I — adjacent-blocker sweep and repair authority

The executor is authorized to repair **multiple independently proven semantic-path blockers in this Task 077** when doing so reduces the chance of another avoidable live-test failure, but only under all of these constraints:

1. the defect is within owner entry, Ticket-before-inference, direct-lane completion/delivery, semantic idempotency/recovery, or a source-level timeout interaction directly affecting the final semantic path;
2. root cause is evidenced before editing;
3. each distinct defect receives a focused RED reproduction before its fix;
4. each fix is the smallest production change that closes that defect;
5. each focused test goes GREEN;
6. full regression remains green;
7. no unrelated refactor or installer/runtime redesign is bundled;
8. no live mutation is used to validate the source fix in Task 077.

If a finding requires a live config/model/timeout change, do not perform it here. Document the exact successor gate instead.

## Required comprehensive finding table

The Task-077 report must include a table with at least these columns:

| Boundary | Exact production path | Evidence | Status | Severity | Next action |
| --- | --- | --- | --- | --- | --- |

Cover all areas A-H.

Use severity:

- `P0` — would violate Ticket-first/security/durable intent invariant;
- `P1` — likely to block or invalidate final semantic acceptance;
- `P2` — real issue but not a blocker for the next semantic acceptance;
- `INFO` — expected behavior/documentation finding.

Every P0/P1 must be either repaired and tested in Task 077 or explicitly carried into a successor task with a hard reason why it cannot be safely repaired source-only.

## Verification expansion

In addition to all verification already required by the base Task 077, run the widest relevant deterministic suite available for the semantic path:

- full plugin validate/tests under both required npm/Node compatibility paths;
- all TicketStore tests;
- all plugin hook/admission tests;
- direct-delivery and outbox tests;
- session/recovery/auto-resume tests;
- workflow/internal-continuation negative admission tests;
- full Python `pytest tests/ -q` with zero failures;
- repository baseline consistency checks;
- final source diff review for unrelated changes;
- final worktree clean after commits.

Where exact OpenClaw behavior is covered by local package source rather than vendored tests, cite exact local file/function/version evidence in the report.

## Publication

The existing Task-077 publication fence remains authoritative:

- implementation/tests commit(s) first;
- report-only commit last;
- report path remains `docs/operations/coordination/reports/CNX-20260826-077-diagnose-owner-entry-semantic-admission-contract.md`;
- report must explicitly state that this comprehensive addendum was executed.

## Successor objective

Do not authorize the next live semantic message merely because the first owner-entry finding is understood.

A successor live semantic task should be opened only after independent review confirms:

1. an exact supported real owner surface is proven;
2. its production hook metadata is executable-tested;
3. Ticket commit-before-provider continuation is proven in source tests;
4. direct response/delivery terminal path is covered sufficiently to make a live run meaningful;
5. no unresolved P0/P1 semantic blocker remains, including provider-timeout risk that would make the next run predictably fail;
6. if source changed, supported install-over/source-live parity is completed before the next semantic message.
