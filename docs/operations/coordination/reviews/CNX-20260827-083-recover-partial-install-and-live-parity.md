# Review — CNX-20260827-083 Recover Partial Install and Live Parity

Decision: `ACCEPT`

Disposition: `ACCEPT_BLOCKER_SAME_VERSION_ROLLOVER_ATTESTATION_GAP`

Reviewed report:

`docs/operations/coordination/reports/CNX-20260827-083-recover-partial-install-and-live-parity.md`

Report HEAD:

`1b5238bc3d7e8611e5fe305a969fad45735b142a`

Execution coordination HEAD:

`58533e25bb23f00606bccf236193e5c2d1a17f86`

Exact recovery source used by Task 083:

`df412ed10522d79a722e1b48d681e7553cb79ae2`

## Publication fence

Independent comparison of execution HEAD to report HEAD proves:

- ahead by exactly one commit;
- the only changed path is `docs/operations/coordination/reports/CNX-20260827-083-recover-partial-install-and-live-parity.md`;
- no source/test/coordination mutation was mixed into the live-task publication.

The Task-083 report-only publication fence is accepted.

## Live execution disposition

The blocker is accepted as correctly reported.

Task 083:

- re-proved the expected Task-081/082 partial PASSTHROUGH state before mutation;
- proved `recovery-preflight = OWNERSHIP_PRESENT` and `classification = upgrade` before the authorized operation;
- used a clean detached checkout at exact source `df412ed10522d79a722e1b48d681e7553cb79ae2`;
- passed candidate npm/plugin validation and the repaired Task-082 npm-pack boundary;
- invoked exactly one supported normal recovery install-over;
- did not retry after nonzero exit;
- sent zero semantic/user/provider messages and created zero Tickets/outbox work;
- did not manually delete/normalize plugin generations or otherwise bypass installer ownership policy.

The repaired npm-pack boundary worked in the live installer: the exact packed artifact was resolved and installed successfully. The failure moved to the subsequent ownership-safe generation rollover boundary.

## Independently confirmed root cause

The accepted source in `skills/cogentnexus-openclaw/scripts/namespace_ownership.py` implements `_exact_rollover_state()` with this invariant:

`replacement fingerprint == manifest-owned retired fingerprint`

A different fingerprint raises:

`replacement payload conflicts with the manifest-owned same-version payload`

The existing `tests/test_plugin_generation_rollover.py` intentionally encodes the same rule in `test_plan_rejects_conflicting_same_version_replacement_payload`.

That rule was appropriate for the original v0.9.3 rollover problem, where a second same-version generation was expected to be byte/payload-equivalent to the already-owned generation. It is no longer sufficient for the current development/install-over workflow because Tasks 078–082 deliberately changed accepted source while retaining package version `0.9.3`.

Task 083 therefore produced the exact condition the current policy cannot represent safely:

- manifest-owned prior generation: `g-5593cbcfff5b35d5`;
- newly installed active/registered generation: `g-7257c4555ca8ad21`;
- both identify `cogentnexus-openclaw@0.9.3`;
- fingerprints differ because the replacement contains the accepted newer v0.9.3 source;
- the rollover correctly failed closed rather than retiring the manifest-owned generation without an authorization proof.

The failure is thus not a regression of the Task-082 npm-pack fix. It is a missing **same-version replacement attestation contract** in the ownership rollover design.

## Additional recovery consequence

Task 083 stopped after OpenClaw had already installed the replacement generation. The live state now contains two canonical v0.9.3 payload candidates with different fingerprints while the ownership manifest still identifies the prior generation and OpenClaw registers the newer generation disabled.

Generic `resolve_installed_plugin()` intentionally rejects two candidates, and normal `classify_install()` verifies the manifest through that unique-resolution contract. Therefore a successor must not assume another unmodified normal installer invocation can safely classify this state.

The next source repair must explicitly support a bounded **pending-rollover recovery** state. It must not weaken generic ownership resolution or silently adopt arbitrary duplicate generations.

## Required security invariant for the repair

Do **not** fix this by simply deleting the fingerprint-equality check or by allowing any same-version replacement.

A differing same-version replacement may be authorized only when all of the following are proven together:

1. controller is PASSTHROUGH;
2. the manifest-owned prior payload is exact and remains one candidate;
3. there are exactly two candidate payloads for the pending-rollover case;
4. OpenClaw has exactly one canonical registration for the replacement and it points at the non-manifest candidate;
5. the replacement package/version/wrapper boundaries are exact;
6. the replacement fingerprint equals an **expected source/plugin fingerprint derived from the exact installer candidate**, not merely a value discovered from the live replacement itself;
7. plan/apply still bind inventory hash, registration hash, project-tree hashes, manifest-before hash and reviewed plan hash;
8. apply re-proves the same attested replacement immediately before retirement;
9. unrelated npm projects remain outside mutation authority.

Without candidate-source attestation, a differing same-version replacement must continue to fail closed.

## Candidate preservation requirement

The Task-084 source repair should not change runtime/plugin package content under `plugins/cogentnexus-openclaw/**`. The already-installed Task-083 replacement generation must remain byte/fingerprint-equivalent to the accepted plugin candidate so a later supported recovery can attest and finish the pending rollover without installing a third semantic generation merely to pick up ownership-script changes.

Allowed production changes should be limited to the ownership/installer control plane, principally:

- `skills/cogentnexus-openclaw/scripts/namespace_ownership.py`;
- `scripts/install.ps1` only where needed for source-attestation and pending-rollover orchestration;
- focused tests under `tests/`.

## Live-state disposition

No MANAGED, source/live parity, no-flash or Dashboard-owner-surface acceptance is granted by Task 083.

Accepted current live facts are limited to:

- controller PASSTHROUGH generation 13;
- startup disabled;
- Supervisor absent;
- AGENTS managed block absent;
- two same-version plugin generations with different fingerprints, with the newer generation registered disabled;
- Gateway healthy / dashboard HTTP 200;
- Ollama healthy with the accepted four-model inventory;
- SQLite integrity `ok`, zero Tickets and zero outbox;
- zero semantic/provider activity from Task 083.

Do not manually delete either generation or edit the manifest to escape this state.

## Successor

Open a source/test-only Task 084 to:

- RED-reproduce the exact Task-083 same-version changed-payload conflict;
- add exact candidate-source fingerprint attestation to rollover planning/apply;
- add a fail-closed, attested pending-rollover classification/recovery path for the current two-generation state;
- make normal upgrade install-over idempotent when the already-installed canonical plugin is already source-exact;
- preserve strict rejection of unattested/foreign/multiple replacements;
- rerun complete ownership/install/recovery plus semantic/delivery regressions;
- leave the current live partial state read-only.

Only after independent acceptance of Task 084 may a new live recovery task mutate the current partial installation.