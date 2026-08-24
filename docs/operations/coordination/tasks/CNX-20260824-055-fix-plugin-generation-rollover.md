# CNX-20260824-055 — Fix Ownership-Safe Plugin Generation Rollover

Status: `READY_FOR_CODEX`

Execution mode: `AUTO_REPOSITORY_ONLY`

Owner: ChatGPT

Executor: Codex

## Goal

Fix the v0.9.3 Windows and POSIX install-over path so replacing the canonical OpenClaw plugin cannot leave multiple exact payload roots at ownership resolution, and add a fail-closed recovery primitive for the exact Task 054 partial state.

This task changes and tests repository code only. It must not repair, enable, reinstall, or otherwise mutate the live installation.

## Accepted diagnosis

Task 054 proved that `openclaw plugins install ... --force` created a new generated npm project while the prior manifest-owned project remained. Both roots contained the same canonical v0.9.3 payload fingerprint, so `resolve_installed_plugin` correctly rejected ambiguity. The installer then stopped in PASSTHROUGH before ownership recreation and enable.

The ambiguity rule is a safety invariant and must not be relaxed.

## Required investigation

Before implementation, inspect read-only:

- the retained Task 054 wrapper/poststate and explain why its exit code became null;
- exact `openclaw plugins install/uninstall/list --help` behavior available on the machine;
- the redacted structural shape of `openclaw plugins list --json` needed to identify the active canonical path;
- the exact relationship between the old manifest-owned npm wrapper/project and the new active generated project;
- Windows and POSIX installer ordering.

Do not access secrets or mutate the live plugin/runtime while investigating.

## Required design invariants

1. A coherent upgrade begins from an exact manifest-owned plugin root.
2. Replacement must use supported OpenClaw plugin management where possible.
3. Only the exact product-owned prior wrapper/project may be retired; unrelated npm projects must never be selected.
4. The replacement root must be exact canonical ID/package/version, contained under the OpenClaw state, and bound to the active canonical registration.
5. Before ownership manifest creation, exactly one canonical payload root must remain.
6. Any missing, extra, conflicting, foreign, out-of-bound, or unproven root fails closed in PASSTHROUGH.
7. Fresh install, legacy migration, linked install, `SkipPlugin`, and POSIX behavior remain explicitly covered.
8. Do not solve the defect by deduplicating candidates in the resolver or accepting identical fingerprints at multiple paths.
9. Recovery of the Task 054 partial state must be plan-first, exact-path, recoverable, and separately authorized before apply.

## TDD requirements

Add failing tests before production changes. At minimum cover:

- reproduced upgrade: old manifest-owned npm project plus newly generated active project causes the current ambiguity;
- corrected upgrade leaves exactly one active canonical payload before manifest creation;
- prior owned project is retired only after exact ownership and replacement proofs;
- unrelated npm projects and similarly named directories remain byte-identical;
- conflicting/foreign/unproven replacement blocks without retiring anything;
- fresh install does not attempt prior-generation retirement;
- `SkipPlugin` preserves the verified current generation;
- linked-plugin handling is explicit and cannot mix linked and npm-managed roots;
- Windows and POSIX installers preserve equivalent ordering/invariants;
- recovery plan for the exact two-root state identifies old manifest path, active replacement path, owning wrapper roots, backup destination, and expected hashes;
- recovery apply requires the exact reviewed plan/hash, moves rather than broadly deletes the retired project, atomically updates ownership, and rolls back on verification failure;
- after recovery, exactly one candidate resolves and manifest verification passes;
- wrapper exit capture test proves numeric zero and nonzero codes and rejects null/unobserved exit.

Use fake OpenClaw/plugin fixtures for mutation tests. Do not use the live OpenClaw state as a test fixture.

## Implementation direction

Choose the smallest robust design supported by the investigation. Acceptable designs include verified uninstall-before-install or an explicit active-generation transition, provided all invariants and tests above hold.

The repository must expose a narrow recovery plan/apply interface that Task 056 can invoke against the Task 054 state. It must:

- verify the existing ownership manifest without requiring single-candidate resolution;
- prove exactly two canonical candidates;
- prove one candidate is the old manifest-owned path;
- prove the other candidate is the active registered replacement;
- bind every path, package ID, version, wrapper ownership, and expected fingerprint/hash;
- produce a machine-readable plan and SHA-256;
- require the exact plan hash during apply;
- move the retired product-owned wrapper/project into a unique CogentNexus-OpenClaw backup location;
- atomically update the manifest to the replacement path;
- verify one candidate and exact ownership after apply;
- restore the old wrapper and manifest automatically if apply verification fails.

The recovery primitive must not enable MANAGED mode itself. Lifecycle return belongs to the separately reviewed live-repair task.

## Verification

Run:

- focused new RED/GREEN tests;
- existing namespace ownership/install-contract/namespace-lint suites;
- Windows PowerShell parser/static contract checks;
- POSIX shell syntax/static contract checks;
- full repository test suite;
- compile/type/build checks already required by the project;
- changed-path and namespace-isolation validation.

Record exact commands and results.

## Results

Return exactly one:

- `PASS_PLUGIN_GENERATION_ROLLOVER_FIXED`
- `BLOCKED_OPENCLAW_PLUGIN_SEMANTICS_UNPROVEN`
- `BLOCKED_RECOVERY_PRIMITIVE_UNSAFE`
- `BLOCKED_TEST_FAILURE`
- `BLOCKED_UNRELATED_DRIFT`
- `BLOCKED_REPORT_PUBLICATION_UNSAFE`

## Report and publication

Publish:

`docs/operations/coordination/reports/CNX-20260824-055-fix-plugin-generation-rollover.md`

The report must include diagnosis, wrapper-null cause, selected design and rejected alternatives, RED/GREEN evidence, exact changed paths/commits, focused/full results, recovery-interface contract, remaining uncertainty, live-action count `0`, and one exact result token.

Implementation commits may change only the minimal installer/ownership/recovery/test/documentation paths required by the fix. The final report commit must add exactly the Task 055 report path relative to the implementation HEAD.

No `ACTIVE.md` or `STATUS.md` edit is authorized inside Task 055.

## Live-system fence

No live installer, plugin install/uninstall, generation retirement, recovery apply, ownership rewrite, AGENTS edit, enable/disable/start/stop/restart, scheduler change, Gateway/Ollama/model mutation, process termination, primary-repository mutation, Procmon/Task 027/038 access, or excluded-system action.

The Task 054 evidence directory and isolated clone must remain intact.

## Progress communication

Report meaningful progress approximately every 3 minutes and immediately after root-cause confirmation, RED reproduction, design selection, GREEN implementation, full validation, and publication.

Updates are not pause points unless a stop gate fires.

