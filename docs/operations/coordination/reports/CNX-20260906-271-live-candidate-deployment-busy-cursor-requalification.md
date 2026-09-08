# CNX-20260906-271 — Live Candidate Deployment and Busy-Cursor Requalification

## Disposition

`PASS_WITH_REVIEW__NO_RECURRING_SUPERVISOR_CURSOR_WAVE`

## Authority and candidate

- Task: `CNX-20260906-271`
- Exact candidate: `6a491d1a95394bba7b70735fbaf9cebf4d619ea6`
- Human authorization: `CNX-20260906-271-human-live-authorization.md`
- Executor: Hermes
- Review owner: ChatGPT
- Remote branch was freshly fetched and remained at `029aefeb1eaf9baf5c5ed75e1cfdb846a1e23047` before publication.

## Installation

Exactly one supported install-over was executed from a detached checkout of the exact candidate:

- Installer: `scripts/install.ps1`
- Workspace: `C:\Users\CDQ-P\.openclaw\workspace`
- Installer exit code: `0`
- Transcript: `C:\Users\CDQ-P\AppData\Local\Temp\cnx-task271-live-20260906\install-transcript.log`
- Installer stages reported `exit_code=0`, including plugin rollover prepare/finalize, local package installation, managed runtime ensure, and health verification.
- No retry, ad-hoc kill, uninstall, reset, or manual repair was performed.

Installed identity changed from the pre-state fingerprint `fcecb29aa6605a888e262dd9d4b1b398f51e7e520feb59b65b99b7662d7f86b4` to the exact candidate-bound fingerprint:

```text
root: c:\users\cdq-p\.openclaw\extensions\cogentnexus-openclaw
version: 0.9.3
fingerprint: e3a1723d9329b00008078d0dfabfa72de21a0f7f042724123e43117148f6ebd3
```

## Fresh runtime verification

Post-install read-only verification showed:

- Host mode: `managed`
- Desired Gateway/provider: `running` / `running`
- Gateway: healthy, loopback `127.0.0.1:18789`, connectivity probe `ok`, PID `3948`
- Ollama: reachable/healthy/ready, PID `8560`
- Supervisor adapter: installed, enabled, hidden, `State=Ready`
- Supervisor command: `host_control_v092.py ... supervisor tick --execute-safe`
- Supervisor cadence: `PT1M`
- Scheduler: `CogentNexus-OpenClaw-Supervisor`, `LastTaskResult=0`, `NumberOfMissedRuns=0`
- Ticket counts: accepted `1`, cancelled `2`, completed `10`
- Pending outbox: `0`
- SQLite read-only integrity: `ok`
- Old Ticket `CNXT-dc11c9a0-8a89-4df5-9c48-345260725be4` remained read-only evidence; no mutation/cancel/redelivery/disposition/replay was issued.

## Cursor/process requalification

Fresh Task268-compatible Win32 observer artifacts:

- Evidence root: `C:\Users\CDQ-P\AppData\Local\Temp\cnx-task271-observation-20260906`
- Observation window: approximately six minutes, `2026-09-06T01:47:06Z` through `2026-09-06T01:53:00Z`
- Cursor samples: `3084`
- Process samples: `11155`
- Task samples: `36`
- Scheduler contract observed in every task sample: enabled, `PT1M`, managed `pythonw.exe` action and `supervisor tick --execute-safe` arguments.
- Gateway PID: `3948` only; no PID churn observed.
- Ollama PID: `8560` only; no PID churn observed.
- `APPSTARTING`: `8` isolated flags in `7` short runs; no sustained/recurring wave. The longest observed run was approximately `0.12s`.
- `WAIT`: `2` isolated flags, both outside a recurring supervisor process wave.
- Process correlation found only stable Gateway/Ollama runtime identities; no recurring `pythonw.exe`/`host_control` process wave was captured.

The result is accepted as removal of the prior healthy-tick `APPSTARTING` wave pattern, not as proof that every unrelated desktop cursor flag disappears. No cadence change or task disable was attempted.

## Recovery and anomaly separation

- Post-install recovery preflight was read-only and returned `READY`, `stateChanged=false`, with no active provider recovery incident.
- The installer transition closed the previously open `ollama:1` incident with `reason=verified_manual_transition` and `operatorVerified=true`. This is recorded as an installer-owned transition anomaly, not as manual recovery replay, redelivery, disposition, semantic acceptance, or Ticket mutation. No separate recovery command was issued by Hermes.
- No live semantic message, session deletion/reset, manual SQLite/Ticket mutation, provider recovery replay, gateway operation outside the supported installer boundary, Scheduled Task mutation, release promotion, or force push occurred.

## Evidence paths

- Pre-state: `C:\Users\CDQ-P\AppData\Local\Temp\cnx-task271-live-20260906\`
- Install transcript: `...\install-transcript.log`
- Post status: `...\final-cnx-status`, `...\final-openclaw-gateway`, `...\final-supervisor-task-info`
- Installed fingerprint: `...\final-installed-fingerprint-correct`
- Runtime hashes: `...\final-runtime-hashes`
- Cursor/process observation: `C:\Users\CDQ-P\AppData\Local\Temp\cnx-task271-observation-20260906\`

After publication, coordination is handed back to ChatGPT for review. Hermes performs no further mutation.
