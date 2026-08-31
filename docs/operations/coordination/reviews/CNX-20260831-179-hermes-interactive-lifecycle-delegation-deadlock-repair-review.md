# CNX-20260831-179 — ChatGPT Review: Interactive Lifecycle Delegation Deadlock Repair

## Disposition

**ACCEPTED_PASS**

Final label:

`PASS — INTERACTIVE_LIFECYCLE_DELEGATION_REPAIR_ACCEPTED`

Task 179 is accepted. The repair candidate is:

`f6392da3e4112ce441526d5ef19925c90a872b0b`

This review accepts the repository repair only. The repaired candidate is not yet accepted as the live installed Windows candidate; install-over and live provenance/health require a successor task before any new reset is authorized.

## Reviewed authority

- Task-179 start authority: `983fafcdd5cc46bab4cdf108fb9f93b547ae4365`
- RED commit: `1c8cdc4effcf970c12cb5a2d0818aa726a3833df`
- repair candidate: `f6392da3e4112ce441526d5ef19925c90a872b0b`
- report publication: `a391ff4d6e4eaa469972d312d932407952265b47`
- report publication compare from candidate is report-only.

Candidate compare from Task-179 start to repair contains only:

- `skills/cogentnexus-openclaw/scripts/cnxclaw.py`
- `tests/test_cnxclaw_interactive_delegation.py`

## Independent findings

### Hung-process cleanup

Accepted. The executor re-verified the Task-178 ledger remained before confirmation (`prompt_observed=0`, `input_send_intent=0`, `input_sent=0`), matched the exact reset command tree, and terminated only that reset root tree. No confirmation was sent and no new reset was started.

### Root cause and minimal repair

Accepted. The pre-fix facade buffered delegated host-control stdout/stderr until child completion while destructive lifecycle confirmation waited inside the delegated child. The candidate adds a narrow interactive delegation path using current stdin/stdout/stderr and routes only `reset` and `uninstall` through it. Ordinary delegated commands retain the captured path.

At candidate SHA, `cnxclaw.py` contains `delegate_interactive()` and `main()` explicitly routes `reset`/`uninstall` through it. The repository blob for the candidate facade is `879083d6186589d4b2774b8fd87fa93692dd2dfc`.

### TDD

Accepted. RED was committed before production source repair and failed on prompt-before-input propagation while the noninteractive control remained valid. GREEN verifies visible prompt propagation, exactly one supplied input, cancellation behavior, and unchanged normal delegation.

### Validation and CI

Accepted. Local full pytest collection had an environment-specific pre-existing `scripts` import-path collection blocker, which the executor disclosed rather than hiding. This does not leave the stabilization full-suite requirement unproven because the exact repair SHA was independently verified by the repository's official `Validate` workflow: every matrix job completed successfully and each ran `python -m pytest -q` successfully, alongside plugin tests and validation.

Required exact-SHA workflows all target `f6392da3e4112ce441526d5ef19925c90a872b0b` and completed `success`:

- Validate `33361090584` — all 7 jobs success; full pytest step success across all OS/Python matrix jobs.
- Windows Installer Pack Smoke `33361090561` — job `npm-pack` success.
- PS5.1 Acceptance Smoke `33361090569` — job `serializer` success.

### Package boundary

The npm plugin package SHA-256 remains `8f6d0b8e64b1b53199ab1841a41bc1032241d107eac68603066fdd2ea642ca91` because this repair changes the CLI facade outside the npm plugin payload. Therefore the next live install-over must prove the active installed facade itself matches the repair candidate, not infer repair installation merely from the unchanged plugin package hash/fingerprint.

## Acceptance matrix

| Property | Verdict |
|---|---|
| exact Task-178 cleanup identity | PASS |
| no confirmation/destructive reset crossing | PASS |
| repository-native RED before source repair | PASS |
| root cause established | PASS |
| minimal interactive delegation repair | PASS |
| reset/uninstall only routed interactive | PASS |
| normal delegation preserved | PASS |
| focused GREEN | PASS |
| official full pytest on exact SHA | PASS |
| plugin tests/build/validation | PASS |
| Validate exact-SHA | PASS |
| Windows Installer exact-SHA | PASS |
| PS5.1 exact-SHA | PASS |
| report-only publication | PASS |
| live repaired installation | NOT YET PERFORMED |

## Next gate

Install-over the exact repaired candidate once on Windows using the supported installer path. Freeze and compare the candidate facade content hash against the actual installed facade reached by `cnxclaw.cmd`; then reaccept provenance, ownership, runtime, Gateway/Ollama, and durable-state health. Do not run reset or uninstall in that install-over task.
