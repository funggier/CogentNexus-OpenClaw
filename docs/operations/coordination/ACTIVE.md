# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `TASK243_TASK242_HARDENED_SCHEDULED_RUNNER_HARNESS_QUALIFICATION`
Current disposition: `TASK242_ACCEPTED__EXECUTION_CHANNEL_PROVEN__TASK241_RUNNER_CHILD_BOUNDARY_UNRESOLVED__HARDENED_HARNESS_QUALIFICATION_AUTHORIZED`
Task ID: `CNX-20260904-243`
Parent task: `CNX-20260904-242`
Installer parent: `CNX-20260904-241`
Candidate-validation parent: `CNX-20260904-240`
Parent umbrella: `CNX-20260831-188`
Updated: 2026-09-04 ICT
Executor: Hermes / authenticated Windows operator
Coordinator / independent reviewer: ChatGPT

## Accepted Task-242 boundary

Independent review verdict:

`ACCEPT_PASS_HARMLESS_CANARY_PROVES_EXECUTION_CHANNEL__TASK241_SPECIFIC_RUNNER_CHILD_BOUNDARY_UNRESOLVED__HARDENED_RUNNER_HARNESS_QUALIFICATION_REQUIRED`

Reviewed Task-242 report HEAD:

`1420fb8ae3c53deb0f99e1ce20c5192822ae91ba`

Task 242 proved the general Scheduled Task -> Windows PowerShell 5.1 -> durable artifact channel works with one harmless canary:

```text
registration = 1
start = 1
retry = 0
LastTaskResult = 0
artifact = present
identity = CDQ-P\CDQ-P
```

Task 241 remains product-unclassified because its child installer invocation was never durably proven.

## Preserved live boundary

Fresh Windows read-only evidence wins. Retained state remains:

```text
controller = passthrough
generation = 39
candidate plugin not installed
Gateway = READY
provider/model/storage/recovery/delivery = READY
pending outbox = 0
SQLite integrity = ok
```

Retained Task-237 evidence token:

`c6aaf93db7c34f718d01302477a292e1`

Do not mutate or clean it.

## Active Task 243

Execute:

`tasks/CNX-20260904-243-task242-hardened-scheduled-runner-harness-qualification.md`

Required flow:

```text
fresh GitHub authority
-> confirm Task-241 runner evidence weakness
-> build new disposable hardened PowerShell 5.1 runner
-> durable runner-started before child
-> explicit transcript/fallback + stdout/stderr + finally result
-> direct harmless nonzero-child test
-> direct harmless child-launch-exception test
-> one scheduled harmless failure-path canary maximum
-> prove exit-code propagation + durable artifacts
-> prove live state unchanged
-> report
-> STOP for independent review
```

## Harmless qualification budget

```text
Task-243 harmless Scheduled Task registrations: 1 maximum
Task-243 harmless Scheduled Task starts: 1 maximum
scheduled canary retries after start: 0
```

Direct local synthetic-child qualification may be repeated only to correct the new disposable Task-243 harness and must remain product/semantic side-effect free.

## Product zero budget

```text
scripts/install.ps1 invocations: 0
installer Scheduled Task registrations/starts: 0
rollover-prepare/finalize: 0
openclaw plugins install: 0
plugin mutation: 0
controller/Gateway/lifecycle mutation: 0
manual Ticket/outbox/recovery/SQLite writes: 0
```

## Semantic zero budget

```text
Dashboard semantic submissions: 0
Discord semantic submissions: 0
direct Discord/API Sends: 0
semantic retries: 0
recovery replay/resend: 0
```

## Hard fences

No installer retry, reset/uninstall/reinstall, managed-state normalization, product/source/test/workflow edits, historical evidence cleanup, release/tag/asset mutation, process termination, provider/model substitution, or force push/history rewrite.

## Stop boundary

Hermes must publish:

`reports/CNX-20260904-243-task242-hardened-scheduled-runner-harness-qualification.md`

Then stop for independent ChatGPT review. Even on PASS, another installer attempt remains unauthorized until a separate successor explicitly allows it.
