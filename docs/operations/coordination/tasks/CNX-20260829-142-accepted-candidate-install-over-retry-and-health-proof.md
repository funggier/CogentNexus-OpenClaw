# CNX-20260829-142 — Accepted Candidate Install-Over Retry and Health Proof

Status: `READY_FOR_HERMES`
Execution mode: `CONTROLLED_ACCEPTED_CANDIDATE_INSTALL_OVER_RETRY_AND_HEALTH_PROOF`
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation
Opened: 2026-08-29 ICT

## Objective

Perform exactly one controlled supported live Windows install-over retry from the independently accepted exact source candidate, then prove installation provenance and runtime health without sending any Dashboard semantic message.

This task is the deployment proof for the combined accepted repair lineage:

- Dashboard durable direct-result capture repair: `16f5c396e9be0af8d1bd34824fe2993613501a6f`;
- direct retired-plugin ownership repair: `4d47629edeb8b4e0ab23f1fabee98c05f702d141`;
- root-level indirection safety repair: `138759d111fe27a0cda75f59ad108d11caf19120`.

The exact deployment source candidate is:

`138759d111fe27a0cda75f59ad108d11caf19120`

Use a detached/fresh worktree or clone at that exact commit. Do not run the installer from a coordination-only branch tip.

## Accepted predecessor state

Task 139 performed one supported install-over from the earlier Dashboard candidate and failed closed before plugin replacement at the ownership-safe rollover boundary.

Accepted post-failure evidence from Task 139:

- controller: `passthrough`;
- exactly one CogentNexus-OpenClaw plugin identity, disabled;
- effective installed plugin fingerprint remained the old baseline `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`;
- Gateway healthy;
- Ollama healthy/ready;
- system/recovery/delivery read-only checks READY;
- SQLite integrity `ok`;
- pending outbox `0`;
- historical Task-136/137 evidence preserved;
- no new semantic Ticket/delivery/recovery state from the failed installer attempt.

That state was intentionally not normalized by Tasks 140/141.

## Phase 0 — Fresh authority and drift gate

Before any live mutation:

1. verify fresh GitHub branch/coordination state and confirm Task 142 is active and unsuperseded;
2. create/fetch an exact detached source tree at `138759d111fe27a0cda75f59ad108d11caf19120`;
3. prove the exact source ancestry includes `16f5c396...`, `4d47629e...`, and `138759d...`;
4. perform read-only live state capture;
5. compare the observed state with the accepted Task-139 post-failure boundary.

Record at minimum:

- controller mode;
- desired Gateway/provider state;
- Gateway health/version;
- Ollama health/selected provider readiness;
- OpenClaw version;
- plugin inventory: identity, enabled/status, root path;
- installed plugin payload fingerprint;
- installed `workspace/skills/cogentnexus-openclaw/scripts/namespace_ownership.py` hash if present;
- ownership manifest state/path;
- SQLite integrity;
- Ticket/event/model-call/outbox/assistant-delivery/recovery counts needed to prove semantic preservation;
- pending outbox count.

### Drift rule

Do not require byte-for-byte equality with Task 139 for ordinary timestamps or benign read-only metadata, but any material lifecycle/ownership/semantic drift must stop the task before mutation.

Examples of material drift:

- plugin unexpectedly enabled, replaced, missing, duplicated, or moved to an unproven path;
- controller unexpectedly `managed` or otherwise inconsistent with accepted post-failure state;
- ownership manifest incoherent;
- new pending semantic delivery/outbox work;
- SQLite integrity failure;
- Gateway/provider state inconsistent in a way that makes supported install-over unsafe;
- new ambiguous plugin/npm-wrapper ownership evidence.

Classification: `BLOCKED_LIVE_STATE_DRIFT`.

Do **not** manually normalize the state to make the installer runnable.

## Phase 1 — Exact candidate build/package provenance

From the exact detached source candidate:

1. record exact Git SHA and clean source status;
2. record Node/npm/Python/PowerShell environment relevant to packaging/install;
3. run the required package/build validation used by the supported installer path;
4. produce the exact candidate plugin package;
5. record package filename, size, SHA-256, packed file count;
6. compute candidate plugin payload fingerprint with the repository ownership tool;
7. compute SHA-256 of candidate `skills/cogentnexus-openclaw/scripts/namespace_ownership.py`;
8. retain provenance evidence in the report.

Do not substitute a package from a previous task.

## Phase 2 — One supported install-over attempt

If and only if Phase 0 is coherent and Phase 1 provenance is complete, invoke the supported installer exactly once from the exact candidate source:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File <exact-candidate-worktree>/scripts/install.ps1 -Workspace C:/Users/CDQ-P/.openclaw/workspace
```

Rules:

- no manual plugin enable/disable before the installer;
- no manual controller-mode change before the installer;
- no manual deletion/replacement of the extension directory;
- no manual ownership-manifest edits;
- no direct `openclaw plugins install` substitute outside the supported installer;
- no retry if the installer returns nonzero;
- no cleanup/reset/uninstall after a failed attempt in this task;
- preserve the installer's own fail-closed behavior.

The current `passthrough` / disabled predecessor state is part of the supported retry input. If the supported installer cannot safely proceed from it, record the exact failure and stop.

Failure classification: `FAIL_INSTALL_OVER` unless a narrower explicit blocker applies.

## Phase 3 — Post-install provenance proof

If the installer exits successfully, prove the effective installed state rather than inferring success from exit code.

Required provenance:

1. exactly one CogentNexus-OpenClaw plugin identity remains;
2. installed plugin root is the canonical supported location selected by OpenClaw/installer;
3. installed plugin payload fingerprint equals the freshly computed exact-candidate source fingerprint;
4. installed plugin/version/package identity is exact;
5. installed `workspace/skills/cogentnexus-openclaw/scripts/namespace_ownership.py` SHA-256 equals the exact candidate script hash;
6. ownership manifest verifies against the effective installed plugin path;
7. no stale ambiguous managed npm wrapper/product root remains;
8. plugin is enabled/loaded as expected by the successful supported installer;
9. controller returns to the expected normal managed operating state through the installer, not manual normalization.

If installer exit is zero but provenance does not match, verdict is `FAIL_PROVENANCE` and no manual repair is authorized.

## Phase 4 — Runtime and data health proof

After successful provenance proof, collect read-only health evidence:

- `cnxclaw`/system status READY as applicable;
- recovery check READY;
- delivery check READY;
- Gateway healthy;
- Ollama/provider healthy and selected model/provider coherent;
- OpenClaw version unchanged unless the supported installer contract explicitly changes it;
- SQLite integrity `ok`;
- pending outbox `0` unless a pre-existing accepted item was explicitly accounted for;
- historical Task-136/137 Tickets/events/model-call evidence still present;
- no unexpected new semantic Ticket, workflow, assistant-delivery, direct-recovery, or outbox rows created by installation;
- no duplicate CogentNexus plugin identity or ambiguous ownership evidence.

Do not create a synthetic semantic Ticket merely to prove health.

## Explicit semantic fence

This task authorizes **zero Dashboard semantic sends**.

Do not:

- click/send a Dashboard message;
- reuse Task-136/137 messages or nonces;
- inject alternate semantic transport;
- manually create Ticket/workflow/outbox/ack/delivery/recovery rows;
- trigger final durable-delivery acceptance.

A successful Task 142 only proves deployment + provenance + health. Final Dashboard durable-delivery reacceptance requires a later independently reviewed task.

## PASS criteria

Task 142 may report `PASS` only if all are true:

1. no material pre-install drift;
2. exact source candidate is `138759d111fe27a0cda75f59ad108d11caf19120`;
3. candidate package/build provenance is complete;
4. exactly one supported installer invocation exits successfully;
5. installed plugin fingerprint equals exact candidate fingerprint;
6. installed ownership script hash equals exact candidate script hash;
7. ownership manifest/plugin inventory are coherent and singular;
8. expected managed operating state is restored by the installer itself;
9. runtime/provider/Gateway/database health checks are GREEN;
10. historical semantic evidence is preserved with no unexpected new semantic rows;
11. zero Dashboard semantic Sends occurred.

## Failure handling

On failure, stop and publish evidence. Do not retry or repair live state inside the same task unless this task explicitly describes that action (it does not).

Use the narrowest applicable verdict:

- `BLOCKED_LIVE_STATE_DRIFT`;
- `BLOCKED_CANDIDATE_PROVENANCE`;
- `FAIL_INSTALL_OVER`;
- `FAIL_PROVENANCE`;
- `FAIL_POST_INSTALL_HEALTH`.

## Required report

Publish exactly:

`docs/operations/coordination/reports/CNX-20260829-142-accepted-candidate-install-over-retry-and-health-proof.md`

The report must include:

- fresh starting coordination HEAD;
- exact detached candidate SHA;
- pre-install live state and drift decision;
- package filename/size/SHA-256/fingerprint;
- candidate and installed `namespace_ownership.py` hashes;
- exact installer command and exit code;
- proof of exactly one installer invocation;
- post-install plugin/manifest/controller provenance;
- health/database/semantic-preservation evidence;
- explicit Dashboard Send count `0`;
- final verdict.

Then stop for independent ChatGPT review.

## Hard fence

No uninstall/reset/clean-reinstall; no manual controller normalization; no manual plugin enable/disable/delete/replace; no alternate plugin installation path; no Dashboard semantic Send/resend; no semantic reuse/injection; no manual Ticket/workflow/outbox/ack/delivery/recovery/database mutation; no crash/recovery injection; no provider/model/OpenClaw config mutation except what the supported installer itself owns; no unrelated process/task/service mutation; no reboot; no credentials/secrets; no merge/tag/release; no force push.
