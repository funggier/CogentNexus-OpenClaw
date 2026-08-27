# CNX-20260827-102 — Open Fresh Dashboard Target and Final Semantic Acceptance

Status: `READY_FOR_HERMES`

Execution mode: `LIVE_OPEN_FRESH_FIREFOX_TARGET_INPUT_DIAGNOSIS_AND_FINAL_SEMANTIC_ACCEPTANCE`

Current authorization: `OPERATOR_DIRECTED_OPEN_FIREFOX_IF_ABSENT_AND_RETRY_FINAL_ACCEPTANCE`

Owner: ChatGPT

Executor: Hermes/Codex after operator continuation

## Goal

Run the final Dashboard semantic acceptance again. The Task-101 observation that no Firefox/OpenClaw window existed is now clarified by the operator: **Firefox simply was not open at that time.** This is not evidence that Firefox window lifecycle itself is broken.

Therefore Task 102 must not stop when no Firefox window is found. If Firefox/OpenClaw is absent, **open Firefox immediately to the non-secret local OpenClaw Dashboard route using the existing authenticated user profile**, wait for the page/window to appear, then rediscover the actual live HWND/PID/session/composer from fresh state before any input.

After a live target is established, test the bounded input methods, report which method works or why each fails, and if one method is proven, continue the original final semantic acceptance in the same task.

## Operator correction to Task 101 interpretation

Task 101 report:

`d06b1397e032749e5b348d5d1054dc1784d67519`

Task 101 semantic send count was `0`; no sentinel/input method was attempted and no Ticket/provider/delivery effect occurred.

The fresh inventory contained no Firefox/OpenClaw window because Firefox was not open. Treat this as an **environment precondition**, not a Firefox lifecycle defect.

Do not reuse stale Task-100 PID/HWND values. After opening Firefox, rediscover the actual live browser window from current OS/UI state.

Historical positive control remains Task 092: one real Dashboard Send created one Ticket, accepted/routed before one `ollama/qwen3.5:9b` inference and one exact visible nonce. Task 093 repaired the later durable staging boundary; Task 096 installed/accepted that source live.

---

# Absolute safety fence

Before the one final semantic Send, only low-impact browser/bootstrap/input experiments are allowed.

Allowed:

- read-only controller/Gateway/SQLite/session/device/log/process/window/UIA/accessibility inspection;
- opening Firefox to the non-secret local OpenClaw Dashboard route using the already-authenticated profile;
- ephemeral PowerShell/Python/.NET/Win32/UIA helpers outside maintained product source;
- UI Automation / Accessibility direct edit of the exact composer;
- deterministic Win32 foreground/input-thread handoff against the freshly correlated target HWND;
- non-sent sentinel drafts and clearing them;
- read-only durable-state polling after the one semantic Send.

Forbidden:

- reading, printing, copying, logging, requesting, exporting or re-entering token/password/credential values;
- typing into any target before exact live window/session/composer correlation;
- sending any sentinel/test draft;
- more than one final semantic Send;
- historical nonce reuse;
- CLI/channel owner substitutes (`openclaw agent`, `chat.inject`, `sessions_send`, channel sends);
- direct provider/Ollama probes;
- synthetic/manual Ticket creation;
- install/install-over/uninstall/reset/cleanup;
- maintained product-source/runtime/config/controller/startup/Supervisor/AGENTS/SQLite mutation;
- provider/model/timeout changes;
- deleting historical sessions merely to normalize the run;
- restart/reboot;
- merge/tag/release/force push.

If any non-sent sentinel is accidentally sent or creates a Ticket/provider effect, stop, correlate it, and do not perform the final semantic Send.

---

# Retry policy

Read-only operations: maximum `3` attempts per operation when useful.

Firefox/dashboard bootstrap: maximum `2` attempts total. Attempt 2 is allowed only after a grace period and fresh process/window/UI evidence prove attempt 1 did not already produce a usable Dashboard target. If the first target appears late, use it and do not open another.

Each low-impact input method family: one normal sentinel attempt plus at most one state-gated retry after fresh evidence proves no conflicting/late effect. Ambiguous partial mutation blocks retry.

The final semantic Send remains exactly one attempt for Task 102. No resend exists.

---

# Phase A — durable/live baseline

Before opening or selecting Firefox:

1. Record coordination execution HEAD.
2. Verify Task 101 report/review are ancestors and publication fence is valid.
3. Verify OpenClaw remains `2026.7.1-2 (0790d9f)`.
4. Verify controller remains MANAGED generation `24`.
5. Verify accepted plugin fingerprint remains:
   `df2600da3ae78e1613793b4a7e5d1ebe61f66f71f0903e1d5d2cd5f0d5f4f4b4`.
6. Verify Gateway/Supervisor healthy and SQLite integrity `ok`.
7. Snapshot Ticket/event/outbox/direct-model-call/assistant-delivery/direct-recovery/workflow counts/tables that exist.
8. Prove no active semantic/provider operation attributable to this task.
9. Enumerate current Dashboard sessions read-only.
10. Prefer existing fresh/empty session `agent:main:dashboard:89992501-1b33-46cf-85f7-eb0c1ef4d311` if it still exists and remains empty/staged. If unsuitable, use another authenticated empty Dashboard session only if exact freshness/identity is proven.

If no safe fresh Dashboard session can be proven:

`BLOCKED_FRESH_SESSION_NOT_ISOLATED`

---

# Phase B — open Firefox if absent, then correlate the live target

## B1. Fresh inventory

Enumerate current `firefox.exe` processes and visible top-level windows.

If a live OpenClaw Dashboard Firefox window already exists and can be correlated to the Phase-A session, use it.

**If no Firefox/OpenClaw window exists, open Firefox immediately. Do not treat absence as a blocker.**

## B2. Open fresh Firefox Dashboard window

Open Firefox to the non-secret local OpenClaw Dashboard/session route using the existing authenticated Firefox profile.

Do not read or re-enter credentials. If the authenticated profile is not usable without credential re-entry, stop with:

`BLOCKED_DASHBOARD_AUTH_REENTRY_REQUIRED`

After opening:

1. wait at least 2 seconds;
2. rediscover current Firefox processes and top-level windows;
3. find the actual `OpenClaw Control — Mozilla Firefox` window (or current equivalent title/class);
4. record fresh HWND/PID/title/class/visibility;
5. obtain fresh UIA/accessibility tree;
6. correlate exact Dashboard session state;
7. locate current `Message Assistant` composer;
8. prove composer empty/staged.

Do not rely on the PID returned by a launch command or on a prior automation `window_id`; they are supporting evidence only.

## B3. Stability proof

Before any sentinel:

1. wait at least 3 seconds after target correlation;
2. enumerate again;
3. prove the same current HWND remains valid/visible;
4. prove UIA/accessibility tree is still obtainable;
5. prove selected Dashboard session remains exact and fresh;
6. prove `Message Assistant` composer remains empty.

Required target token:

`DASHBOARD_LIVE_TARGET_READY`

If the newly opened Firefox window disappears unexpectedly after having been successfully correlated, report the exact evidence and stop with:

`BLOCKED_DASHBOARD_TARGET_WINDOW_DISAPPEARED`

---

# Phase C — input method diagnosis and results

The report must contain a section named exactly:

`Input method diagnosis and results`

For every method attempted, record:

- current HWND/PID/session/composer correlation;
- method-specific capability/probe;
- sentinel attempt count;
- grace/retry decision;
- whether the draft appeared in the exact composer;
- whether clearing succeeded;
- Ticket/provider/durable before/after counts;
- exact failure boundary if failed;
- next tested hypothesis/fix and its outcome.

Use a unique non-secret sentinel per method. Never Send it.

## Method 1 — UI Automation / Accessibility direct edit

Inspect the exact `Message Assistant` element for writable Value/Edit/Text/Legacy or equivalent patterns.

If a supported direct-edit interface exists:

1. set a unique sentinel directly through that exact element without global keyboard input;
2. re-read UIA/accessibility/visual state;
3. prove sentinel exists in the exact composer;
4. clear through the same interface;
5. prove composer empty;
6. prove no Ticket/provider effect.

If unsupported, record the exposed patterns and exact error/return boundary.

## Method 2 — deterministic Win32 foreground/input handoff

If Method 1 cannot write:

1. fresh-rediscover exact target HWND/PID;
2. record current foreground HWND/thread;
3. use bounded ShowWindow/BringWindowToTop/AttachThreadInput/SetForegroundWindow or equivalent as appropriate;
4. **before any global keystroke, require `GetForegroundWindow == exact target HWND`;**
5. focus the exact composer from fresh UIA/location evidence;
6. type one unique non-sent sentinel;
7. verify sentinel in exact composer;
8. clear and prove empty;
9. detach any input-thread attachment even on failure;
10. prove no Ticket/provider effect.

Never type if foreground equality is not proven.

## Method 3 — freshly opened Firefox natural-focus positive control

If Methods 1 and 2 fail, and the current Firefox window can safely be closed/reopened only if doing so does not require credential re-entry or affect semantic state, reproduce the historical positive-control condition with a fresh dedicated Firefox window.

Immediately rediscover its actual HWND, session and composer. Require exact foreground equality before typing. Use one unique non-sent sentinel, verify it, clear it and prove zero semantic/provider effect.

Do not use timing alone as proof.

## Input success

If any method passes, the report must include:

`Known-working Dashboard input method`

and token:

`DASHBOARD_INPUT_METHOD_REPRODUCIBLY_PROVEN`

Composer must be empty and durable baseline unchanged before Phase D.

If all safe methods fail:

`BLOCKED_ALL_BOUNDED_DASHBOARD_INPUT_METHODS`

Do not generate a semantic nonce.

---

# Phase D — one final semantic Send

Only after `DASHBOARD_INPUT_METHOD_REPRODUCIBLY_PROVEN` and a clean composer/durable baseline:

1. re-verify current HWND/PID/session/composer using the proven method;
2. generate brand-new nonce:
   `CNXSEM6-<UTC compact timestamp>-<random uppercase/hex suffix>`;
3. verify nonce absent from current sessions/logs/Tickets;
4. enter exactly:
   `ตอบกลับข้อความนี้เพียงว่า <NEW_NONCE>`
   using the proven input method;
5. re-read exact composer and prove the full prompt before Send;
6. Send exactly once through authenticated Dashboard UI;
7. record send timestamp and non-secret correlation metadata;
8. no resend under any result.

Semantic send count must remain exactly `1` for Task 102.

---

# Phase E — Ticket before provider

Require exactly one new Ticket and durable ordering:

`accepted -> routed -> provider start`

Require one accepted event, one route event, both before correlated provider inference, and no duplicate Ticket/route.

Blockers:

`BLOCKED_TICKET_BEFORE_PROVIDER_ORDERING`

`BLOCKED_DUPLICATE_TICKET_OR_ROUTE`

---

# Phase F — one correlated provider inference

Expected provider/model:

`ollama/qwen3.5:9b`

Require exactly one correlated normal provider call. If actively correlated/running, observe read-only for up to `25 minutes` before declaring failure. Do not resend or change model/timeout.

Blocker:

`BLOCKED_CORRELATED_PROVIDER_INFERENCE`

---

# Phase G — durable payload staging

Require exactly one assistant-delivery payload for the exact session/run/Ticket:

- non-empty final payload;
- normalized text exactly equals nonce;
- durable staging before or at native delivery boundary;
- no competing staged payload;
- no fail-closed regenerated replacement.

Blocker:

`BLOCKED_DURABLE_FINAL_PAYLOAD_STAGING`

---

# Phase H — visible reply and durable completion

Require:

- exactly one visible Dashboard reply equal to nonce;
- exactly one `response_ready`;
- exactly one `delivery_confirmed`;
- non-null `delivery_confirmed_at`;
- Ticket terminal state `completed`;
- no duplicate outbox/delivery/provider/visible nonce;
- no generic resume/promotion regeneration.

Required lifecycle:

`accepted -> routed -> response_ready -> delivery_confirmed -> completed`

Blockers:

`BLOCKED_VISIBLE_NONCE_RESPONSE`

`BLOCKED_RESPONSE_DELIVERY_COMPLETION`

`BLOCKED_DUPLICATE_SEMANTIC_EFFECT`

---

# Phase I — post-completion New Session continuity

Execute only after Ticket `completed`.

Use New Session once with state-gated retry allowed only for this low-impact session-management action.

Prove fresh staged empty state, no stale/unknown-parent/fallback error, no second semantic Send and no additional Ticket/provider effect.

---

# Final health and publication

Verify MANAGED generation `24`, accepted plugin fingerprint unchanged, Gateway/Supervisor healthy, SQLite integrity `ok`, no product/config/install mutation, historical evidence preserved and no secret disclosure.

Required final success token:

`PASS_FINAL_AUTHENTICATED_FRESH_SESSION_SEMANTIC_ACCEPTED`

Publish exactly one report-only commit:

`docs/operations/coordination/reports/CNX-20260827-102-reestablish-dashboard-target-and-final-semantic-acceptance.md`

The report must include:

- `Firefox/bootstrap diagnosis and results`
- `Input method diagnosis and results`
- `Known-working Dashboard input method` if one method passes
- exact semantic result if Phase D is reached
- which method worked, or exact reason none worked
- each tested hypothesis/fix and result.

Only independent review of the report/publication fence may claim final semantic acceptance.