# CNX-20260906-271 — Human Live Authorization

## Decision

`AUTHORIZED_BOUNDED_LIVE_INSTALL_OVER_AND_CURSOR_REQUALIFICATION`

On 2026-09-06 ICT, the human operator explicitly authorized proceeding with Task271 after ChatGPT described the bounded live scope.

## Granted authority

Hermes may:

1. perform exactly one supported install-over of exact candidate `6a491d1a95394bba7b70735fbaf9cebf4d619ea6`;
2. allow/require the supported managed Gateway process boundary that is part of that install-over;
3. verify installed fingerprint/payload binding and fresh Gateway identity;
4. observe at least 5 natural `PT1M` supervisor ticks with Win32 cursor/process correlation;
5. perform read-only health/state verification needed to determine whether the recurring APPSTARTING/busy-cursor symptom is removed.

## Authority not granted

```text
uninstall/reset                                  = 0
live OpenClaw session delete/reset               = 0
Discord/Dashboard/API semantic send              = 0
manual Ticket/session/SQLite mutation            = 0
recovery replay/redelivery/disposition           = 0
Scheduled Task disable/delete/cadence change     = 0
ad-hoc process/service kill outside supported install-over boundary = 0
release/tag/default-branch promotion             = 0
force push/history rewrite                       = 0
```

Old Ticket `CNXT-dc11c9a0-8a89-4df5-9c48-345260725be4` remains read-only evidence. This authorization does not prove its owner intent and does not authorize cancel/redeliver/dispose/replay.

## Retry fence

The install-over is one-shot. If execution is ambiguous, partially fails, or cannot prove the candidate/process boundary, stop and report. Do not blind-retry the installer or semantic/live side effects.
