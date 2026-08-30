# CNX-20260830-165 — Hermes Windows Install-Over Provenance + Health Checkpoint

Status: `READY_HERMES`

Execution mode: `WINDOWS_REPAIRED_CANDIDATE_INSTALL_OVER_PROVENANCE_HEALTH_HERMES`

Current authorization: `CNX-20260830-165_HERMES_WINDOWS_REPAIRED_CANDIDATE_INSTALL_OVER_PROVENANCE_HEALTH`

Task ID: `CNX-20260830-165`

Updated: 2026-08-30 ICT

Executor: Hermes

Coordinator / final reviewer: ChatGPT

Review type at completion: ChatGPT review required before any Dashboard semantic reacceptance

## Purpose

Install-over the accepted repaired CogentNexus-OpenClaw candidate on the real Windows machine and prove exact candidate provenance plus runtime health **without sending any semantic Dashboard message**.

This task exists only because Task 164 was accepted by ChatGPT review as the repository-native transcript authority repair checkpoint.

Parent repair:

`docs/operations/coordination/tasks/CNX-20260830-164-hermes-native-transcript-authority-red-to-green.md`

Task-164 report:

`docs/operations/coordination/reports/CNX-20260830-164-hermes-native-transcript-authority-red-to-green.md`

Task-164 ChatGPT acceptance:

`docs/operations/coordination/reviews/CNX-20260830-164-hermes-native-transcript-authority-red-to-green-review.md`

## Authoritative candidate

Repository:

`funggier/CogentNexus-OpenClaw`

Branch:

`agent/v0.9.3-full-stabilization`

Accepted production repair SHA:

`80b87dfbe0d9176e421f3748b4cee0827db12d0c`

Task-164 report publication SHA:

`a9eccaba3d3acd46530cd59d256a6b13702b29ef`

Task-164 review publication SHA:

`3a8caf12f8d7fc2cd03687ce088d01ccf790a5c0`

Production behavior to be installed is the tree containing repair commit `80b87df...`; later documentation-only coordination commits do not change the product payload.

Pinned intended OpenClaw target remains:

- version: `v2026.7.1-2`
- upstream commit: `0790d9f593ad30c940ed93b5872a8cf6d6f3cf8c`

Do not upgrade or patch OpenClaw in this task.

## Required reading before work

Read fresh from GitHub immediately before execution:

1. `docs/operations/coordination/ACTIVE.md`
2. `docs/operations/coordination/STATUS.md`
3. this Task 165 file
4. Task-164 report
5. Task-164 ChatGPT review
6. current installer/package documentation and scripts actually used by the repository

GitHub remote branch state is authoritative. Do not trust a stale local checkout or a SHA copied from this file if GitHub has moved unexpectedly.

## Objective

Prove all of the following before semantic testing is allowed:

1. the install-over input was built from the accepted repaired candidate;
2. the real Windows machine installed that candidate successfully over the existing installation;
3. installed CogentNexus-OpenClaw files/package provenance correspond to the intended candidate and are not stale from an older build;
4. OpenClaw remains on the intended pinned version unless current GitHub coordination explicitly says otherwise;
5. CogentNexus plugin/package loads successfully;
6. schema/bootstrap/status/health remain coherent after install-over;
7. no semantic Dashboard input was sent;
8. no unrelated live mutation was performed.

This is a provenance/health checkpoint, not a functional semantic acceptance test.

## Preflight

Before any live mutation:

1. re-fetch `ACTIVE.md` and `STATUS.md`;
2. confirm Task 165 remains the only active live authorization;
3. capture current remote branch HEAD;
4. inspect the accepted repair ancestry and identify the exact product tree/package source to install;
5. capture current installed CogentNexus/OpenClaw provenance and health before install-over;
6. capture enough pre-state to distinguish old installation from repaired candidate after install-over;
7. confirm no Dashboard semantic test will be performed in this task.

If the local source/build input cannot be proven to derive from the accepted candidate, stop rather than installing an ambiguous build.

## Install-over authorization

Hermes is authorized to perform the normal supported **install-over** path on the real Windows machine using the accepted repaired candidate.

Do not uninstall first unless the supported install-over path itself proves impossible and ChatGPT separately authorizes a lifecycle change. This task is specifically an install-over checkpoint.

Normal service/runtime transitions that are an unavoidable part of the supported installer are allowed. Do not independently restart or mutate unrelated services merely for experimentation.

## Provenance evidence required after install-over

Capture durable evidence sufficient to answer these questions exactly:

### A. What was installed?

- source repository and branch;
- exact source/product SHA used for package construction;
- package/archive identity if applicable;
- package hash or equivalent immutable artifact identifier;
- installer command/path used;
- installation result/exit status.

### B. What is now present on disk?

At minimum, verify the installed CogentNexus-OpenClaw plugin/package contains the repaired native transcript authority implementation rather than an older copy.

Prefer deterministic hashes/manifest/package metadata over timestamps alone.

Where practical, compare installed file hashes for the repaired production surface against the source/package artifact, especially:

`plugins/cogentnexus-openclaw/src/v091-dashboard-verified-delivery.ts`

or its built/packed runtime equivalent.

Do not claim provenance solely because an installer returned success.

### C. What OpenClaw target is active?

Record the actual installed/running OpenClaw version and relevant provenance. It must remain the intended `v2026.7.1-2` target unless current coordination explicitly authorizes another version.

### D. Is CogentNexus healthy?

Collect non-semantic health/status evidence sufficient to show:

- plugin load succeeds;
- required CogentNexus schema/bootstrap is valid;
- no immediate plugin initialization exception;
- Gateway/CogentNexus status is coherent;
- runtime is not stuck in an installer-induced broken state;
- no unexpected pending semantic delivery was created by the checkpoint itself.

Use status/health/diagnostic commands only. Do not create a semantic user Ticket merely to test health.

## Dashboard semantic hard fence

Absolutely no semantic Dashboard Send is authorized in Task 165.

Do not:

- click Send with semantic input;
- press Enter in a semantic Dashboard composer;
- paste/type a test prompt and submit it;
- use another live OpenClaw surface to simulate the same semantic acceptance;
- inject a synthetic assistant/user semantic message;
- manually create a Ticket/result/delivery row to imitate a Send.

Merely opening/observing the Dashboard or reading status is acceptable only if it does not submit semantic input or mutate delivery state.

## Additional hard fence

Do not:

- uninstall/reinstall/reset unless separately authorized;
- patch OpenClaw source;
- upgrade OpenClaw or dependencies;
- manually edit live Ticket/workflow/result/outbox/delivery/database state;
- delete arbitrary live state;
- perform unrelated CogentNexus feature changes;
- publish a release/tag/package;
- merge to default/release branch;
- force push.

If install-over reveals a source/installer defect, stop the live acceptance path and report it. Repository repair must then be handled as a separate TDD task.

## Success criteria

Task 165 may report `PASS` only when all of the following are true:

1. accepted repaired candidate lineage is proven;
2. install-over completed successfully;
3. installed artifact/file provenance proves the repaired candidate is actually present;
4. intended OpenClaw version/provenance is confirmed;
5. CogentNexus plugin loads and health/status checks are coherent;
6. no semantic Dashboard Send occurred;
7. no prohibited mutation occurred;
8. evidence is sufficient for independent ChatGPT review.

Use `FAIL` if a defect is demonstrated.

Use `BLOCKED` if provenance cannot be established safely or an external machine/installer constraint prevents the checkpoint from being completed without violating the fence.

Do not convert ambiguity into PASS.

## Required completion report

Create:

`docs/operations/coordination/reports/CNX-20260830-165-hermes-windows-install-over-provenance-health.md`

The report must include:

1. exact starting GitHub HEAD;
2. pre-install installed-state provenance;
3. exact candidate/package source and artifact identity;
4. install-over command/path and result;
5. post-install installed-file/package provenance;
6. actual OpenClaw version/provenance;
7. CogentNexus plugin/schema/bootstrap/status/health evidence;
8. any service/runtime transition caused by the supported installer;
9. explicit statement that no semantic Dashboard Send occurred;
10. hard-fence compliance statement;
11. exact final GitHub HEAD before report publication;
12. `PASS` / `FAIL` / `BLOCKED`;
13. recommended next action for ChatGPT review.

## Acceptance gate

Even a Task-165 `PASS` report does not authorize a Dashboard Send on its own.

ChatGPT must review the report and evidence first.

Only after explicit ChatGPT acceptance may coordination open a separate exactly-one-Send Dashboard durable-delivery reacceptance task against this proven installed candidate.
