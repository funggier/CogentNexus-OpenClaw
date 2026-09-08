# Independent Review — CNX-20260901-222 Static Payload Byte Guard and Candidate Requalification

Date: 2026-09-02 ICT  
Coordinator / final reviewer: ChatGPT

## Verdict

`ACCEPT_PASS_STATIC_BYTE_GUARD__CI_WINDOWS_PAYLOAD_IDENTITY_EQUAL__WINDOWS_INSTALLER_REQUALIFICATION_AUTHORIZED`

Task 222 is accepted as PASS for repository/package provenance. Exact candidate `a812f27815b3c87b7ca748dc2dea88f987601f70` is authorized for a separate bounded Windows install-over requalification task. This review does not authorize public Release/tag/asset mutation and does not alter immutable public `v0.9.3` at `26ce64a624255278a3a0266ad38746e0e6ed2e31`.

## Accepted RED → GREEN evidence

Test-only RED commit:

`31d8383d3340cda1e175045da7f554f102d44fc9`

The regression copied the real plugin package, changed `README.md` from LF to CRLF without semantic content change, then invoked the real `verify-package-contents.mjs` boundary. Pre-fix validation returned success and the test failed specifically because contaminated static package bytes were accepted. This is a genuine fail-open RED rather than a harness/import/dependency/path failure.

GREEN candidate:

`a812f27815b3c87b7ca748dc2dea88f987601f70`

The final candidate restores the four package-identity `.gitattributes` rules to `text eol=lf` and makes package validation fail closed before `npm pack` when any guarded static identity file contains a carriage-return byte or is not a regular file. The validator reads exact bytes and does not rewrite them. Generated `dist` canonicalization remains separate and generated-only; the byte-exact payload fingerprint algorithm is unchanged.

Guarded static identity paths:

```text
package.json
README.md
openclaw.plugin.json
scripts/bootstrap-ticket-db.mjs
```

## Repository and CI verification

Task-222 local validation passed the focused static-byte regression, Task-219 real LF/CRLF build regression, normal build, full tests, evaluation, plugin validation, and idempotent generated-`dist` canonicalization.

Independent GitHub verification confirms all required workflows ran on the exact candidate SHA and succeeded:

```text
Validate:                      33532084137  success
Windows Installer Pack Smoke: 33532084225  success
PS5.1 Acceptance Smoke:        33532084092  success
```

Validate package-proof artifact:

```text
artifact ID: 9810139538
artifact digest: sha256:3164b7770e7d8991691d7bbedced092866c208add72b0c03b4aa3d39d1b50ff0
sourceCommit: a812f27815b3c87b7ca748dc2dea88f987601f70
payloadFileCount: 192
payloadV2Fingerprint: e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386
tar.gz SHA-256: 88f1c81d5c68da11e7420388a215bf8b72c55a30e7924f24cf6a83b8912a7494
zip SHA-256: 011aaff51462c47440d973a348b938b12a3c2aadcbbe436acf5d54d9f2ad003d
```

Independent Validate job-log inspection confirms the same exact `sourceCommit`, 192-file count, payload fingerprint, archive identities, and artifact upload identity; acceptance does not rely only on artifact naming.

## Windows exact-first equality

Task 222 used a disposable `--no-checkout` Windows clone and selected `a812f278...` before first working-tree materialization. Under the inherited Windows Git policy (`core.autocrlf=true`), all four static identity paths materialized `i/lf w/lf attr/text eol=lf` and the tracked worktree was clean.

After `npm ci`, build, and plugin validation:

```text
Windows payload files: 192
CI payload files:      192
byte differences:      0
static differences:    0
generated differences: 0
Windows fingerprint:   e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386
CI fingerprint:        e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386
tracked status:         clean
```

This closes the package-determinism blocker that stopped Task 216.

## Runtime boundary

Task 222 performed no installer/install-over, lifecycle command, live plugin/config mutation, Gateway restart, SQLite/ownership/staging/transaction write, provider/model substitution, Discord traffic, Release/tag/asset mutation, or force push.

The next task may requalify installation only with this exact candidate and package identity. It must use:

1. exact-first source materialization; never materialize a newer branch worktree and then detach backward to the candidate;
2. the direct Windows Scheduled Task terminal topology qualified by Task 215; never the failed detached `Popen` topology from Tasks 212–213;
3. exactly one installer invocation, no retry;
4. zero Discord Sends until installer/provenance/runtime health is independently reviewed.

## Disposition

`ACCEPT_PASS_STATIC_BYTE_GUARD__CI_WINDOWS_PAYLOAD_IDENTITY_EQUAL__WINDOWS_INSTALLER_REQUALIFICATION_AUTHORIZED`
