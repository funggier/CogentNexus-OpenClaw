# Independent Review — CNX-20260901-217 Cross-Platform Plugin Fingerprint Provenance Adjudication

## Verdict

`ACCEPT_PASS_NEWLINE_VARIANCE_PROVEN__TDD_DETERMINISTIC_PAYLOAD_REPAIR_REQUIRED`

Task 217 closes the Task-216 authority ambiguity without mutating the live product. The retained Task-207 CI payload and the fresh Windows build have the same 192-path installable payload set, and every byte difference is confined to 43 generated `dist` files whose differences are CRLF/LF-normalizable. Normalizing those Windows payload bytes to LF reproduces the accepted CI payload fingerprint exactly.

## Accepted facts

- exact Task-207 source under test remained `27fe0181b3b65d555a3b0cc8354f6f7945c21c0b`;
- retained CI package payload reproduced `d0677581d60d3d5535c65e3261dae6f50d7aeb245b8680adac0cace4c040643b` with 192 files;
- fresh Windows build reproduced `3b86b13f6d39996f18687510ab65aa4bba46bdf8d80b1aaeef14fe8d199eb3ed` with the same 192 paths;
- exactly 43 `dist` files differed byte-for-byte;
- all 43 differences were explainable by CRLF/LF representation only;
- retained CI `dist` was LF-only at the observed newline boundary, while Windows output contained CRLF bytes;
- explicit `tsc --newLine lf` did not change the Windows output in the controlled experiment and therefore is not an independently sufficient repair;
- isolated CRLF→LF normalization of the declared Windows payload reproduced `d0677581...` exactly;
- no installer, lifecycle, plugin, Gateway, SQLite, provider/model, Discord, release, or live product mutation occurred.

## Interpretation

The product/source semantics are not the source of the Task-216 mismatch. The authority failure is caused by cross-platform nondeterminism in generated installable bytes.

The ownership fingerprint must remain byte-exact. The repair must therefore make the generated/package bytes deterministic; it must not weaken `_plugin_payload()` by normalizing during fingerprint computation or by accepting multiple fingerprints for semantically equivalent payloads.

The `--newLine lf` experiment is important negative evidence: a configuration-only assumption is not sufficient. The repair needs a regression test that deterministically reproduces LF-vs-CRLF source/build conditions and then a bounded canonicalization step at the generated-output/build boundary.

## Required successor

Open Task 218 as a TDD repair task.

Required TDD shape:

1. **RED first**: add a test-only regression that creates logically identical LF-source and CRLF-source build fixtures, executes the real plugin build/package path for each, and asserts identical installable payload bytes/fingerprint. On pre-fix source this test must fail for the proven newline reason.
2. Commit the RED test separately; no production/build-path change in that commit.
3. **Minimal GREEN**: canonicalize generated `dist` text bytes to LF after TypeScript emit and before any package/fingerprint operation. Prefer an explicit fail-closed post-emit utility invoked from the normal build path. Do not normalize source files, do not modify the fingerprint algorithm, and do not accept multiple fingerprints.
4. The canonicalizer must be bounded to generated `dist` regular text artifacts, reject/avoid filesystem indirection, and not silently mutate unrelated package files.
5. Prove the focused regression GREEN, full plugin tests/build/validation GREEN, and fresh Windows payload identity stable.
6. Run authoritative CI for the exact new candidate and retain a new package proof. Because `package.json` and/or build scripts may change, the new candidate fingerprint is expected to be a new exact value; do not require it to remain `d067...` unless the actual repaired package bytes do so naturally.
7. After CI, re-build the exact new candidate on Windows and require its payload fingerprint to equal the new CI package-proof fingerprint exactly.

## Live boundary

Task 218 is repository/build repair only. It must not run the installer, lifecycle actions, Gateway actions, live SQLite mutation, provider/model substitution, or Discord traffic. Windows live state remains at the preserved PASSTHROUGH old generation until the new candidate/package authority is independently reviewed.

## Disposition

`ACCEPT_PASS_NEWLINE_VARIANCE_PROVEN__TDD_DETERMINISTIC_PAYLOAD_REPAIR_REQUIRED`
