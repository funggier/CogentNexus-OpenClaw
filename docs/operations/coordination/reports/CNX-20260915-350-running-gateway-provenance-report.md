Remote branch: `cnx-350-running-gateway-provenance`
Final GitHub HEAD: `99482a7a0235229a8bb650c3239b5ac7b59bd5d8` (GitHub report-publication/finalization commit; verified by remote fetch/read-back)
Parent baseline: `b1ecee8a552821872bb4e815c7ba35bd0418e541` (verified ancestor of starting remote HEAD)

## Classification

**UNRESOLVED** — neither D nor E is proven. The environment exposes a real Gateway PID and installed plugin inventory, but it does not expose process-scoped loaded CogentNexus module identity or an effective hook registry. Static source tracing shows the intended Dashboard/WebChat path is registered through the canonical release entry and `before_agent_run`, but static registration code does not prove that the running process bypasses or invokes it.

## Changed files

- `docs/operations/coordination/reports/CNX-20260915-350-running-gateway-provenance-report.md`
- No production source, build output, configuration, installation, runtime, database, or UI files changed.

## Source identity

- GitHub branch at investigation start: `19907f2fbe27ec3ce785e1d4bea5f5e93f16d713`.
- Repository source was read from that exact remote branch/commit.
- Relevant source paths: `plugins/cogentnexus-openclaw/src/v091-release-entry.ts`, `v091-final-entry.ts`, `v090-final-entry.ts`, `index.ts`, `v095-inference-hook-bridge.ts`, and existing `cnx348-effective-runtime-provenance.test.ts`.
- Source observations: `v091-release-entry.ts` calls the legacy `register(runtimeApi)` and then installs runtime guards; `v091-final-entry.ts` wraps the v090 entry; `index.ts` contains the canonical `before_agent_run` registration at priority `2000` when `preInferenceAdmission !== false`.
- GitHub source SHA-256 observations from the exact checkout: `v091-release-entry.ts` `a70b908fb31c2d6c2d36540b8ffda81f8c088de830c069e5dcae0a9b9709db86`; `index.ts` `6aa3726abfc412a019a92c6b4244ab82d6b79dd3abf82a06a4f0fa9f7983f333`.

## Installed artifact identity

- OpenClaw plugin inventory (`openclaw plugins list --json`) reports:
  - id: `cogentnexus-openclaw`
  - version: `0.9.5`
  - status: `loaded`
  - source: `C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw\dist\v091-release-entry.js`
  - rootDir: `C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw`
  - origin: `global`
  - hookNames: `[]`, hookCount: `0`
- Installed entry artifact byte SHA-256: `c15b2f61a1596f301510e9cd392851ef99427c6c129d653d2d336cfefa79b3a8`.
- The inventory is not process-scoped and its `hookCount=0` is explicitly insufficient to prove an effective dynamic registry; it is not used as proof of D or E.

## Running gateway PID

- `openclaw gateway status` identified the running Gateway as PID `17080`, state `Ready`, port `18789`, with connectivity probe `ok`.
- Service command: `C:\Program Files\nodejs\node.exe C:\Users\CDQ-P\AppData\Roaming\npm\node_modules\openclaw\dist\index.js gateway --port 18789`.
- Parent chain observed read-only: PID `17080` (`node.exe`) -> PID `14104` (`cmd.exe`) -> `C:\Users\CDQ-P\.openclaw\gateway.cmd`.
- Gateway executable SHA-256: `9a4eb5f1c29c6a2e93852ead46b999e284a6a5ca8bab4d4e241d587d025a52de`.

## Running-process identity

The PID is process-identified by OpenClaw's own Gateway status, command line, port, service command, and parent relationship. No process mutation was performed.

## Loaded module identity

**UNOBSERVABLE.** Windows process module inspection exposed only `node.exe`; it did not expose the JavaScript module URL/path or a `require.cache`/ES-module registry for PID `17080`. The installed plugin path and hash therefore cannot be bound to the running PID.

## Artifact SHA-256

- Installed entry file: `c15b2f61a1596f301510e9cd392851ef99427c6c129d653d2d336cfefa79b3a8`.
- Process-loaded CogentNexus artifact SHA-256: **UNOBSERVABLE**.
- Consequently, no exact process-scoped mismatch exists to prove D.

## Registration evidence

- Repository/source evidence: canonical registration chain exists; `v091-release-entry.ts` invokes the legacy registration boundary, and the source `index.ts` registers `before_agent_run` with priority `2000` under the admission configuration gate.
- Existing test-only effective-boundary diagnostic: `src/cnx348-effective-runtime-provenance.test.ts` records module URL, register invocation, hook identity, priority, and retained registry in a simulated OpenClaw-shaped loader. This is not evidence from PID `17080`.
- Live registration invocation metadata: **UNOBSERVABLE**.

## Effective hook registry evidence

- `openclaw plugins list --json`: `hookNames=[]`, `hookCount=0`; this is inventory metadata only and cannot establish the dynamic effective registry.
- Process-scoped effective registry for PID `17080`: **UNOBSERVABLE**.
- Process-scoped `before_agent_run` handler identity, owner, priority: **UNOBSERVABLE**.

## Dashboard path evidence

Static tracing shows the intended source path is:

`v091-release-entry.register` -> legacy `v091-final-entry`/`v090-final-entry` wrappers -> canonical `index.ts` `before_agent_run` admission registration; WebChat delivery adapters are separately registered for `webchat` context.

This does not establish an actual Dashboard/WebChat request reaching provider execution without `before_agent_run`. No UI interaction, semantic Dashboard request, replay, resend, or provider call was performed. Therefore E is **not proven**.

## Exact test commands

- `npm test -- --run src/cnx350-running-gateway-provenance.test.ts`
- Read-only inventory commands: `openclaw --version`; `openclaw gateway status`; `openclaw plugins list --json`.
- Read-only process inspection: `Get-CimInstance Win32_Process` for PID `17080` and its parent; `Get-Process -Id 17080` module listing.
- Read-only artifact hashing: `sha256sum C:/Users/CDQ-P/.openclaw/extensions/cogentnexus-openclaw/dist/v091-release-entry.js`.

## Fresh results

Focused test result: **BLOCKED**. Exact output:

`'vitest' is not recognized as an internal or external command, operable program or batch file.`

The repository test dependencies were not installed, because dependency installation is outside the CNX-350 read-only fence. No build or full test suite was claimed or run.

## Production changes

**NO**

## Hard-fence verification

- Production code change: none.
- Install/reinstall: none.
- OpenClaw restart: none.
- Provider routing/config/runtime mutation: none.
- Database mutation: none.
- UI interaction or semantic Dashboard request: none.
- CNX-344 replay/resend: none.
- `durableAdmissionEligible`, timeout authority, or admission ownership change: none.
- v0.9.5 tag/history mutation: none.
- Force-push/history rewrite: none.
- Self-acceptance: none.

## Smallest next probe

A separately authorized, read-only process diagnostic must expose the JavaScript module URL/cache identity and effective OpenClaw hook registry from the already-running Gateway process (or an equivalent authoritative runtime endpoint). If that boundary remains unavailable, D/E must remain UNRESOLVED; do not infer either result from inventory `hookCount=0` or from static tests.
