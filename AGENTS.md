# CogentNexus Agent Instructions

Use this file as a compact entry point. Deeper project truth lives under `docs/`.

## Coordination with ChatGPT

When the operator is using the GitHub coordination workflow, read:

- `docs/operations/coordination/README.md`
- `docs/operations/coordination/SIGNALS.md`
- `docs/operations/coordination/ACTIVE.md`
- the active task linked by `ACTIVE.md`

The operator should not need to copy the task body from ChatGPT into Codex.

### Minimal trigger

If the operator sends only:

```text
ต่อ
```

safely synchronize the coordination branch, re-read the current GitHub coordination records, and execute the active task **only if** `ACTIVE.md` is `READY_FOR_CODEX`.

Write the result to the matching file under `docs/operations/coordination/reports/`, commit/push normally, then stop for ChatGPT review.

Do not repeat completed disruptive effects if a matching completed report already exists or review is pending.

`สถานะ` is read-only coordination status. `หยุด` means do not begin a new coordination task.

## Safety

Task-specific safety gates are mandatory. A trigger never overrides them. If prerequisites are unsafe, ambiguous, or unsatisfied, report `BLOCKED` rather than improvising.

Never force-push coordination history unless the operator explicitly gives a separate instruction that clearly requires it.

## Project truth

- `docs/operations/` is living project status/roadmap/history.
- Accepted technical claims require code/tests/evidence/release gates.
- v0.9.2 is a frozen historical baseline; do not rewrite it for v0.9.3 convenience.
