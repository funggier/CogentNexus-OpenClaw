# Review — CNX-20260823-018 Remove Wrong-Head Task 017 Worktree

Verdict: `ACCEPT`

## Scope of acceptance

This accepts the Task 018 `BLOCKED_TARGET_DIRTY` report and safety stop only. It does not accept worktree cleanup or provider diagnosis.

## Findings

- The exact target path exists and is registered.
- Its HEAD exactly matches the recorded wrong HEAD `78f6cba4748e59d5975940ca9854961d0e7ff550`.
- The target has exactly three reported tracked deletions.
- A path-filtered process check found one `powershell.exe` record associated with the target.
- No removal, prune, reset, clean, force action, process action, runtime action, source/evidence diagnosis, or unrelated-path inspection occurred.
- Non-force removal was correctly withheld because the clean and no-process gates were not proven.

## Disposition

Do not rerun Task 018 and do not clean or remove the target ad hoc.

Proceed with `CNX-20260823-019`, which may adjudicate only the three named deletions, prove their tracked blobs remain recoverable and identical to durable Git records, re-check exact path use, restore only those exact paths if every preservation gate passes, and then remove only the exact Task 017 worktree using normal non-force Git removal.

Provider diagnosis and any runtime action remain excluded.
