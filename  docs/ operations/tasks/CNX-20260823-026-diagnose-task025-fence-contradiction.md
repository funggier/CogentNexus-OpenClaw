# CNX-20260823-026 — Diagnose Task 025 Control and Duplicate-Fence Contradiction

Status: READY  
Owner: ChatGPT  
Executor: Codex  
Execution mode: `AUTO`  
Predecessor: `CNX-20260823-025` (`REWORK`)

## Objective

Perform a strictly read-only diagnosis of why Task 025 reported the Task 020 destination absent at fetched HEAD `a67515d46927da5b2565d91a6a4bbec532e82aba` even though GitHub records that destination at the same commit as blob `6c165d6f970cd4bc745aa2df83d6500d0be3e059`, and why the exact Task 025 control worktree was registered at unexpected HEAD `5dbf0425ed42f23da95ba3fa25ecbc57893f1d92`.

## Durable facts

- Coordination branch: `agent/v0.9.3-recovery-reality-tests`.
- Task 025 fetched HEAD: `a67515d46927da5b2565d91a6a4bbec532e82aba`.
- Current report commit: `ee545d47e36fb820473b9f92e617f074482cf0ac`.
- The compare from `a67515d...` to `ee545d...` is one commit and adds only the Task 025 report.
- At `a67515d...`, destination `docs/operations/coordination/reports/CNX-20260823-020-isolated-adjudication-and-task017-removal.md` exists as blob `6c165d6f970cd4bc745aa2df83d6500d0be3e059` and contains the earlier blocked Task 020 report.
- Accepted immutable PASS source remains blob `361be921ae0b70124769d1d8b5a2f33d1b277d88`; no publication is authorized in this task.
- Exact Task 025 control path: `C:\Users\CDQ-P\.openclaw\worktrees\cogentnexus-CNX-20260823-025`.
- Task 025 report-publication path: `C:\Users\CDQ-P\.openclaw\worktrees\CNX-20260823-025-report`.

## Execution control

The watcher-created Task 026 worktree may be used only as a clean read-only control after verifying it is registered at freshly fetched coordination HEAD and operation-free. Do not create a fallback worktree. Do not adopt, edit, remove, or clean either Task 025 path.

## Required evidence

1. Fetch the coordination branch normally and record exact fetched HEAD.
2. Verify ACTIVE is Task 026 / `READY_FOR_CODEX` / `AUTO` and the matching Task 026 report is absent.
3. From explicit repository root and explicit commit `a67515d...`, record:
   - `git cat-file -e <commit>:<destination>` exit code;
   - resolved blob ID;
   - byte count, line count, and SHA256 of that blob;
   - first heading and Status/Primary result fields.
4. Record the exact commands, current directory, repository common-dir/top-level, ref/commit, and path used by Task 025's duplicate-fence check if recoverable from shell history, report artifacts, logs, reflog, or Git metadata. If not recoverable, state `NOT_RECORDED`; do not infer.
5. For unexpected commit `5dbf0425ed42f23da95ba3fa25ecbc57893f1d92`, record object type, parent(s), tree, subject, full changed-path list, local and remote reachability, and whether it contains either Task 020 or Task 025 report path.
6. For both Task 025 paths, record registration, HEAD, porcelain status, operation markers, branch/detached state, and read-only process-use evidence. Do not read unrelated user files.
7. Compare all findings and classify the contradiction without changing any state.

## Results

Return exactly one:

- `PASS_FENCE_CONTRADICTION_DIAGNOSED`
- `BLOCKED_REQUIRED_GIT_OBJECT_MISSING`
- `BLOCKED_CONTROL_IDENTITY_UNSAFE`
- `BLOCKED_EVIDENCE_INCOMPLETE`

Include `Human decision required: YES|NO`.

## Prohibited

No report replacement or publication; no worktree creation except watcher-provided Task 026 control; no worktree removal, prune, reset, clean, restore, checkout, commit, ref creation, cherry-pick, or force action; no process action; no runtime/recovery/provider/`cnx`/OpenClaw/Ollama action; no lifecycle, merge, tag, or release action.

## Matching report

`docs/operations/coordination/reports/CNX-20260823-026-diagnose-task025-fence-contradiction.md`

Commit begins `report: CNX-20260823-026`.
