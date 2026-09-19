# CNX-20260919-427 — External Ingress Run Identity and Tailscale Owner Profile Repair Report

Status: `WAITING_FOR_LIVE_DISCORD_ACCEPTANCE`

Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`

## Summary

CNX-427 is split into two independent compatibility repairs.

Track A repaired the CogentNexus external-channel admission boundary. OpenClaw 2026.9.4 can invoke `reply_dispatch` for a Discord turn before assigning an authoritative run ID. CogentNexus previously converted the admission kernel's `missing-run-id` result into `handled:true`, suppressing the turn before `before_agent_run`.

Track B determined that Tailscale Serve itself was healthy. The remote Control UI authenticated as `funggier@github`, but OpenClaw's background GitHub identity synchronization received transient GitHub HTTP 403 responses. While the durable profile remained unresolved, protected session RPCs correctly failed closed with `AUTHENTICATED_PROFILE_UNAVAILABLE`. After the controlled Gateway restart, GitHub verification recovered without any authentication bypass or additional secret configuration.

## Track A — root cause and repair

Live pre-repair traces:

- `28918a57ed3b6262e763500a61ff420b`
- `4ea04d4c89877bc1305113111792190d`

Both recorded:

`CogentNexus-OpenClaw reply_dispatch admission failed closed: missing-run-id`

followed by:

`visible channel turn dispatched with no queued reply payloads`

No current Ticket was created for those turns.

### Repair

The Ticket admission kernel remains fail-closed for `missing-run-id`.

Only the early `reply_dispatch` adapter interpretation changed:

- trusted early ingress + `missing-run-id` => defer to the authoritative execution boundary;
- no Ticket is created early;
- no synthetic run ID is invented;
- all other blocked admission reasons remain fail-closed;
- `before_agent_run` still fails closed if an authoritative run ID is absent there.

Production file:

`plugins/cogentnexus-openclaw/src/index.ts`

New focused contract:

`plugins/cogentnexus-openclaw/src/cnx427-external-ingress-runid.test.ts`

CNX-422's superseded early-boundary expectation was updated to the CNX-427 semantics.

### TDD evidence

Initial focused RED:

- 1 failed / 4 passed;
- failure exactly proved the pre-repair trusted no-runId `reply_dispatch` was claimed as handled.

Focused GREEN/regression:

- 7 files passed;
- 39/39 tests passed;
- includes CNX-422, CNX-423, CNX-424, CNX-427 and Discord delivery/receipt/stale-settlement suites.

Plugin validation:

- TypeScript/build PASS;
- mixed-plugin verification PASS;
- Ticket DB bootstrap PASS;
- package-content verification PASS.

Full suite:

- 381/382 PASS;
- 84/85 files PASS;
- only failure is the pre-existing historical `cnx383-hook-policy-projection.test.ts` baseline;
- no CNX-427 regression observed.

Track A source commit:

`4ed98c8c5cbd03b3cd26acff8082fc1f14c0537b`

## Qualified live artifact

Package:

`openclaw-plugin-cogentnexus-openclaw-0.9.5.tgz`

Package SHA256:

`1E1D337FEAFC339A3E1523C68C751D04DC72CA00C7BBF84770AEFF1390D89491`

Qualified/live `dist/index.js` SHA256:

`6D96AD5FC4F419105E7E6A82EC941926886A05937C143E599C47FE9143A8FBE3`

Pre-install live `dist/index.js` SHA256:

`1CFE440EA4C9E0D87B4E293141C97E51985C33D4BFF422F49A93F68594E269B2`

The qualified package was installed over the live plugin using the OpenClaw plugin installer. After installation, the live `dist/index.js` hash exactly matched the qualified artifact.

## Controlled Gateway restart

OpenClaw:

`2026.9.4 (3a9d69d)`

Gateway PID changed:

- before: `28384`
- after: `12772`

Post-restart:

- Gateway health: GREEN;
- plugin errors: 0;
- Discord: connected/ready;
- config validation: PASS;
- shared SQLite quick_check: ok;
- agent SQLite quick_check: ok;
- CNX SQLite quick_check: ok;
- supervisor LastTaskResult: 0.

The initial health sample immediately after restart briefly reported event-loop startup degradation. A later settled sample returned `degraded=false`.

## Track B — Tailscale/profile root cause

Relevant live configuration:

- `gateway.auth.mode=token`
- `gateway.tailscale.mode=serve`
- `gateway.bind=loopback`
- allowed origin includes `https://cdq-p.tail145b6c.ts.net`
- named Gateway roles are disabled.

Durable state contained:

- `gateway-owner` profile;
- a separate durable profile linked to GitHub login `funggier`;
- no missing owner-profile database condition.

OpenClaw 2026.9.4 attaches `authenticatedGitHubIdentitySync` when the Tailscale login classifies as a GitHub provider identity. It runs that sync in detached connect work and can retry because lazy-promise rejections are evicted.

Pre-restart logs showed multiple connections:

`authenticated user connected ... user=funggier@github`

followed by:

`GitHub identity sync failed ... ControlUiGitHubError: GitHub request failed (HTTP 403)`

This left:

`authenticatedGitHubIdentitySync && !authenticatedUserProfile`

and caused protected RPCs to return `AUTHENTICATED_PROFILE_UNAVAILABLE`.

A direct anonymous GitHub API probe later returned HTTP 200 with remaining public API quota, proving the earlier 403 was transient rather than a persistent missing-account condition.

No GitHub token was copied from the existing `gh` keyring into OpenClaw, and no authentication/profile-verification policy was relaxed.

## Track B post-restart evidence

OpenClaw re-established Tailscale Serve:

`https://cdq-p.tail145b6c.ts.net/`

Current Tailscale Serve proxy:

`https://cdq-p.tail145b6c.ts.net:443/ -> http://127.0.0.1:1721`

The port `1721` is the OpenClaw-mediated Tailscale ingress layer; the main Gateway remains on `127.0.0.1:18789`.

Remote HTTPS probe:

`HTTP 200`

A fresh remote browser connection authenticated as:

`funggier@github`

After restart, no new `GitHub identity sync failed` or `Authenticated profile verification is unavailable` entries were observed.

RPCs that previously failed now completed successfully, including:

- `sessions.groups.list`
- `sessions.subscribe`
- `chat.startup`

Therefore Track B is currently GREEN without source patching or credential duplication.

## Remaining acceptance

One new operator-originated Discord turn is required because the two pre-repair Discord messages were already suppressed and are not replayed automatically.

Required live acceptance:

1. send one new Discord message to channel `1391855033993138217`;
2. verify early `reply_dispatch` logs deferred missing run identity instead of fail-closing;
3. verify `before_agent_run` received an authoritative run ID;
4. verify exactly one CNX Ticket;
5. verify model execution and one Discord delivery;
6. verify no stale lane remains.

Until that new turn is observed, final CNX-427 classification remains pending.

## Live Discord acceptance attempt #1 — visible delivery, Ticket-first NOT accepted

At approximately 15:38 Asia/Bangkok, the operator sent the requested acceptance message and received `CNX427_OK` in Discord. The same turn was visible in both local and Tailscale Control UI views.

Runtime trace:

- trace: `343c6efbf788333b585d1160af9ed4e6`;
- `reply_dispatch`: deferred due to missing authoritative run identity;
- authoritative OpenClaw run later created: `a0660423-e586-4e89-a5c9-fca25d842e1d`;
- model execution occurred;
- Discord response delivered;
- CNX logged `ignored ambiguous Discord message_sent receipt` because that receipt carried no authoritative run ID.

Database verification found no Ticket for this turn and no new Ticket near the 15:38 acceptance timestamp. The latest CNX Ticket rows remained older Dashboard turns.

Classification of acceptance attempt #1:

`VISIBLE_DELIVERY_GREEN__TICKET_FIRST_BYPASS_REMAINS`

This is not a final PASS. Work continues on a pre-inference second-stage admission boundary with authoritative OpenClaw run identity.

## Post-handoff continuation — OpenClaw 2026.9.5 storage/runtime checkpoint

The live host is now OpenClaw `2026.9.5 (ec9c1a1)`. The upstream admitted-runtime-generation continuity fix remains the selected mechanism for the final Discord requalification; no CNX-specific synthetic second-stage workaround was added.

The operator-requested C: -> T: backup relocation is complete and fidelity-verified.

Canonical destination:

`T:\CogentNexus\CogentNexus-OpenClaw`

Current mappings:

- C: `backups` -> T: `backups` via NTFS junction;
- C: `plugin-generation-rollover-backups` -> T: rollover tree via NTFS junction.

Verification evidence:

- main backup dry mirror: 509,383 files / 9.479 GiB, zero copied/mismatch/failed/extras;
- rollover dry mirror: 159,271 files / 1.408 GiB, zero copied/mismatch/failed/extras;
- authoritative CNX-427 manifest hash matched;
- critical config/wrapper/SQLite/CNX artifact hashes matched;
- authoritative reparse topology matched 10 -> 10;
- old C: rollback paths resolve after junction cutover;
- reparse-safe source cleanup completed with no failed deletions;
- C: free space increased from ~13.43 GiB to ~25.48 GiB.

Post-relocation runtime remained GREEN:

- Gateway health ok, event loop not degraded;
- PID 29604 on 127.0.0.1:18789;
- Discord ready/connected, active runs 0;
- CNX runtime attestation runnerReady=true / globalHookCount=7;
- CNX live artifact SHA256 remains `6D96AD5FC4F419105E7E6A82EC941926886A05937C143E599C47FE9143A8FBE3`;
- Supervisor LastTaskResult 0;
- Tailscale Serve -> `http://127.0.0.1:12651`;
- remote HTTPS 200;
- `ollama ps` empty;
- free virtual/commit ~20.57 GiB.

Detailed checkpoint:

`docs/operations/coordination/reports/CNX-20260919-427-storage-relocation-and-pre-acceptance-runtime-checkpoint.md`

The only remaining CNX-427 gate is one new operator-originated Discord turn on live OpenClaw 2026.9.5 proving authoritative runId, exactly one Ticket before inference, exactly one model execution, exactly one Discord delivery, terminal completion, and no stale/duplicate lane.
