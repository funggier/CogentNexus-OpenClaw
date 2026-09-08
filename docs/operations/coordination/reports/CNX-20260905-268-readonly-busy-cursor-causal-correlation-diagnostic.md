# CNX-20260905-268 — Read-only Busy-Cursor Causal Correlation Diagnostic

## Disposition

**STRONG_CAUSAL_MATCH — supervisor process wave and APPSTARTING cursor transitions align repeatedly.**

This is a read-only causal-correlation result. It does not authorize deployment, recovery disposition, session mutation, or any live acceptance action.

## Authority and scope

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`
- Task: `CNX-20260905-268`
- Evidence root: `C:\Users\CDQ-P\AppData\Local\Temp\cnx-task268-cursor-correlation-20260906`
- Remote branch was freshly fetched before capture and the local worktree was re-anchored to the fetched remote commit before report preparation.
- Capture used only read-only Win32 APIs, WMI/CIM process queries, and Scheduled Task metadata queries.
- No input was injected, no window or cursor configuration was changed, and no live service/provider/task/database/session state was mutated.

## Capture evidence

| Evidence | Result |
|---|---|
| `cursor-samples.json` | 3,079 high-frequency cursor samples, approximately 100 ms cadence |
| `process-samples.json` | 11,389 process rows, approximately 1-second snapshots |
| `task-samples.json` | 36 Scheduled Task metadata samples, approximately 10-second cadence |
| `meta.json` | Capture counts and completion metadata |
| `provider-final.log` | Read-only provider status |
| `recovery-final.log` | Read-only recovery status |
| `status-final.log` | Read-only CNX/Gateway/ticket status |
| `action-audit` search result | Source/installed/runtime windowless-execution audit |

The first diagnostic harness run had a PowerShell `$PID` variable collision and was not used for causal conclusions. The harness was corrected in the temporary evidence directory and rerun successfully for the complete required window.

## Cursor observations

The valid rerun captured:

- 3,079 samples over approximately six minutes: `2026-09-05T17:42:17.9277506Z` through `2026-09-05T17:48:17.8538648Z`.
- Standard WAIT cursor comparison: `0` samples.
- Standard APPSTARTING cursor comparison: `414` samples.
- APPSTARTING transitions: `6` distinct runs, one at each natural minute tick:

| Tick | APPSTARTING start | APPSTARTING end | Duration |
|---:|---|---|---:|
| 1 | `17:43:00.481706Z` | `17:43:08.613170Z` | `8.131s` |
| 2 | `17:44:00.464262Z` | `17:44:08.582612Z` | `8.118s` |
| 3 | `17:45:00.525293Z` | `17:45:08.571858Z` | `8.047s` |
| 4 | `17:46:00.490145Z` | `17:46:08.753749Z` | `8.264s` |
| 5 | `17:47:00.470187Z` | `17:47:08.624907Z` | `8.155s` |
| 6 | `17:48:00.562861Z` | `17:48:08.717600Z` | `8.155s` |

The cursor handle was `0x1001B` during APPSTARTING and `0x10005` outside those runs. The captured foreground window was overwhelmingly `classFoxitReader` (3,066 of 3,079 samples in the final analysis), with only brief Chrome/task-switcher observations. This indicates that the cursor transition occurred while the existing foreground application remained in place; it was not explained by a foreground application switch.

## Process and Scheduled Task correlation

The supervisor Scheduled Task remained enabled with:

- repetition interval: `PT1M`
- action executable: product-owned `pythonw.exe`
- action: `host_control_v092.py ... supervisor tick --execute-safe`
- task metadata sampled 36 times; state was predominantly ready/running during query observations.

Across the same six-minute window:

- supervisor-related rows: `290`
- gateway-status-related rows: `186`
- process creation waves appeared once per minute and overlapped each APPSTARTING start, with supervisor process creation and child command chains beginning within the same approximately 10-second wave.
- Gateway process PID `23596` remained stable for the full process window.
- Ollama process PID `8560` remained stable for the full process window.
- No Gateway or Ollama restart was observed.

The observed tree included product-owned `pythonw.exe` supervisor/runtime processes and short-lived `cmd.exe`/`node.exe` `gateway status` children. The source/runtime audit found `CREATE_NO_WINDOW` in the relevant Python subprocess paths, while the registered Scheduled Task action uses `pythonw.exe` and the task is hidden. The observed cursor correlation therefore implicates the **supervisor wave as a whole**, including its child status-command activity, not conclusively one specific executable.

`conhost.exe` was present in the broad process snapshots, but the capture also included the diagnostic/terminal environment and did not establish that every `conhost.exe` row belonged to the supervisor tree. It is therefore not treated as an independent causal attribution.

## Classification rationale

The task contract defines `STRONG_CAUSAL_MATCH` when WAIT/APPSTARTING transitions repeatedly align with the supervisor wave for at least four natural ticks with tight latency and are absent from comparable off-cycle periods.

This capture satisfies that threshold for APPSTARTING:

- six of six natural PT1M ticks aligned with an APPSTARTING transition;
- each transition began within approximately 0.5 seconds of the minute boundary;
- no APPSTARTING cursor state was observed in the off-cycle samples;
- foreground identity remained substantially unchanged;
- Gateway and Ollama remained stable, excluding a service restart as the observed trigger.

The evidence does not distinguish whether the visible symptom is caused by the hidden `pythonw.exe` supervisor itself, the child `gateway status` command chain, or their combined Windows shell/window-manager interaction. A source repair task is required for that narrower attribution.

## Secondary state checks

Fresh read-only checks during/after capture reported:

- Ollama selected/desired: `ollama` / `running`
- Ollama endpoint reachable/healthy/ready: `true` / `true` / `true`
- Ollama models: `4`
- provider transition: `null`
- recovery verdict: `READY_WITH_WARNINGS`
- recovery incident: `ollama:1`
- circuit open: `true`
- recovery allowed: `false`
- recovery attempts: `3/3`
- Gateway healthy and listening on loopback `127.0.0.1:18789`
- pending outbox: `0`
- accepted tickets: `1`

The open recovery incident, unresolved Ticket/recovery boundary, and installed-vs-candidate mismatch remain separate blockers. Task268 did not dispose, replay, cancel, recover, deploy, or mutate them.

## Hard-fence ledger

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

## Required next step

Set coordination state to `WAITING_FOR_CHATGPT_REVIEW` and stop project mutation. Any follow-up repair must separately authorize a source-level fix and its tests. Exact-candidate deployment, recovery-incident disposition, old Ticket handling, live session succession, and semantic acceptance remain unauthorized by Task268.

Credentials and secret values are not included in this report.
