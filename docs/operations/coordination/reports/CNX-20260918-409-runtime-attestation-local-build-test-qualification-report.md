# CNX-20260918-409 — Runtime Attestation Local Build and Test Qualification

## Classification

`RUNTIME_ATTESTATION_LOCAL_REPAIR_GREEN`

Local source/build/test/package qualification passed after one minimal test-fixture repair. No production deployment or live runtime call occurred.

## Authority and repository identity

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Task: `CNX-20260918-409`
- Starting remote HEAD: `7428bf95691e37148d23de3d3a1720fdba5ae448`
- Starting local HEAD: `7428bf95691e37148d23de3d3a1720fdba5ae448`
- Ending local/remote HEAD: verified equal after publication; exact final SHA is reported in the closeout message because embedding the commit containing this report would be self-referential.
- Pre-publication repair commit: `1b686d48126a9aaaf46a21acc3b96ae39e4df424`
- CNX-408 implementation lineage: `a1b38dfcbe961cbbb38da3e44342630176ba954d` (RED test), `6567d1fac5ea0633fb7f5839456ea58a3e7147ca` (implementation), `4576f8c92965957a246578f55fc6920e5af3bb59` (release-entry wiring)

The original operator checkout contained unrelated untracked files, so validation and publication used a fresh clean clone at the authoritative remote branch.

## Dependency and toolchain

From `plugins/cogentnexus-openclaw`:

- `node`: `v22.23.2`
- pinned package declaration: `openclaw: 2026.7.1-2`
- lockfile resolution: `node_modules/openclaw` version `2026.7.1-2`
- resolved tarball: `https://registry.npmjs.org/openclaw/-/openclaw-2026.7.1-2.tgz`
- public SDK resolution:
  - `openclaw/plugin-sdk/plugin-runtime` -> `node_modules/openclaw/dist/plugin-sdk/plugin-runtime.js`
  - `openclaw/plugin-sdk/plugin-entry` -> `node_modules/openclaw/dist/plugin-sdk/plugin-entry.js`
- `npm ci` completed successfully using the existing lockfile. npm reported 8 audit vulnerabilities and blocked optional install scripts; neither changed the locked dependency version. No dependency was patched or upgraded.

## Exact validation commands and results

### Initial focused RED

```text
npm test -- --run src/v095-runtime-hook-attestation.test.ts src/v097-release-wiring.test.ts src/v091-wiring.test.ts src/v090-model-selection-boundary.test.ts src/v095-behavior-matrix.test.ts src/cnx374-registry-wiring.test.ts
```

Result: **failed**, `5 passed / 1 failed`, `20 passed / 21 total`.

Failure:

```text
TypeError: api.registerGatewayMethod is not a function
at registerRuntimeHookAttestation src/v095-runtime-hook-attestation.ts:81:7
at Object.register src/v091-release-entry.ts:185:5
at src/cnx374-registry-wiring.test.ts:53:20
```

Root cause: the older CNX-374 production-shaped test fixture did not provide the newly required public `registerGatewayMethod` API surface after CNX-408 release-entry wiring registered the attestation RPC. This was a test-harness defect, not a provider, routing, Ticket, or OpenClaw dependency defect.

### Minimal repair

Changed exactly one test fixture line in:

```text
plugins/cogentnexus-openclaw/src/cnx374-registry-wiring.test.ts
```

Added:

```text
registerGatewayMethod: vi.fn(),
```

Repair commit: `1b686d48126a9aaaf46a21acc3b96ae39e4df424`.

### Focused runtime-attestation test

```text
npm test -- --run src/v095-runtime-hook-attestation.test.ts
```

Result: **PASS** — 1 file, 3 tests.

### Focused regression suite after repair

```text
npm test -- --run src/v095-runtime-hook-attestation.test.ts src/v097-release-wiring.test.ts src/v091-wiring.test.ts src/v090-model-selection-boundary.test.ts src/v095-behavior-matrix.test.ts src/cnx374-registry-wiring.test.ts
```

Result: **PASS** — 6 files, 21 tests.

Covered:

- runtime attestation;
- release-entry/wiring;
- CNX-374 registry wiring;
- model-selection boundary;
- provider-independent behavior matrix.

### TypeScript/plugin build

```text
npm run build
```

Result: **PASS** — `tsc -p tsconfig.json` completed; `canonicalize-dist.mjs` reported `canonicalized 50 dist text files to LF`.

### `plugin:validate`

```text
npm run plugin:validate
```

Result: **PASS**.

Exact reported checks:

```text
CogentNexus-OpenClaw mixed-plugin artifact verification: PASS (46 config properties, 5 tools)
CogentNexus-OpenClaw ticket DB bootstrap: PASS (9 required tables + v095 registration fence)
{"result":"ok","package":"openclaw-plugin-cogentnexus-openclaw-0.9.5.tgz","required":["dist/v091-release-entry.js","scripts/bootstrap-ticket-db.mjs","openclaw.plugin.json","README.md"],"packedFileCount":256}
```

## Built artifact evidence

After build/validation:

- `dist/v091-release-entry.js` exists, 8,536 bytes.
- `dist/v095-runtime-hook-attestation.js` exists, 1,612 bytes.
- `dist/v091-release-entry.js` imports `./v095-runtime-hook-attestation.js`.
- emitted attestation module contains `cogentnexus.runtimeAttestation` and `{ scope: "operator.read" }`.
- SHA-256:
  - `dist/v091-release-entry.js`: `343c221db6d9259fb38bb335cf5f3293bb838a7515a909666471b990da056f4b`
  - `dist/v095-runtime-hook-attestation.js`: `90d3d95064f1a11b483ce0725dc5782cbaf7fdb6533f1f8b5f443c3da3f33a1d`
- `plugin:validate` package verification confirms the required release entry is included in the generated package.

## Exact files changed by CNX-409

```text
plugins/cogentnexus-openclaw/src/cnx374-registry-wiring.test.ts

docs/operations/coordination/reports/CNX-20260918-409-runtime-attestation-local-build-test-qualification-report.md
docs/operations/coordination/ACTIVE.md
docs/operations/coordination/STATUS.md
```

The attestation source, attestation test, and release-entry wiring were already present in the authoritative starting commit; they were qualified, not rewritten.

## Residual uncertainty

- This task proves local source/build/test/package behavior only. It does not prove that a production Gateway has loaded the candidate or that the live RPC is available.
- No live `cogentnexus.runtimeAttestation` call was made.
- npm audit reported 8 vulnerabilities (4 moderate, 4 high); dependency remediation is outside this task and was not attempted.
- The npm install output noted blocked package install scripts; the pinned package resolved and the required SDK imports/build/tests all succeeded.

## Hard-fence accounting

- Production install/install-over: 0
- Production artifact replacement: 0
- Gateway restart/reload: 0
- Production config/environment/Scheduled Task mutation: 0
- Live Gateway RPC calls: 0
- Semantic/model/provider requests: 0
- Provider/model/auth/routing changes: 0
- TicketStore/durable-state mutation: 0
- OpenClaw dependency patch/version change: 0
- Release/tag/main changes: 0
- Force-push/history rewrite: 0
- CNX-410 created/started: 0

## Closeout

`ACTIVE.md` and `STATUS.md` were changed from `READY_FOR_HERMES` to `WAITING_FOR_CHATGPT_REVIEW`. Final remote/local HEAD equality and clean-worktree state were verified after publication. Execution stops here; no deployment and no CNX-410.

## Final classification

`RUNTIME_ATTESTATION_LOCAL_REPAIR_GREEN`
