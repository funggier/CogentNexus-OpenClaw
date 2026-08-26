# CNX-20260827-084 — Repair Same-Version Rollover Attestation and Pending Recovery

Status: `READY_FOR_HERMES`

Execution mode: `SOURCE_TDD_ATTESTED_ROLLOVER_AND_PENDING_RECOVERY`

Current authorization: `ATTESTED_ROLLOVER_SOURCE_REPAIR_AUTHORIZED`

Owner: ChatGPT

Executor: Hermes/Codex after operator continuation

## Goal

Repair the ownership-safe plugin upgrade contract so a deliberately changed `cogentnexus-openclaw@0.9.3` payload can replace the manifest-owned older `0.9.3` payload **only when the replacement is attested to the exact installer source candidate**, and so the current Task-083 two-generation partial state can later be recovered without manual deletion, manifest edits, or an unnecessary third semantic plugin generation.

This task is source/test only. It must not repair the live product.

The intended invariant is:

`manifest-owned prior payload + exact candidate-source attestation + OpenClaw active replacement`

`-> reviewed rollover plan -> atomic retirement of prior project -> ownership binds exact attested replacement`

while:

`unattested / wrong-fingerprint / foreign / extra candidate`

`-> fail closed with zero retirement/adoption`.

## Accepted predecessor evidence

Task 083 report:

`docs/operations/coordination/reports/CNX-20260827-083-recover-partial-install-and-live-parity.md`

Task 083 report HEAD:

`1b5238bc3d7e8611e5fe305a969fad45735b142a`

Independent review:

Decision: `ACCEPT`

Disposition:

`ACCEPT_BLOCKER_SAME_VERSION_ROLLOVER_ATTESTATION_GAP`

Review path:

`docs/operations/coordination/reviews/CNX-20260827-083-recover-partial-install-and-live-parity.md`

Last accepted source before this repair:

`df412ed10522d79a722e1b48d681e7553cb79ae2`

Preserve all accepted Task-078/079/080 semantic/delivery behavior and Task-082 npm-pack repair.

## Accepted current live partial state — READ ONLY IN TASK 084

Task 083 invoked exactly one supported installer and stopped at the ownership rollover failure.

Accepted post-failure facts:

- OpenClaw `2026.7.1-2`;
- controller `passthrough`, generation 13;
- startup disabled;
- Supervisor Scheduled Task absent;
- AGENTS managed block absent;
- ownership manifest still identifies the prior plugin generation;
- prior generation: `g-5593cbcfff5b35d5`;
- newly installed generation: `g-7257c4555ca8ad21`;
- both identify `cogentnexus-openclaw@0.9.3`;
- the two plugin payload fingerprints differ;
- OpenClaw registers the newer generation disabled;
- Gateway remains healthy / dashboard HTTP `200`;
- Ollama remains healthy with the accepted four-model inventory;
- SQLite integrity `ok`, Tickets `0`, outbox `0`;
- no semantic/provider run was created.

Do not normalize this state during Task 084.

---

# Critical candidate-preservation fence

Task 084 must **not change the runtime/plugin package payload** under:

`plugins/cogentnexus-openclaw/**`

The Task-083 newly installed generation must remain fingerprint-equivalent to the accepted source plugin payload from `df412ed...` so the later recovery task can attest and reuse it.

Production edits are limited to the ownership/installer control plane unless an independently reproduced blocker proves otherwise:

- `skills/cogentnexus-openclaw/scripts/namespace_ownership.py`;
- `scripts/install.ps1`;
- focused tests under `tests/`.

Do not bump package/plugin version in Task 084.

Do not edit plugin `dist`, plugin package metadata, plugin TypeScript, plugin scripts, or plugin tests.

If a required fix would change the plugin payload fingerprint, stop and report a blocker rather than invalidating the recoverable Task-083 replacement generation.

---

# Absolute live fence

Task 084 is source/test only.

Do NOT:

- run the live installer/install-over;
- uninstall/reset/clean-reinstall;
- delete/rename either live plugin generation;
- enable/disable the live plugin/controller/startup manually;
- create/replace/delete the Supervisor task;
- edit live AGENTS;
- edit live ownership manifest/config/runtime/launcher;
- mutate live SQLite/Ticket/session state;
- send any Dashboard/WebChat or CLI semantic/user message;
- call Ollama directly;
- change provider/model/timeouts;
- restart Gateway/Ollama/Supervisor for testing;
- reboot;
- merge/tag/release.

Read-only inspection of the current two-generation state is allowed and encouraged for evidence.

Use a fresh isolated worktree from the exact coordination execution HEAD.

---

# Phase A — execution fence and root-cause reproduction

1. Fetch the coordination branch and record the exact execution HEAD.
2. Verify Task-083 report and independent ACCEPT-blocker review are ancestors.
3. Create a fresh isolated worktree/branch.
4. Record worktree path, branch and clean `git status --short`.
5. Re-read completely:
   - `skills/cogentnexus-openclaw/scripts/namespace_ownership.py` rollover functions;
   - `scripts/install.ps1` classification/plugin-install/rollover ordering;
   - `tests/test_plugin_generation_rollover.py`;
   - `tests/test_namespace_ownership.py`;
   - installer mode/recovery tests.
6. Re-prove the current live Task-083 state read-only only. Record the exact old/new live fingerprints and compare the newer generation fingerprint to the source plugin fingerprint at `df412ed...`.
7. Do not edit production before focused RED evidence.

## A1 — exact source fingerprint proof

Use the production `_plugin_payload()` semantics or a new CLI wrapper around those same semantics to compute the source plugin fingerprint from the isolated candidate `plugins/cogentnexus-openclaw` directory.

Required evidence:

- source plugin package/version exact `0.9.3`;
- source fingerprint is a 64-hex SHA-256 fingerprint under the existing four-file payload contract;
- live `g-7257...` replacement fingerprint equals this source fingerprint;
- live `g-5593...` manifest-owned prior fingerprint differs.

If the Task-083 newer generation does **not** equal the accepted source plugin fingerprint, stop and report `BLOCKED_LIVE_REPLACEMENT_NOT_SOURCE_EXACT`; do not design an adoption path around it.

---

# Gate R — RED reproduce same-version changed-payload policy gap

Extend `tests/test_plugin_generation_rollover.py` using the real production helpers.

## R1 — changed payload without attestation remains rejected

Preserve the existing security contract:

1. create manifest-owned old `0.9.3` generation with marker `old`;
2. create active replacement `0.9.3` generation with marker `new`;
3. no expected candidate fingerprint is supplied;
4. `build_plugin_rollover_plan()` must reject before any retirement.

This should already be GREEN on predecessor source and remains a permanent negative test.

## R2 — source-attested changed payload is RED on predecessor

Add a new test:

1. same old/new layout with different fingerprints;
2. compute expected replacement fingerprint from the intended new/source payload independently through the production fingerprint primitive;
3. call the proposed attested rollover-plan interface with that expected fingerprint;
4. predecessor source must fail with the current `replacement payload conflicts...` behavior or missing attestation interface.

Verify the failure is specifically because the source cannot authorize a legitimate same-version changed payload yet.

## R3 — wrong attestation must fail

Add a test where expected fingerprint does not equal the active replacement fingerprint.

Required final behavior: fail closed with old project, new project and manifest unchanged.

---

# Gate A — explicit source-attestation contract

Implement the smallest explicit contract; do not simply remove fingerprint equality.

## A1 — production source fingerprint interface

Expose one production CLI/API surface in `namespace_ownership.py`, for example:

`plugin-fingerprint --plugin-root <path> --version 0.9.3`

It must:

- reuse `_plugin_payload()` rather than a separate hash algorithm;
- require exact plugin id/package/version/files;
- return normalized root/version/fingerprint JSON;
- fail nonzero if the source payload is incomplete or wrong-version.

The installer must derive expected replacement authority from this **source candidate**, never from the live replacement candidate alone.

## A2 — rollover plan attestation

Extend the rollover-plan contract with an explicit field such as:

`expectedReplacementFingerprint`

and, if useful for auditability:

`replacementAuthorization = "candidate-source-fingerprint"`.

Requirements:

- plan construction requires a valid 64-hex expected fingerprint for a changed same-version replacement;
- replacement fingerprint must equal the expected source fingerprint exactly;
- if replacement fingerprint equals retired fingerprint, existing equivalent-generation behavior remains valid;
- if fingerprints differ and no expected fingerprint is supplied, reject;
- if fingerprints differ and expected fingerprint mismatches replacement, reject;
- never infer expected authority from `openclaw plugins list` alone;
- plan includes the expected fingerprint so review/apply bind the authorization evidence.

## A3 — apply re-proof

`rollover-apply` must re-prove immediately before retirement:

- manifest-before hash;
- controller PASSTHROUGH;
- exact manifest-owned retired path/fingerprint;
- exact OpenClaw active replacement path/registration;
- expected replacement fingerprint from the reviewed plan;
- actual replacement fingerprint equals that expected fingerprint;
- wrapper proofs;
- inventory hash;
- active registration hash;
- retired/replacement project tree hashes;
- plan SHA.

Any drift fails before retirement.

Do not reduce the current atomic rename + rollback behavior.

---

# Gate P — bounded pending-rollover classification/recovery

Task 083 now leaves two exact candidates. Generic ownership resolution must remain strict, but the installer requires a narrowly attested path through this specific recoverable state.

## P1 — generic resolution remains strict

Keep these invariants:

- `resolve_installed_plugin()` with two candidates remains ambiguous/failing;
- ordinary manifest verification that requires unique plugin resolution remains strict;
- no generic API silently chooses the active candidate merely because OpenClaw registered it.

Add/retain tests proving this.

## P2 — explicit attested upgrade classification

Extend the installer-facing classification contract only through explicit parameters, for example:

- `--plugin-inventory-json <path>`;
- `--expected-replacement-fingerprint <sha256>`.

Without these attestation inputs, existing `classify-install` behavior must remain fail-closed for ambiguous two-candidate state.

With explicit attestation inputs, the exact Task-083 topology may return:

```json
{
  "mode": "upgrade",
  "pendingRollover": true,
  "pluginAlreadyExact": false,
  "manifestPluginPath": "...old...",
  "replacementPluginPath": "...new...",
  "expectedReplacementFingerprint": "..."
}
```

only if all are true:

1. ownership manifest structure/path boundaries verify with `verify_plugin=False`;
2. controller is PASSTHROUGH;
3. exactly two canonical product candidates exist;
4. one candidate is exactly manifest-owned;
5. OpenClaw inventory has exactly one canonical product registration;
6. registration points exactly at the other candidate;
7. active candidate package/version/wrapper proofs are exact;
8. active candidate fingerprint equals the expected source fingerprint;
9. unrelated projects do not participate.

Three candidates, two unregistered candidates, wrong active root, wrong fingerprint, wrong version, foreign wrapper or missing manifest all fail closed.

## P3 — already-exact single-generation classification

Add an attested classification result for the idempotent case where:

- exactly one candidate exists;
- it is manifest-owned;
- its fingerprint already equals the expected source fingerprint.

Return:

`pluginAlreadyExact = true`

so an installer recovering from a later-stage failure need not create a redundant generation.

If exactly one manifest-owned candidate exists but fingerprint differs from expected source, return normal upgrade with `pluginAlreadyExact = false`.

---

# Gate I — installer orchestration and idempotent recovery

Update `scripts/install.ps1` only after RED tests establish the required behavior.

## I1 — derive source attestation before classification

Before live classification/mutation, installer must:

1. call the production `plugin-fingerprint` interface against `$pluginDir`;
2. record `$expectedPluginFingerprint`;
3. capture read-only `openclaw plugins list --json` inventory into a bounded temporary/evidence file as required;
4. pass both inventory and expected source fingerprint to the explicit installer-facing classification command.

This is read-only and must occur before the first live mutation.

The existing fresh/legacy classification behavior must remain unchanged when there is no owned upgrade.

## I2 — recover pending rollover before installing a third generation

If classification returns `pendingRollover = true`:

1. do not call `openclaw plugins install` yet;
2. enter/confirm PASSTHROUGH through the existing lifecycle boundary;
3. use the attested `rollover-plan` / `rollover-apply` path to retire the manifest-owned old generation and bind ownership to the already-installed source-exact replacement;
4. re-prove unique plugin resolution and manifest verification;
5. set installer state so the plugin is now considered `pluginAlreadyExact`;
6. **skip npm pack/plugin install/second rollover** for this invocation;
7. continue normal owned-runtime/launcher/ownership/AGENTS/MANAGED restoration.

This is the intended Task-083 recovery path.

## I3 — already-exact upgrade skips redundant plugin creation

If classification returns `pluginAlreadyExact = true` with no pending rollover:

- skip `npm pack` / `openclaw plugins install` / generation rollover;
- preserve existing canonical generation;
- continue the remainder of supported install-over normally.

This makes install-over idempotent after a prior attempt that already installed/committed the exact plugin but failed later.

## I4 — normal changed-payload upgrade

For the ordinary single-old-generation case where the manifest-owned fingerprint differs from expected source:

1. perform the existing npm-pack artifact resolver/install flow;
2. disable the newly installed replacement while PASSTHROUGH;
3. call `rollover-plan` with the expected source fingerprint;
4. require the newly active replacement to match that attestation;
5. apply rollover;
6. continue normal ownership/MANAGED restoration.

A replacement installed by OpenClaw that does not match the source fingerprint must fail before prior-generation retirement.

---

# Gate S — security/negative matrix

Add deterministic tests proving all of these remain fail closed:

1. changed same-version replacement with no source attestation;
2. wrong expected fingerprint;
3. expected fingerprint copied from the live replacement rather than supplied through the installer source contract is not an implicit authority path;
4. active registration points at manifest-owned old generation;
5. active registration points outside OpenClaw state;
6. three candidate generations;
7. foreign/shared wrapper;
8. wrong plugin/package/version;
9. non-PASSTHROUGH controller during pending rollover;
10. inventory changes between plan and apply;
11. manifest changes between plan and apply;
12. replacement payload/tree changes between plan and apply;
13. unrelated npm project remains byte-identical;
14. atomic retirement failure leaves old/new/manifest unchanged;
15. final verification failure restores old project + prior manifest exactly.

Do not weaken existing Task-054/055/057 rollover tests to make new behavior pass.

---

# Gate C — current Task-083 residue fixture

Add a production-facing deterministic fixture matching the current live topology:

- manifest -> old generation with fingerprint A;
- OpenClaw registration -> new disabled generation with fingerprint B;
- A != B;
- expected source fingerprint = B;
- controller PASSTHROUGH;
- exactly two valid managed npm wrappers;
- no Supervisor/AGENTS requirements are needed for this source-only unit.

Required flow:

1. generic resolver fails ambiguous;
2. ordinary/unattested classification fails;
3. attested installer classification returns `upgrade + pendingRollover`;
4. attested rollover plan/apply succeeds;
5. old project moves into the exact backup boundary;
6. manifest binds the new generation;
7. unique resolver now returns the new generation;
8. source fingerprint equals installed generation fingerprint;
9. no third generation is created by the recovery orchestration harness.

Use deterministic temp fixtures only; do not touch the live npm project area.

---

# Full verification

After GREEN, run:

1. focused `test_plugin_generation_rollover.py` including new attestation tests;
2. focused namespace ownership/classification tests;
3. installer wiring/mode/recovery tests including Task-083 residue fixture;
4. Task-082 npm-pack boundary tests;
5. Task-069–074 fresh/upgrade/legacy transaction/recovery suites;
6. Task-078/079/080 semantic/delivery regression suites;
7. Node 24/npm 11 clean plugin `npm ci`, full `npm test`, `npm run plugin:validate`;
8. Node 22/npm 12 accepted compatibility path clean `npm ci`, full `npm test`, `npm run plugin:validate`;
9. full Python `pytest tests/ -q` with zero failures;
10. `python scripts/check_baseline_consistency.py`;
11. PowerShell 5.1 syntax parse for `scripts/install.ps1`;
12. `git diff --check`;
13. final diff review proving **no files under `plugins/cogentnexus-openclaw/**` changed**;
14. final implementation worktree clean after implementation commit(s).

## Required RED/GREEN evidence

The report must explicitly record:

- predecessor RED for source-attested changed-payload rollover;
- predecessor RED for Task-083 pending-rollover classification/recovery;
- GREEN results after source repair;
- confirmation that unattested changed payload remains rejected.

---

# Read-only live preservation proof

Before report publication, re-read the live state only and prove Task 084 did not mutate it:

- controller remains PASSTHROUGH;
- startup remains disabled;
- Supervisor remains absent;
- AGENTS markers remain absent;
- both Task-083 plugin generations remain present;
- OpenClaw registration remains on the newer disabled generation;
- ownership manifest remains unchanged;
- Gateway/Ollama/SQLite health remains as observed;
- Tickets/outbox remain zero.

Record live old/new fingerprints and source fingerprint but perform no rollover.

---

# Publication fence

1. Commit source/tests first.
2. Record exact implementation HEAD(s).
3. Verify execution HEAD -> implementation HEAD contains only justified Task-084 control-plane source/tests and **zero plugin-package payload changes**.
4. Publish report separately at:

`docs/operations/coordination/reports/CNX-20260827-084-repair-same-version-rollover-attestation-and-pending-recovery.md`

The report must include:

- execution/implementation/report HEADs;
- Task-083 root-cause reproduction;
- exact old/new/source fingerprint evidence;
- attestation API/schema;
- ordinary changed-payload upgrade proof;
- pending-rollover recovery proof;
- already-exact idempotent upgrade proof;
- security negative matrix;
- full npm/Python/PowerShell/baseline results;
- explicit proof that plugin package payload files did not change;
- read-only live preservation evidence;
- publication fence.

## Result tokens

Use exactly one:

- `PASS_ATTESTED_SAME_VERSION_ROLLOVER_AND_PENDING_RECOVERY_REPAIRED`
- `BLOCKED_LIVE_REPLACEMENT_NOT_SOURCE_EXACT`
- `BLOCKED_SOURCE_ATTESTATION_CONTRACT`
- `BLOCKED_PENDING_ROLLOVER_CLASSIFICATION`
- `BLOCKED_PENDING_ROLLOVER_RECOVERY`
- `BLOCKED_INSTALLER_IDEMPOTENCY`
- `BLOCKED_ROLLOVER_SECURITY_REGRESSION`
- `BLOCKED_PLUGIN_PAYLOAD_PRESERVATION`
- `BLOCKED_TEST_OR_VALIDATION_FAILURE`
- `BLOCKED_LIVE_PARTIAL_STATE_DRIFT`
- `BLOCKED_EVIDENCE_PUBLICATION_UNSAFE`

## Successor logic

Only after independent acceptance of:

`PASS_ATTESTED_SAME_VERSION_ROLLOVER_AND_PENDING_RECOVERY_REPAIRED`

may a new live recovery task mutate the current Task-083 partial installation.

That live successor must:

- use the exact accepted Task-084 source;
- re-prove the current two-generation partial state;
- prove the newer live generation equals the exact Task-084 source plugin fingerprint;
- use the supported installer exactly once;
- have the installer complete the attested pending rollover without manually deleting either generation and without creating a third semantic plugin generation;
- restore MANAGED/startup/Supervisor/AGENTS through supported installer behavior;
- prove source/live skill/plugin parity, ownership/runtime/Gateway/Ollama/SQLite health;
- observe at least five natural PT1M no-flash ticks;
- prove Dashboard/WebChat owner-surface readiness without sending a semantic prompt.

Only after that live recovery is independently accepted may the final semantic task send exactly one fresh authenticated Dashboard/WebChat owner message.