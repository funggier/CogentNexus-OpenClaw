# CogentNexus-OpenClaw Current Operational State

**Current source line:** `v0.9.7` (published accepted baseline)
**Published baseline branch:** `main`
**Validated OpenClaw runtime baseline:** `2026.9.5 (ec9c1a1)`
**Regression/dev dependency pin:** OpenClaw `2026.7.1-2` (test/development dependency only; not the current live baseline)
**Managed provider ownership:** **Ollama**
**Cloud/provider/model/auth routing:** OpenClaw-owned **pass-through**
**License:** MIT
**Published release:** `v0.9.7`
**Accepted release/tag SHA:** `43f970895e3b6fe5de6d2f11ffe6bf544fcd2026`
**Release workflow:** `35948011186` — SUCCESS

GitHub Releases/tags are authoritative for whether a release has actually been published. The source line may advance to the next version before the publication workflow completes.

## Current classification

CNX-444 / v0.9.7 is complete and release GREEN. The published release closes the exact Gateway-process-boundary continuity gap without restoring timer-only destructive recovery.

Final v0.9.7 evidence:

- exact candidate/tag SHA: `43f970895e3b6fe5de6d2f11ffe6bf544fcd2026`;
- exact-SHA CI: Validate `35944572696`, PS5.1 Acceptance Smoke `35944572682`, Windows Installer Pack Smoke `35944572655` — all SUCCESS;
- installed/source parity: PASS;
- live OpenClaw baseline: `2026.9.5 (ec9c1a1)`, active/MANAGED;
- route preserved: `ollama/qwen3.8:27b`, with provider/model/auth routing OpenClaw-owned;
- final live Ticket: `CNXT-52baf1dc-c5b9-4971-b8d0-db0f6d27abde`;
- Direct model call became `interrupted` with `host-gateway-interruption-authorized`;
- exact canonical inference attempt became `ended` with the same outcome;
- exactly one Direct Recovery ran with `attempt_count=1`;
- exactly one result was delivered: `CNX444_FINAL_43F97089_20260924_OK`;
- final dedicated transcript contained exactly one user message and one assistant delivery, with no OpenClaw native-restart duplicate/control message;
- Release workflow `35948011186`: SUCCESS;
- public `v0.9.7` release is non-draft/non-prerelease and targets the exact accepted SHA;
- downloaded public ZIP/TAR hashes independently matched `SHA256SUMS.txt` and GitHub asset digests.

Final CNX-442 classification:

- `CNX442_PRE_DISPATCH_FIFO_AUTHORITATIVE_STOP_GREEN`
- `CNX442_NO_SUCCESSOR_HOST_RUN_GREEN`
- `CNX442_USER_VISIBLE_STOP_GREEN`

The repair changed queue ownership rather than compensating after OpenClaw had already dequeued a successor message. Later same-generation owner input is durably accepted and held at the claiming `before_dispatch` boundary until older work settles. A valid Stop cancels current + held Tickets before held input reaches the Host queue.

## Final CNX-442 live evidence

Accepted physical session:

`16c1fe33-c906-4391-91ae-b2f0bc3f51b0`

Active Ticket / run:

- Ticket `CNXT-add61119-da8e-475b-9dc5-21d3e9096b9b`
- run `63d998b2-6b12-4639-a0b5-0ce240518fb1`
- provider/model `ollama / qwen3.8:27b`
- context `24576`

Held Ticket:

- Ticket `CNXT-abca44db-728b-4bf1-aef7-9c7d993002a0`
- `bound_run_id = NULL`
- model calls `0`
- inference attempts `0`

After Stop:

- owner generation advanced exactly once: `22 -> 23`;
- active Ticket became `cancelled`;
- held Ticket became `cancelled`;
- held Ticket remained unbound with zero inference;
- pending outbox `0`;
- active Direct Recovery `0`;
- OpenClaw session ended `killed`, not `failed`;
- Host trajectory contained one run only;
- Host transcript did not contain the queued second message;
- no successor Host run was created;
- no new `blocked by cogentnexus-openclaw` or `This turn ended before a reply` appeared.

## Capability boundary

| Capability | Current state |
| --- | --- |
| Ticket-first durable admission | Accepted |
| Pre-dispatch same-session FIFO | Accepted and physically requalified |
| Authoritative user Stop generation barrier | Accepted and physically requalified |
| Held queued Ticket zero-inference cancellation | Accepted |
| No-successor Host run after Stop | Accepted |
| DIRECT lane without forced workflow promotion | Accepted |
| Host-managed recovery authority | Accepted |
| Gateway lifecycle control | Accepted |
| Managed local provider | Ollama |
| Cloud/model/auth routing | OpenClaw-owned pass-through |
| Validated OpenClaw runtime baseline | `2026.9.5 (ec9c1a1)` |
| Regression/dev OpenClaw dependency pin | `2026.7.1-2` (test/development only) |
| Response-ready immutability | Accepted |
| Durable result/delivery confirmation | Accepted |
| Session-generation fencing | Accepted |
| Restart recovery for held unbound ingress | Accepted in repository tests |
| Exact Gateway-interruption recovery for bound active Direct calls | Accepted and physically requalified in v0.9.7 |
| PASSTHROUGH/native compatibility | Accepted |
| MAINTENANCE deliberate-stop semantics | Accepted |
| reset/uninstall ownership boundaries | Accepted |
| Abrupt power-loss/cold-boot acceptance | Still broader than the final CNX-442 proof |
| High-concurrency/long-soak hardening | Not fully accepted |
| Disk-full/DB-corruption recovery | Not production-hardened |
| Arbitrary external side effects exactly once | Requires adapter idempotency/receipt verification |

## OpenClaw compatibility wording

Two separate facts must not be conflated:

1. `plugins/cogentnexus-openclaw/package.json` keeps OpenClaw `2026.7.1-2` as the regression/dev dependency pin.
2. The latest real installed runtime used for final CNX-442 physical acceptance was OpenClaw `2026.9.5 (ec9c1a1)`.

The package peer range is an install compatibility declaration, not an operational guarantee across every OpenClaw version.

## Provider boundary

OpenClaw owns Cloud authentication, routing, provider runtime lifecycle, and probing; CogentNexus-OpenClaw owns durable continuity/recovery evidence and managed Ollama health/lifecycle only.

CogentNexus-OpenClaw manages Ollama only when local managed-provider ownership is active. Cloud providers and model selection remain OpenClaw-owned. CogentNexus-OpenClaw does not take ownership of Cloud credentials, authentication refresh, or provider lifecycle.

Historical LM Studio/provider experiments remain historical evidence only.

## Known validation baseline

Final CNX-444 / v0.9.7 evidence:

- final full Python suite before candidate freeze: `737 passed, 5 skipped, 38 subtests`;
- final full Vitest: `92 files / 432 tests PASS`;
- focused native-restart ownership regression: `12/12 PASS`;
- production `npm audit --omit=dev`: `0 vulnerabilities`;
- plugin validation: PASS, `292` packed files;
- namespace/baseline/workspace/Cogent/runtime/workflow gates: PASS;
- exact-SHA CI: all required workflows SUCCESS;
- Windows same-version install-over: PASS;
- exact live Gateway interruption and exactly-once recovery/delivery: PASS;
- native OpenClaw restart duplicate suppression: PASS;
- public release asset checksum verification: PASS.

CNX-443 / v0.9.6 remains immutable historical evidence and was not rewritten.

## Coordination state

The old Codex `legacy coordination watch` automation was retired and removed. Current coordination is explicit GitHub state plus direct ChatGPT/Hermes execution when required. Do not recreate the retired one-minute watcher from historical instructions.

See:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`
- `docs/operations/coordination/README.md`

## Historical evidence policy

Completed versioned release notes, acceptance files, tasks, reports, and reviews describe the states that existed when they were written. They remain immutable evidence unless a factual transcription error is discovered. Current-facing documents point to the latest accepted state instead of rewriting history.