# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `TASK236_TASK235_EXACT_CANDIDATE_WINDOWS_INSTALL_OVER_REQUALIFICATION`
Current disposition: `TASK235_ACCEPTED_PASS__EXACT_CANDIDATE_LIVE_INSTALL_OVER_AUTHORIZED`
Task ID: `CNX-20260903-236`
Parent task: `CNX-20260903-235`
Installer safety / attestation repair parent: `CNX-20260902-226`
Known-good installer re-entry precedent: `CNX-20260902-230`
Historical installer failure lineage: `CNX-20260902-223`
Parent umbrella: `CNX-20260831-188`
Updated: 2026-09-03 ICT
Executor: Hermes / authenticated Windows operator
Coordinator / independent reviewer: ChatGPT

## Exact candidate authority

Exact source commit:

`ffb0dd4ed47affe2e496c17b74ca74d358905bd7`

Expected installed plugin payload fingerprint:

`1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`

Public `v0.9.3` remains immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

Task-235 independent review:

`reviews/CNX-20260903-235-task234-exact-topology-tdd-evidence-closure-review.md`

Verdict:

`ACCEPT_PASS_REPOSITORY_TDD_EVIDENCE_CLOSED__CANDIDATE_READY_FOR_LIVE_REQUALIFICATION`

Exact candidate Actions accepted GREEN:

- Validate `33688878141` — SUCCESS
- Windows Installer Pack Smoke `33688878183` — SUCCESS
- PS5.1 Acceptance Smoke `33688878240` — SUCCESS

## Active Task 236

Execute:

`tasks/CNX-20260903-236-task235-exact-candidate-windows-install-over-requalification.md`

Required high-level flow:

```text
fresh GitHub authority
-> read-only managed runtime preflight
-> Delivery/Recovery hazard gate
-> exact candidate installer task registration
-> one installer start / one installer invocation maximum
-> installer-owned plugin replacement/rollover if required
-> exact installed fingerprint proof
-> managed convergence + post-install health
-> report
-> STOP for independent review
```

The installer must use exact source candidate `ffb0dd4...`, including the installer contract's temporary `--install-source-commit` override.

## Retry / execution boundary

Before installer execution, bounded evidence-driven registration/tooling retries are permitted only within Task-236 budgets.

As soon as the installer task/process starts:

`INSTALLER_RETRY_GATE=CLOSED`

After that boundary:

```text
installer execution retries: 0
second installer start: 0
second installer invocation: 0
manual plugin repair: 0
```

If installer-owned rollover/finalization fails, collect evidence and stop fail-closed. Do not retry the installer.

## Semantic and direct-effect fence

Task 236 is installer-only.

```text
Dashboard human semantic submissions: 0
Discord-origin semantic submissions: 0
direct operator Discord/API Sends: 0
semantic retries/replays: 0
manual durable delivery: 0
manual Ticket/outbox/recovery/SQLite mutation: 0
reset/uninstall/fresh reinstall: 0
manual provider/model substitution: 0
manual process termination: 0
manual Gateway/lifecycle repair: 0
manual plugin install/copy/delete/rename/manifest repair: 0
Task-223 retained forensic evidence mutation: 0
Release/tag/asset mutation: 0
source/test/workflow production edits: 0
force push/history rewrite: 0
```

Installer-owned plugin replacement/rollover and normal installer-owned lifecycle/convergence operations are allowed only as required by this exact candidate installation.

## Stop boundary

Hermes must publish:

`reports/CNX-20260903-236-task235-exact-candidate-windows-install-over-requalification.md`

Then stop for independent ChatGPT review.

Even after PASS, do **not** perform the one-human Dashboard semantic/durable-delivery turn. That acceptance effect remains a separate successor after Task 236 is independently accepted.