# Coordination Channel Status

**State:** `READY_FOR_HERMES`
**Updated:** 2026-08-27 ICT
**Transport:** GitHub repository history
**Human authority:** operator authorized definitive repair through final live/semantic acceptance and approved heavy comprehensive work while Hermes/Codex budget is available
**Execution trigger:** manual Hermes continuation; scheduled execution remains disabled

## Accepted semantic/delivery lineage

Tasks 078/079/080 remain accepted candidate behavior covering owner/session delivery security, admission/routing idempotency, single timeout recovery authority, direct model-call lease ordering, direct lifecycle convergence, workflow delivery atomicity, crash-safe completion-lock publication, and exact workflow/Ticket delivery-run fencing.

Task 082 independently repaired and proved the Windows/npm 11/npm 12 `npm pack --json` installer boundary.

Provider readiness remains:

`PROVIDER_READY_WITH_FRESH_OWNER_SESSION`

No additional direct Ollama probe is authorized.

## Task 083 accepted blocker

Task 083 attempted one supported recovery install-over and correctly stopped after the source-safe rollover rejected a deliberately changed same-version replacement.

Accepted disposition:

`ACCEPT_BLOCKER_SAME_VERSION_ROLLOVER_ATTESTATION_GAP`

The live system remains in the bounded two-generation PASSTHROUGH topology created by that failed installer attempt.

## Task 084 result and independent review

Task 084 implementation:

`0847a260d6f689f364bb096bd7857bb1dd4d58e1`

Task 084 report:

`658eb55b5163c5d74a44ce75ca2c04f538a46ba3`

Reported token:

`PASS_ATTESTED_SAME_VERSION_ROLLOVER_AND_PENDING_RECOVERY_REPAIRED`

Independent decision:

`REWORK`

Disposition:

`REWORK_ATTESTED_CLASSIFICATION_AND_PENDING_ROLLOVER_CONTROL_FLOW`

Publication fence is valid and the attestation primitives are preserved as rework base evidence.

## Preserved Task-084 evidence

- `plugin-fingerprint` derives authority from the exact source candidate through existing `_plugin_payload()` semantics.
- newer live generation fingerprint `8fd911e3...` equals accepted source candidate fingerprint;
- prior manifest-owned generation fingerprint `7e9189f8...` differs;
- expected source fingerprint is carried into rollover plan/apply;
- changed replacement without attestation and wrong attestation remain rejected;
- generic two-candidate resolution remains fail-closed;
- atomic retirement/rollback and plan/inventory/manifest/wrapper/tree/hash fences remain in place;
- plugin payload source did not change;
- live partial state was not mutated by Task 084.

## Task-084 blocking findings

### Pending rollover production wiring

The installer currently nests rollover under the same outer gate that requires `pendingRollover=false`.

Thus the intended Task-083 recovery state `pendingRollover=true` skips the required rollover-plan/apply and would later reach unique resolution with both candidates still present.

### Ordinary changed-source upgrade classification

A coherent single manifest-owned generation whose fingerprint differs from current candidate source is currently rejected by attested classification.

It must instead remain a supported normal upgrade requiring plugin installation followed by attested rollover.

### Explicit source equality on two-generation topology

When retired and active replacement happen to have equal fingerprints, current `_exact_rollover_state()` can avoid comparing the explicitly supplied expected source fingerprint to the active replacement.

Explicit attestation must always require exact active-replacement/source equality.

## Current live partial state

Still read-only and not accepted MANAGED state:

- controller PASSTHROUGH generation 13;
- startup disabled;
- Supervisor absent;
- AGENTS managed markers absent;
- ownership manifest -> prior `g-5593cbcfff5b35d5`;
- active disabled replacement -> `g-7257c4555ca8ad21`;
- Gateway healthy/dashboard reachable;
- Ollama healthy with accepted four models;
- SQLite integrity ok, Tickets/outbox zero.

Do not manually normalize this topology.

## Active Task 085

[`tasks/CNX-20260827-085-correct-attested-classification-and-pending-rollover-control-flow.md`](tasks/CNX-20260827-085-correct-attested-classification-and-pending-rollover-control-flow.md)

Status: `READY_FOR_HERMES`

Authorization: `TASK084_CONTROL_FLOW_REWORK_AUTHORIZED`

Execution mode: `SOURCE_TDD_ATTESTED_UPGRADE_TRUTH_TABLE_REPAIR`

Task 085 must:

- RED-prove all three review findings;
- correct single-generation normal-upgrade vs already-exact classification;
- require explicit expected source equality for all attested pending replacements;
- add one executable production plugin lifecycle action truth table;
- make installer actions exactly:
  - ordinary upgrade: install + rollover;
  - pending recovery: rollover only;
  - already exact: neither;
  - fresh/legacy: preserve current creation behavior;
- separate package installation and rollover into independent action gates;
- ensure pending rollover finishes before unique resolution and ownership publication;
- preserve Task-084 security/atomicity and Task-078/079/080/082 regressions;
- keep `plugins/cogentnexus-openclaw/**` byte-unchanged;
- run full Python/npm11/npm12/PowerShell/installer/semantic/baseline verification.

## Hard live fence

Task 085 is source/test-only. No live install/install-over/uninstall/reset/cleanup, generation mutation, ownership/controller/startup/Supervisor/AGENTS/config/runtime/SQLite/session mutation, Dashboard/WebChat/CLI semantic message, direct Ollama probe, provider/model/timeout change, restart/reboot, merge/tag or release.

## Successor logic

Only after independent acceptance of:

`PASS_ATTESTED_CLASSIFICATION_AND_PENDING_ROLLOVER_CONTROL_FLOW_REPAIRED`

may one supported live recovery install-over be authorized against the existing two-generation state.

That later live task must complete rollover without a third generation, restore MANAGED/startup/Supervisor/AGENTS, prove exact source/live parity and owned runtime health, observe five natural PT1M ticks with no-flash evidence, and prove Dashboard/WebChat owner-surface readiness without sending a semantic message.
