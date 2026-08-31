# CNX-20260831-180 — Repaired Candidate Windows Install-Over Provenance & Health

- **Task:** `CNX-20260831-180`
- **Execution mode:** `WINDOWS_REPAIRED_CANDIDATE_INSTALL_OVER_PROVENANCE_HEALTH_HERMES`
- **Repository:** `funggier/CogentNexus-OpenClaw`
- **Branch:** `agent/v0.9.3-full-stabilization`
- **Executor:** Hermes/Codex
- **Coordinator / final reviewer:** ChatGPT

## Objective

Install-over the exact accepted repository repair candidate once on the real Windows machine and prove that the active installed CLI facade, package/plugin payload, ownership, runtime, provider route, Gateway health, and durable-state boundary are coherent before any further reset attempt.

This task is an install-over/provenance/health gate only. It does **not** authorize reset, uninstall, reinstall, semantic Dashboard activity, or model/recovery activity.

## Accepted repository candidate

- repair candidate SHA: `f6392da3e4112ce441526d5ef19925c90a872b0b`
- repair commit message: `fix: stream interactive lifecycle delegation`
- candidate facade repository path: `skills/cogentnexus-openclaw/scripts/cnxclaw.py`
- candidate facade Git blob: `879083d6186589d4b2774b8fd87fa93692dd2dfc`
- unchanged npm plugin package SHA-256: `8f6d0b8e64b1b53199ab1841a41bc1032241d107eac68603066fdd2ea642ca91`
- expected plugin fingerprint from the unchanged plugin payload: `e7d7d6c115040368e35232c83cacec315f6667c92452a5641f7a48a6947baf19`
- release: `0.9.3`
- OpenClaw pin: `2026.7.1-2`

Task 179 is reviewed as:

`ACCEPTED_PASS — INTERACTIVE_LIFECYCLE_DELEGATION_REPAIR_ACCEPTED`

## Important provenance rule

The Task-179 repair changes the Python CLI facade outside the npm plugin payload. Therefore the unchanged npm package hash or plugin fingerprint **cannot by itself prove the repair is installed**.

Before install-over, compute and record the SHA-256 of the candidate `cnxclaw.py` from a clean checkout/materialization of exact commit `f6392da3...`. After install-over, resolve the actual `cnxclaw.cmd -> cnxclaw_v093.py -> cnxclaw.py` active installed chain and hash the exact installed `cnxclaw.py`. PASS requires byte identity between the clean exact candidate facade and the active installed facade.

## Phase A — fresh preflight

Before any installer action:

1. fetch fresh GitHub remote HEAD, `ACTIVE.md`, and `STATUS.md`; Task 180 must still be active;
2. verify Task-180 report is absent;
3. establish a clean exact source checkout/materialization at repair SHA `f6392da3...`;
4. compute candidate facade SHA-256 and record the Git blob above;
5. verify current installed release is `0.9.3` and OpenClaw remains `2026.7.1-2`;
6. verify current plugin fingerprint/package provenance is coherent with the previously installed candidate;
7. verify no live reset/uninstall process remains from Task 178/179;
8. read-only verify controller/plugin/Gateway/Ollama/provider route and SQLite integrity;
9. freeze current durable counts and exact Task-171 historical Ticket/delivery identities. They must remain present through this install-over because reset is not authorized;
10. verify no conflicting newer coordination authorization.

If source identity, install provenance, ownership, runtime safety, or process cleanup is materially ambiguous, do not run install-over; publish BLOCKED.

## Phase B — exactly one supported install-over

Run exactly one supported Windows install-over from the exact repaired candidate using the repository-supported `scripts/install.ps1` path and the same supported installation contract used by the accepted Windows install-over phase.

Requirements:

- exact source commit `f6392da3e4112ce441526d5ef19925c90a872b0b`;
- no second installer invocation or retry;
- no uninstall/reset/reinstall/rollback;
- no executor-issued start/stop/restart/enable/disable helper;
- installer-owned internal process boundaries/stages are allowed and must be recorded;
- capture exact command, working directory, child-stage exits, stdout/stderr, and final exit code;
- install-over must return success according to the supported installer contract.

If install-over returns nonzero, times out, or produces ambiguous partial state, do not retry. Preserve evidence and publish the actual disposition.

## Phase C — repaired-facade provenance proof

After install-over, resolve the active installed launch chain from the actual `cnxclaw.cmd` used by the operator.

PASS requires:

1. active `cnxclaw.cmd` resolves to the expected v0.9.3 facade chain;
2. the installed active `cnxclaw.py` SHA-256 exactly equals the clean exact-candidate facade SHA-256 recorded pre-install;
3. the installed file is from the supported installed workspace/package surface, not a temporary checkout;
4. no alternate stale facade is the active target of `cnxclaw.cmd`;
5. read-only source/content evidence shows the installed facade contains the accepted interactive-delegation behavior, but hash equality is the primary proof.

Do not invoke `reset` or `uninstall` merely to prove prompt behavior in Task 180.

## Phase D — package, ownership, and runtime health

After install-over, prove:

- installed release remains `0.9.3`;
- npm plugin package SHA-256 remains `8f6d0b8e64b1b53199ab1841a41bc1032241d107eac68603066fdd2ea642ca91` if the exact unchanged payload is used;
- plugin fingerprint remains `e7d7d6c115040368e35232c83cacec315f6667c92452a5641f7a48a6947baf19` unless evidence proves the fingerprint algorithm includes a changed non-plugin surface; any mismatch must be explained and cannot be silently accepted;
- namespace ownership manifest is present/coherent and legacy inventory remains empty;
- plugin is loaded/enabled/activated as expected;
- controller remains healthy MANAGED state;
- selected provider is Ollama with no unresolved provider transition;
- Gateway is healthy on the expected loopback boundary;
- Ollama is reachable/healthy/ready and configured model route is coherent;
- SQLite `PRAGMA integrity_check` is `ok`;
- no pending outbox/recovery work is manufactured by install-over;
- no semantic/model/recovery action occurs;
- exact pre-existing Task-171 Ticket/delivery history remains present and unchanged pending the future reset acceptance.

## Hard fence

Task 180 semantic action budget: `0`.

Not authorized:

- `cnxclaw reset`;
- uninstall;
- reinstall after uninstall;
- second install-over/retry;
- executor start/stop/restart/enable/disable;
- manual Gateway/Ollama restart;
- Dashboard Send/composer input/`chat.inject`;
- model inference/recovery/regeneration;
- manual durable/config/transcript/route/DB repair;
- product/source/test/workflow/dependency edits;
- upgrade/release/tag/merge;
- force push.

The only product mutation authorized is the exactly-one supported install-over of candidate `f6392da3...`.

## Acceptance boundary

PASS requires all of:

- fresh authority/preflight;
- exactly one supported install-over and exit `0`;
- active installed facade SHA-256 equals exact candidate facade SHA-256;
- installed release/OpenClaw pin/package/plugin provenance coherent;
- ownership/plugin/controller/Gateway/Ollama/route health coherent;
- SQLite integrity `ok`;
- old Task-171 durable history retained unchanged;
- no reset/uninstall/retry/helper/semantic/model/recovery action;
- report-only publication.

Any material criterion left unproven invalidates PASS.

## Required report

Publish only:

`docs/operations/coordination/reports/CNX-20260831-180-hermes-repaired-candidate-windows-install-over-provenance-health.md`

Follow `EXECUTOR_REPORT_CONTRACT.md`, including exact authority/head, install command/stages, candidate-vs-installed facade hashes, package/fingerprint provenance, runtime/DB checks, acceptance matrix, Reviewer Verification Packet, anomalies, residual unknowns, and publication fence.

After report publication, stop for ChatGPT review. Another reset remains unauthorized until Task 180 is independently accepted.
