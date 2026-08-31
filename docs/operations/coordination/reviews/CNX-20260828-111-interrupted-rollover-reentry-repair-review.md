# Independent Review — CNX-20260828-111 Interrupted Rollover Re-entry Repair

## Verdict

`REJECTED — RESIDUAL RE-ENTRY OWNERSHIP-PROOF DEFECT + INCOMPLETE NEGATIVE CONTRACT COVERAGE`

Task 111 is directionally correct and its positive Task-107-shaped re-entry architecture is useful, but the exact candidate is not yet safe enough to authorize real-Windows acceptance.

## Reviewed evidence

- Task report: `docs/operations/coordination/reports/CNX-20260828-111-interrupted-rollover-reentry-repair.md`
- test-only RED: `a7dace1ed86580c6ab39d72283eace3d7e76a02d`
- production candidate: `f4c8c993be80eaf54468f5b2630fd107050a1385`
- report-only descendant: `2840f427b310a45d02b20419dc201de274fce56c`
- Validate: `33166203340` — success
- Windows Installer Pack Smoke: `33166203285` — success
- PS5.1 Acceptance Smoke: `33166203316` — success
- package-proof artifact: `9683680142`

The RED commit is genuinely test-only and directly follows the Task-111 coordination head. The production candidate directly follows the RED commit. The report commit changes only the Task-111 report.

Independent artifact inspection confirmed:

- outer SHA256 `096b194423b83d14adf4dd26eb000612d53d31ef3f7f8c5385eb00e74756b422`;
- inner ZIP SHA256 `9ebbaac9c222f79d2291b6dfeb54791777abe1052b9c71614a9cff21239ade2e`;
- tar.gz SHA256 `503be3b917993ce3d22d5ca8f5bb8bc878eee0b8048582e52c9dd6b13c1a483e`;
- package source `f4c8c993be80eaf54468f5b2630fd107050a1385`;
- version `0.9.3`;
- payload count `178`;
- payload fingerprint `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`;
- packaged installer retains `openclaw plugins install $packagePath --force`, `rollover-prepare`, and `rollover-finalize`;
- packaged ownership source contains `interruptedRolloverReentry` plus Task-110 retired-tree/fingerprint checks;
- recovery harness Git blob remains `80da4a2a23f5b5e936d725dcbd695a631bad1cb6`.

These CI/package facts are accepted as reproducibility evidence. They do not override the source defect below.

## What Task 111 got right

The valid missing-retired-generation path is narrow in several important ways:

- exact normal manifest metadata is parsed with plugin artifact existence temporarily excluded;
- controller must be `passthrough`;
- the manifest-owned retired plugin path must be specifically missing;
- required non-plugin paths must exist;
- mixed legacy namespace is rejected;
- active registration must be unique, contained by OpenClaw state, and exact id/package/version/payload;
- active replacement fingerprint must equal the installer candidate fingerprint;
- exactly one canonical payload candidate must remain;
- the classification returns `upgrade + pluginAlreadyExact=True + pendingRollover=False`;
- the existing action resolver therefore skips a second external plugin install;
- the normal installer later resolves exactly one plugin, creates a new ownership manifest, verifies it, and only then proceeds toward MANAGED enable.

This is the correct overall shape for Task-107-style re-entry.

## Residual source defect — active npm wrapper ownership is not proven

Task 111 explicitly required the re-entry shortcut to reject:

- `foreign/shared wrapper evidence`;
- unrelated user-owned state;
- any state accepted merely because a product payload/name is present.

The production source already contains the strict wrapper proof used by normal rollover paths:

- `_npm_project_for_plugin(...)` proves the plugin is inside the exact managed npm project layout;
- `_managed_wrapper_proof(...)` verifies the wrapper project name, package fields, dependency set, managed peer/override declarations, lockfile binding, and rejects undeclared/foreign dependencies.

However `_classify_interrupted_rollover_reentry(...)` does not call either proof for an active replacement that resides under `npm/projects/.../node_modules/<PLUGIN_PACKAGE>`.

Instead it accepts the active replacement using only:

1. `_active_registered_plugin(...)` — exact registration + exact child payload + OpenClaw containment;
2. `plugin_candidate_roots(...)` + `_plugin_payload(...)` — exact child payload candidate counting.

`plugin_candidate_roots(...)` enumerates npm-project child plugin paths without proving the owning wrapper. Therefore an exact child CogentNexus payload can reside inside a wrapper whose `package.json` also contains unrelated user dependencies or foreign fields and still satisfy the new shortcut.

That violates Task 111's explicit no-shared-wrapper/no-generic-adoption invariant.

### Required semantic RED

A new RED must construct the Task-107-shaped missing-retired-path state while placing the one exact active replacement inside an npm wrapper that contains unrelated/foreign ownership evidence. The current Task-111 candidate should incorrectly return `interruptedRolloverReentry=True`; the repaired source must reject it before mutation.

Do not solve by banning direct `extensions/cogentnexus-openclaw` replacements: Task 107's real replacement was installed through OpenClaw's supported plugin path and a direct canonical extension can be legitimate. The wrapper proof is required only when the active root is under the npm-project boundary.

## Negative-contract coverage is incomplete

Task 111 required focused recovery-path tests for at least:

- fingerprint mismatch;
- multiple canonical payloads / non-unique registration;
- replacement outside OpenClaw boundary;
- wrong package/id/version;
- controller not passthrough;
- corrupt/mismatched manifest metadata;
- missing skill or launcher/non-plugin artifact;
- altered/incomplete retired path rather than specifically missing;
- mixed legacy/new namespace;
- foreign/shared wrapper evidence.

The Task-111 RED commit added only three direct re-entry tests: positive exact replacement, fingerprint mismatch, and altered-retired-path behavior. Existing generic rollover tests are useful background, but they do not prove every branch of the new early-return shortcut. In particular, there is no semantic re-entry regression for foreign/shared wrappers, which is exactly where the residual source defect exists.

The next task must add a focused negative re-entry matrix. It may reuse fixtures/helpers, but assertions must call the actual `classify_install(...)` shortcut surface.

## Pending-rollover observation

The altered-retired-path test was changed in the production commit from expecting a `RuntimeError` to expecting `pendingRollover=True` with no re-entry flag. This does prove that the new shortcut itself is not used for that state.

Do not broaden the next repair into unrelated pending-rollover redesign unless a new semantic regression demonstrates a real unsafe success path. The live blocker for Task 107 is the missing-retired-path shortcut ownership proof described above.

## Live authorization decision

No real-Windows mutation is authorized from candidate `f4c8c993be80eaf54468f5b2630fd107050a1385` or artifact `9683680142`.

Task 107 remains the last authoritative live machine boundary. No Dashboard semantic Send is authorized.

A new source-only TDD repair is required before lifecycle acceptance.
