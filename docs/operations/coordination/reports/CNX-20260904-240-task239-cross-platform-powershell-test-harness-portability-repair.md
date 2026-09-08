# CNX-20260904-240 — Task-239 Cross-Platform PowerShell Test Harness Portability Repair

## Authority and scope

- Task: `CNX-20260904-240`
- Mode: `TASK240_TASK239_CROSS_PLATFORM_POWERSHELL_TEST_HARNESS_PORTABILITY_REPAIR`
- Parent: `CNX-20260904-239`
- Fresh authority before final publication: `b95e1f7cfbeed9224d7ff1ef5482ae523425e15e`
- Accepted production repair candidate: `ec29020632091aae3b50149b51303a36fde26310`
- Scope: test-only portability repair
- Production/runtime source and workflows were not modified.

## Existing RED and reproduction boundary

The authoritative existing RED was GitHub Actions Validate run `33830388146` on Task-239 report HEAD `b70606460c6ea3d8d37a3a8317946aa5b1ceec35`:

```text
Windows Python 3.11 = PASS
Windows Python 3.14 = PASS
Ubuntu Python 3.11/3.14 = FAIL
macOS Python 3.11/3.14 = FAIL
```

The proven exception was:

```text
FileNotFoundError: [Errno 2] No such file or directory: 'powershell.exe'
```

The local operator environment is Windows and has `powershell.exe`, so the same failure cannot be reproduced locally without fabricating a missing runtime. The local focused baseline therefore passed; the authoritative cross-platform CI failure was retained as the RED evidence.

## Minimal repair

Changed file:

```text
tests/test_task239_rollover_diagnostics.py
```

The behavioral helper test now:

- resolves `powershell.exe` first on Windows and `pwsh` as fallback;
- resolves `pwsh` first on non-Windows and `powershell` as fallback;
- skips only the runtime-execution subtest when no PowerShell runtime is available;
- preserves all static Task-239 assertions on every platform;
- preserves real PowerShell helper execution on Windows.

No change was made to `scripts/install.ps1`, rollover implementation, plugin payload, runtime/lifecycle code, or workflows.

## Verification

Focused Windows regression:

```text
6 passed in 0.22s
```

Full local Python validation, with the repository's required PyYAML dependency:

```text
508 passed, 5 skipped, 4 subtests passed in 93.90s
```

An initial full local invocation without PyYAML produced only collection errors for missing `yaml`; rerunning with `PyYAML>=6,<7` passed. This was an environment invocation issue, not a code failure.

Additional checks:

```text
git diff --check = PASS
worktree = clean
authoritative candidate plugin fingerprint = 1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f
```

## Exact-SHA GitHub Actions evidence

Final candidate SHA:

```text
18a51b15768fb3d2196e65f1ef470c34aeef7f36
```

Initial runs on this exact SHA:

| Workflow | Run ID | Initial result |
|---|---:|---|
| PS5.1 Acceptance Smoke | `33832755287` | SUCCESS |
| Windows Installer Pack Smoke | `33832755300` | SUCCESS |
| Validate | `33832755313` | FAILURE — macOS 3.11 `npm audit` registry timeout |

The first Validate failure was not a test failure. The failed step was `Run npm audit --omit=dev`; the log records an npm security endpoint timeout and exit code 1. All other Validate matrix jobs completed successfully.

A failed-only corrective rerun was requested for the same run/SHA. The rerun completed successfully:

```text
Validate 33832755313 = SUCCESS
```

Thus all three required workflows have terminal SUCCESS evidence on the exact final SHA:

```text
PS5.1 Acceptance Smoke       33832755287 = SUCCESS
Windows Installer Pack Smoke 33832755300 = SUCCESS
Validate                      33832755313 = SUCCESS (corrective rerun)
```

## Zero-effect ledger

```text
live installer registrations/starts/invocations: 0
live rollover-prepare/finalize: 0
manual plugin mutation: 0
manual controller/Gateway/lifecycle mutation: 0
manual Ticket/outbox/recovery/SQLite writes: 0
Dashboard semantic submissions: 0
Discord semantic submissions: 0
direct Discord/API sends: 0
recovery replay/resend: 0
process termination: 0
provider/model substitution: 0
forensic evidence cleanup/mutation: 0
release/tag/asset mutation: 0
force-push/history rewrite: 0
```

## Disposition

`PASS_TASK240_CROSS_PLATFORM_TEST_HARNESS_PORTABILITY_REPAIRED`

The Task-239 production diagnostic repair remains unchanged and is now covered by a platform-capability-aware test harness. The exact candidate plugin fingerprint is unchanged. No installer retry, live normalization, semantic requalification, release, tag, asset, or force-push action was performed.

STOP for independent review.
