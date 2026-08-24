# CNX-20260825-061 — Return to Verified MANAGED Lifecycle

Status: `READY_FOR_HERMES`

Execution mode: `MANUAL_WITH_HUMAN_GATE`

Current authorization: `MANAGED_REENTRY_AUTHORIZED`

Owner: ChatGPT

Executor: Hermes after the operator's manual continuation signal

## Goal

Return the repaired CogentNexus-OpenClaw v0.9.3 installation from the accepted Task 060 PASSTHROUGH state to normal MANAGED operation using exactly one supported installed `cnxclaw enable` invocation, then prove ownership, managed policy, plugin registration/configuration, startup adapter, Gateway/provider health, and bounded Ticket/session continuity.

This task is a lifecycle re-entry task only. It must not reinstall, reset, uninstall, rerun rollover, delete the retained rollover backup, or broaden into release/merge work.

## Authorization basis

The operator asked ChatGPT to continue after Task 060 execution.

Task 060 is accepted by ChatGPT with disposition:

`ACCEPT_PLUGIN_GENERATION_ROLLOVER_APPLIED_PASSTHROUGH`

Task 060 report commit:

`0ae317d51a0efc13ebcfaabab6cb6b9595b2d2c5`

Task 060 review commit:

`633cefcfe06c83aae8aede17f3bf6b36ed4d3eb7`

Accepted post-rollover ownership-manifest SHA-256:

`0667004DC9D6483450A3C99DDA6F34BB7F384F0261F43813763019E2C3BA0341`

Accepted replacement payload:

`C:\Users\CDQ-P\.openclaw\npm\projects\openclaw-plugin-cogentnexus-openclaw__openclaw-generation__g-bbc979095f8845a1\node_modules\openclaw-plugin-cogentnexus-openclaw`

Accepted replacement npm project root:

`C:\Users\CDQ-P\.openclaw\npm\projects\openclaw-plugin-cogentnexus-openclaw__openclaw-generation__g-bbc979095f8845a1`

Accepted replacement project-tree SHA-256:

`3621dbb46b6e6fadf5b0c0ecade860f1206640949804a26129612005202d1c7d`

Retained retired-generation backup:

`C:\Users\CDQ-P\AppData\Local\CogentNexus-OpenClaw\plugin-generation-rollover-backups\openclaw-plugin-cogentnexus-openclaw-20260824t181210832193z`

Accepted retired backup project-tree SHA-256:

`05981336d143a83b20d81803a29e66a849e845fe49064b8fd5c97cdecd3f94ee`

The rejected Task 058 plan SHA remains permanently irrelevant to this task.

## Supported lifecycle semantics

The accepted Host implementation defines `enable` as the supported PASSTHROUGH → MANAGED transition. Its bounded internal sequence is:

1. initialize and reconcile terminal fences;
2. transition controller to `mode=managed`, `desiredGateway=running`, `desiredProvider=running`;
3. apply the registered managed policy to workspace `AGENTS.md`;
4. enable the canonical `cogentnexus-openclaw` OpenClaw plugin;
5. configure the bounded managed plugin settings;
6. enable the startup adapter;
7. run runtime lifecycle start with provider authority;
8. reconcile/bootstrap the default OpenClaw session;
9. promote only legitimately interrupted direct work, if any;
10. run one safe supervisor tick.

Task 061 authorizes those internal effects only when reached through the single installed `cnxclaw enable` command after all preflight gates below pass.

Do not reproduce those effects manually with separate plugin/config/startup/lifecycle commands.

## Required repository source

Use a new fresh isolated full clone of:

`funggier/CogentNexus-OpenClaw`

Branch:

`agent/v0.9.3-recovery-reality-tests`

Before any live mutation require:

- local HEAD equals remote coordination HEAD;
- fresh clone is clean;
- Task 057 accepted implementation `f379e5c5d8dddb144cb0d1991b645b16055e1303` is an ancestor;
- Task 060 report `0ae317d51a0efc13ebcfaabab6cb6b9595b2d2c5` is an ancestor;
- Task 060 review `633cefcfe06c83aae8aede17f3bf6b36ed4d3eb7` is an ancestor;
- `ACTIVE.md`, `STATUS.md`, and this task all agree on `READY_FOR_HERMES` / `MANAGED_REENTRY_AUTHORIZED`;
- no completed matching Task 061 report already exists.

Never checkout, reset, clean, repair, or commit from the primary repository:

`C:\Users\CDQ-P\.openclaw\workspace`

## Installed-code identity gate

Before lifecycle mutation, compare the installed live execution files byte-for-byte against the fresh isolated clone and record SHA-256 for both copies. Require exact equality for:

- `skills/cogentnexus-openclaw/scripts/host.py`;
- `skills/cogentnexus-openclaw/scripts/runtime.py`;
- `skills/cogentnexus-openclaw/scripts/startup.py`;
- `skills/cogentnexus-openclaw/scripts/host_control.py`;
- `skills/cogentnexus-openclaw/templates/supervisor/windows-task.xml`;
- `skills/cogentnexus-openclaw/templates/AGENTS.cogentnexus-openclaw.md`.

Also require the installed launcher:

`C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd`

still has SHA-256:

`8DB1F256BB56C298FFFB14E8A761CAA7DBEC56EA334B0F4558C3CDA563AA46EF`

Any code/template/launcher drift stops as `BLOCKED_PRE_ENABLE_STATE_DRIFT` before `cnxclaw enable`.

## Evidence boundary

Before live inspection create a new unique retained directory under:

`%LOCALAPPDATA%\Temp\cnx061-managed-reentry-<UTC-token>`

Retain at minimum:

- fetched repository HEAD and clean status;
- UTC transcript with exact commands and exit codes;
- installed-vs-clone code identity hashes;
- bounded prestate JSON/text and hashes;
- one pre-enable OpenClaw plugin inventory raw JSON file;
- pre-enable bounded plugin-config reads;
- root-process wrapper self-test output;
- exact enable stdout/stderr/poststate and numeric exit code;
- bounded post-enable JSON/text and hashes;
- one post-enable OpenClaw plugin inventory raw JSON file;
- bounded post-enable plugin-config reads;
- startup Scheduled Task evidence;
- managed-policy/AGENTS structural proof;
- ownership/backup/replacement proof;
- report draft and publication verification.

Do not capture secrets, API keys, tokens, full OpenClaw config, environment dumps, unrelated user files, or model contents.

## Duplicate and concurrency fence

Before `enable`, prove zero concurrent:

- other Task 061 executor;
- installer/reset/uninstall/rollover apply;
- `cnxclaw enable/disable/start/stop/restart` process;
- product supervisor adapter/task;
- plugin install/uninstall/enable/disable command;
- report publisher for Task 061;
- Procmon Task 027/038 capture;
- process mutating the accepted replacement or rollover-backup roots.

The bundled `OpenClaw Gateway` task/process is expected and is not a CogentNexus supervisor conflict.

If concurrency cannot be bounded, stop before mutation.

## Phase C1 — accepted post-rollover preflight

Freshly prove read-only:

- `cnxclaw.cmd --json status` reports controller mode exactly `passthrough`;
- generation exactly `7`;
- desired Gateway `running`;
- desired provider `unchanged`;
- selected provider `ollama` where exposed;
- startup policy `disabled` and CogentNexus startup adapter absent;
- Gateway healthy/reachable;
- Ollama healthy with the same four model identities:
  - `qwen3.5:9b`
  - `muse-glimmer:30b`
  - `qwen3.6:27b`
  - `qwen3.8:27b`;
- SQLite read-only integrity `ok` with ticket/event/outbox/session counts all `0`;
- ownership manifest SHA-256 exactly `0667004DC9D6483450A3C99DDA6F34BB7F384F0261F43813763019E2C3BA0341`;
- `namespace_ownership.py verify` exits `0`;
- `namespace_ownership.py resolve-plugin --version 0.9.3` exits `0` and resolves exactly the accepted replacement payload/fingerprint;
- the prior retired npm project root remains absent;
- the exact rollover backup exists and its tree SHA-256 remains `05981336d143a83b20d81803a29e66a849e845fe49064b8fd5c97cdecd3f94ee`;
- the replacement project exists and its tree SHA-256 remains `3621dbb46b6e6fadf5b0c0ecade860f1206640949804a26129612005202d1c7d`;
- registered managed policy remains SHA-256 `14EDEAD0180690C3D9565E864D2BDAAAE60E32DF9EF2C64EBD2A1238DF5CD8B4`;
- workspace `AGENTS.md` currently contains zero CogentNexus-OpenClaw managed marker pairs and, as the stripped baseline, SHA-256 `C9A664B73200AE5D6B0DA0908DE3256CDB4DDA8BA6FE99F5E6C5115C3983604C`.

Capture exactly one pre-enable `openclaw plugins list --json` raw file. Require exactly one canonical `cogentnexus-openclaw` registration at the accepted replacement root, version `0.9.3`, `enabled=false`, `status=disabled`, with all unrelated plugin identities/rootDirs/status values snapshotted for post-comparison.

Any contradiction stops as:

`BLOCKED_PRE_ENABLE_STATE_DRIFT`

No lifecycle mutation is then authorized.

## Phase C2 — pre-enable bounded configuration observation

Read only the following exact plugin configuration keys individually; do not dump the full OpenClaw config:

- `plugins.entries.cogentnexus-openclaw.config.ticketFirst`;
- `preInferenceAdmission`;
- `autoWorkflowCompletion`;
- `enforcedMode`;
- `autoResume`;
- `workspaceDir`;
- `ticketDispatchLimit`;
- `ticketMaximumRunning`;
- `ticketMaximumAttempts`;
- `ticketRecoveryPollMs`;
- `ticketDispatchPollMs`;
- `ticketOutboxPollMs`;
- `plugins.entries.cogentnexus-openclaw.hooks.allowConversationAccess`.

These reads are baseline evidence only; do not require them to already be configured while the product is PASSTHROUGH.

## Phase C3 — root-process proof

Run from the fresh isolated clone:

```powershell
& <isolated-clone>\scripts\invoke-root-process-exact.ps1 -SelfTest
```

Require exit `0` with numeric `0`/`7`, null rejection, and argument round-trip proofs.

Failure stops as `BLOCKED_PRE_ENABLE_STATE_DRIFT`.

## Phase C4 — execute supported MANAGED re-entry once

Invoke exactly once:

```powershell
C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd enable
```

Capture it through the accepted root-process wrapper so stdout, stderr, timing, and an observed numeric exit code are durable.

If direct `.cmd` execution is unsuitable for `Start-Process`, create only an evidence-directory PowerShell shim whose sole behavior is:

```powershell
& 'C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd' enable
$code = $LASTEXITCODE
if ($null -eq $code) { throw 'cnxclaw enable exit code unobserved' }
exit ([int]$code)
```

and invoke that shim through `invoke-root-process-exact.ps1`.

Invocation count for `cnxclaw enable` must be exactly `1`.

Do not manually run any of the internal enable substeps before or after it.

If enable exits nonzero or the numeric exit code is unobserved, do not retry, do not run `disable`, and do not repair manually. Capture bounded poststate and report:

`BLOCKED_MANAGED_ENABLE_FAILED`

## Phase C5 — post-enable MANAGED verification

After an observed enable exit code `0`, prove all of the following without a second lifecycle mutation.

### Controller and desired state

- controller mode exactly `managed`;
- generation exactly `8` (one transition from accepted generation 7);
- desired Gateway exactly `running`;
- desired provider exactly `running`.

### Startup adapter

- startup policy exactly `enabled`;
- Windows Scheduled Task `CogentNexus-OpenClaw-Supervisor` exists;
- adapter is enabled;
- adapter is hidden;
- action executable equals the expected installed Python background executable selected by `startup.py`;
- action arguments point to the installed `skills\cogentnexus-openclaw\scripts\host_control.py` and exact live state root;
- no second or foreign CogentNexus supervisor task exists.

Do not require the Scheduled Task transient `State` to be `Running`; `Ready` after a completed tick is acceptable. Identity/action/enabled/hidden bindings are authoritative.

### Managed policy and AGENTS

- registered policy file remains byte-identical with SHA-256 `14EDEAD0180690C3D9565E864D2BDAAAE60E32DF9EF2C64EBD2A1238DF5CD8B4`;
- `AGENTS.md` contains exactly one `<!-- cogentnexus-openclaw:begin -->` marker and one matching end marker;
- the content inside that managed block equals the registered normalized managed policy;
- stripping the managed block recreates the exact accepted baseline SHA-256 `C9A664B73200AE5D6B0DA0908DE3256CDB4DDA8BA6FE99F5E6C5115C3983604C`;
- no legacy CogentNexus marker/block is introduced.

Record any `AGENTS.pre-host-change-*` backup created by the supported enable path, but do not alter or delete it.

### Canonical plugin registration and config

Capture exactly one post-enable `openclaw plugins list --json` raw file. Require:

- exactly one canonical `cogentnexus-openclaw` registration;
- version exactly `0.9.3`;
- rootDir exactly the accepted replacement payload;
- `enabled=true`;
- status `loaded`;
- if `packageName` is present it equals `openclaw-plugin-cogentnexus-openclaw`; if absent, the replacement payload package identity remains exact;
- the 71 unrelated plugin identities/rootDirs/status values are unchanged from pre-enable, except no assertion should treat normal runtime loading metadata unrelated to CogentNexus as product mutation unless the identity/root/status actually changed.

Read only the bounded configuration keys from C2 and require exact managed values produced by `host.py`:

- `ticketFirst=true`;
- `preInferenceAdmission=true`;
- `autoWorkflowCompletion=true`;
- `enforcedMode=true`;
- `autoResume=true`;
- `workspaceDir=C:\Users\CDQ-P\.openclaw\workspace`;
- `ticketDispatchLimit=1`;
- `ticketMaximumRunning=1`;
- `ticketMaximumAttempts=5`;
- `ticketRecoveryPollMs=5000`;
- `ticketDispatchPollMs=5000`;
- `ticketOutboxPollMs=5000`;
- `hooks.allowConversationAccess=true`.

### Ownership and generation preservation

- ownership manifest remains SHA-256 `0667004DC9D6483450A3C99DDA6F34BB7F384F0261F43813763019E2C3BA0341`;
- ownership still binds the accepted replacement payload;
- `namespace_ownership.py verify` exits `0`;
- `resolve-plugin` exits `0` and still resolves exactly one canonical replacement payload;
- prior retired npm project root remains absent;
- rollover backup tree remains exact at SHA-256 `05981336d143a83b20d81803a29e66a849e845fe49064b8fd5c97cdecd3f94ee`;
- replacement project tree remains exact at SHA-256 `3621dbb46b6e6fadf5b0c0ecade860f1206640949804a26129612005202d1c7d`.

### Runtime/provider/session/Ticket preservation

- Gateway healthy/reachable after enable;
- Ollama healthy with the same four model identities;
- CNX SQLite integrity remains `ok`;
- because the accepted prestate contained zero tickets/events/outbox/sessions, require no unexpected CNX ticket/event/outbox creation from lifecycle re-entry itself;
- any default OpenClaw session bootstrap reported by `enable` must resolve to the configured default agent/main session and persist in OpenClaw session inventory;
- `terminalFences` and `recoveredTickets` returned by enable must be recorded; with the accepted zero-ticket prestate, `recoveredTickets` is expected empty and no terminal-fence mutation should be needed;
- Gateway/provider lifecycle must not be stopped by the task.

If enable exited `0` but any mandatory postcondition fails, do not retry or manually repair. Report:

`BLOCKED_POST_ENABLE_VERIFICATION`

## Phase C6 — publication and mandatory stop

Publish only:

`docs/operations/coordination/reports/CNX-20260825-061-return-managed-lifecycle.md`

For a fully verified re-entry:

Status: `PASS`

Result:

`PASS_MANAGED_REENTRY_VERIFIED`

The report must include:

- execution HEAD and isolated clone path;
- installed-vs-clone code identity hashes;
- prestate controller/startup/ownership/plugin/Gateway/Ollama/SQLite/AGENTS evidence;
- pre/post plugin inventory paths and hashes;
- root-process self-test result;
- exact `cnxclaw enable` invocation count and numeric exit code;
- bounded enable stdout result including mode/startup/lifecycle/sessionBootstrap/terminalFences/recoveredTickets;
- post-enable controller generation/mode/desired state;
- startup Scheduled Task identity/action proof;
- AGENTS managed-block and stripped-baseline proof;
- bounded plugin config values;
- ownership/replacement/backup hashes and resolver results;
- Gateway/Ollama/SQLite/Ticket/session preservation;
- all live mutations attributable to the single supported enable sequence;
- remaining uncertainty;
- exact result token.

The report commit must add only the matching Task 061 report path relative to execution HEAD. Fetch and remote-verify the report commit/blob, then stop for ChatGPT review.

## Result tokens

Return exactly one:

- `PASS_MANAGED_REENTRY_VERIFIED`
- `BLOCKED_PRE_ENABLE_STATE_DRIFT`
- `BLOCKED_MANAGED_ENABLE_FAILED`
- `BLOCKED_POST_ENABLE_VERIFICATION`
- `BLOCKED_EVIDENCE_PUBLICATION_UNSAFE`

## Hard fence

No installer, no reset, no uninstall, no `rollover-plan`, no `rollover-apply`, no manual old-generation move/delete/copy, no deletion or mutation of the retained rollover backup, no manual ownership edit, no separate manual plugin enable/disable/config set, no separate startup enable/disable, no separate lifecycle start/stop/restart, no process termination/force-kill, no model change, no provider selection change, no broad OpenClaw config dump/edit, no primary Git checkout/reset/clean/source edit, no Procmon Task 027/038 action, no HermesAgent mutation, no Ecosystem/staged-capability-loop work, and no merge/tag/release/archive publication.

Only the internal effects reached through the one supported `cnxclaw enable` invocation are authorized.

Report meaningful progress approximately every 3 minutes and immediately after source identity, prestate, root-process self-test, before/after enable, startup/plugin/policy verification, ownership/runtime verification, publication, or blocker.
