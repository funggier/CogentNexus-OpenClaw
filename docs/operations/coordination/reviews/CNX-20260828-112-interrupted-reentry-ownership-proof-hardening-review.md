# CNX-20260828-112 — Interrupted Re-entry Ownership-Proof Hardening — Independent Review

## Verdict

`REJECTED — RESIDUAL CONFLICTING-WRAPPER RE-ENTRY DEFECT + REQUIRED MATRIX NOT COMMITTED`

Task 112 fixes the specific defect identified in the Task-111 review: an **active** replacement child inside a foreign/shared npm wrapper is now rejected by reusing `_npm_project_for_plugin(...)` / `_managed_wrapper_proof(...)`. The exact candidate CI/package evidence is also valid.

However, Task 112 is not acceptable as the live-Windows candidate because the interrupted re-entry shortcut still ignores additional conflicting product-wrapper evidence that is not itself the active replacement, and the explicitly required direct `classify_install(...)` negative matrix was not committed.

## Reviewed source / evidence

- Task-112 RED: `bb8212584b1b7934cc2d9e1d7bc6b5e0303699f2`
- Task-112 production candidate: `023be1a8075c0aa602adda357db9924c170ffb8e`
- Task-112 report: `36bf664ca481d49046d86d5c3993b73185a769e9`
- Validate run: `33167878659` — successful attempt 2 on exact candidate
- Windows Installer Pack Smoke: `33167878626` — success on exact candidate
- PS5.1 Acceptance Smoke: `33167878630` — success on exact candidate
- package-proof artifact: `9684336683`

Independent artifact inspection confirmed:

- outer artifact SHA256: `2be47e00db355be28a782096bd1ab866c787b768f8eb0c3ecaa131a3802e91bf`;
- inner ZIP SHA256: `2240348a163c356fc7958c04f645b9a1f406db6c842fdbd86b4dd3efdeecc8c5`;
- tar.gz SHA256: `b6433b4a6c3d91a6185b3048146243b079b66015d5f7a76564ddf726fc4e81e0`;
- `PACKAGE_IDENTITY.json` source: `023be1a8075c0aa602adda357db9924c170ffb8e`;
- package version `0.9.3`, payload count `178`, payload fingerprint `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`;
- packaged local-archive install path remains `openclaw plugins install $packagePath --force` and contains no old `npm-pack:` invocation;
- packaged ownership source contains `_npm_project_for_plugin(active_root, paths["openclawState"])`, `_managed_wrapper_proof`, and Task-110 `retiredProjectTreeSha256` logic;
- packaged recovery harness Git blob remains `80da4a2a23f5b5e936d725dcbd695a631bad1cb6`.

The report-only descendant differs from the candidate only by the Task-112 report file.

## TDD provenance

The mandatory defect RED is valid:

- `bb821258...` has parent `17f16a1fc135d22919eacd38a7e989126836f662` (the Task-112 coordination HEAD);
- it changes only `tests/test_plugin_generation_rollover.py`;
- it adds the semantic foreign/shared **active-wrapper** regression;
- production candidate `023be1a8...` has direct parent `bb821258...` and changes only `namespace_ownership.py`.

So the core RED -> minimal-fix provenance is accepted.

## Accepted Task-112 repair

The nine-line production change is appropriately narrow:

1. exact direct canonical extension remains an allowed storage shape;
2. any non-direct active root must pass `_npm_project_for_plugin(...)`;
3. that helper enforces exact npm child layout and `_managed_wrapper_proof(...)`;
4. a foreign/shared active wrapper therefore fails closed before `interruptedRolloverReentry=True` is returned.

Independent execution against the packaged candidate reproduced:

- valid managed npm replacement -> accepted;
- valid canonical direct extension replacement -> accepted;
- active replacement inside a foreign/shared wrapper -> rejected.

## Blocking source defect — additional conflicting wrapper evidence is ignored

The re-entry helper still proves only the **active** replacement storage boundary and exact payload candidate count. It does not require the broader `product_plugin_inventory(...)` evidence to contain only the proven active storage shape.

Independent production-shaped reproduction against the exact packaged candidate:

1. construct the Task-107-shaped interrupted state: exact old manifest, PASSTHROUGH, old manifest-owned npm generation missing;
2. keep one exact active replacement;
3. add a separate foreign/shared npm project whose `package.json` declares `openclaw-plugin-cogentnexus-openclaw` plus unrelated user dependency evidence, but provides no exact canonical child payload;
4. `current_inventory(...)` reports the additional evidence as `npmWrapper:user-shared-wrapper=...`;
5. `plugin_candidate_roots(...)` / `_plugin_payload(...)` still sees only one exact active payload;
6. `_classify_interrupted_rollover_reentry(...)` proves the active replacement and returns `interruptedRolloverReentry=True` while silently carrying the extra conflicting wrapper in `inventory["new"]`.

This reproduced for both:

- a valid managed-npm active replacement; and
- the canonical direct-extension active replacement shape recorded by Task 107.

That violates the inherited Task-111/112 invariant that the shortcut must not accept conflicting wrapper / ambiguous product evidence or generically adopt a partial mixed product state.

The correct boundary is not merely “the active wrapper is owned”; the shortcut must prove that **all CogentNexus-specific OpenClaw storage evidence is exactly attributable to the one accepted active replacement shape**.

## Required negative matrix was not committed

Task 112 Phase 1 explicitly required the **same test-only RED commit** to add direct `classify_install(...)` coverage for:

- foreign/shared wrapper;
- more than one canonical payload;
- non-unique registration;
- out-of-bound root;
- wrong id/package/version;
- wrong controller mode;
- corrupt manifest metadata;
- missing `SKILL.md`;
- missing launcher;
- mixed legacy/new namespace;
- plus an explicit valid direct-extension case.

Git history shows `bb821258...` added only the foreign/shared active-wrapper test. No later test commit added the required matrix; `023be1a8...` is production-only.

Existing older rollover/plan tests are useful regression evidence but are not equivalent to the required direct exercise of the new early-return `classify_install(...)` surface. The Task-112 report therefore overstates compliance with the task contract.

Independent reviewer execution shows most omitted boundaries currently reject correctly, which is useful evidence, but the separately conflicting-wrapper case above demonstrates why the direct matrix was required.

## Provenance-report correction

The Task-112 report says the reconciled starting HEAD was `00aa1413397604f31c4d24582cece3225128b491`. Git history proves the Task-112 RED parent was actually `17f16a1fc135d22919eacd38a7e989126836f662`, the proper Task-112 coordination HEAD. Treat the report line as stale wording; Git history is authoritative.

## Live gate

No real-Windows action is authorized from Task 112.

Candidate `023be1a8075c0aa602adda357db9924c170ffb8e` and artifact `9684336683` remain valid historical source/package evidence only.

The next task must be source-only TDD, add the complete direct re-entry matrix in a separate test-only commit, reproduce the separate conflicting-wrapper acceptance defect, minimally tighten product-storage evidence, and produce a new exact candidate/artifact before live acceptance is reconsidered.
