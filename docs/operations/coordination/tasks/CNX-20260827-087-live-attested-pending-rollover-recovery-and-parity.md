# CNX-20260827-087 — Live Attested Pending-Rollover Recovery and Parity

Status: `READY_FOR_HERMES`

Execution mode: `LIVE_SUPPORTED_ATTESTED_PENDING_ROLLOVER_RECOVERY`

Current authorization: `ONE_SUPPORTED_PENDING_RECOVERY_INSTALL_OVER_AUTHORIZED`

Owner: ChatGPT

Executor: Hermes/Codex after operator continuation

## Goal

Use exactly one supported normal install-over from the independently accepted Task-086 source to recover the preserved Task-083 two-generation PASSTHROUGH topology by completing the already-installed **attested pending rollover without creating a third plugin generation**, then restore the product to MANAGED state and prove exact source/live parity, owned runtime health, five natural no-flash Supervisor ticks, and authenticated Dashboard/WebChat owner-surface readiness without sending a semantic message.

This is still not the final semantic acceptance task.

## Exact accepted source

Use exactly:

`71f48c1a134ee9b2646b4cc7f077abe9cae59ebb`

This source contains:

- accepted Task-078/079/080 semantic/delivery/security fixes;
- accepted Task-082 npm-pack boundary repair;
- Task-084 source-fingerprint and rollover attestation primitives;
- Task-085 corrected classification/source-equality truth table;
- accepted Task-086 independent production rollover gate.

Do not mix later unreviewed production source into this live attempt.

## Accepted predecessor review

Task 086 report:

`docs/operations/coordination/reports/CNX-20260827-086-fix-production-pending-rollover-gate-nesting.md`

Report HEAD:

`1430d0a23ee2c477fdb5c2015f262c9df09c83df`

Independent review:

Decision: `ACCEPT`

Disposition:

`ACCEPT_PENDING_ROLLOVER_PRODUCTION_GATE_REPAIRED`

Review path:

`docs/operations/coordination/reviews/CNX-20260827-086-fix-production-pending-rollover-gate-nesting.md`

## Accepted live starting topology

The live product must still match the fail-closed Task-083 residue before mutation:

- OpenClaw `2026.7.1-2`;
- controller `passthrough`, generation `13` unless a read-only natural state detail has changed without mutation;
- startup disabled;
- Supervisor Scheduled Task absent;
- AGENTS managed block absent;
- ownership manifest points to prior generation `g-5593cbcfff5b35d5`;
- prior generation fingerprint begins `7e9189f8...`;
- active/registered disabled replacement is `g-7257c4555ca8ad21`;
- replacement fingerprint begins `8fd911e3...` and equals the exact accepted candidate-source plugin fingerprint;
- exactly two canonical CogentNexus npm generations are present;
- Gateway remains healthy/dashboard reachable;
- Ollama remains healthy with the accepted four-model inventory;
- SQLite integrity remains `ok`, Tickets/outbox remain zero;
- no semantic/provider run is active.

If another actor has normalized, deleted, replaced, enabled, or otherwise materially mutated this topology, stop before the installer and report `BLOCKED_PENDING_RECOVERY_STATE_DRIFT`.

---

# Absolute mutation and semantic fences

## Only authorized product-changing operation

Exactly one supported normal install-over from exact source `71f48c1a...`:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1 -Workspace C:\Users\CDQ-P\.openclaw\workspace -Provider ollama
```

Equivalent invocation is allowed only if it runs the same exact script/source/arguments under the supported Windows PowerShell host.

Installer-internal lifecycle actions are allowed as part of this one command.

## Forbidden

Do NOT:

- invoke the installer a second time after any nonzero result;
- uninstall;
- reset;
- clean reinstall;
- manually delete, move, rename, enable, disable, or edit either plugin generation;
- manually edit ownership manifest/controller/startup/Supervisor/AGENTS/config/runtime/launcher;
- use `SkipPlugin`, `SkipAgentsPolicy`, `LinkPlugin`, developer bypasses or ad-hoc repair flags;
- manually execute rollover-plan/apply outside the supported installer;
- manually create/delete/replace Supervisor;
- mutate SQLite/Ticket/session state;
- send Dashboard/WebChat messages;
- call `chat.send`, `openclaw agent`, `sessions_send`, channel sends or equivalent semantic/user surfaces;
- generate or consume the final semantic nonce;
- call Ollama directly;
- change provider/model/timeouts;
- restart Gateway/Ollama/Supervisor merely to obtain a passing result outside installer-supported behavior;
- reboot;
- merge, tag or release.

If the one install-over fails, capture read-only state and stop.

---

# Phase A — execution fence and pre-mutation re-proof

Before mutation:

1. fetch the coordination branch and record exact execution HEAD;
2. prove Task-086 report and ACCEPT review are ancestors;
3. use a clean isolated deployment checkout at exact `71f48c1a134ee9b2646b4cc7f077abe9cae59ebb`;
4. verify exact HEAD and clean status;
5. record Windows PowerShell, Node, npm and OpenClaw versions;
6. re-prove the accepted live topology read-only.

Required pre-mutation evidence:

- recovery preflight = `OWNERSHIP_PRESENT`;
- controller mode = `passthrough`;
- ownership manifest old-generation path exact;
- exactly two canonical managed npm generations present;
- OpenClaw canonical registration points to the newer replacement and is disabled;
- source candidate plugin fingerprint from production `plugin-fingerprint`;
- old live fingerprint;
- replacement live fingerprint;
- replacement live fingerprint == exact candidate-source fingerprint;
- old fingerprint != replacement fingerprint;
- authoritative SQLite path/integrity/counts;
- Gateway/dashboard health;
- Ollama health/model list;
- no semantic run.

Then run **read-only attested classification** using the production classifier and captured OpenClaw inventory.

Required result:

- `mode=upgrade`;
- `pendingRollover=true`;
- `pluginAlreadyExact=false`;
- manifestPluginPath = prior generation;
- replacementPluginPath = newer generation;
- expectedReplacementFingerprint = exact source fingerprint.

Run the production lifecycle action resolver with this tuple.

Required result:

- `installPlugin=false`;
- `rolloverPlugin=true`.

If any required value differs, stop before mutation with `BLOCKED_PENDING_RECOVERY_PREFLIGHT`.

---

# Phase B — candidate source preflight

In the isolated exact source only:

1. verify Task-086 AST helper reports production rollover outside `installPlugin` and under `rolloverPlugin`;
2. verify rollover precedes strict `resolve-plugin`;
3. run focused Task-086 lifecycle/AST test;
4. run focused Task-085 classification/action tests;
5. run candidate plugin validation only as needed to prove source readiness.

Do not create or install a live npm artifact in this phase.

If candidate preflight fails, stop before mutation with `BLOCKED_PENDING_RECOVERY_CANDIDATE_PREFLIGHT`.

---

# Phase C — exactly one supported live install-over

Invoke the authorized installer exactly once and capture complete stdout/stderr/exit status.

The Task-087 pending path has an unusually strict evidence requirement because it must reuse the existing source-exact replacement rather than create another one.

## C1 — required classification/action evidence inside the live invocation

Prove the invocation follows:

`upgrade + pending=true + exact=false`

and resolves actions:

- installPlugin = false;
- rolloverPlugin = true.

## C2 — required negative package-creation evidence

For this live invocation, prove **zero execution** of replacement-package creation/install actions after classification:

- no `npm pack --json`;
- no `Resolve-NpmPackArtifact` package selection;
- no `openclaw plugins install`;
- no new `g-*` CogentNexus npm generation;
- no third canonical CogentNexus generation at any observed post-classification point.

Candidate-side `npm ci`/validation used before fingerprint derivation is allowed and is not a plugin-generation mutation.

## C3 — required pending rollover evidence

Prove the installer instead:

1. captures fresh plugin inventory;
2. builds rollover plan with the exact expected source fingerprint;
3. binds manifest-owned prior generation as retired;
4. binds active source-exact replacement as replacement;
5. re-captures inventory immediately before apply;
6. applies the exact reviewed plan hash;
7. atomically retires the old managed npm project into the product backup boundary;
8. updates ownership binding to the existing replacement;
9. leaves exactly one canonical runtime-resolvable CogentNexus generation.

Record old/new project paths, fingerprints, plan SHA-256 and backup path.

Required installer exit:

`0`

If the installer returns nonzero, do not retry. Capture read-only post-failure topology and report `BLOCKED_SUPPORTED_PENDING_RECOVERY_INSTALL_OVER`.

---

# Phase D — generation-count and source/live parity proof

After successful install-over, prove:

## D1 — generation convergence

- pre-install canonical generation count = `2`;
- no third generation was created during Task 087;
- post-rollover active canonical generation count = `1`;
- surviving generation is the former Task-083 replacement;
- prior generation is outside active resolution in the exact product rollover backup boundary;
- generic strict `resolve-plugin` now succeeds uniquely.

## D2 — plugin parity

Against exact source `71f48c1a...`:

- surviving installed plugin fingerprint equals exact source plugin fingerprint;
- runtime-relevant package file list and per-file hash/equivalent package parity show zero unexplained differences;
- package metadata, manifest, `dist` and packaged scripts match the exact accepted plugin payload.

Task-086 itself did not change `plugins/cogentnexus-openclaw/**`; therefore the expected plugin fingerprint should remain the Task-083 source-exact fingerprint. Record the exact full hash, do not rely only on prefix.

## D3 — installed skill parity

Compare installed `skills\cogentnexus-openclaw` against exact source `71f48c1a...` using normalized relative file paths and SHA-256, excluding only known runtime caches such as `__pycache__`.

Require zero unexplained differences.

If parity fails, report `BLOCKED_PENDING_RECOVERY_SOURCE_LIVE_PARITY`.

---

# Phase E — MANAGED/startup/runtime restoration

Require all after successful installer completion:

1. controller = `managed`;
2. desired Gateway/provider = running;
3. startup policy enabled/installed as expected;
4. Supervisor Scheduled Task exists and is healthy/Ready with PT1M trigger;
5. Supervisor is Hidden as expected;
6. Supervisor executable is product-owned background `pythonw.exe` under `%LOCALAPPDATA%\CogentNexus-OpenClaw\runtime\python\...`;
7. Supervisor arguments point to installed CogentNexus host-control source, not temp checkout/Hermes/Codex;
8. launcher uses product-owned foreground `python.exe`;
9. ownership verification passes through owned runtime;
10. AGENTS managed block exists exactly once and stripped baseline remains accepted;
11. exactly one canonical CogentNexus plugin is enabled/loaded;
12. Ticket-first/pre-inference/direct-delivery/recovery config remains accepted;
13. SQLite integrity `ok`;
14. no unexpected Ticket/outbox/recovery work created;
15. Gateway and dashboard remain healthy;
16. Ollama remains healthy with same accepted four models;
17. unrelated plugin/config state remains unchanged.

If restoration is incomplete despite installer exit zero, report `BLOCKED_POST_PENDING_RECOVERY_HEALTH`.

---

# Phase F — natural five-tick no-flash acceptance

Observe at least five **natural** Supervisor PT1M ticks after successful recovery.

Do not force-run the task as a substitute.

For each distinct tick record:

- timestamp;
- LastRunTime / LastTaskResult;
- relevant process ancestry/descendants when observable;
- absence of CogentNexus-caused `conhost.exe`, console `python.exe`, Hermes/uv-agent trampoline, `cmd.exe`, PowerShell wrapper or temp-worktree executable chain.

Required classification:

`NO_FLASH_MULTI_TICK_PROVEN`

If natural ticks fail or a causal console flash is observed, report `BLOCKED_NO_FLASH_OR_RUNTIME_BINDING`.

---

# Phase G — authenticated Dashboard/WebChat owner-surface readiness, zero messages

Do not send a user message.

Use exact installed OpenClaw `2026.7.1-2` source/help/runtime metadata and accepted Task-077 findings to re-prove the supported authenticated control-UI surface that the final semantic task will use.

Record:

- dashboard URL/HTTP readiness;
- exact supported first-send surface;
- expected owner/dashboard session namespace only where proven by exact OpenClaw evidence;
- how `before_agent_run` receives trusted owner/session metadata on that surface;
- why the existing `durableAdmissionEligible()` policy admits it;
- why `openclaw agent --session-key agent:main:main` remains forbidden as an owner-authentication substitute.

If creating a fresh Dashboard/WebChat session itself would consume the first message, do not create it. Document exact first-send procedure for the final task instead.

Required result:

`DASHBOARD_OWNER_SURFACE_READY`

If this cannot be established read-only, report `BLOCKED_DASHBOARD_OWNER_SURFACE_READINESS`.

---

# Phase H — final read-only health snapshot

Re-record after the five-tick window:

- controller MANAGED;
- one canonical enabled/loaded source-exact plugin;
- ownership verification;
- startup/Supervisor healthy with owned-runtime binding;
- AGENTS one managed block;
- Gateway/dashboard healthy;
- Ollama healthy/same model list;
- SQLite integrity;
- Ticket/event/outbox counts and pending recovery state;
- no semantic/provider message generated by Task 087;
- unrelated config preserved.

---

# Publication fence

Task 087 is a live task and must not change product source.

Publish only:

`docs/operations/coordination/reports/CNX-20260827-087-live-attested-pending-rollover-recovery-and-parity.md`

in one report-only commit after execution.

The report must include:

- execution HEAD;
- exact source `71f48c1a...`;
- pre-mutation two-generation topology and full fingerprints;
- attested classifier output;
- lifecycle action output;
- exact one installer invocation and exit status;
- explicit evidence that `npm pack` / artifact resolver / `openclaw plugins install` did not execute in the pending path;
- generation-count timeline proving no third generation;
- rollover plan/apply evidence and backup path;
- plugin and skill source/live parity;
- MANAGED/startup/Supervisor/AGENTS/runtime/ownership/Gateway/Ollama/SQLite evidence;
- five natural PT1M ticks/no-flash classification;
- Dashboard/WebChat owner-surface readiness evidence;
- semantic/provider mutation accounting;
- publication fence.

## Result tokens

Use exactly one:

- `PASS_LIVE_ATTESTED_PENDING_RECOVERY_PARITY_NO_FLASH_OWNER_SURFACE_READY`
- `BLOCKED_PENDING_RECOVERY_STATE_DRIFT`
- `BLOCKED_PENDING_RECOVERY_PREFLIGHT`
- `BLOCKED_PENDING_RECOVERY_CANDIDATE_PREFLIGHT`
- `BLOCKED_SUPPORTED_PENDING_RECOVERY_INSTALL_OVER`
- `BLOCKED_PENDING_RECOVERY_CREATED_THIRD_GENERATION`
- `BLOCKED_PENDING_RECOVERY_SOURCE_LIVE_PARITY`
- `BLOCKED_POST_PENDING_RECOVERY_HEALTH`
- `BLOCKED_NO_FLASH_OR_RUNTIME_BINDING`
- `BLOCKED_DASHBOARD_OWNER_SURFACE_READINESS`
- `BLOCKED_EVIDENCE_PUBLICATION_UNSAFE`

## Successor logic

Only an independently accepted:

`PASS_LIVE_ATTESTED_PENDING_RECOVERY_PARITY_NO_FLASH_OWNER_SURFACE_READY`

may authorize the final semantic acceptance task.

That final task will send exactly one fresh authenticated Dashboard/WebChat owner message with a unique new nonce and must prove:

`authenticated owner message`
`-> durable Ticket accepted event before provider inference starts`
`-> routed direct lane`
`-> correlated OpenClaw/Ollama inference`
`-> response_ready`
`-> exact owner/run delivery confirmation`
`-> completed`
`-> exactly one visible nonce response`

The retired Task-076 nonce must never be reused.

No merge/tag/release is implied by Task 087.