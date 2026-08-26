# Coordination Channel Status

**State:** `READY_FOR_HERMES`
**Updated:** 2026-08-27 ICT
**Transport:** GitHub repository history
**Human authority:** operator authorized definitive repair through final live/semantic acceptance and approved heavy comprehensive work while Hermes/Codex budget is available
**Execution trigger:** manual Hermes continuation; scheduled execution remains disabled

## Accepted semantic/delivery source lineage

Tasks 078/079/080 remain accepted candidate behavior covering owner/session delivery security, admission/routing idempotency, one timeout recovery authority, direct model-call lease ordering, direct lifecycle convergence, workflow delivery atomicity, crash-safe completion-lock publication, and exact workflow/Ticket delivery-run fencing.

Provider readiness remains:

`PROVIDER_READY_WITH_FRESH_OWNER_SESSION`

No additional direct Ollama probe is authorized.

## Task 081 accepted blocker

Task 081 attempted exactly one supported live install-over from the then-current semantic candidate and stopped after nonzero exit.

Accepted disposition:

`ACCEPT_BLOCKER_SUPPORTED_INSTALL_OVER_NPM_PACK_PARSER`

The failure occurred after supported PASSTHROUGH/native handoff and skill copy but before plugin rollover and final MANAGED restoration.

## Task 082 acceptance

Task 082 repaired the `npm pack --json` installer boundary source-only.

Implementation:

`df412ed10522d79a722e1b48d681e7553cb79ae2`

Report:

`34057308f75cb7334c83e253b3077358d05918fd`

Independent decision:

`ACCEPT`

Disposition:

`ACCEPT_NPM_PACK_INSTALLER_BOUNDARY_REPAIRED`

Accepted evidence:

- Windows PowerShell 5.1 reproduced the old parser failure against captured npm-12 keyed-object output;
- npm 11 emitted a one-item array;
- npm 12 emitted a one-entry package-keyed object;
- one production resolver now normalizes both shapes and rejects malformed/multiple/unsafe/missing artifacts;
- exact artifact existence/path is verified before `openclaw plugins install`;
- npm 11/npm 12 plugin tests and validation passed;
- full Python reported `362 passed, 2 skipped, 4 subtests passed`;
- live partial state was preserved read-only.

## Current partial live state

Expected state entering Task 083:

- ownership verification passes;
- `recovery-preflight = OWNERSHIP_PRESENT`;
- classification `upgrade`;
- controller `passthrough`, generation 13;
- startup policy disabled;
- Supervisor Scheduled Task absent;
- AGENTS managed block absent;
- prior canonical `cogentnexus-openclaw@0.9.3` generation registered but disabled;
- launcher remains on product-owned runtime;
- SQLite integrity `ok`, zero Tickets/outbox;
- Gateway remains healthy/present;
- Ollama remains healthy with the accepted four-model set.

This is not a MANAGED acceptance state.

## Active Task 083

[`tasks/CNX-20260827-083-recover-partial-install-and-live-parity.md`](tasks/CNX-20260827-083-recover-partial-install-and-live-parity.md)

Status: `READY_FOR_HERMES`

Authorization: `ONE_SUPPORTED_RECOVERY_INSTALL_OVER_AUTHORIZED`

Execution mode: `LIVE_SUPPORTED_PARTIAL_INSTALL_RECOVERY_AND_PARITY`

Exact recovery source:

`df412ed10522d79a722e1b48d681e7553cb79ae2`

Task 083 must:

- re-prove the expected partial state and `upgrade` classification;
- run candidate source/npm-pack preflight in isolation;
- invoke exactly one supported normal install-over with no uninstall/reset/manual cleanup;
- prove live skill/plugin parity against exact recovery source;
- restore MANAGED/startup/Supervisor/AGENTS through installer-supported behavior;
- prove product-owned runtime/launcher/task bindings;
- prove ownership/Gateway/Ollama/SQLite/unrelated-config health;
- observe at least five natural PT1M Supervisor ticks and classify no-flash;
- prove Dashboard/WebChat authenticated owner-surface readiness without sending a semantic prompt.

## Hard semantic fence

Task 083 sends zero semantic messages and zero provider probes.

No Dashboard/WebChat chat send, `chat.send`, `openclaw agent`, `sessions_send`, channel message, synthetic Ticket mutation, direct Ollama probe, model/provider/timeout change, uninstall/reset/manual repair, reboot, merge, tag or release.

The recovery installer may be invoked only once. A nonzero result must be captured and reported, not retried automatically.

## Successor logic

Only after independent acceptance of `PASS_RECOVERY_LIVE_PARITY_NO_FLASH_OWNER_SURFACE_READY` may the final semantic acceptance task send exactly one fresh authenticated Dashboard/WebChat owner message.

That final task must prove:

`owner message -> Ticket accepted before provider -> Ollama inference -> response_ready -> exact owner/run delivery -> delivery_confirmed -> completed -> visible nonce response`.
