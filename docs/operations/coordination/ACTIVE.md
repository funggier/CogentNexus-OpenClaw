# Active Coordination Task

Status: `AWAITING_OPERATOR_DESIGN_APPROVAL`
Execution mode: `SOURCE_TDD_WINDOWS_REPARSE_ATTESTATION_REPAIR_PENDING_APPROVAL`
Current authorization: `NO_LIVE_OR_SEMANTIC_SUCCESSOR_AUTHORIZED`
Task ID: `PENDING_CNX-20260827-095`
Updated: 2026-08-27 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator approval and task publication

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Task 094 review

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

Publication fence is accepted: execution `41ba7815...` -> implementation `33139300...` is one source/test commit and implementation -> report `0902c3c5...` is one report-only commit.

## Preserved Task-094 work

The complete installable-payload v2 fingerprint design remains the intended solution:

- `package.json.files` + `package.json` authority;
- all shipped `dist/**` runtime files covered;
- normalized relative paths + exact bytes + versioned SHA-256 domain;
- absolute roots excluded;
- npm11/npm12 current packed set reported 176/176 exact;
- pre-Task093 live payload and Task093+094 candidate reported as distinct under v2;
- Task-093 Dashboard staging repair remains preserved.

Do not revert or redesign the v2 fingerprint without a new focused blocker.

## Blocking Windows path-indirection gap

The Task-094 contract required rejection of symlinks and reparse-style path indirection.

Current production enumeration checks `os.path.islink(path)` but does not explicitly reject Windows junction/reparse-point entries. A directory junction beneath a declared package directory can therefore be traversed by normal directory APIs even though it is filesystem indirection.

The existing tests prove symlink rejection but not a real Windows junction/reparse case.

Because Windows is the live deployment target and this is an ownership/attestation boundary, no live install-over is authorized yet.

## Pending bounded design

The proposed successor is a narrow source-only TDD correction:

1. add one production path-indirection predicate;
2. reject symlinks plus Windows reparse-point/junction entries before traversal using `lstat`/Windows file attributes or an equally exact supported API;
3. apply the predicate to declared entries and recursively discovered children;
4. never follow a junction merely because its target is within the plugin root;
5. preserve the v2 fingerprint domain and package contract unchanged;
6. mandatory Windows RED with an actual junction/reparse fixture, then GREEN;
7. retain npm11/npm12 equivalence, classifier truth tables, rollover security/atomicity and Task-093 Dashboard staging regressions.

## Hard fence

Until operator approval:

- do not create/run Task 095 implementation;
- no install/install-over/uninstall/reset/cleanup;
- no plugin-generation mutation;
- no semantic message/provider probe;
- no Task-092 record repair;
- no controller/startup/Supervisor/AGENTS/config/runtime/SQLite mutation.

## Successor logic

After explicit operator approval, publish Task 095 for source-only Windows reparse-point hardening. Only independent acceptance of that correction may authorize the one-shot supported live install-over of the exact Task-093+094+095 source.
