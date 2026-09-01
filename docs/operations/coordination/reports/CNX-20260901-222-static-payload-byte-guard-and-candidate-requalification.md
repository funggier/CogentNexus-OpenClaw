# CNX-20260901-222 — Static Payload Byte Guard and Candidate Requalification

Date: 2026-09-01 ICT  
Status: `PASS_STATIC_BYTE_GUARD__CI_WINDOWS_PAYLOAD_IDENTITY_EQUAL`  
Parent: `CNX-20260901-221`  
Repair parent: `CNX-20260831-198`  
Executor: Hermes / repository engineer + authenticated Windows verifier  
Coordinator / final reviewer: ChatGPT

## Scope and disposition

Task 222 was repository/package provenance only. It did not authorize installer execution, lifecycle mutation, live runtime changes, Gateway restart, SQLite writes, provider/model substitution, Release/tag/asset publication, force push, or Discord traffic.

Final disposition:

```text
PASS_STATIC_BYTE_GUARD__CI_WINDOWS_PAYLOAD_IDENTITY_EQUAL
```

This is not installer approval. Independent review is required before any later installer requalification.

## Fresh authority and candidate

Fresh remote authority was read from `agent/v0.9.3-full-stabilization` before execution. Task 222 was `READY_FOR_HERMES` with execution mode `TASK222_STATIC_PAYLOAD_BYTE_GUARD_AND_CANDIDATE_REQUALIFICATION`.

Final candidate:

```text
a812f27815b3c87b7ca748dc2dea88f987601f70
```

The candidate was pushed normally to the authoritative branch. Public `v0.9.3` remains immutable at:

```text
26ce64a624255278a3a0266ad38746e0e6ed2e31
```

Lineage and scope:

- generated-output repair lineage retained from `9af329b4de7c02fda35b467d84e76bb0f0bb0944`;
- Task 221 checkout-boundary evidence retained;
- unaccepted `b081d55c4ffa5fcb03931dc320d39bdcf92a6cf5` `-text` experiment was removed by forward restoration;
- Task-207 semantic repair base `27fe0181b3b65d555a3b0cc8354f6f7945c21c0b` was not rewritten.

Changed files in the final candidate:

```text
.gitattributes
plugins/cogentnexus-openclaw/scripts/verify-package-contents.mjs
plugins/cogentnexus-openclaw/scripts/v222-static-byte-guard.test.mjs
```

## Phase A — drift and preservation gate

The product/source/test/workflow tree had no unexpected drift newer than `b081d55…` before Task 222 changes. The live runtime was not mutated. Read-only preservation checks found the expected runtime SQLite file present; no installer/lifecycle/Gateway/Discord action was performed. The attempted process probe used `pgrep`, which is unavailable in this Git Bash environment; this was a tool limitation only and did not trigger any process action.

## Phase B — genuine RED

Test-only RED commit:

```text
31d8383d3340cda1e175045da7f554f102d44fc9
```

Test:

```text
plugins/cogentnexus-openclaw/scripts/v222-static-byte-guard.test.mjs
```

Exact command:

```text
node scripts/v222-static-byte-guard.test.mjs
```

The fixture copied the real plugin package, converted `README.md` from LF to CRLF without semantic changes, and invoked the real `scripts/verify-package-contents.mjs` validation boundary. Before the repair, validation returned success:

```text
{
  "result": "ok",
  "package": "openclaw-plugin-cogentnexus-openclaw-0.9.3.tgz",
  "packedFileCount": 192
}
```

The regression then failed for the intended reason:

```text
AssertionError: static CRLF contamination was accepted by package validation
actual: 0
expected: 0
operator: notStrictEqual
```

This was a genuine fail-open RED, not a dependency, path, syntax, or harness failure.

## Phase C — minimal GREEN repair

GREEN repair commit:

```text
a812f27815b3c87b7ca748dc2dea88f987601f70
```

The four `.gitattributes` entries were restored forward to:

```gitattributes
plugins/cogentnexus-openclaw/package.json text eol=lf
plugins/cogentnexus-openclaw/README.md text eol=lf
plugins/cogentnexus-openclaw/openclaw.plugin.json text eol=lf
plugins/cogentnexus-openclaw/scripts/bootstrap-ticket-db.mjs text eol=lf
```

`verify-package-contents.mjs` now checks the four static identity files before invoking `npm pack`:

- uses `lstatSync` and requires a regular file;
- reads exact bytes without rewriting;
- rejects any carriage-return byte with an error containing only the offending relative path and policy description;
- does not follow unsupported indirection as a side effect;
- leaves the byte-exact payload fingerprint algorithm unchanged;
- leaves generated `dist` canonicalization separate and generated-only.

The same RED regression passed after the repair. A contaminated `README.md` was rejected before package identity/packing, while the clean package passed with 192 files.

## Phase D — repository validation

The final candidate passed:

```text
focused static-byte regression: PASS
Task-219 real-boundary LF/CRLF regression: PASS
npm run build: PASS
npm test: PASS
npm run evaluation: passed=true
npm run plugin:validate: PASS
packedFileCount: 192
```

The direct second canonicalizer pass returned:

```text
canonicalized 0 dist text files to LF
```

Static byte metrics in the final local candidate:

```text
package.json:                    1051 bytes, CRLF=0, LF-only=36
README.md:                       4022 bytes, CRLF=0, LF-only=66
openclaw.plugin.json:            8162 bytes, CRLF=0, LF-only=68
scripts/bootstrap-ticket-db.mjs: 4269 bytes, CRLF=0, LF-only=106
```

The repository worktree was clean after validation.

## Phase F — authoritative CI

All three workflows ran on the exact final candidate SHA `a812f27815b3c87b7ca748dc2dea88f987601f70`:

| Workflow | Run | Result | URL |
|---|---:|---|---|
| Validate | 33532084137 | success | https://github.com/funggier/CogentNexus-OpenClaw/actions/runs/33532084137 |
| Windows Installer Pack Smoke | 33532084225 | success | https://github.com/funggier/CogentNexus-OpenClaw/actions/runs/33532084225 |
| PS5.1 Acceptance Smoke | 33532084092 | success | https://github.com/funggier/CogentNexus-OpenClaw/actions/runs/33532084092 |

Validate package-proof artifact:

```text
artifact ID: 9810139538
artifact name: cogentnexus-openclaw-v0.9.3-package-proof-a812f27815b3c87b7ca748dc2dea88f987601f70
artifact size: 5832926 bytes
artifact digest: sha256:3164b7770e7d8991691d7bbedced092866c208add72b0c03b4aa3d39d1b50ff0
sourceCommit: a812f27815b3c87b7ca748dc2dea88f987601f70
packageVersion: 0.9.3
payloadFileCount: 192
payloadV2Fingerprint: e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386
tar.gz SHA-256: 88f1c81d5c68da11e7420388a215bf8b72c55a30e7924f24cf6a83b8912a7494
zip SHA-256: 011aaff51462c47440d973a348b938b12a3c2aadcbbe436acf5d54d9f2ad003d
```

## Phase G — fresh Windows exact-first reproduction

Evidence root:

```text
C:\Users\CDQ-P\AppData\Local\Temp\cnx222-windows-exact-qsij57s1
```

The final proof used an independent disposable Windows clone with the final SHA selected before working-tree materialization:

```text
git clone --no-tags --no-checkout https://github.com/funggier/CogentNexus-OpenClaw.git <dir>
git checkout --detach a812f27815b3c87b7ca748dc2dea88f987601f70
```

Immediate first-checkout evidence:

```text
HEAD: a812f27815b3c87b7ca748dc2dea88f987601f70
Git policy: file:C:/Program Files/Git/etc/gitconfig core.autocrlf=true
all four paths: attr/text eol=lf
git ls-files --eol: i/lf w/lf attr/text eol=lf for all four paths
immediate tracked status: clean
```

After `npm ci`, `npm run build`, and `npm run plugin:validate`, the repository-supported identity producer returned:

```json
{"fileCount":192,"fingerprint":"e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386","version":"0.9.3"}
```

The exact CI proof payload and Windows payload were compared using the Windows `npm pack --dry-run --json` file list:

```text
Windows payload files: 192
CI payload files:      192
Total byte differences: 0
Static byte differences: 0
Generated dist differences: 0
Windows fingerprint: e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386
CI fingerprint:      e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386
Final tracked status: clean
```

## Mutation ledger and boundary

```text
product/source changes outside authorized guard: 0
installer/install-over: 0
reset/uninstall/reinstall: 0
cnxclaw lifecycle action: 0
live OpenClaw plugin/config mutation: 0
Gateway restart: 0
live SQLite/ownership/staging/transaction write: 0
provider/model substitution: 0
Discord Sends/API traffic: 0
Release/tag/asset mutation: 0
force push/history rewrite: 0
isolated repository/build evidence: yes
```

## Final decision

```text
PASS_STATIC_BYTE_GUARD__CI_WINDOWS_PAYLOAD_IDENTITY_EQUAL
```

Task 222 closes repository/package provenance only. Stop here for independent review. A later task must explicitly authorize any installer requalification using this exact candidate, fingerprint, fresh exact-first provenance, and the qualified direct Scheduled Task terminal topology from Task 215.
