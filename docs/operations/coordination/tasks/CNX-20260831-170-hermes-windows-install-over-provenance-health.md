# CNX-20260831-170 — Hermes Windows Install-Over Provenance and Health

Status: `READY_HERMES`

Execution mode: `WINDOWS_TASK167_ACCEPTED_CANDIDATE_INSTALL_OVER_PROVENANCE_HEALTH_HERMES`

Authorization: `CNX-20260831-170_HERMES_WINDOWS_INSTALL_OVER_PROVENANCE_HEALTH`

Executor: Hermes/Codex  
Coordinator / final reviewer: ChatGPT

## Objective

Install the accepted Task-167 repair candidate over the currently installed CogentNexus-OpenClaw instance exactly once using the supported Windows installer path, then prove exact package/plugin provenance and healthy post-install runtime state.

This task is a provenance/health checkpoint only. It does not authorize any semantic Dashboard Send or semantic live acceptance experiment.

## Accepted product authority

Frozen accepted repair SHA:

`231761fca24c315e90536955d3e384f55e2e232e`

Final repair disposition:

`PASS — NATIVE_DELIVERY_STAGING_REPAIR_ACCEPTED`

Pinned OpenClaw source/runtime target remains:

`0790d9f593ad30c940ed93b5872a8cf6d6f3cf8c` (`2026.7.1-2`).

Accepted exact-SHA CI:

- PS5.1 Acceptance Smoke `33330458475`: success;
- Windows Installer Pack Smoke `33330458470`: success;
- Validate `33330458434`, attempt 2: success, 7/7 jobs.

Relevant reports/reviews:

- `reports/CNX-20260831-167-hermes-native-delivery-staging-root-cause-repair.md`
- `reports/CNX-20260831-168-hermes-task167-verification-completion.md`
- `reports/CNX-20260831-169-hermes-task167-exact-sha-validate-rerun.md`
- `reviews/CNX-20260831-169-hermes-task167-exact-sha-validate-rerun-review.md`

## Mandatory preflight

Before any install action, Hermes/Codex must:

1. fetch current GitHub remote state and read `ACTIVE.md`, `STATUS.md`, this task, the Task-169 report/review, and the standing executor/report contracts;
2. prove this Task 170 is the active authority and that its matching report does not already exist;
3. prove no product/source/dependency/workflow drift has replaced accepted repair SHA `231761f...`;
4. use a fresh/isolated checkout or worktree tied to the accepted candidate for package creation;
5. verify the installed OpenClaw version is still `2026.7.1-2` and CogentNexus plugin identity is the expected plugin ID;
6. capture the currently installed plugin fingerprint/version/state before installation;
7. capture controller, Gateway, Ollama/provider, startup adapter, recovery, delivery, storage/database integrity and relevant health state before installation;
8. capture read-only pre-install database counts/state sufficient to prove that the install operation did not create semantic work or corrupt durable state;
9. stop before installation and report `BLOCKED` if provenance or runtime state is materially inconsistent with the accepted boundary.

Do not use stale package/fingerprint values as authority. Recompute candidate package identity from the exact accepted candidate during this task.

## Candidate freeze and package provenance

From exact repair SHA `231761f...`, create the installable plugin package using the repository-supported path.

Record at minimum:

- exact source HEAD;
- candidate changed-file/product fence;
- package filename;
- package size;
- package SHA-256;
- package file count/content validation result;
- candidate plugin fingerprint using the repository-supported ownership/provenance mechanism;
- important production source/build hashes if the current installer/provenance tooling exposes them;
- `npm ci` / build / plugin validation results required by the supported packaging path.

The package installed on Windows must be byte/provenance-identical to the package whose identity is recorded in the report.

## Exactly-one install-over authority

Task 170 authorizes exactly **one supported install-over execution** of the accepted candidate.

Use the normal repository-supported Windows installer/install-over path. Capture process/command provenance and installer diagnostic stages as available.

If that one install action fails or is ambiguous:

- do not launch a second installer;
- do not uninstall/reinstall/reset as a workaround;
- do not patch production/source/runtime inside this task;
- collect evidence, analyze the failure deeply, publish `FAIL`/`BLOCKED`/`REWORK_REQUIRED`, and stop.

A retry requires a new explicit task authorization.

## Mandatory post-install provenance proof

After the one install-over completes, independently prove:

1. plugin ID is `cogentnexus-openclaw`;
2. plugin version/state is expected and loaded/enabled;
3. installed plugin fingerprint equals the candidate fingerprint computed before installation;
4. the installed source/build payload corresponds to accepted repair SHA `231761f...` through available hashes/fingerprint evidence;
5. OpenClaw remains `2026.7.1-2` — no upstream upgrade or patch occurred;
6. no unrelated plugin/runtime ownership drift was introduced.

Do not infer provenance merely from installer success text. Installed-state evidence must independently match the frozen candidate.

## Mandatory post-install health proof

Verify at minimum:

- controller/managed state appropriate;
- Gateway healthy/listening as expected;
- Ollama/provider healthy and ready;
- startup adapter healthy/ready;
- CogentNexus plugin enabled and loaded;
- recovery health ready/acceptable;
- delivery health ready/acceptable and no unexpected claimable pending assistant delivery;
- storage/database integrity valid (`PRAGMA integrity_check` or repository-supported equivalent);
- relevant system/plugin/OpenClaw/Gateway/model/storage/resource checks pass;
- bounded logs contain no new unexplained CogentNexus ERROR/FATAL attributable to install-over;
- pre/post durable-state counts are reconciled and no semantic Ticket/result/delivery work was manufactured by this task.

Transient restart/startup warnings are not automatic failures if their lifecycle is explained and the final state is independently healthy.

## Absolute hard fence

This task does **not** authorize:

- any Dashboard semantic Send, Enter submission, prompt, or semantic UI interaction;
- `chat.inject` or equivalent semantic injection;
- any intentional model inference/regeneration request;
- manual Ticket/workflow/result/outbox/delivery/database/transcript mutation;
- uninstall;
- clean reinstall;
- reset;
- a second install-over attempt;
- OpenClaw upgrade/patch;
- dependency upgrade unrelated to the supported frozen package build;
- production source repair;
- release/tag/package publication;
- default/release merge;
- force push.

Read-only Dashboard observation is allowed only if needed for health evidence and must not submit semantic input.

## PASS criteria

All must be proven:

1. exact accepted candidate and package provenance established before installation;
2. exactly one supported install-over executed;
3. no unauthorized retry/lifecycle workaround occurred;
4. installed fingerprint equals candidate fingerprint;
5. OpenClaw remains pinned at `2026.7.1-2`;
6. plugin enabled/loaded and ownership/provenance checks pass;
7. controller/Gateway/provider/startup/recovery/delivery/storage health is acceptable after installation;
8. database integrity is valid and durable state changes are reconciled;
9. no semantic Dashboard Send/model inference/manual semantic mutation occurred;
10. no unexplained new critical runtime error remains;
11. report satisfies `EXECUTOR_REPORT_CONTRACT.md`, including acceptance matrix and Reviewer Verification Packet.

## Failure handling

If any PASS criterion cannot be proven, do not attempt semantic acceptance and do not self-repair beyond the exact Task-170 authority. Analyze the evidence, identify likely cause/smallest next repair or evidence scope, publish the matching report, and stop.

## Required report

Publish exactly:

`docs/operations/coordination/reports/CNX-20260831-170-hermes-windows-install-over-provenance-health.md`

The report must include the standing contract plus a Reviewer Verification Packet prioritizing:

1. exact accepted source/package binding;
2. exactly-one installer execution;
3. candidate vs installed fingerprint equality;
4. pinned OpenClaw preservation;
5. post-install plugin/runtime health;
6. recovery/delivery pending-state proof;
7. DB integrity/state reconciliation;
8. hard-fence compliance, especially zero semantic Sends/inference requests.

After publishing the matching report, stop. Task 170 does not authorize a successor semantic Send.
