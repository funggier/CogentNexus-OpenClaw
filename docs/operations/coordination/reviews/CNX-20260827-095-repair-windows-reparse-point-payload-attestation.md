# Independent Review — CNX-20260827-095

Decision: `ACCEPT`

Disposition:

`ACCEPT_WINDOWS_REPARSE_POINT_PAYLOAD_ATTESTATION_REPAIRED`

Reviewed implementation:

`32212a4331e1f32b5a130bd30d271d4cbc56f6c1`

Reviewed report:

`1e66f8f563b9809cb823fdcd6ea69987a49861ad`

## Publication fence

Accepted.

- execution `4946bdc6365f5d73c1dd4f07db422205a8489d40` -> implementation `32212a4331e1f32b5a130bd30d271d4cbc56f6c1`: exactly one commit;
- implementation delta is limited to `skills/cogentnexus-openclaw/scripts/namespace_ownership.py` and `tests/test_namespace_ownership.py`;
- implementation -> report `1e66f8f563b9809cb823fdcd6ea69987a49861ad`: exactly one commit and exactly the Task-095 report file.

No plugin runtime payload file changed in Task 095.

## Independent source findings

The production correction is narrow and matches the approved defect boundary.

`_filesystem_metadata(path, relative)`:

- uses `Path.lstat()` before target classification;
- rejects symbolic links;
- on Windows reads `st_file_attributes` and rejects `FILE_ATTRIBUTE_REPARSE_POINT`;
- fails closed if required Windows reparse metadata is unavailable;
- returns the non-following metadata used for regular-file/directory classification.

The predicate is invoked for both declared package entries and recursively discovered children before `os.scandir()` descent or file-content inclusion. The v2 fingerprint domain separator, package authority, path framing, classifier and rollover semantics are unchanged.

## Real Windows RED/GREEN evidence

The report records a native Windows 10 junction created with `mklink /J`, independently confirmed as reparse tag `0xa0000003` / Mount Point. Python observed that path as `is_dir() == True` and `is_symlink() == False`.

Against the Task-094 predecessor, the real production fingerprint helper accepted/traversed it and the regression failed with `DID NOT RAISE RuntimeError`. After the Task-095 source change the same production regression passed. This directly proves the Windows junction class that Task 094 had not covered.

The regression places the junction below a declared `dist/` directory, so it exercises recursive-child discovery rather than only a top-level declaration. Independent source inspection confirms the same predicate is also called on each top-level declared entry.

## Preservation evidence

The fresh Task-095 report records:

- focused path/security GREEN;
- full Python suite `382 passed, 3 skipped, 4 subtests passed`;
- Python compile and baseline consistency;
- unchanged v2 candidate fingerprint `df2600da3ae78e1613793b4a7e5d1ebe61f66f71f0903e1d5d2cd5f0d5f4f4b4`;
- canonical payload count `176`;
- npm 11 and npm 12 packed/canonical sets exactly `176/176`, no missing/extra paths;
- Node 24/npm11 and Node22/npm12 clean plugin suites `49 files / 257 tests` plus validate/build/schema/bootstrap/package checks;
- Task-093 Dashboard verified-delivery/re-registration tests remain green;
- `git diff --check` passes;
- zero live mutation and zero semantic/provider activity.

No contradictory repository evidence was found.

## Acceptance

Task 095 closes the specific Windows reparse/junction attestation gap without changing the accepted Task-094 v2 fingerprint semantics.

This review releases exact source:

`32212a4331e1f32b5a130bd30d271d4cbc56f6c1`

for the next bounded live task only.

The next live task may perform exactly one supported install-over from that source, must prove the currently installed pre-Task093 plugin is classified non-exact under v2 and that the repaired package is actually installed and ownership-safe rolled over, then restore/prove MANAGED parity and health.

No semantic message is authorized by this acceptance.