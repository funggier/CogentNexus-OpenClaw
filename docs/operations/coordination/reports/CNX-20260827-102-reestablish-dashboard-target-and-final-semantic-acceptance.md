# CNX-20260827-102 — Open Fresh Dashboard Target and Final Semantic Acceptance

## Result

`BLOCKED_DURABLE_FINAL_PAYLOAD_STAGING`

The Dashboard input method and one final semantic send were completed, but the repaired durable delivery boundary did not produce the required durable assistant-delivery/staging record. No retry or second semantic send was performed.

## Execution and safety

Execution started from synchronized coordination HEAD `9b9cb77b77f3e4e57887c4ffa87a0cd273e4ef55`. Task 101 report/publication was an ancestor and the Task-102 report path was absent before publication.

No product source, runtime, configuration, SQLite, session, provider, model, or delivery state was manually mutated. No credential, password, token, or secret was read, copied, printed, logged, requested, or entered.

## Firefox/bootstrap diagnosis and results

Initial live inventory showed Firefox but no OpenClaw Control window. Following the Task-102 rule, Firefox was opened immediately to the non-secret local Dashboard route using the existing profile. A fresh OpenClaw Control window was discovered as Firefox PID `12060`, window `328720`, title `OpenClaw Control — Mozilla Firefox`.

Fresh UIA state showed the exact target session:

`agent:main:dashboard:89992501-1b33-46cf-85f7-eb0c1ef4d311`

The exact `Message Assistant` composer was present and empty. After the required wait/stability interval, the same window remained visible, UIA remained readable, and `GetForegroundWindow == 328720` was proven. No credential re-entry was required.

## Input method diagnosis and results

### Method 1 — UI Automation / Accessibility direct edit

- Attempt count: `1` invocation, refused before mutation
- Target: Firefox PID `12060`, window `328720`, exact Dashboard session above, `Message Assistant`
- Direct-edit probe: the driver rejected `set_value` because the native capture did not provide the required snapshot token (`snapshot_id_required`)
- Sentinel: not typed by this method
- Result: `INPUT_METHOD_UIA_DIRECT_UNSUPPORTED`
- Safe next step: move to the pre-authorized foreground method; no composer or durable state changed

### Method 2 — deterministic Win32 foreground/input-thread handoff

- Attempts: `2` bounded handoff attempts
- Fresh target: HWND `6227698`/the then-current OpenClaw window was rediscovered before use
- First handoff: `AttachThreadInput=True` and `SetForegroundWindow=True`, but the post-handoff foreground remained HWND `65858`, not the target
- Second handoff: `SwitchToThisWindow=True` and `SetForegroundWindow=True`, but `SetActiveWindow`/`SetFocus` did not succeed and the post-handoff foreground again remained `65858`
- Sentinel: not typed because exact foreground equality could not be proven after the handoff
- Result: `INPUT_METHOD_WIN32_HANDOFF_BLOCKED`
- Safe next step: use the distinct dedicated-new-Firefox positive control; no semantic effect occurred

### Method 3 — dedicated Firefox natural-focus positive control

- Fresh target: Firefox PID `12060`, HWND `328720`, title `OpenClaw Control — Mozilla Firefox`
- Exact session and composer were verified by fresh UIA state
- After the required stability wait, `GetForegroundWindow == 328720` was proven
- The operator then clicked the exact composer with the real mouse, leaving keyboard focus in the intended field
- A fresh foreground check still showed the target HWND, so one non-sent sentinel was typed without clicking again: `CNXINPUT5-MANUAL-AB12`
- The sentinel appeared visually in the exact composer, proving the method
- It was cleared with `Ctrl+A` and `Backspace`; fresh visual state showed the composer empty
- Durable counts remained unchanged during sentinel proof: tickets `1` before final send, ticket events `7`, outbox `0`, direct model calls `1` baseline, assistant deliveries `0`
- Result: `INPUT_METHOD_NEW_FIREFOX_PASS`
- Required method token: `DASHBOARD_INPUT_METHOD_REPRODUCIBLY_PROVEN`

### Known-working Dashboard input method

1. Open Firefox to the non-secret local Dashboard/session URL with the existing authenticated profile.
2. Rediscover the actual live OpenClaw window and current PID/HWND; do not reuse stale identifiers.
3. Wait for UIA to expose the exact target session and `Message Assistant` composer, then wait for stability.
4. Verify `GetForegroundWindow` equals the current Firefox HWND.
5. Have the operator click once inside the exact composer with the real mouse. Do not issue another automation click afterward, because automation click can cause Windows to change the foreground owner.
6. Re-read the foreground/window/session/composer state. Only then send foreground keystrokes.
7. Verify the sentinel or intended text visually in that same composer. Never press Enter during sentinel proof.
8. Clear the draft with `Ctrl+A` and `Backspace`, then verify the composer is empty before semantic use.

The unsafe condition is any loss of exact foreground equality, disappearance of the target window, mismatch of session/composer, or unverifiable text placement. In those cases, stop rather than typing or sending.

## Final semantic acceptance

After the input method passed and the composer was clean, a fresh nonce was generated once:

`CNXSEM6-20260827T102511Z-FCE9FDB0`

The exact prompt was entered and visually verified in the intended composer. The operator then performed the single Dashboard Send. No resend was performed.

Read-only durable evidence correlated the new Ticket to the exact target session:

- Ticket: `CNXT-415b82d9-5553-4bd2-996a-54f57163f7e4`
- owner session: `agent:main:dashboard:89992501-1b33-46cf-85f7-eb0c1ef4d311`
- Ticket count: `2` (baseline `1`, exactly one new Ticket)
- event count: `12` (baseline `7`, three new admission/provider events plus `direct_model_call_ended` and `response_ready`)
- outbox count: `0`
- direct model call count: `2` (baseline `1`, exactly one new call)
- assistant-delivery count: `0`
- SQLite integrity: `ok`

Observed lifecycle so far:

`accepted -> routed -> direct_model_call_started -> direct_model_call_ended -> response_ready`

The provider call was the expected `ollama/qwen3.5:9b` path as shown by the Dashboard model state and the correlated direct-call lifecycle. The UI visibly rendered exactly one assistant reply equal to the nonce.

## Durable staging blocker

After `response_ready`, read-only polling for an additional minute still showed:

- Ticket status: `accepted`
- `response_ready_at` present
- `delivery_confirmed_at`: `null`
- no `cnx_assistant_delivery` row
- no `ticket_outbox` row
- no `delivery_confirmed` event
- no `completed` terminal status

Thus the visible nonce cannot be accepted as final success: the required durable final payload/staging record is absent. This is reported as `BLOCKED_DURABLE_FINAL_PAYLOAD_STAGING`. No repair, retry, resend, or direct provider probe was attempted.

## Post-completion New Session

Not executed because the exact Ticket did not reach durable `completed`.

## Final preservation

No duplicate Ticket, route, provider call, visible nonce, or semantic resend was observed. Historical evidence was not rewritten. This report is the single Task-102 report-only artifact; no product-source commit is included.
