# CNX-349 — Runtime Artifact & Effective Hook Provenance Report

## Result

**Classification: UNRESOLVED — BLOCKED.** Neither D nor E is proven by the authorized read-only evidence. No production repair was made.

## GitHub authority

- Remote branch: `cnx-349-runtime-artifact-provenance`
- Starting GitHub HEAD: `9dcb150d5a120ec5b6bc9c2618f6036abf2680e1`
- Parent baseline: `5d02a044007ece94b66d1845ecbdf7d686678498` (CNX-348)
- Repository: `https://github.com/funggier/CogentNexus-OpenClaw`
- Initial verification: `git remote -v`, `git fetch origin`, and `git rev-parse origin/cnx-349-runtime-artifact-provenance` returned the expected starting HEAD.

## Inventory performed from the GitHub branch

The branch contains these relevant read-only/static mechanisms:

- `plugins/cogentnexus-openclaw/src/cnx348-effective-runtime-provenance.test.ts`
  - records `import.meta.url`;
  - records registration invocation/trace;
  - retains an effective hook map;
  - asserts one `before_agent_run` hook at priority `2000` in a synthetic OpenClaw-shaped loader;
  - contains a negative control where bypassing `register` yields effective admission visibility `0`.
- `plugins/cogentnexus-openclaw/src/v091-release-entry.ts` and `src/v091-final-entry.ts`
  - are the repository source registration path.
- `plugins/cogentnexus-openclaw/package.json`
  - declares `./dist/v091-release-entry.js` as the OpenClaw extension entry.
- Existing installer/acceptance documentation exposes installed plugin fingerprints and paths, but those records are historical/documentary unless freshly read from the current runtime.

Static source can establish the expected registration shape only; it cannot establish the module loaded by the already-running process.

## Boundary evidence

### GitHub source identity

Freshly read from the verified starting commit:

| Path | Git blob | SHA-256 of checked-out source bytes |
|---|---|---|
| `plugins/cogentnexus-openclaw/src/v091-release-entry.ts` | `fb51fbbbd62bb75261e221cd9d4f139be90e803b` | `210d5ce44580781dc413a44f4641e52c2c073e6a9fd0ff08ac58388059b323b4` |
| `plugins/cogentnexus-openclaw/src/v091-final-entry.ts` | `31b0219b3a341e8655eae7adbeed69c63240f21f` | `7b20c7e8a1eea08cc260350a31e883f69cf543da03f480ff5970050cf998e947` |

### Build/dist identity

The repository’s `dist/` directory is ignored/not present in the GitHub source tree at this branch. A fresh build could not be run because the isolated checkout has no installed npm dependencies: the exact focused command returned `'vitest' is not recognized as an internal or external command`. Installing dependencies was prohibited by the hard fence. Therefore no fresh build/dist hash is asserted.

### Installed artifact identity

Read-only hashes from the currently installed extension:

- `C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw\dist\v091-release-entry.js`
  - SHA-256: `c15b2f61a1596f301510e9cd392851ef99427c6c129d653d2d336cfefa79b3a8`
- `C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw\dist\v091-final-entry.js`
  - SHA-256: `8b734db6252696d3ad90d010b7e8f124cb2eb03f22bf683cb83d516748eaaf40`

These are JavaScript build artifacts, while the GitHub source identities above are TypeScript source bytes. Without a fresh authorized build or a published source-to-dist mapping for this exact commit, the differing byte hashes do **not** prove D.

### Running-process identity

`openclaw plugins list --json` was executed read-only. It reported:

- plugin id: `cogentnexus-openclaw`
- version: `0.9.5`
- source/module path: `C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw\dist\v091-release-entry.js`
- root: `C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw`
- origin: `global`
- enabled: `true`
- status: `loaded`
- `hookNames: []`
- `hookCount: 0`
- registry source: `persisted`
- diagnostics: `[]`

This is plugin inventory metadata, not proof of the exact JavaScript bytes loaded by a specific PID and not proof that dynamic hooks were absent from the effective runtime registry. The process inventory exposed two `node.exe` PIDs (`17080`, `20572`) but did not identify either as the OpenClaw gateway, and no `openclaw.exe` process was listed. No loaded-module list tied to a specific running PID was available through the authorized read-only probes. Running-process identity is therefore incomplete.

### Effective hook registry identity

The repository synthetic test proves only that the controlled loader retains the expected `before_agent_run` registration. The live `plugins list` output reported `hookNames: []` and `hookCount: 0`, but the branch’s CNX-348 evidence explains that dynamic registration is not represented by that static inventory field. No live effective-hook registry dump was available. This boundary is unresolved.

### Dashboard execution path / invocation

No semantic Dashboard request or UI interaction was performed. The repository/static evidence reviewed does not provide a read-only proof that the actual Dashboard request path bypasses `before_agent_run`. Therefore E is not proven.

## Tests and fresh results

Exact command attempted:

```text
npm test -- --run src/cnx348-effective-runtime-provenance.test.ts
```

Fresh result: **BLOCKED before test execution** — `vitest` was not recognized because npm dependencies were absent. No dependency installation was performed.

The chained build/adjacent-test command was not allowed to proceed after this prerequisite failure. No test pass is claimed. The existing CNX-348 negative control is synthetic evidence only and is not evidence about the live OpenClaw process.

## D/E decision

- **D — not proven.** Installed artifact path and hashes were observed, but exact source-to-build identity for this commit and exact loaded-module identity for a running OpenClaw PID were not established.
- **E — not proven.** No authorized static/read-only execution-path evidence showed Dashboard/webchat bypassing `before_agent_run`; live semantic traffic was prohibited and not used.
- **Final classification: UNRESOLVED / BLOCKED.**

Smallest next read-only probe: obtain a process-scoped OpenClaw gateway diagnostic that reports the gateway PID, loaded CogentNexus module URL, loaded artifact SHA-256, registration metadata, and effective hook registry without restarting or sending a semantic request. Separately, obtain a source-to-dist mapping or reproducible build proof for the exact GitHub commit.

## Changes

Only this report was added. No production source, runtime configuration, provider routing, database, installation, or UI state was changed.

## Hard-fence verification

- No `durableAdmissionEligible` change.
- No timeout-authority change.
- No second admission owner.
- No provider-routing change.
- No production behavior change.
- No install/reinstall.
- No OpenClaw restart.
- No runtime/config/database mutation.
- No semantic Dashboard request.
- No UI interaction.
- No CNX-344 replay/resend.
- No v0.9.5 tag/history mutation.
- No force-push/history rewrite.
- No self-acceptance.
