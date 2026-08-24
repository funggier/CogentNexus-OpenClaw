# CNX-20260825-061 — Return to Verified MANAGED Lifecycle

Status: **BLOCKED**

Result: `BLOCKED_POST_ENABLE_VERIFICATION`

Current authorization: `MANAGED_REENTRY_AUTHORIZED`

Repository: `funggier/CogentNexus-OpenClaw`

Branch: `agent/v0.9.3-recovery-reality-tests`

Executor: Hermes (operator-selected substitute for Codex)

Fetched execution HEAD: `504dad20f1122c29e77321982980e7d3de72a4de`

## Authorization and accepted predecessor

- Task 060 result `PASS_PLUGIN_GENERATION_ROLLOVER_APPLIED_PASSTHROUGH` accepted by ChatGPT with disposition `ACCEPT_PLUGIN_GENERATION_ROLLOVER_APPLIED_PASSTHROUGH` (review commit `633cefcfe06c83aae8aede17f3bf6b36ed4d3eb7`).
- Accepted post-rollover ownership-manifest SHA-256: `0667004DC9D6483450A3C99DDA6F34BB7F384F0261F43813763019E2C3BA0341`.
- Task 061 published as the next bounded lifecycle step; `ACTIVE.md` shows `MANAGED_REENTRY_AUTHORIZED`.
- Manual continuation signal (operator `ต่อ`) authorized execution of exactly Task 061.

## Evidence boundary

Retained isolated clone:

`C:\Users\CDQ-P\AppData\Local\Temp\cnx061-exec-20260824T202211Z\repo`

Retained evidence directory (unique):

`C:\Users\CDQ-P\AppData\Local\Temp\cnx061-managed-reentry-20260824T202213Z`

Contents: `EVIDENCE_DIR.txt`, `01-clone-and-codeid.txt`, `02-c1-c2.txt`, `c1-status.json`, `c1-gateway.json`, `c1-ollama.txt`, `c1-sqlite.json`, `c1-verify.txt`, `c1-resolve.txt`, `task061-pre-enable-plugins-list.raw.json`, `03-c3-selftest.txt`, `c3-selftest.txt`, `cnxclaw-enable-shim.ps1`, `run-enable.ps1`, `04-c4-enable.txt`, `c4-enable-stdout.log`, `c4-enable-stderr.log`, `c4-enable-poststate.json`, `05-c5-part1.txt`, `c5-status.json`, `c5-tasks.json`, `c5-sqlite.json`, `06-c5-part2.txt`, `task061-post-enable-plugins-list.raw.json`.

## Phase C1 — accepted post-rollover preflight (passed)

Read-only: controller `passthrough`/gen 7, desiredGateway `running`, desiredProvider `unchanged`, selectedProvider `ollama`, startup `disabled`, no CogentNexus adapter; Gateway healthy; Ollama same four models; SQLite `ok`/0; ownership SHA `0667004D…` (accepted); `namespace_ownership.py verify` exit 0; `resolve-plugin` exit 0 resolving replacement payload; retired root absent; rollover backup tree `05981336…`, replacement tree `3621dbb4…`; registered policy `14EDEAD0…`; AGENTS baseline `C9A664B7…` (zero managed markers). Pre-enable inventory: 1 canonical v0.9.3 disabled at replacement root.

## Installed-vs-clone code identity gate (passed)

All six installed execution files are byte-identical to the fresh clone: `host.py` `5D5CB5D4…`, `runtime.py` `F65ADFD0…`, `startup.py` `B60C7BD1…`, `host_control.py` `CFD1B296…`, `windows-task.xml` `3BD8F591…`, `AGENTS.cogentnexus-openclaw.md` `51EA03C2…`. Installed launcher `cnxclaw.cmd` SHA `8DB1F256BB56C298FFFB14E8A761CAA7DBEC56EA334B0F4558C3CDA563AA46EF` matches the required expected value (the repo does not itself carry `cnxclaw.cmd`; verified by expected-SHA comparison).

## Phase C2 — pre-enable bounded config observation (baseline only)

Read individually: `ticketFirst=true`, `allowConversationAccess=true`; the remaining managed keys (`preInferenceAdmission`, `autoWorkflowCompletion`, `enforcedMode`, `autoResume`, `workspaceDir`, `ticketDispatchLimit`, `ticketMaximumRunning`, `ticketMaximumAttempts`, `ticketRecoveryPollMs`, `ticketDispatchPollMs`, `ticketOutboxPollMs`) were empty — expected while product was PASSTHROUGH (baseline evidence only, not required pre-configured).

## Phase C3 — root-process self-test (passed)

`scripts/invoke-root-process-exact.ps1 -SelfTest` exit 0: numeric `0`/`7` preserved, null rejection PASS, argument round-trip PASS.

## Phase C4 — execute supported MANAGED re-entry (executed once)

Invoked exactly once through the wrapper via a PowerShell shim (`cnxclaw.cmd enable`):

- `cnxclaw enable` invocation count = `1`;
- observed numeric exit code = `0`;
- enable stdout `result: ok`, host `mode: managed`, `policyChanged: true`, registered policy `14edead0180690c3d9565e864d2bdaaae60e32df9ef2c64eBD2A1238DF5CD8B4`, startup `policy: enabled`/`installed`, supervisor adapter `installed: true`/`State: Ready`/`Enabled: true`/`Hidden: true`, Gateway restart ok, Ollama healthy, sessionBootstrap ok, `recoveredTickets: []`;
- poststate: pid 27440, duration 164.725048s, observedExitCode 0, stdoutSha256 `CC48B8D15D0139F9BF67A2040E219159A3E5FABB9E5540D2B33BE4CCBAFE266E`.

## Phase C5 — post-enable MANAGED verification (PARTIAL — two mandatory postconditions FAILED)

### Passed

- controller mode exactly `managed`;
- desired Gateway `running`, desired provider `running`;
- startup policy exactly `enabled`; Windows Scheduled Task `CogentNexus-OpenClaw-Supervisor` exists, `Enabled: true`, `Hidden: true`, action `C:\Users\CDQ-P\AppData\Local\hermes\hermes-agent\venv\Scripts\pythonw.exe "C:\Users\CDQ-P\.openclaw\workspace\skills\cogentnexus-openclaw\scripts\host_control_v092.py" --root "C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw" supervisor tick --execute-safe`; no second/foreign CogentNexus supervisor task (only the bundled `OpenClaw Gateway` task coexists);
- Gateway healthy/reachable; Ollama healthy with the same four model identities; CNX SQLite integrity `ok` with zero tickets/events/outbox/sessions;
- ownership manifest SHA `0667004DC9D6483450A3C99DDA6F34BB7F384F0261F43813763019E2C3BA0341` unchanged; ownership still binds replacement payload; `namespace_ownership.py verify` exit 0; `resolve-plugin` exit 0 resolving exactly one canonical replacement payload; retired root still absent; rollover backup tree `05981336…` and replacement tree `3621dbb4…` unchanged;
- post-enable inventory: exactly one canonical `cogentnexus-openclaw` v0.9.3 at replacement root, `enabled=true`, `status=loaded`, `packageName` absent (71 unrelated plugin identities unchanged);
- `ticketFirst=true`, `hooks.allowConversationAccess=true`.

### FAILED (mandatory)

**F1 — AGENTS managed-block stripped baseline does not recreate the accepted pre-enable baseline.**
- accepted baseline SHA-256: `C9A664B73200AE5D6B0DA0908DE3256CDB4DDA8BA6FE99F5E6C5115C3983604C`;
- current AGENTS.md (with exactly one `<!-- cogentnexus-openclaw:begin -->` / one end marker) stripped of the managed block yields SHA-256 `EC6E95E0E28C72327B34C8062AECB962ECEF8A387B467C3E44A4ACEEFB4173A3` (canonical form `7147251E…`);
- the inserted managed-block content itself matches the registered managed policy (`14EDEAD0…`), but the **non-block** portion of AGENTS.md is no longer byte-identical to the accepted pre-enable baseline;
- `enable` did **not** create an `AGENTS.pre-host-change-*` backup in the workspace, so the supported path's own before-state copy is absent;
- consequence: the C5 requirement "stripping the managed block recreates the exact accepted baseline SHA-256 C9A664B7…" is not met.

**F2 — bounded managed plugin config keys were not applied.**
- C5 requires (produced by `host.py`): `enforcedMode=true`, `autoWorkflowCompletion=true`, `preInferenceAdmission=true`, `autoResume=true`, `workspaceDir=C:\Users\CDQ-P\.openclaw\workspace`, `ticketDispatchLimit=1`, `ticketMaximumRunning=1`, `ticketMaximumAttempts=5`, `ticketRecoveryPollMs=5000`, `ticketDispatchPollMs=5000`, `ticketOutboxPollMs=5000`;
- observed via `openclaw config get` on the post-enable install: only `ticketFirst=true` and `plugins.entries.cogentnexus-openclaw.hooks.allowConversationAccess=true` are set; all of `preInferenceAdmission`, `autoWorkflowCompletion`, `enforcedMode`, `autoResume`, `workspaceDir`, `ticketDispatchLimit`, `ticketMaximumRunning`, `ticketMaximumAttempts`, `ticketRecoveryPollMs`, `ticketDispatchPollMs`, `ticketOutboxPollMs` returned **empty**;
- consequence: the C5 requirement for exact managed config values is not met.

**Secondary observation (non-blocking but noted):** the enable internal maintenance reloads advanced the generation counter to `12` (enable stdout `authorityCommit.generation=9`; final `cnxclaw status` `generation=12`), beyond the task's idealized "exactly 8". The host is stable and `mode=managed`, but the exact generation count does not equal 8.

## Decision

Per Task 061 C5: "If enable exited 0 but any mandatory postcondition fails, do not retry or manually repair. Report: BLOCKED_POST_ENABLE_VERIFICATION." Both F1 and F2 are mandatory C5 postconditions. The `enable` transition itself succeeded (MANAGED mode, plugin enabled/loaded, supervisor installed, runtime healthy), but the verified post-state does not conform to the exact C5 acceptance criteria.

No manual repair, no second `cnxclaw enable`, no `disable`, no AGENTS/config edit, and no rollback were performed. The live installation is currently in MANAGED mode with the plugin loaded; all ownership/backup/replacement/SQLite/runtime states are preserved. The blockers are about exact post-state conformance (AGENTS baseline recreation and managed config key application), not about safety or data loss.

## All live mutations attributable to the single supported enable sequence

Exactly the internal effects of the one `cnxclaw enable` invocation (verified from poststate, not assumed): MANAGED controller transition; managed policy application to `AGENTS.md` (inserting the managed block — which produced the F1 baseline deviation); canonical plugin enable (post-enable inventory shows `enabled=true`/`loaded`); startup-adapter enablement (CogentNexus-OpenClaw-Supervisor scheduled task installed/enabled/hidden); runtime lifecycle start with provider authority (Ollama already healthy, skipped); default-session reconciliation (already present); and one safe supervisor tick.

## Remaining uncertainty

None regarding enable success/safety. The two C5 conformance gaps (F1 AGENTS stripped-baseline, F2 managed config keys) require ChatGPT decision: either accept the current MANAGED state as functionally correct (the managed block content is policy-correct; the config defaults may differ from the task's asserted values due to a host.py/config-schema change), or direct a remediation task. Hermes must not improvise that remediation.

## Result token

`BLOCKED_POST_ENABLE_VERIFICATION`
