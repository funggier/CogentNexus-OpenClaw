# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `LIVE_SUPPORTED_PARTIAL_INSTALL_RECOVERY_AND_PARITY`
Current authorization: `ONE_SUPPORTED_RECOVERY_INSTALL_OVER_AUTHORIZED`
Task ID: `CNX-20260827-083`
Updated: 2026-08-27 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260827-083-recover-partial-install-and-live-parity.md`](tasks/CNX-20260827-083-recover-partial-install-and-live-parity.md)

## Task 082 acceptance

Task 082 reported:

`PASS_NPM_PACK_INSTALLER_BOUNDARY_REPAIRED`

Implementation HEAD:

`df412ed10522d79a722e1b48d681e7553cb79ae2`

Report HEAD:

`34057308f75cb7334c83e253b3077358d05918fd`

Independent review:

Decision: `ACCEPT`

Disposition:

`ACCEPT_NPM_PACK_INSTALLER_BOUNDARY_REPAIRED`

Review path:

[`reviews/CNX-20260827-082-repair-npm-pack-installer-boundary.md`](reviews/CNX-20260827-082-repair-npm-pack-installer-boundary.md)

## Accepted recovery source

The exact production source authorized for Task 083 is:

`df412ed10522d79a722e1b48d681e7553cb79ae2`

It preserves the accepted Task-078/079/080 semantic/delivery lineage and adds the accepted Task-082 npm-pack installer repair.

Task 082 independently reproduced:

- npm 11 array-shaped `npm pack --json` output under Node 24/npm 11;
- npm 12 keyed-object output under Node 22/npm 12;
- the pre-fix Windows PowerShell 5.1 parser failure against npm-12 output.

The corrected installer now uses one deterministic artifact resolver supporting both accepted shapes, rejecting malformed/multiple/unsafe metadata and requiring the exact `.tgz` file before plugin installation.

Provider readiness remains:

`PROVIDER_READY_WITH_FRESH_OWNER_SESSION`

The two Task-078 direct Ollama probes are consumed and must not be repeated.

## Current live partial state

Task 081's single install-over failed after supported native handoff. Task 082 preserved this state read-only.

Expected Task-083 starting state:

- ownership verifies;
- recovery preflight `OWNERSHIP_PRESENT`;
- classification `upgrade`;
- controller `passthrough`, generation 13;
- startup policy disabled;
- Supervisor absent;
- AGENTS managed block absent;
- prior canonical v0.9.3 plugin generation registered but disabled;
- launcher still uses the product-owned runtime;
- SQLite integrity `ok`, zero Tickets/outbox;
- Gateway remains healthy/present;
- Ollama remains healthy with the accepted four-model inventory.

If meaningful drift is observed, Task 083 must stop before mutation.

## Task 083 authorization

Task 083 may perform exactly one supported normal install-over from exact source `df412ed10522d79a722e1b48d681e7553cb79ae2` onto the current partial PASSTHROUGH installation.

It must not uninstall/reset/clean/manual-repair first.

It must prove:

1. expected partial state and `upgrade` classification before mutation;
2. candidate preflight including the repaired npm-pack boundary;
3. exactly one supported install-over exits zero;
4. source/live skill and canonical plugin parity;
5. MANAGED/startup/Supervisor/AGENTS restoration through installer behavior only;
6. owned runtime/launcher/Supervisor bindings with no Hermes/Codex/temp durable dependency;
7. ownership/Gateway/Ollama/SQLite health and unrelated config preservation;
8. at least five natural PT1M Supervisor ticks with `NO_FLASH_MULTI_TICK_PROVEN`;
9. `DASHBOARD_OWNER_SURFACE_READY` read-only proof without sending a user message.

## Hard semantic fence

Task 083 sends zero semantic/user messages and zero provider probes.

No Dashboard/WebChat chat send, no `chat.send`, no `openclaw agent`, no `sessions_send`, no channel message, no synthetic Ticket mutation, no direct Ollama probe, no model/provider/timeout change, no uninstall/reset/manual repair, no reboot, merge, tag or release.

If the one recovery install-over returns nonzero, it must not be retried automatically.

## Successor gate

Only an independently accepted `PASS_RECOVERY_LIVE_PARITY_NO_FLASH_OWNER_SURFACE_READY` may authorize the final semantic task.

That final task may send exactly one fresh authenticated Dashboard/WebChat owner message and must prove Ticket-before-provider ordering, correlated Ollama inference, response-ready, exact owner/run delivery confirmation, completed state and one visible nonce response.
