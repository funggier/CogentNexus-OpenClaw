# CNX-20260905-254 — Independent Review

## Verdict

`ACCEPT_PASS_TARGET_CHILD_IDENTITY_BINDING_TDD_REPAIRED__DURABLE_STREAMING_FORENSIC_BOUNDARY_QUALIFIED__ONE_SHOT_LIVE_INSTALL_REQUALIFICATION_AUTHORIZED_SEPARATELY`

## Reviewed authority

- Task: `docs/operations/coordination/tasks/CNX-20260905-254-task253-target-child-identity-binding-tdd-repair.md`
- Report: `docs/operations/coordination/reports/CNX-20260905-254-task253-target-child-identity-binding-tdd-repair.md`
- Report HEAD: `6fe7e19f22ac586120be351e0ef68e658bf5642e`
- Opening coordination HEAD: `cc4d062efe62ce1effed8a63e6dc49759391b1fb`
- Final executable candidate: `6822af464fe7a5cb3f93305d0263dfc86b56ac68`

## TDD adjudication

The final ancestry is valid and minimal:

```text
cc4d062... opening authority
-> e09c2e8335aeec7ce43ee88a7907c0f8faaabc57 TEST-ONLY RED
-> 6822af464fe7a5cb3f93305d0263dfc86b56ac68 production repair
-> 6fe7e19f22ac586120be351e0ef68e658bf5642e report only
```

The RED commit changes only `tests/test_task253_manifest_streaming_runner.py` and directly exposes the Task253 defects:

- recorded PID differs from target self-reported PID;
- invalid target leaves target-start evidence;
- the `cmd.exe` transport contaminates argument binding with shell/redirection semantics.

Reported RED was `3 failed, 2 passed`, for the intended contract failures.

The production repair changes only `scripts/manifest-streaming-runner.ps1`. It removes `cmd.exe` indirection and starts the manifest executable directly through `System.Diagnostics.Process`.

## Contract verification

The repaired runner now satisfies the forensic identity boundary required by Task254:

- `child-started.json` is written only after direct target `Process.Start()` succeeds;
- `child-started.json.pid` is the direct target process PID;
- executable identity in the same artifact is the manifest target executable;
- invalid executable produces `child_launch_exception`, `childStarted=false`, and no target `child-started.json`;
- stdout/stderr remain incrementally durable while the target is alive;
- already-emitted output and target-start evidence survive forced outer-runner termination;
- normal child nonzero exit `23` remains exact;
- argument binding covers spaces, apostrophe, and a literal quote;
- synthetic target cleanup is PID-bound and deterministic.

Focused GREEN is reported as `5 passed in 3.04s` and full Python validation as `516 passed, 5 skipped, 4 subtests passed`.

## Exact candidate gates

Exact candidate `6822af464fe7a5cb3f93305d0263dfc86b56ac68` has terminal SUCCESS on all required workflows:

- Validate — run `33944299263`
- Windows Installer Pack Smoke — run `33944299239`
- PS5.1 Acceptance Smoke — run `33944299258`

All nine observed check-runs on the exact SHA are terminal `success`.

Identity proofs recorded by Task254:

```text
streaming runner SHA-256 = 729fba4552e28cd6f53e62f10c8f3bd098d5ca5dfb8d0e3bf4ba3ba1a6250f3e
scripts/install.ps1 SHA-256 = c0779d9bae69d850a44073134e7799a48a1856935b09aae1ae8c7da9f57e0629
plugin fingerprint = 1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f
```

The public `v0.9.3` tag remains immutable at `26ce64a624255278a3a0266ad38746e0e6ed2e31`.

## Nonblocking security observation

Task254 separately reports two pre-existing high-severity findings in root tooling dependencies (`git` / `mime`) with no available fix, while the production plugin-scope audit is clean and the exact candidate's required Actions are green. This is not evidence of a Task254 regression and does not block the bounded live requalification successor.

## Effect ledger adjudication

Task254 remained repository/test-only. No live installer, installer Scheduled Task, rollover, live plugin/tree mutation, controller/Gateway/provider/model/DB mutation, semantic send, replay, release/tag mutation, or force-push was performed.

## Successor authorization boundary

A separate live successor may perform one exact-candidate installer requalification using the repaired streaming runner as the evidence boundary.

The successor MUST NOT treat a longer Task Scheduler execution limit as a fix. Preserve the known `PT45M` limit for the first requalification so that any repeated stall is diagnosed through incrementally durable stdout/stderr and target PID evidence rather than hidden by a timeout increase.

The successor must retain:

```text
installer task registration <= 1
installer task start <= 1
scripts/install.ps1 invocation <= 1
retry after start = 0
semantic sends = 0
```

If the installer terminates, stalls, or hits the scheduler limit, STOP and preserve the streaming evidence; do not retry. If the Task250 attestation mismatch recurs, preserve the exact `diagnostic=` hash-input/per-path evidence and STOP.
