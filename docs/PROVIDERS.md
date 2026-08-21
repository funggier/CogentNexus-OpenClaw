# Provider lifecycle — CogentNexus v0.9.2

CogentNexus v0.9.2 separates durable user intent/recovery authority from the concrete local inference runtime. The accepted v0.9.1 Ticket, Direct Recovery, durable-result and delivery fences remain authoritative. The v0.9.2 provider layer owns discovery, selected-provider lifecycle, the narrow OpenClaw route/timeout compatibility transaction required by that provider, and bounded provider recovery.

## Supported local providers

| Provider | Default endpoint | OpenClaw route prefix | Control adapter |
| --- | --- | --- | --- |
| Ollama | `http://127.0.0.1:11434` | `ollama/...` | `ollama` CLI |
| LM Studio | `http://127.0.0.1:1234` | `lmstudio_local/...` | `lms` CLI |

Both applications may be installed and their servers may even be running at the same time because their normal ports are different. CogentNexus has exactly one **selected provider** for managed lifecycle/recovery responsibility.

## Selecting a provider

```powershell
.\cnx.cmd start --provider ollama
.\cnx.cmd start --provider lmstudio
```

An explicit provider and its OpenClaw route are validated before lifecycle mutation. On success the Host stores:

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

## Provider + OpenClaw route transaction

Switching providers is transactional. CogentNexus does **not** rewrite arbitrary OpenClaw configuration. While MANAGED it owns only the fields required to make the selected local route safe and usable:

1. the default model route for the selected provider;
2. local-provider timeout ordering;
3. LM Studio llama.cpp tool-schema compatibility keywords proven necessary by live testing.

Before lifecycle mutation, CogentNexus performs provider and route preflight. Once action begins it writes a durable `providerTransition` marker containing `from`, `to`, source and start time and creates a short-lived rollback copy of the pre-transition OpenClaw config.

The new `selectedProvider` is committed only after:

1. the requested provider is available/startable;
2. the OpenClaw route transaction validates;
3. the managed Host/Gateway transition succeeds;
4. provider readiness still succeeds after the transition;
5. Gateway health verification succeeds;
6. the active OpenClaw model route resolves to the selected provider;
7. the route transaction commits.

If the Host transition or verification fails, the OpenClaw route is rolled back while the durable `providerTransition` marker remains. A later `start` therefore resumes the same intended provider rather than guessing or silently falling back.

## Route discovery

CogentNexus does not invent credentials or an unknown model. A provider route must already be resolvable from at least one of:

- the current OpenClaw default route;
- a previously verified CogentNexus route for that provider;
- an existing model entry in the provider's OpenClaw catalog;
- `CNX_OLLAMA_MODEL` or `CNX_LMSTUDIO_MODEL`.

For LM Studio, an existing `models.providers.lmstudio_local` configuration is required. This keeps API endpoint/auth/model ownership explicit.

## LM Studio compatibility profile

Live Windows testing with OpenClaw `2026.7.1-2`, LM Studio and Qwen3.5:9B proved two independent compatibility boundaries.

### llama.cpp tool schema

LM Studio's llama.cpp grammar path rejects some OpenClaw tool-schema keywords unless they are stripped. The verified compatibility profile is:

```json
{
  "unsupportedToolSchemaKeywords": [
    "pattern",
    "maxLength"
  ]
}
```

This profile passed isolated `cron`, isolated `image_generate`, combined `cron + image_generate`, and the full OpenClaw `coding` tool surface.

### Timeout ordering

OpenAI-compatible streaming does not expose LM Studio prompt-prefill progress to OpenClaw. A valid cold request can therefore remain silent for several minutes even while llama.cpp is actively processing the prompt.

CogentNexus v0.9.2 applies an LM Studio timeout envelope in which the inner provider request expires before the outer liveness/agent boundaries. The current verified profile is:

```text
provider timeout             = 1100 s
stuck-session abort          = 1140 s
agent timeout                = 1200 s
```

The invariant is more important than the exact numbers:

```text
provider timeout < stuck-session abort < agent timeout
```

`disable`, `reset` and `uninstall` restore the pre-CogentNexus values rather than leaving this profile behind.

## No silent fallback

CogentNexus never silently chooses a different provider because a requested provider is missing, unhealthy, or missing a model route.

If a persisted provider is later uninstalled or its route is no longer resolvable, `cnx start` fails closed. Choose another provider explicitly.

## Fresh state and reset

On a fresh CNX state:

- exactly one installed supported provider -> it may be used without an explicit flag;
- both providers installed -> explicit provider selection is required;
- neither installed -> managed provider start is refused.

`stop` preserves the selected provider and MANAGED route. `disable` preserves the durable provider preference but restores native OpenClaw route/timeout/compat fields. A later `enable/start` reapplies the selected provider transactionally.

`reset` means fresh-install semantics. It intentionally does not preserve the old provider preference. If both providers are installed, specify the fresh provider explicitly:

```powershell
.\cnx.cmd reset --provider ollama
# or
.\cnx.cmd reset --provider lmstudio
```

The destructive `y` confirmation and v0.9.1 PASSTHROUGH-first reset safety boundary remain intact. Before CNX state is removed, OpenClaw's pre-CNX managed fields are restored.

## LM Studio control

LM Studio control requires its `lms` CLI for CogentNexus-managed start/stop. A desktop LM Studio installation without the CLI is detectable but is reported as not controllable.

If LM Studio API authentication is enabled, `LM_API_TOKEN` may be supplied to the CogentNexus process for readiness probes.

## Recovery boundary

The provider adapter does not decide whether an inference may be repeated. That authority remains in the Recovery Core plus the v0.9.2 evidence-aware provider guard:

- deterministic provider protocol/schema/grammar failure -> non-retryable; do not restart provider;
- healthy LM Studio + healthy Gateway + first expired silent Direct call -> classify `cold_model_long_running`, extend the durable call deadline once, and do not restart provider;
- no durable result + second eligible expiry -> accepted Direct recovery path may run if the provider recovery circuit is open for recovery;
- durable result already exists -> provider restart must not regenerate; delivery owns retry;
- possible external side effect -> receipt/idempotency verification is required before any repeated action.

Automatic provider recovery is bounded durably. The current LM Studio policy allows at most two automatic recoveries in the rolling hour and uses a 15-minute cooldown/circuit guard. A verified manual provider transition starts a fresh automatic-recovery budget.

During a Host-authorized Direct model-call recovery, Gateway is quiesced before the selected local provider is stopped. Classification occurs only while the inference-capable runtime is quiescent, preserving the accepted v0.9.1 ordering.
