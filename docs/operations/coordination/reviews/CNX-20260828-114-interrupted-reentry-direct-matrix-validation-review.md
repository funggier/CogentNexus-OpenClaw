# CNX-20260828-114 — Independent Review

## Verdict

`SOURCE BEHAVIOR ACCEPTED; LIVE GATE BLOCKED — MATRIX FIDELITY / SEMANTIC ASSERTION DEFECTS`

Task 114 correctly remained tests-only and did not alter production source. Its exact candidate `83e8452de116bf6204be884e4cddf9f3b92b90da` passed all three required workflows and produced a reproducible package-proof artifact. However, the committed Task-114 matrix does not faithfully exercise every boundary required by the Task-114 contract, so it is not yet sufficient durable regression evidence for live authorization.

## Accepted evidence

- starting coordination HEAD: `a21f58b2cc5c0ae774ef9d2310409c5b221fff62`;
- tests-only candidate: `83e8452de116bf6204be884e4cddf9f3b92b90da`;
- candidate changed only `tests/test_plugin_generation_rollover.py` (+37 lines);
- no production source changed from accepted Task-113 repair semantics `d8c5f5f5e7936e673a6731f5a8a0f17e7bd39a06`;
- report-only descendant: `39bd1ed4fb9a12d291323a4c395d07888e873e0b`;
- candidate -> report differs only by the Task-114 report;
- Validate `33173131342`: completed/success on exact candidate;
- Windows Installer Pack Smoke `33173131369`: completed/success on exact candidate;
- PS5.1 Acceptance Smoke `33173131410`: completed/success on exact candidate;
- artifact `9686448746` bound to exact candidate;
- independently verified outer SHA256 `8706b146b021832c8b167c82dd27f145ad52c2735980f6f0eb39f03d379ce053`;
- independently verified inner ZIP SHA256 `dfcff2d27a1fe0bcac7417f609afa3e5e3254588f0ce1fe22d274c1410ab6349`;
- independently verified tar.gz SHA256 `9746eb6f9b61f9dd99b7e6e1eb9d2ecad2f49619f7cdacff964bd51257617ceb`;
- `PACKAGE_IDENTITY.json` binds source `83e8452de116bf6204be884e4cddf9f3b92b90da`, version `0.9.3`, payload count `178`, fingerprint `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`;
- Task-113 conflict rejection, Task-112 wrapper proof, Task-110 retired-tree exactness, and local archive install boundary remain packaged.

## Confirmed matrix-fidelity defects

### 1. `mixed_namespace` does not create legacy namespace residue

The Task-114 case named `mixed_namespace` appends another plugin-inventory registration using the current `PRODUCT_ID`. It does not create any of the legacy evidence that production `current_inventory(...)` actually recognizes:

- `<workspace>/cnx.cmd`;
- `<workspace>/cnx`;
- `<workspace>/skills/cogentnexus`;
- `<workspace>/.cogent`;
- `<openclaw-state>/extensions/cogentnexus-rotation`.

The test may therefore pass because of active-registration ambiguity rather than because `inventory["legacy"]` blocks re-entry. It does not prove the requested mixed legacy/new namespace boundary.

Independent reviewer reproduction against the exact packaged candidate created real legacy residues (`cnx.cmd`, `.cogent`, and `extensions/cogentnexus-rotation`). All three were rejected by the production source with `interrupted rollover re-entry rejects mixed legacy state`. This confirms source behavior is currently correct; the defect is durable test fidelity.

### 2. Out-of-bound / noncanonical fixtures do not contain exact active payloads

The `outside_state` and `noncanonical_root` cases only rewrite the registration `rootDir` to paths where no exact payload was created. They can therefore fail because the payload is missing rather than proving that an otherwise exact active payload is rejected specifically because its storage boundary is outside OpenClaw or noncanonical.

The corrected matrix must copy an exact candidate payload to those locations, remove the normal active candidate where needed, bind the registration to the copied payload, and then assert the intended containment/canonical-storage rejection.

### 3. Negative cases do not assert semantic failure reasons

Task 114 required each rejection case to assert a semantic `RuntimeError` relevant to the violated boundary. The matrix currently catches any `RuntimeError` and treats it as success for nearly every negative case. This allows a fixture to pass for the wrong reason.

### 4. Classification non-mutation is not asserted

Task 114 required rejection cases to assert that classification does not mutate the fixture beyond setup. The matrix does not snapshot/compare the manifest, controller, product/legacy inventory, or sentinel data across the `classify_install(...)` call.

### 5. Positive result contract is not fully committed in Task 114

The Task-114 matrix commit does not add explicit positive direct and managed assertions for all required fields and paths. Independent reviewer execution against the exact packaged candidate confirmed that both shapes currently return:

- `mode == "upgrade"`;
- `pendingRollover is False`;
- `pluginAlreadyExact is True`;
- `interruptedRolloverReentry is True`;
- exact `replacementPluginPath`;
- exact missing retired `manifestPluginPath`.

Again, source behavior is correct; repository regression evidence is incomplete.

## Why live authorization remains blocked

The purpose of Task 114 was durable, direct regression coverage of the early-return surface, not merely one-time reviewer confidence. A generic `RuntimeError` matrix with several fixtures that can fail for a different cause does not provide that durable guarantee.

The production source repair from Task 113 is preserved. No retroactive RED should be manufactured and no production rewrite is justified by this review.

## Required next gate

Open a tests-only semantic matrix hardening task. Correct the fixtures and assertions first. If the corrected semantic matrix is GREEN on current production, production must remain unchanged. If a corrected test produces a genuine behavioral RED, preserve that test-only commit as valid RED evidence and only then make a minimal production repair.

No real-Windows lifecycle or Dashboard semantic send is authorized by this review.
