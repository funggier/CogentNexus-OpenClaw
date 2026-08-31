# CNX-20260831-186 — Final Post-Lifecycle Dashboard Semantic / Durable-Delivery Acceptance

Status: `READY_HERMES`

Execution mode: `FINAL_POST_LIFECYCLE_DASHBOARD_SEMANTIC_DURABLE_DELIVERY_HYBRID`

Authorization: `CNX-20260831-186_HERMES_FINAL_POST_LIFECYCLE_DASHBOARD_SEMANTIC_DURABLE_DELIVERY_ACCEPTANCE`

Executor: Hermes/Codex

Coordinator / final reviewer: ChatGPT

UI actor: User

## Objective

Prove that the accepted CogentNexus-OpenClaw candidate still performs the designed semantic path after the completed reset → uninstall → fresh reinstall lifecycle sequence:

`one human Send → one Ticket → one model call → one durable assistant delivery → one logical assistant result in Dashboard`

The acceptance must start from the clean post-Task-185 durable baseline and must not manufacture a second semantic action, recovery action, or retry.

## Accepted starting authority

Task 179 repository repair:

`ACCEPTED_PASS — INTERACTIVE_LIFECYCLE_DELEGATION_REPAIR_ACCEPTED`

Exact frozen candidate:

`f6392da3e4112ce441526d5ef19925c90a872b0b`

Required active facade SHA-256:

`aa747f8f30080ef839a8d2cbf5758f9981a007ca01f41a988576f42edea8682f`

Accepted plugin fingerprint:

`e7d7d6c115040368e35232c83cacec315f6667c92452a5641f7a48a6947baf19`

Task 183:

`ACCEPTED_PASS — QUALIFIED_HARNESS_RESET_FRESH_STATE_REACCEPTED`

Task 184:

`ACCEPTED_PASS — QUALIFIED_HARNESS_UNINSTALL_EXTERNAL_PRESERVATION_ACCEPTED`

Task 185:

`ACCEPTED_PASS — FRESH_REINSTALL_POST_UNINSTALL_ACCEPTED`

Task-185 report publication commit:

`a0bba58c6318c35533342d30ba3e6149cbb8d179`

## Phase A — Fresh authority and live preflight

Before any UI semantic action, Hermes/Codex must independently prove all of the following from current live state.

1. Fresh remote branch HEAD, `ACTIVE.md`, and `STATUS.md` authorize Task 186 and are mutually consistent.
2. Expected Task-186 report is absent before work.
3. No relevant reset/uninstall/install/lifecycle observer or prior Task-186 semantic residue is active.
4. Installed active facade SHA-256 is exactly:
   `aa747f8f30080ef839a8d2cbf5758f9981a007ca01f41a988576f42edea8682f`.
5. Release/plugin state is accepted:
   - release `0.9.3`;
   - OpenClaw `2026.7.1-2 (0790d9f)`;
   - plugin `cogentnexus-openclaw` loaded and enabled;
   - fingerprint `e7d7d6c115040368e35232c83cacec315f6667c92452a5641f7a48a6947baf19`.
6. Ownership is present and legacy namespace is empty.
7. Controller is MANAGED, selected provider is Ollama, provider transition is null.
8. Gateway and Ollama are healthy and ready.
9. Delivery and recovery are READY and pending outbox is `0`.
10. SQLite integrity is `ok`.
11. Exact pre-semantic durable baseline is zero:

| Table | Required pre-action count |
|---|---:|
| `tickets` | 0 |
| `ticket_events` | 0 |
| `ticket_outbox` | 0 |
| `cnx_assistant_delivery` | 0 |
| `cnx_direct_model_call` | 0 |
| `cnx_direct_recovery` | 0 |
| `cnx_sessions` | 0 |

If any authority, process, provenance, health, or durable-baseline condition fails, stop without a Dashboard Send and report the bounded disposition. Do not repair the live system under this task.

## Phase B — Freeze one semantic test identity

After Phase A passes, Hermes/Codex must generate and persist a unique Task-186 nonce before any UI typing, for example:

`CNX186-<UTC timestamp>-<short random suffix>`

Freeze one exact test message containing that nonce. Use a simple semantic request such as:

`<NONCE>. Please include this nonce in your response and give a brief acknowledgement.`

The exact nonce and exact test text must be persisted in evidence before the UI gate is armed.

## Phase C — Human-controlled Dashboard UI gate

This is a hybrid acceptance. UI authority is deliberately split.

### User controls

The user must personally:

1. navigate/open the intended OpenClaw Dashboard session surface;
2. choose New Session if needed;
3. click/focus the intended composer input;
4. after the frozen Task-186 test text is present and visually confirmed, press **Send exactly once**.

### Hermes/Codex may do only this UI-input action

After the user has focused the intended composer input, Hermes may type/paste the already frozen Task-186 test text into that focused field.

Hermes/Codex must **not**:

- press Enter as a send action;
- click Send;
- invoke `chat.inject` or another semantic injection route;
- create a second semantic turn;
- regenerate/retry/re-send the message.

The user's one Send is the only semantic-action root authorized by Task 186.

## Loss-of-control / ambiguity rule

If the UI, executor shell, Dashboard, model response, delivery path, or observer becomes slow or ambiguous after the human Send:

- do not press Send again;
- do not re-enter the test message;
- do not invoke model/recovery/regeneration manually;
- do not restart Gateway/Ollama/CNX merely to obtain a cleaner result;
- inspect the same Ticket/run/session/model/delivery durable state;
- preserve evidence from the one existing semantic action;
- report `UNPROVEN`, `FAIL`, or `BLOCKED` as supported if terminal evidence cannot be obtained.

A timeout or missing UI response never authorizes a second semantic action.

## Phase D — Required correlation evidence

After the one human Send, correlate the frozen nonce through all available durable/runtime/UI identities.

At minimum record:

- user Send count and actor;
- Ticket ID;
- Ticket state and event chain;
- session/run identity;
- provider and model identity;
- direct model-call record;
- assistant-delivery identity/state;
- outbox state;
- recovery count/state;
- durable transcript/session representation;
- Dashboard logical user/assistant node evidence;
- post-action controller/Gateway/Ollama/delivery/recovery health.

Prefer exact IDs, timestamps, hashes, and raw read-only database/query output over narrative inference.

## PASS requirements

### Semantic-root uniqueness

- Human Send count: exactly `1`.
- Hermes/Codex Send count: `0`.
- `chat.inject`/semantic injection count: `0`.
- Retry / second Send count: `0`.

### Ticket / session uniqueness

Starting from the zero baseline, exactly one logical semantic turn must exist:

- `tickets = 1`;
- `cnx_sessions = 1`;
- exactly one Ticket correlates with the frozen nonce;
- exactly one logical session/run correlates with that Ticket and turn.

Do not require a brittle fixed `ticket_events` numeric count. Instead prove a coherent single-Ticket event history with no duplicate logical completion/delivery branch.

### Model-call uniqueness

- `cnx_direct_model_call = 1`;
- exactly one model inference correlates to the Ticket/session/run;
- provider is Ollama;
- expected selected model is `qwen3.5:9b` unless the accepted live config independently proves another explicitly selected model before Send;
- no second model call/retry/regeneration is permitted.

### Durable delivery uniqueness

- `cnx_assistant_delivery = 1`;
- exactly one durable assistant delivery correlates to the same Ticket/session/run;
- `ticket_outbox = 0` after successful drain/delivery;
- no duplicate logical assistant delivery exists.

### Recovery exclusion

- `cnx_direct_recovery = 0`;
- no manufactured provider recovery, direct recovery, regeneration, or manual repair occurred.

### UI semantic result

The Dashboard must show exactly one logical user message for the frozen test and exactly one logical assistant result for that turn.

The assistant result must be non-empty and must correlate to the frozen nonce/request. Visual wrapper/chrome elements are not counted as additional logical messages; duplicated logical transcript nodes are a failure.

The durable assistant transcript/delivery and the visible logical assistant result must represent the same semantic response. Preserve exact evidence sufficient for reviewer correlation.

### Runtime remains healthy

After the semantic turn:

- active facade provenance remains accepted;
- controller remains MANAGED;
- selected provider remains Ollama with no unresolved transition;
- Gateway remains healthy;
- Ollama remains healthy;
- delivery/recovery checks remain healthy/READY;
- pending outbox is `0`;
- SQLite integrity remains `ok`.

## Expected post-action durable cardinalities

The clean Task-185 baseline makes these counts strong acceptance invariants:

| Table | Expected post-action count |
|---|---:|
| `tickets` | 1 |
| `ticket_outbox` | 0 |
| `cnx_assistant_delivery` | 1 |
| `cnx_direct_model_call` | 1 |
| `cnx_direct_recovery` | 0 |
| `cnx_sessions` | 1 |

`ticket_events` must be internally coherent for one Ticket but is not assigned a fixed cardinality.

## Hard fence

```text
human Dashboard Send: maximum 1
Hermes/Codex Send: 0
chat.inject / semantic injection: 0
second Send / semantic retry: 0
manual model retry/regeneration: 0
manual recovery action: 0
reset: 0
uninstall: 0
install/reinstall/install-over: 0
executor-issued lifecycle helper: 0
manual Gateway/Ollama lifecycle action: 0
manual DB/config/transcript/route repair: 0
source/product/test/workflow/dependency edits: 0
release/tag/merge/force push: 0
```

Read-only probes and evidence collection are authorized. Normal internal product processing caused by the one human Send is authorized and is the subject of the acceptance.

## Report contract

Publish exactly one report:

`docs/operations/coordination/reports/CNX-20260831-186-hermes-final-post-lifecycle-dashboard-semantic-durable-delivery-acceptance.md`

The report must contain:

1. disposition;
2. fresh authority/head and preflight;
3. frozen nonce and exact test message;
4. UI actor/action ledger proving user Send `1`, Hermes Send `0`;
5. Ticket/event/session/run correlation;
6. model-call correlation;
7. durable delivery/outbox correlation;
8. Dashboard logical-node evidence;
9. pre/post durable cardinalities;
10. runtime/provenance health after the turn;
11. complete issue/anomaly register;
12. hard-fence audit;
13. Reviewer Verification Packet;
14. publication commit/state.

After report publication, stop for ChatGPT review. Do not perform another semantic action to improve or confirm the result.
