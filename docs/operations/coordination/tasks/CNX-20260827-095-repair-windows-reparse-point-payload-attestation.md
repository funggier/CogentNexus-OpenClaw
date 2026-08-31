# CNX-20260827-095 — Repair Windows Reparse-Point Payload Attestation

Status: `READY_FOR_HERMES`

Execution mode: `SOURCE_TDD_WINDOWS_REPARSE_POINT_ATTESTATION_REPAIR`

Current authorization: `TASK094_WINDOWS_REPARSE_BOUNDARY_REPAIR_AUTHORIZED`

Owner: ChatGPT

Executor: Hermes/Codex after operator continuation

## Goal

Close the remaining Windows filesystem-indirection gap in the Task-094 complete installable-payload fingerprint without redesigning the v2 fingerprint algorithm.

The accepted Task-094 direction remains authoritative: `package.json.files` plus `package.json` define the installable payload; normalized relative paths and exact bytes are hashed under the existing v2 domain. This task changes only the safety predicate used before package traversal so Windows junction/reparse-point entries cannot be followed and attested as if they were ordinary package-owned files/directories.

## Operator-approved design

The operator explicitly approved the bounded correction:

1. add one production filesystem-indirection predicate;
2. reject symbolic links and Windows reparse-point/junction entries before any traversal;
3. apply the predicate to declared package entries and recursively discovered children;
4. never accept a reparse/junction merely because its resolved target is still inside the package root;
5. preserve Task-094 v2 digest framing, file-set authority and classifier semantics unchanged;
6. prove the defect with a real Windows junction/reparse RED before production edits;
7. preserve npm11/npm12 package-set equivalence and all rollover/install/staging regressions.

## Accepted predecessor state

Task 093 staging candidate:

`a924157ecdedef1d4f166d5762529b0d59536fc9`

Task 094 implementation:

`3313930064123867ad760908a77b498f3bad029a`

Task 094 report:

`0902c3c50fb1a46adfa9b8df86495fa521d01719`

Task 094 independent disposition:

`REWORK_WINDOWS_REPARSE_POINT_INDIRECTION_NOT_REJECTED`

The following Task-094 work is preserved and must not be redesigned without a new focused blocker:

- complete installable-payload v2 fingerprint;
- `package.json.files` + `package.json` authority;
- all shipped `dist/**` runtime coverage;
- normalized relative POSIX paths + exact bytes + versioned SHA-256 domain;
- root-location independence;
- npm11/npm12 current package set equivalence;
- Task-093 candidate and pre-Task093 live payload distinction under v2;
- classifier/rollover attestation integration.

## Exact defect

Current production enumeration in:

`skills/cogentnexus-openclaw/scripts/namespace_ownership.py`

rejects `os.path.islink(path)` while recursively expanding package payload entries.

That does not prove rejection of all Windows reparse-point forms. In particular, a directory junction/reparse point may be traversable via ordinary `Path.is_dir()` / `os.scandir()` semantics without satisfying the symbolic-link predicate used by the current code.

Because this is the package ownership/attestation boundary on the live Windows deployment target, any filesystem indirection must fail closed before traversal.

---

# Absolute live/semantic fence

Task 095 is source/test-only.

Do NOT:

- install/install-over/uninstall/reset/cleanup;
- mutate any OpenClaw plugin generation;
- mutate ownership/controller/startup/Supervisor/AGENTS/config/runtime/SQLite;
- send Dashboard/WebChat content;
- call `chat.send`, `chat.inject`, `openclaw agent`, `sessions_send` or channel sends;
- generate a semantic nonce;
- call Ollama/provider directly;
- repair/rewrite Task-092 Ticket/session/transcript evidence;
- change provider/model/timeouts;
- restart/reboot;
- merge/tag/release.

Use a fresh isolated worktree from the coordination execution HEAD.

Read-only inspection of platform/path metadata is allowed.

---

# Phase A — re-prove the Windows defect

Before source edits:

1. Fetch/reset the coordination branch and record execution HEAD.
2. Prove Task-094 implementation/report/review are ancestors.
3. Verify Task-094 publication fence remains valid.
4. Create a fresh isolated worktree.
5. Confirm the host is Windows and record Python/PowerShell/Node/npm versions.
6. Build a valid package-shaped fixture using the real production fingerprint helper.
7. Create a real directory junction or equivalent Windows reparse-point entry inside a declared package directory, preferably beneath `dist/`, targeting content outside that physical package directory.
8. Prove the current Task-094 implementation does not reject the real junction/reparse case before traversal.

The RED must establish the actual filesystem behavior, not simulate it only with monkeypatching.

If the environment cannot create or inspect a real junction/reparse point, stop with:

`BLOCKED_REAL_WINDOWS_REPARSE_RED_UNAVAILABLE`

rather than claiming the boundary fixed from synthetic-only evidence.

---

# Gate R — mandatory RED

Add the smallest regression test against the real production helper.

Required RED cases:

1. A real Windows directory junction/reparse point appears under a declared package directory.
2. `plugin_fingerprint()` must reject it before reading/traversing target content.
3. Under Task-094 source, the test must fail for the intended reason: current code accepts/traverses the junction or otherwise fails to identify the reparse boundary.
4. Existing symbolic-link rejection remains represented separately.

Also add a nested-child case so the implementation cannot protect only top-level `package.json.files` entries while following a reparse point discovered recursively.

If Windows exposes a supported regular-file reparse form in the test environment, add focused coverage; otherwise directory junction coverage is mandatory and sufficient for this task when combined with the generic reparse predicate.

---

# Gate F — minimal production fix

Implement one reusable filesystem-indirection predicate in `namespace_ownership.py`.

Requirements:

- inspect path metadata without following the target;
- reject POSIX/Windows symbolic links;
- on Windows reject any path carrying the reparse-point file attribute, including directory junctions;
- use a supported Python/OS API available on the project target runtime; `stat.FILE_ATTRIBUTE_REPARSE_POINT` with `lstat().st_file_attributes` or an equivalent exact check is acceptable;
- fail closed if the metadata required to decide the Windows reparse boundary is malformed/unreadable;
- apply the predicate before `is_file()`, `is_dir()`, `scandir()` or content reads for declared entries;
- apply the same predicate to every recursively discovered child before descending;
- do not resolve/follow the target first and then decide;
- do not whitelist a junction merely because its target resolves within the package root.

Keep the implementation narrow. Do not change:

- fingerprint v2 domain separator;
- path+NUL+bytes+NUL framing;
- `package.json.files` authority;
- package identity/version checks;
- classifier truth table;
- rollover plan/apply semantics;
- Dashboard staging behavior.

---

# Gate G — GREEN and negative proofs

After the minimal fix, prove:

1. the real top-level/nested Windows junction fixtures are rejected;
2. existing symlink fixture remains rejected;
3. ordinary physical directories/files remain accepted;
4. identical ordinary package payload copied to another root retains the same v2 fingerprint;
5. changing a shipped runtime file/path still changes fingerprint;
6. source/tests/node_modules/transient artifacts remain outside the fingerprint domain unless declared by package contract.

The RED test must be shown failing on the exact Task-094 predecessor and passing only after the production fix.

---

# Gate N — npm package-set equivalence

Re-run actual package-set equivalence on both supported paths:

- Node 24 / npm 11;
- Node 22 / npm 12.

Use actual pack/dry-run metadata as in Task 094. The canonical payload file set must still equal the packed file set with no missing shipped runtime and no new extra entries.

The v2 candidate fingerprint may change only if source/package bytes changed for legitimate reasons; the algorithm/framing itself must remain unchanged in this task.

Record the final candidate fingerprint and canonical file count.

---

# Gate C — classifier/lifecycle/rollover preservation

Re-run and record fresh evidence for:

- changed single-generation payload => `mode=upgrade`, `pendingRollover=false`, `pluginAlreadyExact=false`, actions install+rollover;
- exact single-generation payload => no install/no rollover;
- attested two-generation pending rollover => install false / rollover true;
- explicit expected replacement fingerprint mismatch => reject;
- 3+ candidates/ambiguous/foreign wrapper/path boundary cases => reject;
- rollover plan/apply atomicity and rollback tests from Tasks 084/085/086;
- Task-089 production PowerShell action-resolver boundary and installer AST/order invariants.

No lifecycle truth-table duplication is allowed in the new helper.

---

# Gate D — preserve Task-093 Dashboard repair

Re-run the focused Task-093 verified-delivery/re-registration tests and the full plugin suite on both supported Node/npm paths.

No source change under the Dashboard staging implementation is expected in Task 095. Any such change requires a new focused RED and must be reported as scope expansion/blocker rather than silently included.

---

# Full verification

Record fresh evidence for at least:

- real Windows junction/reparse RED then GREEN;
- existing symlink/path safety tests;
- focused complete-payload fingerprint suite;
- full Python suite;
- `python -m py_compile` for modified Python;
- PowerShell 5.1 syntax/action/installer-AST checks;
- npm pack artifact parser tests;
- Node 24/npm 11 clean install + full plugin suite + `plugin:validate` + build + schema/bootstrap/package verification;
- Node 22/npm 12 isolated clean install + full plugin suite + `plugin:validate` + build + schema/bootstrap/package verification;
- npm11/npm12 canonical packed file-set equivalence;
- Task-093 Dashboard staging focused tests;
- baseline consistency;
- `git diff --check`;
- clean final worktree.

No completion claim from old Task-094 test output alone.

---

# Publication fence

Commit source/tests first.

Then publish exactly one separate report-only commit:

`docs/operations/coordination/reports/CNX-20260827-095-repair-windows-reparse-point-payload-attestation.md`

Required result tokens:

- `PASS_WINDOWS_REPARSE_POINT_PAYLOAD_ATTESTATION_REPAIRED`
- `BLOCKED_REAL_WINDOWS_REPARSE_RED_UNAVAILABLE`
- `BLOCKED_REPARSE_BOUNDARY_STILL_FOLLOWED`
- `BLOCKED_FINGERPRINT_V2_REGRESSION`
- `BLOCKED_NPM_PACKAGE_SET_MISMATCH`
- `BLOCKED_CLASSIFICATION_OR_ROLLOVER_REGRESSION`
- `BLOCKED_TEST_OR_VALIDATION_FAILURE`
- `BLOCKED_EVIDENCE_PUBLICATION_UNSAFE`

## Successor gate

Only independent acceptance of:

`PASS_WINDOWS_REPARSE_POINT_PAYLOAD_ATTESTATION_REPAIRED`

may authorize the next live task.

That successor must perform exactly one supported install-over using the exact accepted Task-093+094+095 implementation HEAD, prove that the pre-fix live plugin is classified non-exact and the repaired package is actually installed/rolled over, restore MANAGED parity/health, and send zero semantic messages.

Only after that live task is independently accepted may one new final authenticated fresh-session semantic attempt be authorized. The fresh-session hard gate from Task 092 remains in force.