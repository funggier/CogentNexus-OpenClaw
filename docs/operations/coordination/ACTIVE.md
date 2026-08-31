# Active Coordination Task

Status: `AWAITING_HERMES_WINDOWS_EXECUTION`
Execution mode: `TASK188_SUBTASK189_BOUNDED_WINDOWS_REQUALIFICATION`
Current disposition: `IN_PROGRESS`
Task ID: `CNX-20260831-188`
Execution subtask: `CNX-20260831-189`
Updated: 2026-08-31 ICT
Executor: Hermes for bounded Windows requalification
Coordinator / final reviewer: ChatGPT
Human release authority: User

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

GitHub remote branch `agent/v0.9.3-full-stabilization` is authoritative for coordination history.

## Active umbrella task

[`tasks/CNX-20260831-188-documentation-payload-convergence-and-proportional-requalification.md`](tasks/CNX-20260831-188-documentation-payload-convergence-and-proportional-requalification.md)

## Current execution subtask

[`tasks/CNX-20260831-189-bounded-windows-documentation-payload-requalification.md`](tasks/CNX-20260831-189-bounded-windows-documentation-payload-requalification.md)

Pre-Windows checkpoint:

[`notes/CNX-20260831-188-checkpoint-02-pre-windows-requalification.md`](notes/CNX-20260831-188-checkpoint-02-pre-windows-requalification.md)

## Frozen product candidate

**Task-188/189 product candidate:**

`604569c286e930f1a596362ab926b065b56d486e`

This SHA is immutable for Task 189. Coordination-only commits after the freeze do not redefine the candidate and must not be installed/tested instead.

### Frozen identities

- version: `0.9.3`
- package payload-v2: `408167da1bfba7fa9723d1bd557f29d516ed27c27398b4e48abf9a4f294e6b5b` / `184` files
- installed skill-tree Git tree: `a1e873ba404205507a1623961b49f1b1a0689f9f`
- executable scripts-tree Git tree: `3d9d323ba19443d46e970b87cef52ce878da274f`
- accepted facade Git blob: `879083d6186589d4b2774b8fd87fa93692dd2dfc`
- accepted facade SHA-256: `aa747f8f30080ef839a8d2cbf5758f9981a007ca01f41a988576f42edea8682f`

## Repository gate

Exact `604569c286e930f1a596362ab926b065b56d486e` is green:

- Validate `33382417045` — PASS
- Windows Installer Pack Smoke `33382417032` — PASS
- PS5.1 Acceptance Smoke `33382417028` — PASS
- package-proof artifact `9754267508`

## Current objective

Hermes performs bounded real-Windows requalification of exact `604569c286e930f1a596362ab926b065b56d486e`:

`one install-over -> provenance/health/installed-byte proof -> one bounded human Dashboard semantic/durable-delivery turn`

Then Hermes publishes the Task-189 report and stops for ChatGPT review.

## Requalification principle

The implementation already passed the full v0.9.3 stabilization sequence at a meaningful level. Task 188 changed documentation/instruction-bearing product files while preserving executable/runtime bytes. Therefore reset/uninstall/fresh-reinstall are not repeated by default.

If new evidence requires destructive lifecycle requalification, Task 189 must stop with `REQUALIFICATION_SCOPE_EXPANSION_REQUIRED`; it must not broaden scope automatically.

## Transport state

This ChatGPT session does not expose an installed Hermes/LConnect/Windows remote-execution connector. Task 189 is therefore a durable repository handoff. Do not claim Windows execution until real Task-189 evidence is published.

## Hard fence

No production/runtime/plugin executable source, tests, dependencies, workflow behavior, provider/runtime semantics, or durable-schema changes under Task 189. No reset, uninstall, fresh reinstall, release PR merge, Release workflow dispatch, tag/release publication, or force push from Task 189.
