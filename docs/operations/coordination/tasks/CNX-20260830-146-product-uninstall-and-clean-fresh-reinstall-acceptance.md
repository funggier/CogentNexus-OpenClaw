# CNX-20260830-146 — Product Uninstall and Clean Fresh-Reinstall Acceptance

Status: `READY_FOR_HERMES`
Execution mode: `LIVE_WINDOWS_PRODUCT_UNINSTALL_AND_CLEAN_FRESH_REINSTALL_ACCEPTANCE`
Owner: ChatGPT
Executor: Hermes/Codex on the operator's real Windows machine

## Purpose

Prove the accepted candidate's **operator-facing destructive lifecycle** on the real Windows machine:

1. run the installed `cnxclaw.cmd uninstall` command with the required explicit `y` confirmation exactly once;
2. prove CogentNexus-OpenClaw is cleanly removed while native OpenClaw remains healthy and provider state is not destructively altered;
3. perform exactly one normal fresh installation from the exact accepted pre-release candidate source;
4. prove the result is a genuinely fresh, canonical, healthy MANAGED installation.

This task deliberately tests the product command itself. Do **not** substitute `scripts/clean-reinstall.ps1`, manual plugin uninstall, manual deletion, or another cleanup path.

The public GitHub Release download/install smoke remains a later distribution acceptance step after the final candidate is frozen/published; Task 146 must not create/tag/publish a release.

## Accepted implementation source

Exact accepted production SHA:

`fb5781c1abd68280760bd5b3b4a65fabd8a60e58`

Task-145 live acceptance proved this SHA is currently installed coherently and that the supported installer can re-enter the prior partial state.

Task-145 review disposition: **ACCEPT**.

## Starting live boundary

Task 145 last proved:

- controller `managed`;
- exactly one canonical direct `cogentnexus-openclaw` plugin;
- plugin `enabled=true`, `status=loaded`, version `0.9.3`;
- installed plugin fingerprint `12c6d1b5b6ffd938353dd60c5d6190c34a609663369f619ff4fc7cbd176119e0`;
- installed `namespace_ownership.py` hash `10dda985e6d4553a73a8cdd3ef7f660937482c3ef0c2d2da8d15bcbfe8d39b66`;
- exact ownership verification PASS with refreshed manifest;
- Gateway/OpenClaw/Ollama healthy;
- recovery/delivery `READY`, pending `0`;
- SQLite integrity `ok`;
- durable counts `tickets=2`, `ticket_events=14`, `cnx_direct_model_call=2`, `cnx_direct_recovery=0`, `cnx_assistant_delivery=0`, `ticket_outbox=0`, `cnx_sessions=2`;
- Dashboard semantic Send count `0`.

This is historical evidence only. Re-verify material state read-only before the first destructive action. Do not normalize drift.

## Remote and source authority

Before live mutation:

1. fetch GitHub branch `agent/v0.9.3-full-stabilization`;
2. verify `ACTIVE.md` and `STATUS.md` still authorize this exact Task 146 and no matching report exists;
3. preserve uncertain local checkout; use a fresh detached clone/worktree at exact SHA `fb5781c1...` for the later fresh install;
4. record candidate `install.ps1`, ownership-helper, plugin fingerprint and package provenance needed to identify the fresh result;
5. do not merge/rebase/tag/release/force-push.

## Phase A — pre-uninstall read-only acceptance gate

Capture, without changing live state:

- installed launcher path and CLI help proving `reset` and `uninstall` are operator-facing commands;
- ownership `verify` result and manifest;
- controller mode/status;
- OpenClaw plugin inventory, raw canonical root, enabled/loaded status, and root non-reparse attestation;
- installed plugin fingerprint and installed ownership-helper hash;
- Gateway/OpenClaw version/health/listener;
- Ollama selected-provider health;
- supervisor and Gateway scheduled-task state;
- recovery check read-only;
- delivery check read-only and pending count;
- SQLite read-only `pragma integrity_check` plus exact semantic counts;
- current native-route/managed-route evidence sufficient to verify native restoration after uninstall;
- Dashboard semantic Send count `0`.

If ownership is ambiguous, plugin storage is noncanonical/conflicting, Gateway/native-route safety cannot be proven, or other material drift makes destructive lifecycle unsafe: publish `BLOCKED` and stop before mutation.

### Evidence backup

Because uninstall intentionally removes CNX-owned durable state, preserve test evidence **outside** the workspace and outside `%LOCALAPPDATA%\CogentNexus-OpenClaw` before uninstall. A read-only copy/hash of the pre-uninstall database/state may be retained under a Task-146 evidence directory. This backup is test evidence only and must never be restored into the live product during this task.

## Phase B — operator-facing uninstall, exactly once

Execute the installed launcher itself:

`<workspace>\cnxclaw.cmd uninstall`

Feed exactly one explicit lowercase `y` response to its confirmation prompt using a harness that preserves the real process exit code and stdout/stderr.

Requirements:

- uninstall command invocation count: **1**;
- confirmation answer: **exactly `y`**;
- no manual `openclaw plugins uninstall` command;
- no `clean-reinstall.ps1`;
- no manual file deletion;
- no second uninstall attempt if the command fails.

If uninstall exits nonzero, stop immediately. Capture only read-only post-failure state and report `FAIL_UNINSTALL`. Do not fresh-install, retry, clean up, or normalize.

### Windows deferred-cleanup boundary

The product may schedule deletion of `cnxclaw.cmd` and remaining owned paths after the uninstall command exits. After a successful exit, allow only a bounded read-only polling period for product-owned deferred cleanup to finish. Do not manually delete residue.

## Phase C — prove clean native state before reinstall

A successful uninstall is not accepted until read-only proof shows the intended product absence/native boundary:

- `cnxclaw.cmd` absent after product-owned deferred cleanup;
- `.cogentnexus-openclaw` live state root absent;
- workspace `skills/cogentnexus-openclaw` absent;
- OpenClaw inventory contains no `cogentnexus-openclaw` registration;
- canonical CNX plugin root absent and no conflicting CNX product storage remains;
- CNX supervisor scheduled task absent;
- CNX-owned application-data/runtime surfaces that the ownership contract says uninstall removes are absent; explicitly report any intentionally retained backup/evidence surfaces outside the live tree;
- OpenClaw Gateway remains healthy on the native route after uninstall;
- OpenClaw itself remains installed and usable;
- Ollama/provider installation is unchanged and not uninstalled by CNX;
- no semantic Dashboard/Ticket activity occurred during uninstall.

If product-owned cleanup does not reach this clean state within a bounded wait, report `FAIL_UNINSTALL_CLEANUP` and stop. Do not manually finish cleanup.

## Phase D — one fresh install from exact accepted candidate

Only after Phase C passes, use the fresh detached exact candidate source and invoke the normal supported installer exactly once:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File <exact-detached-source>\scripts\install.ps1 -Workspace C:/Users/CDQ-P/.openclaw/workspace
```

Requirements:

- fresh installer invocation count: **1**;
- no `cnxclaw install` command exists or is to be invented;
- no skip/staging flags;
- no `clean-reinstall.ps1` wrapper;
- no alternate installer;
- no retry if the fresh installer fails.

The installer must itself classify the system as a coherent fresh installation boundary. Record the production recovery/classification/action evidence around the run where observable without adding mutations.

If fresh install exits nonzero, stop and report `FAIL_FRESH_INSTALL` with the exact first failure and read-only post-failure state. Do not retry or manually repair.

## Phase E — post-fresh-install proof

If the installer exits `0`, prove read-only:

- exactly one canonical `cogentnexus-openclaw` plugin identity exists;
- direct root is real/non-reparse and there is no conflicting CNX product storage;
- plugin is enabled/loaded at version `0.9.3`;
- installed plugin fingerprint equals the exact candidate fingerprint;
- installed ownership-helper hash equals accepted candidate provenance;
- ownership manifest is newly created for this fresh installation and exact `verify` passes;
- controller is normal `managed`;
- Gateway is healthy and connected on loopback;
- selected provider is Ollama and healthy/ready;
- recovery `READY` read-only;
- delivery `READY`, pending `0`, read-only;
- supervisor and Gateway scheduled tasks are registered/Ready as expected;
- SQLite integrity is `ok`;
- the new live durable store is fresh: historical Task-145 Tickets/events/sessions are not present in the new live database; report exact new counts rather than assuming them;
- no stale fresh-install transaction/rollover staging remains;
- Dashboard semantic Send count remains `0`.

## PASS criteria

`PASS` requires all of:

1. fresh GitHub authority and exact accepted candidate provenance;
2. coherent safe pre-uninstall gate;
3. exactly one real `cnxclaw.cmd uninstall` invocation with explicit `y`;
4. uninstall exit `0`;
5. product-owned deferred cleanup reaches a clean CNX-absent/native-OpenClaw state without manual deletion;
6. exactly one normal fresh `scripts/install.ps1` invocation from exact SHA `fb5781c1...`;
7. fresh installer exit `0`;
8. new installation has exact candidate provenance, canonical ownership, MANAGED state and healthy runtime/provider/recovery/delivery;
9. fresh durable database contains no historical Task-145 product data;
10. no retry/manual normalization/alternate lifecycle path and Dashboard semantic Sends remain `0`.

## Required report

Publish exactly:

`docs/operations/coordination/reports/CNX-20260830-146-product-uninstall-and-clean-fresh-reinstall-acceptance.md`

Report must include:

- exact authority HEAD and detached candidate SHA;
- full pre-uninstall evidence summary;
- explicit confirmation/input proof and uninstall command count;
- uninstall exit/output and first failure if any;
- bounded deferred-cleanup evidence and exact clean/native state;
- exact fresh installer command/count/exit;
- candidate package/fingerprint/hash provenance;
- complete post-fresh-install health/ownership/storage/database evidence;
- side-effect accounting;
- verdict exactly one of `PASS`, `FAIL_UNINSTALL`, `FAIL_UNINSTALL_CLEANUP`, `FAIL_FRESH_INSTALL`, `BLOCKED`;
- unproven items.

Then stop for independent ChatGPT review.

## Hard fence

No Dashboard semantic Send/resend; no manual Ticket/workflow/outbox/delivery/recovery/database mutation; no reset in Task 146; no crash/recovery injection; no manual plugin install/uninstall/enable/disable; no manual CNX live-file deletion or ownership/controller normalization; no clean-reinstall helper; no retry after destructive failure; no unrelated process/service/task mutation; no reboot; no credentials/secrets; no merge/tag/release; no force push.
