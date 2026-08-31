# Coordination Channel Status

**State:** `READY_HERMES`  
**Execution mode:** `WINDOWS_REPAIRED_CANDIDATE_INSTALL_OVER_PROVENANCE_HEALTH_HERMES`  
**Updated:** 2026-08-31 ICT  
**Transport:** GitHub repository history  
**Active task:** `CNX-20260831-180`

## Active work

[`tasks/CNX-20260831-180-hermes-repaired-candidate-windows-install-over-provenance-health.md`](tasks/CNX-20260831-180-hermes-repaired-candidate-windows-install-over-provenance-health.md)

Executor: Hermes/Codex. Coordinator / final reviewer: ChatGPT.

Standing model: executor-heavy / reviewer-light.

## Accepted repository state

Task 179 is independently accepted:

`ACCEPTED_PASS — INTERACTIVE_LIFECYCLE_DELEGATION_REPAIR_ACCEPTED`

Accepted repository repair candidate:

`f6392da3e4112ce441526d5ef19925c90a872b0b`

Candidate facade Git blob:

`879083d6186589d4b2774b8fd87fa93692dd2dfc`

Exact-SHA workflows:

- Validate `33361090584`: completed/success, 7/7 jobs; full pytest step success in each matrix job.
- Windows Installer Pack Smoke `33361090561`: completed/success.
- PS5.1 Acceptance Smoke `33361090569`: completed/success.

Task-179 report publication is `a391ff4d6e4eaa469972d312d932407952265b47` and its publication commit is report-only relative to the repair candidate.

## Live installed baseline entering Task 180

The live installation has not yet been proven to contain the Task-179 facade repair. Treat the installed baseline as the prior accepted v0.9.3 candidate until Task 180 completes:

- previous repair SHA `231761fca24c315e90536955d3e384f55e2e232e`;
- plugin fingerprint `e7d7d6c115040368e35232c83cacec315f6667c92452a5641f7a48a6947baf19`;
- npm plugin package SHA-256 `8f6d0b8e64b1b53199ab1841a41bc1032241d107eac68603066fdd2ea642ca91`;
- release `0.9.3`;
- OpenClaw `2026.7.1-2`.

Task 178 never crossed confirmation. The historical Task-171 Ticket/delivery state is therefore expected to remain present before and after Task-180 install-over.

## Task 180 gate

Task 180 authorizes exactly one supported install-over from exact candidate `f6392da3...`.

Primary acceptance proof is byte identity between:

1. `skills/cogentnexus-openclaw/scripts/cnxclaw.py` from a clean exact-candidate source checkout/materialization; and
2. the actual installed `cnxclaw.py` reached by the operator's active `cnxclaw.cmd` chain after install-over.

Because the repair is outside the npm plugin payload, unchanged npm package SHA/plugin fingerprint cannot substitute for active facade proof.

Post-install must also prove ownership, plugin/controller health, selected Ollama route, Gateway health, OpenClaw pin, SQLite integrity, no pending recovery/outbox manufacture, and preservation of pre-reset durable history.

## Hard fence

Task 180 semantic action budget is `0`.

No reset, uninstall, reinstall, second install-over/retry, executor-issued lifecycle helper, manual Gateway/Ollama restart, Dashboard Send, model/recovery action, manual durable/config/transcript/route/DB repair, product/source/test/workflow edit, release/tag/merge, or force push.

After Task-180 report publication, stop for ChatGPT review. Another reset remains unauthorized.
