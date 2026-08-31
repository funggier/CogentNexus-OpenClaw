# CNX-20260829-137 — Final Dashboard Durable-Delivery Re-Acceptance

- Status: `READY_FOR_HERMES`
- Execution mode: `LIVE_WINDOWS_DASHBOARD_DURABLE_DELIVERY_REACCEPTANCE_ONLY`
- Owner / independent reviewer: ChatGPT
- Executor: Hermes/Codex after operator continuation
- Date: 2026-08-29 ICT
- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`

## Purpose

Perform one new clean real-OpenClaw-Dashboard durable-delivery acceptance after Task 136 was independently classified as an acceptance FAIL whose causal interpretation was contaminated by an accidental Hermes interruption, a composer duplication anomaly, and an observation window shorter than demonstrated local-model latency.

This task does **not** repair or modify production source. It tests the currently accepted runtime again under a corrected acceptance protocol.

Task 136 remains immutable historical evidence. Its Send ledger is consumed and its failed Ticket must not be deleted, reset, normalized, retried, or reused.

## Accepted candidate and identity

Accepted source candidate:

`1424d6fbee2c458c8c30440616783d2fa1bc1201`

Accepted payload/plugin fingerprint:

`3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`

Authoritative installed launcher:

`C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd`

Authoritative root:

`C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw`

Task-136 independent review:

`docs/operations/coordination/reviews/CNX-20260829-136-final-dashboard-durable-delivery-acceptance-review.md`

## Fresh Task-137 semantic ledger

This task grants a new ledger, distinct from Task 136:

- fresh nonce: maximum `1`;
- exact Dashboard message composition: `1`;
- Dashboard submission activation: maximum `1 / 1`;
- semantic resend after activation: `0` allowed;
- alternate CLI/Gateway/API/database semantic injection: `0` allowed;
- manual Ticket/outbox/delivery retry or acknowledgement: `0` allowed.

Once the Task-137 Dashboard submission activation occurs, this Task-137 authorization is consumed regardless of UI or durable outcome.

The historical Task-136 nonce and Ticket must never be resent or reused.

## Critical executor-interruption rule

The operator must allow Hermes/Codex to continue uninterrupted through the Task-137 report commit once Send has occurred.

If Hermes/Codex is externally stopped, canceled, killed, or otherwise interrupted **before Send**, record `BLOCKED_BEFORE_SEND`; the Task-137 Send ledger remains unconsumed and no semantic side effect has occurred.

If an external executor interruption occurs **after Send**, immediately classify the run `INVALIDATED_AFTER_SEND`, preserve durable evidence read-only, and do not attribute the resulting runtime state to a product defect from this run alone. The Task-137 Send ledger remains consumed and no resend is permitted. A further attempt would require a new task.

Do not stop Hermes merely because the local model is slow or the Dashboard appears idle.

## Phase 0 — fresh authority and delta baseline

Before composing the new message:

1. Fresh-fetch branch HEAD, `ACTIVE.md`, and `STATUS.md`; confirm Task 137 remains authoritative and unsuperseded.
2. Confirm no source/runtime/plugin deployment change since accepted candidate. Do not install or install-over.
3. Freshly read/hash/parse the explicit installed launcher and require the authoritative `.cogentnexus-openclaw` root.
4. Capture an already-safe live read-only baseline through the installed launcher and authoritative SQLite URI `mode=ro`.
5. Preserve historical Task-136 rows. Do not require an empty historical database.

Required current health:

- mode `managed`;
- desired Gateway/provider `running`;
- selected provider `ollama`;
- recovery exact `READY`;
- delivery exact `READY`;
- no active provider incident/circuit/unsafe transition;
- exact installed fingerprint `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`;
- OpenClaw `2026.7.1-2`;
- exactly one current CogentNexus-OpenClaw plugin loaded/enabled;
- Gateway healthy;
- Ollama healthy; record version and full model inventory;
- authoritative SQLite exists and `PRAGMA integrity_check` is exactly `ok` via URI `mode=ro`;
- `pendingOutbox=0`;
- `nonterminalTickets=0`;
- no active direct-model call;
- no active workflow/direct-recovery/outbound-send operation;
- Task-136 historical Ticket remains terminal `failed` and no Task-136 retry/outbox/delivery mutation has appeared.

Capture complete pre-send counts and stable IDs for relevant Ticket/event/model-call/outbox/assistant-delivery/outbound-send/recovery tables. Those counts form the **Task-137 delta baseline**.

If there is unexplained new durable activity, pending/nonterminal residue, unsafe state, source drift, or an active semantic execution, stop `BLOCKED_BEFORE_SEND`. Do not clean or normalize.

## Phase 1 — fresh nonce and exact composer content

Generate one new non-secret nonce only after the safe delta baseline is captured, for example:

`CNX-DDA2-<UTC timestamp>-<random suffix>`

Verify read-only that it does not exist anywhere in historical Ticket/event/result/delivery records.

Use exactly this conceptual message with the fresh nonce:

`CogentNexus final durable-delivery re-acceptance <NONCE>. Reply with exactly: ACK <NONCE>`

Before typing/composing:

- inspect the Dashboard composer;
- clear any stale draft text locally in the composer if needed;
- enter the acceptance text exactly once;
- immediately before Send, verify the composer contains exactly one copy of the intended message, one nonce occurrence in the request prefix and one nonce occurrence in the requested ACK phrase, with no duplicated full message or accidental appended text;
- capture enough pre-send evidence to establish the exact composer contents without publishing unrelated private conversation content.

If exact composer contents cannot be verified, stop `BLOCKED_BEFORE_SEND`. Do not Send.

## Phase 2 — real Dashboard, exactly one Send

Use the real OpenClaw Dashboard conversation UI only.

Confirm the Dashboard is connected to the accepted runtime and identify the intended normal/default Dashboard session.

Perform exactly **one** deliberate submission activation, preferably one click on the Dashboard Send control.

Do not press Enter as an additional submission gesture. Do not click Send twice.

Record the activation timestamp immediately and mark Task-137 Send ledger `1 / 1 consumed`.

After activation:

- never resend;
- never edit and re-submit;
- never inject the same semantics by CLI/Gateway/API/database/test harness;
- UI ambiguity is resolved only by read-only durable observation.

## Phase 3 — realistic bounded observation

Task 136 demonstrated a direct local-model call of about 14 minutes 10 seconds, and the operator has observed `qwen3.5:9b` first-response latency around 20 minutes when used directly through Ollama.

Therefore ordinary silence, spinner state, or absence of an assistant bubble during early local inference is **not failure evidence**.

After Send, allow read-only observation for up to **45 minutes from the submission activation**, unless the new Ticket reaches an unambiguous durable terminal outcome earlier.

During this interval:

- do not stop Hermes because of slowness;
- do not Send again;
- do not refresh into a second semantic submission;
- do not edit/re-submit;
- do not manually dispatch, retry, ack, clean, normalize, restart, recover, or kill processes;
- do not write SQLite.

If the runtime itself reaches durable terminal `failed` earlier while the executor remained uninterrupted and composer/Semantic-Send evidence is clean, preserve that first failure immediately; no need to wait the full 45 minutes before classifying FAIL.

If the Ticket remains genuinely nonterminal at 45 minutes with no runtime-owned terminal failure, classify `FAIL_TIMEOUT_OR_NONCONVERGENCE`, preserve read-only evidence, and stop. No resend.

## Phase 4 — Ticket-first and single-execution proof

For the fresh nonce prove exactly one new Ticket was created by comparing against the Task-137 delta baseline.

Capture:

- Ticket ID and durable creation timestamp;
- complete event/status sequence with stable ordering IDs where available;
- exact model-call/execution identity;
- workflow/direct-recovery association only if actually present;
- zero duplicate Ticket for the nonce;
- zero duplicate concurrent execution for the Ticket.

PASS requires affirmative durable evidence that Ticket commit/event ordering precedes inference/model execution.

## Phase 5 — result / validator proof

For full PASS require:

- one coherent execution chain;
- successful terminal Ticket state (`completed` or reviewed equivalent);
- durable result/output for the exact Ticket;
- validators/guards associated with terminal completion pass;
- result identity/hash/metadata coherent where available;
- assistant semantic result corresponds to exactly `ACK <NONCE>` or is otherwise classified as a semantic mismatch.

A semantic mismatch is a FAIL for this final acceptance even if transport delivered once; do not resend.

## Phase 6 — durable delivery and exactly-once proof

Track the new result through the actual reviewed delivery path.

Require:

- exactly one logical outbox/delivery chain for the new Ticket/result;
- terminal delivered/acknowledged state or reviewed equivalent;
- `pendingOutbox=0` after terminal delivery;
- attempt and acknowledgement metadata where available;
- no duplicate logical outbox/delivery rows for the same result;
- no duplicate `cnx_assistant_delivery` / `cnx_outbound_send` external-send identity where applicable;
- no duplicate external semantic assistant delivery;
- visible Dashboard assistant response corresponds to the durable delivered result.

Use the Task-137 pre-send counts/IDs and post-send delta. Do not require historical Task-136 rows to disappear.

## Phase 7 — final read-only snapshot

After successful terminal delivery or first definitive failure, capture through the same installed launcher/root:

- managed/Ollama state;
- desired Gateway/provider running;
- recovery verdict/checks/incident/circuit;
- delivery verdict/checks;
- Gateway/Ollama health;
- Ollama version and model inventory unchanged from Task-137 preflight;
- exact installed plugin/fingerprint unchanged;
- SQLite `PRAGMA integrity_check=ok`;
- Task-137 Ticket terminal state;
- `nonterminalTickets=0` expected after a terminal result;
- `pendingOutbox=0` expected after successful delivery;
- no unresolved duplicate workflow/direct-recovery/outbound-send state;
- Task-136 historical failed Ticket still preserved and unmodified except for any implementation-owned read-only-observable metadata that is independently explained;
- no lifecycle/recovery/config mutation.

No cleanup or normalization is authorized even after failure.

## PASS criteria

Task 137 passes only if all of the following are established:

- executor remained uninterrupted after Send;
- pre-send composer contained exactly one intended message;
- exactly one Task-137 Send activation;
- exactly one new Ticket for the fresh nonce;
- Ticket committed before inference;
- one coherent execution chain;
- successful terminal result with validators/guards coherent;
- requested ACK semantics coherent;
- exactly one logical durable assistant delivery, terminal acknowledged/delivered;
- no duplicate semantic delivery/external side effect;
- no pending/nonterminal residue after success;
- final runtime/recovery/delivery/SQLite/model state coherent and unchanged except for expected new historical delivery records.

## Failure / invalidation discipline

After Send, the Task-137 ledger is consumed. There is never a resend under this task.

Classify distinctly:

- `FAIL_PRODUCT_OR_RUNTIME` only when the executor remained uninterrupted and clean evidence demonstrates runtime/product failure;
- `FAIL_SEMANTIC_MISMATCH` when delivery succeeds but requested ACK semantics do not;
- `FAIL_TIMEOUT_OR_NONCONVERGENCE` when the clean run remains nonterminal for the full 45-minute bound;
- `INVALIDATED_AFTER_SEND` when Hermes/Codex is externally interrupted after Send or another external execution contamination occurs;
- `BLOCKED_BEFORE_SEND` for unsafe/ambiguous preflight or composer/session conditions before activation.

Never convert an invalidated run into product-root-cause proof.

## Required report

Publish exactly:

`docs/operations/coordination/reports/CNX-20260829-137-final-dashboard-durable-delivery-reacceptance.md`

Include:

- coordination start HEAD;
- candidate/fingerprint/launcher/root identity;
- Task-136 historical baseline identity and preserved failed Ticket;
- fresh Task-137 delta baseline counts and IDs;
- fresh nonce absence proof;
- exact composer contents and pre-send single-copy verification;
- real Dashboard/session identity sufficient for acceptance without unrelated private content;
- one Send activation timestamp and ledger `1 / 1`;
- explicit executor-interruption status;
- complete Ticket/event/model-call/workflow/result/validator timeline;
- Ticket-before-inference proof;
- durable outbox/delivery/ack exactly-once proof using pre/post deltas;
- local-model timing including admission, model start/end, response-ready, delivery and terminal timestamps;
- final visible Dashboard response classification;
- final runtime/provider/recovery/delivery/SQLite/model snapshot;
- exact PASS/FAIL/BLOCKED/INVALIDATED classification and first evidence supporting it;
- explicit no resend, manual retry, cleanup, normalization, lifecycle/recovery or source mutation.

Then STOP for independent ChatGPT review.

Do not merge, tag, publish a GitHub Release, or automatically open release/finalization work.

## Hard fence

Except for the one explicitly authorized Task-137 Dashboard semantic submission, forbidden actions are:

- any second Send/resend;
- alternate semantic injection through CLI/Gateway/API/database/test harness;
- source/runtime/plugin edit;
- install/install-over/reset/uninstall/reinstall;
- start/stop/restart/enable/disable;
- recovery suite/crash injection;
- provider/model/OpenClaw/config mutation;
- manual Ticket/workflow/outbox/ack/delivery mutation;
- SQLite write/migration/cleanup;
- process kill;
- scheduled-task/service mutation;
- normalization;
- reboot;
- credential/secret access;
- unrelated external side effects;
- merge/tag/release;
- force push.
