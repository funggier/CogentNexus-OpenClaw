# Independent Review — CNX-20260828-110 Rollover Retired-State Exactness Repair

## Verdict

`ACCEPTED PASS — TASK-110 DEFECT REPAIRED; LIVE GATE BLOCKED BY PRE-EXISTING INTERRUPTED-ROLLOVER RE-ENTRY GAP`

Task 110 is accepted for its stated source-only scope. Its exact retired-state rollback defect is repaired with a valid separate RED -> production-fix history, broad GREEN validation, exact same-source CI, and exact package proof.

This review does **not** authorize real-Windows lifecycle acceptance yet. Independent review of the preserved Task-107 post-failure boundary against the Task-110 installer found a separate pre-existing re-entry gap: the machine state left by Task 107 cannot be safely classified by the current installer without an additional source repair.

## Task-110 TDD provenance — ACCEPTED

The required sequence is present in Git history:

1. Coordination head before Task 110: `07d7147bd363ad49147661544b26cd742490b321`.
2. Separate test-only RED commit: `edec90ac455cf3cf6b3b9842e5ca3fe5c0014338`.
   - parent: `07d7147bd363ad49147661544b26cd742490b321`;
   - changed only `tests/test_plugin_generation_rollover.py`;
   - production-shaped regression leaves the retired project directory present while deleting part of its owned payload, injects final ownership verification failure, and requires the normal manifest not to be restored.
3. Separate production fix commit: `25d229cd496a11af37ea2ff556a0126dfc194377`.
   - parent: `edec90ac455cf3cf6b3b9842e5ca3fe5c0014338`;
   - changed only `skills/cogentnexus-openclaw/scripts/namespace_ownership.py`.
4. Report commit: `efbb8f19d19dfcb9ad8b8525a6393996db688324`.
   - comparison from `25d229cd...` to `efbb8f19...` changes only the Task-110 report.

This satisfies the explicit Task-110 TDD provenance requirement.

## Task-110 source semantics — ACCEPTED

The production fix no longer treats mere path existence as proof that the old generation can safely receive `manifestBefore`.

On a failed final replacement verification, the old manifest is restored only when both transaction-bound proofs remain exact:

- `_project_tree_sha256(retiredProjectRoot) == retiredProjectTreeSha256`;
- the retired plugin payload fingerprint equals `retiredFingerprint`.

If the retired state is missing, incomplete, altered, or cannot be re-proved, the normal ownership manifest remains quarantined/removed and the operation fails non-zero. This preserves the Task-108/109 fail-closed intent without falsely reasserting a stale generation.

## Validation and package proof — ACCEPTED

Task-110 report records:

- semantic RED: `1 failed, 32 deselected` before production change;
- targeted GREEN: `3 passed, 30 deselected`;
- related GREEN set: `72 passed`;
- full repository validation: `424 passed, 3 skipped, 4 subtests passed`;
- Python compile, installer AST, npm install/plugin validation, and `git diff --check`: PASS.

Exact source candidate:

`25d229cd496a11af37ea2ff556a0126dfc194377`

Exact Actions evidence:

- Validate `33164787392` — `success`;
- Windows Installer Pack Smoke `33164787432` — `success`;
- PS5.1 Acceptance Smoke `33164787396` — `success`.

Independent GitHub checks confirm all three runs are bound to source `25d229cd496a11af37ea2ff556a0126dfc194377` and completed successfully.

Exact package proof:

- artifact ID `9683127656`;
- artifact name `cogentnexus-openclaw-v0.9.3-package-proof-25d229cd496a11af37ea2ff556a0126dfc194377`;
- outer SHA256 `90a9e329c040312ded336de4c7dd6f81b1c546aceb7869d6d284a119d7a87b25`;
- inner ZIP SHA256 `898413145589f4faede6cb04f3d478b956ab83492942747467ca674f13b890e3`;
- tar.gz SHA256 `b6a6056bb3d2472531000c1212621c878269a6f4f5d583164a3fb280c65ac047`;
- version `0.9.3`;
- payload file count `178`;
- payload-v2 fingerprint `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`;
- recovery harness Git blob `80da4a2a23f5b5e936d725dcbd695a631bad1cb6`.

Independent artifact extraction reproduced the outer/inner archive hashes, `PACKAGE_IDENTITY.json` source binding, payload identity, and packaged installer/ownership repair.

## Newly confirmed live-gate blocker

The preserved Task-107 report records that its one install-over attempt successfully performed the external OpenClaw plugin install and then failed ownership rollover. The attempt removed the previous manifest-owned npm generation while the normal ownership manifest remained from the pre-mutation state. The post-failure machine was left in PASSTHROUGH with OpenClaw/Gateway/Ollama healthy and installer residue intentionally retained.

No Tasks 108–110 performed live mutation, so Task 107 remains the last authoritative live boundary.

The Task-110 installer cannot safely re-enter that exact state today:

1. `recovery-preflight` sees an existing normal ownership manifest and returns `OWNERSHIP_PRESENT`; it only performs bounded automatic rollback for an incomplete **fresh-install** transaction.
2. `classify-install` then enters attested upgrade classification because product state/registration is present.
3. It calls `verify_manifest(..., verify_plugin=False)` without disabling `require_artifacts`.
4. `verify_manifest` therefore still requires `pluginPath` to exist.
5. The Task-107 retired `pluginPath` is the generation that the external install already removed.
6. Classification consequently fails closed with an incomplete-owned-installation condition before any Task-110 rollover transaction can begin.

This is desirable fail-closed behavior, but it means a new live install-over would predictably stop at pre-mutation classification rather than prove the repaired lifecycle.

## Required next action

Authorize a new **source-only TDD** task for interrupted-upgrade/rollover re-entry.

The repair must be narrowly bound to the Task-107-shaped state and must not become generic partial-state adoption. At minimum it must prove all of the following before allowing re-entry:

- exact normal ownership manifest schema/product/workspace/state/launcher identity remains valid;
- the manifest-owned prior plugin path is specifically missing after an interrupted upgrade, not merely altered/foreign;
- controller state is PASSTHROUGH;
- exactly one canonical active CogentNexus-OpenClaw replacement registration/payload is present;
- the active replacement is inside the OpenClaw boundary, exact version/package/id, and matches the expected candidate plugin fingerprint;
- no conflicting second product payload, mixed legacy namespace, or ambiguous registration exists;
- unrelated OpenClaw/user-owned state is not adopted or removed;
- successful classification/re-entry does not rerun an unnecessary external plugin install when the exact replacement is already present;
- the normal later ownership create+verify path rebinds durable ownership to the exact active replacement before MANAGED authority is granted;
- every mismatch remains non-zero/fail-closed.

A new real-Windows lifecycle task may be opened only after that source repair receives independent review and a new exact package proof.

## Safety decision

- Task 110: CLOSED / ACCEPTED PASS.
- Candidate `25d229cd496a11af37ea2ff556a0126dfc194377`: valid Task-110 source evidence, but **not yet live-authorized**.
- Artifact `9683127656`: valid Task-110 package evidence, but **not yet live-authorized**.
- Task 107 must not be replayed.
- Do not manually normalize/delete the preserved live residue.
- No Dashboard semantic Send is authorized.
