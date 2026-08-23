# CNX-20260823-032 — Diagnose Recurring Task 027 Materialization Loss

Status: `PASS_CAUSE_NOT_PROVEN_SAFE_NEXT_DIAGNOSTIC_DEFINED`

Repository: `funggier/CogentNexus-OpenClaw`
Branch: `agent/v0.9.3-recovery-reality-tests`
Primary: `C:\Users\CDQ-P\.openclaw\workspace`
Target: `C:\Users\CDQ-P\.openclaw\worktrees\cogentnexus-CNX-20260823-027`
Target HEAD: `748b6e7accb22b6bb4a5503c9ac04265f153f9e5` (detached, registered)

## Evidence and commands

- `git fetch origin --prune` — exit 0.
- Matching report duplicate check — exit 128; report absent at fetched HEAD.
- Target identity/registration/common repository checks — exit 0; common dir is `C:\Users\CDQ-P\.openclaw\workspace\.git`.
- Current target status/counts — exit 0: 387 indexed, 5 materialized, 382 absent, status count 382. Canonical absent-list SHA256 `6A078DA7D54615B67E0020D978A065171E803B0A0DFE134CE978BB2616B91FB8`, exactly matching Task 029/031 evidence.
- Target administrative metadata — target directory last write `2026-08-23 09:39:57Z`; worktree index last write `2026-08-23 09:38:48Z` (observed read-only).
- Process inventory — read-only. ChatGPT/Codex processes are present; filtered Git status processes were observed, but no process command line referenced the exact Task027 path or a removal/materialization command. No process was stopped or acted on.
- Scheduled-task inventory — read-only. `CogentNexus Supervisor` is `Ready` and invokes `C:\DATAstore\Python\Python3-14-3\pythonw.exe` with `C:\Users\CDQ-P\.openclaw\workspace\skills\cogentnexus\scripts\host_control_v092.py --root C:\Users\CDQ-P\.openclaw\workspace\.cogent supervisor tick --execute-safe`. This is a correlation candidate only; the task action does not contain the exact Task027 path.
- Source search of `host_control_v092.py` — exit 1 for exact Task027/materialization tokens; only generic route/cleanup/restore-native references were found. No direct proof of this worktree being deleted.
- Windows TaskScheduler operational events — `NOT_AVAILABLE` (no matching events); Security log — `NOT_AVAILABLE` (unauthorized access). Auditing was not enabled or changed.
- Stability observation — read-only 60 seconds: T0 `2026-08-23T12:29:38Z`, T30 `12:30:08Z`, T60 `12:30:38Z`; all samples status 382, absent 382, canonical hash unchanged. No transition or actor correlation occurred.

## Conclusion

The recurring state is confirmed and exactly matches prior evidence, but the actor/mechanism and time boundary are not proven. The scheduled `CogentNexus Supervisor` is a plausible correlation candidate because it is enabled/Ready and runs a safe supervisor tick, but process presence and generic source references do not establish that it removed these files. No direct command, event record, or log tying it to Task027 was available.

Proven: exact target identity, recurring 382-path pattern, no sparse/identity drift observed, current stable absence, process/task inventory results, and unavailable event-log limitations.

Unproven: deletion actor, deletion time boundary, whether the supervisor or Codex watcher caused it, and any filesystem watcher mechanism.

## Narrow remediation manifest (proposed, not executed)

- Evidence-supported cause: `CAUSE_NOT_PROVEN`.
- Current actor state: `CogentNexus Supervisor` is registered `Ready`; no matching process was proven active at the sample, and the Codex Scheduled task remains active.
- Safe containment candidate: ChatGPT may authorize a separate task to pause only the identified `CogentNexus Supervisor` scheduled task and/or the Codex coordination watcher, but this diagnostic did not change either. Capture task state, trigger, and target counts immediately before/after containment.
- Restoration candidate: a separate reviewed task may repeat exact-path restoration only after containment and a fresh 387/387 precondition; preserve absent-set/status hashes and verify no re-loss during a bounded observation.
- Required evidence before either action: exact task identity, current target registration, process inventory, before/after status hashes, and explicit confirmation of which watcher is being paused.

Human decision required: NO.

Side-effect accounting: read-only inspection only; no file/index/timestamp/config/ref/worktree mutation; no process or scheduled-task action; no runtime/provider/lifecycle action; no restoration repeated; no force push. Only mutation was publication of this matching report.