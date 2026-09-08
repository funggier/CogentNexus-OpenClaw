# CNX-20260904-244 — Hardened-Runner Exact-Candidate Windows Install-Over Requalification

## Status
`READY_FOR_HERMES`

## Purpose
Run one bounded live Windows install-over requalification of the accepted exact executable candidate, using a freshly regenerated and freshly qualified hardened Scheduled Task runner. This task authorizes installer execution only; semantic sends remain forbidden.

## Authority
- Repo: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`
- Parent: `CNX-20260904-243`
- Installer evidence parent: `CNX-20260904-241`
- Runner forensic parent: `CNX-20260904-242`
- Umbrella: `CNX-20260831-188`
- Reviewed Task-243 report HEAD: `ad94e992fec3cbf414bf82a3dd5073b229e6b5b8`
- Accepted Task-243 review verdict: `ACCEPT_PASS_HARDENED_RUNNER_FUNCTIONALLY_QUALIFIED__PRECREATE_REGISTRATION_CORRECTION_ACCEPTED__RUNNER_SHA_REPORT_GAP_NONBLOCKING_WITH_FRESH_REGENERATION_GATE__SEPARATE_BOUNDED_INSTALLER_REQUALIFICATION_AUTHORIZED`
- Exact executable candidate: `18a51b15768fb3d2196e65f1ef470c34aeef7f36`
- Candidate plugin fingerprint: `1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`
- Immutable public `v0.9.3`: `26ce64a624255278a3a0266ad38746e0e6ed2e31`

## Critical temp rule
Do not depend on Task-243 temp files still existing. Create a new unique Task-244 evidence root and runner. Temp content may have been removed between tasks.

## A — Fresh GitHub / exact-candidate gate
Before any live mutation:
1. Fetch branch HEAD, ACTIVE, STATUS, this task, Task-243 report/review, and exact-candidate Actions fresh.
2. Require exact SHA `18a51b15768fb3d2196e65f1ef470c34aeef7f36` to have `Validate`, `Windows Installer Pack Smoke`, and `PS5.1 Acceptance Smoke` = SUCCESS.
3. Recompute/verify candidate plugin fingerprint exactly `1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`.
4. Use a clean detached exact checkout. Never run installer from the moving coordination branch.
5. Reconcile any post-candidate branch drift; unexpected product/source/test/workflow drift => `BLOCKED_PREFLIGHT_DRIFT`.

## B — Fresh read-only Windows inventory
Record current:
- controller mode/generation;
- Gateway/provider/model/storage/recovery/delivery health;
- SQLite integrity and pending delivery/outbox state;
- canonical installed plugin path/fingerprint;
- plugin ownership/manifest state;
- pending rollover state recognized by the installer;
- historical rollover transaction/inventory files;
- retained Task-237 backup token `c6aaf93db7c34f718d01302477a292e1`.

Do not mutate historical Task-223/237/241/242/243 evidence. Do not assume the old installed fingerprint; prove the live value fresh. If candidate is already installed due external drift, stop `BLOCKED_ALREADY_EXACT_EXTERNAL_DRIFT` before installer execution.

## C — Re-derive installer state machine
From exact candidate source plus fresh live inventory, record before execution whether this invocation should:
- replace/install plugin payload;
- create a new rollover transaction and backup;
- finalize rollover;
- call `openclaw plugins install` or not;
- normalize controller/startup state;
- preserve stale/historical transactions.

Do not reuse Task-230 already-exact assumptions. Prove any new backup/transaction identity cannot collide with retained Task-237/223 evidence.

## D — Fresh hardened runner gate
Create a new unique PowerShell 5.1 runner implementing the accepted Task-243 contract:
- evidence root create/probe before child call;
- `runner-started.json` before child launch;
- absolute source/executable paths and exact arguments;
- identity/PID/CWD/timestamps;
- durable stdout/stderr;
- transcript path plus fallback log;
- explicit `child_nonzero_exit` vs `child_launch_exception`;
- `runner-result.json` from `finally`;
- exact child exit propagated only after durable capture.

Before installer task registration:
1. save exact runner source/bytes and SHA-256;
2. direct-qualify the exact runner with harmless stdout/stderr + exit `37` fixture;
3. direct-qualify a nonexistent-child launch exception;
4. require both to pass;
5. hash again and prove byte identity;
6. freeze the runner; no edits after this point.

Safe tooling corrections are allowed only before installer registration, must be materially different, and must be recorded. Report must include frozen runner SHA and enough persistent source/provenance to reconstruct it if temp is later deleted.

## E — One installer Scheduled Task
Use the known-good fully-qualified principal from the first registration attempt:
`CDQ-P\CDQ-P`

Use absolute `powershell.exe` and runner paths.

Budget:
```text
successful installer Scheduled Task registrations: 1 max
installer Scheduled Task starts: 1 max
installer child invocations: 1 max
installer retries after start: 0
```

If registration fails before task creation, prove `TaskPresent=false`, stop `BLOCKED_INSTALLER_TASK_REGISTRATION`, and do not retry registration in this task.

Before start, read back principal, action executable/arguments, frozen runner path/SHA, execution limit, restart policy, and task state.

Then start exactly once. The frozen runner must invoke the detached exact source `scripts/install.ps1` with the intended workspace arguments.

Once started, the retry gate closes: no second start, manual installer, manual rollover, manual plugin/runtime repair, or forced termination.

## F — Terminal classification
Consume hardened runner evidence first. Minimum expected:
```text
runner-started.json
child-stdout.txt
child-stderr.txt
runner-transcript.txt OR explicit fallback record
runner-result.json
```

Classify:
- `child_launch_exception`: tooling failure; report exact exception; no retry.
- child started + nonzero: classify exact installer stage/error from captured evidence; no retry.
- child exit `0`: continue to postflight; exit 0 alone is not PASS.
- missing/incomplete runner evidence: `BLOCKED_EVIDENCE`; no retry.

If `rollover-prepare` fails, capture the Task-239 bounded diagnostic output exactly enough to identify stage/exit/error.

## G — PASS postflight
PASS requires fresh proof that:
1. installed plugin fingerprint exactly equals `1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`;
2. rollover/backup/finalization behavior matches the pre-derived state machine;
3. new backup/transaction IDs are unique and attestation succeeds;
4. historical Task-223/237 evidence remains unchanged;
5. controller/startup converges to expected managed state;
6. Gateway healthy;
7. Ollama/provider/model healthy with no substitution;
8. delivery READY and pending state acceptable;
9. recovery READY;
10. SQLite integrity `ok`;
11. no manual Ticket/outbox/recovery mutation;
12. zero semantic/Discord activity attributable to Task 244.

Any failed postflight invariant => narrowest supported FAIL and stop without repair/retry.

## Side-effect fences
Authorized only through the one installer child invocation. Manual equivalents are forbidden.

Semantic budget:
```text
Dashboard submissions: 0
Discord submissions: 0
direct Discord/API sends: 0
semantic retries: 0
recovery replay/resend: 0
```

No reset/uninstall/reinstall sequence, second installer attempt, manual plugin replacement, manual rollover, manual lifecycle normalization, manual DB writes, provider/model substitution, evidence cleanup, release/tag mutation, force push, or semantic message.

## Required report
Publish exactly:
`docs/operations/coordination/reports/CNX-20260904-244-task243-hardened-runner-exact-candidate-windows-install-over-requalification.md`

Include fresh authority/Actions, live preflight, installed preflight fingerprint, derived installer path, detached source proof, frozen runner path/SHA/source provenance/direct tests, task definition/readback, cardinalities, runner artifacts, exact terminal classification, rollover evidence, postflight health/plugin/DB proof, side-effect ledger, exact report HEAD, and PASS/FAIL/BLOCKED disposition.

Then STOP for independent ChatGPT review. Do not perform semantic requalification in Task 244.

## Allowed dispositions
- `PASS_EXACT_CANDIDATE_INSTALL_OVER_REQUALIFIED`
- `BLOCKED_PREFLIGHT_DRIFT`
- `BLOCKED_ALREADY_EXACT_EXTERNAL_DRIFT`
- `BLOCKED_RUNNER_QUALIFICATION`
- `BLOCKED_INSTALLER_TASK_REGISTRATION`
- `BLOCKED_EVIDENCE`
- `FAIL_CHILD_LAUNCH`
- `FAIL_INSTALLER_TERMINAL`
- `FAIL_POSTFLIGHT_CONVERGENCE`
- `FAIL_LIVE_STATE_PRESERVATION`
