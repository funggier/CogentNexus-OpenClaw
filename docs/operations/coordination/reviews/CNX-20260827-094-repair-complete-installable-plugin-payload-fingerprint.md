# Review — CNX-20260827-094 Repair Complete Installable Plugin Payload Fingerprint

Decision: `REWORK`

Disposition: `REWORK_WINDOWS_REPARSE_POINT_INDIRECTION_NOT_REJECTED`

## Publication fence

Accepted.

- execution HEAD: `41ba7815dd87b7ebda1b0a4e89b97ff9325c9272`
- implementation: `3313930064123867ad760908a77b498f3bad029a`
- report: `0902c3c50fb1a46adfa9b8df86495fa521d01719`
- execution -> implementation is exactly one source/test commit.
- implementation -> report is exactly one report-only commit.

## Sound work preserved

The v2 design is materially stronger than the prior four-file sample and should be preserved:

- `package.json.files` is used as the package ownership contract;
- `package.json` is always included;
- declared directories are recursively expanded;
- normalized relative paths and exact bytes are framed into a versioned SHA-256 domain;
- absolute roots are excluded;
- shipped runtime changes under `dist/**` now affect the fingerprint;
- current npm11/npm12 packed-file-set evidence reports exact 176/176 equivalence;
- Task-093 candidate and currently installed pre-Task093 payload are distinguishable under v2;
- existing classifier/rollover semantics are reported green.

The Task-093 Dashboard staging repair remains preserved.

## Blocking finding

Task 094 explicitly required fail-closed rejection of `symlinks/reparse-style path indirection`.

The production implementation only tests `os.path.islink(path)` while recursively walking declared package paths. On Windows, a directory junction/reparse point is not guaranteed to be reported as a symbolic link. A junction under a declared directory such as `dist/**` can therefore be followed by `Path.is_dir()` / `os.scandir()` without triggering the current `islink` guard.

This violates the approved attestation boundary: the fingerprint must attest package-owned regular files, not silently traverse Windows filesystem indirection.

The current regression suite covers a symlink case but does not prove rejection of a real Windows junction/reparse-point case.

Because the deployment target is Windows and this is an ownership/security boundary, this is a release blocker rather than a cosmetic test gap.

## Required bounded correction

Preserve the v2 algorithm and make the smallest Windows-safe path-indirection correction.

Required behavior:

1. one production helper determines whether a path is filesystem indirection;
2. reject ordinary symlinks;
3. on Windows reject junctions and other reparse-point entries detectable from `lstat`/Windows file attributes before any file/directory traversal;
4. do not follow a reparse point merely because its target remains inside the plugin root;
5. apply the check to declared package entries and every recursively discovered child;
6. preserve normal regular-file/directory enumeration on non-Windows systems;
7. no change to the v2 digest framing/domain/package contract.

Mandatory RED on Windows:

- create a valid package fixture;
- create a directory junction/reparse point beneath a declared payload directory (prefer under `dist`);
- current implementation must demonstrate that the path is not rejected for the intended reason;
- after the fix, `plugin_fingerprint` must fail closed before traversing the junction target.

Also retain the existing symlink RED/GREEN coverage and add a safe platform-conditional skip only if the Windows fixture cannot create the junction in the test environment.

## Regression fence

Re-run the full Task-094 verification matrix, especially:

- v2 content/path/root-independence tests;
- symlink + Windows junction/reparse rejection;
- npm11/npm12 176-file equivalence;
- changed/exact/pending classifier truth table;
- Task-084/085/086 rollover plan/apply security and atomicity;
- Task-089 PowerShell action boundary;
- Task-093 Dashboard staging tests;
- full Python and both Node/npm plugin matrices.

No live install-over or semantic send is authorized by this review.

## Successor

A narrowly scoped source-only correction may be prepared after operator approval of the bounded reparse-point design. Only independent acceptance of that successor may release the one-shot live install-over.
