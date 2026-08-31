# CNX-20260827-094 — Repair Complete Installable Plugin Payload Fingerprint

Status: `READY_FOR_HERMES`

Execution mode: `SOURCE_TDD_COMPLETE_INSTALLABLE_PLUGIN_PAYLOAD_ATTESTATION`

Current authorization: `TASK093_DEPLOYMENT_ATTESTATION_REPAIR_AUTHORIZED`

Owner: ChatGPT

Executor: Hermes/Codex after operator continuation

## Goal

Replace the current four-file sample plugin fingerprint with one deterministic attestation over the complete installable CogentNexus-OpenClaw plugin payload, so any runtime byte/path change that would be shipped to OpenClaw changes the fingerprint and cannot be misclassified as `pluginAlreadyExact=true`.

This is a bounded source/test-only repair. It preserves the accepted Task-093 Dashboard durable-staging implementation and does not install it live yet.

## Operator-approved design

The operator explicitly approved the complete installable-payload approach.

The fingerprint must answer exactly:

> Does the currently installed plugin contain the same package-owned executable/installable payload, byte-for-byte and path-for-path, as the candidate package?

Do not hash the whole source repository. Do not retain the four-file sample model.

## Accepted predecessor state

Task 093 implementation:

`a924157ecdedef1d4f166d5762529b0d59536fc9`

Task 093 report:

`62fdd69d2a4a27566c0e986171b949347cf0df68`

Task 093 independent disposition:

`REWORK_PLUGIN_FINGERPRINT_DOES_NOT_ATTEST_RUNTIME_PAYLOAD`

Task 093 source fix remains preserved:

- process-global `TicketStore.prototype` patch lifetime is separated from per-runtime `reply_dispatch` registration lifetime;
- legitimate re-registration receives a staging hook;
- same API object remains idempotent;
- full Node/Python regressions reported green.

Do not revert or broaden that Dashboard fix unless a focused regression proves it necessary.

## Blocking defect to reproduce

Current production helper:

`skills/cogentnexus-openclaw/scripts/namespace_ownership.py::_plugin_payload()`

hashes only:

- `openclaw.plugin.json`;
- `package.json`;
- `scripts/bootstrap-ticket-db.mjs`;
- `dist/ticket-store.js`.

It therefore ignores most shipped runtime code.

Task 093 changed the runtime that compiles to:

`dist/v091-dashboard-verified-delivery.js`

but the reported fingerprint remained the same as the pre-fix live package:

`8fd911e3b8f6326c8907b7d92c11028d931df203dcaafdb59cc1e6d0a3b56360`

That means `classify-install` can incorrectly return `pluginAlreadyExact=true`, making the installer skip the Task-093 package installation entirely.

---

# Absolute live/semantic fence

Task 094 is source/test-only.

Read-only inspection/fingerprinting of the current installed plugin root is allowed solely to prove old-live vs candidate payload identity/difference.

Do NOT:

- install/install-over/uninstall/reset/cleanup;
- mutate any OpenClaw plugin generation;
- mutate ownership/controller/startup/Supervisor/AGENTS/config/runtime/SQLite;
- send Dashboard/WebChat content;
- call `chat.send`, `chat.inject`, `openclaw agent`, `sessions_send` or a channel send;
- generate a semantic nonce;
- call Ollama/provider directly;
- repair/rewrite Task-092 Ticket/session/transcript evidence;
- change provider/model/timeouts;
- restart/reboot;
- merge/tag/release.

Use a fresh isolated source worktree from the coordination execution HEAD.

---

# Phase A — re-prove the defect before edits

1. Fetch/reset the coordination branch and record the execution HEAD.
2. Prove Task-093 implementation/report/review are ancestors.
3. Verify Task-093 publication fence remains valid.
4. Create an isolated worktree.
5. Build/validate the Task-093 plugin candidate exactly as production would.
6. Using the current `_plugin_payload()` implementation, prove that a copy differing only in `dist/v091-dashboard-verified-delivery.js` still produces the same fingerprint.
7. If read-only live inspection is available, prove the currently installed pre-Task093 runtime and the Task-093 candidate are behaviorally/file-wise different while the old fingerprint contract cannot distinguish them.

If this defect cannot be reproduced, stop with:

`BLOCKED_FINGERPRINT_DEFECT_UNPROVEN`.

---

# Gate R — mandatory RED

Before production changes, add the smallest executable regression tests using the real production fingerprint helper.

Required RED cases:

1. Copy an exact valid plugin package fixture.
2. Change only one shipped runtime file under `dist/**`, specifically a non-`ticket-store.js` file such as `dist/v091-dashboard-verified-delivery.js`.
3. Assert the fingerprint must change.
4. Under the current four-file implementation, watch this assertion fail because fingerprints remain equal.

Add RED coverage for path identity as well:

- rename/add/remove a shipped runtime file under `dist/**` and require fingerprint change.

The RED must fail for the intended attestation reason, not because fixture identity/package validation is broken.

---

# Gate F — canonical complete installable-payload fingerprint

Implement one canonical package-payload enumerator/fingerprint source of truth in `namespace_ownership.py` and make all existing fingerprint consumers use it.

## F1 — package contract authority

Use `package.json` as the package ownership contract.

For the current CogentNexus-OpenClaw package, `package.json.files` identifies shipped package-owned content such as:

- `dist`;
- `scripts/bootstrap-ticket-db.mjs`;
- `openclaw.plugin.json`;
- `README.md`.

`package.json` itself is always included in the fingerprint because npm includes package metadata even though it is not listed in `files`.

Do not hardcode individual runtime JS filenames.

The implementation may enforce the current package contract strictly. Unsupported wildcard/glob/path forms should fail closed rather than silently omit files.

## F2 — deterministic expansion

For every safe literal `files` entry:

- normalize it as a relative package path;
- reject absolute paths, `..` traversal, empty/ambiguous paths, NULs or platform path escape;
- if it names a regular file, include that file;
- if it names a directory, recursively include every regular file beneath it;
- reject symlinks/reparse-style path indirection that could escape or make the payload ambiguous;
- reject a declared entry that is missing;
- deduplicate canonical relative paths;
- sort using one stable cross-platform relative-path representation (POSIX `/` form recommended).

Development-only content not selected by the package contract must remain outside the fingerprint domain, including normal `src/**`, tests, `node_modules/**`, caches and transient `.tgz` artifacts.

## F3 — canonical digest framing

Use a versioned fingerprint domain separator so the new algorithm is explicit, for example conceptually:

`cogentnexus-openclaw-plugin-payload-v2\0`

Then for every sorted file:

`normalized-relative-path UTF-8 + NUL + exact file bytes + NUL`

The absolute root path must never enter the digest.

Consequences that must hold:

- content byte change -> fingerprint changes;
- file add/remove -> fingerprint changes;
- rename/path change -> fingerprint changes;
- same package copied to another root -> fingerprint identical.

Return the same external 64-hex SHA-256 shape expected by existing rollover/classification contracts.

## F4 — package identity validation remains strict

Before fingerprinting, preserve/strengthen existing identity checks:

- manifest id is `cogentnexus-openclaw`;
- manifest version is exact expected version;
- npm package name is `openclaw-plugin-cogentnexus-openclaw`;
- npm package version is exact expected version.

Malformed/missing `package.json.files`, unsafe payload paths or incomplete declared payload must fail closed.

## F5 — actual npm package-set equivalence

Prove the canonical payload enumerator corresponds to what the current package ships.

On both supported npm paths (Node 24/npm 11 and Node 22/npm 12):

- use package validation/pack metadata to obtain the actual packed file path set without relying on tarball byte identity;
- compare that path set to the canonical fingerprint file set, allowing only npm-mandatory metadata behavior that is explicitly understood and documented;
- no shipped runtime file may exist outside the fingerprint domain.

Do not fingerprint the `.tgz` container itself; archive metadata is not the attestation authority.

---

# Gate C — classifier/lifecycle integration truth table

After GREEN, prove the new fingerprint reaches the existing install classifier and lifecycle resolver correctly.

## C1 — changed installed runtime

One coherent manifest-owned installed generation contains the pre-Task093 runtime; candidate source contains Task-093 runtime fix.

Required classification:

- `mode = upgrade`;
- `pendingRollover = false`;
- `pluginAlreadyExact = false`.

Required production lifecycle actions with `SkipPlugin=false`:

- `installPlugin = true`;
- `rolloverPlugin = true`.

This must prove the Task-093 fix will actually be installed rather than skipped.

## C2 — exact installed runtime

Installed package and candidate package have identical canonical payload.

Required classification:

- `mode = upgrade`;
- `pendingRollover = false`;
- `pluginAlreadyExact = true`.

Required actions:

- `installPlugin = false`;
- `rolloverPlugin = false`.

## C3 — two-generation pending rollover

Preserve Task-084/085/086 exact behavior under the new fingerprint algorithm:

- exactly two generations;
- manifest binds retired generation;
- active replacement must exactly equal expected candidate fingerprint when explicit expected source attestation is supplied;
- pending path remains `installPlugin=false`, `rolloverPlugin=true`;
- equivalent-generation legacy behavior without an explicit expected fingerprint remains only where previously authorized;
- changed replacement without expected source attestation remains rejected.

## C4 — ambiguity/security

Preserve rejection for:

- 3+ canonical candidates;
- active registration outside OpenClaw state boundary;
- invalid wrapper/project ownership;
- wrong package/id/version;
- inventory/manifest/plan hash drift;
- unsafe paths or symlinks;
- replacement fingerprint mismatch.

---

# Gate T — required regression matrix

At minimum test:

1. Task-093 runtime-only JS change changes fingerprint;
2. any `dist/**` content change changes fingerprint;
3. add/remove/rename under shipped `dist/**` changes fingerprint;
4. README/bootstrap/manifest/package metadata change changes fingerprint when still identity-valid;
5. same package at different absolute roots hashes identically;
6. source-only `src/**` or test change does not change installable payload fingerprint unless it changes built `dist/**`;
7. `node_modules/**`, transient tarball/cache files do not enter fingerprint;
8. unsafe path traversal rejected;
9. symlink/path indirection rejected;
10. missing declared package file rejected;
11. malformed/unsupported `files` contract rejected;
12. npm11 packed file set and canonical fingerprint file set are equivalent;
13. npm12 packed file set and canonical fingerprint file set are equivalent;
14. changed single-generation classification -> install+rollover;
15. exact single-generation classification -> neither;
16. pending two-generation classification -> rollover-only;
17. explicit expected fingerprint mismatch rejected;
18. Task-084/085/086 rollover plan/apply atomicity/security fixtures remain green;
19. Task-089 PowerShell action-resolver boundary and installer AST/order invariants remain green;
20. Task-093 Dashboard staging tests remain green unchanged except fixture updates required by the new fingerprint test domain.

---

# Full verification

Record fresh evidence for:

- focused fingerprint RED then GREEN;
- classification/action truth-table tests;
- plugin generation rollover tests;
- namespace/install/recovery tests from Tasks 067-075 and 082-090 as applicable;
- PowerShell 5.1 syntax/action/installer-AST checks;
- npm pack artifact parser tests;
- full Python suite;
- Python `py_compile` where applicable;
- Node 24/npm 11 clean plugin suite + `plugin:validate` + build + schema/bootstrap/package verification;
- Node 22/npm 12 isolated clean plugin suite + `plugin:validate` + build + schema/bootstrap/package verification;
- Task-093 Dashboard verified-delivery focused tests;
- baseline consistency;
- `git diff --check`;
- clean final worktree.

Record the exact new v2 candidate fingerprint after the final build.

If read-only live comparison is available, also record:

- current installed pre-Task093 v2 fingerprint;
- Task-093+094 candidate v2 fingerprint;
- proof they differ.

Never mutate live state to obtain this evidence.

---

# Publication fence

Commit source/tests first.

Then publish a separate report-only commit:

`docs/operations/coordination/reports/CNX-20260827-094-repair-complete-installable-plugin-payload-fingerprint.md`

Required result tokens:

- `PASS_COMPLETE_INSTALLABLE_PLUGIN_PAYLOAD_ATTESTATION_REPAIRED`
- `BLOCKED_FINGERPRINT_DEFECT_UNPROVEN`
- `BLOCKED_PACKAGE_PAYLOAD_CONTRACT_UNSAFE`
- `BLOCKED_NPM_PACKAGE_SET_MISMATCH`
- `BLOCKED_CLASSIFICATION_OR_ROLLOVER_REGRESSION`
- `BLOCKED_SECURITY_OR_PATH_REGRESSION`
- `BLOCKED_TEST_OR_VALIDATION_FAILURE`
- `BLOCKED_EVIDENCE_PUBLICATION_UNSAFE`

## Successor gate

Only independent acceptance of:

`PASS_COMPLETE_INSTALLABLE_PLUGIN_PAYLOAD_ATTESTATION_REPAIRED`

may authorize the next live task.

That live successor must install the exact accepted Task-093+094 source through one supported install-over, prove the new fingerprint caused real package installation and ownership-safe rollover, restore MANAGED parity/health, and send **zero** semantic messages.

Only after that live parity task is independently accepted may one new final authenticated fresh-session semantic attempt be authorized.