# Coordination Channel Status

**State:** `READY_FOR_HERMES`  
**Execution mode:** `TASK236_TASK235_EXACT_CANDIDATE_WINDOWS_INSTALL_OVER_REQUALIFICATION`  
**Updated:** 2026-09-03 ICT  
**Transport:** GitHub repository / Actions authoritative; Task 236 is installer-only live requalification with zero semantic submission budget  
**Active task:** `CNX-20260903-236`  
**Parent:** `CNX-20260903-235`  
**Installer safety / attestation repair parent:** `CNX-20260902-226`  
**Known-good installer re-entry precedent:** `CNX-20260902-230`  
**Historical installer failure lineage:** `CNX-20260902-223`  
**Parent umbrella:** `CNX-20260831-188`  
**Disposition:** `TASK235_ACCEPTED_PASS__EXACT_CANDIDATE_LIVE_INSTALL_OVER_AUTHORIZED`

## Exact candidate authority

Exact source commit:

`ffb0dd4ed47affe2e496c17b74ca74d358905bd7`

Expected installed plugin payload fingerprint:

`1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`

Public `v0.9.3` remains unchanged at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

Task-235 independent review verdict:

`ACCEPT_PASS_REPOSITORY_TDD_EVIDENCE_CLOSED__CANDIDATE_READY_FOR_LIVE_REQUALIFICATION`

Exact candidate GitHub Actions accepted GREEN:

- Validate `33688878141` — SUCCESS
- Windows Installer Pack Smoke `33688878183` — SUCCESS
- PS5.1 Acceptance Smoke `33688878240` — SUCCESS

## Active Task 236

Execute:

`docs/operations/coordination/tasks/CNX-20260903-236-task235-exact-candidate-windows-install-over-requalification.md`

Required sequence:

```text
fresh repository authority
-> read-only live preflight
-> Delivery/Recovery hazard gate
-> exact candidate install-over
-> installer-owned plugin replacement/rollover if required
-> exact installed fingerprint proof
-> managed convergence/post-install health
-> report
-> STOP for independent review
```

Use exact source candidate `ffb0dd4...` and the installer's temporary `--install-source-commit` contract. Fresh GitHub authority supersedes this summary if newer coordination state appears before execution.

## Installer retry boundary

Before installer execution, only bounded evidence-driven tooling/registration retries defined by Task 236 are authorized.

Once the installer task/process starts:

`INSTALLER_RETRY_GATE=CLOSED`

Then:

```text
installer execution retries: 0
second installer start: 0
second installer invocation: 0
manual plugin repair: 0
```

A rollover/finalizer failure after start is terminal for this task. Collect read-only evidence; do not rerun the installer.

## Live / semantic effect budget

```text
Dashboard human semantic submissions: 0
Discord-origin semantic submissions: 0
direct operator Discord/API Sends: 0
semantic retries/replays: 0
manual durable delivery: 0
manual Ticket/outbox/recovery/SQLite mutation: 0
manual provider/model substitution: 0
manual process termination: 0
manual Gateway/lifecycle repair: 0
manual plugin install/copy/delete/rename/manifest repair: 0
reset: 0
uninstall: 0
fresh reinstall: 0
installer successful start lineage: <= 1
installer invocation lineage: <= 1
installer execution retries after start: 0
Task-223 retained forensic evidence mutation: 0
Release/tag/asset mutation: 0
source/test/workflow production edits: 0
force push/history rewrite: 0
```

Installer-owned plugin replacement/rollover and normal installer-owned lifecycle/convergence are permitted only as required by the one exact-candidate installer invocation.

## PASS requirements

Task 236 must prove, at minimum:

- exact candidate `ffb0dd4...` was the installer source;
- installer terminal success and task result/exit code success;
- installed canonical plugin fingerprint exactly `1ff69c459...`;
- Task-226 fail-closed namespace-ownership repair remains present;
- resulting controller/runtime is coherently managed;
- startup adapter, Supervisor/doctor, Gateway, Ollama/model, Delivery, Recovery, SQLite and process state are healthy/coherent;
- Delivery pending outbox returns to 0;
- no duplicate/recovery replay was introduced;
- Task-223 retained forensic evidence is unchanged;
- any new Task-236 rollover artifacts are separately captured and self-consistent;
- Dashboard semantic submissions = 0;
- direct operator Discord/API Sends = 0;
- installer execution retries after start = 0.

## Stop boundary

Hermes must publish:

`docs/operations/coordination/reports/CNX-20260903-236-task235-exact-candidate-windows-install-over-requalification.md`

Then stop for independent ChatGPT review.

Even on PASS, do not proceed into the one-human Dashboard semantic/durable-delivery test, Discord semantic testing, old-lineage replay/settlement, stale Task-223 cleanup, reset/uninstall/reinstall, or public Release/tag/asset mutation. The semantic acceptance remains a separate successor after Task 236 review.