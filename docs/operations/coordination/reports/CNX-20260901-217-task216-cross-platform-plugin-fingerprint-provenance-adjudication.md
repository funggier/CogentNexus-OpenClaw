# CNX-20260901-217 — Cross-Platform Plugin Fingerprint Provenance Adjudication

## Disposition

`PASS_NEWLINE_VARIANCE_PROVEN__NO_INSTALLER_AUTHORIZED`

Task 217 was diagnostic/build-only. It did not register or start a Scheduled Task, run the CogentNexus installer, perform lifecycle actions, mutate live plugin/SQLite state, restart Gateway, or send Discord traffic.

## Authority

- Task: `CNX-20260901-217`
- Parent: `CNX-20260901-216`
- Exact source commit: `27fe0181b3b65d555a3b0cc8354f6f7945c21c0b`
- Accepted CI fingerprint: `d0677581d60d3d5535c65e3261dae6f50d7aeb245b8680adac0cace4c040643b`
- Windows default fingerprint from Task 216: `3b86b13f6d39996f18687510ab65aa4bba46bdf8d80b1aaeef14fe8d199eb3ed`
- Evidence root: `C:/Users/CDQ-P/AppData/Local/Temp/cnx217-task216-fingerprint-adjudication-20260901T/`

## Fresh source and package validation

A fresh exact-commit candidate checkout was used. The prior Task-216 validation was independently retained:

```text
HEAD: 27fe0181b3b65d555a3b0cc8354f6f7945c21c0b
worktree: clean before build
npm ci: PASS
npm run plugin:validate: PASS
packedFileCount: 192
```

The repository-supported payload-v2 algorithm was inspected directly. It hashes the ordered relative path and exact bytes of the npm `files` payload, including generated `dist/`; it performs no CRLF/LF normalization.

The retained Task-207 tarball was extracted read-only from:

`C:/Users/CDQ-P/AppData/Local/Temp/cnx210-task205-cancel-requal-20260901T/c01-package-proof/cogentnexus-openclaw-v0.9.3.tar.gz`

The archive contained 1,202 tar members and a 192-file package payload.

## Fingerprint reproduction

The extracted retained CI package reproduced the accepted identity exactly:

```text
CI extracted payload:
d0677581d60d3d5535c65e3261dae6f50d7aeb245b8680adac0cace4c040643b
files=192
```

The fresh Windows-default build reproduced the Task-216 discrepancy:

```text
Windows default:
3b86b13f6d39996f18687510ab65aa4bba46bdf8d80b1aaeef14fe8d199eb3ed
files=192
```

The path sets were equal. There were 43 differing `dist` files; all 43 were CRLF/LF-normalizable byte differences. No missing or additional payload path accounted for the fingerprint mismatch.

Line-ending counts in `dist`:

```text
CI extracted payload: CRLF=0, LF=19102
Windows build:       CRLF=957, LF=19102
```

## Controlled LF experiment

An isolated copy of the Windows build was run with:

```text
npm exec -- tsc -p tsconfig.json --newLine lf
```

The resulting output was byte-identical to the Windows-default output; its fingerprint remained:

```text
3b86b13f6d39996f18687510ab65aa4bba46bdf8d80b1aaeef14fe8d199eb3ed
```

The default and explicit-`--newLine lf` output trees had zero byte differences. Therefore the compiler flag alone did not canonicalize the generated output in this Windows checkout; source/newline preservation remained effective.

A separate isolated normalization experiment converted CRLF to LF for the declared payload bytes only. It produced:

```text
normalized Windows payload:
d0677581d60d3d5535c65e3261dae6f50d7aeb245b8680adac0cace4c040643b
files=192
TARGET_MATCH=true
```

This proves that the accepted CI and fresh Windows identities differ solely at the byte-level newline representation of generated payload files, with the observed differences confined to 43 `dist` files.

## Live preservation check

Final read-only checks after all isolated work:

```text
status exit: 0
mode: passthrough
generation: 33
selected provider: ollama
Gateway: healthy
startup adapter installed: false
Delivery: READY, stateChanged=false
Recovery: READY, stateChanged=false
```

No live product path was modified.

## Mutation ledger

```text
Fresh isolated checkout/build: yes
CI archive extraction: read-only
CRLF/LF normalization experiment: isolated copy only
Scheduled Task registration: 0
Installer invocation: 0
Installer retry: 0
Lifecycle action: 0
Plugin/OpenClaw mutation: 0
Gateway restart: 0
SQLite write: 0
Provider/model/config mutation: 0
Process termination: 0
Discord traffic: 0
Source/test/workflow edit or commit: 0
Release/tag/asset mutation: 0
```

## Conclusion

The cross-platform payload mismatch is proven to be exact generated-byte newline variance: CI payload bytes are LF-only, while the Windows build contains CRLF in 43 generated `dist` files. The simple TypeScript `--newLine lf` option did not change the Windows output in this controlled run; a future repair must explicitly canonicalize generated/package bytes or otherwise establish a deterministic cross-platform build. No installer requalification is authorized by this diagnostic report. A separate TDD repair task is required before creating a new candidate/package proof.
