# CNX-20260829-139 — Repaired Candidate Install-Over and Health Proof

- Status: `READY_FOR_HERMES`
- Execution mode: `LIVE_WINDOWS_REPAIRED_CANDIDATE_INSTALL_OVER_AND_HEALTH_PROOF_ONLY`
- Owner / independent reviewer: ChatGPT
- Executor: Hermes/Codex after operator continuation
- Date: 2026-08-29 ICT
- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`

## Purpose

Deploy the independently accepted Task-138 source repair to the established Windows runtime using one controlled supported install-over, then prove exact package/install provenance and a clean post-install runtime state **without sending any new Dashboard semantic message**.

This task separates deployment mutation from the later exactly-once Dashboard acceptance ledger. It is not a semantic delivery acceptance task.

## Authority

Task-138 report:

`docs/operations/coordination/reports/CNX-20260829-138-dashboard-direct-result-durable-capture-repair.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260829-138-dashboard-direct-result-durable-capture-repair-review.md`

Accepted repaired source candidate:

`16f5c396e9be0af8d1bd34824fe2993613501a6f`

Pre-repair installed payload/plugin fingerprint from Task 137:

`3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`

Historical Task-137 Ticket:

`CNXT-a38e1408-205f-4606-a5c8-ec54e9515aea`

Task-137 Send ledger remains permanently consumed `1 / 1`. Its nonce/message/Ticket must never be resent or reused.

## Phase 0 — fresh authority and pre-install safety baseline

Before any mutation:

1. fresh-fetch branch HEAD, `ACTIVE.md`, `STATUS.md`, Task 139, Task-138 report, and Task-138 review;
2. confirm Task 139 remains active and unsuperseded;
3. confirm exact repaired source candidate `16f5c396e9be0af8d1bd34824fe2993613501a6f` is reachable and the source/test diff remains the independently reviewed Task-138 repair only;
4. identify the established supported packaging/install-over procedure from repository scripts/docs rather than improvising a new installer path;
5. inspect the installed runtime read-only before install-over.

Required pre-install live state:

- controller mode `managed`;
- desired Gateway/provider `running` / `running`;
- selected provider `ollama`;
- recovery verdict exactly `READY`;
- delivery verdict exactly `READY`;
- `pendingOutbox=0`;
- `nonterminalTickets=0`;
- no active direct model call, workflow, direct recovery, outbound send, install transition, or other unexplained semantic execution;
- Gateway healthy;
- Ollama healthy/ready;
- OpenClaw remains `2026.7.1-2`;
- exactly one CogentNexus-OpenClaw plugin identity in the accepted runtime path;
- authoritative SQLite exists and `PRAGMA integrity_check` is exactly `ok` using a read-only URI;
- Task-136 and Task-137 historical failed Tickets remain present and terminal;
- no historical Task-137 retry/outbox/assistant-delivery/direct-recovery mutation has appeared;
- currently installed payload fingerprint is proven and compared against the Task-137 baseline `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`.

If active/nonterminal/pending semantic work, unexplained source/runtime drift, an unsafe controller state, or an unexpected installed identity is present, stop `BLOCKED_BEFORE_INSTALL`. Do not normalize or clean.

## Phase 1 — exact candidate build/package provenance

Prepare the deployable package from **exact source commit**:

`16f5c396e9be0af8d1bd34824fe2993613501a6f`

Use an isolated clean checkout/worktree or equivalent exact-commit source root. Do not build from a moving branch working tree unless the exact commit identity is positively proven first.

Before install-over, capture:

- exact source commit;
- clean/expected source diff state;
- Node/npm versions used;
- package/build commands;
- package filename, size, and SHA-256;
- package-content verification result;
- plugin build/validation result required by the established installer path;
- any installer artifact hash or manifest identity used to deploy.

The artifact must contain the Task-138 repaired `v091-dashboard-verified-delivery` behavior. Do not edit production source during Task 139.

## Phase 2 — controlled install-over

Perform exactly one supported **install-over/update** of the currently installed CogentNexus-OpenClaw payload using the repository's established installation/package procedure.

Requirements:

- install over the existing product; do not clean uninstall first;
- do not run reset;
- preserve the authoritative `.cogentnexus-openclaw` durable state;
- preserve Task-136/137 historical Ticket/event/model-call evidence;
- allow only lifecycle transitions that are part of the established installer/update procedure and record each one;
- do not manually delete plugin/runtime/database state to make installation pass;
- do not change provider/model/OpenClaw configuration;
- do not send semantic messages before, during, or after installation.

If the established install-over procedure unexpectedly requires destructive cleanup, reset, data deletion, reboot, or a semantic test message, stop and report `BLOCKED_INSTALL_PROCEDURE_CONFLICT` instead of improvising.

## Phase 3 — installed provenance proof

After install-over, prove that the loaded/installed payload is the artifact built from exact repaired candidate `16f5c396e9be0af8d1bd34824fe2993613501a6f`.

Capture at minimum:

- final installed plugin path;
- installed package/payload fingerprint using the same accepted fingerprint method used by prior acceptance tasks;
- package/artifact SHA-256 and its relationship to the installed payload;
- version metadata;
- relevant repaired source/dist file hash or equivalent package-manifest evidence sufficient to distinguish the new repaired payload from the old fingerprint;
- exactly one loaded/enabled CogentNexus-OpenClaw plugin;
- no stale duplicate plugin copy taking runtime authority.

The new installed fingerprint must be reported explicitly. If the effective installed payload is indistinguishable from the old pre-repair fingerprint or provenance to `16f5c396...` cannot be proven, classify `FAIL_PROVENANCE` and do not proceed to semantic acceptance.

## Phase 4 — post-install health proof

After the installer has converged, perform read-only health/evidence collection through the installed launcher/runtime.

Require:

- mode `managed`;
- desired Gateway/provider `running` / `running`;
- selected provider `ollama`;
- Gateway healthy and connected on the expected local endpoint;
- Ollama healthy/ready;
- OpenClaw `2026.7.1-2` unchanged;
- recovery exactly `READY` with no active provider incident/circuit/unsafe transition;
- delivery exactly `READY`;
- `pendingOutbox=0`;
- `nonterminalTickets=0`;
- no active direct-model call, workflow, direct-recovery, or outbound delivery operation;
- SQLite `PRAGMA integrity_check=ok` through read-only URI;
- historical Task-136 and Task-137 failed Tickets and their durable event/model-call evidence preserved;
- no new semantic Ticket created by installation itself;
- no new assistant-delivery/outbox/direct-recovery semantic work caused by installation itself;
- no unexplained duplicate process/plugin/runtime authority.

Do not clean historical failure records after proving health.

## PASS criteria

Task 139 passes only if all of the following are proven:

- exact repaired source candidate `16f5c396e9be0af8d1bd34824fe2993613501a6f` was the build/package source;
- build/package provenance and SHA-256 are captured;
- one supported install-over completed without destructive cleanup/reset;
- effective installed payload provenance points to the repaired candidate;
- a new installed payload fingerprint is captured and distinguished from the pre-repair baseline;
- runtime returns to coherent managed/Ollama running state;
- Gateway/Ollama/recovery/delivery/SQLite/plugin health is GREEN;
- `pendingOutbox=0` and `nonterminalTickets=0`;
- Task-136/137 historical evidence remains preserved;
- installation created no semantic Ticket/delivery/recovery side effect;
- no Dashboard semantic Send occurred.

## Failure discipline

Use the first applicable exact classification:

- `BLOCKED_BEFORE_INSTALL` — unsafe or unexplained pre-install state;
- `BLOCKED_INSTALL_PROCEDURE_CONFLICT` — supported install path requires an action outside this task;
- `FAIL_BUILD_OR_PACKAGE` — exact repaired candidate cannot produce the required validated artifact;
- `FAIL_INSTALL_OVER` — supported install-over fails or does not converge;
- `FAIL_PROVENANCE` — effective installed payload cannot be proven to originate from the repaired candidate;
- `FAIL_POST_INSTALL_HEALTH` — install succeeds but required runtime health/integrity/pending-state gates fail;
- `PASS` — all criteria above proven.

No failure class authorizes cleanup, reset, reinstall, or a semantic test under Task 139.

## Required report

Publish exactly:

`docs/operations/coordination/reports/CNX-20260829-139-repaired-candidate-install-over-and-health-proof.md`

Include:

- Task ID, start HEAD, branch, and ACTIVE verification;
- exact repaired candidate SHA;
- pre-install runtime health and installed fingerprint;
- exact build/package commands and artifact SHA-256/provenance;
- exact install-over command/procedure and installer exit/result evidence;
- all installer-owned lifecycle transitions actually observed;
- final installed path/fingerprint/version/provenance proof;
- post-install Gateway/Ollama/recovery/delivery/SQLite/plugin/Ticket/outbox/assistant-delivery/recovery state;
- historical Task-136/137 preservation proof;
- semantic-side-effect accounting proving zero Dashboard/alternate semantic sends;
- exact PASS/FAIL/BLOCKED classification;
- exact final repository HEAD used for the report.

Then STOP for independent ChatGPT review.

Do not automatically open or execute the final Dashboard semantic re-acceptance.

## Hard fence

Task 139 authorizes only the exact repaired-candidate build/package, one supported install-over, installer-required lifecycle convergence, and read-only provenance/health evidence.

Forbidden:

- any Dashboard semantic Send/resend;
- reuse of Task-136/137 acceptance message or nonce;
- alternate semantic injection via CLI/Gateway/API/database/test harness;
- clean uninstall;
- reset;
- manual runtime/database/plugin cleanup or normalization;
- manual Ticket/workflow/outbox/ack/delivery/recovery mutation;
- recovery/crash injection;
- provider/model/OpenClaw configuration mutation;
- unrelated process kill or scheduled-task/service mutation;
- reboot unless a future separately reviewed task explicitly authorizes it;
- credential/secret access;
- merge/tag/GitHub Release;
- force push.
