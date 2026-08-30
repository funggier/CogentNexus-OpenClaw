# CNX-20260831-168 — Hermes/Codex Task-167 Verification Completion

## 1. Disposition

**REWORK_REQUIRED**

The Task-167 repair passes all completed local validation and the two completed required workflow gates, and the exact candidate lineage/change fence is correct. Final Task-168 acceptance cannot be marked `PASS` because the required exact-SHA GitHub `Validate` run `33330458434` concluded `cancelled`; its Windows pytest and subsequent validation steps were cancelled rather than completed. No production source change, CI rerun, live mutation, or semantic Send was authorized or performed in this task.

This is an evidence/CI completion boundary, not evidence of a newly discovered product contradiction. A separately authorized CI-completion or review decision is required before Task 167 can be accepted.

## 2. Objective and acceptance contract

- Task ID: `CNX-20260831-168`
- Task path: `docs/operations/coordination/tasks/CNX-20260831-168-hermes-task167-verification-completion.md`
- Objective: complete the mandatory validation, exact-SHA workflow inspection, risk analysis, acceptance matrix, and Reviewer Verification Packet for Task-167 repair SHA `231761fca24c315e90536955d3e384f55e2e232e`, without changing the product candidate or mutating live state.
- Reviewed product candidate: `231761fca24c315e90536955d3e384f55e2e232e`
- Required disposition rule: a required exact-SHA workflow that is pending, cancelled, skipped unexpectedly, or failed prevents `PASS`.

Task-168 hard fences were binding: no Dashboard semantic Send, no `chat.inject`, no live OpenClaw/Gateway/Ollama/Supervisor mutation, no install-over/uninstall/reinstall/reset, no manual Ticket/database/transcript/delivery mutation, no dependency or upstream upgrade, no production source edit merely to improve acceptance, no release/merge, and no force push.

## 3. Authority and starting state

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`
- Fresh remote HEAD at task start: `7b934b9a39ffbfe10242315aa40e17d5e8c02859`
- Exact detached validation worktree: `C:/Users/CDQ-P/AppData/Local/Temp/cnx-cont-20260830T192219Z/candidate-231761f`
- Exact candidate HEAD: `231761fca24c315e90536955d3e384f55e2e232e`
- Candidate parent: `5b481ff1c5d64e40f9a87ff792599c63cfcf84a9`
- Pinned OpenClaw source read-only SHA: `0790d9f593ad30c940ed93b5872a8cf6d6f3cf8c` (`2026.7.1-2`)
- Task-167 review: `docs/operations/coordination/reviews/CNX-20260831-167-hermes-native-delivery-staging-root-cause-repair-review.md`
- Task-167 prior report: `docs/operations/coordination/reports/CNX-20260831-167-hermes-native-delivery-staging-root-cause-repair.md`

The current coordination tip contains Task-168 coordination state; it was not treated as a product candidate. Validation was performed from the detached Task-167 repair SHA.

The fresh candidate worktree was clean before and after validation. Build/package outputs and `node_modules` remained untracked/ignored temporary validation state and were not committed.

## 4. Candidate lineage and changed-file scope

Exact `git diff-tree --name-status` from Task-167 base to repair SHA:

```text
A docs/operations/coordination/reports/CNX-20260831-167-hermes-native-delivery-staging-root-cause-repair.md
M plugins/cogentnexus-openclaw/src/v091-dashboard-verified-delivery.ts
A plugins/cogentnexus-openclaw/src/v167-native-delivery-staging-order.test.ts
```

No dependency manifest, lockfile, OpenClaw source, installer, runtime, or unrelated product file is in the Task-167 repair diff.

Source hashes captured from the exact candidate worktree:

```text
5f21d2beb760c823387f1cb5fd71f8b10e1040a4876e08e4c347c1413ed0bd33  plugins/cogentnexus-openclaw/src/v091-dashboard-verified-delivery.ts
af4a52c6eb4f0b3c7e22a41c6abd5669c7fe2f795ddb74f44292a5e5037bec4b  plugins/cogentnexus-openclaw/src/v167-native-delivery-staging-order.test.ts
```

The Task-167 change is therefore a three-file report/source/test repair surface with exact parent lineage and no adjacent drift.

## 5. Task-167 repair and causal conclusion

Task 166 showed a visible exact assistant response but no durable direct-result row or marker. Task 167 traced the pinned OpenClaw lifecycle and demonstrated that the prior implementation learned the final candidate at `before_agent_finalize`, after the native `before_message_write` opportunity. The repair resolves the unique accepted direct Dashboard Ticket from `owner_session_key` at the pre-write hook, stages the exact text, injects the deterministic marker before native append, and settles only from the post-persistence transcript event.

The production-shaped Task-167 test models:

```text
before_message_write -> native transcript update -> before_agent_finalize
```

The pre-repair RED failed because the native assistant text lacked the delivery marker. The repaired GREEN verifies marker-bearing persistence, one durable direct-result row, delivery confirmation, and completed Ticket state.

### Alternatives and contradictions

- Keeping candidate discovery only in `before_agent_finalize` was rejected because pinned upstream ordering and Task-166 evidence place it after the native write boundary.
- Treating `reply_dispatch` or a visible UI response as durable persistence was rejected because neither independently proves native transcript commit.
- Broadly binding any assistant message in a Dashboard session was rejected; the repair requires exactly one eligible accepted direct Ticket and refuses ambiguity.
- Patching OpenClaw upstream was not permitted and was not needed for the proposed repair.
- The only material contradiction/anomaly found in this checkpoint is workflow-level cancellation of the exact-SHA `Validate` run. Completed local and CI steps did not contradict the repair.

## 6. Required local validation

All commands below ran against the detached exact candidate SHA `231761fca24c315e90536955d3e384f55e2e232e`.

| Requirement | Exact command | Result |
|---|---|---|
| Task-167 production-faithful regression | `./node_modules/.bin/vitest run src/v167-native-delivery-staging-order.test.ts` | PASS |
| Task-162 transcript authority regression | `./node_modules/.bin/vitest run src/v162-dashboard-transcript-authority.test.ts` | PASS |
| v091 verified-delivery regression | `./node_modules/.bin/vitest run src/v091-dashboard-verified-delivery.test.ts` | PASS, 11 tests |
| Duplicate/no-regeneration/recovery set | v090/v091 recovery, restart, delivery-continuity tests | PASS |
| Related regression set | v167 + v162 + v091 + v090 restart + delivery continuity | PASS, 5 files / 34 tests |
| Full plugin test suite | `./node_modules/.bin/vitest run` | PASS, 53 files / 273 tests |
| TypeScript no-emit | `./node_modules/.bin/tsc --noEmit` | exit 0 |
| Official build | `npm run build` | exit 0 |
| Plugin/schema/package validation | `npm run plugin:validate` | exit 0; schema PASS, DB bootstrap PASS, packed package 184 files |
| Baseline consistency | `python scripts/check_baseline_consistency.py` | PASS, Bridge v0.9.3 |
| Full Python suite | `uv run --no-project --with-requirements requirements-dev.txt python -m pytest -q` | PASS, 499 passed / 5 skipped / 4 subtests |
| Evaluation gates | `npm run evaluation` | `passed: true`; integrity, interruption, retry, duplication, retrieval, provenance, latency gates true |

The first plain `python -m pytest -q` invocation failed only because the Hermes Python environment did not have pytest installed (`No module named pytest`). Per the coordination procedure, the corrected ephemeral `uv` invocation used the repository's existing `requirements-dev.txt` without modifying project dependency files and passed the full suite.

## 7. Exact-SHA GitHub workflow results

Fresh GitHub CLI/API state for commit `231761fca24c315e90536955d3e384f55e2e232e`:

| Workflow | Run ID | Final status | Conclusion | Evidence |
|---|---:|---|---|---|
| PS5.1 Acceptance Smoke | `33330458475` | completed | success | [run](https://github.com/funggier/CogentNexus-OpenClaw/actions/runs/33330458475) |
| Windows Installer Pack Smoke | `33330458470` | completed | success | [run](https://github.com/funggier/CogentNexus-OpenClaw/actions/runs/33330458470) |
| Validate | `33330458434` | completed | cancelled | [run](https://github.com/funggier/CogentNexus-OpenClaw/actions/runs/33330458434) |

The cancelled Validate run had successful package dry-run, Ubuntu 3.11/3.14, macOS 3.11/3.14, and initial Windows validation steps. The Windows 3.11/3.14 jobs reached the pytest step and then were cancelled; later Windows checks were skipped. The run therefore cannot be converted into a successful full Validate result by inference.

No CI rerun was requested or performed in Task 168. No source edit was made to affect CI. The cancelled exact-SHA run remains the blocking evidence gap.

## 8. Risk, crash-window, duplicate, and ambiguity analysis

### Session-key fallback ownership

The fallback does not accept an arbitrary assistant write. It requires:

1. `ctx.sessionKey` to be present;
2. the session to be a Dashboard session according to the existing Dashboard predicate;
3. exactly one Ticket whose `owner_session_key` equals that session key;
4. Ticket status `accepted`;
5. `workflow_eligible=0`; and
6. `workflow_id IS NULL`.

The query limits to two rows and refuses when the result is zero or greater than one. It then passes the selected Ticket's stored `run_id` into the existing `stageDashboardDirectResult`, which rechecks the Ticket and session authority inside its writable transaction. This prevents binding an assistant write to an unrelated session or an ambiguous concurrent Ticket under the tested schema assumptions.

Residual uncertainty: this is a bounded unique-session fallback, not a host-provided atomic run ID. If a host permits multiple same-session direct Tickets concurrently, the repair deliberately refuses to stage; it does not guess. A future upstream contract carrying run identity at pre-write would reduce this ambiguity further.

### Zero or multiple eligible Tickets

- Zero eligible accepted direct Dashboard Tickets: no candidate is created, no staging occurs, and the message is left unchanged.
- More than one eligible Ticket: no candidate is selected, no staging occurs, and the system remains fail-closed.
- One eligible Ticket: the stored `run_id` is used, the staging function revalidates ownership/session state, and the idempotency key is derived from Ticket ID plus owner generation.

### Crash after staging/claim but before native append

The durable row and claim may exist while the native message is absent. This is an intentional durable-first boundary. Recovery must not regenerate an inference while native ownership is active; the existing direct-result row is the exact answer to deliver/reconcile. If the claim expires or the host delivery path resumes, idempotency key and marker/history dedupe prevent a second semantic result. Residual uncertainty is limited to host-side recovery convergence, which is not exercised by this repository-only task.

### Crash after native append before transcript settlement

The native message can be persisted with the marker while the transcript-update callback is delayed or lost. The durable row remains pending and can be reconciled by the existing marker/history host delivery path. A duplicate transcript event is a no-op through the existing status/idempotency checks. If settlement is not observable by the deadline, the existing fail-closed recovery policy refuses regeneration rather than emitting a competing answer.

### Host recovery and marker/history dedupe

The repair preserves `cnx_assistant_delivery` idempotency keys, claim leases, marker matching, and the native-owned recovery fence. Recovery does not delegate to legacy regeneration while a pending native direct-result row or native-owned run exists. The full plugin suite and evaluation gates passed the existing duplication, retry, interruption, and recovery coverage, but those tests are not a substitute for a real post-install/live acceptance.

### Post-write finalize behavior

`before_agent_finalize` can still observe the final candidate after the pre-write path. The transcript callback settles and deletes the in-memory candidate after a marker-bearing post-persistence event. A later finalize event may create a short-lived candidate again, but `stageDashboardDirectResult` sees the already-settled/non-accepted Ticket and refuses a second row. It cannot overwrite the completed delivery state through the accepted/direct staging path. This is covered by the existing idempotency and terminal-state guards; a full cross-event ordering stress test remains residual evidence.

### Liveness tradeoff

The repair can refuse delivery when session ownership is ambiguous or when the post-persistence receipt cannot be observed. This may leave a result pending until host reconciliation or eventually fail closed. That is an intentional liveness tradeoff for exactly-once/duplicate safety. No recovery regeneration is used to mask missing proof.

## 9. Acceptance matrix

| Criterion | Verdict | Exact evidence |
|---|---|---|
| Validate exact Task-167 repair lineage | PASS | Detached HEAD `231761f...`; parent `5b481ff...`; exact three-file diff |
| Preserve pinned OpenClaw boundary | PASS | Read-only upstream SHA `0790d9f...`; no upstream file in diff |
| Task-167 production-faithful RED/GREEN | PASS | `v167-native-delivery-staging-order.test.ts`; pre-repair missing-marker RED; repaired GREEN |
| Task-162 authority regression | PASS | `v162-dashboard-transcript-authority.test.ts` passed |
| v091 delivery and duplicate/recovery regressions | PASS | 34/34 related tests passed; full plugin 273/273 passed |
| Full TypeScript validation | PASS | `tsc --noEmit` exit 0 |
| Official build | PASS | `npm run build` exit 0 |
| Plugin/schema/package validation | PASS | `npm run plugin:validate`; schema/DB/package checks passed; 184 packed files |
| Baseline consistency | PASS | `python scripts/check_baseline_consistency.py`; Bridge v0.9.3 PASS |
| Full Python validation | PASS | 499 passed, 5 skipped, 4 subtests passed via ephemeral uv |
| Evaluation gates | PASS | `npm run evaluation`; `passed=true`, all listed gates true |
| Exact-SHA PS5.1 workflow | PASS | Run `33330458475`, completed/success |
| Exact-SHA Windows Installer Pack workflow | PASS | Run `33330458470`, completed/success |
| Exact-SHA Validate workflow | UNPROVEN | Run `33330458434`, completed/cancelled; Windows pytest and later checks cancelled |
| Required crash-window/duplicate/ambiguity analysis | PASS | Sections 8 and 9 of this report; bounded fallback and fail-closed behavior stated |
| Required Reviewer Verification Packet | PASS | Section 10, six critical claims with independent checks |
| No live semantic/runtime mutation | PASS | Zero Dashboard Send, zero install/lifecycle/live DB actions |
| Final Task-168 `PASS` eligibility | FAIL | Task contract rejects PASS while required exact-SHA Validate is cancelled |

Because the exact-SHA Validate criterion is `UNPROVEN`, the overall disposition is `REWORK_REQUIRED`, not `PASS`.

## 10. Reviewer Verification Packet

| # | Critical claim | Why it matters | Exact evidence | Narrow independent ChatGPT check |
|---:|---|---|---|---|
| 1 | Task-167 repair is the exact candidate under review and has no adjacent product drift | Prevents validating a different or broadened candidate | Candidate SHA `231761f...`; parent `5b481ff...`; exact three-file `git diff-tree` in Section 4 | Run `git show --stat 231761f...` and compare the three paths against Section 4 |
| 2 | The production-shaped regression passes after the pre-write staging repair | Directly tests the causal boundary from Task 166 | `src/v167-native-delivery-staging-order.test.ts`; full Vitest 53/273 pass | Run the single v167 test and inspect marker, durable row, delivered state, and completed Ticket assertions |
| 3 | All required local plugin/Python/build/package checks pass | Establishes source/package correctness independent of CI | Section 6 commands/results; evaluation `passed=true`; Python 499/5 | Re-run `npm run plugin:validate`, baseline checker, and ephemeral pytest from exact SHA |
| 4 | The fallback refuses ambiguous session ownership | Prevents wrong-Ticket durable binding | `dashboardTicketForSession` implementation and Section 8 analysis; query requires exactly one row | Inspect the helper and add/run a two-eligible-ticket fixture or equivalent focused test |
| 5 | Duplicate/recovery safety remains fail-closed | Prevents a crash or late callback from producing a second semantic answer | Existing v090/v091 recovery/continuity tests, full suite, and Section 8 crash-window analysis | Inspect `stageDashboardDirectResult`, `settleDashboardNativeDelivery`, and recovery fence for idempotency/status guards |
| 6 | Task 168 cannot be accepted as PASS yet because required Validate is cancelled | Prevents overstating incomplete CI as success | GitHub run `33330458434`, final `completed/cancelled`; jobs `99307984962` and `99307984978` cancelled at pytest | Run `gh run view 33330458434 --json status,conclusion,jobs` and require every required run to be completed/success |

## 11. Anomalies and residual uncertainty

- The first lineage probe used an expected SHA with one extra trailing character and exited before producing output. The corrected exact-SHA check passed; no repository or runtime state was changed.
- Plain executor `python -m pytest -q` lacked pytest. The corrected ephemeral uv command passed the full suite. This is recorded as a setup miss, not a product failure.
- GitHub Validate was cancelled after substantial successful work. Cancellation is not treated as success, and no source change or CI rerun was used to hide it.
- npm dependency installation emitted the existing deprecation/vulnerability notices. No dependency upgrade or `npm audit fix` was run.
- The repository test harness proves the registered plugin boundary and storage semantics, not a new real Windows install or live Dashboard acceptance. Those remain intentionally unproven under Task-168 hard fences.
- Session-key fallback safety is bounded by the unique eligible-ticket query; exact run identity at the pre-write host boundary remains a residual architectural limitation.

## 12. Hard-fence compliance

Authorized effects:

- Created one detached source worktree outside the live runtime.
- Installed existing lockfile dependencies into the temporary worktree with `npm ci --ignore-scripts`.
- Generated temporary build/package artifacts inside the detached worktree.
- Created this verification report only after validation and remote race-check.

Prohibited effects performed: **none**.

Counts:

- Dashboard semantic Send: `0`
- Other live semantic OpenClaw input: `0`
- `chat.inject`: `0`
- Live Gateway/Ollama/Supervisor/OpenClaw mutation: `0`
- Install-over/uninstall/reinstall/reset: `0`
- Manual live Ticket/workflow/result/outbox/delivery/database/transcript mutation: `0`
- Dependency upgrade: `0`
- OpenClaw patch: `0`
- Production source edit in Task 168: `0`
- Force push/merge/release/tag/promotion: `0`

## 13. Residual unproven items

1. Exact-SHA GitHub `Validate` workflow completion; run `33330458434` is cancelled.
2. Full Windows matrix steps after the cancelled pytest boundary in that run.
3. Real install-over provenance/health for the Task-167 repair candidate.
4. Real Dashboard one-shot durable reacceptance after installation.
5. Stress behavior under concurrent same-session direct Tickets; current repair intentionally refuses ambiguity.
6. Native host behavior when the transcript-update receipt is lost after a marker-bearing append; repository guards are present, but no live acceptance was authorized.

## 14. Recommended successor gate

First obtain an independently reviewed CI-completion decision for the cancelled exact-SHA Validate run or a separately authorized exact-SHA validation run, without changing the product candidate. If all required CI evidence becomes successful and ChatGPT accepts this packet, open a separate Windows install-over/provenance/health checkpoint for exact repair SHA `231761f...`. Do not perform install-over or Dashboard semantic testing under Task 168.

## 15. Publication state

This report is the only intended Task-168 repository addition. It must be published as a report-only commit after the remote race check, with the final report blob and changed-path scope read back from GitHub.
