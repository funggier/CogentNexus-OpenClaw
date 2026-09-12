**Current v0.9.5 release candidate:** pre-publication validation in progress.

# Provider lifecycle — CogentNexus-OpenClaw v0.9.4

CogentNexus-OpenClaw v0.9.4 (currently unreleased) has a managed Ollama mode and an OpenClaw-owned Cloud pass-through mode.

The accepted Recovery Core remains responsible for Ticket, session/generation, durable-result, and delivery fences. Managed provider selection remains Ollama-only: CogentNexus-OpenClaw owns Ollama health, lifecycle, and recovery. Cloud routes are OpenClaw-owned pass-through. OpenClaw owns their authentication, routing/model selection, runtime, lifecycle, probing, and recovery. CogentNexus-OpenClaw never reads, copies, persists, refreshes, or logs Cloud credentials and never starts, stops, probes, or recovers a Cloud provider.

## Current managed provider

| Provider | Default endpoint | OpenClaw route prefix | v0.9.4 status |
| --- | --- | --- | --- |
| Ollama | `http://127.0.0.1:11434` | `ollama/...` | Supported / managed |

Current lifecycle examples:

```powershell
.\cnxclaw.cmd start
.\cnxclaw.cmd start --provider ollama
.\cnxclaw.cmd restart
.\cnxclaw.cmd restart --provider ollama
```

Provider-bearing v0.9.4 lifecycle operations normalize to Ollama. Unsupported provider names fail closed rather than falling back silently.

## Provider + OpenClaw route boundary

CogentNexus-OpenClaw does not rewrite arbitrary OpenClaw configuration. Managed route/configuration mutation must remain limited to the fields required for the current Ollama lifecycle and the accepted recovery/compatibility contract.

Before lifecycle mutation, the system performs read-only preflight. A successful managed transition must verify Ollama and Gateway readiness before committing the managed target.

## Native/PASSTHROUGH boundary

`cnxclaw cloud` is the supported non-destructive transition into Cloud-capable pass-through. It accepts no provider, model, or credential arguments. The command first restores OpenClaw's native route, removes the managed `AGENTS.md` policy block, disables supervisor startup, commits Host `mode=passthrough`, `desiredGateway=running`, and `desiredProvider=unchanged`, keeps the CogentNexus-OpenClaw plugin enabled in passive mode, and restarts the Gateway once so continuity hooks load. It never starts, stops, probes, or recovers Ollama or the Cloud provider. After this transition succeeds, the operator selects the Cloud route with OpenClaw-owned configuration such as `openclaw models set <provider/model>`; running that selection before `cnxclaw cloud` is not authoritative because native-route restoration may replace it.

```powershell
.\cnxclaw.cmd cloud
```

`disable` is a runtime boundary, not merely a configuration edit. Unlike `cloud`, it disables the plugin; its existing semantics are unchanged. Native OpenClaw must remain usable when CogentNexus-OpenClaw is disabled or uninstalled.

`reset` and `uninstall` reuse the supported PASSTHROUGH/native boundary and must fail closed before destructive cleanup if native OpenClaw cannot be restored/verified safely.

## Route discovery

v0.9.4 does not invent credentials or an unknown model. The managed route must resolve to Ollama from the current/verified OpenClaw model configuration and supported local model evidence.

A non-Ollama model route is outside the managed-provider contract, but may be used through OpenClaw-owned Cloud pass-through when configured in OpenClaw. Provider/model failure stays an OpenClaw model-call outcome: it does not authorize Ollama recovery or implicit fallback.

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

If Ollama is unavailable, unhealthy, uncontrollable, or lacks a usable model route, `cnxclaw start` must fail closed. v0.9.4 does not silently select another provider.

## Fresh state and reset

Fresh v0.9.4 managed state targets Ollama.

```powershell
.\cnxclaw.cmd reset
.\cnxclaw.cmd reset --provider ollama
```

The explicit-`y`, ownership-safe, PASSTHROUGH-first destructive boundary remains required.

## Historical v0.9.2 note

v0.9.2 was a provider-neutral development/release line that included LM Studio lifecycle and compatibility work. Its source modules, release notes, and historical evidence may preserve those facts because they are part of repository history.

That historical implementation must not be interpreted as a current v0.9.4 managed-provider promise. Current v0.9.4 source manages Ollama only and separately supports OpenClaw-owned Cloud pass-through without taking ownership of Cloud credentials, lifecycle, probing, or recovery.

## Recovery Core boundary

The provider layer never decides that a committed result or possible external side effect may be repeated. Accepted recovery fences remain authoritative:

- deterministic protocol failure -> classify/fail according to evidence;
- durable exact result exists -> delivery retry only;
- ambiguous visible response without durable payload -> fail closed;
- possible external side effect -> receipt/idempotency proof required;
- Host-authorized Direct recovery -> runtime quiescence and durable result fences remain mandatory.
