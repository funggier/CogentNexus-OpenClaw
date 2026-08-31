# CNX-20260827-101 — Focus-Independent Dashboard Input and Final Semantic Acceptance

Status: `READY_FOR_HERMES`

Execution mode: `LIVE_BOUNDED_INPUT_ROOT_CAUSE_AND_FINAL_SEMANTIC_ACCEPTANCE`

Current authorization: `TASK100_ACCEPTED_OPERATOR_AUTHORIZED_BOUNDED_INPUT_REPAIR_AND_TEST`

Owner: ChatGPT

Executor: Hermes/Codex after operator continuation

## Goal

Remove dependence on accidental Firefox foreground-focus timing, prove at least one reproducible safe method for targeting the exact OpenClaw Dashboard composer, document which method works or why each method fails, and — only after the composer method is proven and the durable baseline is clean — continue the original final authenticated semantic acceptance in the same task.

The operator explicitly asked that if a method fails, the executor must identify the concrete failure boundary, form a plausible evidence-based fix/hypothesis, test the next bounded method, and report the outcome rather than stopping at the first simple UI-control failure.

This task is an operational/UI-input investigation. It must not redesign CogentNexus semantic architecture or mutate product source.

## Accepted predecessor

Task 100 report:

`8ad8377750f72fcee69c78fa26a199233f997b5f`

Task 100 independent disposition:

`ACCEPT_BLOCKER_WINDOWS_FOREGROUND_INPUT_OWNERSHIP`

Task 100 established all of the following without a semantic send:

- exact target session: `agent:main:dashboard:89992501-1b33-46cf-85f7-eb0c1ef4d311`;
- Firefox PID observed: `15980`;
- Firefox HWND observed: `394370`;
- title: `OpenClaw Control — Mozilla Firefox`;
- exact accessibility composer: `Message Assistant`;
- durable SQLite baseline remained healthy;
- no Task-100 Ticket, route, provider inference, outbox or delivery effect.

PID/HWND are observations from Task 100, not permanent identifiers. Task 101 must rediscover/correlate current PID/HWND fresh before using them.

Historical positive control: Task 092 successfully sent once through a fresh authenticated Dashboard session, produced one Ticket, routed before one `ollama/qwen3.5:9b` call, and visibly rendered the exact nonce. It failed later at durable delivery completion. Task 093 repaired the durable staging boundary and Task 096 installed/accepted that repaired source live.

## Root-cause hypothesis carried forward

The accepted Task-100 boundary is:

`WINDOWS_FOREGROUND_INPUT_OWNERSHIP_NOT_DETERMINISTIC`

Target identification and composer identification were correct. The failure occurred because global keyboard input was unsafe when the exact Firefox/OpenClaw window was not the verified Windows foreground input owner.

The earlier successful operator/Codex test occurred while a newly opened Firefox window naturally still held focus. Task 101 must convert that timing-dependent observation into a reproducible method or find a focus-independent alternative.

---

# Absolute safety fence

Before semantic Send, only low-impact UI/input experiments are allowed.

Allowed:

- read-only controller/Gateway/SQLite/session/device/log/window/process/UIA/accessibility inspection;
- ephemeral diagnostic/UI helper code or commands outside product source, including PowerShell/Python/.NET/Win32/UI Automation probes, provided they are not committed as product changes;
- direct UI Automation / Accessibility value-edit operations against the exact correlated `Message Assistant` composer;
- bounded Win32 foreground/input-thread handoff operations against the exact correlated Firefox/OpenClaw HWND;
- opening one dedicated Firefox Dashboard window as a bounded positive-control fallback when the URL/state can be used without exposing/re-entering secrets;
- non-sent sentinel drafts for input proof;
- clearing non-sent sentinel drafts;
- read-only durable-state polling after the one authorized semantic send.

Forbidden:

- reading, printing, copying, logging, requesting, exporting or re-entering token/password/credential values;
- typing into any window unless the method-specific target proof is satisfied;
- sending any sentinel/test draft;
- more than one final semantic Send;
- reusing Task-099/Task-100 or older semantic nonces;
- CLI/channel owner substitutes (`openclaw agent`, `chat.inject`, `sessions_send`, channel sends);
- direct provider/Ollama inference probes;
- synthetic/manual Ticket creation;
- install/install-over/uninstall/reset/cleanup;
- product source/runtime/config/controller/startup/Supervisor/AGENTS/SQLite mutation;
- deleting/normalizing historical Dashboard sessions merely to make the test clean;
- provider/model/timeout changes;
- restart/reboot;
- merge/tag/release/force push.

If any non-sent sentinel is accidentally sent or produces a Ticket/provider effect, stop immediately, correlate and report that semantic effect, and do not perform the final semantic Send.

---

# Retry policy for Task 101

Read-only operations: maximum 3 attempts total per operation when useful.

For each low-impact input method family below:

- one normal sentinel attempt;
- at most one additional state-gated retry for that same method family;
- retry only after a grace interval and fresh UI/session/durable evidence prove the first attempt produced no conflicting/late effect;
- if the first attempt takes effect late, count it as success and do not repeat;
- ambiguous/partial mutation is not retryable.

Failure of one method family does **not** prohibit moving to the next distinct pre-authorized method family after proving the composer is empty and durable semantic state is unchanged.

The final semantic Send remains exactly one attempt for the entire task. No resend exists.

---

# Phase A — baseline and exact target correlation

Before any sentinel:

1. Record coordination execution HEAD.
2. Verify Task 100 report/review are ancestors and Task-100 publication fence is valid.
3. Verify OpenClaw remains `2026.7.1-2 (0790d9f)`.
4. Verify controller remains MANAGED generation 24 and the accepted plugin fingerprint remains `df2600da3ae78e1613793b4a7e5d1ebe61f66f71f0903e1d5d2cd5f0d5f4f4b4`.
5. Verify Gateway healthy, Supervisor healthy/recent, SQLite integrity `ok`.
6. Snapshot current Ticket/event/outbox/direct-model-call/assistant-delivery/direct-recovery/workflow counts/tables that exist.
7. Re-correlate the current authenticated Dashboard window, current Firefox PID/HWND/title/class, exact selected session and `Message Assistant` composer.
8. Require the semantic target to be a fresh/empty Dashboard session. Prefer the Task-099/100 target if it is still empty and selected; otherwise a newly staged empty Dashboard session may be used only through normal non-semantic Dashboard session management under the existing state-gated policy.
9. Prove no active semantic/provider operation and composer empty before input tests.

If no exact fresh target can be established, stop before sentinel/nonces.

---

# Phase B — bounded input method ladder

The executor must test these method families in order unless an earlier method succeeds. Do not skip directly to global keyboard injection merely because coordinates are known.

## Method 1 — focus-independent UI Automation / Accessibility direct edit

Goal: write the draft into the exact `Message Assistant` control without relying on global Windows keyboard focus.

1. Inspect the exact composer element's supported UIA/Accessibility control type and patterns/interfaces.
2. Prefer direct editable/value mechanisms exposed by the control, for example a writable ValuePattern/Value interface or equivalent accessibility edit operation.
3. Use a unique non-sent sentinel such as `CNXINPUT5-UIA-<short-random>`.
4. After the direct-edit operation, read fresh accessibility state and visual/UI state from the same composer.
5. Success requires the exact sentinel to be present in that exact composer and zero durable semantic/provider effects.
6. Clear the sentinel through the same safe control path if possible; verify empty.

If direct edit is unsupported or rejected, record exactly which control patterns/interfaces were present and the exact reason direct editing is unavailable. Do not treat unsupported ValuePattern as generic failure; it is evidence for the next method.

Method result tokens:

- `INPUT_METHOD_UIA_DIRECT_PASS`
- `INPUT_METHOD_UIA_DIRECT_UNSUPPORTED`
- `INPUT_METHOD_UIA_DIRECT_FAILED`

## Method 2 — deterministic Win32 foreground/input-thread handoff

Use only if Method 1 did not pass.

Goal: make the exact correlated Firefox/OpenClaw HWND the verified foreground input owner before any global keyboard input.

The implementation may use supported Win32 mechanisms as needed, including fresh `GetForegroundWindow`, target/foreground thread IDs, `ShowWindow/ShowWindowAsync`, `BringWindowToTop`, `SetForegroundWindow`, and a temporary `AttachThreadInput` handoff where appropriate. Avoid permanent hooks or system policy changes.

Required sequence:

1. Freshly rediscover the exact target HWND/PID; do not reuse stale Task-100 handles blindly.
2. Restore/show target if needed.
3. Record current foreground HWND and both relevant thread IDs.
4. Perform one bounded foreground/input ownership handoff.
5. Detach any temporary thread-input attachment after the handoff.
6. Re-read `GetForegroundWindow` and require exact equality with target HWND.
7. Focus/click the exact fresh `Message Assistant` composer and verify UIA focused element/descendant correlation when available.
8. Only after exact foreground verification may global keystrokes type a unique sentinel `CNXINPUT5-WIN32-<short-random>`.
9. Verify exact sentinel appears in the intended composer and durable semantic/provider state remains unchanged.
10. Clear and re-verify empty.

If foreground ownership cannot be acquired, report the exact Win32 call outcomes/last-error values where meaningful, current foreground HWND/PID, target HWND/PID and evidence explaining the restriction. Do not type if foreground equality is not proven.

Method result tokens:

- `INPUT_METHOD_WIN32_HANDOFF_PASS`
- `INPUT_METHOD_WIN32_HANDOFF_BLOCKED`
- `INPUT_METHOD_WIN32_HANDOFF_FAILED`

## Method 3 — controlled dedicated Firefox window positive-control handoff

Use only if Methods 1 and 2 did not pass and only when it can be done without reading/re-entering credentials.

This method intentionally reproduces the condition under which the operator/Codex previously succeeded: a newly created dedicated Firefox OpenClaw Dashboard window naturally owns foreground focus.

1. Open at most one dedicated Firefox window to the authenticated local Dashboard state/session using a non-secret URL/navigation path.
2. Do not expose token/password values in command lines, logs or report.
3. Correlate the new window to the OpenClaw Dashboard and exact intended fresh session/composer.
4. Immediately verify `GetForegroundWindow` equals this exact Firefox HWND; do not assume new-window focus.
5. Focus the freshly captured `Message Assistant` composer.
6. Type unique non-sent sentinel `CNXINPUT5-NEWFW-<short-random>` only while foreground equality remains proven.
7. Verify sentinel in exact composer, zero durable semantic/provider effect, clear, and re-verify empty.

If the new window is not foreground or cannot be correlated to the intended authenticated session, do not type.

Method result tokens:

- `INPUT_METHOD_NEW_FIREFOX_PASS`
- `INPUT_METHOD_NEW_FIREFOX_BLOCKED`
- `INPUT_METHOD_NEW_FIREFOX_FAILED`

---

# Phase C — required method diagnosis/reporting

Whether a method succeeds or fails, the report must include a section named exactly:

`Input method diagnosis and results`

For every method actually attempted, record:

- method name;
- exact non-secret target correlation used;
- attempt count;
- whether sentinel appeared in the intended composer;
- whether the composer was returned to empty;
- whether any Ticket/provider/delivery effect occurred;
- PASS/BLOCKED/FAILED token;
- exact failure boundary if not PASS;
- evidence-based hypothesis/fix attempted next;
- why moving to the next method was safe.

If a method passes, also include a section named exactly:

`Known-working Dashboard input method`

Document the reproducible non-secret sequence precisely enough for a later executor to reuse it without rediscovering the focus problem.

Required input token before semantic continuation:

`DASHBOARD_INPUT_METHOD_REPRODUCIBLY_PROVEN`

If all three methods fail, stop with:

`BLOCKED_ALL_BOUNDED_DASHBOARD_INPUT_METHODS`

Do not generate a semantic nonce.

---

# Phase D — clean semantic preflight after input proof

Only after one method passes:

1. Verify composer empty.
2. Verify exact fresh Dashboard target/session still selected and has no prior semantic transcript attributable to this task.
3. Re-snapshot durable counts and require no sentinel-related Ticket/route/provider/outbox/delivery effect.
4. Verify Gateway/controller/plugin/SQLite health unchanged.
5. Verify no active provider call.
6. Retain the proven input method and target correlation; do not switch to an unproven method for the semantic send.

If this clean baseline is not proven, stop before nonce generation.

---

# Phase E — exactly one final semantic send

Generate a brand-new execution-time nonce only now:

`CNXSEM5-<UTC compact timestamp>-<random uppercase/hex suffix>`

Verify it does not pre-exist in durable state/session history.

Using the exact method proven in Phase B, enter exactly:

`ตอบกลับข้อความนี้เพียงว่า <NEW_NONCE>`

Verify the complete intended prompt is present in the exact composer before Send.

Then invoke Send exactly once.

Semantic Send count for Task 101 must remain exactly `1`.

No resend, no alternate channel, no second nonce, no provider probe.

---

# Phase F — fresh-session isolation and Ticket-before-provider

Require:

- the message is the first semantic message in the selected fresh target for this task;
- no stale/unknown-parent/Main fallback;
- exactly one new Ticket correlated to the session/run;
- exactly one accepted event;
- exactly one routed event;
- durable accepted/routed timestamps precede correlated provider inference start;
- no duplicate Ticket/route/promotion.

Blockers:

- `BLOCKED_FRESH_SESSION_NOT_ISOLATED`
- `BLOCKED_TICKET_BEFORE_PROVIDER_ORDERING`
- `BLOCKED_DUPLICATE_TICKET_OR_ROUTE`

---

# Phase G — correlated provider inference

Require exactly one normal correlated provider call:

`ollama/qwen3.5:9b`

No direct readiness probe is allowed.

Task 092 showed this local call may be slow. Do not infer failure merely from elapsed time while the correlated call remains active. Use read-only observation/polling; an active correlated provider call may be observed for up to 25 minutes without resend or timeout/model mutation.

Require exactly one call start and one terminal outcome.

Blocker:

`BLOCKED_CORRELATED_PROVIDER_INFERENCE`

---

# Phase H — durable final payload staging before native delivery

This is the Task-093 repaired boundary.

Require exactly one durable assistant-delivery/staging record for the exact owner/session/run/Ticket and require the staged final text to normalize exactly to the nonce.

Prove staging is committed before or at the required native delivery boundary and before visible delivery is accepted as success.

Visible nonce without durable staging is failure.

Blocker:

`BLOCKED_DURABLE_FINAL_PAYLOAD_STAGING`

---

# Phase I — visible reply and durable completion

Require:

- exactly one visible assistant reply equal to nonce after whitespace normalization;
- exactly one `response_ready`;
- exactly one `delivery_confirmed`;
- Ticket terminal state `completed`;
- lifecycle `accepted -> routed -> response_ready -> delivery_confirmed -> completed` for the exact Ticket/run/session;
- no duplicate provider call, Ticket, route, staged payload, outbox, visible nonce, durable-promotion or recovery effect.

Blockers:

- `BLOCKED_VISIBLE_NONCE_RESPONSE`
- `BLOCKED_RESPONSE_DELIVERY_COMPLETION`
- `BLOCKED_DUPLICATE_SEMANTIC_EFFECT`

---

# Phase J — post-completion New Session continuity

Only after terminal `completed`:

1. Enter New Session/New Chat with zero message send.
2. State-gated low-impact retry policy may be used once if needed: wait, inspect state, and retry only when the first action is proven effect-free.
3. Prove a fresh/empty staged session can be entered without stale/unknown-parent/Main fallback.
4. Require zero additional Ticket/provider/delivery semantic effect.

Blocker:

`BLOCKED_POST_COMPLETION_NEW_SESSION_CONTINUITY`

---

# Final preservation and publication

Verify controller remains MANAGED, plugin fingerprint unchanged, Gateway healthy, Supervisor healthy, SQLite integrity `ok`, prior retired evidence unchanged, no product-source/runtime/config mutation, and no secret disclosure.

Publish exactly one report-only commit:

`docs/operations/coordination/reports/CNX-20260827-101-focus-independent-dashboard-input-and-final-semantic-acceptance.md`

Required final PASS token:

`PASS_FINAL_AUTHENTICATED_FRESH_SESSION_SEMANTIC_ACCEPTED`

Other terminal result tokens include the phase-specific blockers above and:

- `BLOCKED_ALL_BOUNDED_DASHBOARD_INPUT_METHODS`
- `BLOCKED_UNEXPECTED_SENTINEL_SEMANTIC_EFFECT`
- `BLOCKED_LIVE_HEALTH_REGRESSION`
- `BLOCKED_EVIDENCE_PUBLICATION_UNSAFE`

## Publication fence

No product source commit is expected in Task 101. The report must be the only intended publication delta from the coordination execution HEAD. If an operational diagnostic helper was created outside the repo, do not publish it unless a later task separately reviews and authorizes turning it into a maintained tool.
