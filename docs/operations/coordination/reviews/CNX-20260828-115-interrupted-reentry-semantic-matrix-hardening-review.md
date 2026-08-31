# CNX-20260828-115 — Independent Review

## Verdict

`ACCEPTED PASS — SEMANTIC MATRIX COMPLETE; EXACT CANDIDATE MAY ADVANCE TO A SEPARATE READ-ONLY-FIRST REAL-WINDOWS LIFECYCLE TASK`

## Reviewed candidate

`47b069daed90f54feae2c9eb26f38c438493f3c8`

Task-115 report-only descendant:

`fb1a395f223c8f955f5df4101b3353cebb7594b1`

Candidate -> report comparison contains exactly one added report file and no source/test drift.

## Test/source provenance

Task-115 began from coordination baseline `464bb97457054bef829e10f778b469b82e3a5e60`.

Implementation sequence:

1. `74e44e053ed0888e0b5e3ded113b30fd20f2365f` — tests-only semantic matrix, adding only `tests/test_interrupted_reentry_semantic_matrix.py`;
2. `47b069daed90f54feae2c9eb26f38c438493f3c8` — tests-only source-text correction for repository namespace isolation; runtime fixture semantics unchanged.

No production file changed in Task 115. The accepted Task-113 production repair remains intact.

## Semantic contract review

The Task-115 suite fixes the fidelity defects identified in Task 114:

- real production-recognized legacy residue is constructed and proven visible in `current_inventory(...)["legacy"]`;
- outside-state and contained-noncanonical cases use real exact product payloads before classification;
- negative cases assert boundary-specific error messages rather than any generic `RuntimeError`;
- classification rejection paths preserve pre-call filesystem/inventory/sentinel snapshots;
- direct and managed positive paths assert full mode/pending/pluginAlreadyExact/interrupted/path contracts;
- altered retired path proves the re-entry shortcut is not selected;
- unrelated npm projects do not become false product conflicts.

Independent execution of the corrected semantic suite returned `24 passed`. No corrected case exposed a production behavioral RED, so retaining production unchanged is correct.

## CI review

All required workflows are completed/success on exact candidate `47b069daed90f54feae2c9eb26f38c438493f3c8`:

- Validate `33175145162` — success;
- Windows Installer Pack Smoke `33175145179` — success;
- PS5.1 Acceptance Smoke `33175145178` — success.

The initial Task-115 candidate's Validate failure was independently traced to forbidden literal legacy namespace spellings inside test source at the namespace-isolation checker. The final tests-only commit changed only how those runtime legacy path strings are assembled; it did not weaken the checker or change production semantics.

Fresh Windows Validate evidence includes:

- Python full suite: `474 passed, 1 skipped, 4 subtests passed`;
- plugin tests: `268 passed` across `50` files;
- evaluation passed;
- production npm audit reported zero vulnerabilities;
- plugin package validation passed with packed file count 178.

## Package proof review

Artifact `9687249771` is bound to the exact reviewed candidate.

Independent verification:

- outer artifact SHA256 `c009450560176ce89c8a5a6ef65aec5ce9f821e75053617d56de212cf6093fdf`;
- inner ZIP SHA256 `8771869962babe591c6ba4431b8f4737b716f2258cfcfc6fd45eec4f582b2fc5`;
- tar.gz SHA256 `057cc016becd91ba4baf49a3c59152ce9ff467ff0a30b758e8e460e43f6ee2c5`;
- package source commit `47b069daed90f54feae2c9eb26f38c438493f3c8`;
- version `0.9.3`;
- payload count `178`;
- payload fingerprint `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`.

Packaged source preserves Task-113 conflict rejection, Task-112 wrapper proof, Task-110 retired-state exactness, the supported local archive install command, and recovery harness Git blob `80da4a2a23f5b5e936d725dcbd695a631bad1cb6`.

## Live authorization boundary

This review accepts Task 115 for repository/source/test/CI/package stabilization only. It does not assert the current state of the real Windows machine.

A separate lifecycle acceptance task may now be opened, but it must:

1. pin reviewed candidate `47b069daed90f54feae2c9eb26f38c438493f3c8` and artifact `9687249771`;
2. begin with a fresh read-only machine preflight;
3. stop `BLOCKED` before mutation if current live state is not safely attributable to the previously interrupted lifecycle or otherwise cannot be proven coherent;
4. perform any destructive lifecycle sequence once only, stopping on the first non-zero/ambiguous result;
5. preserve external OpenClaw/Ollama and existing provider/model configuration;
6. perform no Dashboard semantic Send.

The Dashboard durable-delivery semantic test remains a later, separate acceptance gate after lifecycle acceptance passes.
