# CNX-20260828-113 — Independent Review

## Verdict

`SOURCE REPAIR ACCEPTED; TASK COMPLETION BLOCKED — REQUIRED DIRECT CLASSIFY_INSTALL MATRIX INCOMPLETE`

Task 113 repaired the confirmed conflicting-product-evidence defect and produced valid exact-source CI/package evidence. However, the task's explicit test contract was not completed: the mandatory test-only commit did not contain the full direct `classify_install(...)` matrix required before production editing. Therefore candidate `d8c5f5f5e7936e673a6731f5a8a0f17e7bd39a06` is accepted as source-repair evidence but is **not yet live-authorized**.

## Fresh repository evidence

Task-113 report HEAD:

`20d2734a4ae62086d8af3ca2768f9c844361fbf7`

Candidate-to-report comparison is exactly one documentation file:

`docs/operations/coordination/reports/CNX-20260828-113-interrupted-reentry-conflicting-wrapper-matrix-closure.md`

No production or test drift exists between candidate and report.

## TDD evidence accepted for the actual defect

The first Task-113 implementation commit was test-only:

`fe72982c89c10dfd5fbc447c89d6bfc827e68e61`

It changed only:

`tests/test_plugin_generation_rollover.py`

The mandatory direct and managed conflicting-wrapper scenarios were semantic REDs under the predecessor source. Reported selector result:

`2 failed, 5 passed, 33 deselected`

Both failures were `DID NOT RAISE RuntimeError`, proving the actual defect before production repair.

The production repair commit was separate and directly followed the RED commit:

`d8c5f5f5e7936e673a6731f5a8a0f17e7bd39a06`

It changed only:

`skills/cogentnexus-openclaw/scripts/namespace_ownership.py`

The repair is narrow and source-derived. After proving the active storage shape, re-entry now obtains `product_plugin_inventory(...)` and permits only:

- direct shape: `directPlugin`;
- managed shape: `npmPackage:<active-project>` plus `npmWrapper:<active-project>`.

Any other CogentNexus product storage evidence fails closed. Classification performs no cleanup or mutation.

## Residual task-contract failure

Task 113 explicitly required its same test-only commit to add direct `classify_install(...)` coverage for at least:

- active foreign/shared wrapper;
- separate conflicting wrapper evidence;
- multiple exact canonical payloads;
- non-unique active registration;
- active root outside OpenClaw state;
- contained but noncanonical active root;
- wrong id;
- wrong package;
- wrong version;
- candidate fingerprint mismatch;
- controller not passthrough;
- corrupted/mismatched ownership manifest metadata;
- missing `SKILL.md`;
- missing launcher;
- mixed legacy/new namespace;
- altered retired path staying on normal rollover rather than the re-entry shortcut;
- explicit valid direct and managed positive cases.

Git history shows `fe72982c...` added only the direct-positive helper/case and the two separate conflicting-wrapper cases. It did **not** commit the complete required direct matrix before production edit. The Task-113 report instead relies on older tests for the remaining dimensions. Those older tests are useful regression evidence, but they do not satisfy the explicit Task-113 requirement that this early-return surface be directly visible in the Task-113 test-only commit.

This cannot be corrected retroactively by pretending the missing tests preceded the production change.

## Independent CI verification

All required workflows are exact-source successes on candidate `d8c5f5f5e7936e673a6731f5a8a0f17e7bd39a06`:

- Validate `33170454396` — completed/success, attempt 2;
- Windows Installer Pack Smoke `33170454132` — completed/success;
- PS5.1 Acceptance Smoke `33170454130` — completed/success.

The Validate rerun remained on the same source SHA.

## Independent artifact verification

Artifact:

- ID `9685376213`;
- name `cogentnexus-openclaw-v0.9.3-package-proof-d8c5f5f5e7936e673a6731f5a8a0f17e7bd39a06`;
- workflow head SHA `d8c5f5f5e7936e673a6731f5a8a0f17e7bd39a06`;
- outer SHA256 `20b0c096061363509045d7c93dad97068a2c3cae084fd2ba54c7e9e9a0b57731`.

Independent extraction/hash verification produced:

- inner ZIP SHA256 `76b363dbb7ab49137d4335e5c08ee7d381fea06f4ed265743d2482708b151499`;
- tar.gz SHA256 `32627e56a411092e03b74017741ba714d9f801843205e2bb0a902fe084b616dd`;
- source commit `d8c5f5f5e7936e673a6731f5a8a0f17e7bd39a06`;
- version `0.9.3`;
- payload file count `178`;
- payload fingerprint `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`.

Packaged source contains the conflicting-product-evidence rejection, Task-110 retired-tree exactness, and `openclaw plugins install $packagePath --force` for installation-required paths.

## Decision

Do not discard or revert the Task-113 source repair. It is technically supported by semantic RED/GREEN and exact CI/package proof.

Do not authorize it for live Windows acceptance yet because the required direct classification matrix is incomplete.

Open a validation-first Task 114. Task 114 must commit the complete direct matrix before any further production edit. If all matrix cases pass on the current repair, production source must remain unchanged. If a matrix case exposes a real defect, that tests-only commit becomes legitimate RED evidence and only then may a minimal source repair follow.

## Safety gate

Until Task 114 passes independent review:

- no real-Windows install/reset/uninstall/reinstall/lifecycle/recovery action;
- no Task-107 replay or manual normalization;
- no Dashboard semantic Send;
- no OpenClaw/Ollama update/reinstall/uninstall/rebaseline;
- no live config/SQLite/session mutation;
- no merge/tag/release/force push.
