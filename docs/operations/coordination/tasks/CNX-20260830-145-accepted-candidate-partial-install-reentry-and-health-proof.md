# CNX-20260830-145 — Accepted Candidate Partial-Install Re-entry and Health Proof

Status: `READY_FOR_HERMES`
Execution mode: `LIVE_WINDOWS_SUPPORTED_INSTALLER_REENTRY_AND_HEALTH_PROOF`
Owner: ChatGPT
Executor: Hermes/Codex on the operator's real Windows machine

## Purpose

Prove that the supported v0.9.3 installer can safely re-enter from the intentionally preserved Task-142 partial install-over state and reach a coherent accepted-candidate installation, without manual normalization, cleanup, plugin manipulation, or semantic Dashboard traffic.

This is the first live task after the offline Task-143/144 rollover repairs. It is **not** a Dashboard acceptance task and it is **not** a clean uninstall/reinstall task.

## Accepted source and evidence

Accepted implementation SHA:

`fb5781c1abd68280760bd5b3b4a65fabd8a60e58`

This exact production SHA contains the Task-144 canonical-registration repair and completed the required exact-SHA workflows successfully:

- Validate `33264956365`
- Windows Installer Pack Smoke `33264956369`
- PS5.1 Acceptance Smoke `33264956375`

Review/coverage descendant:

`b4e943b20e699dd19707b80a6b6f2d395c75b03a`

The descendant adds only the missing outside-state registration-alias regression test; it does not change production implementation. Use the exact implementation SHA `fb5781c1...` as the detached live deployment source unless the review explicitly records an equivalent descendant with zero production/package-relevant source delta.

## Preserved live starting boundary

Do not assume it still holds. Verify it read-only before mutation.

Task 142 last observed:

- one singular `cogentnexus-openclaw` plugin identity;
- canonical direct root `C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw`;
- plugin disabled;
- controller `passthrough`;
- old/pre-attempt ownership manifest remains;
- installed plugin fingerprint `12c6d1b5b6ffd938353dd60c5d6190c34a609663369f619ff4fc7cbd176119e0`;
- installed `namespace_ownership.py` SHA-256 `e51f03553a24ea67037a3131b5ff4edb8aa435fbbc82b19974ae18f0d03df666`;
- Gateway healthy;
- OpenClaw `2026.7.1-2`;
- Ollama reachable/healthy/ready;
- recovery and delivery `READY` read-only;
- pending outbox `0`;
- SQLite integrity `ok`;
- semantic counts `tickets=2`, `ticket_events=14`, `cnx_direct_model_call=2`, `cnx_direct_recovery=0`, `cnx_assistant_delivery=0`, `ticket_outbox=0`, `cnx_sessions=2`;
- Dashboard semantic Send count `0`.

Any material drift must be reported. Do not normalize drift manually.

## Remote/worktree authority

GitHub remote working branch is authority, not a stale local checkout.

Before execution:

1. fetch `agent/v0.9.3-full-stabilization` from GitHub;
2. verify `ACTIVE.md` and `STATUS.md` authorize this exact Task 145 and no matching report already exists;
3. preserve any uncertain local checkout; do not reset it;
4. use a fresh detached clone/worktree of exact implementation SHA `fb5781c1abd68280760bd5b3b4a65fabd8a60e58` for packaging/execution;
5. do not merge, rebase, or force-push.

## Phase A — detached candidate provenance, no live mutation

From exact implementation SHA `fb5781c1...`:

1. confirm clean detached source;
2. run the candidate plugin validation/build/package path needed by the supported installer;
3. record package filename, bytes, SHA-256, and packed-file count;
4. compute candidate plugin fingerprint using the production ownership helper;
5. compute SHA-256 of candidate `skills/cogentnexus-openclaw/scripts/namespace_ownership.py`;
6. record source `scripts/install.ps1` SHA-256;
7. record exact OpenClaw/plugin version expectations.

Do not reuse Task-142 candidate hashes as assumptions. Recompute them from this exact source.

## Phase B — live read-only drift and classification gate

Before the first live mutation, capture read-only evidence for:

### Ownership/storage

- current `openclaw plugins list --json` inventory;
- exactly one `cogentnexus-openclaw` identity;
- raw inventory `rootDir` is lexically the exact canonical direct root, not an alias/junction/symlink/noncanonical path;
- canonical direct root itself is a real normal directory and not a reparse/junction/symlink;
- no conflicting managed npm/product storage;
- current plugin enabled/disabled status;
- current installed plugin fingerprint;
- current installed `namespace_ownership.py` hash;
- current ownership manifest and its `installedAt`/plugin path/fingerprint-relevant evidence;
- controller mode.

### Runtime/health

- OpenClaw version;
- Gateway listener/health;
- selected provider and Ollama health/readiness;
- CogentNexus recovery check read-only;
- delivery check read-only and pending count;
- SQLite `pragma integrity_check`;
- semantic table counts matching the Task-142 baseline or an explicitly explained harmless delta;
- Dashboard semantic Send count remains zero.

### Candidate-aware classification

Use the exact candidate fingerprint and the production `namespace_ownership.py` classifier with the real current plugin inventory. Record the complete classification and lifecycle action resolution **before mutation**.

Do not assume whether the Task-145 candidate fingerprint equals Task-142's installed fingerprint.

Accepted classification families:

- coherent `upgrade` + `pluginAlreadyExact=true` + `pendingRollover=false`, in which case lifecycle actions must not replay plugin installation/rollover; or
- coherent `upgrade` with a genuinely different accepted candidate fingerprint, in which case lifecycle actions may authorize exactly one bounded rollover using Task-144 protections.

If classification is partial/mixed/ambiguous, registration is noncanonical, product storage conflicts, manifest/state drift cannot be safely explained, or action resolution contradicts the classifier: **BLOCKED before mutation**.

## Phase C — exactly one supported installer invocation

If and only if all Phase-B gates pass, execute exactly one normal supported installer invocation from the exact detached candidate source:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File <exact-detached-source>\scripts\install.ps1 -Workspace C:/Users/CDQ-P/.openclaw/workspace
```

Do not add staging/skip flags unless this task is explicitly amended before execution. The goal is the supported normal install-over/re-entry path.

Invocation count: **exactly 1**.

Prohibited before/during/after the invocation:

- no manual plugin copy/delete/replace;
- no separate `openclaw plugins install/uninstall/enable/disable` command outside what `install.ps1` itself performs;
- no manual controller mutation;
- no manual ownership-manifest edit/delete;
- no reset/uninstall/clean reinstall;
- no cleanup/normalization of Task-142 state;
- no retry if the installer fails;
- no alternate installer or semantic transport.

## Failure boundary

If the supported installer exits nonzero or hits a first product/runtime failure:

1. stop immediately;
2. do not retry;
3. do not clean up or normalize;
4. capture only read-only post-failure provenance/health/state;
5. report verdict `FAIL_INSTALL_REENTRY` with the first failing boundary and exact state transition.

A controlled failure is evidence; it is not permission to improvise another attempt.

## Phase D — post-success proof

If the one supported invocation exits `0`, prove read-only that:

- exactly one canonical plugin identity remains;
- installed plugin fingerprint equals the exact accepted candidate fingerprint;
- installed `namespace_ownership.py` hash equals candidate provenance;
- ownership manifest was refreshed/finalized and exact ownership verification passes;
- plugin enabled/disabled state matches the normal supported installer contract;
- controller reached the normal managed operating state expected by the installer;
- Gateway is healthy and reachable after installer lifecycle work;
- selected Ollama/provider is healthy/ready;
- recovery is `READY` read-only;
- delivery is `READY`, pending `0`, read-only;
- SQLite integrity is `ok`;
- pre-existing Ticket/event/session history is preserved; report exact count deltas and explain any expected operational changes;
- there is no duplicate/conflicting plugin/product storage;
- no stale rollover transaction remains;
- Dashboard semantic Send count is still `0`.

Do not inject a crash/recovery test and do not send a Dashboard message in Task 145.

## PASS criteria

`PASS` requires all of:

1. fresh remote Task145 authority and exact detached candidate provenance;
2. Phase-B live state is coherent and canonical;
3. candidate-aware classifier/action plan is coherent and recorded before mutation;
4. exactly one supported installer invocation;
5. installer exit code `0`;
6. accepted candidate provenance installed exactly;
7. ownership/controller/plugin/runtime health reach coherent normal state;
8. durable data integrity/history preserved;
9. no manual normalization/retry/alternate path;
10. Dashboard semantic Sends `0`.

## Required report

Publish exactly:

`docs/operations/coordination/reports/CNX-20260830-145-accepted-candidate-partial-install-reentry-and-health-proof.md`

The report must include:

- exact remote authority HEAD at start;
- exact detached source SHA;
- candidate package/fingerprint/hash provenance;
- complete preflight drift evidence;
- classifier and lifecycle actions before mutation;
- exact installer command and invocation count;
- installer output/exit code/first failure if any;
- complete post-state evidence;
- side-effect accounting;
- verdict `PASS`, `FAIL_INSTALL_REENTRY`, or `BLOCKED`;
- unproven items.

Then stop for independent ChatGPT review.

## Hard fence

No Dashboard semantic Send/resend; no Ticket/workflow/outbox/delivery/recovery semantic mutation; no crash/recovery injection; no reset/uninstall/clean reinstall; no manual plugin/controller/manifest normalization; no unrelated service/process/task mutation; no reboot; no credentials/secrets; no release/tag/merge; no force push.
