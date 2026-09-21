# CogentNexus-OpenClaw Current Operational State

**Current source/release line:** `v0.9.6`
**Current working branch:** `cnx-357-openai-dashboard-ticket-first-requalification-v2`
**Latest physical runtime acceptance:** OpenClaw `2026.9.5 (ec9c1a1)`
**Regression/dev dependency pin:** OpenClaw `2026.7.1-2`
**Managed provider ownership:** **Ollama**
**Cloud/provider/model/auth routing:** OpenClaw-owned **pass-through**
**License:** MIT

GitHub Releases/tags are authoritative for whether a release has actually been published. The source line may advance to the next version before the publication workflow completes.

## Current classification

The v0.9.6 source line includes the CNX-442 session-input serialization and authoritative Stop repair, physically requalified on Windows against OpenClaw 2026.9.5.

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
| Latest physical OpenClaw compatibility | `2026.9.5 (ec9c1a1)` |
| Regression/dev OpenClaw dependency pin | `2026.7.1-2` |
| Response-ready immutability | Accepted |
| Durable result/delivery confirmation | Accepted |
| Session-generation fencing | Accepted |
| Restart recovery for held unbound ingress | Accepted in repository tests |
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

The final CNX-442 source qualification before documentation/release convergence reported:

- affected Stop/FIFO/restart/wiring suite: `49/49 PASS`;
- full plugin suite: `427 PASS / 1 historical CNX-383 RED`;
- TypeScript build: PASS;
- `plugin:validate`: PASS;
- Ticket DB/package validation: PASS;
- supported Windows install-over: PASS.

CNX-443 re-runs the release gates against the final v0.9.6 candidate before publication.

## Coordination state

The old Codex `legacy coordination watch` automation was retired and removed. Current coordination is explicit GitHub state plus direct ChatGPT/Hermes execution when required. Do not recreate the retired one-minute watcher from historical instructions.

See:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`
- `docs/operations/coordination/README.md`

## Historical evidence policy

Completed versioned release notes, acceptance files, tasks, reports, and reviews describe the states that existed when they were written. They remain immutable evidence unless a factual transcription error is discovered. Current-facing documents point to the latest accepted state instead of rewriting history.
