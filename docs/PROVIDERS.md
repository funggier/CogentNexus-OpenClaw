# Provider lifecycle — CogentNexus-OpenClaw v0.9.3

CogentNexus-OpenClaw v0.9.3 has one current managed provider: **Ollama only**.

The accepted Recovery Core remains responsible for Ticket, recovery-authority, durable-result, and delivery fences. The v0.9.3 provider facade narrows operator-facing provider selection to Ollama while retaining older v0.9.2 compatibility modules in-tree where migration/native restoration requires them.

## Current managed provider

| Provider | Default endpoint | OpenClaw route prefix | v0.9.3 status |
| --- | --- | --- | --- |
| Ollama | `http://127.0.0.1:11434` | `ollama/...` | Supported / managed |

Current lifecycle examples:

```powershell
.\cnxclaw.cmd start
.\cnxclaw.cmd start --provider ollama
.\cnxclaw.cmd restart
.\cnxclaw.cmd restart --provider ollama
```

Provider-bearing v0.9.3 lifecycle operations normalize to Ollama. Unsupported provider names fail closed rather than falling back silently.

## Provider + OpenClaw route boundary

CogentNexus-OpenClaw does not rewrite arbitrary OpenClaw configuration. Managed route/configuration mutation must remain limited to the fields required for the current Ollama lifecycle and the accepted recovery/compatibility contract.

Before lifecycle mutation, the system performs read-only preflight. A successful managed transition must verify Ollama and Gateway readiness before committing the managed target.

## Native/PASSTHROUGH boundary

`disable` is a runtime boundary, not merely a configuration edit. Native OpenClaw must remain usable when CogentNexus-OpenClaw is disabled or uninstalled.

`reset` and `uninstall` reuse the supported PASSTHROUGH/native boundary and must fail closed before destructive cleanup if native OpenClaw cannot be restored/verified safely.

## Route discovery

v0.9.3 does not invent credentials or an unknown model. The managed route must resolve to Ollama from the current/verified OpenClaw model configuration and supported local model evidence.

A non-Ollama model route is outside the current v0.9.3 managed-provider contract.

## Recovery authority

Elapsed time alone does not authorize provider recovery.

```text
provider/Gateway healthy + silent active call
    -> no destructive recovery without stronger evidence

provider failure evidence + eligible Direct call
    -> bounded recovery authority

successful model completion
    -> durable success evidence
```

Once a durable result exists, delivery uncertainty is not permission to regenerate inference.

## No silent fallback

If Ollama is unavailable, unhealthy, uncontrollable, or lacks a usable model route, `cnxclaw start` must fail closed. v0.9.3 does not silently select another provider.

## Fresh state and reset

Fresh v0.9.3 managed state targets Ollama.

```powershell
.\cnxclaw.cmd reset
.\cnxclaw.cmd reset --provider ollama
```

The explicit-`y`, ownership-safe, PASSTHROUGH-first destructive boundary remains required.

## Historical v0.9.2 note

v0.9.2 was a provider-neutral development/release line that included LM Studio lifecycle and compatibility work. Its source modules, release notes, and historical evidence may preserve those facts because they are part of repository history.

That historical implementation must not be interpreted as a current v0.9.3 operator-facing provider promise. Current v0.9.3 source exposes Ollama only.

## Recovery Core boundary

The provider layer never decides that a committed result or possible external side effect may be repeated. Accepted recovery fences remain authoritative:

- deterministic protocol failure -> classify/fail according to evidence;
- durable exact result exists -> delivery retry only;
- ambiguous visible response without durable payload -> fail closed;
- possible external side effect -> receipt/idempotency proof required;
- Host-authorized Direct recovery -> runtime quiescence and durable result fences remain mandatory.
