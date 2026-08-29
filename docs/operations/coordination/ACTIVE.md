# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `LIVE_WINDOWS_READONLY_EVIDENCE_CLOSEOUT_ONLY`
Current authorization: `CNX-20260829-130_TASK129_READONLY_EVIDENCE_PUBLICATION_CLOSEOUT`
Task ID: `CNX-20260829-130`
Updated: 2026-08-29 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260829-130-task129-readonly-evidence-publication-closeout.md`](tasks/CNX-20260829-130-task129-readonly-evidence-publication-closeout.md)

Task 130 is a **read-only evidence-publication closeout** for Task 129. It must publish the retained forensic authority chain needed for independent acceptance of the Task-129 root-mismatch diagnosis. It is not a recovery/lifecycle task and authorizes no normalization.

## Task 129 status

Task-129 report:

`docs/operations/coordination/reports/CNX-20260829-129-managed-state-root-authority-readonly-diagnosis.md`

Report commit:

`e107e6408bbd7ad91e9d93f6c9b21349fd902597`

Independent review:

`docs/operations/coordination/reviews/CNX-20260829-129-managed-state-state-root-authority-readonly-diagnosis-review.md`

Review verdict:

`NEEDS EVIDENCE CLOSEOUT — the reported root-cause classification is technically credible and consistent with the installed-launcher contract, and Task 129 appears to have respected the read-only hard fence, but the published report does not contain enough of the evidence explicitly required by the Task-129 contract for independent acceptance. Do not mutate or normalize the live runtime; publish the retained forensic evidence first.`

Likely diagnosis to prove from retained evidence:

- `LAUNCHER_OR_ROOT_MISMATCH` — Task-128 probe used workspace parent as `--root` while the installed launcher uses `<workspace>\.cogentnexus-openclaw`;
- corresponding `SQLITE_PATH_OR_STATUS_PROBE_DEFECT` at the Task-128 acceptance-probe layer if the missing-SQLite observation is shown to derive from the same wrong root.

## Task 130 required work

Prefer the existing Task-129 evidence root:

`C:\Users\CDQ-P\AppData\Local\Temp\cnx129-authority-20260829T083000Z`

Publish in the Task-130 report:

- exact coordination/provenance;
- installed launcher content/hash and parsed Python/CLI/explicit `--root` target;
- installed CLI hashes/identity;
- authoritative controller/runtime/ownership/SQLite chain;
- literal installed-launcher read-only commands and exit codes;
- bounded competing-root inventory;
- scheduled-task/service command authority;
- relevant non-secret environment overrides;
- Task-125 cleanup versus current generation/mode/provider/timestamp comparison where evidence exists;
- exact SQLite read-only integrity result;
- evidence-backed final classification.

New live probing is discouraged. If a required fact was not retained, only a narrowly scoped deterministic read-only probe equivalent to Task 129 is allowed.

## Accepted repository candidate

Task-127 accepted source candidate remains:

`1b922bf400fdbccb1f9c7019b89b69fd67f44070`

Exact recovery harness:

- `scripts/test-v093-ollama-recovery-windows-v3.ps1`
- Git blob `622f70b339fea0f2ef7c564253aa3c6bf90ffc97`

Task-128 repaired-harness recovery suite remains **unlaunched**: `0 / 1`.

## Historical consumed ledger

Remain consumed/forbidden:

- Task-121 install-over `1 / 1`;
- Task-124 reset/uninstall/fresh reinstall/standalone stop/start/restart `1 / 1` each;
- Task-125 old-harness recovery suite `1 / 1`;
- Task-125 gateway-crash `1 / 1 PASS`;
- Task-125 provider-crash `1 / 1 old-harness convergence FAIL`;
- Task-128 repaired-harness recovery suite `0 / 1 launched`.

Task 130 authorizes zero recovery/lifecycle mutations.

## Completion signal

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260829-130-task129-readonly-evidence-publication-closeout.md`

Then stop for independent ChatGPT review. Do not open recovery re-acceptance or Dashboard acceptance automatically.

## Hard fence

No recovery suite/crash scenario, install/install-over/reset/uninstall/reinstall, start/stop/restart, enable/disable, provider/OpenClaw/model/config mutation, state/database/log edit or initialization, process kill, task/service run/change, cleanup/normalization, reboot, credential/secret access, Dashboard semantic Send, source/runtime repair, merge/tag/release, or force push.
