# Coordination Channel Status

**State:** `READY_FOR_HERMES`  
**Execution mode:** `TASK244_TASK243_HARDENED_RUNNER_EXACT_CANDIDATE_WINDOWS_INSTALL_OVER_REQUALIFICATION`  
**Updated:** 2026-09-04 ICT  
**Transport:** GitHub repository / Actions authoritative; Task 244 authorizes one exact-candidate live installer attempt through a freshly regenerated, hashed, directly-qualified, frozen hardened runner; semantic budget remains zero  
**Active task:** `CNX-20260904-244`  
**Parent:** `CNX-20260904-243`  
**Installer evidence parent:** `CNX-20260904-241`  
**Runner forensic parent:** `CNX-20260904-242`  
**Candidate-validation parent:** `CNX-20260904-240`  
**Parent umbrella:** `CNX-20260831-188`  
**Disposition:** `TASK243_ACCEPTED__HARDENED_RUNNER_FUNCTIONALLY_QUALIFIED__FRESH_RUNNER_REGENERATION_GATE_REQUIRED__ONE_SHOT_INSTALLER_REQUALIFICATION_AUTHORIZED`

## Task-243 accepted result

Reviewed report HEAD:

`ad94e992fec3cbf414bf82a3dd5073b229e6b5b8`

Independent review verdict:

`ACCEPT_PASS_HARDENED_RUNNER_FUNCTIONALLY_QUALIFIED__PRECREATE_REGISTRATION_CORRECTION_ACCEPTED__RUNNER_SHA_REPORT_GAP_NONBLOCKING_WITH_FRESH_REGENERATION_GATE__SEPARATE_BOUNDED_INSTALLER_REQUALIFICATION_AUTHORIZED`

Task 243 proved a hardened disposable runner can durably capture both a synthetic child nonzero exit and a child-launch exception, and can propagate a deterministic exit code through Task Scheduler with one successful registration and one start.

The failed first registration method in Task 243 created no task (`TaskPresent=false`) and was accepted as a pre-start tooling correction. The report did not record the qualified runner SHA, so Task 244 must regenerate and persist a fresh runner identity rather than reuse temp state.

## Exact executable candidate

```text
candidate SHA = 18a51b15768fb3d2196e65f1ef470c34aeef7f36
plugin fingerprint = 1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f
public v0.9.3 = 26ce64a624255278a3a0266ad38746e0e6ed2e31 (immutable)
```

Task 244 must fresh-prove the exact candidate's three required Actions before live mutation.

## Active Task 244

Execute:

`docs/operations/coordination/tasks/CNX-20260904-244-task243-hardened-runner-exact-candidate-windows-install-over-requalification.md`

Required flow:

```text
fresh GitHub authority + exact-candidate Actions
-> detached exact source
-> fresh read-only live inventory
-> derive installer classifier/resolver path
-> new unique hardened runner/evidence root
-> persist runner source + SHA
-> direct synthetic nonzero + launch-exception qualification
-> byte-identical rehash and freeze
-> one installer Scheduled Task registration with CDQ-P\CDQ-P
-> one installer start
-> hardened evidence classification
-> if exit 0, exact plugin/rollover/runtime/DB postflight
-> report
-> STOP for independent review
```

## One-shot installer budget

```text
successful installer Scheduled Task registrations: 1 maximum
installer Scheduled Task starts: 1 maximum
installer child invocations: 1 maximum
installer retries after start: 0
```

If installer task registration fails before creation, prove `TaskPresent=false` and stop; no second installer registration is allowed in Task 244.

## Preserved evidence

Fresh Windows inventory wins. Do not assume old live plugin/rollover state.

Retained Task-237 backup token:

`c6aaf93db7c34f718d01302477a292e1`

Do not mutate or clean historical Task-223/237/241/242/243 evidence.

## Semantic zero-effect budget

```text
Dashboard semantic submissions: 0
Discord semantic submissions: 0
direct Discord/API sends: 0
semantic retries: 0
recovery replay/resend: 0
```

## Hard fences

No reset/uninstall/reinstall sequence, second installer attempt, manual plugin replacement, manual rollover prepare/finalize, manual controller/Gateway/lifecycle normalization, manual Ticket/outbox/recovery/SQLite writes, provider/model substitution, process termination to coerce outcome, historical evidence cleanup, release/tag/asset mutation, force push/history rewrite, or semantic message.

## Stop boundary

Hermes must publish:

`docs/operations/coordination/reports/CNX-20260904-244-task243-hardened-runner-exact-candidate-windows-install-over-requalification.md`

Then stop for independent ChatGPT review. Semantic requalification remains a separate successor even if installer PASSes.
