# CNX-20260831-192 — NO_REPLY Repair Windows Requalification

- **Status:** `READY_FOR_HERMES`
- **Date:** 2026-08-31 ICT
- **Repository:** `funggier/CogentNexus-OpenClaw`
- **Working branch:** `agent/v0.9.3-full-stabilization`
- **Parent umbrella:** `CNX-20260831-188`
- **Parent repair:** `CNX-20260831-191`
- **Triggered by:** Task-190 `FAIL_SEMANTIC_DURABLE_DELIVERY`
- **Executor:** Hermes on accepted Windows host + exactly one genuine human Dashboard Send by user
- **Coordinator / final reviewer:** ChatGPT
- **Human release authority:** User

## Mission

Requalify the repaired v0.9.3 candidate on the accepted real Windows host with the smallest scope proportional to the Task-191 executable plugin change.

This task must prove that the `NO_REPLY` direct-Dashboard repair works in the actual OpenClaw/Ollama runtime while preserving the already-accepted install-over, provenance, health, and durable exactly-once semantics.

## Immutable product candidate

Use exactly:

`050ab53f4b593ab538143084d6bbdbf7e1672e34`

This SHA is the repaired **product candidate**.

Any later commits on `agent/v0.9.3-full-stabilization` are coordination/report commits only and **DO NOT redefine the product candidate**.

Hermes must not install branch HEAD unless it is exactly the candidate above. Acquire/check out the exact candidate in an isolated/detached candidate worktree or equivalent supported mechanism.

Historical pre-repair candidate `604569c286e930f1a596362ab926b065b56d486e` must not be installed for this task.

## Candidate identities

- root Git tree: `1c10a631b58e1609fc76168e76a26dbe72444e6c`
- plugin tree `plugins/cogentnexus-openclaw`: `eeab5fb8c67e5c16284d5df49ec413a53c251a13`
- fixed source blob `v091-dashboard-verified-delivery.ts`: `aa97d7a5411f799c612cd0aeece050085298a8bb`
- installed skill tree `skills/cogentnexus-openclaw`: `a1e873ba404205507a1623961b49f1b1a0689f9f`
- executable skill scripts-tree: `3d9d323ba19443d46e970b87cef52ce878da274f`
- `cnxclaw.py` Git blob: `879083d6186589d4b2774b8fd87fa93692dd2dfc`
- expected accepted Windows facade SHA-256, to be re-proved live: `aa747f8f30080ef839a8d2cbf5758f9981a007ca01f41a988576f42edea8682f`
- package payload-v2: `b1ca9f3b42009cf4b1ae0a04f0e75add8d2ff9bd5dc97fce4040dc4753562d93`
- package file count: `186`

## Exact-candidate CI already passed

Candidate `050ab53f4b593ab538143084d6bbdbf7e1672e34` has fresh successful repository gates:

1. Validate `33390552591` — `completed/success`
   - package dry-run success;
   - Ubuntu 3.11/3.14 success;
   - macOS 3.11/3.14 success;
   - Windows 3.11/3.14 success;
   - Python, plugin tests, evaluation, production audit, plugin validation all green.
2. PS5.1 Acceptance Smoke `33390552613` — `completed/success`.
3. Windows Installer Pack Smoke `33390552545` — `completed/success`.

Task-191 regression evidence on exact candidate:

- `src/v191-no-reply-direct-dashboard.test.ts`: `2/2` PASS;
- plugin suite: `54` files / `275` tests PASS on inspected exact-candidate matrix job.

## Package proof

- artifact ID: `9757273396`
- artifact name: `cogentnexus-openclaw-v0.9.3-package-proof-050ab53f4b593ab538143084d6bbdbf7e1672e34`
- artifact size: `5,307,533` bytes
- artifact ZIP digest: `7bfa3d16ed12ab0ee380ad62f7ac512381252c90c35618970038b4efa61d86cc`
- tar: `cogentnexus-openclaw-v0.9.3.tar.gz`
  - SHA-256: `7ed09e96163bd1e3fb3977abe30439728e93fb0a54ea2104286de8ece7cb4950`
- zip: `cogentnexus-openclaw-v0.9.3.zip`
  - SHA-256: `d4c478365475ed7dd064168a89caf9bce89c5486d4238947cd048de0c4070c6a`

These are CI proof artifacts only; do not publish a GitHub Release in this task.

## Repair semantics under test

Task 191 changed only the direct Dashboard verified-delivery boundary plus its regression test.

Required behavior:

1. Bare `NO_REPLY` or `no_reply`, after trim and case-insensitive exact match, is a silent sentinel and must **not** be staged as `cnx_assistant_delivery`, markerized, or shown as a logical Dashboard assistant result.
2. Mixed substantive text containing the token remains ordinary visible content.
3. For a genuine accepted direct Dashboard Ticket, if the first natural final assistant answer is the bare sentinel, `before_agent_finalize` may request exactly one same-run OpenClaw revision:
   - `action='revise'`;
   - idempotency key `cnxclaw-dashboard-visible-final:<runId>`;
   - `maxAttempts=1`;
   - instruction requests a visible answer and forbids `NO_REPLY/no_reply` for that turn.
4. CogentNexus must not fabricate the visible answer itself.
5. No external CogentNexus direct-recovery run may be created for this semantic repair.

## Hard fence

Authorized:

- read-only host/state/provenance checks;
- exactly one supported install-over of exact candidate `050ab53f...`;
- normal service/runtime convergence caused by supported installer/runtime behavior;
- exactly one genuine human Dashboard Send, when Hermes explicitly instructs the user;
- read-only post-send observation/evidence collection;
- this report and coordination-only commits.

Not authorized:

- reset;
- uninstall;
- fresh reinstall;
- state/database deletion;
- provider replacement;
- OpenClaw upgrade/downgrade;
- production/source/test/dependency/workflow/schema changes;
- second human Send;
- retry Send;
- regenerate;
- `chat.inject` or synthetic semantic injection;
- release PR merge;
- Release workflow dispatch;
- tag/release publication;
- force push.

If any excluded action appears necessary, STOP and report instead of expanding scope.

# Execution phases

## Phase A — read-only preflight

Before candidate acquisition or installation, capture:

- current branch/coordination authority;
- host identity sufficient to establish this is the accepted Windows host;
- current OpenClaw version, expected `2026.7.1-2 (0790d9f)`;
- current CogentNexus mode/state;
- managed provider identity and health, expected Ollama;
- Gateway status/connectivity;
- delivery readiness and pending outbox count;
- recovery readiness / active incident state;
- SQLite integrity;
- durable table counts at minimum:
  - `tickets`
  - `ticket_events`
  - `ticket_outbox`
  - `cnx_assistant_delivery`
  - `cnx_direct_model_call`
  - `cnx_direct_recovery`
  - `cnx_sessions`
- current installed facade SHA-256;
- current installed plugin/package provenance if available.

Do not mutate anything in Phase A.

If host/runtime is materially unhealthy before install-over, stop with `BLOCKED_HOST_DRIFT` rather than using Task 192 to repair unrelated state.

## Phase B — exact candidate acquisition

Acquire exactly:

`050ab53f4b593ab538143084d6bbdbf7e1672e34`

Prove:

- commit SHA exact;
- root tree exact;
- fixed source blob exact;
- package payload/version/file count exact;
- candidate is not a later coordination HEAD.

Prefer isolated/detached candidate acquisition so coordination commits cannot accidentally enter the installed product.

## Phase C — exactly one supported install-over

Perform exactly one supported repository/release-style install-over from the exact candidate using the normal installer path accepted by previous Windows tasks.

Record:

- exact command/path;
- candidate source/provenance;
- exit code;
- relevant installer output;
- whether normal runtime/service convergence occurred.

No retry of install-over is authorized. If it fails, report `FAIL_INSTALL_OVER`.

## Phase D — post-install provenance and health

After install-over, prove:

### Installed product identity

- installed plugin corresponds to candidate plugin/package bytes;
- fixed `NO_REPLY` repair is present in installed built plugin payload;
- package/provenance points to exact candidate `050ab53f...` where supported;
- installed skill tree remains candidate-consistent;
- facade SHA-256 remains:
  `aa747f8f30080ef839a8d2cbf5758f9981a007ca01f41a988576f42edea8682f`.

Do not compare TypeScript source to installed JavaScript naively. Prove the installed built plugin using candidate package/build identities or exact corresponding built-file hashes.

### Runtime health

Prove:

- OpenClaw remains `2026.7.1-2 (0790d9f)`;
- mode/state is expected MANAGED operating state;
- managed provider remains Ollama;
- provider healthy/reachable/ready;
- Gateway healthy/listening/connectivity probe ok;
- delivery `READY`, read-only checks do not mutate state, pending outbox `0`;
- recovery healthy/ready with no active incident requiring intervention;
- SQLite `PRAGMA integrity_check=ok`;
- install-over did not unexpectedly destroy prior durable state.

If installed executable/plugin identity differs from candidate, stop as `BLOCKED_EXECUTABLE_IDENTITY_DRIFT` or `FAIL_INSTALL_OVER`; do not proceed to semantic Send.

## Phase E — one genuine human Dashboard semantic turn

Hermes owns orchestration but **must not perform the Send**.

### E.0 — fresh pre-send attribution baseline

Immediately before asking the user to Send, record a fresh read-only baseline of durable counts and health sufficient to attribute exactly one new turn.

### E.1 — generate nonce and instruct user

Generate a fresh nonce immediately before instruction:

`CNX192-<UTC timestamp>-<short random suffix>`

Tell the user to send exactly this one-line prompt in the normal OpenClaw Dashboard:

`ตอบกลับข้อความนี้เพียงว่า <nonce>`

Tell the user:

- Send exactly once;
- do not retry;
- do not regenerate;
- do not send a second message even if the local model is slow;
- return to Hermes and say `ส่งแล้ว` after the one Send.

Hermes must then remain in the same execution context and continue post-send evidence collection immediately when the user reports `ส่งแล้ว`.

### E.2 — Hermes interaction fence

Hermes must not:

- click Send;
- press Enter as Send;
- invoke a chat send tool;
- use `chat.inject`;
- fabricate/inject the user prompt;
- perform a second semantic turn.

Human Send budget is exactly `1 / 1`.

### E.3 — observe settlement read-only

After the user says `ส่งแล้ว`, observe read-only until terminal settlement or a clearly bounded failure state.

The local model may be slow. Do not infer failure from elapsed time alone and do not retry while the correlated Ticket/model call is still legitimately in flight.

### E.4 — accepted semantic shapes

A PASS may take one of two forms.

#### Shape A — no sentinel emitted

`1 human Send -> 1 Ticket -> 1 logical OpenClaw run -> 1 Ollama model call -> 1 durable assistant delivery -> 1 logical visible Dashboard assistant result`

#### Shape B — first natural final is bare sentinel and repaired hook revises once

`1 human Send -> 1 Ticket -> 1 logical OpenClaw run -> first natural final bare NO_REPLY -> exactly 1 same-run finalization revision -> final visible answer -> 1 durable assistant delivery -> 1 logical visible Dashboard assistant result`

For Shape B:

- bare sentinel must **not** create a durable `cnx_assistant_delivery` row;
- bare sentinel must **not** receive a CogentNexus marker;
- bare sentinel must **not** appear as a logical Dashboard assistant bubble;
- exactly one same-run revision is allowed;
- revision idempotency key must correspond to `cnxclaw-dashboard-visible-final:<runId>` where observable;
- `maxAttempts` behavior must be bounded to one revision;
- final visible content must correspond to the requested nonce acknowledgement;
- there must still be only one Ticket and one final durable delivery;
- `cnx_direct_recovery` delta must remain `0` for this turn;
- no second human Send/regenerate/injection.

The same-run host-owned finalization revision may result in a second model inference inside the same logical run depending on OpenClaw hook semantics. This is allowed **only** for the bounded sentinel revision and must not create a second Ticket, external recovery run, or duplicate durable result.

### E.5 — semantic PASS criteria

All must hold:

1. exactly one human Send;
2. exactly one correlated new Ticket;
3. exactly one logical OpenClaw run/Ticket execution;
4. no external CogentNexus direct recovery;
5. no duplicate Ticket;
6. no duplicate durable assistant delivery;
7. one final durable `direct_result` corresponding to the visible assistant result;
8. final durable text is not bare `NO_REPLY`/`no_reply`;
9. final Dashboard logical assistant content corresponds to the nonce acknowledgement;
10. no visible bare `NO_REPLY` assistant result;
11. pending terminal outbox returns to `0`;
12. SQLite remains healthy;
13. Gateway/Ollama/delivery/recovery health remains acceptable after settlement.

If a bare sentinel remains after the single permitted revision, or there is no visible semantic answer, classify `FAIL_SEMANTIC_DURABLE_DELIVERY` and STOP. Do **not** request another human Send.

## Phase F — final health/provenance

After semantic settlement, re-prove:

- exact installed candidate/product identity;
- facade hash;
- OpenClaw baseline;
- managed Ollama health;
- Gateway health;
- delivery readiness / pending outbox zero;
- recovery state;
- SQLite integrity;
- durable counts and correlation.

## Required report

Publish:

`docs/operations/coordination/reports/CNX-20260831-192-no-reply-repair-windows-requalification.md`

Required disposition must be one of:

- `PASS`
- `FAIL_INSTALL_OVER`
- `FAIL_INSTALLED_IDENTITY`
- `FAIL_SEMANTIC_DURABLE_DELIVERY`
- `BLOCKED_HOST_DRIFT`
- `BLOCKED_EXECUTABLE_IDENTITY_DRIFT`
- `REQUALIFICATION_SCOPE_EXPANSION_REQUIRED`

Report must contain exact evidence, not only conclusions.

## Stop boundary

After publishing the Task-192 report, STOP for ChatGPT review.

Hermes must not create or merge a release PR, dispatch the Release workflow, create `v0.9.3`, publish assets, or perform any destructive lifecycle action.
