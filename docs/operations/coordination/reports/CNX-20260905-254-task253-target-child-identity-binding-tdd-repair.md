# CNX-20260905-254 — Task-253 Target Child Identity Binding TDD Repair

## Fresh authority

At task opening, `origin/agent/v0.9.3-full-stabilization` was fetched and re-read. Remote coordination HEAD was `cc4d062efe62ce1effed8a63e6dc49759391b1fb`, with `ACTIVE.md` and `STATUS.md` both declaring `READY_FOR_HERMES` and Task254 active. The authority was:

`docs/operations/coordination/tasks/CNX-20260905-254-task253-target-child-identity-binding-tdd-repair.md`

Public tag immutability was checked against remote:

`v0.9.3 = 26ce64a624255278a3a0266ad38746e0e6ed2e31`

Task253's independent review correctly rejected its PASS as a live forensic boundary because the recorded PID belonged to the `cmd.exe` launcher rather than the manifest target and invalid targets could leave `child-started.json`.

Task254 remained repository/test-only. No installer, installer Scheduled Task, rollover, runtime, database, semantic, release, or force-push operation was authorized or performed.

## Strict TDD lineage

### RED

Test-only RED commit:

`e09c2e8335aeec7ce43ee88a7907c0f8faaabc57`

The commit changed only:

`tests/test_task253_manifest_streaming_runner.py`

Exact RED command:

```text
PYTHONPATH=. pytest -q tests/test_task253_manifest_streaming_runner.py
```

Captured output is retained at:

`C:/Users/CDQ-P/AppData/Local/Temp/cnx254-red.txt`

RED result:

```text
3 failed, 2 passed in 3.95s
```

The failures were the required identity defects on Task253's candidate: `child-started.pid` was `21396` while the synthetic target self-reported `17100`; invalid target left `child-started.json`; and the quote-edge argument vector included redirection tokens. The failure was not a platform skip or malformed environment.

### Minimal repair

Production repair commit:

`6822af464fe7a5cb3f93305d0263dfc86b56ac68`

Changed production file:

`scripts/manifest-streaming-runner.ps1`

The repair replaces `cmd.exe` indirection with direct `System.Diagnostics.Process` target creation. The runner creates stdout/stderr files and `runner-started.json` before launch, attaches a compiled static .NET stdout/stderr event sink, starts the manifest executable directly, and writes `child-started.json` only after `Process.Start()` succeeds. Its `pid` is `$proc.Id`, the actual target process PID. Launch exceptions do not create target child-start evidence. The Windows argument quoting routine preserves literal quote/backslash edge cases. Existing terminal exit and outcome classifications remain fail-closed.

No `scripts/install.ps1`, ownership/backup/transaction, plugin payload, lifecycle/provider/model, delivery, or release file was changed.

## Focused GREEN and durable evidence

Exact final-candidate command:

```text
PYTHONPATH=. pytest -q tests/test_task253_manifest_streaming_runner.py --basetemp C:/Users/CDQ-P/AppData/Local/CogentNexus-OpenClaw/forensics/CNX-20260905-254/pytest
```

Result:

```text
5 passed in 3.04s
```

Durable evidence root:

`C:/Users/CDQ-P/AppData/Local/CogentNexus-OpenClaw/forensics/CNX-20260905-254/pytest`

The suite proves:

- synthetic target self-reported PID equals `child-started.json.pid`;
- target executable identity matches the manifest executable;
- no `child-started.json` exists for an invalid executable;
- stdout and stderr markers are visible while the target remains alive;
- after only the disposable outer runner is terminated, emitted stdout/stderr and the already-proven target artifact remain;
- normal target exit code `23` and `childStarted=true` remain exact;
- launch failure remains `child_launch_exception` with `childStarted=false`;
- a path containing spaces, an apostrophe, and a literal quote are delivered exactly;
- the target/runner process tree is deterministically cleaned using the self-reported target PID.

The forced-termination case uses only synthetic disposable processes. It does not invoke OpenClaw, CogentNexus, the installer, Gateway, or a production database.

## Full validation

- Full Python suite: `516 passed, 5 skipped, 4 subtests passed in 76.19s`
- PowerShell parser: `PS_PARSE=PASS`
- Production plugin-scope `npm audit --omit=dev --audit-level=high`: exit `0`, no findings
- Root repository audit: separately reported `2 high severity vulnerabilities` in existing `git`/`mime` dependencies, both with `No fix available`; this is a pre-existing tooling dependency result and not in the production plugin scope. It was not hidden and did not alter source.
- `git diff --check`: PASS
- Installer SHA-256 unchanged:
  `c0779d9bae69d850a44073134e7799a48a1856935b09aae1ae8c7da9f57e0629`
- Final streaming runner SHA-256:
  `729fba4552e28cd6f53e62f10c8f3bd098d5ca5dfb8d0e3bf4ba3ba1a6250f3e`
- Expected unchanged plugin fingerprint:
  `1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`

## Exact-SHA GitHub Actions

Final candidate SHA:

`6822af464fe7a5cb3f93305d0263dfc86b56ac68`

All nine observed check-runs reached terminal `success` on this exact SHA:

| Check/job | Check-run ID | Check-suite ID | Conclusion |
|---|---:|---:|---|
| `npm-pack` | `101247485728` | `91991149874` | success |
| `package dry-run (no publish)` | `101247485892` | `91991149951` | success |
| `serializer` | `101247485787` | `91991149941` | success |
| `validate (macos-latest, 3.11)` | `101247486008` | `91991149951` | success |
| `validate (macos-latest, 3.14)` | `101247486052` | `91991149951` | success |
| `validate (ubuntu-latest, 3.11)` | `101247486003` | `91991149951` | success |
| `validate (ubuntu-latest, 3.14)` | `101247486019` | `91991149951` | success |
| `validate (windows-latest, 3.11)` | `101247486029` | `91991149951` | success |
| `validate (windows-latest, 3.14)` | `101247486055` | `91991149951` | success |

The workflow display names for `npm-pack` and `serializer` are `Windows Installer Pack Smoke` and `PS5.1 Acceptance Smoke`, respectively. Run/job identities were kept separate; no release workflow was dispatched.

## Hard-fence effect ledger

All prohibited live effects remained zero:

- live `scripts/install.ps1` invocations: `0`
- installer Scheduled Task registrations/starts: `0`
- rollover prepare/finalize: `0`
- live plugin, retired-tree, or rollover-backup mutation: `0`
- controller/Gateway/provider/model/DB mutation: `0`
- Ticket/outbox/recovery/SQLite mutation: `0`
- Dashboard/Discord/direct API semantic sends: `0`
- recovery replay/resend: `0`
- release/tag mutation: `0`
- force-push/history rewrite: `0`

Repository changes were limited to the authorized runner test and runner implementation, followed by this report. Synthetic processes were confined to the focused test harness and were cleaned deterministically.

## Final disposition

`PASS_TARGET_CHILD_IDENTITY_BINDING_TDD_REPAIRED`

The runner now binds durable child-start evidence to the actual manifest target process while retaining incremental stdout/stderr and forced-termination preservation. This PASS does not authorize live installer requalification or semantic acceptance; a separate successor task is required.

STOP for independent ChatGPT review.
