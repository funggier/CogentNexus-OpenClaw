# CNX-20260922-444 — v0.9.7 Exact Gateway-Interruption Direct Recovery Report

Status: `RELEASE_GREEN`

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

## OpenClaw 2026.9.5 explicit Gateway-stop authority repair

The first controlled live interruption acceptance against installed candidate `87a5da93e24c47e219322d25b99c97e487c34624` exposed a second production compatibility gap after exact generation scoping was already correct.

The Host entered recoverable maintenance and attempted the ordered hard-hang boundary, but OpenClaw 2026.9.5 rejected the Gateway stop request because the runtime wrapper invoked `openclaw gateway stop` without explicit force authority. OpenClaw returned the exact safety refusal that stopping the operator's running Gateway requires `--force`.

This was a clean RED, not a recovery-classification failure:

- Gateway remained healthy and running;
- the controlled Direct fixture remained `accepted` / model-call `active`;
- no recovery row was created;
- no maintenance marker was stranded;
- the fixture was explicitly dispositioned through canonical Direct-recovery APIs after the RED observation.

The minimal repair keeps ordinary lifecycle stop behavior unchanged and adds explicit force authority only where CNX already has exact Gateway replacement authority:

- `runtime.py lifecycle stop` now accepts optional `--force` and forwards it to `openclaw gateway stop --force` only when requested;
- confirmed hard-hang replacement passes `--force` to its quiesced Gateway stop;
- exact current-boot orphan reconciliation passes `--force` to its quiesced Gateway stop;
- provider/model/auth/routing ownership remains OpenClaw-owned and no provider stop/restart was added.

RED-to-GREEN evidence:

- three initial failures proved missing force propagation at runtime, hard-hang Host, and boundary-orphan Host layers;
- focused lifecycle/Host suite: `19/19 PASS`;
- selected recovery/lifecycle regression: `62/62 PASS`;
- full Python repository suite: `732 passed, 5 skipped, 38 subtests passed`;
- Vitest: `91/91 files, 429/429 tests PASS`;
- namespace isolation / v0.9.7 baseline / workspace / Cogent / runtime / workflow / benchmark gates: PASS;
- evaluation: PASS, evidence SHA-256 `52fea355d20a58a7f5e4899b04f1a3dbcd8cfd6ae91c46d43a418f17be4ba75e`;
- production `npm audit --omit=dev`: `0 vulnerabilities`;
- plugin validation: PASS, 290 packed files;
- `git diff --check`: PASS.

Candidate `87a5da93...` is superseded for release acceptance. A new exact candidate must pass CI, install-over parity, and the controlled live interruption acceptance before publication.

## Direct model-call owner-session liveness repair

Exact candidate `18f9a5d890a03709aa8d77c21091eecd1940d911` passed exact-SHA CI after the Windows Validate Vitest teardown flake was rerun successfully (Validate run `35758562382`, attempt 3). PS5.1 Acceptance Smoke and Windows Installer Pack Smoke were also SUCCESS.

The candidate was installed over the live Windows machine with source/installed parity confirmed. A fresh controlled current-boot interruption fixture then proved that the OpenClaw 2026.9.5 force-stop repair works physically:

- old Gateway PID: `28328`;
- exact boot ID: `cd955aa0-e2b2-4a1e-a745-44f46a4f7a5d`;
- fixture Ticket: `CNXT-e8296356-e204-4834-9a66-17be730e9f5b`;
- exact model call: `cnx444-force-live-698bfae0:model:1`;
- Gateway stop: PASS with explicit force authority;
- old Gateway verified stopped;
- replacement Gateway became healthy as PID `29592`;
- exact interruption classifier emitted one `host_direct_model_gateway_interruption_authorized` event;
- model-call outcome became `host-gateway-interruption-authorized`;
- exactly one pending `cnx_direct_recovery` row was created;
- no inference attempt, assistant delivery, or outbox duplication was created during classification.

That acceptance exposed a separate recovery-liveness defect. The owner session remained:

```text
state = active
generation = 0
updated_at = 2026-09-22T16:52:42.910Z
```

while the interrupted call/recovery was created around `20:50Z`. The v0.9.7 startup bridge correctly classified the durable recovery as `ready`, but the v0.9.1 worker's 15-minute `sessionLivenessFence` correctly rejected the stale owner heartbeat. Repeated startup pulses therefore could not make the row claimable.

Root cause: `recordDirectModelCallStarted()` persisted exact provider-call liveness but did not refresh the already-active owner session's `updated_at`. A real model-call start is itself exact evidence that the owner generation is live; failing to project that evidence into the session heartbeat made the startup bridge and worker eligibility semantics inconsistent.

The minimal repair:

- expands the exact accepted Direct Ticket lookup to include `owner_session_key`;
- after the model-call lease is successfully written, refreshes only `cnx_sessions.updated_at` for that exact owner when the session row exists and remains `active`;
- does not create/reactivate sessions;
- does not change session state or generation;
- does not relax the 15-minute stale-session fence;
- does not change provider/model/auth/routing ownership.

TDD evidence:

- RED reproduced an active owner session stale by one hour; the successful Direct model-call start left `updated_at` stale and the later recovery remained ineligible;
- GREEN proves the exact model-call start refreshes the owner heartbeat and, after the model-call fence is released, `dueDirectRecovery()` selects the same Ticket under generation 4;
- focused model-call/recovery/liveness cluster: `4 files / 15 tests PASS`;
- full Vitest: `91/91 files, 430/430 tests PASS`;
- evaluation: PASS, evidence SHA-256 `e2e460a5e086b84afe8e6e51f2c8a85563b4a2b5aec071e95f82a3ef56c9931f`;
- production `npm audit --omit=dev`: `0 vulnerabilities`;
- plugin validation: PASS, 290 packed files;
- full Python repository suite: `732 passed, 5 skipped, 38 subtests passed`;
- namespace isolation: PASS;
- v0.9.7 baseline consistency: PASS;
- `git diff --check`: PASS.

The controlled fixture was then dispositioned through the canonical exact-generation Direct-recovery API. Final live cleanup showed zero pending recovery rows and zero pending outbox rows.

Candidate `18f9a5d8...` is superseded for release acceptance. The next exact candidate must pass CI, install-over parity, and a fresh controlled interruption acceptance proving the recovery worker actually claims the pending row and reaches exactly-one inference/delivery.

## OpenClaw 2026.9.5 detached Direct Recovery compatibility repair

After the owner-session liveness repair was installed and physically requalified, a fresh controlled Gateway interruption advanced farther than the prior acceptance: the pending Direct recovery was claimed by the worker and its attempt count increased. No inference had started yet.

The worker then retried with the exact OpenClaw core error:

`Plugin session ownership checks require a SQLite transcript marker.`

This is a separate OpenClaw 2026.9.5 compatibility boundary, not an inference/provider failure. The existing v0.9.5 compatibility wrapper still supplied a temporary filesystem `session.jsonl` as `sessionFile` for the one-shot embedded recovery helper. OpenClaw 2026.9.5 plugin async-action ownership now accepts persisted transcript identity only through its SQLite session target/marker contract and rejects that legacy JSONL target before inference begins.

Installed OpenClaw 2026.9.5 type/runtime evidence also exposes a purpose-built ephemeral contract:

- `sessionPersistence: "detached"`;
- detached runs may use session identity for policy resolution;
- detached runs do not write durable transcript or session metadata.

The minimal repair therefore preserves the existing isolated recovery identity and v0.9.6 `:subagent:` admission fence while removing the obsolete temporary JSONL transcript target:

- no `sessionFile` is supplied;
- the embedded recovery run sets `sessionPersistence: "detached"`;
- `disableTrajectory: true` remains;
- provider/model selection remains inherited from the original Direct call;
- no SQLite marker is fabricated by CogentNexus-OpenClaw;
- no durable helper session is created, so no helper-session cleanup transaction is required.

TDD and regression evidence:

- RED: v0.9.5 compatibility test observed a real temporary `session.jsonl` where the 2026.9.5 contract requires no legacy filesystem transcript target;
- GREEN: focused v0.9.5 compatibility test `2/2 PASS`;
- recovery compatibility cluster v0.9.1 through v0.9.7: `8/8 files, 24/24 tests PASS`;
- full Vitest: `91/91 files, 430/430 tests PASS`;
- full Python repository suite: `732 passed, 5 skipped, 38 subtests passed`;
- namespace isolation / v0.9.7 baseline / workspace / Cogent / runtime / workflow / benchmark gates: PASS;
- evaluation: PASS, evidence SHA-256 `522c2df2e8325403fbe6a69b50bc797d6dfc6624c4c72cc1134873c03661a973`;
- production `npm audit --omit=dev`: `0 vulnerabilities`;
- plugin validation: PASS, 290 packed files;
- `git diff --check`: PASS.

The live fixture that exposed the SQLite marker incompatibility was explicitly dispositioned through the canonical exact-generation Direct-recovery API after observation. It produced no inference, assistant delivery, or outbox result, and no pending recovery row remains.

Candidate `92e945c4...` is superseded for release acceptance. The next exact candidate must pass exact-SHA CI, install-over parity, and a fresh physical interruption acceptance proving detached recovery reaches exactly-one inference/result/delivery without duplicate work.

## Windows Gateway RPC UTF-8 + durable delivery wake repair

The first detached-recovery live acceptance reached a real Direct recovery result:

- Ticket: `CNXT-df3d2a62-f057-4008-b893-df75d7fdf0b8`;
- recovery runtime: exactly one attempt;
- provider/model: `ollama/qwen3.8:27b`;
- response: `CNX444_RECOVERY_OK`;
- recovery state advanced to `awaiting_delivery`;
- exactly one durable `direct_result` delivery row was created.

The first Host delivery attempt then failed before `chat.inject` with:

`OpenClaw Gateway RPC chat.history returned no JSON output (exit=0, stdout=none, stderr=empty)`

Exact reproduction against the installed Host proved the Windows subprocess root cause:

- embedded Python preferred encoding: `cp1252`;
- `openclaw gateway call chat.history --json` returned UTF-8 JSON containing Thai text;
- Python's subprocess reader thread raised `UnicodeDecodeError` while decoding stdout with `cp1252`;
- the failed reader left captured stdout unavailable, producing the observed no-JSON error.

The Host transport repair pins captured OpenClaw Gateway RPC streams to UTF-8 with replacement only for undecodable bytes:

- `encoding="utf-8"`;
- `errors="replace"`;
- command/timeout/check semantics are otherwise unchanged.

A second production defect then prevented the failed durable delivery from retrying. The durable delivery worker still considered the row actionable, but `wake_authority_v095` applied the 15-minute Direct-Recovery liveness cutoff to `cnx_assistant_delivery.updated_at`. Once the pending delivery became older than 15 minutes, Supervisor wake classification returned idle forever even though exact session state/generation remained valid.

The repair removes delivery age as wake authority. Delivery remains actionable until settled or fenced by durable authority:

- owner session must still exist and remain `active`;
- owner generation must still match;
- terminal ticket rules remain unchanged;
- Direct-Recovery 15-minute session-liveness fencing remains unchanged;
- delivery retry/backoff remains owned by `host_delivery.next_actionable_delivery()`.

RED-to-GREEN evidence:

- UTF-8 capture focused delivery suite: `9/9 PASS`;
- wake authority RED reproduced an old pending delivery incorrectly returning idle;
- delivery/wake/actionability regression cluster: `34/34 PASS`;
- stale Direct-owner liveness tests remain PASS;
- full Python repository suite: `733 passed, 5 skipped, 38 subtests passed`;
- full Vitest: `91/91 files, 430/430 tests PASS`;
- namespace isolation / v0.9.7 baseline / workspace / Cogent / runtime / workflow / benchmark gates: PASS;
- evaluation: PASS, evidence SHA-256 `376525eee0cb331163169f75567ec7583e552e31a7ff515ba3255e30b2fbcbf4`;
- production `npm audit --omit=dev`: `0 vulnerabilities`;
- plugin validation: PASS, 290 packed files;
- `git diff --check`: PASS.

The live pending delivery remains durable evidence and will be used after exact-candidate install-over to prove that the repaired Supervisor wake + UTF-8 Gateway RPC path retries and settles without regenerating inference.

## Supervisor durable-delivery dispatch repair

The exact candidate `742248ca7785f6e4ef377f7b2fd25e1ad210d81e` was then installed over the live Windows machine before touching the preserved durable result. The install completed with exit code 0 and restored the canonical runtime contract:

- source/installed parity: PASS for `host_delivery.py`, `wake_authority_v095.py`, `host_v091.py`, `host_stall_v091.py`, `runtime.py`, and `namespace_ownership.py`;
- plugin: v0.9.7, enabled and loaded;
- controller: active/MANAGED, generation 16, `providerOwnership=openclaw`;
- OpenClaw: 2026.9.5;
- route: `ollama/qwen3.8:27b`;
- `agents.defaults.timeoutSeconds=2700`;
- canonical `CogentNexus-OpenClaw-Supervisor`: Ready, Enabled, `LastTaskResult=0`.

Before the retry, the preserved live Ticket still proved exactly one recovery result and no regeneration:

- Ticket `CNXT-df3d2a62-f057-4008-b893-df75d7fdf0b8` remained `accepted`;
- stored response remained `CNX444_RECOVERY_OK`;
- Direct recovery remained `awaiting_delivery`, `attempt_count=1`;
- exactly one `direct_result` delivery row remained `pending`, `attempt_count=1`;
- no `ticket_outbox` row existed;
- exactly one `host_direct_model_gateway_interruption_authorized`, one `direct_recovery_runtime_started`, and one `direct_recovery_response_ready` event existed;
- no new inference attempt was created.

A canonical Supervisor run still left that durable state unchanged. Source tracing showed why: `wake_authority_v095.classify_wake()` correctly returned `authority=delivery`, but `host_v091.supervisor_tick()` sent every actionable wake into the legacy heavy Supervisor. That path reconciles runtime health/workflows and never calls `host_delivery.flush_deliveries()`. The previous regression test mocked the legacy heavy path as though it consumed delivery, so the missing production wiring was not covered.

The new TDD repair is deliberately narrow:

- RED: an authoritative `wake/delivery` decision expected the Host delivery bridge, but `_execute_delivery_wake` was called 0 times;
- GREEN: only canonical assistant-delivery wakes (`wake/delivery` and the assistant-delivery legacy compatibility reason) dispatch to bounded `host_delivery.flush_deliveries(root, limit=1)`;
- non-execute-safe observation returns delivery-pending without side effects;
- outbox/direct-recovery legacy wake reasons retain their existing path;
- provider/model/auth/routing ownership is unchanged.

Local qualification after the production repair:

- focused wake/session/delivery cluster: `16/16 PASS`;
- expanded Host/wake/delivery regression: `45/45 PASS`;
- full Python repository suite: `734 passed, 5 skipped, 38 subtests passed`;
- full Vitest: `91/91 files, 430/430 tests PASS`;
- namespace isolation / v0.9.7 baseline / workspace / Cogent / runtime / workflow / benchmark gates: PASS;
- Windows PowerShell syntax / PS5.1 serializer / exact root-process self-tests: PASS;
- evaluation: PASS, evidence SHA-256 `d99762bc9c272f9d087c187535fc2b61e6cd8bd6781d6ff7ab963f9e67172966`;
- production `npm audit --omit=dev`: `0 vulnerabilities`;
- plugin validation: PASS, 290 packed files;
- `git diff --check`: PASS.

Candidate `742248ca...` is retained as diagnostic live evidence but is superseded for release acceptance because it lacks the Supervisor delivery-dispatch repair. The preserved durable delivery intentionally remains the first live proof target for the next exact candidate; it must settle from stored `CNX444_RECOVERY_OK` without another recovery inference.

## Version state

Current source/package metadata:

- `VERSION = 0.9.7`;
- package = `0.9.7`;
- manifest = `0.9.7`;
- lock root/package = `0.9.7`.

Publication state:

- latest published release: `v0.9.7`;
- accepted v0.9.7 tag SHA: `43f970895e3b6fe5de6d2f11ffe6bf544fcd2026`;
- Release workflow: `35948011186` — SUCCESS;
- v0.9.6 remains immutable historical evidence.

## Historical incident residue disposition

The original production incident Ticket `CNXT-6866c23d-8c58-4a48-8699-2e48944ffb73` is already explicitly retired through canonical durable authority. Read-only live DB verification shows:

- Ticket state: `cancelled`;
- Direct recovery state: `cancelled`, `attempt_count=0`;
- event: `direct_recovery_dispositioned`;
- disposition reason: recovery was created by a superseded pre-exact-scoping candidate and the historical operator request must not be replayed.

This gate is satisfied and the historical Ticket must not be reopened during final acceptance.

## Final exact candidate and live acceptance

Final candidate:

`43f970895e3b6fe5de6d2f11ffe6bf544fcd2026` — `fix(v0.9.7): fence native restart recovery ownership`

The final repair closed the last duplicate-result hazard discovered during physical acceptance. OpenClaw 2026.9.5 can synthesize a native restart-continuation prompt after a Gateway restart. The earlier ownership fence recognized only the older restart prompt and only `host-timeout-authorized` durable authority, so the OpenClaw native continuation could run in parallel with already-authorized CNX Direct Recovery.

The final v0.9.7 ownership repair:

- recognizes the exact legacy and OpenClaw 2026.9.5 restart prompt forms;
- accepts durable CNX ownership from either `host-timeout-authorized` or `host-gateway-interruption-authorized`;
- blocks only restart dispatches with matching durable recovery authority;
- suppresses the synthetic restart-shaped user transcript message;
- cancels the corresponding blocked-run gate reply;
- remains fail-open for ordinary user input, unknown prompts, missing DB evidence, or ambiguous ownership.

TDD and full local proof after the final repair:

- focused native-restart ownership suite: `12/12 PASS`;
- full Python repository suite: `737 passed, 5 skipped, 38 subtests`;
- full Vitest: `92 files / 432 tests PASS`;
- production `npm audit --omit=dev`: `0 vulnerabilities`;
- plugin validation: PASS, `292` packed files;
- namespace / baseline / workspace / Cogent / runtime / workflow gates: PASS;
- `git diff --check`: PASS.

Exact-SHA CI for `43f970895e3b6fe5de6d2f11ffe6bf544fcd2026`:

- Validate run `35944572696`: SUCCESS;
- PS5.1 Acceptance Smoke run `35944572682`: SUCCESS;
- Windows Installer Pack Smoke run `35944572655`: SUCCESS.

The exact candidate was installed over the live Windows system. Installation completed with exit code 0, restored active/MANAGED generation 28, retained OpenClaw 2026.9.5 health, retained the canonical Supervisor as Ready/Enabled with `LastTaskResult=0`, and preserved the OpenClaw-owned route `ollama/qwen3.8:27b`. Source/installed parity passed for the final ownership fence and exact Gateway-interruption classifier.

Final controlled physical Ticket:

- session: `agent:main:cnx444-final-43f97089`;
- Ticket: `CNXT-52baf1dc-c5b9-4971-b8d0-db0f6d27abde`;
- original run: `bd0204f3-a4de-4c0e-b901-fe56595a5a46`;
- original model call: `bd0204f3-a4de-4c0e-b901-fe56595a5a46:model:1`;
- canonical attempt: `cnx-attempt-a5ec10b5-f480-46a8-9358-d77e94d26f0b`;
- provider/model: `ollama/qwen3.8:27b`;
- response token: `CNX444_FINAL_43F97089_20260924_OK`.

The production hard-hang path captured the exact old Gateway boundary and completed with exit code 0. The underlying OpenClaw stop command reported `disk I/O error`, but the Host independently verified the old Gateway was stopped, classified only the exact captured call, restored a healthy replacement Gateway, and completed the bounded recovery path. This command-level warning is retained here rather than reclassified as a clean stop.

Durable acceptance result:

- Direct model call: `interrupted`;
- model-call outcome: `host-gateway-interruption-authorized`;
- exact canonical inference attempt: `ended`;
- inference-attempt outcome: `host-gateway-interruption-authorized`;
- exactly one `inference_attempt_ended` event;
- exactly one Direct Recovery runtime;
- Direct Recovery `attempt_count=1`;
- recovery provider/model preserved as `ollama/qwen3.8:27b`;
- exactly one `direct_recovery_response_ready`;
- exactly one `direct_result` delivery row;
- delivery status: `delivered`, attempt count `0`;
- Ticket status: `completed`;
- no outbox row;
- no duplicate inference, recovery, response-ready, or delivery work.

The dedicated OpenClaw transcript contained exactly two messages: the original user prompt and one assistant delivery. The assistant token appeared once, the CNX delivery marker appeared once, and no OpenClaw native restart synthetic user message, duplicate assistant result, or restart-control gate reply appeared.

## Release publication and independent verification

`main` was fast-forwarded without force from `8a6112016a6affa73e3ad5b7d5c2dbb701e7e133` to the accepted candidate.

Release workflow:

- workflow: `Release`;
- run: `35948011186`;
- event: `workflow_dispatch`;
- candidate SHA: `43f970895e3b6fe5de6d2f11ffe6bf544fcd2026`;
- package job: SUCCESS;
- publish job: SUCCESS;
- overall conclusion: SUCCESS.

Published release:

- tag: `v0.9.7`;
- target: `43f970895e3b6fe5de6d2f11ffe6bf544fcd2026`;
- draft: false;
- prerelease: false;
- published: `2026-09-24T02:40:09Z`.

Independent public-asset verification downloaded the release to `T:\CNX-release-verify\v0.9.7` and recomputed hashes:

- `cogentnexus-openclaw-v0.9.7.tar.gz`:
  `6af5d0d23606ebd2bfe5f2974d0c237c001fd5e6ec8e0f6867ba24068c65c9bf`;
- `cogentnexus-openclaw-v0.9.7.zip`:
  `190b1224fc23f45a662e6e66d15a4e651313e13ee2782ccc2ad8df48674bee12`;
- `SHA256SUMS.txt`:
  `4e9fdda8c43373366cf3ba18704a8fe0831f77412c1819185407af29771b5485`.

The ZIP/TAR hashes match both the downloaded `SHA256SUMS.txt` and GitHub asset digests. Required release files were independently found inside the downloaded ZIP.

## Completed release gates

1. exact v0.9.7 candidate frozen and pushed — PASS;
2. exact-SHA GitHub CI — PASS;
3. Windows install-over of exact candidate — PASS;
4. installed/source parity — PASS;
5. active/MANAGED OpenClaw 2026.9.5 health and route preservation — PASS;
6. preserved durable delivery settlement without inference regeneration — PASS;
7. bounded physical lifecycle qualification — PASS;
8. fresh exact Gateway-interruption recovery with no duplicate inference/delivery — PASS;
9. v0.9.7 publication — PASS;
10. independent tag/assets/checksum verification — PASS.

## Current classification

`CNX444_V097_RELEASE_GREEN`
