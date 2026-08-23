# CNX-20260823-034 — Trace Task027 Filesystem I/O and Audit Deletion-Capable Source

Status: `PASS_SOURCE_CAPABILITY_MAPPED_NO_ACTOR`

Repository: `funggier/CogentNexus-OpenClaw`
Branch: `agent/v0.9.3-recovery-reality-tests`
Primary: `C:\Users\CDQ-P\.openclaw\workspace`
Target: `C:\Users\CDQ-P\.openclaw\worktrees\cogentnexus-CNX-20260823-027`
Target HEAD: `748b6e7accb22b6bb4a5503c9ac04265f153f9e5` detached; common dir `C:\Users\CDQ-P\.openclaw\workspace\.git`

## Preflight

`git fetch origin --prune` exit 0. Matching report duplicate check exit 128 (absent). Target identity/count/status checks exit 0: 387 indexed, 5 materialized, 382 absent, status 382, canonical absent SHA256 `6A078DA7D54615B67E0020D978A065171E803B0A0DFE134CE978BB2616B91FB8`.

## Trace tool discovery

Read-only `Get-Command` inventory: `procmon` and `procmon64` NOT_FOUND; `wpr`, `logman`, and `PktMon` installed. No already-installed facility was available with a safe exact-path filesystem create/write/delete/rename filter without enabling policy or requiring an unapproved configuration/elevation. No trace was started, no audit/policy was enabled, and no software was installed or downloaded. Trace result: `TRACE_TOOL_NOT_AVAILABLE`.

## Source audit

Current fetched branch was searched read-only with `git grep` for deletion, cleanup, reset/restore/checkout/worktree operations, exact target patterns, and supervisor entry points.

- `skills/cogentnexus/scripts/lifecycle_v092.py` (`reset`, around line 240; `uninstall`, around lines 338–340): `shutil.rmtree(root)` and owned-path `shutil.rmtree`/`unlink`. Classification: `CAPABLE_NOT_REACHABLE_FOR_TARGET`; these operate on the supplied Cogent runtime root or uninstall-owned paths, not `.openclaw\\worktrees\\cogentnexus-CNX-20260823-027`. No worktree construction or target path appears in the call chain.
- `skills/cogentnexus/scripts/host_control_v092.py` (`stop`/`disable` helpers): provider-adapter cleanup and native-route restoration through the supplied runtime root. Classification: `NOT_DELETION_CAPABLE` for the Task027 worktree; no worktree path or recursive worktree deletion.
- `skills/cogentnexus/templates/supervisor/windows-task.xml` and supervisor templates: configured entry point invokes `supervisor tick --execute-safe` with a runtime `--root`; classification: `CAPABLE_CONFIGURED_NOT_OBSERVED` only for supervisor runtime behavior, with no worktree cleanup operation or exact target construction.
- `scripts/clean-reinstall.ps1`: `Remove-Item -Recurse -Force` is scoped to explicitly owned `.cogent`, skill, launcher, and extension paths under its supplied workspace; classification: `CAPABLE_NOT_REACHABLE_FOR_TARGET`. It is not a scheduled supervisor path and does not name Task027/worktrees.
- `scripts/accept-*`, install/test scripts, and `skills/cogentnexus/scripts/cogent.py` temporary cleanup matches: classification `NOT_DELETION_CAPABLE` for the target because paths are task temp files/fixtures or runtime state, not the registered Git worktree.
- No source match constructed `cogentnexus-CNX-`, `.openclaw\\worktrees`, or the exact Task027 path. No `git worktree remove/prune`, `git clean`, `git reset`, or broad checkout/restore call was found in the searched source scope.

A source capability without trace/log evidence is not classified as `CAPABLE_AND_RUNTIME_OBSERVED`.

## Evidence artifacts

Read-only captures were stored outside the repository under `%TEMP%\\cnx033` during this task. SHA256:

- identity `8C96768B20BD4D7206AC7C9E355C37F4C4763DC985F1E86B7A50831D61DE28D2`
- config `5E7EDD90C9308AB0E0D5D266235FD1E1BB05AE86086789EF63509E6F15162FAF`
- worktrees `3270C3FDFD1D9780CB2D4FBACAAAE13630415EA9FB78B46F1F0CAB8784027083`
- survivors `0D36E460AC7980F6C0CD2F5047A95FB3F96EDD0CE791838F66BFD33C285DC42E`
- processes `8752BFDA5EC686869A0DF72A37C9E25AFED9F02BE6C077BB53A41890BB40FAD8`
- scheduled task `032D5EEF3040F5144DC1A09BC52166D74E7F62DB63BEDF182ACF44060CBA7EA0`
- Codex automation `F0A65A5C954A7DB8A9C48AE10A54B6E5877EB6F657A69EB9E0CC7C60EB5DD106`
- events `CDC9ED0BCE602DC56F3C78FD342ED31DAA32662FAA34EBEDB7345CBFF566CE62`
- artifact search `EB33A0C865F7BBB77358BA7926C7D5E747A579C43D61DB5A596A399AD3935C2B`

## Correlation and conclusion

No filesystem I/O trace, event log entry, or process command line directly identified a delete/rename initiator for the Task027 path. The configured `CogentNexus Supervisor` remains only a configured runtime entry point; source capability is not target reachability and is not runtime attribution. The recurring 382-path absence therefore remains unexplained by available evidence.

Proven: target identity, recurring materialization state, trace-facility availability result, deletion-capable source locations and scopes, configured supervisor entry point, and absence of direct actor evidence.

Unproven: actor PID, deletion timestamp, filesystem operation sequence, and any causal link from Supervisor/Codex watcher to Task027.

Human decision required: NO.

Side-effect accounting: no restoration/materialization; no target/index/timestamp/config/ref/worktree mutation; no process/task/watcher/Supervisor action; no audit enablement; no runtime/provider/lifecycle action; no software install/download; no repeated side effect. The only repository mutation was publication of this matching report.