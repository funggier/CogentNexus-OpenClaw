# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `TASK237_TASK236_SOURCE_BINDING_CONTRACT_CORRECTION_EXACT_CANDIDATE_WINDOWS_INSTALL_OVER_REQUALIFICATION`
Current disposition: `TASK236_BLOCKER_ACCEPTED__COORDINATION_SOURCE_BINDING_CONTRACT_CORRECTED__LIVE_INSTALL_OVER_REAUTHORIZED`
Task ID: `CNX-20260904-237`
Parent task: `CNX-20260903-236`
Repository/TDD parent: `CNX-20260903-235`
Installer safety / attestation repair parent: `CNX-20260902-226`
Known-good exact-source installer precedent: `CNX-20260902-230`
Historical installer failure lineage: `CNX-20260902-223`
Parent umbrella: `CNX-20260831-188`
Updated: 2026-09-04 ICT
Executor: Hermes / authenticated Windows operator
Coordinator / independent reviewer: ChatGPT

## Exact candidate authority

Exact source commit:

`ffb0dd4ed47affe2e496c17b74ca74d358905bd7`

Expected installed plugin payload fingerprint:

`1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`

Public `v0.9.3` remains immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

Task-236 report:

`reports/CNX-20260903-236-task235-exact-candidate-windows-install-over-requalification.md`

Task-236 independent review:

`reviews/CNX-20260903-236-task235-exact-candidate-windows-install-over-requalification-review.md`

Review verdict:

`ACCEPT_BLOCKED_PREFLIGHT_DRIFT__COORDINATION_SOURCE_BINDING_CONTRACT_DEFECT_CONFIRMED__SUCCESSOR_REQUIRED`

Task 236 consumed zero installer/product/semantic mutation budget. The blocker was the coordination task's invented source-commit argument, not a production installer defect.

## Corrected Task-237 source binding

Do not pass `--install-source-commit` / `-InstallSourceCommit`.

Use:

```text
fresh fetch
-> disposable detached checkout at exact ffb0dd4...
-> prove exact HEAD + clean checkout + exact plugin fingerprint
-> invoke that checkout's scripts/install.ps1 directly
```

This is the exact-source topology proven by Task 230.

## Active Task 237

Execute:

`tasks/CNX-20260904-237-task236-source-binding-contract-correction-exact-candidate-windows-install-over-requalification.md`

Required high-level flow:

```text
fresh GitHub authority
-> exact detached source-binding proof
-> read-only live preflight
-> Delivery/Recovery hazard gate
-> exact candidate installer task registration
-> one installer start / one installer invocation maximum
-> installer-owned plugin replacement/rollover if required
-> exact installed fingerprint proof
-> managed convergence + post-install health
-> report
-> STOP for independent review
```

## Retry / execution boundary

Before installer execution, only bounded evidence-driven registration/tooling retries within Task-237 budgets are allowed.

As soon as the installer task/process starts:

`INSTALLER_RETRY_GATE=CLOSED`

After that:

```text
installer execution retries: 0
second installer start: 0
second installer invocation: 0
manual plugin repair: 0
manual lifecycle repair: 0
```

## Semantic and direct-effect fence

Task 237 remains installer-only.

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
Task-233 replay/settlement/deletion: 0
Release/tag/asset mutation: 0
production/source/test/workflow edits: 0
force push/history rewrite: 0
```

Installer-owned plugin replacement/rollover and normal installer-owned lifecycle/convergence are allowed only as required by the single exact-candidate installer invocation.

## Stop boundary

Hermes must publish:

`reports/CNX-20260904-237-task236-source-binding-contract-correction-exact-candidate-windows-install-over-requalification.md`

Then stop for independent ChatGPT review.

Even after PASS, do **not** perform the one-human Dashboard semantic/durable-delivery turn. That remains a separate successor after Task 237 is independently accepted.