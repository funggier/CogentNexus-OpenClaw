# CNX-20260907-303 — Adopt Task301 Repair Through Supported Path

## Status

`READY_FOR_HERMES`

Parent: `CNX-20260907-302`  
Executor: `Hermes`  
Reviewer: `ChatGPT`

## Authority

Hermes is authorized to determine and execute the supported canonical adoption/deployment path for the Task301 quiescence repair. Hermes may choose technical implementation details, inspect the installed package/release provenance, and make bounded corrective decisions without micro-confirmation.

The objective is to make the exact Task301 wiring available in the live installation through an existing supported managed mechanism. Manual file copying, guessed commands, or uncontrolled replacement are not allowed.

## Procedure

1. Fresh-fetch current branch, task state, latest report, and exact candidate.
2. Identify the supported adoption path from repository/install contracts and installed provenance.
3. Run repository/source/CI or read-only preflight as needed.
4. If adoption requires a live mutation, prove the exact target, scope, rollback/restore behavior, and health boundary before acting.
5. Adopt only the Task301 repair; preserve unrelated live state.
6. Recompute installed-vs-candidate hashes and verify Supervisor/Host wiring.
7. Publish an evidence-rich report describing the chosen method, why it is supported, commands/actions performed, exact files/hashes, tests, and PASS/FAIL/BLOCKED.
8. Stop at the boundary before any additional `cnxclaw enable` invocation unless explicitly authorized by a successor task.

## Allowed bounded technical autonomy

Hermes may choose between supported repository-defined update, activation, or maintenance paths; adjust implementation or documentation if a defect is found; add TDD coverage where needed; and retry a bounded technical step only when the failure evidence shows the retry is safe and materially different.

## Hard fences

No semantic send, replay/redelivery/disposition, manual Ticket/SQLite/session/transcript mutation, protected-state mutation, destructive cleanup, installer/uninstall/reset outside the proven supported adoption path, unrelated Scheduled Task/service mutation, credential action, release promotion, or force push. Do not touch protected Ticket `CNXT-dc11c9a0-8a89-4df5-9c48-345260725be4` or owner session `agent:main:discord:channel:1531199905673252946`.
