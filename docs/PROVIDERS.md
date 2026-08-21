# Provider lifecycle — CogentNexus v0.9.2

CogentNexus v0.9.2 separates durable user intent/recovery authority from the concrete local inference runtime. The accepted v0.9.1 Ticket, Direct Recovery, durable-result and delivery fences remain authoritative; the provider layer only owns discovery, start/stop/readiness and which local provider the Host supervises.

## Supported local providers

| Provider | Default endpoint | Control adapter |
| --- | --- | --- |
| Ollama | `http://127.0.0.1:11434` | `ollama` CLI |
| LM Studio | `http://127.0.0.1:1234` | `lms` CLI |

Both applications may be installed and their servers may even be running at the same time because their normal ports are different. CogentNexus has exactly one **selected provider** for managed lifecycle/recovery responsibility.

## Selecting a provider

```powershell
.\cnx.cmd start --provider ollama
.\cnx.cmd start --provider lmstudio
```

An explicit provider is validated before the new selection is committed. On success the Host stores:

- `selectedProvider` — last successfully selected provider;
- `providerSelection.selectedAt`;
- `providerSelection.selectionSource`;
- `providerSelection.lastVerifiedAt`.

Later commands may omit `--provider`:

```powershell
.\cnx.cmd start
.\cnx.cmd restart
```

They reuse the last successfully selected provider.

## Provider transition fence

Switching providers is transactional. Before mutation CogentNexus performs provider preflight. Once action begins it writes a durable `providerTransition` marker containing `from`, `to`, source and start time.

The new `selectedProvider` is committed only after:

1. the requested provider is available/startable;
2. provider readiness succeeds;
3. the managed Host/Gateway transition succeeds;
4. provider readiness still succeeds after the transition;
5. Gateway health verification succeeds.

If the process or machine dies after the transition marker but before selection commit, the next `start` resumes the same transition target instead of silently falling back to another provider.

## No silent fallback

CogentNexus never silently chooses a different provider because a requested provider is missing or unhealthy.

If a persisted provider is later uninstalled, `cnx start` refuses to commit another provider automatically. Use an explicit command instead:

```powershell
.\cnx.cmd start --provider ollama
```

## Fresh state and reset

On a fresh CNX state:

- exactly one installed supported provider -> it may be used without an explicit flag;
- both providers installed -> explicit provider selection is required;
- neither installed -> managed provider start is refused.

`stop`, `disable`, restart and reboot preserve the selected provider.

`reset` means fresh-install semantics. It intentionally does not preserve the old provider preference. If both providers are installed, specify the fresh provider explicitly:

```powershell
.\cnx.cmd reset --provider ollama
# or
.\cnx.cmd reset --provider lmstudio
```

The destructive `y` confirmation and v0.9.1 PASSTHROUGH-first reset safety boundary remain intact.

## LM Studio specifics

LM Studio control requires its `lms` CLI for CogentNexus-managed start/stop. A desktop LM Studio installation without the CLI is detectable but is reported as not controllable.

OpenClaw model routing remains OpenClaw configuration. CogentNexus provider selection does not silently rewrite the user's model selection. Use OpenClaw's LM Studio setup/model commands to configure the desired LM Studio model route, then use CNX provider lifecycle to supervise that local backend.

If LM Studio API authentication is enabled, `LM_API_TOKEN` may be supplied to the CogentNexus process for readiness probes.

## Recovery boundary

The provider adapter does not decide whether an inference may be repeated. That authority remains in the accepted Recovery Core:

- no durable result + eligible stalled call -> bounded recovery may be authorized;
- durable result already exists -> provider restart must not regenerate; delivery owns retry;
- possible external side effect -> receipt/idempotency verification is required before any repeated action.

During a Host-authorized Direct model-call recovery, Gateway is quiesced before the selected local provider is stopped. Classification occurs only while the inference-capable runtime is quiescent, preserving the accepted v0.9.1 ordering.
