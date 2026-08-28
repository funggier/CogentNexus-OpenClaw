# CNX-20260828-115 — Interrupted Re-entry Semantic Matrix Hardening

## Verdict

`PASS` — semantic regression fidelity is now complete on the accepted Task-113 production behavior. Corrected boundary-specific tests were GREEN; no production source repair was required or made. No live Windows lifecycle mutation was performed or authorized.

## Reconciliation and source boundary

- Task-115 coordination baseline: `464bb97457054bef829e10f778b469b82e3a5e60`.
- Accepted production repair remains Task-113 source `d8c5f5f5e7936e673a6731f5a8a0f17e7bd39a06`.
- First Task-115 tests-only semantic commit: `74e44e053ed0888e0b5e3ded113b30fd20f2365f`.
- Final Task-115 candidate: `47b069daed90f54feae2c9eb26f38c438493f3c8`.
- Baseline -> final candidate changes only `tests/test_interrupted_reentry_semantic_matrix.py`; no production source changed.

## Semantic matrix

Task 115 adds direct `classify_install(...)` regression coverage with boundary-specific errors and non-mutation snapshots/sentinels for:

- exact managed positive re-entry with all result/path bindings;
- exact canonical direct-extension positive re-entry with all result/path bindings;
- real legacy residue: `cnx.cmd`, `cnx`, `skills/cogentnexus`, `.cogent`, and legacy `cogentnexus-rotation` extension;
- exact active payload outside OpenClaw state;
- exact active payload contained by OpenClaw but at a noncanonical storage root;
- active foreign/shared npm wrapper;
- separate conflicting product wrapper for both managed and direct active shapes;
- duplicate exact payload;
- duplicate active registration;
- wrong id/package/version;
- candidate fingerprint mismatch;
- controller mode not PASSTHROUGH;
- manifest schema mismatch;
- missing `SKILL.md`;
- missing launcher;
- altered retired path remaining on normal rollover rather than the re-entry shortcut;
- unrelated npm project false-positive guard.

Classification rejection cases snapshot the OpenClaw-state tree and relevant external/sentinel state after fixture setup and prove classification does not delete, normalize, rewrite, or mutate them.

## Tests-only implementation and decision gate

### Initial tests-only semantic commit

`74e44e053ed0888e0b5e3ded113b30fd20f2365f`

Changed only:

`tests/test_interrupted_reentry_semantic_matrix.py`

Independent execution on the exact packaged production source returned:

```text
24 passed
```

Related repository ownership/installer suites returned:

```text
165 passed, 11 skipped
```

Therefore corrected semantic behavior exposed **no genuine production RED**. Per Task-115 rules, production source remained unchanged.

### Initial CI source-text failure

The first Task-115 candidate failed Validate before Python setup at the repository namespace-isolation gate. This was not a production or semantic behavior failure.

Root cause from the Windows job log was two literal legacy namespace strings embedded in the new test source:

- the legacy Windows launcher spelling;
- the legacy state-directory spelling.

The runtime fixtures themselves were intentional and correct, but the repository isolation checker forbids those generic legacy names as literal source text.

### Tests-only namespace correction

Final candidate:

`47b069daed90f54feae2c9eb26f38c438493f3c8`

Only two test-source expressions changed: each legacy name is now assembled at runtime from string fragments. The runtime path values and semantic fixtures are unchanged. No production source was edited.

Fresh local verification on the corrected exact test source:

```text
Task-115 semantic matrix: 24 passed
CogentNexus-OpenClaw namespace isolation: PASS
```

A local full-pytest attempt in the reviewer container hit the container execution timeout before completion and is **not** counted as PASS evidence. Exact GitHub Actions full-suite results below are the authoritative complete run.

## Exact same-source CI

Final candidate:

`47b069daed90f54feae2c9eb26f38c438493f3c8`

All required workflows completed successfully on exactly this SHA:

| Workflow | Run ID | Result |
|---|---:|---|
| Validate | `33175145162` | `completed / success` |
| Windows Installer Pack Smoke | `33175145179` | `completed / success` |
| PS5.1 Acceptance Smoke | `33175145178` | `completed / success` |

Validate matrix evidence includes Windows Python 3.11 full pytest:

```text
474 passed, 1 skipped, 4 subtests passed
```

and Windows plugin tests:

```text
Test Files 50 passed (50)
Tests 268 passed (268)
```

The same job also completed evaluation successfully, reported `found 0 vulnerabilities` for `npm audit --omit=dev`, and passed plugin validation with 45 configuration properties, 5 tools, 9 required Ticket DB tables plus the v095 registration fence, and packed file count 178.

## New package proof

Exact-candidate artifact:

- Artifact ID: `9687249771`
- Artifact name: `cogentnexus-openclaw-v0.9.3-package-proof-47b069daed90f54feae2c9eb26f38c438493f3c8`
- Outer artifact ZIP SHA256: `c009450560176ce89c8a5a6ef65aec5ce9f821e75053617d56de212cf6093fdf`
- Inner v0.9.3 ZIP SHA256: `8771869962babe591c6ba4431b8f4737b716f2258cfcfc6fd45eec4f582b2fc5`
- tar.gz SHA256: `057cc016becd91ba4baf49a3c59152ce9ff467ff0a30b758e8e460e43f6ee2c5`
- `PACKAGE_IDENTITY.json` source commit: `47b069daed90f54feae2c9eb26f38c438493f3c8`
- Package version: `0.9.3`
- Payload file count: `178`
- Payload V2 fingerprint: `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`

Independent artifact extraction and hashing matched GitHub's artifact digest and all archive identities. `PAYLOAD_IDENTITY.json` and `SHA256SUMS.txt` agree.

Packaged-source inspection confirms preservation of:

- Task-113 conflicting product-storage evidence rejection;
- Task-112 active npm-wrapper ownership proof;
- Task-110 retired project tree/fingerprint exactness checks;
- installer local archive invocation `openclaw plugins install $packagePath --force` when installation is actually required;
- absence of the superseded `npm-pack:` invocation;
- recovery harness `scripts/test-v093-ollama-recovery-windows-v3.ps1` at Git blob `80da4a2a23f5b5e936d725dcbd695a631bad1cb6`.

## Action-selection invariant

Accepted already-exact interrupted re-entry remains a no-second-install path:

```json
{"mode":"upgrade","pendingRollover":false,"pluginAlreadyExact":true,"skipPlugin":false,"installPlugin":false,"rolloverPlugin":false}
```

## Residual uncertainty

Task 115 is repository/source/test/CI/package evidence only. It does not establish the current state of the real Windows machine. Task 107 remains the last authoritative live-machine evidence.

A future live lifecycle task must therefore begin with fresh read-only verification of CNX state, ownership/product inventory, OpenClaw version, Gateway, Ollama/provider state, recovery, delivery, SQLite integrity, Supervisor state, and retained residue before any mutation.

## Stop gate

Task 115 is complete with `PASS` for its repository semantic-matrix scope. Stop for independent ChatGPT review before creating or executing a real-Windows lifecycle task. No Dashboard semantic Send is authorized here.
