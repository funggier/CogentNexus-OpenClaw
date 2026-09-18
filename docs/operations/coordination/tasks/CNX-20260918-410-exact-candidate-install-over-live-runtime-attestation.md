# CNX-20260918-410 — Exact Candidate Install-Over and Live Runtime Attestation

Status: `READY_FOR_HERMES`

## Authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Parent: `CNX-20260918-409`
- Executor: `Hermes`
- Reviewer: `ChatGPT`
- Human final authority: `Operator`
- Parent review: `docs/operations/coordination/reviews/CNX-20260918-409-chatgpt-review.md`
- Qualified source candidate: `3d27ee85ff84ff2bf80d537e9046fb25e7a260ff`
- Parent report: `docs/operations/coordination/reports/CNX-20260918-409-runtime-attestation-local-build-test-qualification-report.md`

GitHub remote is authoritative for coordination state. The exact product/source candidate for installation is frozen at `3d27ee85ff84ff2bf80d537e9046fb25e7a260ff`.

## Objective

Perform one bounded production install-over of the exact CNX-409-qualified candidate, allow only normal installer-owned Gateway/runtime convergence, then call the new read-only Gateway RPC exactly once:

`cogentnexus.runtimeAttestation`

No semantic/model/provider request is authorized in this task.

The purpose is to answer one production question:

> Does the running Gateway's live composed hook runtime attest CogentNexus `before_agent_run` as PRESENT after installing the qualified candidate?

## Expected qualified artifact evidence

From CNX-409:

- OpenClaw pinned dependency: `2026.7.1-2`
- candidate `dist/v091-release-entry.js` SHA-256:
  `343c221db6d9259fb38bb335cf5f3293bb838a7515a909666471b990da056f4b`
- candidate `dist/v095-runtime-hook-attestation.js` SHA-256:
  `90d3d95064f1a11b483ce0725dc5782cbaf7fdb6533f1f8b5f443c3da3f33a1d`
- RPC: `cogentnexus.runtimeAttestation`
- RPC scope: `operator.read`

Fresh exact-candidate build output may be recomputed during installer execution, but if these deterministic emitted hashes differ before mutation, stop and classify source/build drift rather than installing an unexplained candidate.

## Phase A — fresh authority and source binding

Before live mutation:

1. fetch current coordination branch;
2. re-read ACTIVE, STATUS, this task, CNX-409 report/review;
3. require CNX-410 remains the active `READY_FOR_HERMES` task;
4. verify `3d27ee85ff84ff2bf80d537e9046fb25e7a260ff` is an ancestor of current coordination HEAD;
5. compare candidate -> current HEAD;
6. require post-candidate drift to be coordination/review/task documentation only; any product/source/test/install-script drift is `BLOCKED_PREFLIGHT_DRIFT`;
7. create/use a fresh disposable checkout pinned exactly to `3d27ee85ff84ff2bf80d537e9046fb25e7a260ff`;
8. prove exact HEAD and clean checkout;
9. verify current `scripts/install.ps1` comes from that exact candidate.

Do not install from a mutable working tree.

## Phase B — read-only production preflight

Capture before-state without mutation:

- controller mode/generation;
- CogentNexus Host/Supervisor/doctor state;
- Gateway endpoint/health/PID;
- OpenClaw version;
- installed plugin id/version/path/source/status;
- installed `dist/v091-release-entry.js` hash;
- presence/hash of any existing attestation module;
- current provider/model configuration or selected default state needed only to prove it remains unchanged;
- Delivery READY state and pending outbox count;
- Recovery READY state and any emittable unresolved recovery;
- SQLite integrity;
- relevant OpenClaw/CogentNexus/Ollama process inventory.

Do not print credentials, tokens, API keys, or unrelated secret-bearing config.

## Phase C — delivery/recovery hazard gate

Require before installer start:

```text
pending outbox = 0
no emittable unresolved recovery
no unexplained active/nonterminal lineage likely to produce delivery during install
SQLite integrity = OK
```

If unsafe or ambiguous:

`BLOCKED_DELIVERY_HAZARD`

Do not mutate Ticket/outbox/recovery/SQLite state to force the gate.

## Phase D — exact single install-over

Use the repository's established ownership-safe installer path from the exact detached candidate:

`scripts/install.ps1`

Use the proven authenticated Windows execution topology already established for this project. If elevation requires the existing Scheduled Task execution pattern, use that pattern; do not invent a second installation mechanism.

Do not use:

- `-SkipPlugin`
- `-SkipGatewayRestart`
- `-SkipAgentsPolicy`
- `-LinkPlugin`

Authorized live product mutations are limited to the single normal installer transaction, including its own native handoff, plugin replacement/rollover, Gateway restart, and managed convergence.

Cardinality:

- installer successful starts: maximum 1;
- installer invocations: exactly 1 if start occurs;
- installer retry after process start: 0;
- manual plugin copy/replace: 0;
- manual Gateway repair: 0;
- manual lifecycle repair: 0;
- manual Ticket/DB repair: 0.

If installer fails after start, preserve exact evidence and stop.

## Phase E — post-install exact identity

Only after installer success, prove:

- installer exit code = 0;
- live plugin id/version/path/source coherent;
- installed release entry SHA-256 =
  `343c221db6d9259fb38bb335cf5f3293bb838a7515a909666471b990da056f4b`;
- installed attestation module SHA-256 =
  `90d3d95064f1a11b483ce0725dc5782cbaf7fdb6533f1f8b5f443c3da3f33a1d`;
- `cogentnexus.runtimeAttestation` string exists in installed emitted module;
- OpenClaw remains `2026.7.1-2`;
- provider/model configuration observed in preflight is unchanged;
- controller converges coherently to managed/active state expected by current v0.9.5 semantics;
- Gateway becomes healthy;
- Delivery remains READY with pending outbox 0;
- Recovery remains READY with no new replay/resend;
- SQLite integrity remains OK.

If installed identity differs:

`FAIL_INSTALLED_CANDIDATE_IDENTITY`

No manual correction in this task.

## Phase F — live read-only runtime attestation

After Gateway health is established, invoke exactly once through the supported OpenClaw CLI:

```text
openclaw gateway call cogentnexus.runtimeAttestation --params '{}' --json
```

Record exact stdout/stderr, exit code, UTC time, Gateway PID, installed artifact hashes, and response.

This RPC is observation-only. Do not invoke `before_agent_run`, do not send a chat prompt, and do not call any model/provider route.

Expected response fields include:

- `schemaVersion`
- `pluginId`
- `hookName`
- `runnerReady`
- `globalHookCount`
- `latestRegistryPluginHookCount`
- `classification`

Expected successful classification:

`PRESENT`

### Result handling

If:

`classification = PRESENT`

-> classify:

`PASS_LIVE_RUNTIME_ATTESTATION_PRESENT`

and stop.

If:

`classification = ABSENT`

-> classify:

`FAIL_LIVE_RUNTIME_ATTESTATION_ABSENT`

and stop.

If:

`classification = AMBIGUOUS`

-> classify:

`BLOCKED_LIVE_RUNTIME_ATTESTATION_AMBIGUOUS`

and stop.

If:

`classification = RUNNER_UNAVAILABLE`

-> classify:

`FAIL_LIVE_RUNTIME_ATTESTATION_RUNNER_UNAVAILABLE`

and stop.

If the RPC method is unavailable despite exact installed identity:

`FAIL_LIVE_RUNTIME_ATTESTATION_RPC_UNAVAILABLE`

and stop.

Do not send a semantic request under any non-PRESENT result.

## Read-only observation retry policy

Gateway health/status polling needed to establish post-restart readiness is allowed and does not count as an attestation call.

The attestation RPC itself must be called exactly once after health is established.

Do not retry the attestation RPC in this task. A transport failure is evidence and should be reported.

## Hard fences

- Semantic Web Chat submissions: 0
- Ollama semantic/model requests: 0
- OpenAI semantic/model requests: 0
- provider/model selection changes: 0
- provider credential/auth mutation: 0
- manual Ticket/outbox/recovery/SQLite mutation: 0
- manual durable delivery/replay: 0
- manual plugin copy/replace/rename/delete: 0
- manual Gateway restart after installer execution: 0
- manual runtime/lifecycle repair: 0
- OpenClaw dependency patch/version change: 0
- release/tag/main: 0
- force push/history rewrite: 0
- CNX-411 created/started: 0

## Allowed classifications

- `PASS_LIVE_RUNTIME_ATTESTATION_PRESENT`
- `BLOCKED_PREFLIGHT_DRIFT`
- `BLOCKED_SOURCE_BINDING`
- `BLOCKED_DELIVERY_HAZARD`
- `FAIL_INSTALLER_TERMINAL`
- `FAIL_INSTALLED_CANDIDATE_IDENTITY`
- `FAIL_MANAGED_CONVERGENCE`
- `FAIL_POST_INSTALL_HEALTH`
- `FAIL_LIVE_RUNTIME_ATTESTATION_ABSENT`
- `BLOCKED_LIVE_RUNTIME_ATTESTATION_AMBIGUOUS`
- `FAIL_LIVE_RUNTIME_ATTESTATION_RUNNER_UNAVAILABLE`
- `FAIL_LIVE_RUNTIME_ATTESTATION_RPC_UNAVAILABLE`
- `BLOCKED_EVIDENCE`

## Required report

Publish:

`docs/operations/coordination/reports/CNX-20260918-410-exact-candidate-install-over-live-runtime-attestation-report.md`

Include:

- fresh GitHub authority;
- exact candidate/source binding;
- preflight;
- delivery/recovery hazard gate;
- installer attempt ledger;
- exact installer path/command/result;
- installed artifact hashes;
- managed convergence evidence;
- Gateway health/PID;
- exact one-shot RPC command/result;
- full attestation response;
- semantic/model request counts explicitly zero;
- effect/cardinality ledger;
- final classification.

Then update ACTIVE/STATUS to `WAITING_FOR_CHATGPT_REVIEW`, verify local/remote HEAD equality and clean worktree, and stop.

Do not create/start CNX-411.
