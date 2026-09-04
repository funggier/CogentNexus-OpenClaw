# Coordination Channel Status

**State:** `READY_FOR_HERMES`  
**Execution mode:** `TASK237_TASK236_SOURCE_BINDING_CONTRACT_CORRECTION_EXACT_CANDIDATE_WINDOWS_INSTALL_OVER_REQUALIFICATION`  
**Updated:** 2026-09-04 ICT  
**Transport:** GitHub repository / Actions authoritative; Task 237 corrects source binding only and remains installer-only with zero semantic submission budget  
**Active task:** `CNX-20260904-237`  
**Parent:** `CNX-20260903-236`  
**Repository/TDD parent:** `CNX-20260903-235`  
**Installer safety / attestation repair parent:** `CNX-20260902-226`  
**Known-good exact-source installer precedent:** `CNX-20260902-230`  
**Historical installer failure lineage:** `CNX-20260902-223`  
**Parent umbrella:** `CNX-20260831-188`  
**Disposition:** `TASK236_BLOCKER_ACCEPTED__COORDINATION_SOURCE_BINDING_CONTRACT_CORRECTED__LIVE_INSTALL_OVER_REAUTHORIZED`

## Exact candidate authority

Exact source commit:

`ffb0dd4ed47affe2e496c17b74ca74d358905bd7`

Expected installed plugin payload fingerprint:

`1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`

Public `v0.9.3` remains unchanged at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

Task-236 report disposition:

`BLOCKED_PREFLIGHT_DRIFT`

Task-236 independent review verdict:

`ACCEPT_BLOCKED_PREFLIGHT_DRIFT__COORDINATION_SOURCE_BINDING_CONTRACT_DEFECT_CONFIRMED__SUCCESSOR_REQUIRED`

The blocker was not an installer/product failure. Task 236 required a nonexistent source-commit parameter and correctly stopped before any registration/start/mutation. Installer invocation count and semantic effect count remained zero.

## Correct source-binding rule

Task 237 must not pass `--install-source-commit` / `-InstallSourceCommit`.

Instead:

```text
fresh-fetch repository
-> materialize disposable detached checkout exactly at ffb0dd4...
-> prove exact HEAD + clean worktree + candidate fingerprint
-> invoke scripts/install.ps1 directly from that exact checkout
```

This matches the source-binding topology already proven by Task 230 and requires no production source change.

## Active Task 237

Execute:

`docs/operations/coordination/tasks/CNX-20260904-237-task236-source-binding-contract-correction-exact-candidate-windows-install-over-requalification.md`

Required sequence:

```text
fresh repository authority
-> exact detached source-binding proof
-> read-only live preflight
-> Delivery/Recovery hazard gate
-> exact candidate install-over
-> installer-owned plugin replacement/rollover if required
-> exact installed fingerprint proof
-> managed convergence/post-install health
-> report
-> STOP for independent review
```

## Installer retry boundary

Before execution, only bounded evidence-driven registration/tooling retries defined by Task 237 are authorized.

Once the installer task/process starts:

`INSTALLER_RETRY_GATE=CLOSED`

Then:

```text
installer execution retries: 0
second installer start: 0
second installer invocation: 0
manual plugin repair: 0
manual lifecycle repair: 0
```

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
Task-233 replay/settlement/deletion: 0
Release/tag/asset mutation: 0
production/source/test/workflow edits: 0
force push/history rewrite: 0
```

Installer-owned plugin replacement/rollover and normal installer-owned lifecycle/convergence are permitted only as required by the single exact-candidate installer invocation.

## PASS requirements

Task 237 must prove at minimum:

- exact detached checkout HEAD is `ffb0dd4...` and clean immediately before installer registration/start;
- source plugin fingerprint is `1ff69c459...`;
- exact checkout's `scripts/install.ps1` is the invoked installer;
- installer terminal success / exit code 0 / task result 0 where applicable;
- installed canonical plugin fingerprint exactly `1ff69c459...`;
- Task-226 fail-closed namespace-ownership repair remains present;
- controller/runtime converges coherently to managed;
- startup adapter, Supervisor/doctor, Gateway, Ollama/model, Delivery, Recovery, SQLite and process state are healthy/coherent;
- Delivery pending outbox = 0;
- no duplicate/recovery replay is introduced;
- Task-223 and Task-233 retained evidence remains preserved;
- Dashboard semantic submissions = 0;
- direct operator Discord/API Sends = 0;
- installer execution retries after start = 0.

## Stop boundary

Hermes must publish:

`docs/operations/coordination/reports/CNX-20260904-237-task236-source-binding-contract-correction-exact-candidate-windows-install-over-requalification.md`

Then stop for independent ChatGPT review.

Even on PASS, do not proceed into the one-human Dashboard semantic/durable-delivery acceptance, Discord semantic testing, old-lineage replay/settlement, historical-evidence cleanup, reset/uninstall/reinstall, or public Release/tag/asset mutation without a separate successor.