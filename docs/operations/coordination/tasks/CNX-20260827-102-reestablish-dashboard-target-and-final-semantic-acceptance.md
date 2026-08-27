# CNX-20260827-102 — Re-establish Dashboard Target and Final Semantic Acceptance

Status: `READY_FOR_HERMES`

Execution mode: `LIVE_TARGET_LIFECYCLE_REESTABLISHMENT_INPUT_DIAGNOSIS_AND_FINAL_SEMANTIC_ACCEPTANCE`

Current authorization: `TASK101_ACCEPTED_OPERATOR_REQUESTED_NEW_ATTEMPT`

Owner: ChatGPT

Executor: Hermes/Codex after operator continuation

## Goal

Run the final Dashboard semantic acceptance again, but first fix the new Task-101 blocker by establishing a live, durable, freshly correlated Firefox/OpenClaw Dashboard target window before attempting any input method.

Task 102 must not stop merely because a launch process exits or a prior automation window id becomes stale. It must distinguish:

- browser process launch;
- the actual top-level Firefox window that receives the request;
- live OS HWND/PID identity;
- OpenClaw Dashboard/session identity;
- exact `Message Assistant` composer identity.

Only after all target layers are freshly correlated may Task 102 test input and eventually perform one final semantic Send.

The operator explicitly requested a new attempt and previously authorized iterative diagnosis: if a bounded method fails, identify the exact boundary, form an evidence-based next hypothesis, test the next pre-authorized bounded method, and report which method worked or why none worked.

## Accepted predecessor

Task 101 report:

`d06b1397e032749e5b348d5d1054dc1784d67519`

Task 101 independent disposition:

`ACCEPT_BLOCKER_TARGET_WINDOW_LIFECYCLE_NOT_ESTABLISHED`

Task 101 semantic send count was `0`.

No Task-101 sentinel, Ticket, route, provider inference, outbox, assistant delivery or semantic lifecycle effect occurred.

Task 101 failed before input testing because fresh automation/window inventory contained no Firefox/OpenClaw target. A previously observed window id was stale.

Accepted root-cause boundary:

`DASHBOARD_TARGET_WINDOW_LIFECYCLE_NOT_ESTABLISHED`

Historical positive control remains Task 092: a real authenticated Dashboard send once produced one Ticket, Ticket-before-provider ordering, one `ollama/qwen3.5:9b` call and one exact visible nonce. Task 093 repaired the later durable payload-staging boundary; Task 096 installed that repaired source live.

---

# Key operational correction

**Do not equate the PID/process handle returned by launching Firefox with the resulting browser window identity.**

Firefox may forward a `-new-window` request into an existing Firefox process and the launcher process may exit. Therefore every launch/bootstrap attempt must be followed by fresh OS-level window rediscovery.

Use current process/window state, not stale ids:

- enumerate `firefox.exe` processes;
- enumerate visible top-level windows with `EnumWindows`/equivalent;
- obtain HWND, PID, title/class and visibility;
- correlate the actual OpenClaw window through UIA/accessibility and non-secret Dashboard/session state;
- then discover the current `Message Assistant` composer under that exact window.

Automation-driver window ids are supporting evidence only; they are not durable identity.

---

# Absolute safety fence

Before final semantic Send, only low-impact target/bootstrap/input experiments are allowed.

Allowed:

- read-only controller/Gateway/SQLite/session/device/log/process/window/UIA/accessibility inspection;
- ephemeral PowerShell/Python/.NET/Win32/UIA helpers outside maintained product source;
- launching or opening one dedicated Firefox Dashboard window using the existing authenticated user profile and a non-secret local Dashboard URL/session route;
- one bounded bootstrap retry if fresh evidence proves the first launch/window attempt produced no usable conflicting target;
- UIA/accessibility direct composer edit;
- deterministic Win32 foreground/input-thread handoff;
- non-sent sentinel drafts and clearing them;
- read-only durable-state polling after the one semantic Send.

Forbidden:

- reading, printing, copying, logging, requesting, exporting or re-entering token/password/credential values;
- typing into any target before exact live window/session/composer correlation;
- sending any sentinel/test draft;
- more than one final semantic Send;
- historical nonce reuse;
- CLI/channel owner substitutes (`openclaw agent`, `chat.inject`, `sessions_send`, channel sends);
- direct Ollama/provider probes;
- synthetic/manual Ticket creation;
- install/install-over/uninstall/reset/cleanup;
- maintained product-source/runtime/config/controller/startup/Supervisor/AGENTS/SQLite mutation;
- provider/model/timeout changes;
- deleting historical sessions merely to normalize the run;
- restart/reboot;
- merge/tag/release/force push.

If a non-sent sentinel is accidentally sent or produces a semantic Ticket/provider effect, stop, correlate that effect and do not perform the final semantic Send.

---

# Retry policy

Read-only operations: maximum `3` attempts per operation when useful.

## Target bootstrap

Maximum `2` bootstrap attempts total.

Attempt 2 is allowed only after:

1. at least 3 seconds grace;
2. fresh Firefox process enumeration;
3. fresh OS top-level window enumeration;
4. proof attempt 1 did not leave a usable or conflicting OpenClaw Dashboard target.

If attempt 1's window appears late, use it and do not launch again.

If multiple candidate OpenClaw windows appear, stop bootstrap and disambiguate by session/UI state rather than opening more windows.

## Each input method family

- one normal sentinel attempt;
- at most one state-gated retry for that same method family;
- retry only after grace plus fresh UI/session/durable evidence prove no conflicting/late effect;
- late success means success/no retry;
- ambiguous partial mutation blocks retry.

Failure of one method family may advance to the next distinct pre-authorized method only after the composer is empty and durable semantic state is unchanged.

Final semantic Send remains exactly one attempt for Task 102. No resend exists.

---

# Phase A — durable/live baseline

Before launching or selecting a target:

1. Record coordination execution HEAD.
2. Verify Task 101 report/review are ancestors and publication fence is valid.
3. Verify OpenClaw remains `2026.7.1-2 (0790d9f)`.
4. Verify controller remains MANAGED generation `24`.
5. Verify accepted plugin fingerprint remains:
   `df2600da3ae78e1613793b4a7e5d1ebe61f66f71f0903e1d5d2cd5f0d5f4f4b4`.
6. Verify Gateway healthy, Supervisor healthy/recent and SQLite integrity `ok`.
7. Snapshot Ticket/event/outbox/direct-model-call/assistant-delivery/direct-recovery/workflow counts/tables that exist.
8. Prove no active semantic/provider operation attributable to this task.
9. Enumerate current Dashboard sessions read-only.
10. Prefer existing fresh/empty Dashboard session `agent:main:dashboard:89992501-1b33-46cf-85f7-eb0c1ef4d311` if it still exists and remains empty/staged. If it is no longer suitable, select another authenticated empty Dashboard session only if exact identity/freshness can be proven without semantic mutation. Do not fabricate or reuse a non-empty historical semantic session.

If no safe fresh Dashboard session can be proven:

`BLOCKED_FRESH_SESSION_NOT_ISOLATED`

---

# Phase B — establish a live target window

## B1. Pre-launch OS inventory

Independently of the UI driver:

- enumerate all current `firefox.exe` processes;
- enumerate visible top-level windows;
- record HWND/PID/title/class/visibility;
- record current foreground HWND;
- identify whether any existing window already shows OpenClaw Control.

If an existing live OpenClaw window can be uniquely correlated to the Phase-A target session, use it and do not launch another.

## B2. Dedicated-window bootstrap if needed

Open one dedicated Firefox window to the non-secret local OpenClaw Dashboard/session route using the already authenticated user profile.

Important:

- do **not** assume the process returned by the launch command owns the resulting window;
- do not depend on a prior automation `window_id`;
- wait at least 2 seconds, then rediscover from live OS windows;
- if the launcher exits but a new/existing Firefox process/window contains OpenClaw, that is valid and should be correlated rather than treated as launch failure.

If no live OpenClaw window appears, capture:

- launch exit/result;
- Firefox process before/after delta;
- top-level window before/after delta;
- whether Firefox reused an existing process;
- any non-secret OS/UI error.

A second bootstrap attempt is allowed only under the state-gated rule above.

## B3. Stability proof

Before any sentinel:

1. identify exact current OpenClaw HWND/PID/title/class;
2. wait at least 3 seconds;
3. enumerate again;
4. prove the same window still exists (`IsWindow`/equivalent) and is visible;
5. prove current UIA/accessibility tree is obtainable under that exact window;
6. prove exact target Dashboard session is selected;
7. locate the current `Message Assistant` composer and prove it is empty.

Required target token:

`DASHBOARD_LIVE_TARGET_REESTABLISHED`

If the window vanishes between rediscoveries:

`BLOCKED_DASHBOARD_TARGET_WINDOW_LIFECYCLE`

The report must state the observed process/window lifetime behavior and the tested hypothesis.

---

# Phase C — input method diagnosis ladder

The report must contain a section named exactly:

`Input method diagnosis and results`

For every method attempted, record:

- target HWND/PID/session/composer correlation;
- method-specific capability/probe;
- sentinel attempt count;
- grace/retry decision;
- whether draft appeared in exact composer;
- whether clearing succeeded;
- Ticket/provider/durable before/after counts;
- exact failure boundary if failed;
- next hypothesis and why it is safe.

Use a unique non-secret sentinel per method. Never Send it.

## Method 1 — UI Automation / Accessibility direct edit

Inspect the exact `Message Assistant` element for writable automation/accessibility interfaces, including Value/Edit/Text/Legacy patterns or equivalent.

If a supported direct-edit interface exists:

1. set a unique sentinel through that exact element without global keyboard input;
2. re-read UIA/accessibility and visual state;
3. prove the sentinel exists only in that exact composer;
4. clear through the same safe interface;
5. prove composer empty;
6. prove no Ticket/provider effect.

If direct edit is unsupported, record exactly which patterns are exposed and the failure/return code rather than treating that as generic focus failure.

## Method 2 — deterministic Win32 foreground/input handoff

If Method 1 cannot write:

1. fresh-rediscover exact target HWND/PID;
2. record current foreground HWND/thread;
3. use a bounded supported handoff such as ShowWindow/BringWindowToTop/AttachThreadInput/SetForegroundWindow as appropriate;
4. **before any global keystroke**, require `GetForegroundWindow == exact target HWND`;
5. focus the exact composer from fresh UIA/location evidence;
6. type one unique non-sent sentinel;
7. verify sentinel in exact composer;
8. clear and prove empty;
9. detach any input-thread attachment even on failure;
10. prove no Ticket/provider effect.

Never type if foreground equality is not proven.

## Method 3 — controlled natural-focus positive control

If Methods 1 and 2 fail but target bootstrap can safely create another dedicated window under retry limits:

- reproduce the historical positive-control condition where a newly opened dedicated Firefox window naturally owns foreground;
- immediately rediscover its actual HWND rather than trusting launcher PID;
- require exact session/composer correlation and foreground equality before typing;
- use a unique non-sent sentinel;
- verify, clear and prove zero semantic/provider effect.

Do not use timing alone as proof. The window must be positively identified.

## Input success

If any method passes, report:

`Known-working Dashboard input method`

and issue token:

`DASHBOARD_INPUT_METHOD_REPRODUCIBLY_PROVEN`

Composer must be empty and durable baseline unchanged before Phase D.

If all safe methods fail:

`BLOCKED_ALL_BOUNDED_DASHBOARD_INPUT_METHODS`

Do not generate a semantic nonce.

---

# Phase D — one final semantic Send

Only after `DASHBOARD_INPUT_METHOD_REPRODUCIBLY_PROVEN` and a clean composer/durable baseline:

1. re-verify exact current HWND/PID/session/composer with the proven method;
2. generate a brand-new nonce:
   `CNXSEM6-<UTC compact timestamp>-<random uppercase/hex suffix>`;
3. verify nonce absent from current sessions/logs/Tickets;
4. enter exactly:
   `ตอบกลับข้อความนี้เพียงว่า <NEW_NONCE>`
   using the proven input method;
5. re-read the exact composer and prove the full prompt exactly before Send;
6. Send exactly once through the authenticated Dashboard UI;
7. record send timestamp and non-secret correlation metadata;
8. no resend under any result.

Semantic send count must remain exactly `1` for Task 102.

---

# Phase E — Ticket before provider

Require exactly one new Ticket for the one message.

Prove durable ordering:

`accepted -> routed -> provider start`

Require:

- one Ticket;
- one accepted event;
- one route event;
- accepted/routed timestamps before correlated provider inference;
- no duplicate Ticket/route.

Blockers:

`BLOCKED_TICKET_BEFORE_PROVIDER_ORDERING`

`BLOCKED_DUPLICATE_TICKET_OR_ROUTE`

---

# Phase F — exactly one correlated provider inference

Expected provider/model:

`ollama/qwen3.5:9b`

Require exactly one correlated normal provider call.

The historical Task-092 call was slow. If the provider call remains actively correlated/running, observe read-only for up to `25 minutes` before calling it failed. Do not resend, change model or change timeout.

Blocker:

`BLOCKED_CORRELATED_PROVIDER_INFERENCE`

---

# Phase G — durable payload staging

Require exactly one assistant-delivery payload for the exact session/run/Ticket and prove:

- non-empty final payload;
- normalized text exactly equals nonce;
- durable staging occurs before or at native delivery boundary;
- no competing staged payload;
- no fail-closed regenerated replacement.

Blocker:

`BLOCKED_DURABLE_FINAL_PAYLOAD_STAGING`

---

# Phase H — visible reply and durable completion

Require:

- exactly one visible Dashboard assistant reply equal to nonce;
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

Prove:

- new staged empty state;
- no stale/unknown-parent/fallback error;
- no second semantic Send;
- no additional Ticket/provider effect.

---

# Final health and preservation

Verify:

- MANAGED generation `24`;
- accepted plugin fingerprint unchanged;
- Gateway/Supervisor healthy;
- SQLite integrity `ok`;
- no product/config/install mutation;
- historical evidence preserved;
- no secret disclosure.

Required final success token:

`PASS_FINAL_AUTHENTICATED_FRESH_SESSION_SEMANTIC_ACCEPTED`

---

# Publication fence

No product-source commit is expected.

Publish exactly one report-only commit:

`docs/operations/coordination/reports/CNX-20260827-102-reestablish-dashboard-target-and-final-semantic-acceptance.md`

The report must include:

- `Target lifecycle diagnosis and results`
- `Input method diagnosis and results`
- `Known-working Dashboard input method` if one method passes
- exact semantic result if Phase D is reached
- which method worked, or exact reason none worked
- each tested fix/hypothesis and result

Only independent review of the report/publication fence may claim final semantic acceptance.