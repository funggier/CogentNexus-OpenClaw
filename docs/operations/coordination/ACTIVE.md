# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `SOURCE_TDD_ATTESTED_UPGRADE_TRUTH_TABLE_REPAIR`
Current authorization: `TASK084_CONTROL_FLOW_REWORK_AUTHORIZED`
Task ID: `CNX-20260827-085`
Updated: 2026-08-27 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260827-085-correct-attested-classification-and-pending-rollover-control-flow.md`](tasks/CNX-20260827-085-correct-attested-classification-and-pending-rollover-control-flow.md)

## Task 084 review

Task 084 reported:

`PASS_ATTESTED_SAME_VERSION_ROLLOVER_AND_PENDING_RECOVERY_REPAIRED`

Implementation HEAD:

`0847a260d6f689f364bb096bd7857bb1dd4d58e1`

Report HEAD:

`658eb55b5163c5d74a44ce75ca2c04f538a46ba3`

Independent review:

Decision: `REWORK`

Disposition:

`REWORK_ATTESTED_CLASSIFICATION_AND_PENDING_ROLLOVER_CONTROL_FLOW`

Review path:

[`reviews/CNX-20260827-084-repair-same-version-rollover-attestation-and-pending-recovery.md`](reviews/CNX-20260827-084-repair-same-version-rollover-attestation-and-pending-recovery.md)

Publication fence itself is accepted: Task 084 used one bounded implementation commit followed by one report-only commit and did not change `plugins/cogentnexus-openclaw/**`.

## Task-084 evidence preserved

Task 085 should preserve, not redo unnecessarily:

- production `plugin-fingerprint` on the existing `_plugin_payload()` contract;
- live newer generation `g-7257c4555ca8ad21` fingerprint equals accepted source candidate fingerprint `8fd911e3...`;
- manifest-owned prior generation `g-5593cbcfff5b35d5` fingerprint differs (`7e9189f8...`);
- expected replacement fingerprint carried in rollover plan/apply;
- changed replacement without attestation rejected;
- wrong attestation rejected;
- generic two-candidate resolution remains ambiguous;
- existing plan/inventory/manifest/wrapper/tree/hash/atomic rollback fences remain present;
- no live mutation occurred in Task 084.

## Why Task 084 is REWORK

Three production contract violations were independently found.

### 1. Pending recovery skips its required rollover

`install.ps1` currently places both plugin installation and the entire upgrade rollover block beneath a condition requiring:

`-not $pendingRollover -and -not $pluginAlreadyExact`

Therefore `pendingRollover=true` skips both the third-generation install (correct) and the required rollover-plan/apply (incorrect). The later unique resolver would still see two candidates.

### 2. Ordinary single-generation changed-source upgrade is rejected

Attested `classify_install()` currently raises when one coherent manifest-owned generation fingerprint differs from the candidate-source fingerprint.

The required behavior is normal upgrade:

- `pendingRollover=false`
- `pluginAlreadyExact=false`

so npm-pack/install can create the source-exact replacement and then roll it over.

### 3. Explicit source fingerprint is not always enforced for two candidates

If retired and active replacement fingerprints happen to equal one another, `_exact_rollover_state()` currently does not require the explicitly supplied expected source fingerprint to equal the active replacement.

Explicit attestation must always mean:

`active replacement fingerprint == expected candidate-source fingerprint`.

## Current live state remains read-only

The Task-083 two-generation partial state remains the accepted live baseline:

- PASSTHROUGH generation 13;
- startup disabled;
- Supervisor absent;
- AGENTS managed block absent;
- manifest -> `g-5593cbcfff5b35d5`;
- active disabled replacement -> `g-7257c4555ca8ad21`;
- Gateway/Ollama healthy;
- SQLite integrity ok, Tickets/outbox zero.

Do not delete/rename either generation or edit ownership manually.

## Task 085 requirements

Task 085 is source/test-only and must:

1. RED-prove the three review findings against Task-084 implementation.
2. Correct the attested classification truth table.
3. Introduce one executable production plugin lifecycle action truth table consumed by `install.ps1`.
4. Require:
   - ordinary upgrade -> install=true, rollover=true;
   - pending recovery -> install=false, rollover=true;
   - already exact -> install=false, rollover=false;
   - fresh/legacy -> preserve existing intended plugin creation without upgrade rollover.
5. Separate plugin install and rollover into independent production action gates.
6. Ensure pending rollover completes before later unique `resolve-plugin` / ownership publication.
7. Require active replacement to equal explicitly supplied expected source fingerprint even when retired/replacement are otherwise equivalent.
8. Preserve Task-084 security/atomicity fences and all accepted semantic/delivery/npm-pack work.
9. Keep zero diff under `plugins/cogentnexus-openclaw/**`.
10. Run full Python, npm11/npm12, PowerShell 5.1, installer, semantic/delivery and baseline gates.

## Hard live fence

Task 085 may not run live install/install-over/uninstall/reset/cleanup; may not mutate live plugin generations, controller/startup/Supervisor/AGENTS/ownership/config/runtime/SQLite/session state; may not send Dashboard/WebChat/CLI semantic messages; may not call Ollama directly or change provider/model/timeouts; and may not restart/reboot/merge/tag/release.

## Successor gate

Only an independently accepted:

`PASS_ATTESTED_CLASSIFICATION_AND_PENDING_ROLLOVER_CONTROL_FLOW_REPAIRED`

may authorize another live recovery attempt.

That live successor must complete the existing attested pending rollover with one supported installer invocation, create no third generation, restore MANAGED/startup/Supervisor/AGENTS, prove parity/health, observe five natural no-flash ticks and prove Dashboard owner-surface readiness with zero semantic messages.
