# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `SOURCE_TDD_WINDOWS_REPARSE_POINT_ATTESTATION_REPAIR`
Current authorization: `TASK094_WINDOWS_REPARSE_BOUNDARY_REPAIR_AUTHORIZED`
Task ID: `CNX-20260827-095`
Updated: 2026-08-27 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260827-095-repair-windows-reparse-point-payload-attestation.md`](tasks/CNX-20260827-095-repair-windows-reparse-point-payload-attestation.md)

## Operator approval

The operator approved the bounded Windows reparse-point hardening design after Task 094 independent review.

## Task 094 review carried forward

Task 094 implementation:

`3313930064123867ad760908a77b498f3bad029a`

Task 094 report:

`0902c3c50fb1a46adfa9b8df86495fa521d01719`

Independent decision:

`REWORK`

Disposition:

`REWORK_WINDOWS_REPARSE_POINT_INDIRECTION_NOT_REJECTED`

Review:

[`reviews/CNX-20260827-094-repair-complete-installable-plugin-payload-fingerprint.md`](reviews/CNX-20260827-094-repair-complete-installable-plugin-payload-fingerprint.md)

Task-094 publication fence remains accepted.

## Preserved implementation

Do not redesign the Task-094 complete installable-payload v2 fingerprint. Preserve:

- `package.json.files` + `package.json` authority;
- all shipped `dist/**` runtime coverage;
- normalized relative path + exact bytes under the existing v2 SHA-256 domain;
- root-location independence;
- npm11/npm12 packed-set equivalence;
- classifier/rollover integration;
- Task-093 Dashboard durable-staging repair.

## Task 095 exact target

Current v2 enumeration rejects `os.path.islink(path)` but does not prove rejection of all Windows junction/reparse-point forms.

Task 095 must RED a real Windows junction/reparse fixture before production edits, then apply one minimal filesystem-indirection predicate that rejects symlinks and Windows reparse points before any file/directory traversal.

The check must apply to both declared package entries and recursively discovered children. It must not follow/allow a junction merely because the resolved target is inside the package root.

## Required preservation proofs

Task 095 must retain:

- fingerprint v2 algorithm/framing unchanged;
- ordinary package root-copy fingerprint equality;
- runtime byte/path sensitivity;
- npm11/npm12 package-set equivalence;
- changed/exact/pending classifier/action truth tables;
- Task-084/085/086 rollover security/atomicity;
- Task-089 PowerShell action/AST boundaries;
- Task-093 Dashboard staging regressions.

## Hard live/semantic fence

Task 095 is source/test-only.

No install/install-over/uninstall/reset/cleanup, plugin-generation mutation, controller/startup/Supervisor/AGENTS/config/runtime/SQLite mutation, semantic message, provider probe, model/timeout change, Task-092 record repair, restart/reboot, merge/tag/release is authorized.

Task-092 semantic artifacts remain retired evidence.

## Successor gate

Only independent acceptance of:

`PASS_WINDOWS_REPARSE_POINT_PAYLOAD_ATTESTATION_REPAIRED`

may authorize one supported live install-over of the exact Task-093+094+095 source.

That future live task sends zero semantic messages. Only after live MANAGED/source parity/health are independently accepted may one new final authenticated fresh-session semantic attempt be authorized.