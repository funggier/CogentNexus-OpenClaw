# Review — CNX-20260827-093 Repair Dashboard Durable Payload Staging Boundary

Decision: `REWORK`

Disposition: `REWORK_PLUGIN_FINGERPRINT_DOES_NOT_ATTEST_RUNTIME_PAYLOAD`

Reviewed report HEAD:

`62fdd69d2a4a27566c0e986171b949347cf0df68`

Execution HEAD:

`dad3f991f5dd392d8dff602584c13e80c36ddf03`

Implementation HEAD:

`a924157ecdedef1d4f166d5762529b0d59536fc9`

## Publication fence

Accepted.

- execution -> implementation is exactly one source/test commit;
- changed files are only:
  - `plugins/cogentnexus-openclaw/src/v091-dashboard-verified-delivery.ts`
  - `plugins/cogentnexus-openclaw/src/v091-dashboard-verified-delivery.test.ts`;
- implementation -> report is exactly one report-only commit;
- no live mutation is represented in repository history.

## Dashboard staging repair review

The Task-093 root cause and source repair are technically credible and independently supported.

The accepted pre-fix code coupled two distinct lifetimes behind one `TicketStore.prototype` `PATCH` marker: one-time prototype patching and runtime `reply_dispatch` hook registration. The Task-093 RED reproduces the second-registration hook loss and the source change separates those lifetimes.

The new `WeakSet<object>` per-runtime registration guard is consistent with exact upstream OpenClaw `2026.7.1-2` (`0790d9f`) loader behavior:

- each plugin load creates an API using `createApi(...)`;
- `runPluginRegisterSync(...)` wraps the supplied API in a fresh guarded `Proxy` for the registration callback;
- a legitimate later plugin registration therefore receives a distinct registration API object even when the module/prototype state remains in the same Node process;
- the one-time prototype patch may safely remain process-global while hook registration must occur for each fresh runtime API lifecycle.

The focused RED/GREEN and full plugin/Python compatibility evidence are otherwise sufficient for this narrow source fix.

## Blocking attestation defect

Task 093 explicitly required that any plugin payload source change produce a new plugin fingerprint and that the exact new fingerprint be recorded for a later supported install-over.

That requirement is not satisfied.

The report records the candidate fingerprint as:

`8fd911e3b8f6326c8907b7d92c11028d931df203dcaafdb59cc1e6d0a3b56360`

which is the same fingerprint already accepted for the pre-Task-093 live plugin.

Fresh source review explains why. Production `skills/cogentnexus-openclaw/scripts/namespace_ownership.py::_plugin_payload()` hashes only four files:

1. `openclaw.plugin.json`;
2. `package.json`;
3. `scripts/bootstrap-ticket-db.mjs`;
4. `dist/ticket-store.js`.

It does not hash `dist/v091-dashboard-verified-delivery.js` or the rest of the installed runtime payload.

Task 093 changed the source that compiles into `dist/v091-dashboard-verified-delivery.js`, while none of the four fingerprinted files changed. Therefore the unchanged fingerprint is expected under the current algorithm and does not attest the repaired runtime behavior.

## Why this blocks live installation

This is not a documentation-only issue.

The installer builds/validates the candidate, calculates `expectedPluginFingerprint`, and passes it into `classify-install`. For a coherent one-generation upgrade state, classification currently sets:

`pluginAlreadyExact = liveCandidateFingerprint == expectedReplacementFingerprint`

and the lifecycle action resolver then skips package installation when `pluginAlreadyExact=true`.

Because the old live runtime and the repaired Task-093 candidate can receive the same four-file fingerprint, a successor install-over can incorrectly classify the old live plugin as already exact and skip installing the Task-093 fix.

Therefore Task 093 cannot safely release a live-install successor while the fingerprint authority is blind to most runtime files.

## Required rework direction

Preserve the Task-093 Dashboard staging implementation/test commit as the candidate source fix. Do not discard or broaden it.

Before any live install-over, repair the plugin attestation boundary so the fingerprint binds the complete installable/runtime payload deterministically rather than a four-file sample.

The successor design should at minimum:

- hash `package.json` plus the complete package-owned runtime payload that can be installed (`dist/**`, `openclaw.plugin.json`, packaged bootstrap script, README/package metadata as appropriate);
- include normalized relative paths as well as bytes in the digest so renames/substitutions are detectable;
- exclude non-package development residue (`src/**`, tests, `node_modules/**`, transient npm artifacts) unless it is actually shipped;
- reject unsafe/symlink/path-escape payload entries;
- prove a mutation to `dist/v091-dashboard-verified-delivery.js` changes the fingerprint;
- prove an identical packed/copied installed payload yields the same fingerprint;
- prove the Task-093 candidate fingerprint differs from the currently installed pre-fix payload;
- prove `classify-install` returns ordinary changed-payload upgrade (`pluginAlreadyExact=false`, install=true, rollover=true) for this exact case;
- preserve same-version rollover source-attestation, exact plan/apply inventory/tree fences and npm 11/npm 12 package behavior.

No live install or semantic retest is authorized by this review.

## Successor gate

A new source-only TDD task is required for full installable-payload fingerprint attestation. Only after that repair is independently accepted may the Task-093 staging fix be installed live and parity re-proven.
