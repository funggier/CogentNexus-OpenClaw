# CNX-20260918-409 — Runtime Attestation Local Build and Test Qualification

Status: `READY_FOR_HERMES`

## Authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Parent: `CNX-20260918-408`
- Executor: `Hermes`
- Reviewer: `ChatGPT`
- Human final authority: `Operator`
- Base report: `docs/operations/coordination/reports/CNX-20260918-408-live-hook-runner-runtime-attestation-surface-report.md`

GitHub remote is authoritative. Re-fetch the branch and re-read ACTIVE/STATUS before execution. Do not trust an embedded SHA if the remote has moved.

## Objective

Qualify the new read-only runtime hook attestation implementation on the operator's local development checkout using the exact pinned OpenClaw development dependency.

This task is local source/build/test qualification only.

Do not install or deploy the candidate into the production OpenClaw extension in this task.

## Candidate changes

Expected implementation surfaces include:

- `plugins/cogentnexus-openclaw/src/v095-runtime-hook-attestation.ts`
- `plugins/cogentnexus-openclaw/src/v095-runtime-hook-attestation.test.ts`
- `plugins/cogentnexus-openclaw/src/v091-release-entry.ts`

Gateway RPC:

`cogentnexus.runtimeAttestation`

Expected scope:

`operator.read`

## Required checks

From the plugin package directory, use the repository's normal toolchain and exact dependency lock/state.

At minimum run:

1. focused attestation test;
2. TypeScript/plugin build;
3. `plugin:validate`;
4. relevant focused regression tests:
   - runtime attestation;
   - release-entry/wiring;
   - model-selection boundary;
   - provider-independent capabilities;
5. inspect the resulting built `dist/v091-release-entry.js` and related emitted module to verify the RPC is packaged;
6. confirm the public OpenClaw SDK import resolves from the pinned `openclaw@2026.7.1-2` dependency.

If the exact commands differ because the current repository scripts changed, use the current package scripts and record them exactly.

## TDD evidence

Record:

- the RED test commit from CNX-408;
- current candidate implementation commit lineage;
- actual focused-test result;
- build result;
- validation result;
- any repair required.

If a source defect is found, a minimal repository repair is authorized inside CNX-409 using RED -> minimal fix -> GREEN, provided it does not alter provider routing, Ticket semantics, or production runtime.

## Hard fences

- No production extension install/install-over.
- No production artifact replacement.
- No Gateway restart/reload.
- No production config/environment/Scheduled Task mutation.
- No live Gateway RPC call.
- No semantic/model/provider request.
- No provider/model/auth/routing change.
- No TicketStore/durable-state mutation.
- No OpenClaw dependency patch/version change.
- No release/tag/main.
- No force push/history rewrite.
- Do not create/start CNX-410 yourself.

## Exit classification

Use one:

- `RUNTIME_ATTESTATION_LOCAL_VALIDATION_GREEN`
- `RUNTIME_ATTESTATION_LOCAL_REPAIR_GREEN`
- `RUNTIME_ATTESTATION_LOCAL_VALIDATION_FAILED`
- `BLOCKED_BY_LOCAL_DEPENDENCY_STATE`

## Closeout

Publish:

`docs/operations/coordination/reports/CNX-20260918-409-runtime-attestation-local-build-test-qualification-report.md`

Then set ACTIVE/STATUS to `WAITING_FOR_CHATGPT_REVIEW`, verify local HEAD equals remote HEAD, verify clean worktree, and stop.

Do not deploy or call the live RPC.
