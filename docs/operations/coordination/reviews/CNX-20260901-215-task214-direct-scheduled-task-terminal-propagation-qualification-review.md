# Independent Review — CNX-20260901-215 Direct Scheduled Task Terminal Propagation Qualification

## Verdict

`ACCEPT_WITH_DURATION_DEVIATION__DIRECT_TERMINAL_PROPAGATION_PROVEN__INSTALLER_REQUALIFICATION_AUTHORIZED`

Task 215 proves the central launcher property required after Tasks 212–214: a Windows Scheduled Task whose action directly owns one PowerShell process can survive independently of the Hermes observer, persist durable progress/terminal evidence, and propagate the process exit code to Task Scheduler.

The report's literal `PASS_DIRECT_SCHEDULED_TASK_TERMINAL_PROPAGATION` is narrowed because two task-spec details were not met exactly:

- the direct script's own timestamps prove `55.1713166` seconds from `DIRECT_START` to `DIRECT_END`, while Phase B requested at least 65 seconds;
- the registered `ExecutionTimeLimit` was `PT3M`, while Phase C requested at least five minutes.

These are evidence-contract deviations and must not be silently normalized. They do not invalidate the proven terminal-propagation mechanism because the direct process remained sustained, produced 11 heartbeats, reached `DIRECT_END`, persisted intended exit code `23`, and Task Scheduler independently reported `LastTaskResult=23` with one start and no retry. The 60-second Scheduler sample is not used to rewrite the direct script's 55.17-second elapsed time; Scheduler finalization can lag the script's own terminal timestamp.

## Accepted facts

- Task-215 temporary task was registered once and started once.
- Action was direct `powershell.exe -File <direct.ps1>` with no wrapper, nested PowerShell, `Popen`, detached flags, or shell relay.
- Exact direct PowerShell PID `3460` and executable identity were captured.
- Durable `DIRECT_START`, heartbeat records `n=1..11`, and `DIRECT_END` were persisted.
- `intended-exit-code.txt` contained `23` before process exit.
- Scheduler reached non-running/Ready state and `LastTaskResult=23`.
- `NumberOfMissedRuns=0`; no retry/second run was reported.
- Exact temporary task was unregistered and proved absent.
- Product state was preserved: PASSTHROUGH, generation 33, old live fingerprint `f82674172a3946e00ddcb3a94fd14c8476bf91abc11ed7d44b5fa53acb74eaf1`, Gateway healthy, delivery/recovery READY, no product process residue.
- No CogentNexus installer/lifecycle/plugin/SQLite/provider/model/Discord mutation occurred.

## Interpretation

Task 213 proved the detached Python launcher was incompatible with this executor. Task 214 proved Scheduled Task launch but failed at wrapper -> child terminal propagation. Task 215 removes that nested boundary and proves direct Scheduled Task terminal propagation.

Repeating another harmless 65-second qualification would add little safety relative to the remaining objective. The successor may therefore use the qualified **direct Scheduled Task-owned PowerShell process** as the execution boundary for the real installer, provided it corrects the duration-setting deviation by using an execution time limit of at least 30 minutes and captures installer terminal/provenance evidence independently.

## Successor constraints

A successor installer task must:

1. use a freshly verified exact Task-207 candidate checkout/source boundary at `27fe0181b3b65d555a3b0cc8354f6f7945c21c0b`;
2. re-prove the safe ordinary-upgrade preflight before mutation;
3. register one uniquely named temporary installer Scheduled Task with `RestartCount=0`, no recurrence, demand start only, and execution time limit >=30 minutes;
4. keep one top-level Scheduled Task-owned PowerShell process; no detached PowerShell/Python launcher and no nested PowerShell child;
5. invoke the exact candidate `scripts/install.ps1` at most once in that same PowerShell process;
6. durably capture runner start/end/result plus installer transcript/output containing all seven diagnostic stage pairs and final success/failure evidence;
7. require Scheduler terminal `LastTaskResult=0` for success;
8. independently prove installed fingerprint `d0677581d60d3d5535c65e3261dae6f50d7aeb245b8680adac0cace4c040643b`, plugin enabled/loaded, ownership exact, MANAGED runtime healthy, OpenClaw pinned, delivery/recovery healthy, SQLite integrity `ok`;
9. unregister only the exact temporary installer task after terminal evidence is captured;
10. perform no Discord Send. Semantic Discord acceptance remains a separate successor.

## Disposition

`ACCEPT_WITH_DURATION_DEVIATION__DIRECT_TERMINAL_PROPAGATION_PROVEN__INSTALLER_REQUALIFICATION_AUTHORIZED`
