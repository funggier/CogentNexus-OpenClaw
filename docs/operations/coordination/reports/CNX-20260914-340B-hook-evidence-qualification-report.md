# CNX-340B — before_agent_run Hook Evidence Qualification

Status: `PASS — awaiting independent ChatGPT review`

## Provenance

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.6-hook-evidence-qualification`
- Tested candidate before this change: `30318c8e942317ce8da3a4794d5dd96f642b1861`
- Parent CNX-340A: `460a8cd661d02ba419cc1eff13c0efc721cfa928`
- Candidate artifact: `dist/v091-release-entry.js`
- Candidate artifact SHA-256: `c15b2f61a1596f301510e9cd392851ef99427c6c129d653d2d336cfefa79b3a8`
- Evidence test: `plugins/cogentnexus-openclaw/src/cnx340b-hook-evidence.test.ts`
- Evidence test SHA-256: `249a21fbd24b25e8d0fadafddbddc3db69559fec54c41c4e42b0cf2fc215b699`

## Source/provenance qualification

The source path was inspected and exercised as:

`v091-release-entry.ts` imports `legacyEntry` from `v091-final-entry.ts` → obtains `legacyEntry.register` → calls `register(runtimeApi)` → the legacy registration reaches `src/index.ts` canonical `api.on("before_agent_run", ...)` registration at source line 730.

The harness records the registration call stack, not merely source text, and identifies exactly one callback whose registration stack reaches `src/index.ts:730`.

## Executed harness evidence

The test creates a fresh temporary directory and an isolated SQLite database under that directory. It writes only a synthetic Host schema-v2 active controller fixture. It then registers the candidate `v091-release-entry` against an in-process API stub.

- `before_agent_run` registrations captured: 7 total plugin callbacks.
- Relevant canonical admission callback owner: exactly 1, identified by executed registration stack at `src/index.ts:730`.
- Callback invocation: exactly 1 explicit invocation.
- Event/context: synthetic eligible owner event, `senderIsOwner: true`, session `agent:main:owner`, run `cnx-340b-run`.
- Result: `{ outcome: "pass" }`.
- Admission evidence: isolated SQLite contains one Ticket with the synthetic run ID, owner session, prompt, and `status: "accepted"`; its event sequence is exactly `accepted`, `routed`.
- No duplicate/idempotency/retry/recovery/fallback/resend/manual dispatch was performed.
- Provider/model fence: API stub exposes provider/model methods that would throw and records calls; recorded provider/model calls: `[]`.

## Production-state and traffic fence

The harness uses `mkdtemp` and an isolated fixture database path. No production runtime DB, Dashboard/Web Session, controller, installation state, provider/model configuration, tag, or release history was accessed for mutation. No semantic/provider request, inference, delivery, or Dashboard traffic was created. The only controller used was the temporary synthetic fixture; no production controller was changed.

## Verification commands and results

| Command | Exit | Result |
|---|---:|---|
| `npx vitest run --config ./vitest.config.ts src/cnx340b-hook-evidence.test.ts` | 0 | 2 tests passed |
| `npm test` | 0 | 77 test files, 369 tests passed |
| `npm run plugin:build` | 0 | TypeScript build and v0.9.1 schema verification passed |
| `npm run plugin:validate` | 0 | Build, 9-table ticket bootstrap, and package-content verification passed; 248 packed files |

The build reproduced the candidate artifact SHA-256 listed above. No failure classification applies.

## Scope and stop condition

Only the CNX-340B evidence test and this report were added. This task did not modify production runtime logic, provider/model/configuration, controller, installation state, or release/tag history. The report is published for independent ChatGPT review; Hermes does not self-close or self-accept CNX-340B.
