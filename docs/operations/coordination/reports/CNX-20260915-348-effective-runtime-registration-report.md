# CNX-348 — Effective Runtime Registration Provenance Report

**Result token: `BLOCKED_GREEN_UNRESOLVED`**

## Authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-348-effective-runtime-registration`
- Remote baseline verified before work: `c636eb4512d2d49f91387cbba61f3b5be6340241`
- Parent CNX-347: `7c563592625f71c817cc38649caa1047a7efb746`
- Investigation commit: published with this report; verify the final remote SHA from GitHub.

## Scope and safety

This was an evidence-only investigation. No production source was changed. No OpenClaw installation, restart, provider routing, runtime/config/database state, UI, or semantic Dashboard request was used. CNX-344 was not replayed or resent. No v0.9.5 tag/history was touched and no force-push was used.

## Harness

Added `src/cnx348-effective-runtime-provenance.test.ts`. The harness loads the actual `v091-release-entry` module through an OpenClaw-shaped loader boundary, invokes its public `register(api)` once, retains registrations in an effective host hook registry, and observes registration timing and wrapper activity through the API surface. It does not call the canonical admission handler in isolation.

The harness records/asserts:

- loaded module identity (`import.meta.url`, source `src` directory, and test-bound module identity);
- one release-entry invocation;
- observable wrapper-chain activity through `api.on` and `api.registerService` calls;
- `before_agent_run` registration at priority `2000`;
- one retained canonical admission handler and its function identity;
- synchronous/Promise registration shape and `register.observable` timing marker;
- effective plugin configuration (`preInferenceAdmission=true`, `ticketFirst=true`);
- Host authority fixture (`schemaVersion=2`, `cnxMode=active`), Dashboard context, and `senderIsOwner=true`;
- unchanged controller-file SHA-256 after registration;
- invocation of the retained handler, which returned the expected Ticket-admission block for an eligible Dashboard-shaped prompt;
- effective registry visibility after the loader boundary.

The test also includes an intentional negative control: a loader that bypasses `register()` is required to fail the effective-admission visibility assertion with `effective admission visibility=0`. This demonstrates that the harness detects a broken registration boundary rather than merely proving that the current source can be imported.

## TDD evidence

The initial focused run was RED before any production edit. It showed:

- current-path assertion mismatch because the first probe prompt was not admission-eligible; and
- the intentional bypass control correctly produced `effective admission visibility=0`.

The prompt assertion was corrected in the test-only harness to use the existing eligible multi-phase fixture. No production code was changed.

## Fresh verification

Exact commands and results:

```text
npm test -- --run src/cnx348-effective-runtime-provenance.test.ts
  PASS — 1 file, 2 tests

npm test -- --run src/cnx347-registration-boundary.test.ts src/v091-wiring.test.ts
  PASS — 2 files, 6 tests

npm run build
  PASS — TypeScript build and dist canonicalization

npm test
  PASS — 78 files, 370 tests
```

## Classification

The evidence is GREEN for the repository/test-shaped effective registration path:

- A: not supported by this harness; release entry was invoked once.
- B: not supported by this harness; registration reached the canonical hook.
- C: not supported by this harness; the simulated effective registry retained and invoked the hook.
- D: not proven; this environment does not establish the artifact/module loaded by the already-running OpenClaw process. The test proves the repository module identity only.
- E: not tested; no live Dashboard execution path or UI/semantic request was used.
- F: not supported by this harness; the effective fixture is admission-enabled and the retained hook blocks the eligible request.

Therefore CNX-344's live divergence remains **unresolved / BLOCKED**. The next boundary is runtime artifact/process provenance and the actual Dashboard execution-path hook invocation, using read-only evidence from the authorized runtime environment. A repair task is not justified by this result.

## Production-change and mutation declaration

Production behavior changed: **No**. Changed files are test/report only. There was no live/UI/provider/runtime/database mutation, no installation/reinstallation, no restart, and no semantic Dashboard request.
