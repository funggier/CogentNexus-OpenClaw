# CNX-20260904-243 — Independent Review

## Reviewed report

`docs/operations/coordination/reports/CNX-20260904-243-task242-hardened-scheduled-runner-harness-qualification.md`

Reviewed report HEAD:

`ad94e992fec3cbf414bf82a3dd5073b229e6b5b8`

## Verdict

`ACCEPT_PASS_HARDENED_RUNNER_FUNCTIONALLY_QUALIFIED__PRECREATE_REGISTRATION_CORRECTION_ACCEPTED__RUNNER_SHA_REPORT_GAP_NONBLOCKING_WITH_FRESH_REGENERATION_GATE__SEPARATE_BOUNDED_INSTALLER_REQUALIFICATION_AUTHORIZED`

## Findings

Task 243 functionally qualifies the hardened operator runner/evidence contract.

Direct qualification proved both required failure paths:

- synthetic child nonzero: durable `runner-started`, stdout, stderr, transcript, `runner-result`, `childStarted=true`, and exact propagated exit code `37`;
- synthetic child launch exception: durable `runner-started`, explicit `child_launch_exception`, `childStarted=false`, exception capture, fallback log, and `runner-result` from `finally`.

Scheduled qualification then proved one successfully-created harmless task, one start, zero starts after the first start, zero post-start retries, durable stdout/stderr/result artifacts, and coherent `LastTaskResult=37`.

The first registration method failed before task creation with `0x80070057`; Task 243 then proved `TaskPresent=false` before using a materially different fully-qualified principal method. I accept that event as a safe pre-start tooling correction under the established retry policy rather than as a second successful Scheduled Task registration. No product, semantic, or runtime side effect was possible from the failed pre-creation attempt.

The product/semantic zero-effect ledger is internally consistent with the report: installer invocations `0`, installer task starts `0`, plugin/runtime/DB/semantic mutations `0`, and the live controller remained `passthrough`, generation `39`, with gateway/provider/model/storage/recovery/delivery read-only checks READY.

## Evidence-quality note

Task 243 required the hardened runner path **and SHA**, but the report records the path/design and runtime evidence without recording the hardened runner SHA-256. That is a reproducibility/reporting gap.

It does not invalidate the behavioral qualification, but it means a successor must not assume that an old temporary runner is authoritative or even still present. In particular, temp content may disappear between tasks.

Therefore any live installer successor must:

1. create a fresh unique evidence root and fresh hardened runner;
2. record the complete runner bytes/source and SHA-256 before any installer action;
3. direct-qualify that exact runner with harmless synthetic nonzero and launch-exception fixtures;
4. freeze the runner bytes after qualification;
5. use that byte-identical runner for the single installer Scheduled Task attempt;
6. stop before product execution if the fresh runner cannot be qualified exactly.

## GitHub / Actions interpretation

The executable candidate remains:

`18a51b15768fb3d2196e65f1ef470c34aeef7f36`

with plugin fingerprint:

`1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`

Fresh Actions for that exact executable SHA remain GREEN for the required three workflows.

The Task-243 coordination authority SHA `8df79e1d3121b5bc659a9f3b0b3b212a4ee1ff2a` later completed Validate as FAILURE only because multiple matrix jobs timed out at `npm audit --omit=dev`; Python, plugin tests, installer syntax/self-tests, build, and evaluation had already passed in those jobs. The report-head SHA is docs-only relative to that authority; PS5.1 Acceptance Smoke and Windows Installer Pack Smoke are SUCCESS while Validate was still in progress at review time. These network audit failures do not establish a Task-243 harness or product regression and do not supersede the exact executable candidate's all-GREEN Actions.

## Authorization boundary

Task 243 itself did not authorize an installer retry. This review authorizes opening a **separate** bounded live installer requalification task only.

That successor must preserve:

- exact source candidate `18a51b15768fb3d2196e65f1ef470c34aeef7f36`;
- candidate plugin fingerprint `1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`;
- retained Task-237 backup token `c6aaf93db7c34f718d01302477a292e1`;
- Task-241/242/243 evidence;
- zero semantic-send budget;
- one successful installer Scheduled Task registration maximum;
- one installer Scheduled Task start maximum;
- one installer child invocation maximum;
- zero retry after installer start.

A fresh live preflight must re-prove the current installed/plugin/rollover state and re-derive the expected installer state-machine path before execution. No current live state should be assumed from this review.
