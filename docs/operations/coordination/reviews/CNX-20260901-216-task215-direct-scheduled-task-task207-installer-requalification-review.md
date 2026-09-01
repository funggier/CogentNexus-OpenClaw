# Independent Review — CNX-20260901-216 Task-207 Installer Requalification

## Verdict

`ACCEPT_BLOCKED_AUTHORITY__CROSS_PLATFORM_PAYLOAD_FINGERPRINT_ADJUDICATION_REQUIRED`

Task 216 stopped at the correct boundary. It did not register a Scheduled Task or invoke the installer after the fresh exact Windows checkout at `27fe0181b3b65d555a3b0cc8354f6f7945c21c0b` produced plugin payload fingerprint `3b86b13f6d39996f18687510ab65aa4bba46bdf8d80b1aaeef14fe8d199eb3ed` instead of the accepted Task-207 package-proof fingerprint `d0677581d60d3d5535c65e3261dae6f50d7aeb245b8680adac0cace4c040643b`.

## Accepted facts

- fresh checkout HEAD was exact `27fe0181b3b65d555a3b0cc8354f6f7945c21c0b` and clean;
- `scripts/install.ps1` and the Task-207 production repair source file matched the exact candidate bytes;
- `npm ci` and `npm run plugin:validate` passed on Windows;
- packed file count remained `192`;
- repository-supported `plugin-fingerprint` after the Windows build returned `3b86b13f6d39996f18687510ab65aa4bba46bdf8d80b1aaeef14fe8d199eb3ed`;
- accepted CI package proof from Validate run `33483589170`, artifact `9790881384`, is still available and is bound to head SHA `27fe0181...`, digest `sha256:1733897690890f9adcb12176b79db2b43e27799a4022743c4597fad44d2d5a34`, with payload fingerprint `d0677581...`;
- no live installer/lifecycle/plugin/Gateway/SQLite/provider/model/Discord mutation occurred in Task 216.

## Independent source interpretation

The two fingerprint values use the same payload-v2 ownership algorithm. `_plugin_payload()` hashes `package.json` plus every file selected by `package.json.files` byte-for-byte, including the generated `dist/` tree.

The package dry-run that established `d0677581...` runs on `ubuntu-latest`, performs `npm ci` and `npm run plugin:validate`, then computes the payload identity. Task 216 performed the corresponding build on Windows.

`plugins/cogentnexus-openclaw/tsconfig.json` does not explicitly set TypeScript `compilerOptions.newLine`. Therefore generated output bytes are not yet proven platform-independent. This is a concrete hypothesis, not a concluded root cause.

## Required next action

Open a read-only/product-preserving Task 217 to compare the retained Ubuntu package-proof payload against a fresh Windows build file-by-file and determine whether the fingerprint mismatch is entirely generated-output newline/platform variance or another payload difference.

Task 217 must not install, enable, restart, edit product source, mutate SQLite, or send Discord traffic. It may build exact-candidate copies in isolated evidence directories and may use the still-unexpired package-proof artifact.

If Windows `tsc --newLine lf` produces a byte-identical payload and fingerprint `d0677581...`, the cross-platform build nondeterminism is proven and a separate TDD repair task should make the build canonical before another installer attempt.

## Disposition

`ACCEPT_BLOCKED_AUTHORITY__CROSS_PLATFORM_PAYLOAD_FINGERPRINT_ADJUDICATION_REQUIRED`
