# CNX-20260919-425 — Controlled Live OpenClaw 2026.9.4 Upgrade and Post-Upgrade Acceptance

Status: `COMPLETE`

## Authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Parent: `CNX-20260919-424`
- Review decision: `ACCEPTED_PASS__CONTROLLED_OPENCLAW_2026_9_4_UPGRADE_AUTHORIZED`
- Parent review: `docs/operations/coordination/reviews/CNX-20260919-424-chatgpt-review.md`
- Executor: `ChatGPT via LConnect`
- Reviewer: `ChatGPT`
- Human final authority: `Operator`

## Objective

Upgrade the live OpenClaw host from `2026.7.1-2` to exact `2026.9.4` and prove CogentNexus-OpenClaw remains functional with preserved live state.

## Phase 0 — Preflight

Record:

- installed OpenClaw version and binary path;
- Gateway PID/status/health;
- session count;
- live config path;
- live workspace path;
- shared/agent/CNX DB versions and integrity;
- relevant plugin paths;
- free disk space;
- exact candidate plugin/package provenance.

Do not send semantic provider traffic.

## Phase 1 — Quiesce and rollback snapshot

Gracefully stop the live Gateway.

Verify port `18789` is closed.

Create a timestamped rollback snapshot outside `~/.openclaw` containing at minimum:

- complete `C:\Users\CDQ-P\.openclaw` tree;
- old global OpenClaw package directory;
- npm OpenClaw launcher/wrapper files;
- explicit copies/hashes of config, workspace migration files, shared state DB, agent DB/session store and CNX DB;
- version/provenance manifest.

Use consistent SQLite backup where required.

Verify snapshot hashes/integrity before proceeding.

If snapshot verification fails: stop and classify BLOCKED.

## Phase 2 — Exact target installation

Install exact OpenClaw `2026.9.4`.

Prefer reproducible exact package provenance. Verify:

`openclaw --version`

before live migration/startup.

Do not select a newer version.

## Phase 3 — Live config/state migration

Run target-version config validation/doctor in non-interactive controlled mode.

Known prequalified migrations include:

- shared state schema `v1 -> v17`;
- agent DB `v1 -> v19`;
- legacy sessions -> SQLite;
- workspace setup/HEARTBEAT/TOOLS migration semantics.

Record all changes.

Do not manually edit live SQLite rows.

If migration fails: stop target runtime and execute full rollback.

## Phase 4 — Live Gateway start and non-semantic acceptance

Start/re-enable the live Gateway under the intended normal ownership mechanism.

Verify:

- listener `127.0.0.1:18789`;
- health `ok=true`;
- exact version `2026.9.4`;
- CogentNexus plugin loaded without errors;
- reply_dispatch registration present;
- runtime attestation collected;
- session count preserved;
- channels expected by the operator remain healthy;
- CNX DB residue/integrity is not unexpectedly consumed or rewritten.

No semantic send until every gate above passes.

## Phase 5 — Controlled semantic Ticket-first acceptance

After all non-semantic gates pass, perform one bounded controlled acceptance using the operator's intended Dashboard/provider path.

Requirements:

- verify provider/model selection immediately before send;
- create one fresh session if stale browser/provider state could contaminate the test;
- one semantic owner message only;
- prove Ticket exists before model execution;
- prove one Ticket / one route event;
- prove provider/model/harness remain OpenClaw-owned;
- capture terminal/delivery evidence;
- do not repeat semantic sends randomly.

If browser mutation is required and cannot be safely automated, stop at `WAITING_FOR_OPERATOR_SEMANTIC_SEND` with exact instructions rather than inventing evidence.

## Phase 6 — Rollback trigger

Rollback immediately if any of the following cannot be repaired safely in-place before semantic acceptance:

- target binary/version mismatch;
- migration inconsistency;
- Gateway cannot become healthy;
- session loss/corruption;
- CNX plugin load failure;
- state integrity failure.

Rollback means:

- stop target Gateway;
- restore old OpenClaw package/wrappers;
- restore complete pre-upgrade snapshot;
- validate 2026.7.1-2;
- start old Gateway;
- verify health/session count/CNX integrity.

Do not perform binary-only downgrade over v17 migrated state.

## Final classifications

### PASS

`LIVE_OPENCLAW_2026_9_4_UPGRADE_ACCEPTED`

### WAITING

`WAITING_FOR_OPERATOR_SEMANTIC_SEND`

### BLOCKED/ROLLED BACK

`LIVE_UPGRADE_BLOCKED_AND_ROLLED_BACK`

## Repository closeout

Publish:

`docs/operations/coordination/reports/CNX-20260919-425-controlled-live-openclaw-2026-9-4-upgrade-and-post-upgrade-acceptance-report.md`

Update ACTIVE.md/STATUS.md to the exact final state.

No release/tag/main or force-push.
