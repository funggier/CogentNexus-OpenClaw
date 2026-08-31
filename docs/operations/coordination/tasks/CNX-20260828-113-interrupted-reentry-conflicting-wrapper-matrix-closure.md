# CNX-20260828-113 — Interrupted Re-entry Conflicting-Wrapper and Matrix Closure

- Status: `READY_FOR_HERMES`
- Execution mode: `SOURCE_ONLY_TDD`
- Owner / reviewer: ChatGPT
- Executor: Hermes/Codex after operator continuation
- Date: 2026-08-28 ICT
- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`

## Goal

Close the residual interrupted-rollover re-entry ambiguity found during independent review of Task 112 and finish the direct `classify_install(...)` contract matrix before any real-Windows lifecycle acceptance is authorized.

Task 112 correctly hardened the **active** replacement storage boundary. Task 113 addresses a different condition: one exact active replacement is valid, but an additional foreign/shared CogentNexus-related wrapper exists elsewhere under OpenClaw npm projects. The current shortcut ignores that extra product evidence and still returns `interruptedRolloverReentry=True`.

This task is source/test/CI only. It does not authorize real-Windows mutation.

## Authoritative predecessor evidence

- Task-107 live report: `docs/operations/coordination/reports/CNX-20260828-107-v093-real-windows-lifecycle-acceptance-retry.md`
- Task-112 report: `docs/operations/coordination/reports/CNX-20260828-112-interrupted-reentry-ownership-proof-hardening.md`
- Task-112 independent review: `docs/operations/coordination/reviews/CNX-20260828-112-interrupted-reentry-ownership-proof-hardening-review.md`
- Task-112 RED: `bb8212584b1b7934cc2d9e1d7bc6b5e0303699f2`
- Task-112 source candidate: `023be1a8075c0aa602adda357db9924c170ffb8e`
- Task-112 report descendant: `36bf664ca481d49046d86d5c3993b73185a769e9`
- Task-112 review commit: `ee3f0dca79929ce771add3381d1817766b2ff8f7`
- Task-112 artifact `9684336683` is historical evidence only and is not live-authorized.

Task-112 review verdict:

`REJECTED — RESIDUAL CONFLICTING-WRAPPER RE-ENTRY DEFECT + REQUIRED MATRIX NOT COMMITTED`

## Confirmed source defect

At Task-112 candidate `023be1a8...`, `_classify_interrupted_rollover_reentry(...)` proves:

- exact manifest metadata with retired plugin existence excluded;
- PASSTHROUGH controller;
- missing retired path;
- non-plugin artifacts;
- no legacy namespace;
- exact active registration/payload/fingerprint;
- exactly one exact payload candidate;
- direct canonical storage OR strict active npm-wrapper ownership.

But it does **not** prove that all other CogentNexus-specific OpenClaw storage evidence is absent or attributable to that active replacement.

`current_inventory(...)` uses `product_plugin_inventory(...)`, which can report another `npmWrapper:<project>` merely because that wrapper declares `openclaw-plugin-cogentnexus-openclaw`. If the extra wrapper has no exact child payload, it does not increase the exact candidate count. The shortcut therefore accepts the state despite conflicting product evidence.

Independent reviewer reproduction against the exact packaged Task-112 candidate confirmed this for:

1. exact managed-npm active replacement + separate foreign wrapper;
2. exact canonical direct-extension active replacement + separate foreign wrapper.

In both cases `current_inventory(...)` contained the extra `npmWrapper:user-shared-wrapper=...`, while `classify_install(...)` still returned `interruptedRolloverReentry=True`.

This violates the inherited no-conflicting-wrapper/no-ambiguous-product-evidence invariant.

## Live-shape relevance

Task 107 recorded that OpenClaw installed the replacement to:

`~\.openclaw\extensions\cogentnexus-openclaw`

and removed the old manifest-owned npm generation. Therefore the **canonical direct-extension** re-entry shape is especially important. Task 113 must explicitly test it rather than infer it from npm-generation fixtures.

## Core invariant

Interrupted rollover re-entry is valid only when all CogentNexus-specific OpenClaw storage evidence is exactly explainable by one accepted active replacement shape.

### Valid direct shape

If active root is exactly:

`<openclaw-state>/extensions/cogentnexus-openclaw`

then product storage evidence must contain that direct product extension and no additional CogentNexus npm package/wrapper evidence.

### Valid managed-npm shape

If active root is exactly an accepted managed child:

`<openclaw-state>/npm/projects/<managed-project>/node_modules/openclaw-plugin-cogentnexus-openclaw`

then:

- `_npm_project_for_plugin(...)` / `_managed_wrapper_proof(...)` must pass;
- the CogentNexus-specific product inventory must be exactly attributable to that active child + its proven wrapper;
- no other CogentNexus direct extension, npm package, or wrapper evidence may exist.

### Failure rule

Any extra product evidence — including a foreign/shared wrapper with no exact child payload — is ambiguous and must fail closed before installer mutation.

Do not delete or normalize the conflicting state during classification.

## Phase 0 — reconcile before editing

1. Fetch current remote branch HEAD.
2. Confirm Task 113 is active in both `ACTIVE.md` and `STATUS.md`.
3. Read Task-107 report, Task-112 report, and Task-112 independent review.
4. Compare production/test source with `023be1a8075c0aa602adda357db9924c170ffb8e`; stop `BLOCKED` on unexplained production drift.
5. Inspect completely:
   - `product_plugin_inventory(...)`;
   - `current_inventory(...)`;
   - `plugin_candidate_roots(...)`;
   - `_active_registered_plugin(...)`;
   - `_npm_project_for_plugin(...)`;
   - `_managed_wrapper_proof(...)`;
   - `_classify_interrupted_rollover_reentry(...)`;
   - `classify_install(...)`;
   - installer action resolver and final `resolve-plugin -> ownership create -> verify` path;
   - existing re-entry/rollover tests.

No live machine action.

## Phase 1 — mandatory TEST-ONLY matrix commit

The first Task-113 implementation commit must contain tests only. It must be pushed before any Task-113 production edit.

Use the actual production `classify_install(...)` surface. String/order-only tests are not sufficient.

### Mandatory RED A — direct active replacement + separate conflicting wrapper

Model the closest Task-107 shape:

1. exact v0.9.3 manifest/controller/skill/launcher;
2. controller `passthrough`;
3. manifest-owned old npm generation removed;
4. exactly one active replacement at canonical direct path `<openclaw-state>/extensions/cogentnexus-openclaw`;
5. active payload/fingerprint exactly matches candidate;
6. create a separate npm project whose wrapper declares `openclaw-plugin-cogentnexus-openclaw` plus unrelated user dependency evidence, but provides no exact canonical plugin child;
7. prove `current_inventory(...)` contains that extra `npmWrapper:*` product evidence;
8. call actual `classify_install(...)`.

Current Task-112 source is expected to incorrectly return successful re-entry.

Desired result: `RuntimeError` / non-zero ambiguous product evidence.

### Mandatory RED B — managed active replacement + separate conflicting wrapper

Repeat the same conflict with the active replacement in a valid managed generation wrapper. The active wrapper itself must pass `_managed_wrapper_proof(...)`; the failure must be caused by the **additional** conflicting wrapper.

### Required positive direct tests

In the same test-only commit, explicitly prove the intended successful results for:

- exact canonical direct extension with no conflicting product evidence;
- exact managed npm replacement with its one proven wrapper and no conflicting evidence.

Both should return:

- `mode == "upgrade"`;
- `pendingRollover is False`;
- `pluginAlreadyExact is True`;
- `interruptedRolloverReentry is True`.

### Required direct negative matrix

In the same test-only commit, add direct `classify_install(...)` coverage for at least:

- active foreign/shared wrapper;
- separate conflicting wrapper evidence;
- more than one exact canonical payload;
- non-unique active registration;
- active root outside OpenClaw state;
- contained but noncanonical active root;
- wrong id;
- wrong package;
- wrong version;
- candidate fingerprint mismatch;
- controller not `passthrough`;
- corrupted/mismatched manifest metadata;
- missing `SKILL.md`;
- missing launcher;
- mixed legacy/new namespace;
- altered retired path must stay on normal rollover path, not re-entry shortcut.

Existing older tests may be reused via helpers, but the Task-113 commit must exercise the early-return `classify_install(...)` surface directly and make the matrix visible in Git history.

### RED evidence

Run a smallest selector proving at least one conflicting-wrapper scenario fails under current production. Record:

- test-only commit SHA;
- exact command;
- exact failing test count;
- failure assertion/output;
- confirmation that no production file changed in RED commit.

If both mandatory conflict tests unexpectedly pass, stop and investigate before production edits.

## Phase 2 — minimal production repair

Preferred file:

`skills/cogentnexus-openclaw/scripts/namespace_ownership.py`

Use existing inventory/ownership helpers. Do not duplicate wrapper parsing rules.

Expected design properties:

1. prove the active storage shape exactly as Task 112 already does;
2. obtain all CogentNexus-specific OpenClaw product storage evidence from `product_plugin_inventory(...)` or an equivalently exact helper;
3. derive the exact allowed evidence for the proven active shape;
4. direct active shape allows only the exact direct extension product evidence;
5. managed active shape allows only the exact active plugin child plus its exact proven wrapper;
6. any additional direct/npm-package/npm-wrapper evidence fails closed;
7. do not treat ordinary non-CogentNexus OpenClaw projects as conflicts;
8. do not mutate/delete conflicting evidence during classification;
9. retain all Task-110/111/112 exactness, fingerprint, containment, wrapper, PASSTHROUGH, and no-second-install behavior.

Do not weaken `product_plugin_inventory`, `_managed_wrapper_proof`, manifest validation, candidate attestation, or final ownership verification merely to pass tests.

Production repair must be a separate commit after the test-only matrix commit.

## Phase 3 — targeted GREEN

Run and record exact results for:

1. the Task-113 direct re-entry matrix;
2. all `tests/test_plugin_generation_rollover.py`;
3. namespace ownership/install contract tests;
4. installer transaction wiring;
5. fresh transaction recovery/failure coverage;
6. npm-12 local archive boundary;
7. plugin lifecycle action resolver.

Explicitly prove action selection for valid exact re-entry remains:

```json
{"mode":"upgrade","pendingRollover":false,"pluginAlreadyExact":true,"skipPlugin":false,"installPlugin":false,"rolloverPlugin":false}
```

No redundant external `openclaw plugins install` may be selected for valid already-exact re-entry.

## Phase 4 — full repository validation

Run fresh:

- full pytest suite;
- Python compile for modified ownership source;
- installer lifecycle/AST analysis;
- `npm ci`;
- `npm run plugin:validate`;
- `git diff --check`.

Record exact commands, counts, exits, and any reruns. A CI rerun is allowed only for demonstrably flaky infrastructure/test timing with unchanged source; record attempt history transparently.

## Phase 5 — exact same-source CI/package proof

Push one exact GREEN candidate and require on that exact SHA:

- Validate — success;
- Windows Installer Pack Smoke — success;
- PS5.1 Acceptance Smoke — success.

Produce a **new** package-proof artifact. Do not reuse Task-112 artifact `9684336683`.

Record and verify:

- exact candidate SHA;
- artifact ID/name;
- outer artifact SHA256/digest;
- inner v0.9.3 ZIP SHA256;
- tar.gz SHA256;
- `PACKAGE_IDENTITY.json` source/version;
- payload count/fingerprint;
- packaged conflicting-product-evidence rejection logic;
- packaged Task-112 active wrapper proof;
- packaged Task-110 retired-state exactness proof;
- installer local archive command remains exactly `openclaw plugins install $packagePath --force` when installation is required;
- recovery harness Git blob identity.

## Phase 6 — report and stop

Publish exactly:

`docs/operations/coordination/reports/CNX-20260828-113-interrupted-reentry-conflicting-wrapper-matrix-closure.md`

Report must include:

- repository reconciliation HEAD;
- test-only matrix commit SHA and full changed-file list;
- mandatory RED A/B evidence;
- direct positive/negative matrix results;
- production fix commit/files;
- targeted/full validation;
- exact three workflow runs and attempt history;
- new artifact identities/hashes/fingerprint;
- residual uncertainty;
- final `PASS`, `FAIL`, or `BLOCKED`.

After report publication, stop for independent ChatGPT review. Do not create or execute a live-Windows task.

## Hard fence — NOT authorized

Task 113 does not authorize:

- any real Windows install-over/reset/uninstall/reinstall/lifecycle/recovery action;
- replay of Task 107;
- manual cleanup/normalization of Task-107 residue;
- Dashboard semantic nonce/message/Send;
- OpenClaw/Ollama update, reinstall, uninstall, stop, or rebaseline;
- provider/model/timeout changes;
- live SQLite/config/session mutation;
- credentials/tokens/password access or re-entry;
- LM Studio management;
- process-tree kills;
- reboot;
- merge/tag/GitHub Release/force push;
- weakening namespace, wrapper, manifest, payload, ownership, or final verification boundaries.

If the conflict cannot be resolved without generic adoption or destructive cleanup, publish `BLOCKED` rather than weaken the boundary.
