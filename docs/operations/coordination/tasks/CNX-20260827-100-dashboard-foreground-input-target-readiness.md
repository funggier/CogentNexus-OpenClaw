# CNX-20260827-100 — Known-Working Dashboard Input and Final Semantic Acceptance

Status: `READY_FOR_HERMES`

Execution mode: `LIVE_KNOWN_WORKING_DASHBOARD_INPUT_AND_FINAL_SEMANTIC_ACCEPTANCE`

Current authorization: `OPERATOR_APPROVED_KNOWN_WORKING_INPUT_REPRODUCTION_AND_FINAL_SEMANTIC_CONTINUATION`

Owner: ChatGPT

Executor: Hermes/Codex after operator continuation

## Goal

Use the Dashboard input method that the operator/Codex has now demonstrated can type into the real OpenClaw composer, document that known-working method precisely, and then continue the previously authorized final semantic acceptance in the same task instead of stopping at readiness-only.

The final semantic proof remains:

`fresh authenticated Dashboard session -> exactly one Ticket accepted/routed before provider -> exactly one correlated Ollama inference -> durable final payload staged before native delivery -> exact visible nonce once -> response_ready -> delivery_confirmed -> completed`

After successful completion only, prove another New Session transition with zero additional semantic/provider effect.

## New operator evidence and instruction

The operator reported that current testing has reached the point where Codex can type into the actual OpenClaw Dashboard composer and now knows the working interaction method.

Task 100 must therefore:

1. reuse/reproduce the method that just worked instead of rediscovering a stricter HWND path when that is unnecessary;
2. verify that the method targets the exact intended Dashboard session/composer;
3. record the method in the report under a required section named exactly:

`Known-working Dashboard input method`

4. after input-method proof passes and the composer is clean/empty, continue the final semantic acceptance immediately in this same task.

Do not publish credential/token values or other secrets as part of the method documentation.

## Accepted predecessor state

Task 096 accepted live deployment:

- exact installed source `32212a4331e1f32b5a130bd30d271d4cbc56f6c1`;
- exact installed plugin fingerprint `df2600da3ae78e1613793b4a7e5d1ebe61f66f71f0903e1d5d2cd5f0d5f4f4b4`;
- MANAGED generation `24`;
- healthy startup/Supervisor/Gateway/SQLite/Ollama;
- Task-092 retired evidence preserved;
- `NO_FLASH_MULTI_TICK_REPROVEN`.

Task 098 accepted authenticated fresh-session readiness.

Task 099 report:

`d5fde8d5f1e5968a1ae5ce11f4017a15d9884dac`

Task 099 independent disposition:

`ACCEPT_BLOCKER_DASHBOARD_WINDOW_FOREGROUND_TARGETING_BEFORE_SEND`

Exact target established by Task 099:

`agent:main:dashboard:89992501-1b33-46cf-85f7-eb0c1ef4d311`

Task 099 semantic send count was `0`; its nonce is retired and must never be reused.

Task 092 remains the historical positive control showing the real authenticated Dashboard send path can execute through Ticket admission, one Ollama call and one exact visible reply. It failed later at durable delivery completion. Task 093 repaired that staging boundary and Task 096 installed the repaired source live.

---

# Retry policy v1

Read-only operations may use up to `3` attempts total.

Low-impact UI operations before Send — focus, click, activation, composer targeting, non-sent typing and clearing — may use at most `2` attempts total, and attempt 2 requires a bounded grace interval plus fresh UI/session/state evidence proving attempt 1 did not already take effect in a conflicting way.

If attempt 1 takes effect late, count it as success and do not re-issue.

Ambiguous or partial UI/session mutation is not retryable.

The semantic Send is **single-attempt only**:

- one new nonce;
- one exact user send;
- no resend;
- no second semantic prompt;
- no CLI/channel/provider substitute.

---

# Absolute fence

Allowed:

- read-only controller/Gateway/SQLite/session/device/log/window/process inspection;
- use of the already-authenticated Firefox/OpenClaw Dashboard;
- reproducing the currently known-working UI input method;
- typing a non-sent local sentinel into the intended composer solely to prove input targeting;
- clearing that sentinel before semantic nonce generation;
- exactly one final semantic user message after all pre-send gates pass;
- normal runtime effects of that one semantic turn;
- after successful durable completion only, one low-impact New Session transition plus at most one state-gated retry if eligible.

Forbidden:

- reuse of Task-099 nonce;
- more than one semantic send;
- resend after timeout/failure/ambiguity;
- `chat.inject`, `openclaw agent`, `sessions_send`, channel sends or CLI owner substitutes;
- direct Ollama/provider probes;
- synthetic/manual Ticket creation;
- install/install-over/uninstall/reset/cleanup;
- plugin-generation/controller/startup/Supervisor/AGENTS/ownership/runtime/config mutation;
- SQLite edits or prior-evidence repair;
- session deletion/normalization merely to make the test pass;
- provider/model/timeout changes;
- restart/reboot;
- merge/tag/release/force push;
- reading, copying, printing, logging, requesting or re-entering token/password/credential values.

---

# Phase A — fresh baseline and target identity

Before semantic nonce generation:

1. record coordination execution HEAD;
2. verify Task 099 report/review are ancestors and publication fence remains valid;
3. verify OpenClaw build remains `2026.7.1-2 (0790d9f)`;
4. verify controller remains MANAGED generation 24;
5. verify exactly one canonical loaded/enabled CogentNexus plugin with accepted fingerprint;
6. verify Gateway healthy and SQLite integrity `ok`;
7. snapshot exact pre-test counts for Tickets, Ticket events, outbox, direct-run/delivery/workflow tables that exist;
8. prove no active semantic/provider operation;
9. re-snapshot the exact selected Dashboard session ID/key;
10. prefer the Task-099 target `agent:main:dashboard:89992501-1b33-46cf-85f7-eb0c1ef4d311` if it remains authenticated, fresh and appropriate;
11. prove the target is distinct from Main Session and Task-092/Task-076 historical semantic sessions;
12. inspect the composer before changing it.

If a non-sent local draft exists because of the operator/Codex input test, do not publish its text. Record only that a non-sent draft was present, prove it produced no Ticket/provider effect, clear it, and verify the composer is empty before continuing.

If any test text was actually sent, or any new Ticket/provider effect already exists, stop and correlate that state instead of creating another semantic send.

Blocker:

`BLOCKED_TARGET_SESSION_OR_BASELINE_CHANGED`

---

# Phase B — reproduce and document the known-working input method

Use the exact interaction sequence that Codex has just established works on this machine.

The report must include a section named exactly:

## Known-working Dashboard input method

That section must document, without secrets:

- how the correct OpenClaw Dashboard window/tab/session is identified;
- which UI interaction is used to reach/focus the real composer;
- whether foreground activation, click location/control selection, browser focus or another step is required;
- the ordering of those actions;
- any required wait/grace interval;
- which low-impact retry, if any, was required and the evidence that made it eligible;
- how Codex verifies that keystrokes entered the intended composer rather than another Firefox window/control;
- how Codex verifies that no Send occurred during input-method proof;
- how to leave the composer clean/empty before the real semantic send;
- any observed condition that would make the method unsafe or ambiguous and require stopping.

Do not invent a method from old instructions if Codex's currently working method differs. Report what actually works now.

### Non-sent sentinel proof

To prove end-to-end composer targeting, Task 100 may type this local sentinel into the intended composer:

`CNXINPUT-READY`

Rules:

1. do not press Enter if Enter can Send;
2. do not click Send;
3. verify the exact sentinel appears in the intended composer;
4. verify Ticket/event/outbox/provider counts remain unchanged;
5. clear the sentinel completely;
6. verify the composer is empty;
7. verify no semantic/provider effect occurred.

If the current known-working method can be proven equivalently without the sentinel, that is acceptable, but the report must explain the evidence.

Required input-readiness token:

`DASHBOARD_KNOWN_WORKING_INPUT_METHOD_PROVEN`

If input targeting remains ambiguous, stop before nonce generation:

`BLOCKED_KNOWN_WORKING_INPUT_METHOD_NOT_REPRODUCIBLE`

---

# Phase C — final pre-send gate and nonce

Only after Phase A and B pass:

1. re-verify exact target session identity;
2. verify composer is empty;
3. verify authenticated Dashboard owner/control state remains active;
4. verify pre-semantic Ticket/outbox/provider counts still equal the baseline;
5. generate one fresh nonce:

`CNXSEM4-<UTC compact timestamp>-<random uppercase/hex suffix>`

6. prove the nonce does not already exist in current durable/session evidence.

The nonce must be generated only after known-working input proof is complete.

---

# Phase D — exactly one semantic send

Using the same known-working composer-input method, send exactly:

`ตอบกลับข้อความนี้เพียงว่า <NEW_NONCE>`

Semantic send count for Task 100 must be exactly `1`.

No resend exists under any outcome.

Immediately record non-secret correlation metadata including exact target session, send time and any request/run identifiers available.

---

# Phase E — fresh-session isolation and Ticket-before-provider ordering

Require:

1. exact sent session equals the selected Phase-C Dashboard target;
2. the nonce prompt is the first semantic user message for the accepted fresh target, apart from any non-sent local draft/sentinel which must have been cleared and never emitted;
3. no Main/old-session fallback or stale/unknown-parent substitution occurred;
4. exactly one new durable Ticket exists for the one semantic message;
5. exactly one accepted event and one route event exist;
6. accepted/routed durable timestamps precede the correlated provider inference;
7. no duplicate Ticket or route exists.

Blockers:

`BLOCKED_FRESH_SESSION_NOT_ISOLATED`

`BLOCKED_TICKET_BEFORE_PROVIDER_ORDERING`

`BLOCKED_DUPLICATE_TICKET_OR_ROUTE`

---

# Phase F — correlated provider inference

Prove exactly one normal provider inference correlated to the exact session/run/Ticket.

Expected provider/model:

`ollama/qwen3.5:9b`

No direct readiness probe is allowed.

If provider fails or times out, capture durable state and stop without resend or model/timeout mutation.

Blocker:

`BLOCKED_CORRELATED_PROVIDER_INFERENCE`

---

# Phase G — durable payload staging before native delivery

This is the live proof of the Task-093 repair.

Require:

1. exactly one durable assistant-delivery payload bound to the exact owner/session/run;
2. staged final text normalizes exactly to the nonce and is non-empty;
3. staging occurs before or at the repaired native delivery boundary;
4. no competing staged payload exists;
5. no fail-closed replacement/recovery payload supersedes the expected final response.

A visible nonce without durable staging fails.

Blocker:

`BLOCKED_DURABLE_FINAL_PAYLOAD_STAGING`

---

# Phase H — visible response and durable completion

Require visible Dashboard assistant reply equal to the nonce exactly, allowing whitespace normalization only.

Require exact durable lifecycle:

`accepted -> routed -> response_ready -> delivery_confirmed -> completed`

Prove:

- exactly one `response_ready`;
- exactly one visible nonce;
- exactly one `delivery_confirmed`;
- Ticket terminal state `completed`;
- no duplicate outbox delivery;
- no generic `cogent-resume-*` duplicate promotion;
- no workflow/durable duplicate promotion;
- no second provider inference;
- no duplicate visible response.

Blockers:

`BLOCKED_VISIBLE_NONCE_RESPONSE`

`BLOCKED_RESPONSE_DELIVERY_COMPLETION`

`BLOCKED_DUPLICATE_SEMANTIC_EFFECT`

---

# Phase I — post-completion New Session continuity

Execute only after the exact Ticket is durably `completed`.

Use the actual Dashboard New Session action with zero semantic content.

State-gated retry policy v1 applies to this low-impact session-management operation only:

- attempt 1 once;
- if result is unverifiable, wait at least 5 seconds and re-read session/UI state;
- if effect appeared, do not retry;
- attempt 2 only if fresh evidence proves attempt 1 had no effect;
- no third attempt.

Require entry to a fresh staged state without stale/unknown-parent failure, fallback, new Ticket or additional provider inference.

Blocker:

`BLOCKED_POST_COMPLETION_NEW_SESSION_CONTINUITY`

---

# Final health and preservation

Verify:

- controller remains MANAGED;
- accepted plugin fingerprint unchanged;
- Gateway healthy;
- SQLite integrity `ok`;
- Task-092 and Task-099 historical evidence not rewritten;
- exact Task-100 accounting is one semantic send, one Ticket, one route, one provider inference, one staged final payload, one visible final reply, one delivery confirmation and one completed Ticket;
- no credential value exposed.

---

# Publication fence

No product-source commit is expected.

Publish exactly one report-only commit:

`docs/operations/coordination/reports/CNX-20260827-100-dashboard-foreground-input-target-readiness.md`

The report must include the required section:

`Known-working Dashboard input method`

Required success token:

`PASS_FINAL_AUTHENTICATED_FRESH_SESSION_SEMANTIC_ACCEPTED`

Additional required method token:

`DASHBOARD_KNOWN_WORKING_INPUT_METHOD_PROVEN`

Other blocker tokens are those defined above plus:

`BLOCKED_UNEXPECTED_SEMANTIC_OR_PROVIDER_EFFECT`

`BLOCKED_LIVE_HEALTH_REGRESSION`

`BLOCKED_EVIDENCE_PUBLICATION_UNSAFE`

## Final gate

Only independent review of the Task-100 report and publication fence may close final OpenClaw semantic acceptance. A visible correct reply alone is insufficient; durable staging, delivery confirmation and terminal completion are mandatory.
