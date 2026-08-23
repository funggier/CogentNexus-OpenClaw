# CNX-20260823-033 — Complete Recurring Materialization-Loss Evidence

Status: `PASS_SINGLE_NEXT_DIAGNOSTIC_DEFINED`

Repository: `funggier/CogentNexus-OpenClaw`
Branch: `agent/v0.9.3-recovery-reality-tests`
Primary: `C:\Users\CDQ-P\.openclaw\workspace`
Target: `C:\Users\CDQ-P\.openclaw\worktrees\cogentnexus-CNX-20260823-027`
Target HEAD: `748b6e7accb22b6bb4a5503c9ac04265f153f9e5` detached; common dir `C:\Users\CDQ-P\.openclaw\workspace\.git`

## Evidence artifacts

All artifacts were written outside the repository under task-specific `%TEMP%\cnx033` and were read-only captures. SHA256:

- `identity.txt` `8C96768B20BD4D7206AC7C9E355C37F4C4763DC985F1E86B7A50831D61DE28D2`
- `config.txt` `5E7EDD90C9308AB0E0D5D266235FD1E1BB05AE86086789EF63509E6F15162FAF`
- `worktrees.txt` `3270C3FDFD1D9780CB2D4FBACAAAE13630415EA9FB78B46F1F0CAB8784027083`
- `survivors.txt` `0D36E460AC7980F6C0CD2F5047A95FB3F96EDD0CE791838F66BFD33C285DC42E`
- `processes.txt` `8752BFDA5EC686869A0DF72A37C9E25AFED9F02BE6C077BB53A41890BB40FAD8`
- `scheduled-task.txt` `032D5EEF3040F5144DC1A09BC52166D74E7F62DB63BEDF182ACF44060CBA7EA0`
- `codex-automation.txt` `F0A65A5C954A7DB8A9C48AE10A54B6E5877EB6F657A69EB9E0CC7C60EB5DD106`
- `events.txt` `CDC9ED0BCE602DC56F3C78FD342ED31DAA32662FAA34EBEDB7345CBFF566CE62`
- `artifacts.txt` `EB33A0C865F7BBB77358BA7926C7D5E747A579C43D61DB5A596A399AD3935C2B`

## Observations

- Fresh preflight and duplicate fence passed (matching report absent, checks exit 0/128 respectively).
- Current state is exactly recurring pattern: 387 indexed, 5 materialized, 382 absent; canonical absent-list SHA256 `6A078DA7D54615B67E0020D978A065171E803B0A0DFE134CE978BB2616B91FB8`.
- All five surviving tracked paths were enumerated with byte length, creation/write UTC metadata, and SHA256 in `survivors.txt`. Representative absent parent and target/admin/index metadata were captured in the identity/worktree artifacts.
- Sparse/config/flags/operation markers were captured. No sparse-checkout or worktree-specific config, and no active merge/rebase/cherry-pick/revert/bisect/index lock was observed.
- Filtered process inventory captured PID, PPID, executable, start time, and command line. ChatGPT/Codex and Git status processes were present, but no process command line referenced the exact Task027 path or a deletion/materialization command.
- Exact scheduled candidate: `CogentNexus Supervisor`, state `Ready`, action `C:\DATAstore\Python\Python3-14-3\pythonw.exe "C:\Users\CDQ-P\.openclaw\workspace\skills\cogentnexus\scripts\host_control_v092.py" --root "C:\Users\CDQ-P\.openclaw\workspace\.cogent" supervisor tick --execute-safe`. The action does not contain the Task027 path. Codex automation is separately active every minute against the workspace.
- TaskScheduler Operational channel query over UTC window `2026-08-23T04:44:00Z` to capture time returned no matching entries; Security channel returned `NOT_AVAILABLE` due unauthorized access. Auditing was not enabled or changed.
- Authorized artifact search under `.openclaw` for exact Task027 references in filtered log/json/toml/ps1/py files returned no matching records. No unrelated user content or secrets were read.

## UTC timeline and inference

- Task030 report commit: `2026-08-23T09:41:16Z`; target directory/admin index metadata were around `09:38:48Z–09:39:57Z` during the restored state.
- Task031 report commit: `2026-08-23T10:03:15Z`; it recorded the target back at 5/387 and the exact path absent.
- Task032 60-second stability window: `12:29:38Z–12:30:38Z`, unchanged at 382 absent with the accepted hash.
- Task033 capture: current target remained 5/387; no event or process evidence narrows the deletion boundary further.

These timestamps establish recurrence and a broad boundary, not causation. Neither Supervisor nor Codex watcher is directly implicated.

## Single next diagnostic target

`CAUSE_NOT_PROVEN`. The one recommended next target is a bounded, read-only filesystem I/O trace focused only on `C:\Users\CDQ-P\.openclaw\worktrees\cogentnexus-CNX-20260823-027` and its 382 absent tracked paths, capturing delete/rename/create initiator PID and UTC timestamps during a controlled observation. Do not change Supervisor or Codex watcher, restore files, enable auditing, or alter runtime state until that trace exists. This is an evidence-acquisition diagnostic, not containment.

Human decision required: NO.

Side-effect accounting: no file/index/timestamp/config/ref/worktree/process/task/watcher/audit/runtime mutation; no restoration or containment; no repeated side effect. The only mutation was publication of this matching report.