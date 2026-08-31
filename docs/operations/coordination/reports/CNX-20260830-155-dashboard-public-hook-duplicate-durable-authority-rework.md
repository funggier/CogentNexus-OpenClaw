# CNX-20260830-155 — Dashboard Public-Hook Duplicate Durable-Authority Rework

## Verdict

`PASS`

Task 155 completed the authorized offline RED → minimal GREEN → exact-SHA verification rework. The duplicate public-hook final path now re-enters the durable authority on every qualifying callback while ownership side effects remain single-shot. No live Windows/runtime mutation and no Dashboard semantic Send occurred.

## Authority and scope

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`
- Task: `CNX-20260830-155`
- Execution mode: `OFFLINE_REPOSITORY_TDD_PUBLIC_HOOK_DUPLICATE_DURABLE_AUTHORITY_REWORK`
- Accepted predecessor: Task 154 independent disposition `REWORK`
- RED parent: `232bc2ce3975e076de4214e4742f4a712a3966bb`
- Production repair SHA: `1ec8cfc81b8a21a178200c33816427f9abfd31b9`

The task fence prohibited Dashboard interaction/semantic transport, live Windows/runtime mutation, lifecycle/install/reset/uninstall/reinstall actions, manual semantic/database/plugin/controller mutation, OpenClaw source patching, dependency upgrades, merge/tag/release, and force push. Those fences were preserved.

## Blocking defect carried from Task 154 review

The Task-154 public fallback contained this ownership guard in `reply_payload_sending`:

```ts
if (kind !== "final") return;
if (fallback.owned) return;
```

That guard was unsafe because `fallback.owned` meant the first qualifying final had already been durably staged, but a later qualifying public-hook callback for the same run could still occur. Returning early skipped `stageDashboardDirectResult(...)`, which is the durable authority that both reuses the generation-bound idempotency row and rejects text drift.

The resulting defect had two concrete branches:

1. **Repeated same text** — the second callback returned no rewritten payload, so the durable marker was not reasserted at the public pre-delivery boundary even though the durable row already existed.
2. **Repeated changed text** — the second callback never reached the existing durable text-mismatch check, so the callback did not fail closed.

This was a narrow ownership/durable-authority ordering defect, not a SQLite insertion defect, run-correlation defect, final-payload filter defect, or append-capable-path defect.

## TDD — genuine RED before production repair

### Test-only RED commit

`232bc2ce3975e076de4214e4742f4a712a3966bb` — `test: expose public-hook duplicate durable authority gap`

Only the regression file changed:

`plugins/cogentnexus-openclaw/src/v154-dashboard-public-hook-fallback.test.ts`

The RED strengthened the public-hook fallback contract to require:

- a second same-text `reply_payload_sending` callback to return the exact same marker-bearing durable native text;
- only one `cnx_assistant_delivery` durable row;
- only one settlement waiter (`waitForIdle` call count `1`);
- a second changed-text final for the same run/generation to throw `durable Dashboard result changed`;
- durable row count to remain `1` after the changed-text rejection.

### Exact RED CI evidence

- Exact RED SHA: `232bc2ce3975e076de4214e4742f4a712a3966bb`
- Validate workflow: `33292884867`
- Ubuntu/Python 3.11 job: `99207499738`
- Job result: `failure` in `npm test`

The failure was limited to the strengthened Task-155 assertions in `src/v154-dashboard-public-hook-fallback.test.ts`; the predecessor `src/v091-dashboard-verified-delivery.test.ts` suite still passed `11/11`.

The two intended RED failures were:

1. `reuses the durable marker for a repeated same-text public-hook final without a second waiter`
   - expected the existing marker-bearing `CNX-V154-ACK ... <!-- cogentnexus-openclaw-delivery:... -->`
   - received `undefined`
   - assertion location: line 92
2. `fails closed when a repeated public-hook final changes durable text`
   - expected the callback to throw
   - callback returned without throwing
   - assertion location: line 180

Run totals at the RED boundary were `1 failed | 50 passed` test files and `2 failed | 269 passed` tests.

This establishes a genuine behavior-specific RED before the production edit.

## Minimal GREEN production repair

### Production commit

`1ec8cfc81b8a21a178200c33816427f9abfd31b9` — `fix: preserve durable authority on repeated public-hook finals`

GitHub compare from the RED parent to the repair shows exactly one production file changed:

`plugins/cogentnexus-openclaw/src/v091-dashboard-verified-delivery.ts`

Delta size: `6 additions`, `4 deletions`, `10 changes`.

The repair is deliberately narrow:

1. remove `if (fallback.owned) return;`;
2. compute `const firstOwnership = !fallback.owned;`;
3. keep every qualifying final routed through `stageDashboardDirectResult(...)`;
4. keep worker pulse/log ownership effects inside `if (firstOwnership)`;
5. retain the pre-existing `if (!fallback.waiterStarted)` gate for settlement waiter creation;
6. continue returning `staged.nativeText`, so both first and repeated same-text callbacks receive the durable marker-bearing payload.

The existing `stageDashboardDirectResult(...)` durable authority remains unchanged. Its generation-bound idempotency key is reused for the same text, while an existing row with different text throws:

`durable Dashboard result changed for <ticket> generation <generation>`

Therefore the fix restores durable authority on duplicate callbacks without creating a second durable row or a second settlement owner.

## Duplicate-path acceptance evidence

### Same-text marker reuse

The strengthened regression now requires the second same-text callback to return exactly the first callback's `durableNativeText`, including the CogentNexus delivery marker.

On repair SHA `1ec8cfc81b8a21a178200c33816427f9abfd31b9`, the Task-155 regression file passed `2/2` inside the full plugin suite.

The same test also proves:

- durable direct-result row count remains `1`;
- `waitForIdle` call count remains `1` before settlement;
- after the controlled idle release, normal delivery settlement can complete without duplicate durable ownership.

### Changed-text fail-closed

The second regression invokes a repeated final for the same run/generation with changed text and requires:

```text
durable Dashboard result changed
```

The repair no longer returns early on `fallback.owned`; it re-enters `stageDashboardDirectResult(...)`, so the durable row's existing text is compared and drift throws before native rewrite/delivery can proceed.

The durable row count remains `1`.

### Single waiter / pulse ownership

The regression directly asserts one `waitForIdle` call. Source inspection additionally shows the worker pulse and ownership log are guarded by `if (firstOwnership)`, while the existing settlement waiter remains guarded independently by `if (!fallback.waiterStarted)`.

Repeated durable re-observation therefore does not create a second ownership pulse/waiter sequence.

### Append-capable path preservation

The repair commit changes only the `reply_payload_sending` public-hook fallback block. The existing append-capable `reply_dispatch` path is outside the changed hunk and was not modified.

The related predecessor delivery suite `src/v091-dashboard-verified-delivery.test.ts` passed `11/11` on the repair SHA, while the full plugin suite also passed.

## Verification

### Focused and related regression evidence

Exact repair SHA:

`1ec8cfc81b8a21a178200c33816427f9abfd31b9`

Representative exact Validate job: macOS/Python 3.14 job `99207897243`.

- `src/v154-dashboard-public-hook-fallback.test.ts`: `2 tests` — PASS
- `src/v091-dashboard-verified-delivery.test.ts`: `11 tests` — PASS
- full plugin test files: `51 passed (51)`
- full plugin tests: `271 passed (271)`
- Python suite in that job: `469 passed, 33 skipped, 4 subtests passed`

### Build / evaluation / plugin / package validation

The exact repair Validate matrix passed all required repository/plugin gates. Representative job evidence includes:

- `npm ci` — PASS
- `npm test` — PASS
- `npm run evaluation` — PASS
  - includes `npm run build`
  - TypeScript build command `tsc -p tsconfig.json` — PASS
- `npm audit --omit=dev` — PASS, `found 0 vulnerabilities`
- `npm run plugin:validate` — PASS
  - plugin build / TypeScript build — PASS
  - mixed-plugin/schema artifact verification — PASS
  - ticket DB bootstrap — PASS (`9 required tables + v095 registration fence`)
  - package-content verification — PASS (`packedFileCount: 180`)

The Validate `package dry-run (no publish)` job `99207897292` also passed:

- v0.9.3 metadata verification;
- built plugin payload validation;
- payload-v2 identity computation;
- release archive build and verification without publishing;
- exact package provenance recording;
- package-proof artifact retention.

### `git diff --check`

The execution container could not resolve `github.com` for a direct local clone, so no claim is made that a network clone succeeded.

GitHub compare proved the repair is exactly one commit ahead of the RED parent and modifies only `v091-dashboard-verified-delivery.ts`. The exact changed hunk was fetched from both GitHub SHAs, reconstructed offline, and checked with literal `git diff --check`.

Result:

```text
EXIT=0
```

No whitespace error was reported in the complete production delta (`6 additions`, `4 deletions`).

## Exact-SHA GitHub Actions

All required workflows for production repair SHA `1ec8cfc81b8a21a178200c33816427f9abfd31b9` completed successfully:

| Workflow | Run | Result |
|---|---:|---|
| Validate | `33293037351` | `success` |
| PS5.1 Acceptance Smoke | `33293037346` | `success` |
| Windows Installer Pack Smoke | `33293037362` | `success` |

The Validate run includes Ubuntu, macOS, and Windows across Python 3.11/3.14 plus the package dry-run, all successful.

## Acceptance-contract review

- genuine RED before production repair: **PASS**
- second same-text public-hook final returns marker-bearing durable payload: **PASS**
- same-text repeat keeps one durable row: **PASS**
- changed-text repeat reaches durable authority and fails closed: **PASS**
- changed-text rejection keeps one durable row: **PASS**
- only one settlement waiter: **PASS**
- ownership pulse remains first-ownership-only: **PASS**
- append-capable path unchanged: **PASS**
- full plugin tests: **PASS**
- TypeScript build/evaluation: **PASS**
- plugin validation / DB bootstrap / package-content verification: **PASS**
- package dry-run/provenance verification: **PASS**
- exact production delta `git diff --check`: **PASS**
- exact-SHA Validate / PS5.1 / installer smoke: **PASS**

## Files / commits

Regression:

- `plugins/cogentnexus-openclaw/src/v154-dashboard-public-hook-fallback.test.ts`
- RED commit: `232bc2ce3975e076de4214e4742f4a712a3966bb`

Production:

- `plugins/cogentnexus-openclaw/src/v091-dashboard-verified-delivery.ts`
- repair commit: `1ec8cfc81b8a21a178200c33816427f9abfd31b9`

Report:

- `docs/operations/coordination/reports/CNX-20260830-155-dashboard-public-hook-duplicate-durable-authority-rework.md`

## Safety / side effects

During Task 155 continuation/reporting:

- Dashboard semantic Sends: `0`
- Dashboard click/focus/type/paste actions: `0`
- live Windows/runtime mutations: `0`
- install/reset/uninstall/reinstall invocations: `0`
- manual Ticket/outbox/delivery/database mutations: `0`
- OpenClaw source patches: `0`
- dependency upgrades: `0`
- merge/tag/release operations: `0`
- force pushes: `0`

## Conclusion

`PASS`

The Task-154 review blocker is repaired offline. Repeated public-hook finals no longer bypass durable authority: same-text repeats reuse the exact marker-bearing durable payload without duplicating ownership, while changed-text repeats fail closed through the existing durable mismatch check. The append-capable predecessor path remains untouched and the exact repair SHA is fully green in the required GitHub workflows.

Phase P is **not** declared accepted by Task 155. Publish this report and stop for independent review. No repaired Windows install-over, runtime mutation, or Dashboard semantic reacceptance is authorized by this task.
