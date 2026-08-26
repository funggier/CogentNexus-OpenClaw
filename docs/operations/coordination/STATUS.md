# Coordination Channel Status

**State:** `READY_FOR_HERMES`
**Updated:** 2026-08-27 ICT
**Transport:** GitHub repository history
**Human authority:** operator authorized definitive repair through final live/semantic acceptance and approved heavy comprehensive work while Hermes/Codex budget is available
**Execution trigger:** manual Hermes continuation; scheduled execution remains disabled

## Accepted semantic/delivery lineage

Tasks 078/079/080 remain accepted candidate behavior covering owner/session delivery security, admission/routing idempotency, single timeout recovery authority, direct model-call lease ordering, direct lifecycle convergence, workflow delivery atomicity, crash-safe completion-lock publication, and exact workflow/Ticket delivery-run fencing.

Task 082 independently repaired and proved the Windows/npm 11/npm 12 `npm pack --json` installer boundary.

Last accepted source before the current rollover-attestation repair:

`df412ed10522d79a722e1b48d681e7553cb79ae2`

Provider readiness remains:

`PROVIDER_READY_WITH_FRESH_OWNER_SESSION`

No additional direct Ollama probe is authorized.

## Task 083 result

Task 083 attempted one supported live recovery install-over from exact source `df412ed10522d79a722e1b48d681e7553cb79ae2`.

Reported result:

`BLOCKED_SUPPORTED_RECOVERY_INSTALL_OVER`

Report HEAD:

`1b5238bc3d7e8611e5fe305a969fad45735b142a`

Independent review:

Decision: `ACCEPT`

Disposition:

`ACCEPT_BLOCKER_SAME_VERSION_ROLLOVER_ATTESTATION_GAP`

Publication fence: report-only, one commit from execution HEAD `58533e25bb23f00606bccf236193e5c2d1a17f86`.

## Task 083 failure boundary

The Task-082 npm-pack repair worked live: the installer successfully packed, resolved and installed the exact candidate artifact.

The next ownership-safe generation rollover then failed closed with:

`replacement payload conflicts with the manifest-owned same-version payload`

Current rollover source intentionally requires the active replacement fingerprint to equal the manifest-owned prior fingerprint. Existing tests intentionally reject a conflicting same-version payload.

That invariant is now incomplete for development install-over because accepted Tasks 078–082 changed source while retaining plugin version `0.9.3`.

The required replacement policy is not “accept any same-version payload.” It is:

`accept a changed same-version replacement only when it equals the exact expected source-candidate fingerprint and all existing ownership/inventory/plan/apply fences also pass`.

## Current live partial state

Task 083 stopped without retry or manual repair.

Current accepted state:

- controller PASSTHROUGH, generation 13;
- startup disabled;
- Supervisor absent;
- AGENTS managed markers absent;
- ownership manifest still identifies the prior generation;
- old generation `g-5593cbcfff5b35d5` present;
- newer Task-083 generation `g-7257c4555ca8ad21` present and registered disabled;
- both identify v0.9.3 but have different fingerprints;
- Gateway healthy / dashboard HTTP `200`;
- Ollama healthy with accepted four models;
- SQLite integrity `ok`, Tickets `0`, outbox `0`;
- no semantic/provider work created by Task 083.

Generic unique plugin resolution is now intentionally ambiguous. Do not manually delete a generation or edit the manifest.

## Active Task 084

[`tasks/CNX-20260827-084-repair-same-version-rollover-attestation-and-pending-recovery.md`](tasks/CNX-20260827-084-repair-same-version-rollover-attestation-and-pending-recovery.md)

Status: `READY_FOR_HERMES`

Authorization: `ATTESTED_ROLLOVER_SOURCE_REPAIR_AUTHORIZED`

Execution mode: `SOURCE_TDD_ATTESTED_ROLLOVER_AND_PENDING_RECOVERY`

Task 084 is source/test-only and must:

- prove the newer live Task-083 generation fingerprint equals the exact accepted source plugin fingerprint;
- preserve plugin runtime/package payload files unchanged;
- RED-prove the current same-version changed-payload policy gap;
- add a production source-plugin fingerprint interface;
- bind expected replacement fingerprint into rollover plan/apply;
- preserve rejection of unattested/wrong replacements;
- add an explicit attested installer classification for the exact pending-rollover topology while generic two-candidate resolution remains strict;
- make recovery complete the already-installed pending rollover before any new plugin install;
- skip redundant plugin generation creation when the canonical generation is already source-exact;
- preserve all existing atomic retirement/rollback/inventory/manifest/tree/hash fences;
- rerun full ownership/install/recovery, semantic/delivery, npm 11/npm 12, Python, PowerShell and baseline regressions.

## Plugin payload preservation requirement

Task 084 may not change:

`plugins/cogentnexus-openclaw/**`

The current newer live generation must remain source-exact for the later supported recovery.

## Hard live fence

No live install/install-over/uninstall/reset/cleanup or plugin generation mutation is authorized in Task 084. No controller/startup/Supervisor/AGENTS/ownership/runtime/config repair, no live Ticket/session/SQLite mutation, no Dashboard/WebChat or CLI semantic message, no direct Ollama probe, no provider/model/timeout change, no restart/reboot, merge, tag or release.

Read-only live state/fingerprint inspection is allowed.

## Successor logic

If Task 084 is independently accepted, the next live recovery task will use the exact corrected source and one supported installer invocation to:

- attest and complete the current pending rollover without manual deletion or a third semantic generation;
- restore MANAGED/startup/Supervisor/AGENTS;
- prove source/live plugin+skill parity and ownership/runtime/Gateway/Ollama/SQLite health;
- observe at least five natural PT1M ticks with no-flash evidence;
- prove Dashboard/WebChat authenticated owner-surface readiness without sending a semantic prompt.

Only after that live recovery passes independent review may the final semantic task send exactly one fresh authenticated Dashboard/WebChat owner message.