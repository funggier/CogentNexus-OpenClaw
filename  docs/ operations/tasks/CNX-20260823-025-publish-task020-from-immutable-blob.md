# CNX-20260823-025 — Publish Task 020 Report from Immutable Git Blob

Status: READY  
Owner: ChatGPT  
Executor: Codex  
Execution mode: `AUTO`  
Predecessor: `CNX-20260823-024` (`ACCEPT` safe block)

## Objective

Publish the verified Task 020 report from the immutable Git blob object itself. Do not source publication bytes from any checked-out worktree file.

## Immutable source contract

Commit containing object: `2bda9b71952f838da515e046fb3efa10a75f2089`  
Blob: `361be921ae0b70124769d1d8b5a2f33d1b277d88`  
SHA256: `93b06be819c09b56b46352a07c244bf29e76e4c1c7b0bbd2d79cbc76d44c68e9`  
Size: `2795 bytes`  
Lines: `36`  
Destination: `docs/operations/coordination/reports/CNX-20260823-020-isolated-adjudication-and-task017-removal.md`

The accepted Task 023 report also reproduces the full content, but the immutable Git blob object is publication authority.

## Execution control

Use or adopt only:

`C:\Users\CDQ-P\.openclaw\worktrees\cogentnexus-CNX-20260823-025`

It must be the exact registered worktree at freshly fetched coordination HEAD, clean, operation-free, and not in actual process use. A watcher-created exact control worktree may be adopted if all fences match. No fallback or suffix.

## Duplicate fence

After normal fetch, verify ACTIVE is Task 025 / `READY_FOR_CODEX` / `AUTO`, and verify both the destination Task 020 report and matching Task 025 report are absent. Re-fetch and repeat immediately before each push.

## Authorized procedure

1. Verify the source object exists and is type `blob`.
2. Stream/read exact object payload bytes using Git object plumbing such as `git cat-file blob 361be...`; do not read publication bytes from a worktree path and do not apply text/eol conversion.
3. Compute payload SHA256, byte count, and line count; require exact contract match.
4. Materialize only the destination file with exact payload content in the Task 025 control worktree.
5. Verify the indexed/committed destination blob ID equals `361be...` and payload SHA256 remains exact before push.
6. Commit only the destination report with message beginning `report: CNX-20260823-020`, then push normally.
7. Re-fetch remote, resolve the destination blob, and require blob ID and payload SHA256 exact.
8. Publish matching Task 025 report with commands, exit codes, source/destination blob IDs, SHA256, commit SHA, remote verification, and safety accounting.
9. Stop after publication and control-cleanup accounting.

## Results

Return exactly one:

- `PASS_IMMUTABLE_TASK020_BLOB_PUBLISHED`
- `BLOCKED_DESTINATION_ALREADY_EXISTS`
- `BLOCKED_BLOB_OBJECT_MISMATCH`
- `BLOCKED_INDEXED_BLOB_MISMATCH`
- `BLOCKED_CONTROL_COLLISION`
- `BLOCKED_REMOTE_ADVANCED`
- `BLOCKED_PUBLICATION_FAILED`

Include `Human decision required: YES|NO`.

## Prohibited

No publication/ref/push/cherry-pick of commit `2bda9b...` itself; no reading publication bytes from a worktree file; no modification/removal of the Task 020 preserving worktree; no repeated Task 017 cleanup; no force/reset/clean/prune; no process action; no runtime/recovery/provider/`cnx`/OpenClaw/Ollama action; no source/lifecycle/merge/tag/release action.

## Matching report

`docs/operations/coordination/reports/CNX-20260823-025-publish-task020-from-immutable-blob.md`

Commit begins `report: CNX-20260823-025`.
