# CNX-20260905-253 — Task-252 Streaming Diagnostic Runner TDD Qualification

## Authority and scope

Fresh authority was fetched from `origin/agent/v0.9.3-full-stabilization` before implementation. Active task was `CNX-20260905-253-task252-streaming-diagnostic-runner-tdd-qualification.md`, `READY_FOR_HERMES`. Public immutable tag remained `v0.9.3 = 26ce64a624255278a3a0266ad38746e0e6ed2e31`.

This task was repository/test-only. No live installer, installer Scheduled Task, rollover, runtime/database operation, semantic submission, or release operation was performed.

## TDD lineage

The test-only RED commit was:

`bb66b67ff9fe5dec344a59b4d130e0d2a55988d2`

It changed only `tests/test_task253_manifest_streaming_runner.py`. The exact RED command was:

```text
PYTHONPATH=. pytest -q tests/test_task253_manifest_streaming_runner.py
```

RED result:

```text
5 failed in 16.60s
```

The failures were attributable to the absent streaming runner: no live markers, no normal terminal result, no launch-failure result, and no argument-binding execution. Windows PowerShell 5.1 was present; this was not a capability skip or malformed test environment.

The implementation commit and final candidate are:

`cc35ce506b6a9ffee3223ec79ddb0373a898e4a5`

Only this production file was added:

`scripts/manifest-streaming-runner.ps1`

## Runner contract

The runner accepts `-LaunchManifest` and `-EvidenceRoot`, freezes manifest and runner SHA-256 identities, writes `runner-started.json` before launch, and creates empty stdout/stderr artifacts before launching the target.

The final PS5.1-compatible transport uses direct `.NET Process` for runner lifecycle and a `cmd.exe` redirection boundary for the manifest-bound target. The target executable and exact quoted argument vector are retained in the start metadata; stdout and stderr are redirected by the operating system to the precreated evidence files, so emitted bytes are visible while the target remains alive. Delayed `!ERRORLEVEL!` preserves normal nonzero exit status and maps command-not-found `9009` to `child_launch_exception`.

The runner records child-start metadata immediately after launching the redirection transport, including UTC time, PID, target executable identity, manifest SHA-256, runner SHA-256, and transport identity. The recorded PID is the `cmd.exe` redirection launcher PID; the manifest target path/arguments are recorded separately. This distinction is explicit rather than presenting the launcher PID as the target process PID.

## Focused GREEN evidence

Exact command:

```text
PYTHONPATH=. pytest -q tests/test_task253_manifest_streaming_runner.py
```

Final result:

```text
5 passed in 3.69s
```

Covered cases:

1. stdout marker `STDOUT_MARKER_A` and stderr marker `STDERR_MARKER_B` were visible before the synthetic child exited;
2. after terminating only the disposable runner, both pre-kill markers remained durable;
3. normal nonzero completion preserved exact exit code `23` and both streams;
4. invalid executable was classified as `child_launch_exception`, distinct from child exit `23`/success;
5. an argument path containing spaces arrived exactly at the synthetic child.

Durable focused evidence was retained under:

`C:/Users/CDQ-P/AppData/Local/CogentNexus-OpenClaw/forensics/CNX-20260905-253/pytest/`

Forced-termination evidence:

- `test_forced_outer_termination_0/evidence/child-stdout.txt`: `17` bytes, SHA-256 `569e1cf0bd1b351541210f1607716877bca7f67c6039bc2c091b04c67c715178`
- `test_forced_outer_termination_0/evidence/child-stderr.txt`: `17` bytes, SHA-256 `c2ae6ed25614f02ddafb1afdf8fe05f97a8ff753f18542b8b77db1e0978313c0`
- pre-kill `runner-started.json`: `343b28cfe0dbf63cbaaadd9605edc12d2ac51669a69b27512a49ad0ebc64ac55`
- `child-started.json`: `9f5acfaa8d57e4f38a5b22c13b9f980f873a5d3f1decc9eeb63f45e8bfc7ab51`
- no terminal result is required for the forced outer-kill case; the test proves the already-emitted stream bytes survive.

## Full validation

- Full Python suite: `516 passed, 5 skipped, 4 subtests passed in 78.20s`
- Production plugin audit: `found 0 vulnerabilities`
- PowerShell parser: `PS_PARSE=PASS`
- `git diff --check`: PASS
- Plugin fingerprint unchanged and independently recomputed:
  `1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`
- `scripts/install.ps1` SHA-256 unchanged:
  `c0779d9bae69d850a44073134e7799a48a1856935b09aae1ae8c7da9f57e0629`

## Exact-SHA Actions

Candidate SHA:

`cc35ce506b6a9ffee3223ec79ddb0373a898e4a5`

Terminal success was verified from GitHub Checks API:

- `validate (windows-latest, 3.11)`: success, job `101231503981`
- `validate (windows-latest, 3.14)`: success, job `101231503898`
- `validate (ubuntu-latest, 3.11)`: success, job `101231503890`
- `validate (ubuntu-latest, 3.14)`: success, job `101231503891`
- `validate (macos-latest, 3.11)`: success, job `101231503956`
- `validate (macos-latest, 3.14)`: success, job `101231503919`
- Windows Installer Pack Smoke job `npm-pack`: success, job `101231503769`, run `33938651860`
- package dry-run: success, job `101231503756`
- PS5.1 Acceptance Smoke job `serializer`: success, job `101231503736`, run `33938651855`

The check-run names are job names; the corresponding workflow display names are `Windows Installer Pack Smoke` and `PS5.1 Acceptance Smoke`.

## Effect ledger

All prohibited live effects were zero:

- live `scripts/install.ps1` invocations: `0`
- live installer task registrations/starts: `0`
- rollover prepare/finalize: `0`
- live plugin or backup mutation: `0`
- controller/Gateway/provider/model lifecycle mutation: `0`
- Ticket/outbox/recovery/SQLite mutation: `0`
- Dashboard/Discord/direct API semantic sends: `0`
- recovery replay/resend: `0`
- release/tag/history mutation: `0`
- force-push: `0`

Synthetic child processes used only the disposable test harness and did not invoke OpenClaw, CogentNexus runtime, Gateway, installer, or production databases.

## Final disposition

`PASS_STREAMING_DIAGNOSTIC_RUNNER_TDD_QUALIFIED`

The streaming diagnostic runner is qualified for a future separately authorized live successor. This PASS does not authorize installer execution, rollover, semantic acceptance, recovery actions, or release operations.

STOP for independent ChatGPT review.
