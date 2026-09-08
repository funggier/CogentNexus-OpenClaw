# CNX-20260905-262 — Task261 One-Shot Live Install-Over Requalification

Status: `READY_FOR_LUNA`
Executor: `Luna`
Independent reviewer / next actor: `Musethree`
Parent task: `CNX-20260905-261`
Parent umbrella: `CNX-20260831-188`

## Authority

ChatGPT decision:

`docs/operations/coordination/reviews/CNX-20260905-261-live-install-over-chatgpt-decision.md`

Decision:

`AUTHORIZE_TASK262_ONE_SHOT_LIVE_INSTALL_OVER_REQUALIFICATION`

This task authorizes one bounded live install-over requalification on the authenticated Windows machine. It does not authorize any semantic response, recovery disposition/redelivery, or unrelated production repair.

## Exact candidate and accepted evidence

- Source candidate: `a87c3930651eecf4563d5d8bafe897e058bbdfe0`
- Reviewed publication: `d7cf125393994444178644732d50ffbfb3cb8e03`
- Review commit/escalation authority: `442ed7321e25408fa972f4b527ce8fad5afbf006`
- Candidate `scripts/install.ps1` Git blob: `383f1bd05197381ffd6b4f3fa054ee11ab365c1a`
- Candidate `host_v091.py` Git blob: `77d3ad291ce6b2e9109066a0367d5115810c3965`
- Reviewed publication CI: 9/9 check-runs success; workflow runs `33960828088`, `33960828097`, `33960828083` success.
- Public `v0.9.3` tag remains reference-only for this task and must not move.

## Objective

Prove on the real Windows machine that the exact Task261 candidate can install over the current CogentNexus-OpenClaw installation using the supported install-over path, that the successful transition includes a fresh managed Gateway process boundary loading the candidate payload, and that the pre-existing stale recovery row does not emit, replay, redeliver, or mutate during the transition.

## Opening authority / race gate

Before any live side effect:

1. Fetch the remote branch and require Task262 to remain the active task assigned to Luna.
2. Verify linear ancestry from `442ed7321e25408fa972f4b527ce8fad5afbf006`; do not overwrite any newer baton state.
3. Establish a clean detached/fresh worktree at exact candidate `a87c3930651eecf4563d5d8bafe897e058bbdfe0` for installer source. Do not execute installer from moving branch HEAD.
4. Verify `git rev-parse HEAD` exact equality and clean worktree.
5. Verify candidate blob identities above and recompute the candidate plugin fingerprint using the repository's canonical namespace/fingerprint mechanism. Record it before installation.
6. Verify the Task261 reviewed publication CI remains terminal green. If GitHub evidence is temporarily non-terminal/unavailable, use `DELAYED_RECHECK_QUEUE.md`; do not ask the human to wake the task manually.
7. Verify no matching Task262 completion report already exists. A matching report is a replay fence: never repeat the installer side effect.

Any authority, identity, ancestry, candidate, report, or CI drift before live execution => `BLOCKED_PREFLIGHT_DRIFT`, no installer start.

## Live preflight

Capture durable evidence before the single installer attempt:

- current installed ownership/version/plugin root/fingerprint;
- Gateway PID/process start time/command/health and controller/provider posture;
- current launcher/workspace identity;
- SQLite database path and `PRAGMA integrity_check` via read-only access;
- exact subject Ticket `CNXT-dc11c9a0-8a89-4df5-9c48-345260725be4` recovery row, owner session/generation/`updated_at`, `attempt_count`, `active_run_id`, model-call fence state, assistant-delivery/outbox rows;
- direct-recovery due/wake posture under the candidate predicate, without mutation;
- semantic-send/recovery attempt counters or equivalent evidence needed to prove zero emission across the action.

The subject row may remain `pending/redeliver`; this task does not dispose it. Require its owner session to remain outside the accepted 15-minute freshness window immediately before installer execution. If it has become fresh or otherwise eligible/emittable under the candidate predicate, STOP before installer and publish `BLOCKED_RECOVERY_PREFLIGHT_DRIFT`.

## Authorized action — cardinality exactly one

Run the supported normal install-over from the verified exact candidate source.

Requirements:

- `scripts/install.ps1` live starts: **maximum 1**;
- use the normal managed install-over path; do **not** use `-SkipGatewayRestart` or another bypass that weakens fresh-process proof;
- if elevation/privileged execution requires the established Windows Scheduled Task/runner pattern, registration/start cardinality is maximum 1 each and the exact command/source must be recorded;
- allow only installer-owned lifecycle actions required by the supported transaction, including the Task261 mandatory managed Gateway process boundary;
- capture exact command, environment-relevant arguments, timestamps, exit code, stdout/stderr/log/evidence paths and hashes;
- no automatic second live attempt for nonzero, timeout, ambiguous, or partially successful result.

If the installer fails or the result is ambiguous, preserve rollback/poststate evidence and STOP. Diagnosis may be read-only; do not repair source or rerun the installer in Task262.

## Mandatory postflight

A PASS requires all of the following:

1. Installer result is unambiguously successful from the one authorized attempt.
2. Installed plugin fingerprint exactly equals the precomputed exact-candidate fingerprint.
3. Installed ownership manifest/root/version/launcher are coherent and point to the intended canonical installation.
4. Gateway is healthy and the final managed Gateway process is demonstrably fresh relative to preflight (PID/start-boundary/process evidence) and postdates candidate replacement/activation.
5. Managed enable/process-boundary evidence reports verified success; no predecessor process is accepted merely because it stayed healthy.
6. Controller/provider/Gateway posture is internally consistent after install-over.
7. SQLite `integrity_check` remains `ok`.
8. Subject recovery Ticket has no recovery execution side effect: no incremented attempt attributable to Task262, no claim/run, no replay/redelivery/resend, and no new assistant-delivery/outbox semantic output.
9. The subject stale row is non-due/non-waking under the installed candidate freshness predicate at postflight.
10. Dashboard/Discord/API semantic sends attributable to Task262 = 0.
11. No release/tag mutation and no force push/history rewrite occurred.

Unexpected semantic output, recovery attempt, wrong fingerprint, non-fresh Gateway, integrity failure, ownership ambiguity, or postflight identity drift => FAIL/BLOCKED and STOP; do not retry.

## Source-mutation fence

Task262 is a live execution/evidence task. Production/source/test repair is **not** authorized inside it.

If live evidence reveals a product defect, publish the exact blocker and hand off to Musethree for review/rework-task selection. A new source repair requires a new candidate and fresh CI before any later live attempt.

## Effect ledger

Report exact counts for:

```text
installer Scheduled Task registrations <= 1 (only if required)
installer Scheduled Task starts <= 1 (only if required)
scripts/install.ps1 live starts <= 1
installer-owned Gateway/process-boundary transitions = observed exact count
manual Gateway/controller/provider mutations outside installer = 0
manual DB/recovery mutation = 0
recovery dispose/clear/cancel/claim/replay/redeliver/resend = 0
Dashboard/Discord/API semantic sends = 0
release/tag mutation = 0
force push/history rewrite = 0
live retry after failure/ambiguity = 0
```

## Required report

Publish:

`docs/operations/coordination/reports/CNX-20260905-262-task261-one-shot-live-install-over-requalification.md`

Use `EXECUTOR_REPORT_CONTRACT.md` and include:

- exact opening/final authority and race checks;
- exact candidate/worktree/blob/fingerprint evidence;
- preflight installed/runtime/recovery/SQLite state;
- exact one-shot installer command and cardinality;
- process-boundary evidence proving a fresh Gateway;
- installed fingerprint/ownership identity;
- postflight recovery non-emission and SQLite integrity;
- logs/evidence paths and SHA-256 hashes;
- acceptance matrix;
- hard-fence/effect ledger;
- residual uncertainty and recommended successor;
- 3–10 item reviewer verification packet.

After report publication, hand the baton to Musethree and invoke/call Musethree when Hermes supports direct peer handoff. Musethree independently reviews Task262. Pending asynchronous CI during report/review processing must use the persistent five-minute delayed recheck queue rather than becoming dormant.
