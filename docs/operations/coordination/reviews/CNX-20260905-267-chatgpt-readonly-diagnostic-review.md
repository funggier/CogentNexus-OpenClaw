# CNX-20260905-267 — ChatGPT Read-Only Diagnostic Review

Verdict: `ACCEPT_READONLY_DIAGNOSTIC__BUSY_CURSOR_CAUSAL_PROOF_REQUIRED`

## Accepted evidence

Task267 stayed within its read-only fence and established all of the following:

- `CogentNexus-OpenClaw-Supervisor` is enabled with a Windows Scheduled Task repetition interval of `PT1M`.
- The task runs `host_control_v092.py ... supervisor tick --execute-safe` and produces short-lived `supervisor tick -> lifecycle status -> gateway status` process waves at approximately one-minute cadence.
- Gateway PID `23596` and Ollama PID `8560` remained stable throughout the bounded capture; no restart was observed.
- Current Ollama health is good, but the durable recovery state still reports open incident `ollama:1`, classification `provider_unreachable`, circuit open, attempts `3/3`.
- The installed plugin payload still does not match accepted Task265 candidate `ec1fdbb2ea036c6dcd1c375b8171868335d63fc8`.
- The old target Ticket/recovery remains unresolved and read-only; generic continuation does not authorize disposition.

## Busy-cursor assessment

The one-minute process churn is a strong temporal correlate for the user's approximately one-minute busy-circle symptom, but Task267 did not observe the Windows cursor state itself. Therefore causal attribution is not yet proven.

Historical evidence from Task063 is relevant: the same PT1M supervisor previously caused a visible console-flash defect through its child process chain, and the repair moved the durable Windows task to a product-owned `pythonw.exe` runtime. The current source still intentionally keeps the PT1M cadence and a hidden InteractiveToken Scheduled Task. This makes the supervisor a credible suspect, but not yet a proven cause of the current cursor symptom.

## Required successor

Open Task268 as a strictly read-only causal-correlation diagnostic. It must capture the actual Windows cursor state at high frequency and correlate WAIT / APPSTARTING transitions directly with supervisor process-start waves over multiple natural PT1M ticks.

No Scheduled Task disable/stop/reconfiguration, Gateway/provider lifecycle mutation, install-over, session delete/reset, semantic send, recovery disposition, or database mutation is authorized.

## Deployment / recovery position

Task267 does not clear deployment or live-acceptance gates. Exact-candidate deployment remains required before live session acceptance, and the old Ticket plus open provider recovery incident remain separate authority/acceptance blockers.