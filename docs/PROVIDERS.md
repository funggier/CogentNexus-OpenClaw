# Provider Lifecycle — CogentNexus-OpenClaw v0.9.8

CogentNexus-OpenClaw separates **continuity ownership** from **provider/model/auth ownership**.

## Current boundary

OpenClaw owns Cloud authentication, routing, provider runtime lifecycle, and probing; CogentNexus-OpenClaw owns durable continuity/recovery evidence and managed Ollama health/lifecycle only.

| Concern | Authority |
| --- | --- |
| Ticket/session/generation continuity | CogentNexus-OpenClaw |
| Durable result/delivery fences | CogentNexus-OpenClaw |
| Managed local-provider lifecycle | Ollama only |
| Cloud credentials/auth refresh | OpenClaw |
| Cloud provider/model selection | OpenClaw |
| Cloud provider lifecycle/probing/recovery | OpenClaw |

The managed provider contract does not silently fall back from Ollama to another provider.

## OpenClaw compatibility facts

Two facts are intentionally separate:

- regression/dev dependency pin: OpenClaw `2026.7.1-2`;
- latest physical runtime acceptance: OpenClaw `2026.9.5 (ec9c1a1)`.

The peer dependency range is an install-compatibility declaration. It does not prove every behavior against every version in that range.

## Managed Ollama mode

Default endpoint:

`http://127.0.0.1:11434`

Typical lifecycle:

```powershell
.\cnxclaw.cmd start
.\cnxclaw.cmd restart
.\cnxclaw.cmd check provider
```

Provider/model selection itself remains an OpenClaw routing concern. Legacy `--provider` input that implied CNX provider-routing authority is not part of the current v0.9.8 contract.

If Ollama is unavailable, unhealthy, or has no usable selected route, managed startup must fail closed rather than choose another provider implicitly.

## OpenClaw-owned pass-through

Use native/pass-through operation when OpenClaw should own the selected Cloud or other route. CogentNexus-OpenClaw keeps continuity boundaries without taking possession of Cloud credentials.

The supported boundary must preserve:

- native OpenClaw model routing;
- credentials outside CNX durable state;
- no implicit provider fallback;
- no CNX start/stop/probe of a Cloud provider;
- Ticket/session/generation continuity where the plugin remains active.

## Recovery authority

Elapsed time alone is not provider-failure evidence.

```text
provider/Gateway healthy + silent active call
    -> do not destructively recover from elapsed time alone

eligible interruption/failure evidence + no durable result
    -> bounded recovery may be authorized

durable result exists
    -> delivery retry only; do not regenerate inference
```

The original provider/model provenance remains part of recovery fencing.

## Stop and queued-input boundary

Provider ownership does not override session Stop authority. The v0.9.8 pre-dispatch FIFO barrier prevents a cancelled held message from reaching the Host queue after a user Stop, regardless of provider.

## Fresh state/reset

Fresh managed state targets the provider-neutral CNX controller with managed local-provider support for Ollama. `reset` and `uninstall` remain ownership-bounded and must restore/verify the native OpenClaw boundary before destructive cleanup.

## Historical provider work

LM Studio and older provider-neutral experiments remain in historical source/docs where needed for migration or evidence. They are not a current managed-provider promise.

See:

- [CURRENT_STATE.md](CURRENT_STATE.md)
- [BASELINE.md](BASELINE.md)
- [INSTALL.md](INSTALL.md)
