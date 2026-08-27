# Coordination Channel Status

**State:** `READY_FOR_HERMES`
**Updated:** 2026-08-27 ICT
**Transport:** GitHub repository history
**Human authority:** operator approved the complete installable-payload fingerprint design and remains authority for definitive repair through final fresh-session semantic acceptance
**Execution trigger:** manual Hermes continuation; scheduled execution remains disabled

## Accepted baseline

Accepted source/live lineage through Tasks 078/079/080, 082, 084/085/086, 089, 090 and 091 remains in force.

Task 090 live recovery remains accepted: MANAGED, one canonical loaded plugin, accepted source/live parity, Gateway/Ollama/SQLite healthy and `NO_FLASH_MULTI_TICK_PROVEN`.

Task 091 authenticated Dashboard/WebChat owner surface remains accepted without secret disclosure.

Task 092 remains an accepted semantic blocker: first fresh-session creation, Ticket-before-provider ordering, one correlated Ollama inference and one visible nonce passed; durable payload staging did not.

Task-092 semantic artifacts remain retired evidence.

## Task 093 result

Implementation:

`a924157ecdedef1d4f166d5762529b0d59536fc9`

Report:

`62fdd69d2a4a27566c0e986171b949347cf0df68`

Reported result:

`PASS_DASHBOARD_DURABLE_PAYLOAD_STAGING_REPAIRED`

Independent disposition:

`REWORK_PLUGIN_FINGERPRINT_DOES_NOT_ATTEST_RUNTIME_PAYLOAD`

The Task-093 staging repair remains the preserved candidate fix. Exact OpenClaw loader review supports its per-registration API lifetime model.

## Why Task 093 cannot be installed yet

Production plugin fingerprinting is only a four-file sample. It does not bind most installed runtime code.

The Task-093 runtime change compiles into `dist/v091-dashboard-verified-delivery.js`, but the reported fingerprint remained identical to the pre-fix live plugin because that file is outside the current fingerprint domain.

`classify-install` uses the fingerprint to decide `pluginAlreadyExact`. Therefore the old live plugin can be incorrectly classified as exact and the supported installer can skip the Task-093 package installation.

## Operator-approved Task 094 design

The next task uses `package.json` as the installable package contract and fingerprints the complete package-owned payload rather than the repository or a hardcoded runtime-file sample.

Canonical v2 fingerprint requirements:

- include `package.json` plus every safe regular file selected by `package.json.files`;
- recursively cover all shipped `dist/**` runtime code;
- cover shipped manifest/bootstrap/README metadata;
- sort normalized relative POSIX-style paths;
- hash versioned domain separator + relative path + NUL + exact bytes + NUL;
- never include absolute installation root;
- reject traversal, unsafe/symlink path indirection, missing declared content or unsupported package-file patterns;
- exclude development-only source/tests/node_modules/cache/tarball content not selected by the package contract.

Actual npm 11 and npm 12 packed file path sets must be proven equivalent to the canonical fingerprint payload set. Tarball container bytes are not the attestation authority.

## Active Task 094

[`tasks/CNX-20260827-094-repair-complete-installable-plugin-payload-fingerprint.md`](tasks/CNX-20260827-094-repair-complete-installable-plugin-payload-fingerprint.md)

Execution mode:

`SOURCE_TDD_COMPLETE_INSTALLABLE_PLUGIN_PAYLOAD_ATTESTATION`

Authorization:

`TASK093_DEPLOYMENT_ATTESTATION_REPAIR_AUTHORIZED`

Task 094 must RED the current blind spot before production edits, then preserve the complete classifier/lifecycle/rollover truth tables under the new v2 fingerprint.

Required deployment proof includes:

- Task-093 candidate v2 fingerprint differs from current pre-fix live payload;
- changed single-generation state => `pluginAlreadyExact=false`, install+rollover;
- exact state => no install/no rollover;
- pending two-generation state => rollover-only;
- same-version rollover source attestation and atomicity/security remain intact;
- npm 11/npm 12 package behavior remains compatible.

## Hard fence

Task 094 performs no live mutation and sends zero semantic/provider messages.

Only read-only inspection/fingerprinting of the current installed plugin root is allowed for attestation evidence.

No install/reset/repair, generation mutation, controller/startup/Supervisor/AGENTS/config/runtime/SQLite change, provider/model/timeout change, reboot, merge, tag or release is authorized.

## Successor logic

Only independent acceptance of:

`PASS_COMPLETE_INSTALLABLE_PLUGIN_PAYLOAD_ATTESTATION_REPAIRED`

may authorize a one-shot supported live install-over of the exact accepted Task-093+094 source.

That live installation task must restore and prove MANAGED/source parity/health with zero semantic sends. Only after its independent acceptance may a new final authenticated fresh-session semantic attempt be authorized.
