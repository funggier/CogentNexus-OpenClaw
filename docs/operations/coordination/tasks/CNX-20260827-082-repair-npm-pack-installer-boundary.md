# CNX-20260827-082 — Repair npm Pack Installer Boundary

Status: `READY_FOR_HERMES`

Execution mode: `SOURCE_TDD_NPM_PACK_INSTALLER_BOUNDARY_REPAIR`

Current authorization: `NPM_PACK_INSTALLER_BOUNDARY_REPAIR_AUTHORIZED`

Owner: ChatGPT

Executor: Hermes/Codex after operator continuation

## Goal

Repair the supported Windows installer's `npm pack --json` artifact-resolution boundary so the accepted semantic candidate can later be restored onto the current partial PASSTHROUGH live installation through one supported install-over.

This task is source/test only. It must not repair the live product.

The invariant is:

`npm pack succeeds -> exactly one valid package artifact is resolved deterministically -> installer installs that exact artifact`

for both accepted npm 11 and npm 12 JSON shapes under Windows PowerShell 5.1.

## Accepted predecessor state

Task 081 report:

`docs/operations/coordination/reports/CNX-20260826-081-install-over-semantic-candidate-live-parity.md`

Task 081 report HEAD:

`ade320d2c32dde1143c2e8dc4ffbf8f3580e44a1`

Independent review:

Decision: `ACCEPT`

Disposition:

`ACCEPT_BLOCKER_SUPPORTED_INSTALL_OVER_NPM_PACK_PARSER`

Review path:

`docs/operations/coordination/reviews/CNX-20260826-081-install-over-semantic-candidate-live-parity.md`

Preserve the accepted Task-078/079/080 semantic production candidate lineage. The last accepted production candidate before this repair is:

`70d02e76233ca1084da445d488f88b628455f4aa`

## Accepted live partial state — DO NOT normalize in Task 082

Task 081's one supported install-over failed after the installer entered supported native handoff/PASSTHROUGH but before plugin rollover and final MANAGED publication.

Accepted post-failure live facts:

- Gateway healthy and dashboard HTTP `200`;
- Ollama healthy; accepted four-model inventory unchanged;
- product SQLite integrity `ok`, zero Tickets, zero outbox;
- installed skill tree already matches the Task-080 candidate where copied;
- ownership manifest still verifies;
- controller `passthrough`;
- startup policy disabled;
- Supervisor Scheduled Task absent;
- AGENTS managed block absent;
- previous canonical plugin generation remains registered but disabled;
- launcher remains present and references the previously owned runtime.

This is a bounded supported-installer partial state. Task 082 must not enable, restore, reinstall, clean up or otherwise mutate it.

## Absolute live fence

Do NOT in Task 082:

- run `scripts/install.ps1` against the live workspace;
- install/install-over/uninstall/reset/clean-reinstall;
- enable/disable controller/plugin/startup manually;
- create/replace Supervisor Scheduled Task;
- edit AGENTS;
- mutate live ownership manifest/runtime/launcher/config;
- mutate live Ticket/session/SQLite state;
- send any OpenClaw semantic/user message;
- use Dashboard/WebChat for a live turn;
- call `openclaw agent`, `chat.send`, `sessions_send` or equivalent semantic surface;
- call Ollama directly;
- change provider/model/timeouts;
- reboot, merge, tag or release.

Read-only inspection of the current partial live state/toolchain is allowed. Packaging/build/test artifacts must stay in a fresh isolated worktree/evidence directory.

---

# Phase A — execution fence and exact reproduction map

1. Fetch the coordination branch and record exact execution HEAD.
2. Verify Task-081 report and ACCEPT-blocker review are ancestors.
3. Create a fresh isolated worktree/branch from the execution HEAD.
4. Record clean `git status --short`.
5. Record read-only host/toolchain versions used for the reproduction:
   - Windows version;
   - `powershell.exe` / `$PSVersionTable.PSVersion`;
   - `node --version`;
   - default `npm --version`;
   - exact npm 11 and npm 12 compatibility toolchains used by existing project gates.
6. Read at minimum:
   - `scripts/install.ps1` around the `npm pack --json` boundary;
   - `plugins/cogentnexus-openclaw/scripts/verify-package-contents.mjs`;
   - plugin `package.json` / lockfile;
   - existing installer regression tests.
7. Re-prove the current live partial state read-only only as needed to ensure no other actor normalized it. Do not repair drift.

No production edit before RED evidence.

---

# Gate R — reproduce the actual pack-shape failure

## R1 — capture exact current-host output

In the isolated candidate/worktree plugin directory:

1. ensure dependencies/build prerequisites through normal source/test setup only;
2. run the same external boundary used by the installer:
   `npm pack --json`;
3. capture:
   - exact npm version;
   - raw stdout as text and, where practical, bytes/UTF-8 length;
   - stderr separately;
   - exit code;
   - parsed JSON top-level type;
   - top-level property/key names or array count;
   - exact location/name of generated `.tgz` artifact;
4. run the current production PowerShell parsing logic against that captured stdout and prove whether it reproduces the Task-081 failure.

If the default host no longer reproduces because toolchain resolution differs, use the exact supported npm 12 compatibility path and separately the npm 11 path. Do not guess the Task-081 runtime shape; report what each toolchain actually emits.

Delete worktree `.tgz` artifacts after evidence capture.

## R2 — explicit shape fixtures

Add focused parser tests for at least:

1. npm 11 array shape containing exactly one artifact object with `filename`;
2. npm >=12 single-entry object keyed by package name whose value contains `filename`;
3. a direct single artifact object with `filename` if the selected implementation intentionally supports it;
4. zero artifacts;
5. multiple package/object entries;
6. missing/empty filename;
7. invalid JSON;
8. unsafe filename/path traversal or path separator input if artifact name is accepted from JSON.

The pre-fix production boundary must fail at least the keyed npm-12 fixture or the exact reproduced current-host shape before production is edited.

---

# Gate P — one canonical normalization contract

Repair the smallest boundary that eliminates the PowerShell/npm shape ambiguity.

Preferred architecture: move npm-pack JSON normalization/artifact-name validation into one deterministic helper that can be executable-tested independently and used by `install.ps1`; reuse the same normalization semantics already recognized by `verify-package-contents.mjs` rather than maintaining contradictory assumptions.

Acceptable implementations include a small Node helper/module consumed by the installer, or an equivalently testable PowerShell helper. Do not add a broad packaging framework.

Required normalization semantics:

- accepted npm 11 array shape -> exactly one package item;
- accepted npm 12 keyed-object shape -> normalize `Object.values(...)` / equivalent and require exactly one package item;
- if direct-object compatibility is supported, it must be explicit and tested;
- artifact item must contain a non-empty string `filename`;
- filename must resolve as a package artifact inside the plugin working directory and must not escape through `..`, absolute path or unexpected path separators;
- zero/multiple/invalid results fail closed with a diagnostic including enough shape information to debug without leaking secrets;
- `npm pack` nonzero remains a hard installer failure;
- artifact existence is verified before `openclaw plugins install`;
- generated artifact remains cleaned in `finally` after install attempt.

Do not solve this by selecting the first arbitrary `*.tgz` already present in the directory; stale artifacts must not become install authority.

## P2 — PowerShell 5.1 production boundary proof

Execute a focused Windows PowerShell 5.1 harness that uses the same helper/path as production `install.ps1` and proves:

- npm 11 fixture resolves exactly one expected filename;
- npm 12 keyed fixture resolves exactly one expected filename;
- malformed/multiple/unsafe shapes fail nonzero/fail closed;
- actual `npm pack --json` output from the current isolated plugin resolves the exact artifact that was just created;
- no PowerShell array-enumeration quirk changes the result.

The proof must exercise the production parser/helper boundary, not only a reimplementation in the test.

---

# Gate I — installer wiring regression

Add/extend executable source tests proving `scripts/install.ps1`:

1. invokes the repaired normalization helper after a successful `npm pack --json`;
2. requires exactly one safe artifact name;
3. checks artifact existence;
4. passes exactly that package path to:
   `openclaw plugins install ("npm-pack:" + $packagePath) --force`;
5. preserves artifact cleanup;
6. does not regress upgrade/nonfresh/fresh transaction ordering;
7. does not start plugin rollover if packing/artifact resolution fails;
8. still leaves failure handling inside the existing installer-supported lifecycle boundary.

Where practical, run a production-facing dry installer harness against a completely isolated temporary workspace/stub OpenClaw surface. It must not touch the user's live workspace/config/tasks.

---

# Gate C — npm 11 / npm 12 compatibility

Under the already accepted compatibility toolchains, prove all of the following:

## npm 11 path

- clean `npm ci`;
- actual `npm pack --json` shape recorded;
- repaired artifact resolver accepts it;
- `npm run plugin:validate` passes;
- plugin full tests pass.

## npm 12 path

- clean `npm ci`;
- actual `npm pack --json` shape recorded;
- repaired artifact resolver accepts the npm-12 keyed-object shape actually produced or the exact supported fixture if the environment wrapper differs;
- `npm run plugin:validate` passes;
- plugin full tests pass.

Keep the existing `verify-package-contents.mjs` npm-shape normalization green. Prefer sharing normalization code if it reduces drift without expanding scope.

---

# Full verification

After GREEN:

1. focused npm-pack parser/resolver tests;
2. Windows PowerShell 5.1 production-boundary harness;
3. PowerShell syntax/parse check for `scripts/install.ps1` and any new `.ps1` helper;
4. Node 24 / npm 11 clean `npm ci`, full plugin tests and `plugin:validate`;
5. accepted npm 12 path clean `npm ci`, full plugin tests and `plugin:validate`;
6. full Python `pytest tests/ -q` with zero failures;
7. Task-069 through Task-074 targeted installer/recovery suites;
8. Task-078/079/080 semantic/delivery regression suites remain green;
9. `python scripts/check_baseline_consistency.py`;
10. `git diff --check`;
11. final diff review proving only justified packaging/installer source/tests changed;
12. implementation worktree clean after implementation commit(s).

No live install or semantic test is part of this verification.

---

# Publication fence

1. Commit source/tests first.
2. Record implementation HEAD.
3. Verify execution HEAD -> implementation HEAD contains only Task-082 justified source/tests.
4. Publish report separately at:

`docs/operations/coordination/reports/CNX-20260827-082-repair-npm-pack-installer-boundary.md`

The report must include:

- execution / implementation / report HEADs;
- exact Task-081 failure diagnosis;
- exact default-host, npm11 and npm12 raw pack shapes/version evidence;
- RED evidence;
- normalization/helper design;
- Windows PowerShell 5.1 GREEN evidence;
- actual artifact-path proof;
- npm 11/npm 12/full Python/baseline results;
- live partial-state read-only confirmation;
- live mutation accounting;
- publication fence.

## Result tokens

Use exactly one:

- `PASS_NPM_PACK_INSTALLER_BOUNDARY_REPAIRED`
- `BLOCKED_NPM_PACK_SHAPE_REPRODUCTION`
- `BLOCKED_PACK_ARTIFACT_SECURITY`
- `BLOCKED_INSTALLER_WIRING_REGRESSION`
- `BLOCKED_NPM11_COMPATIBILITY`
- `BLOCKED_NPM12_COMPATIBILITY`
- `BLOCKED_TEST_OR_VALIDATION_FAILURE`
- `BLOCKED_LIVE_PARTIAL_STATE_DRIFT`
- `BLOCKED_EVIDENCE_PUBLICATION_UNSAFE`

## Successor logic

If independent review accepts `PASS_NPM_PACK_INSTALLER_BOUNDARY_REPAIRED`, the next task is a live supported recovery/install-over from the exact accepted Task-082 implementation onto the current Task-081 partial PASSTHROUGH installation.

That successor must:

- start with read-only re-proof of the partial state;
- require ownership verification and `upgrade` classification;
- perform no manual cleanup/uninstall/reset;
- invoke exactly one supported normal install-over;
- prove source/live plugin+skill parity;
- restore MANAGED/startup/Supervisor/AGENTS through installer-supported behavior only;
- prove ownership/runtime/Gateway/Ollama/SQLite health;
- observe at least five natural PT1M ticks and re-prove no-flash;
- prepare/verify the Dashboard/WebChat owner surface without sending a semantic prompt.

Only after that live recovery task is independently accepted may a separate final semantic task authorize exactly one fresh Dashboard/WebChat owner message.
