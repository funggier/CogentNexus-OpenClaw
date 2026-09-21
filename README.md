# CogentNexus-OpenClaw

CogentNexus-OpenClaw is a durable Host/control layer for OpenClaw. It keeps accepted user intent outside the lifetime of a single model call, OpenClaw session, Gateway process, delivery attempt, or context window.

## Current status

- **Current source/release line:** `v0.9.6`
- **Latest physically accepted OpenClaw runtime:** `2026.9.5 (ec9c1a1)`
- **Regression/dev dependency pin:** OpenClaw `2026.7.1-2`
- **Managed provider ownership:** Ollama
- **Cloud/provider/model/auth routing:** OpenClaw-owned pass-through
- **CNX-442 authoritative Stop + session FIFO:** final live GREEN
- **License:** MIT

The package peer range remains broader than the exact runtimes physically qualified by this repository. A peer range is install compatibility, not proof of behavioral acceptance.

See [docs/CURRENT_STATE.md](docs/CURRENT_STATE.md) for the authoritative operational state and [docs/operations/coordination/ACTIVE.md](docs/operations/coordination/ACTIVE.md) for the current development/release task.

> **Continuity invariant:** once eligible work is durably accepted, it must not silently disappear. It must eventually become delivered/completed, cancelled, or explicitly failed with durable evidence.

## Architecture

```text
User / Channel
      |
      v
Durable pre-dispatch Ticket admission
      |
      +--> same-session FIFO barrier for later accepted input
      |
      v
CogentNexus-OpenClaw Host authority
  - desired runtime state
  - session/generation ownership
  - deterministic supervision
  - cancellation / terminal fences
      |
      v
OpenClaw Gateway + selected provider/model
      |
      +--> DIRECT / LOOKUP / ACTION / STAGED
      |
      v
Response-ready commit
      |
      v
Durable result / delivery
      |
      v
Delivery confirmed -> completed
```

### Authoritative Stop behavior

For eligible owner input, later same-generation messages are durably accepted at `before_dispatch` but remain outside the native Host queue while an older Ticket is non-terminal. A valid user Stop advances the owner generation once, cancels the active and held Tickets, and consumes held cancelled ingress before Host queue admission. This prevents a cancelled queued message from becoming a successor Host run.

The final physical Discord acceptance on OpenClaw 2026.9.5 proved:

- generation advanced exactly once;
- active and held Tickets became `cancelled`;
- held Ticket remained `bound_run_id = NULL`;
- held Ticket performed zero model calls and zero inference attempts;
- no successor Host run was created;
- no new `blocked by cogentnexus-openclaw` error was emitted.

## Operating modes

- **MANAGED** — Ticket-first continuity and CNXCLAW lifecycle/recovery ownership are active.
- **PASSTHROUGH** — provider/model/auth remain OpenClaw-owned and CNX managed provider ownership is inactive.
- **MAINTENANCE** — deliberate stop state; durable state is preserved and recovery must not fight operator intent.

`disable` returns to native/pass-through behavior. `stop` preserves managed intent but deliberately stops managed runtime activity.

## Provider contract

OpenClaw owns Cloud authentication, routing, provider runtime lifecycle, and probing; CogentNexus-OpenClaw owns durable continuity/recovery evidence and managed Ollama health/lifecycle only.

CogentNexus-OpenClaw manages Ollama health/lifecycle/recovery when operating in managed local-provider mode. Cloud and other OpenClaw routes remain OpenClaw-owned: OpenClaw owns credentials, model selection, provider runtime, probing, and recovery. CogentNexus-OpenClaw preserves Ticket/session/generation continuity without copying or persisting Cloud credentials.

There is no silent fallback from an unavailable Ollama route to another provider.

See [docs/PROVIDERS.md](docs/PROVIDERS.md).

## Installation

Use an exact GitHub Release archive and verify `SHA256SUMS.txt`. A moving branch is not a release identity.

```powershell
python -m pip install "PyYAML>=6.0,<7"
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
.\scripts\install.ps1 -Workspace "$HOME\.openclaw\workspace"
```

See:

- [English install guide](docs/INSTALL.md)
- [คู่มือติดตั้งภาษาไทย](docs/INSTALL.th.md)
- [คู่มือคำสั่งภาษาไทย](docs/COMMANDS.th.md)
- [Clean reinstall](docs/CLEAN_REINSTALL.md)
- [ล้างและติดตั้งใหม่แบบสะอาด](docs/CLEAN_REINSTALL.th.md)

## Everyday control

```powershell
.\cnxclaw.cmd status
.\cnxclaw.cmd provider list
.\cnxclaw.cmd check system
.\cnxclaw.cmd start
.\cnxclaw.cmd stop
.\cnxclaw.cmd restart
.\cnxclaw.cmd gateway start
.\cnxclaw.cmd gateway stop
.\cnxclaw.cmd gateway restart
.\cnxclaw.cmd ticket list
.\cnxclaw.cmd ticket cancel <ticket-id>
.\cnxclaw.cmd session cancel <session-key>
.\cnxclaw.cmd disable
.\cnxclaw.cmd enable
.\cnxclaw.cmd reset
.\cnxclaw.cmd uninstall
```

Destructive `reset` and `uninstall` require explicit confirmation and remain ownership-bounded.

## Validation

```sh
python -m pip install -r requirements-dev.txt
python scripts/check_namespace_isolation.py
python scripts/check_baseline_consistency.py
python skills/cogentnexus-openclaw/scripts/validate.py --workspace-singleton
python skills/cogentnexus-openclaw/scripts/cogent.py self-test
python skills/cogentnexus-openclaw/scripts/runtime.py self-test
python skills/cogentnexus-openclaw/scripts/workflow.py self-test
python -m pytest -q

cd plugins/cogentnexus-openclaw
npm ci
npm test
npm run evaluation
npm audit --omit=dev
npm run plugin:validate
```

## Documentation and historical evidence

Current-facing guidance lives in this README, `docs/CURRENT_STATE.md`, installation/provider docs, and current coordination authority. Versioned release notes, completed coordination tasks/reports/reviews, and version-named acceptance files are historical evidence and are intentionally not rewritten to pretend they described a later state.

## License

CogentNexus-OpenClaw is licensed under the [MIT License](LICENSE).

Copyright (c) 2026 funggier.
