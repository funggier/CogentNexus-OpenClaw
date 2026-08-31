# CNX-20260827-090 — Live Pending-Rollover Recovery Retry After Published Boundary Fix

Status: `READY_FOR_HERMES`

Execution mode: `LIVE_SUPPORTED_PENDING_ROLLOVER_RECOVERY_RETRY`

Current authorization: `ONE_SUPPORTED_PENDING_RECOVERY_RETRY_AFTER_PUBLISHED_FIX_AUTHORIZED`

Owner: ChatGPT

Executor: Hermes/Codex after operator continuation

## Goal

Use exactly one supported normal install-over from independently accepted source `d6daf8f93fcd5578f267b2017c6cc82e5de20095` to recover the preserved Task-087 two-generation PASSTHROUGH topology, complete the already-installed attested pending rollover without creating a third plugin generation, restore the product to MANAGED state, and prove exact source/live parity, owned-runtime health, five natural no-flash Supervisor ticks, and authenticated Dashboard/WebChat owner-surface readiness without sending a semantic message.

This is not the final semantic acceptance task.

## Exact accepted source

Use exactly:

`d6daf8f93fcd5578f267b2017c6cc82e5de20095`

This source includes:

- accepted Task-078/079/080 semantic/delivery/security fixes;
- accepted Task-082 npm-pack boundary repair;
- Task-084 source fingerprint attestation and rollover plan/apply binding;
- Task-085 classification/source-equality truth table;
- Task-086 independent production install/rollover gates and AST regression;
- Task-089 published PowerShell named-parameter caller repair.

Do not mix later unreviewed production source into this live attempt.

## Accepted predecessor review

Task 089 report:

`docs/operations/coordination/reports/CNX-20260827-089-recover-and-publish-task088-implementation.md`

Report HEAD:

`ebd6df825f6b84e68edd2ba24869333154be48c6`

Independent review:

Decision: `ACCEPT`

Disposition:

`ACCEPT_ACTION_RESOLVER_BOUNDARY_PUBLISHED_SAFE`

Review path:

`docs/operations/coordination/reviews/CNX-20260827-089-recover-and-publish-task088-implementation.md`

## Preserved live starting topology

Task 087 stopped on the action-resolver parameter boundary before pending rollover. Tasks 088/089 were source-only and did not mutate live state.

Before mutation Task 090 must re-prove the exact live baseline, expected to remain:

- OpenClaw `2026.7.1-2`;
- controller `passthrough`, generation `13` unless a read-only natural state field changed without product mutation;
- startup disabled;
- Supervisor Scheduled Task absent;
- AGENTS managed block absent;
- ownership manifest points to prior generation `g-5593cbcfff5b35d5`;
- prior generation fingerprint `7e9189f81eeda728a35a0722f69cfd4a3b48e0fac36fde8d846a188072577332`;
- active/registered disabled replacement `g-7257c4555ca8ad21`;
- replacement fingerprint `8fd911e3b8f6326c8907b7d92c11028d931df203dcaafdb59cc1e6d0a3b56360`;
- exact accepted source plugin fingerprint equals the replacement fingerprint;
- exactly two canonical CogentNexus npm generations;
- no third generation;
- Gateway healthy/dashboard reachable;
- Ollama healthy with the accepted four-model inventory;
- authoritative SQLite integrity `ok`, Tickets/outbox zero;
- no semantic/provider run active.

If another actor materially changed, deleted, normalized, enabled, replaced or rewrote this topology, stop before the installer and report `BLOCKED_PENDING_RECOVERY_STATE_DRIFT`.

---

# Absolute mutation and semantic fences

## Only authorized product-changing operation

Exactly one supported normal install-over from exact source `d6daf8f9...`:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1 -Workspace C:\Users\CDQ-P\.openclaw\workspace -Provider ollama
```

Equivalent invocation is allowed only if it runs the same exact script/source/arguments under the supported Windows PowerShell host.

Installer-internal lifecycle actions are authorized only as effects of this one command.

## Forbidden

Do NOT:

- invoke the installer a second time after any nonzero result;
- uninstall;
- reset;
- clean reinstall;
- manually delete/move/rename/enable/disable either plugin generation;
- manually edit ownership/controller/startup/Supervisor/AGENTS/config/runtime/launcher;
- use `SkipPlugin`, `SkipAgentsPolicy`, `LinkPlugin`, developer bypasses or ad-hoc repair flags;
- manually run rollover-plan/apply outside the installer;
- manually create/delete/replace Supervisor;
- mutate SQLite/Ticket/session state;
- send Dashboard/WebChat messages;
- call `chat.send`, `openclaw agent`, `sessions_send`, channel sends or any semantic/user surface;
- create or consume the final semantic nonce;
- call Ollama directly;
- change provider/model/timeouts;
- restart Gateway/Ollama/Supervisor merely to manufacture a passing result outside installer-supported behavior;
- reboot;
- merge, tag or release.

If the one install-over returns nonzero, capture read-only state and stop.

---

# Phase A — execution fence and pre-mutation re-proof

Before mutation:

1. fetch current coordination branch and record exact execution HEAD;
2. prove Task-089 report and ACCEPT review are ancestors;
3. create/use a clean isolated deployment checkout at exact `d6daf8f93fcd5578f267b2017c6cc82e5de20095`;
4. verify exact HEAD and clean status;
5. record Windows, PowerShell, Node, npm and OpenClaw versions;
6. re-prove the accepted live topology read-only.

Required evidence:

- recovery preflight = `OWNERSHIP_PRESENT`;
- controller mode = `passthrough`;
- ownership manifest old-generation path exact;
- exactly two canonical managed npm generations;
- canonical OpenClaw registration points to newer replacement and is disabled;
- source candidate plugin fingerprint from production `plugin-fingerprint`;
- old live fingerprint;
- replacement live fingerprint;
- replacement fingerprint == source fingerprint;
- old fingerprint != replacement fingerprint;
- authoritative SQLite path, integrity and counts;
- Gateway/dashboard health;
- Ollama health/model inventory via normal read-only supported surfaces only;
- no semantic/provider run.

Run read-only attested classification using production classifier + captured OpenClaw plugin inventory.

Required result:

```text
mode=upgrade
pendingRollover=true
pluginAlreadyExact=false
manifestPluginPath=<prior generation>
replacementPluginPath=<newer generation>
expectedReplacementFingerprint=<exact source fingerprint>
```

Run the production lifecycle action resolver using the same **named-parameter boundary now present in production**.

Required result:

```text
installPlugin=false
rolloverPlugin=true
```

Also perform a focused read-only PowerShell check proving the Task-087 `Mode="-Mode"` error no longer occurs with the production named caller pattern.

If any required value differs, stop before mutation with `BLOCKED_PENDING_RECOVERY_PREFLIGHT`.

---

# Phase B — exact candidate preflight

In the isolated exact source only:

1. run Task-089 action-resolver caller boundary regression;
2. run Task-086 production AST helper and require:
   - package install under `installPlugin`;
   - rollover under `rolloverPlugin`;
   - rollover not under `installPlugin`;
   - rollover before strict `resolve-plugin`;
3. run focused Task-085 classification/action tests;
4. run candidate plugin validation sufficient to prove source readiness;
5. verify zero diff under `plugins/cogentnexus-openclaw/**` from accepted payload lineage.

Do not create/install a live npm artifact in this phase.

If candidate preflight fails, stop before mutation with `BLOCKED_PENDING_RECOVERY_CANDIDATE_PREFLIGHT`.

---

# Phase C — exactly one supported live install-over

Invoke the authorized installer exactly once and capture complete stdout/stderr/exit status.

Required invocation count:

`1`

Required retry count:

`0`

If exit is nonzero, stop immediately after read-only post-failure capture and report a blocker. Do not repair or retry.

## C1 — action boundary must pass

The invocation must get beyond the Task-087 failure boundary.

There must be no:

`Cannot validate argument on parameter 'Mode'`

or equivalent action-resolver parameter-binding failure.

Prove the live invocation resolves:

- `mode=upgrade`;
- `pendingRollover=true`;
- `pluginAlreadyExact=false`;
- `installPlugin=false`;
- `rolloverPlugin=true`.

## C2 — zero replacement package creation

For this pending path prove zero execution of:

- `npm pack --json` after classification;
- `Resolve-NpmPackArtifact` artifact selection;
- `openclaw plugins install`;
- creation of any new CogentNexus `g-*` npm generation.

Candidate-side `npm ci`/validation before fingerprint derivation is allowed and is not a plugin-generation mutation.

Capture generation inventory before mutation and immediately after rollover. No third generation may exist at any observed point.

## C3 — attested pending rollover

Prove installer performs reviewed rollover against existing two-generation state:

1. fresh OpenClaw inventory captured;
2. rollover-plan called with exact expected source fingerprint;
3. plan returns a nonempty exact hash;
4. inventory re-proved immediately before apply;
5. rollover-apply succeeds using exact plan hash;
6. old generation is atomically retired to product-owned backup boundary;
7. manifest is rebound to existing source-exact replacement;
8. canonical generation count converges `2 -> 1`;
9. surviving canonical generation is exactly `g-7257c4555ca8ad21` or the same exact project/root if OpenClaw representation differs read-only;
10. surviving fingerprint equals exact accepted source fingerprint;
11. no third semantic generation was created.

If rollover fails, stop with read-only state capture. Do not manually repair.

---

# Phase D — supported MANAGED restoration

Only if the one installer continues successfully after rollover, prove its normal supported lifecycle restores:

- ownership manifest exact verification;
- launcher using product-owned Python runtime;
- managed AGENTS block;
- controller MANAGED;
- startup enabled per product contract;
- Supervisor Scheduled Task restored;
- plugin canonical registration enabled/healthy as expected by managed state;
- no legacy/shared/foreign plugin generation adopted.

No manual enable/repair is allowed outside installer behavior.

---

# Phase E — source/live parity and health

Prove after successful installer exit:

1. installed skill parity against exact source `d6daf8f9...`;
2. installed plugin payload parity against exact source plugin fingerprint and expected file set;
3. one canonical CogentNexus plugin generation only;
4. ownership verify passes;
5. product-owned runtime manifest/interpreters valid;
6. launcher points to product-owned foreground interpreter;
7. Supervisor task/background interpreter product-owned;
8. Gateway healthy and dashboard reachable;
9. Ollama healthy with exact accepted four models unchanged;
10. SQLite integrity `ok`, Tickets/outbox remain zero;
11. unrelated OpenClaw configuration remains intact;
12. no legacy generation becomes active;
13. no semantic/provider activity was created by the task.

Do not use direct Ollama inference probes.

---

# Phase F — five natural PT1M no-flash ticks

Observe at least five **natural** Supervisor PT1M cycles after successful MANAGED restoration.

Do not manually invoke Supervisor to simulate ticks.

For each tick collect sufficient evidence to correlate:

- scheduler/task execution timestamp;
- supervisor/runtime log activity;
- child process command line/path where observable;
- foreground/background interpreter choice;
- absence of terminal-window or user-visible console spawning according to the accepted no-flash evidence method.

Required final token:

`NO_FLASH_MULTI_TICK_PROVEN`

If five natural ticks cannot be observed or evidence is ambiguous, report `BLOCKED_NO_FLASH_EVIDENCE` rather than infer success.

---

# Phase G — Dashboard/WebChat owner-surface readiness, read-only

Without sending a semantic message, prove a fresh authenticated Dashboard/WebChat surface can provide the owner-authenticated signal required by accepted semantic admission logic.

Allowed:

- open/connect/authenticate to Dashboard/WebChat if needed;
- inspect read-only authenticated client/session metadata;
- prove owner/admin scope and supported surface identity;
- prepare a fresh session for the future final semantic task.

Forbidden:

- sending text;
- `chat.send`;
- synthetic user message;
- final nonce;
- `openclaw agent`;
- provider inference.

Required token:

`DASHBOARD_OWNER_SURFACE_READY`

If owner-authenticated readiness cannot be proven without a message, report `BLOCKED_OWNER_SURFACE_READINESS` and stop. Do not weaken owner policy.

---

# Final verification and report

Report path:

`docs/operations/coordination/reports/CNX-20260827-090-live-pending-rollover-recovery-retry-after-published-boundary-fix.md`

Required result tokens:

- `PASS_LIVE_PENDING_RECOVERY_PARITY_NO_FLASH_OWNER_SURFACE_READY`
- `BLOCKED_PENDING_RECOVERY_STATE_DRIFT`
- `BLOCKED_PENDING_RECOVERY_PREFLIGHT`
- `BLOCKED_PENDING_RECOVERY_CANDIDATE_PREFLIGHT`
- `BLOCKED_ACTION_RESOLVER_BOUNDARY_LIVE`
- `BLOCKED_SUPPORTED_PENDING_RECOVERY_INSTALL_OVER`
- `BLOCKED_PENDING_ROLLOVER_APPLY`
- `BLOCKED_MANAGED_RESTORATION`
- `BLOCKED_SOURCE_LIVE_PARITY`
- `BLOCKED_RUNTIME_OR_HEALTH`
- `BLOCKED_NO_FLASH_EVIDENCE`
- `BLOCKED_OWNER_SURFACE_READINESS`
- `BLOCKED_EVIDENCE_PUBLICATION_UNSAFE`

Mutation accounting must explicitly include:

- supported installer invocation count;
- retry count;
- package install count;
- generation count before/after;
- manual repair count;
- semantic message count;
- direct provider probe count;
- restart/reboot count outside installer-supported effects.

Task 090 should produce no product source change. Publish only the report in a report-only commit from the execution coordination HEAD unless a blocker requires no report publication.

## Successor gate

Only independent acceptance of:

`PASS_LIVE_PENDING_RECOVERY_PARITY_NO_FLASH_OWNER_SURFACE_READY`

may authorize the final semantic acceptance task.

That final task may send exactly one fresh authenticated Dashboard/WebChat owner message with a new nonce and must prove:

`owner message -> durable Ticket accepted before correlated provider inference -> exactly one route -> response_ready -> exact owner/run delivery_confirmed -> completed -> exactly one visible nonce response`

The Task-076 nonce and session remain permanently retired.
