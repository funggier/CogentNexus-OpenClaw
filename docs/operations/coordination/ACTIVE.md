# Active Coordination Task

Status: `READY_HERMES`
Execution mode: `WINDOWS_RESET_FRESH_STATE_RECONSTRUCTION_ACCEPTANCE_HERMES`
Current authorization: `CNX-20260831-174_HERMES_RESET_FRESH_STATE_RECONSTRUCTION_ACCEPTANCE`
Task ID: `CNX-20260831-174`
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

[`tasks/CNX-20260831-174-hermes-reset-fresh-state-reconstruction-acceptance.md`](tasks/CNX-20260831-174-hermes-reset-fresh-state-reconstruction-acceptance.md)

Task 174 is the bounded real-Windows `cnxclaw reset` / fresh-state reconstruction acceptance for the already installed frozen candidate.

## Accepted baseline

- Product repair SHA: `231761fca24c315e90536955d3e384f55e2e232e`
- Installed plugin fingerprint: `e7d7d6c115040368e35232c83cacec315f6667c92452a5641f7a48a6947baf19`
- Accepted package SHA-256: `8f6d0b8e64b1b53199ab1841a41bc1032241d107eac68603066fdd2ea642ca91`
- OpenClaw: `2026.7.1-2`
- Task-171 through Task-173 result: `PASS — DASHBOARD_NATIVE_DURABLE_DELIVERY_REACCEPTANCE_ACCEPTED`

The Task-171 semantic Send count remains permanently frozen at exactly `1`. No additional semantic Send is authorized.

## Task-174 reset contract

Task 174 authorizes exactly one normal installed invocation:

`cnxclaw.cmd reset`

and exactly one interactive confirmation:

`y`

The reset implementation itself owns the PASSTHROUGH/native-route boundary, CogentNexus state removal/reconstruction, database bootstrap, policy application, re-enable, Gateway process boundary, and plugin/Gateway/Ollama/route verification required to return `fresh-install MANAGED`.

No separate helper lifecycle command is authorized. In particular, after reset starts Hermes/Codex must not issue a second reset, start/stop/restart/enable/disable, manual Gateway/Ollama restart, installer, uninstall, reinstall, rollback, or repair action.

## Current gate

Hermes/Codex must first perform fresh read-only authority/provenance/runtime/database preflight. If the accepted installed identity or safety prerequisites are materially inconsistent, do not reset; report `BLOCKED`.

If preflight passes:

1. run exactly one `cnxclaw.cmd reset`;
2. answer the documented prompt with exactly one `y`;
3. never retry under any failure/timeout/uncertainty condition;
4. collect read-only post-reset evidence;
5. prove the same installed candidate/release and OpenClaw pin remain;
6. prove reset itself reconstructed healthy fresh `MANAGED` controller/plugin/Gateway/Ollama/route state;
7. prove the fresh CogentNexus database is valid and the pre-reset Task-171 CogentNexus durable history was removed as required by reset;
8. prove no semantic/model/recovery work was manufactured;
9. prove OpenClaw/Ollama external data and unrelated namespaces remain intact within the documented preservation boundary;
10. publish the Task-174 report and stop for ChatGPT review.

## Hard fence

Task 174 authorizes semantic action count `0`.

Authorized only: read-only preflight, exactly one reset invocation, exactly one interactive `y`, implementation-owned internal reset subprocesses/process boundaries, read-only post-reset evidence, and Task-174 report publication.

No Dashboard Send, Enter semantic submission, composer typing/paste, `chat.inject`, alternate semantic input, manual inference, recovery/regeneration, second reset, executor-issued lifecycle helper, installer/uninstall/reinstall/rollback, manual durable/config/transcript mutation, source/product/test/workflow/dependency change, upgrade, release/promotion, merge, or force push.

After the Task-174 report is published, stop. Uninstall is not yet authorized.
