# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `LIVE_SUPPORTED_ATTESTED_PENDING_ROLLOVER_RECOVERY`
Current authorization: `ONE_SUPPORTED_PENDING_RECOVERY_INSTALL_OVER_AUTHORIZED`
Task ID: `CNX-20260827-087`
Updated: 2026-08-27 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260827-087-live-attested-pending-rollover-recovery-and-parity.md`](tasks/CNX-20260827-087-live-attested-pending-rollover-recovery-and-parity.md)

## Task 086 acceptance

Task 086 reported:

`PASS_PENDING_ROLLOVER_PRODUCTION_GATE_REPAIRED`

Implementation HEAD:

`71f48c1a134ee9b2646b4cc7f077abe9cae59ebb`

Report HEAD:

`1430d0a23ee2c477fdb5c2015f262c9df09c83df`

Independent review:

Decision: `ACCEPT`

Disposition:

`ACCEPT_PENDING_ROLLOVER_PRODUCTION_GATE_REPAIRED`

Review path:

[`reviews/CNX-20260827-086-fix-production-pending-rollover-gate-nesting.md`](reviews/CNX-20260827-086-fix-production-pending-rollover-gate-nesting.md)

Publication fence is accepted: one implementation commit from execution HEAD `08a53963820bd27f8418e66d5a574b12e87bd9f7`, followed by one report-only commit. No file under `plugins/cogentnexus-openclaw/**` changed.

## Accepted source for live recovery

Use exactly:

`71f48c1a134ee9b2646b4cc7f077abe9cae59ebb`

Accepted behavior now includes:

- Task-078/079/080 semantic/delivery/security fixes;
- Task-082 npm-pack parser repair;
- source-derived plugin fingerprint attestation;
- expected replacement fingerprint bound through rollover plan/apply;
- ordinary changed-source upgrade vs already-exact classification;
- explicit expected-source equality for all attested pending replacements;
- production lifecycle truth table;
- independent production install vs rollover gates;
- AST regression proving rollover is not nested under `installPlugin` and precedes strict `resolve-plugin`.

Provider readiness remains:

`PROVIDER_READY_WITH_FRESH_OWNER_SESSION`

No additional direct Ollama probe is authorized.

## Accepted current live baseline

The Task-083 two-generation partial topology remains the required pre-mutation baseline:

- controller PASSTHROUGH generation 13;
- startup disabled;
- Supervisor absent;
- AGENTS managed markers absent;
- ownership manifest -> prior generation `g-5593cbcfff5b35d5`;
- prior fingerprint `7e9189f8...`;
- active/registered disabled source-exact replacement -> `g-7257c4555ca8ad21`;
- replacement/source fingerprint `8fd911e3...`;
- exactly two canonical CogentNexus managed npm generations;
- Gateway/Ollama healthy from accepted evidence;
- SQLite integrity accepted, Tickets/outbox zero.

Do not manually normalize this topology.

## Task 087 authorization

Task 087 may invoke exactly one supported normal install-over from exact source `71f48c1a...`.

Before mutation it must re-prove:

- ownership/recovery state;
- exact old/new generation paths;
- exact full fingerprints;
- replacement fingerprint == exact source fingerprint;
- attested classification = `upgrade + pendingRollover=true + pluginAlreadyExact=false`;
- lifecycle actions = `installPlugin=false + rolloverPlugin=true`.

During the one installer invocation it must prove the pending path executes no `npm pack`, no artifact installation and no `openclaw plugins install`, creates no third generation, and completes rollover-plan/apply against the already-installed replacement.

After rollover it must prove:

1. canonical generation count converges 2 -> 1;
2. surviving generation is the Task-083 source-exact replacement;
3. source/live plugin and skill parity against exact `71f48c1a...`;
4. MANAGED/startup/Supervisor/AGENTS restoration;
5. owned runtime/launcher/Supervisor bindings;
6. ownership/Gateway/Ollama/SQLite/unrelated-config health;
7. five natural PT1M ticks with `NO_FLASH_MULTI_TICK_PROVEN`;
8. `DASHBOARD_OWNER_SURFACE_READY` read-only proof.

## Hard semantic and mutation fence

Task 087 sends zero semantic messages and zero provider probes.

No Dashboard/WebChat send, `chat.send`, `openclaw agent`, `sessions_send`, channel message, synthetic Ticket mutation, direct Ollama probe, model/provider/timeout change, uninstall/reset/manual plugin cleanup, manual rollover, reboot, merge, tag or release.

The supported installer may be invoked only once. A nonzero result must be captured and reported, not retried.

## Successor gate

Only an independently accepted:

`PASS_LIVE_ATTESTED_PENDING_RECOVERY_PARITY_NO_FLASH_OWNER_SURFACE_READY`

may authorize the final semantic acceptance task.

That final task may send exactly one fresh authenticated Dashboard/WebChat owner message and must prove Ticket-before-provider ordering, correlated Ollama inference, response-ready, exact owner/run delivery confirmation, completed state and exactly one visible nonce response. The Task-076 nonce remains permanently retired.
