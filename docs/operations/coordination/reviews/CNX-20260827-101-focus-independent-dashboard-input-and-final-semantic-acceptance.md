# Review — CNX-20260827-101 Focus-Independent Dashboard Input and Final Semantic Acceptance

Decision: `ACCEPT`

Disposition: `ACCEPT_BLOCKER_TARGET_WINDOW_LIFECYCLE_NOT_ESTABLISHED`

## Publication fence

Execution coordination HEAD:

`ef4e71628c4b4906f0a26ed4f6673241bb9999bc`

Report HEAD:

`d06b1397e032749e5b348d5d1054dc1784d67519`

Independent compare shows exactly one commit and exactly one added file:

`docs/operations/coordination/reports/CNX-20260827-101-focus-independent-dashboard-input-and-final-semantic-acceptance.md`

No product source mutation occurred in the publication delta.

## Accepted evidence

Task 101 stopped before any sentinel, UIA edit, Win32 handoff, nonce generation or semantic Send.

Semantic send count: `0`.

The required Dashboard target remained conceptually:

`agent:main:dashboard:89992501-1b33-46cf-85f7-eb0c1ef4d311`

but the fresh live window inventory contained no Firefox/OpenClaw window. A previously observed window identifier was stale and fresh capture failed because that window no longer existed in the automation inventory.

Therefore Task 101 correctly refused to use stale PID/HWND values and correctly refused global keyboard input without a freshly correlated target.

No new Ticket, route, provider inference, outbox item, assistant delivery or lifecycle effect was initiated by Task 101.

## Root-cause boundary

Task 101 did **not** test the three authorized input method families. It failed earlier at target-window lifecycle/discovery.

Accepted boundary:

`DASHBOARD_TARGET_WINDOW_LIFECYCLE_NOT_ESTABLISHED`

This is distinct from the Task-100 boundary `WINDOWS_FOREGROUND_INPUT_OWNERSHIP_NOT_DETERMINISTIC`.

A likely operational pitfall is treating the process/handle returned by a Firefox launch as the durable browser window identity. Firefox may route a `-new-window` request into an existing browser process and the launcher process can exit; therefore the target must be rediscovered from live top-level windows after launch rather than inferred from the launch process.

## Successor direction

The operator explicitly requested a new attempt and previously authorized iterative diagnosis/fix/testing.

The successor should first establish a durable dedicated Dashboard target window using live OS-level process/window discovery independent of stale automation IDs. It should:

1. enumerate current Firefox processes and visible top-level windows with Win32/OS evidence before launch;
2. if needed open one dedicated Firefox Dashboard window using the existing authenticated profile and a non-secret local Dashboard URL;
3. never assume the launcher PID owns the resulting window;
4. after a bounded wait rediscover the actual Firefox top-level HWND/PID/title via `EnumWindows`/equivalent and correlate it to OpenClaw UI/session state with fresh UIA/accessibility evidence;
5. if the window disappears, diagnose Firefox process/window lifetime and retry the launch/bootstrap at most once when state proves no conflicting window remains;
6. only after exact target/session/composer correlation begin the already-authorized UIA -> Win32 handoff -> controlled natural-focus input ladder;
7. if an input method succeeds, continue the final one-send semantic acceptance in the same task.

No historical nonce may be reused. Semantic Send remains single-attempt.