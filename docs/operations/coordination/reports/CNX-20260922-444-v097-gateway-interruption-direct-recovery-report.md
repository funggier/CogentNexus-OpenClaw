# CNX-20260922-444 — v0.9.7 Exact Gateway-Interruption Direct Recovery Report

Status: `LOCAL_QUALIFICATION_GREEN_LIVE_ACCEPTANCE_PENDING`

Task: `CNX-20260922-444-v097-gateway-interruption-direct-recovery.md`

Target release line: `v0.9.7`

## Production trigger

A real Discord turn on OpenClaw 2026.9.5 exposed a continuity gap while using the intended OpenClaw-owned route:

- provider/model: `ollama/qwen3.8:27b`;
- Ticket: `CNXT-6866c23d-8c58-4a48-8699-2e48944ffb73`;
- original run: `397c29b1-beeb-4421-b786-abb84c360f52`;
- Ticket accepted: approximately `2026-09-22T11:19:07Z`;
- model call started: `2026-09-22T11:19:10.804Z`;
- CNX observational model-call deadline: `2026-09-22T11:34:10.804Z`;
- external Host entered recoverable maintenance after confirming an unresponsive Gateway: approximately `2026-09-22T11:21:16Z`;
- Gateway process replacement occurred approximately `2026-09-22T11:22:27Z–11:22:30Z`.

The old Gateway process disappeared before model-call terminal hooks could persist `model_call_ended` / failing `agent_end`.

The durable CNX state remained:

- Ticket status: `accepted`;
- Direct model-call state: `active`;
- recovery attempt count: `0`;
- no `cnx_direct_recovery`;
- no outbox;
- no assistant delivery.

OpenClaw later reached its configured whole-run timeout. OpenClaw state recorded approximately `2,705,578 ms` runtime (~45m05s), consistent with `agents.defaults.timeoutSeconds=2700`.

Therefore increasing the OpenClaw timeout is not the repair.

## Timeout authority finding

The CNX 15-minute Direct model-call deadline is observational only.

That deadline is recorded by the model-call observation hook and does not configure the OpenClaw runner timeout.

Historical qualification already proved a successful Qwen turn can take roughly 44m43s. Restoring timer-only destructive recovery would therefore create duplicate-inference risk.

Invariant preserved:

```text
elapsed CNX model-call deadline
+ healthy/current Gateway execution boundary
= observation only
= no cancellation
= no restart
= no replacement inference
```

## Root cause

The provider-neutral Host intentionally suppresses legacy timer-only model-call recovery.

Exact terminal-error recovery exists, but a Gateway process replacement can destroy an in-flight model call before the old process emits terminal hooks. The row then remains `active`, so neither terminal-error recovery nor the startup Direct-Recovery liveness bridge can act.

The old confirmed hard-hang path used one opaque:

```text
lifecycle restart
```

operation.

That provided no quiescent boundary at which to convert old-generation active Direct calls into durable recovery authority.

## v0.9.7 repair

The confirmed hard-hang path is now ordered:

```text
confirmed hard hang
  -> prepare recoverable maintenance
  -> stop/quiesce Gateway
  -> atomically classify eligible active Direct calls as gateway-interrupted
  -> persist pending Direct Recovery
  -> start replacement Gateway
```

Production changes:

- `skills/cogentnexus-openclaw/scripts/host_stall_v091.py`
  - adds exact Gateway-interruption classification;
  - preserves delivery/terminal/workflow/session fences;
  - writes `host_direct_model_gateway_interruption_authorized`;
  - writes model-call outcome `host-gateway-interruption-authorized`;
  - keeps the Ticket in the Direct lane;
  - queues the existing `cnx_direct_recovery` authority;
  - does not inspect or mutate provider routing/lifecycle.

- `skills/cogentnexus-openclaw/scripts/host_v091.py`
  - replaces the opaque confirmed-hard-hang restart with
    `prepare -> stop -> classify -> start`;
  - commits pending recovery before replacement Gateway startup;
  - resolves the current live Gateway PID to its exact `gateway_boot_lifecycle` row;
  - performs post-restart orphan reconciliation only for calls in the immediate predecessor boot window;
  - excludes older-generation historical residue from automatic replay;
  - attempts bounded Gateway restoration if classification/start fails after stop.

## Safety properties retained

The repair does not:

- restore timer-only destructive recovery;
- select or silently change provider/model;
- own Cloud credentials;
- restart Ollama as part of Direct-call recovery;
- regenerate a response-ready Ticket;
- reinterpret delivery uncertainty as inference authority;
- bypass owner session/generation authority;
- modify the immutable v0.9.6 release/tag.

## TDD evidence

Initial RED reproduced the missing behavior:

- missing exact Gateway-interruption classifier;
- confirmed hard-hang path still executed one opaque `lifecycle restart`;
- classification failure did not have a stop/classify/start restoration boundary.

After the minimal production repair:

- focused Host/stall suite: `24/24 PASS`;
- expanded Host/provider/recovery suite: `112/112 PASS`;
- existing timer-only suppression test remains PASS;
- healthy expired-call observational guard remains PASS.

## Full local qualification

Python:

- final full repository suite after exact Gateway-generation evidence scoping: `730 passed, 5 skipped, 38 subtests passed`;
- version/baseline/current-doc focused suite: `53 passed`;
- namespace isolation: PASS;
- v0.9.7 baseline consistency: PASS;
- workspace validation: PASS;
- Cogent self-test: PASS;
- runtime self-test: PASS;
- workflow self-test: PASS;
- benchmark validator positive + tamper self-test: PASS;
- `git diff --check`: PASS;
- Windows PowerShell syntax: PASS;
- PowerShell 5.1 serializer/acceptance self-test: PASS;
- exact root-process numeric/null/argument self-test: PASS.

Plugin:

- `npm ci`: completed;
- dev dependency tree observation: 8 vulnerabilities (4 moderate, 4 high), unchanged class from predecessor and not the production audit;
- Vitest: `91/91 files, 429/429 tests PASS`;
- evaluation: PASS;
- evaluation evidence SHA-256 after exact-scoping repair: `663cc43daf8d25521517d07b1e261451f2d0df62879870d6314f2dd8471c4d00`;
- production `npm audit --omit=dev`: `0 vulnerabilities`;
- plugin schema verification: PASS, 46 config properties / 5 tools;
- Ticket DB bootstrap: PASS, 9 required tables + v095 registration fence;
- package validation: PASS, 290 packed files.

A first package validation attempt correctly rejected CRLF bytes accidentally introduced into `package.json` during the version bump. The candidate was repaired by reconstructing package metadata from the accepted predecessor blob and applying only the v0.9.7 version edit. The successful package validation above is after that correction.

## v0.9.6 -> v0.9.7 install-over preflight repair

Before live install-over, exact preflight review found that the v0.9.7 version bump still allowed only `0.9.4` and `0.9.5` ownership manifests as upgrade predecessors. A RED test using an owned v0.9.6 fixture reproduced the failure: `installedVersion=0.9.6` was rejected against expected `0.9.7`.

The minimal repair adds `0.9.6` to `UPGRADE_FROM_VERSIONS` while retaining all fail-closed ownership checks. Evidence after repair:

- exact v0.9.6 predecessor RED -> GREEN;
- ownership/installer regression: `66 passed, 1 skipped`;
- focused predecessor + install-contract proof: `12 passed`;
- final full Python suite exit: `0`;
- final collection identity: `734 tests collected`;
- final full suite accounting: `729 passed, 5 skipped, 38 subtests passed`.

This repair was completed before any v0.9.7 mutation of the live v0.9.6 installation.

## Exact Gateway-generation evidence scoping repair

Before the first live interruption injection, read-only inspection of the installed v0.9.7 development candidate showed one older historical incident row still intentionally preserved as `active`. That exposed an important pre-acceptance safety issue: the quiesced classifier accepted Gateway-interruption evidence but still selected every eligible `active` Direct call in the database.

That behavior could have replayed historical residue together with the genuinely interrupted current-generation call during a controlled or real hard-hang recovery.

A new RED test added two simultaneous active calls: one exact call listed in the captured current-Gateway evidence and one older historical residue call not listed in that evidence. The RED result proved both were being selected.

The minimal repair now:

1. snapshots current-Gateway Direct calls before `prepare/stop`;
2. resolves the current Gateway PID to its exact `gateway_boot_lifecycle` boundary;
3. records an exact allow-list of `{ticket_id, call_id}` identities owned by that Gateway generation;
4. passes that immutable evidence into the classifier only after Gateway quiescence;
5. classifies only allow-listed calls;
6. leaves older active residue untouched.

Post-repair evidence:

- focused Host/stall suite: `25/25 PASS`;
- selected Host/provider/recovery regression: `60/60 PASS`;
- full Python repository suite: `730 passed, 5 skipped, 38 subtests passed`;
- Vitest: `91/91 files, 429/429 tests PASS`;
- namespace isolation / v0.9.7 baseline / workspace / Cogent / runtime / workflow / benchmark gates: PASS;
- evaluation: PASS, evidence SHA-256 `663cc43daf8d25521517d07b1e261451f2d0df62879870d6314f2dd8471c4d00`;
- production `npm audit --omit=dev`: `0 vulnerabilities`;
- plugin validation: PASS, 290 packed files;
- `git diff --check`: PASS.

The previously installed `d2263cbe...` development candidate is therefore superseded for release acceptance. A new exact candidate must be committed, pushed, pass exact-SHA CI, and be installed over the live machine before the interruption acceptance is executed.

## Version state

Current source/package metadata:

- `VERSION = 0.9.7`;
- package = `0.9.7`;
- manifest = `0.9.7`;
- lock root/package = `0.9.7`.

Publication state remains separate:

- latest published release: `v0.9.6`;
- accepted v0.9.6 tag SHA: `db8433676c2412706ef3b3966c97e3509f2255c8`;
- v0.9.7 is not yet published.

## Remaining gates

Before CNX-444 can be classified release GREEN:

1. freeze an exact v0.9.7 candidate commit;
2. install-over the exact candidate on Windows;
3. verify source/installed parity for the repaired Host files;
4. verify active/MANAGED health and OpenClaw 2026.9.5 route preservation;
5. perform bounded physical lifecycle qualification;
6. perform live exact Gateway-interruption recovery acceptance without duplicate inference/delivery;
7. handle the historical stranded incident Ticket explicitly as residue, without silently replaying it;
8. push the exact candidate and require GitHub CI success;
9. publish v0.9.7 only after local/live/exact-SHA gates are GREEN;
10. independently verify release tag/assets/checksums.

## Current classification

`CNX444_V097_LOCAL_QUALIFICATION_GREEN_LIVE_ACCEPTANCE_PENDING`
