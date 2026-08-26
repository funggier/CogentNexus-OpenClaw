# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `SOURCE_TDD_ATTESTED_ROLLOVER_AND_PENDING_RECOVERY`
Current authorization: `ATTESTED_ROLLOVER_SOURCE_REPAIR_AUTHORIZED`
Task ID: `CNX-20260827-084`
Updated: 2026-08-27 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260827-084-repair-same-version-rollover-attestation-and-pending-recovery.md`](tasks/CNX-20260827-084-repair-same-version-rollover-attestation-and-pending-recovery.md)

## Task 083 accepted blocker

Task 083 reported:

`BLOCKED_SUPPORTED_RECOVERY_INSTALL_OVER`

Report HEAD:

`1b5238bc3d7e8611e5fe305a969fad45735b142a`

Independent review:

Decision: `ACCEPT`

Disposition:

`ACCEPT_BLOCKER_SAME_VERSION_ROLLOVER_ATTESTATION_GAP`

Review path:

[`reviews/CNX-20260827-083-recover-partial-install-and-live-parity.md`](reviews/CNX-20260827-083-recover-partial-install-and-live-parity.md)

Publication fence is accepted: Task 083 published one report-only commit from execution HEAD `58533e25bb23f00606bccf236193e5c2d1a17f86`.

## Task 083 execution facts

Task 083 correctly:

- re-proved the expected partial PASSTHROUGH state;
- used exact accepted source `df412ed10522d79a722e1b48d681e7553cb79ae2`;
- invoked one supported recovery install-over only;
- proved the Task-082 npm-pack resolver works live;
- stopped after the ownership-safe rollover rejected a different-fingerprint same-version replacement;
- did not retry, manually clean, edit ownership, or send any semantic/provider message.

Failure boundary:

`replacement payload conflicts with the manifest-owned same-version payload`

The current source requires replacement fingerprint equality with the manifest-owned prior generation. That policy cannot represent an intentionally changed but still-versioned `0.9.3` replacement unless the new payload has an independent candidate-source attestation.

## Accepted current live partial state

Task 083 left a bounded fail-closed state:

- controller `passthrough`, generation 13;
- startup disabled;
- Supervisor absent;
- AGENTS managed block absent;
- ownership manifest identifies the prior generation;
- prior generation `g-5593cbcfff5b35d5` remains present;
- newly installed generation `g-7257c4555ca8ad21` remains present and registered disabled;
- both are `cogentnexus-openclaw@0.9.3` but have different fingerprints;
- Gateway healthy / dashboard HTTP `200`;
- Ollama healthy with accepted four-model inventory;
- SQLite integrity `ok`, Tickets `0`, outbox `0`;
- zero semantic/provider activity from Task 083.

This is not MANAGED acceptance. Do not manually delete either plugin generation or rewrite the manifest.

## Why Task 084 exists

Task 084 must repair the source contract without weakening ownership safety.

A different-fingerprint same-version replacement may be accepted only when its fingerprint equals the expected plugin fingerprint derived from the exact installer source candidate.

Task 084 also must support the current pending-rollover topology through an explicit attested installer classification/recovery path while keeping generic two-candidate plugin resolution ambiguous/fail-closed.

Required source behavior includes:

- production source-plugin fingerprint interface;
- expected-replacement fingerprint bound into rollover plan/apply;
- changed same-version replacement remains rejected without attestation;
- wrong attestation remains rejected;
- exact Task-083 two-generation state can be classified only with explicit source attestation;
- installer completes an attested pending rollover before any new plugin install and does not create a third semantic generation;
- already source-exact single-generation upgrade skips redundant plugin install;
- normal changed-payload upgrade installs then rolls over only if the new generation matches source attestation;
- all existing inventory/manifest/project-tree/plan-hash/rollback fences remain intact.

## Plugin payload preservation fence

Task 084 must not change any file under:

`plugins/cogentnexus-openclaw/**`

The Task-083 newer live generation must remain fingerprint-equivalent to the source candidate so it can be safely reused by the later recovery task.

Allowed production scope is the ownership/installer control plane plus focused tests.

## Hard live fence

Task 084 is source/test only.

No live install/install-over/uninstall/reset/cleanup, no deletion/rename of live plugin generations, no controller/plugin/startup/Supervisor/AGENTS/ownership/runtime/config repair, no live SQLite/Ticket/session mutation, no Dashboard/WebChat or CLI semantic message, no direct Ollama probe, no provider/model/timeout change, no restart/reboot, merge, tag or release.

Read-only live fingerprint/state inspection is allowed.

## Successor gate

Only an independently accepted:

`PASS_ATTESTED_SAME_VERSION_ROLLOVER_AND_PENDING_RECOVERY_REPAIRED`

may authorize the next live recovery task.

That successor must use one supported installer invocation to complete the existing attested pending rollover, restore MANAGED/startup/Supervisor/AGENTS, prove source/live parity and ownership/runtime health, observe five natural no-flash ticks, and prove Dashboard/WebChat owner-surface readiness without sending a semantic prompt.

Final semantic acceptance remains a separate later task with exactly one fresh authenticated Dashboard/WebChat owner message.