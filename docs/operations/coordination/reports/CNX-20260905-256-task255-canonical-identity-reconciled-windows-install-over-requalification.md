# CNX-20260905-256 — Canonical-Identity-Reconciled Exact-Candidate Windows Install-Over Requalification

## Final disposition

`BLOCKED_PREFLIGHT_DRIFT`

The authorized one-shot installer was **not started**. A fresh read-only live preflight found an emittable, due direct-recovery row for an accepted Ticket. Under the recovery safety gate, install-over cannot be armed while that row may emit delayed output. No Scheduled Task was registered or started, and no product or semantic mutation occurred.

## Fresh authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`
- Fresh remote HEAD: `d6e1d86395d1bd60d110a2a905d1c9518ba9064e`
- `ACTIVE.md` / `STATUS.md`: `READY_FOR_HERMES`, active `CNX-20260905-256`
- Matching report absent before publication (GitHub API 404)
- Public tag: `v0.9.3 = 26ce64a624255278a3a0266ad38746e0e6ed2e31` (unchanged)
- Exact candidate Actions: terminal success for Validate (`33944299263`), Windows Installer Pack Smoke (`33944299239`), and PS5.1 Acceptance Smoke (`33944299258`); the candidate’s nine checks were independently reported as success by the read-only pre-gate.

## Exact candidate identity

Fresh detached checkout:

`C:/Users/CDQ-P/AppData/Local/Temp/cnx256-exact-candidate-6822af4`

- HEAD: `6822af464fe7a5cb3f93305d0263dfc86b56ac68`
- detached: `true`
- `core.autocrlf=false`
- worktree: clean
- `VERSION`: `0.9.3`

Canonical installer triple proof, all byte-identical:

```text
git show 6822af4:scripts/install.ps1 = 9d53a42794e0052a817a9f7dd60d0e5895b75882f62261e08427ee414e17b57b
detached working tree             = 9d53a42794e0052a817a9f7dd60d0e5895b75882f62261e08427ee414e17b57b
raw GitHub bytes                  = 9d53a42794e0052a817a9f7dd60d0e5895b75882f62261e08427ee414e17b57b
```

Canonical size was `31983` bytes. The CRLF materialization digest `c0779d9bae69d850a44073134e7799a48a1856935b09aae1ae8c7da9f57e0629` was recorded as diagnosis-only and was never used as a gate. Runner SHA-256 was `729fba4552e28cd6f53e62f10c8f3bd098d5ca5dfb8d0e3bf4ba3ba1a6250f3e`. After `npm ci` and `npm run plugin:build`, candidate plugin fingerprint was independently computed as `1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`.

Evidence: `C:/Users/CDQ-P/AppData/Local/CogentNexus-OpenClaw/forensics/CNX-20260905-256/a01-identity.json`, `a02-npm-ci.txt`, `a03-plugin-build.txt`, `a04-candidate-fingerprint.json`, and byte copies `installer-git.ps1`, `installer-working.ps1`, `installer-raw.ps1`, `runner.ps1`.

## Fresh live preflight

Read-only launcher checks were rerun at approximately `2026-09-05T06:05Z`; each returned exit `0`, `readOnly=true`, and `stateChanged=false`:

- controller mode `passthrough`, generation `39`;
- Gateway healthy on loopback `127.0.0.1:18789`;
- selected provider `ollama`, reachable/healthy/ready with four models;
- Delivery `READY`, pending terminal deliveries `0`;
- Recovery launcher check `READY`, with no active provider incident;
- Storage `READY`, SQLite integrity `ok`;
- status ticket counts: `accepted=1`, `cancelled=2`, `completed=10`;
- installed resolver: version `0.9.3`, current installed fingerprint `e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386` (predecessor, not candidate).

## Blocking recovery finding

Direct SQLite was opened using `file:<path>?mode=ro`; schema was inspected before querying. Database:

`C:/Users/CDQ-P/.openclaw/workspace/.cogentnexus-openclaw/runtime/cogentnexus-openclaw.sqlite3`

The row below is due and still potentially emittable:

```text
ticket_id       = CNXT-dc11c9a0-8a89-4df5-9c48-345260725be4
Ticket status   = accepted
recovery mode   = redeliver
recovery state  = pending
attempt_count   = 0
next_attempt_at = 2026-09-03T01:49:59.316Z
owner_generation= 1
session state   = active
session gen.    = 1
workflow_eligible=0
workflow_id     = NULL
```

The exact candidate source confirms this is an eligible recovery path, not an informational status: `plugins/cogentnexus-openclaw/src/v091-direct-recovery.ts:72-84` selects `r.state='pending'`, `t.status='accepted'`, `workflow_eligible=0`, null workflow, active session, matching generation, and due `next_attempt_at`. The wake calculation at lines `125-150` likewise schedules a pending matching row. Therefore global `recovery=READY` and `pendingOutbox=0` do not override this exact matching row.

Evidence: `b01-*` read-only launcher outputs, `b02-sqlite.json`, and `b03-recovery-binding.json`; installed identity is in `b04-installed-resolver.json`.

## Execution ledger / hard fences

```text
Scheduled Task registrations       = 0
Scheduled Task starts              = 0
scripts/install.ps1 target starts  = 0
installer retries after start      = 0
Dashboard semantic sends           = 0
Discord semantic sends             = 0
direct API semantic sends          = 0
recovery replay/resend             = 0
DB/manual lifecycle mutation       = 0
retained forensic evidence edits   = 0
release/tag mutation               = 0
force-push/history rewrite         = 0
```

No manifest was frozen, no Scheduler XML/action readback was performed, and no installer parameter or skip switch was invented. Task256’s PT45M / `AllowHardTerminate=true` contract remains unconsumed.

## Harness/anomaly notes

One initial installed-resolver invocation used an incorrect relative script path and failed with exit `2`; it was a harness-only command error, preserved separately, then corrected with an absolute native path and succeeded. `npm ci` emitted dependency audit/install-script warnings; no audit fix or dependency mutation was performed. These issues do not alter the product disposition.

## Reviewer verification packet

1. Verify remote branch HEAD and this report’s blob at the final publication HEAD.
2. Recompute the three installer hashes and runner hash from candidate `6822af4`.
3. Recompute candidate fingerprint after build and compare to `1ff69c45...babb5f`.
4. Re-open the SQLite database read-only, inspect schema, and verify the exact pending recovery row/generation binding.
5. Verify no Task256 Scheduled Task exists and no installer target process was started.
6. Verify public `v0.9.3` still targets `26ce64a...2e31` and semantic counts remain zero.

## Required next action

Do not clear, cancel, replay, resend, or mutate the pending recovery row in this task. Do not register/start the installer and do not retry Task255. A separately authorized successor must reconcile the recovery provenance and authorize any remaining install-over phase; semantic acceptance remains unauthorized.
