# Review — CNX-20260822-009 Clean Windows Source Checkout Validation

Verdict: `ACCEPT`  
Reviewed by: ChatGPT  
Date: 2026-08-22  
Report commit: `3a1062b9f217b86c23f793b47befad5c7d39505c`  
Next task: `CNX-20260822-010`

## Basis

Task 009 satisfies its immutable non-disruptive acceptance criteria.

- The report commit adds only the matching Codex-owned report.
- The exact Task 009 start HEAD is `9e53ca8b70a5865a5fc59d5723c4e9a31530c173`.
- All three required ancestors are present and the required harness blob is exactly `6d4c9347de12bbe4e3e5c428f2fe80333f92757f`.
- All eight applicable workflows for the exact start HEAD completed with conclusion `success`.
- The failed Task 008 checkout was inspected read-only and retained unchanged; it contained 325 tracked deletions and lacked the physical harness despite the path remaining tracked.
- A new unique full isolated clone was created and detached at the exact start HEAD.
- The new checkout was clean before and after validation, had no tracked deletion residue, and contained the physical harness at the required relative path.
- PowerShell parser validation returned zero errors and the exact harness `-SyntaxOnly` invocation exited 0.
- The report records the harness SHA256, byte size, timestamp, clone commands, path, and safety accounting.
- No runtime preflight, confirmation, disruptive scenario, process kill, `openclaw`, `ollama`, or `cnx` command, lifecycle action, source edit, package installation, cleanup, or force-push occurred.

## Consequence

The incomplete-checkout blocker from Task 008 is resolved as an execution-environment checkout defect, not a harness or runtime defect. Task 008 remains permanently closed and must not be resumed.

The next unambiguous gate is one fresh authorization for the full real-Windows v3 process-recovery suite from a newly created complete clean isolated clone. That authorization is Task `CNX-20260822-010`.

Install, reset, uninstall, reinstall, tag, merge, and release remain unauthorized until the complete process-recovery suite is accepted.
