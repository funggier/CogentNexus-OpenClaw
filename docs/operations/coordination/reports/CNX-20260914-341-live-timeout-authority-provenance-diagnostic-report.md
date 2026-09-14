# CNX-341 — Live Timeout Authority Provenance Diagnostic Report

Status: `PASS`
Classification: `ROOT_CAUSE_PROVEN — STALE_RUNTIME_ARTIFACT`
Task: `CNX-341`
Parent: `CNX-340F`
Diagnostic branch: `agent/v0.9.6-live-timeout-authority-diagnostic`
Diagnostic commit: `41e8593fd95c5790ae24ef75c99b9f72a561ba75`
Reference repair branch: `agent/v0.9.6-direct-model-call-timeout-authority-repair`
Reference repair commit inspected: `460a8cd6`
Known CNX-340F session: `agent:main:dashboard:945504d3-42f1-497a-b635-9975561e4bd5`

## Disposition

The concrete cause of the `900000` lease is proven: the installed plugin directory used by the local Gateway contains a legacy `v091-direct-model-call-lease.js`. That loaded-path module defines `DIRECT_MODEL_CALL_TIMEOUT_MS = 15 * 60_000` and persists the clamped input directly; it does not contain `runtimeModelCallTimeoutMs` and does not contain the repaired resolver call site. Therefore the runtime could only produce the observed legacy `900000` value on the affected path.

No repair, restart, installation, semantic request, model call, retry, Dashboard session creation, or `New session` click was performed.

## Proven

### Exact running Gateway and installed paths

- Gateway process: PID `3172`
- Command line: `C:\\Program Files\\nodejs\\node.exe C:\\Users\\CDQ-P\\AppData\\Roaming\\npm\\node_modules\\openclaw\\dist\\index.js gateway --port 18789`
- Working directory: `C:\\Windows\\system32`
- Process start time observed through process inspection: `2026-09-14T05:51:19.621974`
- Installed plugin directory: `C:\\Users\\CDQ-P\\.openclaw\\extensions\\cogentnexus-openclaw`
- Entry path: `C:\\Users\\CDQ-P\\.openclaw\\extensions\\cogentnexus-openclaw\\dist\\v091-release-entry.js`
- Entry SHA-256: `c15b2f61a1596f301510e9cd392851ef99427c6c129d653d2d336cfefa79b3a8`
- Entry size: `10121` bytes
- Entry modification time: `2026-09-14T05:49:00.159955`
- Entry imports `./v091-direct-model-call-lease.js`.
- Loaded-path lease module: `C:\\Users\\CDQ-P\\.openclaw\\extensions\\cogentnexus-openclaw\\dist\\v091-direct-model-call-lease.js`
- Lease module SHA-256: `943a6d0d71cf71e32d6d1a79722d6e25200d0419ebc5b15e4c144e654cfaa480`
- Lease module size: `17017` bytes
- Lease module was inspected directly and contains:
  - `export const DIRECT_MODEL_CALL_TIMEOUT_MS = 15 * 60_000;`
  - `const timeoutMs = Math.max(60_000, Math.min(input.timeoutMs ?? DIRECT_MODEL_CALL_TIMEOUT_MS, 3_600_000));`
- The installed lease module contains none of:
  - `runtimeModelCallTimeoutMs`
  - `timeoutMs: runtimeModelCallTimeoutMs`
  - `2700000`
  - `900000` as a literal (the 900000 result is the evaluated `15 * 60_000` fallback)

The entry file's import path plus the exact installed module contents establish the artifact composition at the Gateway's plugin path. The process was already running from the OpenClaw Gateway command above; no restart was attempted.

### Repaired source reference

At reference commit `460a8cd6` on `agent/v0.9.6-direct-model-call-timeout-authority-repair`, the source file contains:

- `runtimeModelCallTimeoutMs(api: any, event: any, ctx: any)`
- explicit precedence for `event.timeoutMs`, `event.timeoutSeconds`, `ctx.timeoutMs`, and `ctx.timeoutSeconds`
- runtime defaults/provider/plugin configuration lookup
- `timeoutMs: runtimeModelCallTimeoutMs(api, event, ctx)` at the `model_call_started` persistence call

This is reference evidence only. It is not treated as proof that the live Gateway loaded that repaired source.

### Resolver-boundary result

The installed runtime module has no resolver boundary. Its effective boundary is the legacy expression:

```js
input.timeoutMs ?? (15 * 60_000)
```

For the CNX-340F event where no repaired runtime-derived timeout was persisted, this evaluates to `900000`. The durable CNX-340F result was `timeoutMs = 900000`, exactly matching this installed legacy authority.

No additional live model call or semantic request was made to reproduce it.

### Package/version metadata

The installed extension root contains `package.json` with:

- name: `openclaw-plugin-cogentnexus-openclaw`
- version: `0.9.5`
- private: `true`
- OpenClaw extension entry: `./dist/v091-release-entry.js`

This metadata is not used alone for the classification; the classification is based on the exact installed module contents and hashes.

## Gateway load boundary evidence and limits

- The running Gateway process was identified without restart.
- Its process start time is approximately two minutes after the installed entry file modification time.
- The entry file imports the legacy lease module at the exact installed plugin path.
- No independent OpenClaw plugin-loader trace exposing an absolute resolved module path was available in the read-only inspection.
- Timestamps are supporting evidence only and are not treated as causal proof.
- The decisive evidence is the legacy implementation in the exact imported module at the installed plugin path, not the timestamps or branch names.

## Timeout inputs observed

A live resolver diagnostic was not run because the installed module does not expose the repaired resolver and the task forbids adding persistent instrumentation or sending another model call. The observable effective inputs/authority are:

| Boundary | Observed value |
|---|---:|
| `event.timeoutMs` | Not available from a new live event; no request was sent |
| `event.timeoutSeconds` | Not available from a new live event; no request was sent |
| `ctx.timeoutMs` | Not available from a new live event; no request was sent |
| `ctx.timeoutSeconds` | Not available from a new live event; no request was sent |
| `api.config.agents.defaults.timeoutSeconds` | Not required/consulted by installed legacy module |
| `api.config.models.providers.ollama.timeoutSeconds` | Not required/consulted by installed legacy module |
| plugin/runtime config timeout fields | Not required/consulted by installed legacy module |
| effective installed fallback | `15 * 60_000 = 900000` |
| CNX-340F durable lease | `900000` |

## Hypotheses not needed for classification

- It is not necessary to claim that the Gateway was stale solely because repository branches differ.
- It is not proven whether the installation process selected an old package, assembled a mixed package, or copied only part of a repaired build.
- It is not proven whether a prior process load boundary contributed independently.
- Those are packaging/load-history hypotheses. The evidence-backed runtime cause is that the installed imported lease module remained legacy.

## Reconciliation with CNX-340F

CNX-340F persisted `timeoutMs = 900000`. The exact installed module used by the running Gateway has a legacy default of `15 * 60_000` and no repaired resolver. The numerical result is therefore explained directly and without guessing: `15 * 60_000 = 900000`.

The repaired source's expected `2700000` can never be reached by this installed module because it does not contain the repaired runtime authority function or call site.

## Classification

`ROOT_CAUSE_PROVEN — STALE_RUNTIME_ARTIFACT`

Narrow meaning in this report: the artifact actually present at the Gateway's installed/imported path is legacy with respect to CNX-340A's timeout-authority repair. This classification does not rely on branch-name comparison or timestamps.

## Successor recommendation

Create a successor repair/requalification task that:

1. builds a complete artifact from the repair commit;
2. verifies the SHA-256 of every imported direct-model-call module, not only `v091-release-entry.js`;
3. installs the complete artifact atomically at the Gateway plugin path;
4. records an installation manifest containing entry and imported-module hashes;
5. authorizes a Gateway restart/load-boundary refresh explicitly;
6. performs the separate live requalification only after the artifact manifest and loaded-path evidence match the repaired implementation.

Do not perform those actions inside CNX-341.

## Fences and review

- Read-only diagnostic only.
- No Dashboard `New session` click.
- No new session.
- No semantic traffic or additional model call.
- No retry/resend/recovery/fallback/manual dispatch.
- No provider/model/config/controller/database mutation.
- No installation or Gateway restart.
- No production code/test changes.
- No `v0.9.5` change.
- No force-push or history rewrite.
- CNX-341 is not self-accepted; stop for independent ChatGPT review.

## Evidence status

`PASS` for the diagnostic criterion: the concrete cause of `900000` is identified sufficiently to choose the next successor action without guessing.
