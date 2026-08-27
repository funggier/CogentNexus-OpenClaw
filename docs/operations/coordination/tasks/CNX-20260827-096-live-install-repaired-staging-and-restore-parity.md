# CNX-20260827-096 — Live Install Repaired Dashboard Staging and Restore Parity

Status: `READY_FOR_HERMES`

Execution mode: `LIVE_ONE_SHOT_SUPPORTED_INSTALL_TASK093_095_SOURCE`

Current authorization: `TASK095_ACCEPTED_ONE_SHOT_LIVE_INSTALL_AUTHORIZED`

Owner: ChatGPT

Executor: Hermes/Codex after operator continuation

## Goal

Perform exactly one supported normal install-over from the independently accepted Task-093+094+095 source, prove that the currently installed pre-Task093 plugin is no longer misclassified as exact under the v2 payload fingerprint, prove the repaired package is actually installed and ownership-safe rolled over, then restore and verify a coherent MANAGED live deployment with zero semantic/provider messages.

Exact released source implementation:

`32212a4331e1f32b5a130bd30d271d4cbc56f6c1`

Do not install from a report/review/coordination HEAD. Use an isolated exact checkout of the implementation SHA above.

## Accepted predecessor chain

Task 093 preserved Dashboard staging repair:

`a924157ecdedef1d4f166d5762529b0d59536fc9`

It separates process-global `TicketStore.prototype` patch lifetime from per-runtime `reply_dispatch` hook registration so legitimate plugin re-registration does not lose durable payload staging.

Task 094 introduced the complete installable-payload v2 fingerprint using `package.json.files` + `package.json`, normalized relative paths and exact bytes.

Task 095 implementation:

`32212a4331e1f32b5a130bd30d271d4cbc56f6c1`

Task 095 independent disposition:

`ACCEPT_WINDOWS_REPARSE_POINT_PAYLOAD_ATTESTATION_REPAIRED`

Candidate v2 fingerprint reported by Task 095:

`df2600da3ae78e1613793b4a7e5d1ebe61f66f71f0903e1d5d2cd5f0d5f4f4b4`

Canonical candidate payload count reported: `176`.

Read-only Task-094 evidence reported the currently installed pre-Task093 payload under the v2 algorithm as:

`6d40f856313f6c295a51956d130cd977337a3dd8ac64fd51ed6db20f568b40cb`

Do not trust these values blindly: recompute both candidate and live values during this task before mutation.

## Current live-state caution

Task 090 restored a coherent MANAGED deployment and no-flash multi-tick health.

Task 092 later performed one authenticated fresh-session semantic attempt. It created durable semantic evidence that ended fail-closed because the Dashboard final payload was not staged. Those Task-092 Ticket/run/session/transcript records are retired evidence and must be preserved byte/logically unchanged by this task.

Therefore do not assume `tickets=0` or `events=0` now. Snapshot the current SQLite state and prove no new semantic rows are created by Task 096. Do not repair/delete/reclassify Task-092 evidence.

---

# Absolute one-shot and semantic fence

Exactly one invocation of the supported normal installer is authorized.

Authorized live mutation:

- one supported normal install-over using exact source `32212a4331e1f32b5a130bd30d271d4cbc56f6c1`;
- only the normal effects performed by that supported installer and its supported controller transition/restart path.

Forbidden:

- a second installer invocation or retry;
- manual plugin install/uninstall/disable/enable as a repair;
- manual deletion/move/rename of plugin generations;
- manual ownership-manifest rewrite;
- manual controller/startup/Supervisor/AGENTS repair;
- reset/uninstall/cleanup;
- direct SQLite mutation;
- Task-092 Ticket/session/transcript repair;
- Dashboard/WebChat message/send;
- `chat.send`, `chat.inject`, `openclaw agent`, `sessions_send` or channel send;
- generation of a semantic nonce;
- direct Ollama/provider inference/probe;
- provider/model/timeout changes;
- reboot;
- merge/tag/release;
- force push.

If the single supported install-over fails, stop and report the exact blocker. Do not normalize the live state manually and do not retry.

Read-only health/status/inventory/SQLite/provider inventory inspection is allowed. `ollama list` / `ollama ps` are read-only; do not invoke a model.

---

# Phase A — fresh pre-mutation proof

Before the one installer invocation, record fresh evidence from the exact implementation checkout and live machine.

## A1 — versions and exact source

Record:

- Windows build;
- Windows PowerShell version;
- Node and npm versions used by the supported installer;
- OpenClaw exact version/build;
- Git exact source HEAD = `32212a4331e1f32b5a130bd30d271d4cbc56f6c1`;
- clean isolated source worktree.

Run candidate build/validation required to compute the final package payload exactly as production classification will see it.

## A2 — live coherent baseline

Read-only prove and record:

- controller mode/generation;
- startup enabled/disabled state;
- Supervisor state;
- AGENTS managed marker count/content hash or equivalent exact evidence;
- ownership manifest path, SHA and pluginPath;
- OpenClaw plugin inventory, canonical CogentNexus generation count and active registration;
- Gateway status/probe;
- SQLite integrity;
- complete current Ticket/event/outbox/direct-delivery counts and hashes/identifiers sufficient to prove no Task-096 semantic mutation later;
- exact Task-092 retired Ticket/run/session state remains present and unchanged;
- Ollama process/list inventory only, with no model call.

If live ownership is already incoherent or ambiguous before mutation, stop. Do not install into an unproven topology.

## A3 — prove v2 non-exact classification before mutation

Using the production Task-095 `namespace_ownership.py` from exact source and the real live plugin inventory:

1. compute candidate v2 fingerprint from exact built candidate;
2. compute/resolve the live manifest-owned plugin v2 fingerprint;
3. require candidate and live fingerprints differ;
4. require the live topology has exactly one canonical currently installed generation before this ordinary upgrade;
5. run the real production `classify-install` with exact live inventory and candidate expected fingerprint;
6. require:
   - `mode = upgrade`;
   - `pendingRollover = false`;
   - `pluginAlreadyExact = false`;
7. run the real production lifecycle action resolver through the same named-parameter boundary used by `install.ps1` and require:
   - `installPlugin = true`;
   - `rolloverPlugin = true`.

Also inspect the real production `install.ps1`/AST invariants carried from Tasks 086/089:

- package install is under `installPlugin`;
- rollover is independently under `rolloverPlugin`;
- rollover is not nested under `installPlugin`;
- rollover occurs before the strict final plugin resolution.

If any precondition differs, stop before mutation with an exact blocker.

---

# Phase B — exactly one supported install-over

Invoke the supported normal installer exactly once from the exact implementation checkout:

`powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1 -Workspace C:\Users\CDQ-P\.openclaw\workspace -Provider ollama`

Record:

- invocation count = `1`;
- retry count = `0`;
- complete exit status;
- bounded installer evidence sufficient to prove whether package installation and rollover actually occurred.

For a PASS, the installer must exit `0`.

Do not issue any separate plugin lifecycle command.

---

# Phase C — prove real package installation and ownership-safe rollover

A successful Task 096 must prove this was not an `already exact` no-op.

## C1 — package installation really happened

Correlate installer output/filesystem/inventory evidence to prove:

- candidate classification was non-exact;
- the package-install branch executed;
- `npm pack` was executed by the supported installer;
- `openclaw plugins install` was executed by the supported installer using the produced package artifact;
- the new installed generation payload fingerprint equals the exact candidate v2 fingerprint;
- Task-093 repaired `dist/v091-dashboard-verified-delivery.js` is present in the installed generation and source/live package file-set parity is exact;
- no unrelated plugin installation occurred.

## C2 — rollover converged safely

Prove:

- ordinary upgrade transiently created only the expected replacement generation;
- rollover used the exact candidate source attestation;
- retired generation was moved through the reviewed same-volume backup boundary, not deleted ad hoc;
- ownership manifest now binds the surviving exact replacement;
- final canonical CogentNexus generation count is exactly `1`;
- no third persistent generation remains;
- the surviving registration root is the manifest pluginPath;
- final active/enabled state is the normal MANAGED state expected by CogentNexus/OpenClaw;
- backup evidence is bounded to the product backup root.

Do not delete the supported rollover backup.

---

# Phase D — restore/prove MANAGED parity and health

After the one supported installer returns success, prove fresh live state.

Required:

- controller `managed` with a new coherent generation;
- startup enabled as expected;
- Supervisor installed/running/healthy as expected;
- AGENTS managed block exactly once and content/source parity valid;
- ownership manifest verifies against workspace and exact surviving plugin;
- installed skill/source parity with exact implementation checkout;
- installed plugin canonical payload file set = exact candidate file set (`176` if unchanged after exact build) and candidate/live v2 fingerprint equality;
- OpenClaw plugin inventory has exactly one canonical CogentNexus registration and no duplicate linked/global residue;
- Gateway running and probe healthy;
- Dashboard/control UI remains reachable read-only;
- authenticated owner surface from Task 091 remains supportable/readiness-only; do not send content;
- SQLite integrity `ok`;
- Task-092 retired evidence unchanged;
- Task-096 creates zero new Tickets, semantic events, response/delivery rows, outbox work or provider inference;
- unrelated OpenClaw configuration remains unchanged except expected supported installer-owned CogentNexus surfaces;
- Ollama model inventory remains the accepted model set and no direct model invocation occurs.

If any durable semantic row appears during this task, stop and report it; Task 096 must be semantically silent.

---

# Phase E — natural supervisor/no-flash proof

Because the supported install updates/restarts the live integration, re-prove supervisor stability using natural scheduling rather than manually forcing ticks.

Observe at least five natural PT1M supervisor ticks after MANAGED restoration.

Require:

- no visible flashing console/window attributable to CogentNexus/OpenClaw child process launches;
- controller remains MANAGED throughout;
- Gateway remains healthy;
- Supervisor remains healthy;
- no unexpected provider call;
- no semantic Ticket/event creation;
- no recovery churn or duplicate plugin generation appears.

Result token for this sub-gate:

`NO_FLASH_MULTI_TICK_REPROVEN`

If the operator reports visible flashing during the observation window, treat that as a blocker even if machine-readable health is otherwise green.

---

# Phase F — read-only final fresh-session readiness

Do not send a message.

Using the already accepted authenticated Dashboard/WebChat owner surface, prove only readiness for the final semantic successor:

- Control UI can connect as authenticated operator/admin without exposing bearer secret;
- `sessions.list` or equivalent read-only method works;
- New Chat control is present/usable as a staged UI action only if exercising it produces no semantic send and no Ticket/provider call;
- do not create a semantic nonce;
- do not perform the final first send in Task 096.

The final semantic task remains responsible for proving a newly materialized session after first send and post-completion New Session continuity.

Readiness token:

`DASHBOARD_OWNER_FRESH_SESSION_READY_NO_SEND`

If exercising New Chat itself risks an external semantic effect in this exact OpenClaw build, do not click it; prove owner/control readiness read-only and report that first-send materialization remains deferred.

---

# Required verification summary

For PASS record at least:

- exact execution/source implementation SHA;
- candidate and pre-install live v2 fingerprints and their inequality;
- production classifier `upgrade / pending=false / exact=false`;
- production actions `install=true / rollover=true`;
- supported installer invocation count 1, retry 0, exit 0;
- proof npm pack + supported plugin install actually executed;
- transient/final generation topology and rollover backup;
- final candidate/live v2 fingerprint equality;
- final canonical payload file-set parity;
- MANAGED/controller/startup/Supervisor/AGENTS/ownership health;
- Gateway/OpenClaw/Ollama/SQLite health;
- Task-092 retired evidence unchanged;
- zero Task-096 semantic/provider activity;
- five natural PT1M ticks and `NO_FLASH_MULTI_TICK_REPROVEN`;
- owner Dashboard readiness with no send;
- no manual repair/retry.

---

# Publication fence

This is a live evidence task and should not modify product source.

Execution HEAD is the coordination HEAD at task start; exact deploy source remains separately pinned to implementation `32212a4331e1f32b5a130bd30d271d4cbc56f6c1`.

Publish exactly one report-only commit:

`docs/operations/coordination/reports/CNX-20260827-096-live-install-repaired-staging-and-restore-parity.md`

Required result tokens:

- `PASS_REPAIRED_STAGING_LIVE_INSTALLED_PARITY_READY`
- `BLOCKED_PREINSTALL_TOPOLOGY_OR_ATTESTATION`
- `BLOCKED_SUPPORTED_INSTALL_OVER`
- `BLOCKED_PACKAGE_INSTALL_NOT_PROVEN`
- `BLOCKED_ROLLOVER_OR_OWNERSHIP_CONVERGENCE`
- `BLOCKED_MANAGED_PARITY_OR_HEALTH`
- `BLOCKED_NO_FLASH_REPROOF`
- `BLOCKED_OWNER_SURFACE_READINESS`
- `BLOCKED_UNEXPECTED_SEMANTIC_OR_PROVIDER_ACTIVITY`
- `BLOCKED_EVIDENCE_PUBLICATION_UNSAFE`

## Successor gate

Only independent acceptance of:

`PASS_REPAIRED_STAGING_LIVE_INSTALLED_PARITY_READY`

may authorize one new final authenticated fresh-session semantic attempt.

That final successor must use a brand-new nonce exactly once through the authenticated Dashboard/WebChat owner surface, create/use a genuinely fresh session, prove Ticket acceptance/routing before Ollama, prove durable final-payload staging before native visibility, prove exact delivery settlement to `completed`, and then prove New Session can be entered again without stale/unknown-parent failure and without additional semantic/provider effects.