# CNX-20260829-130 — Task-129 Read-Only Evidence Publication Closeout

- Status: `READY_FOR_HERMES`
- Execution mode: `LIVE_WINDOWS_READONLY_EVIDENCE_CLOSEOUT_ONLY`
- Owner / independent reviewer: ChatGPT
- Executor: Hermes/Codex after operator continuation
- Date: 2026-08-29 ICT
- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`

## Purpose

Close the evidence-publication gap identified by the independent Task-129 review without changing the live runtime.

Task 129 produced a technically credible diagnosis that Task 128 used the workspace parent as `--root` while the installed launcher uses `<workspace>\.cogentnexus-openclaw`, causing a false `passthrough` / null-provider / missing-SQLite preflight. The independent review did **not** reject that diagnosis; it rejected the completeness of the published evidence needed to independently accept it.

Task 130 must primarily consume and summarize the already-retained Task-129 forensic evidence. It is not a new recovery or lifecycle task and does not authorize normalization.

## Prior artifacts

Task-129 report:

`docs/operations/coordination/reports/CNX-20260829-129-managed-state-root-authority-readonly-diagnosis.md`

Task-129 independent review:

`docs/operations/coordination/reviews/CNX-20260829-129-managed-state-state-root-authority-readonly-diagnosis-review.md`

Task-129 evidence root reported by executor:

`C:\Users\CDQ-P\AppData\Local\Temp\cnx129-authority-20260829T083000Z`

Accepted Task-127 candidate remains:

`1b922bf400fdbccb1f9c7019b89b69fd67f44070`

Exact recovery harness remains:

- `scripts/test-v093-ollama-recovery-windows-v3.ps1`
- Git blob `622f70b339fea0f2ef7c564253aa3c6bf90ffc97`

Task-128 repaired-harness suite remains **unlaunched**: `0 / 1`.

## Execution policy

1. Fresh-fetch coordination and confirm Task 130 is authoritative before any evidence work.
2. Prefer existing Task-129 evidence files. Do not repeat a live probe merely because it is convenient.
3. If one required fact is genuinely absent from retained evidence, a narrowly scoped deterministic **read-only** probe equivalent to Task 129 is allowed only for that missing fact.
4. Any such probe must use the explicit installed launcher/path or direct read-only filesystem/task inspection; never use lifecycle commands.
5. Do not alter controller/runtime/ownership/database/log/task/service/provider/OpenClaw/Ollama state.
6. Do not rerun Task 128 or any recovery scenario.

## Required evidence publication

Publish enough detail in the Task-130 report itself for independent verification. At minimum:

### A. Coordination / provenance

- exact branch HEAD observed at Task-130 execution start;
- exact Task-129 report commit `e107e6408bbd7ad91e9d93f6c9b21349fd902597`;
- Task-129 evidence root existence and relevant file inventory;
- whether each published fact came from retained Task-129 evidence or from a new strictly read-only closeout probe.

### B. Installed launcher authority

For `C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd`, publish:

- existence;
- size;
- creation/write timestamps if retained;
- SHA256;
- complete launcher text (it must contain no secret; if an unexpected secret is present, redact only the secret and state that redaction occurred);
- parsed foreground Python executable;
- parsed installed `cnxclaw_v093.py` path;
- parsed explicit `--root` path;
- proof `%*` forwarding is present;
- `Get-Command cnxclaw.cmd -All` / PATH ambiguity result if retained.

### C. Installed CLI identity

Publish SHA256/existence/absolute paths for at least:

- installed `cnxclaw_v093.py`;
- installed `cnxclaw.py`;
- installed `host_control_v092.py`;

and compare those identities with the accepted candidate/package where retained evidence permits. If exact candidate comparison was not captured, state that limitation rather than infer equality.

### D. Authoritative state-root chain

Publish the literal parsed authoritative root and relevant file metadata/state for:

- `host\controller.json`;
- relevant runtime/ownership metadata files discovered by Task 129;
- authoritative SQLite database.

For controller state publish at least:

- mode;
- selectedProvider;
- desiredGateway;
- desiredProvider;
- generation;
- updatedAt;
- providerTransition;
- providerSelection metadata if present.

For SQLite publish:

- exact absolute path;
- existence;
- read-only open method;
- exact `PRAGMA integrity_check` result.

### E. Exact authoritative read-only commands

Publish literal command lines/paths and exit codes for the Task-129 installed-launcher probes:

- `status`;
- `provider status --json`;
- `check recovery --json`;

including the resulting authoritative mode/provider/recovery verdict.

### F. Competing roots

Publish the bounded competing-root inventory from Task 129:

- each relevant root/path found;
- controller/ownership identity where retained;
- whether any installed launcher/task/service references that root;
- explicitly identify the Task-128 wrong root and why it was non-authoritative.

If no additional competing root was found, state that explicitly.

### G. Scheduled-task/service authority

Publish the relevant read-only task/service authority evidence retained from Task 129, at minimum for `CogentNexus-OpenClaw-Supervisor` and relevant OpenClaw Gateway authority:

- executable/action path;
- arguments;
- working directory if configured;
- state;
- last result/time if retained;
- whether it resolves to the same authoritative installed state/workspace chain.

If a field was not captured, mark it unproven; do not fill it from assumption.

### H. Non-secret environment overrides

Publish whether relevant non-secret root/config overrides were present, including `OPENCLAW_CONFIG_PATH` and any CNX workspace/root variable actually used by source. Do not publish credentials/tokens/API keys.

### I. Task-125 → current timeline

Use retained evidence to publish:

- Task-125 cleanup/final controller mode/provider/generation/updatedAt if actually available;
- Task-129 current controller mode/provider/generation/updatedAt;
- whether the generation advanced, reset, or cannot be compared;
- whether any durable post-Task-125 mutating transition is evidenced;
- if exact historical generation/timestamp cannot be proven, state that explicitly.

The core question is whether there is evidence of authoritative managed-state drift versus a Task-128 probe false negative. Do not invent an actor or transition.

## Required final classification

Conclude with the Task-129 classification only if the evidence supports it:

- `LAUNCHER_OR_ROOT_MISMATCH`;
- optionally paired with `SQLITE_PATH_OR_STATUS_PROBE_DEFECT` if the missing-SQLite observation is demonstrated to derive from the same wrong root.

If retained evidence contradicts the Task-129 report, use `INDETERMINATE` or the appropriate Task-129 classification and explain exactly why.

## Required report

Publish exactly:

`docs/operations/coordination/reports/CNX-20260829-130-task129-readonly-evidence-publication-closeout.md`

The report must include the evidence above, the execution ledger, and explicit statement that no mutation or Dashboard semantic Send occurred.

Then STOP for independent ChatGPT review. Do not open the recovery re-acceptance task automatically.

## Historical ledger / hard fence

Remain consumed/forbidden:

- Task-121 install-over `1 / 1`;
- Task-124 reset/uninstall/fresh reinstall/standalone stop/start/restart `1 / 1` each;
- Task-125 old-harness recovery suite `1 / 1`;
- Task-128 repaired-harness suite `0 / 1 launched` and remains unconsumed.

Task 130 authorizes **zero** recovery/lifecycle mutation.

Forbidden:

- recovery suite or crash injection;
- install/install-over/reset/uninstall/reinstall;
- start/stop/restart/enable/disable;
- provider/model/config selection/change;
- controller/runtime/ownership/database/log edits;
- database initialization/migration/write;
- process kill;
- scheduled-task/service run/start/stop/change;
- cleanup/normalization;
- OpenClaw/Ollama update/change;
- reboot;
- credential/secret access or capture;
- Dashboard semantic Send;
- source/runtime repair;
- merge/tag/release/force push.
