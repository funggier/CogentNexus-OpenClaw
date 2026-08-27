# Review — CNX-20260827-100

Decision: `ACCEPT`

Disposition:

`ACCEPT_BLOCKER_WINDOWS_FOREGROUND_INPUT_OWNERSHIP`

## Publication verification

Task 100 execution coordination HEAD:

`0ac2655418cee76c7de8058f77cd22c29cf931cd`

Task 100 report HEAD:

`8ad8377750f72fcee69c78fa26a199233f997b5f`

Independent compare confirms exactly one report-only commit and no product-source mutation.

## What is accepted

The report correctly stopped before semantic nonce generation and before Send.

It established the intended Dashboard target at multiple independent boundaries:

- target session `agent:main:dashboard:89992501-1b33-46cf-85f7-eb0c1ef4d311`;
- Firefox PID `15980`;
- HWND `394370`;
- title `OpenClaw Control — Mozilla Firefox`;
- accessibility composer `Message Assistant`;
- composer empty before and after both sentinel attempts.

Durable baseline remained unchanged: SQLite integrity `ok`, no new Ticket, route, outbox, assistant delivery or provider activity attributable to Task 100.

## Root-cause disposition

The failure boundary is not Dashboard target identification and not composer coordinate discovery.

Both low-impact sentinel attempts failed because the intended Firefox/OpenClaw window could not be proven as the active Windows foreground input owner when keyboard input was about to be delivered. The earlier successful operator/Codex test occurred while a newly opened Firefox window still naturally held foreground focus.

Therefore the accepted root-cause class is:

`WINDOWS_FOREGROUND_INPUT_OWNERSHIP_NOT_DETERMINISTIC`

Task 100 is not evidence of a CogentNexus semantic-pipeline regression and does not invalidate the Task-093 staging repair or Task-096 live installation.

## Successor direction

The operator authorized a bounded successor to remove dependence on incidental Firefox focus timing.

The successor should test in order:

1. focus-independent UI Automation / Accessibility direct-edit mechanisms for the exact `Message Assistant` composer;
2. deterministic Win32 foreground handoff for the already-correlated Firefox HWND, including fresh foreground verification before any global keyboard input;
3. if necessary, a controlled dedicated-new-Firefox-window handoff as a positive-control fallback, but only with explicit foreground verification before typing.

Each method must use non-sent sentinel text first, clear the composer, and report whether it worked. If a method fails, the executor must capture the exact failure boundary, form a concrete hypothesis, try the next bounded mechanism, and report the evidence.

Only after a method is proven and the composer is clean may the same task generate one new semantic nonce and perform exactly one Send with no resend.
