# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `DOCS_TEST_CONTRACT_REPAIR`
Current authorization: `CNX-20260828-119_INSTALLER_DOCUMENTATION_AUTHORITY_ALIGNMENT`
Task ID: `CNX-20260828-119`
Updated: 2026-08-28 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260828-119-installer-documentation-authority-alignment.md`](tasks/CNX-20260828-119-installer-documentation-authority-alignment.md)

Task 119 is a **documentation/test contract repair** that aligns canonical installation guidance with the provider-neutral installer implementation already accepted from Tasks 117/118.

## Task 118 closure

Task-118 report:

`docs/operations/coordination/reports/CNX-20260828-118-posix-installer-provider-neutrality-alignment.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260828-118-posix-installer-provider-neutrality-alignment-review.md`

Review verdict:

`REJECTED FOR CANDIDATE ADVANCEMENT — CODE REPAIR ACCEPTED; CANONICAL INSTALL DOCUMENTATION/AUTHORITY REMAINS INCONSISTENT`

Accepted Task-118 implementation:

- both `scripts/install.ps1` and `scripts/install.sh` are provider-neutral at installer level;
- no installer provider parameter/default/validation remains;
- no direct provider executable prerequisite remains merely for installation;
- both installers use generic runtime `enable` handoff;
- runtime provider policy remains in runtime/provider modules;
- Task-118 source candidate CI/package proof was green;
- no live mutation occurred.

Blocking documentation findings:

- `docs/INSTALL.md` and `docs/INSTALL.th.md` still mix Ollama runtime requirements into general installer requirements;
- they still claim installer-owned provider preflight;
- canonical POSIX provider-free source-install command is not present in user-facing installation guidance;
- the Task-118 automated POSIX command assertion reads a coordination task document instead of canonical consumer documentation.

## Architectural invariant

**Every subsystem defines only data genuinely required to perform or verify that subsystem's own responsibility.**

Documentation must preserve the same boundary as implementation. Installer prerequisites/behavior must be distinguished from runtime/provider readiness. Current runtime provider support may still be documented where runtime actually owns it.

Required Task-119 method:

`fresh reconcile -> TESTS-ONLY canonical-doc RED -> minimal current-doc/test alignment -> GREEN -> focused/full validation -> exact same-SHA CI/package proof -> report -> independent review`

## Preserved live boundary

Task 116 remains the latest authoritative live-machine evidence:

- CNX passthrough, generation 25;
- OpenClaw exactly `2026.7.1-2`;
- current runtime/provider healthy;
- Gateway healthy;
- SQLite integrity `ok`;
- interrupted-reentry classification coherent;
- no lifecycle phase beyond the failed pre-body Task-116 install-over binding executed.

Task 119 must not mutate live state.

## Hard fence

Task 119 does **not** authorize:

- live install-over/reset/uninstall/reinstall;
- live POSIX installation;
- Task-116 destructive replay;
- live stop/start/restart/recovery harness;
- manual cleanup/normalization;
- OpenClaw/provider-runtime changes;
- provider/model/endpoint/timeout changes;
- live SQLite/config/session/manifest/plugin mutation;
- credentials/secrets access;
- Dashboard semantic Send;
- reboot/process-tree kill;
- merge/tag/release/force push.

## Completion signal

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260828-119-installer-documentation-authority-alignment.md`

Then stop for independent ChatGPT review. Do not create or execute a real-Windows lifecycle retry task.
