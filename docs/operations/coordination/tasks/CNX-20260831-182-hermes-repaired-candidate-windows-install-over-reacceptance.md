# CNX-20260831-182 — Repaired Candidate Windows Install-Over Reacceptance

- **Task:** `CNX-20260831-182`
- **Execution mode:** `WINDOWS_REPAIRED_CANDIDATE_INSTALL_OVER_REACCEPTANCE_HERMES`
- **Repository:** `funggier/CogentNexus-OpenClaw`
- **Branch:** `agent/v0.9.3-full-stabilization`
- **Accepted repair candidate:** `f6392da3e4112ce441526d5ef19925c90a872b0b`
- **Candidate facade:** `skills/cogentnexus-openclaw/scripts/cnxclaw.py`
- **Candidate facade Git blob:** `879083d6186589d4b2774b8fd87fa93692dd2dfc`
- **Candidate facade SHA-256:** `aa747f8f30080ef839a8d2cbf5758f9981a007ca01f41a988576f42edea8682f`
- **Executor:** Hermes/Codex
- **Coordinator / final reviewer:** ChatGPT

## Objective

Install over the current Windows CogentNexus-OpenClaw v0.9.3 installation exactly once from the accepted Task-179 repair candidate, then prove provenance and health with emphasis on the active installed CLI facade.

Task 181 established a clean process boundary. Task 182 must independently re-check that boundary immediately before mutation; Task-181 evidence is not a substitute for fresh preflight.

## Accepted baseline

Repository repair:

`ACCEPTED_PASS — INTERACTIVE_LIFECYCLE_DELEGATION_REPAIR_ACCEPTED`

Clean observer boundary:

`ACCEPTED_PASS — HISTORICAL_TASK178_OUTER_OBSERVER_RETIRED_CLEAN_BOUNDARY_PROVEN`

Expected unchanged plugin/package identity unless fresh evidence proves otherwise:

- release `0.9.3`;
- npm package SHA-256 `8f6d0b8e64b1b53199ab1841a41bc1032241d107eac68603066fdd2ea642ca91`;
- plugin fingerprint `e7d7d6c115040368e35232c83cacec315f6667c92452a5641f7a48a6947baf19`;
- OpenClaw `2026.7.1-2`.

These unchanged package values are supporting evidence only. They cannot prove the Task-179 Python facade repair is active.

Task-171 historical durable state is expected to remain present throughout Task 182 because reset remains unauthorized.

## Phase A — fresh authority and clean-boundary preflight

Before installer invocation:

1. fetch fresh remote HEAD, `ACTIVE.md`, `STATUS.md`, and Task-182 task/report state;
2. materialize or use a clean detached source at exact candidate `f6392da3...`;
3. hash the clean candidate facade and confirm SHA-256 exactly `aa747f8f30080ef839a8d2cbf5758f9981a007ca01f41a988576f42edea8682f`;
4. perform a fresh process scan proving zero Task-178 observer residue and zero reset/uninstall/lifecycle process residue;
5. read-only verify ownership, controller state, selected Ollama route, Gateway, Ollama, delivery, recovery, OpenClaw pin, and SQLite integrity;
6. record pre-install durable counts and exact Task-171 Ticket/delivery presence;
7. record the current installed active launcher chain and pre-install facade hash.

If any lifecycle/observer residue is present or core preflight is not coherent, stop without invoking the installer. Do not clean it under this task.

## Phase B — exactly one supported install-over

If and only if Phase A passes, invoke the repository-supported Windows installer/install-over path from the exact clean candidate once.

Requirements:

- exactly one installer root invocation;
- no retry or second install-over under Task 182;
- preserve exact stdout/stderr, exit code, stage ledger, source/candidate provenance, package provenance, and installer-owned process boundaries;
- installer-owned internal stop/start/restart/bootstrap stages are permitted only as part of that one supported invocation;
- do not issue executor-side lifecycle helpers before, during, or after the installer.

If the installer fails or evidence becomes ambiguous, stop and report the bounded failure. Do not retry.

## Phase C — active facade provenance

After a successful installer exit, resolve the actual operator launcher chain beginning at the installed `cnxclaw.cmd` and identify the `cnxclaw.py` used by the active v0.9.3 path.

PASS requires byte identity with the clean candidate facade. Record at minimum:

- installed facade absolute path;
- bytes;
- SHA-256;
- candidate SHA-256;
- equality verdict.

The installed facade SHA-256 must equal:

`aa747f8f30080ef839a8d2cbf5758f9981a007ca01f41a988576f42edea8682f`

Do not infer this from npm package or plugin fingerprint.

## Phase D — post-install provenance and health

Read-only verify:

- installed release remains `0.9.3`;
- OpenClaw remains exactly `2026.7.1-2`;
- ownership manifest/inventory valid and legacy namespace empty;
- plugin installed, loaded/enabled/activated as expected;
- controller coherent in managed mode;
- selected provider is Ollama with no stuck transition;
- Gateway healthy on the expected loopback boundary;
- Ollama healthy/ready and current route coherent;
- delivery/recovery READY;
- pending outbox `0`;
- no active incident or manufactured recovery work;
- SQLite read-only integrity `ok`;
- Task-171 historical Ticket/delivery still present;
- no unexpected Ticket/event/model/recovery/delivery/session growth attributable to Task 182.

Record fresh package/fingerprint values even if unchanged.

## Hard fence

Task 182 semantic action budget: `0`.

Not authorized:

- reset;
- uninstall;
- reinstall after uninstall;
- second installer/install-over invocation or retry;
- executor-issued start/stop/restart/enable/disable;
- manual Gateway/Ollama lifecycle action;
- Dashboard Send/composer input/`chat.inject`;
- model inference/recovery/regeneration;
- manual durable/config/transcript/route/DB repair;
- product/source/test/workflow/dependency edits;
- release/tag/merge;
- force push.

Repository coordination/report publication is authorized.

## Required disposition

Use one of:

- `PASS — REPAIRED_CANDIDATE_INSTALL_OVER_ACTIVE_FACADE_PROVEN`
- `FAIL — REPAIRED_CANDIDATE_INSTALL_OVER_OR_PROVENANCE_FAILED`
- `BLOCKED — PREINSTALL_GATE_NOT_CLEAN`
- `UNPROVEN — INSTALL_OVER_COMPLETION_OR_ACTIVE_FACADE_IDENTITY_UNAVAILABLE`

PASS requires exactly one successful supported install-over, exact active-facade byte identity, and coherent post-install health/provenance.

## Required report

Publish:

`docs/operations/coordination/reports/CNX-20260831-182-hermes-repaired-candidate-windows-install-over-reacceptance.md`

Follow `EXECUTOR_REPORT_CONTRACT.md`. Include installer count, exact command/stages/exit, candidate and installed facade hashes, package/fingerprint provenance, runtime/DB health, before/after durable counts, hard-fence audit, acceptance matrix, Reviewer Verification Packet, residual unknowns, and publication fence.

After report publication, stop for ChatGPT review. Reset and uninstall remain unauthorized until a later successor explicitly opens them.
