# CNX-20260918-408 — Live Hook Runner Runtime Attestation Surface Report

## Classification

`RUNTIME_ATTESTATION_IMPLEMENTED_PENDING_LIVE_QUALIFICATION`

A read-only operator-scoped Gateway runtime-attestation surface has been implemented in repository source.

No production deploy, Gateway restart, provider/model mutation, semantic request, or live RPC invocation occurred in this task.

## Authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Parent: `CNX-20260918-407`
- Architecture disposition: `BEFORE_AGENT_RUN_RETAINED_WITH_RUNTIME_ATTESTATION_NEXT`
- Exact OpenClaw runtime/source identity used for SDK validation: `2026.7.1-2 (0790d9f593ad30c940ed93b5872a8cf6d6f3cf8c)`

## TDD sequence

### RED

Commit:

`a1b38dfcbe961cbbb38da3e44342630176ba954d`

Added:

`plugins/cogentnexus-openclaw/src/v095-runtime-hook-attestation.test.ts`

The test intentionally imported the not-yet-existing attestation module and defined the required contract:

- conservative classification;
- `operator.read` Gateway RPC;
- no false-positive `PRESENT` when only a non-CogentNexus/global hook is known.

This is a deterministic source RED boundary because the imported module did not yet exist.

### Implementation

Commit:

`6567d1fac5ea0633fb7f5839456ea58a3e7147ca`

Added:

`plugins/cogentnexus-openclaw/src/v095-runtime-hook-attestation.ts`

The module uses public OpenClaw SDK exports:

```text
openclaw/plugin-sdk/plugin-runtime
  -> getGlobalHookRunner()
  -> getGlobalPluginRegistry()
```

and exposes:

`cogentnexus.runtimeAttestation`

through the plugin Gateway API with:

`scope: "operator.read"`

### Release-entry wiring

Commit:

`4576f8c92965957a246578f55fc6920e5af3bb59`

Updated:

`plugins/cogentnexus-openclaw/src/v091-release-entry.ts`

The attestation RPC is registered only after normal Host authority has accepted runtime registration.

The same change also corrected the outdated CNX-374 source comment. Later CNX-385/CNX-391 evidence established that the authoritative non-bundled conversation-hook policy input is normalized runtime configuration:

`plugins.entries.<id>.hooks.allowConversationAccess`

rather than treating the executable-definition field as proof of host acceptance.

The executable-definition field remains for compatibility/documentation and was not removed in this task.

## Attestation contract

Returned snapshot:

- `schemaVersion`
- `pluginId`
- `hookName`
- `runnerReady`
- `globalHookCount`
- `latestRegistryPluginHookCount`
- `classification`

Target:

`before_agent_run`

Classifications:

### `RUNNER_UNAVAILABLE`

No global hook runner exists.

### `ABSENT`

Global runner exists but its total `before_agent_run` hook count is zero.

This is sufficient negative evidence that no plugin currently contributes that hook to the composed runner.

### `PRESENT`

Global runner count is positive and the most recently initialized registry explicitly contains at least one:

```text
pluginId = cogentnexus-openclaw
hookName = before_agent_run
```

This is sufficient positive evidence because the latest registry is a source of the composed hook runner.

### `AMBIGUOUS`

The global runner contains `before_agent_run`, but the latest registry does not establish CogentNexus ownership.

This state intentionally does not infer absence because OpenClaw 2026.7.1-2 composes hooks from multiple live registries.

## Why this closes a major observability gap

Earlier production work had to infer live hook state from:

- plugin-side registration logs;
- persisted plugin inventory;
- loader/cache source;
- process chronology.

CNX-394/CNX-395 proved that `plugins list --json` hook-count fields are not authoritative live registry evidence.

The new Gateway method executes in the Gateway process and asks the public runtime hook surfaces directly.

It therefore gives a pre-semantic decision point:

```text
attestation PRESENT
    -> live semantic admission qualification is worth running

attestation ABSENT
    -> do not waste a model/provider request; diagnose activation first

attestation AMBIGUOUS
    -> gather one narrower registry identity observation before semantic traffic

runner unavailable
    -> plugin/runtime activation is not ready for semantic qualification
```

## Safety properties

The attestation path:

- does not call `runBeforeAgentRun`;
- does not invoke any hook handler;
- does not register/re-register hooks;
- does not mutate the registry;
- does not read credentials;
- does not inspect provider configuration;
- does not mutate TicketStore;
- does not route provider/model selection;
- does not send model traffic.

It is observation-only.

## Exact OpenClaw SDK evidence

OpenClaw source identity:

`0790d9f593ad30c940ed93b5872a8cf6d6f3cf8c`

The package export map exposes:

- `openclaw/plugin-sdk/plugin-runtime`

The runtime barrel publicly re-exports:

- `getGlobalHookRunner`
- `getGlobalPluginRegistry`

The exact global hook runner:

- keeps a stable runner;
- uses a live composed registry facade;
- exposes `hasHooks` / `getHookCount`;
- documents that the most recently initialized registry is one composition source.

The exact plugin API supports:

`registerGatewayMethod(method, handler, { scope })`

including `operator.read`.

## Validation status

No GitHub Actions workflow run was associated with commit:

`4576f8c92965957a246578f55fc6920e5af3bb59`

and no pull request is currently associated with the working branch.

Therefore this report does **not** claim:

- TypeScript build GREEN;
- focused Vitest GREEN;
- `plugin:validate` GREEN;
- packaged artifact GREEN;
- live Gateway RPC availability.

Those are delegated to the next bounded local validation task.

## Hard-fence accounting

- Production deploy/install-over: 0
- Gateway restart/reload: 0
- Live Gateway RPC calls: 0
- Semantic/model/provider requests: 0
- Provider/model/auth/config mutation: 0
- TicketStore mutation: 0
- OpenClaw patch: 0
- Release/tag/main: 0
- Force push/history rewrite: 0

## Next bounded step

Run exact local source validation on the operator's machine without production deployment:

1. focused attestation test;
2. plugin TypeScript build;
3. plugin validation/package checks;
4. focused regression tests around release-entry wiring/model-selection/provider independence;
5. inspect the built artifact for the new RPC;
6. publish exact evidence.

Only after that passes should a separately authorized task install/deploy the candidate and query the read-only Gateway RPC.

## Final classification

`RUNTIME_ATTESTATION_IMPLEMENTED_PENDING_LIVE_QUALIFICATION`
