# CNX-20260905-268 — Read-Only Busy-Cursor Causal Correlation Diagnostic

Status: `READY_FOR_HERMES`

Parent: `CNX-20260905-267`

Executor: `Hermes`

Review owner: `ChatGPT`

## Objective

Prove or disprove whether the user's approximately one-minute Windows busy-circle cursor symptom is causally tied to `CogentNexus-OpenClaw-Supervisor` process churn, without changing the live system.

## Required evidence

Capture at least 6 minutes or enough time to include at least 5 natural supervisor PT1M ticks.

1. Sample the actual Windows cursor state at high frequency (target 50–100 ms where practical) using a read-only Win32 API path such as `GetCursorInfo` and compare against the standard WAIT and APPSTARTING cursor handles. Record timestamped transitions and duration.
2. In parallel, capture process creation/termination with timestamp, PID, parent PID, executable path and command line for the supervisor tree and any other short-lived process near cursor transitions.
3. Record Scheduled Task last/next run timestamps and correlate each natural supervisor tick.
4. Record foreground process/window identity read-only where practical so an application-specific cursor change can be distinguished from system/process launch correlation. Do not inject input or manipulate windows.
5. Compare on-cycle and off-cycle periods. Do not infer causation from process name alone.
6. Inspect whether any `conhost.exe`, console-subsystem child, shell helper, PowerShell, cmd, or other foreground-capable process appears in the current supervisor tree despite the product-owned `pythonw.exe` design.
7. Audit the current source/installed action for windowless execution assumptions (`pythonw.exe`, `CREATE_NO_WINDOW`, hidden task, InteractiveToken) and reconcile them with observed runtime process behavior.

## Classification contract

- `STRONG_CAUSAL_MATCH`: cursor WAIT/APPSTARTING transitions repeatedly align with the supervisor wave (preferably at least 4 natural ticks, tight latency) and are absent from comparable off-cycle periods.
- `CORRELATED_NOT_PROVEN`: timing overlaps but cursor evidence is incomplete/ambiguous or other plausible process waves overlap.
- `NOT_SUPERVISOR`: cursor transitions do not align with supervisor ticks and another repeatable source is identified.
- `INCONCLUSIVE`: instrumentation cannot reliably distinguish the cursor state or capture enough natural events.

If custom Windows cursor themes make standard handle comparison unreliable, document that limitation and use additional read-only cursor metadata where available; do not change the user's cursor/theme.

## Secondary read-only checks

- Reconfirm Gateway/Ollama remain stable during capture; no restart action.
- Reconfirm open recovery incident `ollama:1` and installed-vs-candidate mismatch only as context; do not dispose/reset/recover/deploy anything.
- Old Ticket `CNXT-dc11c9a0-8a89-4df5-9c48-345260725be4` remains read-only and must not be redelivered/cancelled/disposed/replayed.

## Hard fences

```text
installer/install-over/uninstall/reset           = 0
Gateway/provider/service lifecycle mutation      = 0
live OpenClaw session delete/reset                = 0
live Discord/Dashboard/API semantic send         = 0
manual live Ticket/session/SQLite mutation       = 0
recovery replay/redelivery/disposition            = 0
Scheduled Task enable/disable/create/delete/run   = 0
stop/kill/restart unrelated live processes        = 0
input injection/window/cursor configuration       = 0
release/tag/default-branch promotion              = 0
force push/history rewrite                       = 0
```

Only temporary diagnostic processes created by Task268 may be stopped after capture.

## Completion

Publish:

`docs/operations/coordination/reports/CNX-20260905-268-readonly-busy-cursor-causal-correlation-diagnostic.md`

Then set `ACTIVE.md` and `STATUS.md` to `WAITING_FOR_CHATGPT_REVIEW` and stop project mutation.