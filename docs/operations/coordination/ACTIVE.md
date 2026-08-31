# Active Coordination Task

Status: `READY_HERMES`
Execution mode: `WINDOWS_REPAIRED_CANDIDATE_INSTALL_OVER_PROVENANCE_HEALTH_HERMES`
Current authorization: `CNX-20260831-180_HERMES_REPAIRED_CANDIDATE_INSTALL_OVER_PROVENANCE_HEALTH`
Task ID: `CNX-20260831-180`
Updated: 2026-08-31 ICT
Executor: Hermes/Codex
Coordinator / final reviewer: ChatGPT
Review model: executor-heavy / reviewer-light

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

GitHub remote branch `agent/v0.9.3-full-stabilization` is authoritative.

## Active task

[`tasks/CNX-20260831-180-hermes-repaired-candidate-windows-install-over-provenance-health.md`](tasks/CNX-20260831-180-hermes-repaired-candidate-windows-install-over-provenance-health.md)

## Accepted repository repair

Task 179:

`ACCEPTED_PASS — INTERACTIVE_LIFECYCLE_DELEGATION_REPAIR_ACCEPTED`

Accepted repair candidate:

`f6392da3e4112ce441526d5ef19925c90a872b0b`

Candidate facade:

- path `skills/cogentnexus-openclaw/scripts/cnxclaw.py`
- Git blob `879083d6186589d4b2774b8fd87fa93692dd2dfc`

Required exact-SHA CI:

- Validate `33361090584` — success
- Windows Installer Pack Smoke `33361090561` — success
- PS5.1 Acceptance Smoke `33361090569` — success

The official Validate matrix ran full `python -m pytest -q` successfully on every matrix job.

## Installed baseline before Task 180

Until Task 180 proves otherwise, the live machine is still considered to have the previous installed v0.9.3 candidate:

- previous repository repair SHA `231761fca24c315e90536955d3e384f55e2e232e`;
- plugin fingerprint `e7d7d6c115040368e35232c83cacec315f6667c92452a5641f7a48a6947baf19`;
- npm plugin package SHA-256 `8f6d0b8e64b1b53199ab1841a41bc1032241d107eac68603066fdd2ea642ca91`;
- release `0.9.3`;
- OpenClaw `2026.7.1-2`.

Task-171 historical durable state remains expected before the future reset acceptance because Task 178 never crossed confirmation.

## Task-180 authorization

After fresh preflight, Hermes/Codex may perform exactly one supported Windows install-over from exact repaired source candidate `f6392da3...`.

Task 180 must prove the actual active installed `cnxclaw.py` reached by `cnxclaw.cmd` is byte-identical to the clean exact candidate facade. The unchanged npm package hash/plugin fingerprint are not sufficient proof by themselves because Task-179 changed the CLI facade outside the npm plugin payload.

## Hard fence

Task 180 semantic action budget: `0`.

No reset, uninstall, reinstall, second installer invocation/retry, executor lifecycle helper, manual Gateway/Ollama restart, Dashboard Send, model/recovery action, manual state repair, source/product/test/workflow change, release/tag/merge, or force push.

Installer-owned internal stages/process boundaries are authorized only as part of the one supported install-over.

After Task-180 report publication, stop for ChatGPT review. Another reset remains unauthorized.
