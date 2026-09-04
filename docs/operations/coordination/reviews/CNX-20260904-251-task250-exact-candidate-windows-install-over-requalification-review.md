# CNX-20260904-251 — Independent Review

## Verdict

`ACCEPT_BLOCKED_EVIDENCE__ONE_SHOT_BOUNDARY_RESPECTED__SCHEDULER_EXECUTION_LIMIT_TERMINATION_PROVEN__INSTALLER_CHILD_STAGE_UNPROVEN__READ_ONLY_TIMEOUT_FORENSIC_REQUIRED`

## Reviewed authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`
- Reviewed report HEAD: `be6be78760fa1071ba2d4749db5ecd20025ac312`
- Reviewed report: `docs/operations/coordination/reports/CNX-20260904-251-task250-exact-candidate-windows-install-over-requalification.md`
- Exact candidate: `9c3c4e0fe0afbedf9233c25c0dd36e4209fb9d96`
- Expected installed plugin fingerprint: `1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`
- Public `v0.9.3`: `26ce64a624255278a3a0266ad38746e0e6ed2e31` unchanged.

Fresh compare from the pre-execution coordination HEAD `44c63eeca34508d94af088ea8cf1be733b613cf7` to the report HEAD contains one report-only commit and no product/source/test/workflow drift.

Report-head Actions are terminal SUCCESS:

- PS5.1 Acceptance Smoke `33905872979`
- Windows Installer Pack Smoke `33905872955`
- Validate `33905872866`

## Adjudication

The Task-251 source/hazard gates were passed sufficiently to authorize the single live attempt. The exact candidate was bound through a detached checkout and manifest-bound runner. The successful Scheduled Task registration count was one, installer start count was one, installer invocation count was one, and installer retry after start was zero.

The run is not an installer PASS and is not classifiable as a Task-250 attestation mismatch. The child was observed starting at `2026-09-04T17:22:05.7455411Z`, but no terminal runner result, child stdout/stderr, or complete transcript was retained. The Scheduled Task remained Running until its configured execution limit and then returned Ready with `LastTaskResult=267014 (0x41306)`.

Therefore the strongest supported conclusion is:

```text
Scheduled Task execution-limit termination = proven by retained Task-251 evidence
child process started = proven
child terminal exit code = unproven
last installer stage reached = unproven
plugin-rollover-prepare reached = unproven
Task-250 diagnostic= emission = unproven
candidate installed = not proven; postflight remains predecessor identity
managed convergence = not achieved/proven
```

The absence of terminal runner artifacts after forced task termination is an observability boundary, not evidence that the installer itself returned a specific failure. No second product execution is authorized from this evidence.

## Safety / cardinality review

Accepted:

```text
successful installer task registration = 1
installer successful starts = 1
installer invocations = 1
installer retries after start = 0
manual product repair = 0
manual process termination = 0
semantic submissions = 0
recovery replay/resend = 0
release/tag mutation = 0
```

Postflight remained passthrough generation 39 with predecessor plugin identity, Ollama selected, Gateway healthy, Delivery READY/pending 0, Recovery READY, and SQLite integrity OK. Historical Task-223/233/248/249 evidence was reported preserved.

## Required successor

Before any further installer attempt, perform a separate read-only forensic task to determine the last provable child stage and why the process exceeded the scheduler execution limit.

Required evidence includes:

1. exported Task-251 Scheduled Task XML/settings, especially exact `ExecutionTimeLimit`, action, arguments, principal, and termination policy;
2. exact Task-251 run duration and Scheduler operational events proving start/termination reason;
3. complete inventory and hashes of the Task-251 evidence root, runner, manifest, observer logs, and any start markers;
4. static inspection of the runner's child stdout/stderr persistence semantics, including whether child output is buffered until terminal completion and therefore lost on external process termination;
5. bounded Windows PowerShell/TaskScheduler/process-creation evidence for the Task-251 window;
6. read-only inventory of installer-owned residues created during the run: workspace `install-backups`, `install-staging`, external `plugin-generation-rollover-backups`, rollover transactions/inventories, and relevant timestamps;
7. classify any new rollover backup as absent, partial, or complete without modifying it;
8. current process inventory to prove whether any Task-251 child survived the scheduler termination;
9. no installer/prepare/finalize rerun and no cleanup/repair.

If evidence identifies the last stage/root cause, report it and stop. If static evidence remains insufficient, the successor should recommend a separate harmless/synthetic runner instrumentation qualification rather than retrying the live installer blindly.

## Stop boundary

Installer retry and Dashboard/Discord semantic acceptance remain unauthorized pending the successor forensic report and independent review.
