# CNX-20260907-307 — Activation safety contract TDD repair

## Disposition

`PASS_SOURCE_CONTRACT_GREEN__READY_FOR_EXACT_CANDIDATE_INSTALL_AND_MANAGED_ACTIVATION`

Task307 completed the source-only activation-safety repair. No live installer, activation, lifecycle, semantic, durable-state, protected-state, or release mutation occurred.

## Exact lineage and provenance

- authoritative pre-repair branch HEAD: `ee67094ff1700b4acbcc8ecc938511cae4570d96`
- genuine RED commit: `768c8507c51359a2d846c16e6bc5e81c999bf2fb`
  - tree: `22f58c5022ba69747776605734ad291df98bde99`
  - subject: `test: reproduce activation safety contract gaps`
- verified repair candidate: `853650ce7f59687fbce172bd96543a38f288e47a`
  - parent: `768c8507c51359a2d846c16e6bc5e81c999bf2fb`
  - tree: `3afb448e83b406dc0e51965d484dc72897494d83`
  - subject: `[verified] fix: fence activation authority paths`
- source plugin fingerprint after declared build: `9af4712dd3265afc577a233b4716279901b9eab1128ad6640c63e0ba846f0f33`
- version metadata remains `0.9.3`; no version/tag/release change was authorized by Task307.

## Root causes and repairs

1. **Composed Supervisor overlays ran before the bare-host quiescence guard.**
   - Added a state-free `supervisor_quiesced_result()` helper.
   - Both `host_provider_v092.supervisor_tick()` and `host_stall_v091.supervisor_tick()` now return `result=quiesced`, `action=none` before provider state, adapter, event, recovery, probe, claim, start, or restart work.
2. **Enable lease cleanup was not unconditional.**
   - Moved acquisition/ownership into an outer enable wrapper.
   - Every post-acquire exit now releases only the acquired owner/token in `finally`.
   - A release failure cannot mask the original in-flight exception; transactional behavior remains in the inner authority operation.
3. **Interrupted-Direct promotion lacked session lifecycle authority.**
   - Promotion now requires the production session schema, active state, non-negative generation (generation `0` is valid), non-null lifecycle identity, and bounded freshness evaluated at actual promotion time rather than enable-start time.
   - Missing/ambiguous schema or lifecycle evidence fails closed; no Ticket/session IDs or payload content are hardcoded or inspected.
4. **Pending assistant delivery could arm the startup worker globally.**
   - Both due selection and wake scheduling now join exact `owner_session_key` plus `owner_generation` to an active, identified, fresh session.
   - Stale/ambiguous delivery rows neither become due nor arm a wake timer. A fresh explicitly owned current-generation row remains deliverable.

## TDD and review evidence

The initial test-only RED produced four expected failures:

- composed production supervisor performed overlay state/provider work under a lease;
- a pre-transaction classifier exception retained the enable lease;
- stale/null-identity interrupted Direct Tickets were promoted;
- a stale pending assistant delivery remained due and scheduled.

Each slice was made GREEN with the smallest owning-boundary change. Additional review-driven RED cases proved and repaired:

- valid lifecycle generation `0` was initially rejected by an over-strict `>=1` predicate;
- freshness tied to enable start could become stale during a long activation and was moved to actual promotion time.

A full-suite fixture that had no production session/clock dependency failed after the contract tightened; it was corrected narrowly by seeding a fresh identified session and pinning the fixture clock. This was a test-fixture correction, not a product failure.

Independent pre-commit review cycle 1 found the generation-0 and freshness-clock defects. After RED→GREEN corrections, review cycle 2 returned:

```json
{"passed":true,"security_concerns":[],"logic_errors":[],"suggestions":[]}
```

The static secret-pattern scan matched the parameterized quiescence lease `token` field; inspection classified it as a false positive, not a credential. No dangerous shell/eval/pickle/formatted-SQL additions were found.

## Local validation

Final candidate results:

- focused activation/delivery suites: GREEN
- full Python suite: `253` tests, `1` skipped, GREEN
- full plugin suite: `61` files / `298` tests, GREEN
- `npm run plugin:validate`: build, schema, bootstrap, and package-content validation GREEN
- `npm run evaluation`: all gates true; evidence SHA-256 `076f3bd631724edba7a46413699b825f5063f713883d0c34b2981415458e2de5`
- `npm audit --omit=dev`: `0` vulnerabilities
- `git diff --check`: GREEN
- final candidate worktree: clean

## Exact-SHA GitHub Actions

All required runs completed successfully for candidate `853650ce7f59687fbce172bd96543a38f288e47a`:

| Workflow | Run | Result | URL |
|---|---:|---|---|
| Validate | `34137033103` | `completed/success` | https://github.com/funggier/CogentNexus-OpenClaw/actions/runs/34137033103 |
| PS5.1 Acceptance Smoke | `34137033075` | `completed/success` | https://github.com/funggier/CogentNexus-OpenClaw/actions/runs/34137033075 |
| Windows Installer Pack Smoke | `34137033014` | `completed/success` | https://github.com/funggier/CogentNexus-OpenClaw/actions/runs/34137033014 |

The preceding coordination SHA `ee67094ff1700b4acbcc8ecc938511cae4570d96` had Validate run `34130318411` fail in `v274-discord-receipt-lifecycle.test.ts` by timeout while its smoke siblings passed. The exact repair candidate's full local suite and fresh Validate run passed; the earlier failure is preserved rather than upgraded or hidden.

## Candidate changed paths and Git-object SHA-256

| Path | Git blob | Raw blob SHA-256 |
|---|---|---|
| `plugins/cogentnexus-openclaw/src/v091-direct-recovery.test.ts` | `2906d030430c462116b6a7c12c3f802e8767c04c` | `51ed2b2a123d2e3a73ecd5051e4471daf335aab9322002100aae39d7cb7f0613` |
| `plugins/cogentnexus-openclaw/src/v091-direct-recovery.ts` | `883f2662e8a377cecfc063ef7359768198bbde68` | `147b585fa435e0ddcc26734a3f5db4385d7b24f6377656ffd8c710dea586b1cb` |
| `skills/cogentnexus-openclaw/scripts/host_authority_v091.py` | `b21a3cbdcd223784a80d8c0fc47a237d133bc5a3` | `d819d0c8b99329acde8965ee63c64c9d3138e3cdf04aee62bf9fb1631bc04bf9` |
| `skills/cogentnexus-openclaw/scripts/host_provider_v092.py` | `74ffe648a61b9c94438a69c64d914c19f36cf597` | `d6c13750db37a29c258a1b11b0f5ea7b63e42a2535bfbe983a66fd9ad1c39cbf` |
| `skills/cogentnexus-openclaw/scripts/host_stall_v091.py` | `8aea81ef98dea502c33d771bbf021b1cfd54188f` | `421654e646594048494b83857dfc2f976adca7d9341912351fc9dca1081c09fd` |
| `skills/cogentnexus-openclaw/scripts/host_v091.py` | `85c8c1632d75092b13cb5315f44e8aabd9d0255c` | `a3e841d9bcc8e04a1ebfa3669368f5ab88c109d6e0bccb6bdc360ad31162009b` |
| `skills/cogentnexus-openclaw/scripts/supervisor_quiescence.py` | `33aed9736fbe52c1b5c61e9fa072fd4c79cdeea1` | `4e64ad27010b4b5a67e74e757b007b13cc1c106821ea9a80c5f8518c400f582f` |
| `tests/test_activation_safety_contract.py` | `69228c2aba31e9865bc58665384b91822d4ee3bd` | `28b2109c9737ec38e60dad0b48c852d386405bffa7816a5011a09eacf639821b` |
| `tests/test_host_v091_delivery_fence.py` | `2c60f2d21d96af3c5db4752931ac626d3dfd2507` | `fd26190c25b99896c453ad2f5905ec81346f35a02ab71d69b159f7ff3f6bf1da` |

## Tooling/anomaly register

- Two read-only report/task probes used guessed filenames and returned path-not-found; both were corrected from `ACTIVE.md` exact paths. No product state changed.
- A `git ls-remote origin` probe ran outside the repo and failed after the independent GitHub release query succeeded; it was rerun in the correct workdir.
- The shallow/no-tag clone lacked the historical `v0.9.3` target object; authoritative GitHub API verified commit `26ce64a624255278a3a0266ad38746e0e6ed2e31` and tag ref without repointing the checkout.
- The delayed cron record warned that the Hermes gateway was stopped, while the local scheduler later completed the read-only job. A separate bounded terminal observer independently provided the CI evidence. The cron record was removed after completion.

## Release provenance conflict

Authoritative GitHub state at `2026-09-07T15:15:02Z` showed public release/tag `v0.9.3` already exists at `26ce64a624255278a3a0266ad38746e0e6ed2e31`. The release workflow refuses duplicate publication, and candidate metadata remains `0.9.3`. Therefore Task307 does not attempt release; a later source/version successor must align a new version only after live acceptance.

## Safety accounting

```text
live installer/enable/lifecycle/scheduler/Gateway/provider mutation: 0
semantic send/Delete/cancel/replay/redelivery/disposition: 0
manual SQLite/Ticket/session/transcript/config mutation: 0
protected Ticket/session mutation: 0
release/tag/default-branch mutation: 0
force push: 0
```

## Successor

Task308 authorizes a bounded exact-candidate supported install and managed activation requalification. It requires pre/post byte and durable-state comparison, one installer invocation at most, one canonical enable invocation at most, and no semantic send or disposition.
