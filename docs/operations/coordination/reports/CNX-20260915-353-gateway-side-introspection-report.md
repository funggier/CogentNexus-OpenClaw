# CNX-353 — Gateway-Side Introspection Report

## Authority and ancestry

- Remote branch: `cnx-353-gateway-side-introspection`
- Starting verified HEAD: `858a8416407c3b5777419d21119f9f6a6210fadf`
- Parent baseline: `596a02f640e05f9e74c85778adc2fcb2b6db8d57`
- Baseline ancestry: verified with `git merge-base --is-ancestor`; exit `0`.
- Starting worktree: clean.

Preflight was run against the fetched remote ref:

```text
git remote -v
origin https://github.com/funggier/CogentNexus-OpenClaw.git (fetch)
origin https://github.com/funggier/CogentNexus-OpenClaw.git (push)

git rev-parse origin/cnx-353-gateway-side-introspection
858a8416407c3b5777419d21119f9f6a6210fadf

git merge-base --is-ancestor 596a02f640e05f9e74c85778adc2fcb2b6db8d57 origin/cnx-353-gateway-side-introspection
exit 0
```

## Gateway process identity

Read-only command: `openclaw gateway status`

```text
Gateway: bind=loopback (127.0.0.1), port=18789
Gateway version: 2026.7.1-2
Runtime: running (pid 17080, state Ready, Gateway process detected for gateway port 18789.)
Connectivity probe: ok
Listening: 127.0.0.1:18789
Command: C:\\Program Files\\nodejs\\node.exe C:\\Users\\CDQ-P\\AppData\\Roaming\\npm\\node_modules\\openclaw\\dist\\index.js gateway --port 18789
```

The PID is the Gateway PID reported by OpenClaw, not an inferred `node.exe` process. The available status output supplies PID, state, port, and command, but not JavaScript module cache identity, ESM registry identity, plugin-manager object identity, or hook-handler identity.

## Gateway-owned diagnostics and RPC inventory

Read-only commands inspected:

- `openclaw gateway probe`
- `openclaw gateway call health`
- `openclaw gateway call --help`
- `openclaw plugins list --json`
- `openclaw plugins inspect cogentnexus-openclaw --json --runtime`
- `openclaw plugins inspect --help`

### Gateway probe

Result:

```text
Reachable: yes
Capability: connected-no-operator-scope
Read-probe diagnostics are limited by gateway scopes (missing operator.read).
Connect: ok; Capability: connect-only; Read probe: limited - missing scope: operator.read
```

This establishes connection to the Gateway but also records the exact scope limitation. It does not expose plugin-local state.

### Gateway `health`

The Gateway-owned response returned:

```json
{
  "ok": true,
  "plugins": {
    "loaded": ["browser", "canvas", "codex", "cogentnexus-openclaw", "device-pair", "discord", "file-transfer", "memory-core", "ollama", "openai", "phone-control", "talk-voice"],
    "errors": []
  },
  "configReload": {"hotReloadStatus": "active"}
}
```

Classification: **A — Gateway response**, but only a coarse loaded-plugin/health report. It does not provide module identity, registration count/owner, effective hook registry, handler identity, or priority. `plugins.loaded` is therefore not process-scoped registration proof for D/E.

### Gateway method inventory

Exact `openclaw gateway call --help` output identified only:

```text
method  Method name (health/status/system-presence/cron.*)
```

No diagnostic, plugin-inspection, runtime-inspection, registration, hook-registry, or operator introspection method was documented. `gateway probe` reported `missing operator.read`; no scope was broadened or bypassed.

### Plugin list and runtime inspect

`openclaw plugins list --json` reports the persisted plugin registry and inventory. For CNX it reported source:

```text
C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw\dist\v091-release-entry.js
status=loaded
hookCount=0
```

`openclaw plugins inspect cogentnexus-openclaw --json --runtime` reported:

```text
activated=true
status=loaded
source=C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw\dist\v091-release-entry.js
hookCount=42
before_agent_run priority=2000
services include CNX services
```

The command's implementation/behavior is a CLI runtime inspection seam: it loads/inspects the plugin for the CLI inspection process. It provides no PID/process binding option, and its response contains no Gateway PID, module-cache identity, Gateway plugin-manager identity, or Gateway effective-registry owner. The two outputs are consequently not contradictory process evidence: list is persisted/inventory state, while `--runtime` is CLI-process runtime inspection. Neither proves the effective hook registry in PID `17080`.

## Source/plugin-manager seams inspected

Read from the starting remote checkout:

- `plugins/cogentnexus-openclaw/src/v091-release-entry.ts`
- `plugins/cogentnexus-openclaw/src/v091-final-entry.ts`
- `plugins/cogentnexus-openclaw/src/v090-final-entry.ts`
- `plugins/cogentnexus-openclaw/src/index.ts`

Findings:

- `v091-release-entry.ts` obtains the legacy `register` function and invokes `register(runtimeApi)`.
- The legacy registration return type is `void | Promise<void>`.
- `v091-release-entry.ts` calls `installManagedRuntimeGuards()` immediately for synchronous registration and via `Promise.resolve(registered).then(...)` for an asynchronous registration result.
- `v091-final-entry.ts` proxies `registerService` and returns the wrapped registration result.
- `v090-final-entry.ts` proxies registration/service calls but exposes no persistent process-scoped registration record.
- `index.ts` registers `before_agent_run` at priority `2000` when `preInferenceAdmission !== false`, alongside other hooks and services.

No source seam in the repository exposes the Gateway's internal plugin manager, loaded module cache, registration owner, registration event/counter, or effective hook registry through a read-only Gateway API. The source proves call sites only; it is not evidence that the call occurred in PID `17080`.

## Process-scoped observations

| Observation | Result | Process-scoped? |
|---|---|---|
| Gateway PID | `17080`, Ready, port `18789` | Yes, from Gateway status identity; no plugin state attached |
| Gateway health | CNX appears in `plugins.loaded`; no errors | Gateway-owned, but coarse only |
| Actual loaded CNX JS module identity/cache | Not exposed | No |
| `releaseEntry.register()` entered | Not exposed | No |
| Legacy `register(runtimeApi)` invoked/returned | Not exposed | No |
| Promise pending/resolved | Not exposed | No |
| `installManagedRuntimeGuards` completed | Not exposed | No |
| Gateway plugin-manager instance | Not exposed | No |
| Gateway effective `before_agent_run` registry | Not exposed | No |
| Gateway handler identity/owner/priority | Not exposed | No |

## Registration and hook observations

The CLI runtime inspection reported `hookCount=42` and a `before_agent_run` entry with priority `2000`. This is useful CLI-process observation only. The persisted list reported `hookCount=0`, which is inventory data and is not treated as proof of an empty Gateway registry. No observation binds either result to PID `17080`.

No Dashboard/WebChat/provider execution was performed, so there is no process-scoped evidence of a provider execution path with or without `before_agent_run`.

## Async registration boundary

The investigated production pattern is:

```ts
const registered = register(runtimeApi);
if (registered && typeof (registered as Promise<void>).then === "function") {
  return Promise.resolve(registered).then(installManagedRuntimeGuards);
}
installManagedRuntimeGuards();
```

Static source establishes the synchronous and Promise-returning paths. No Gateway lifecycle diagnostic reports register entry, return/pending state, Promise resolution, or guard-install completion. The code was not changed and no asynchronous registration was initiated by this investigation.

## Test result

Read-only focused test command:

```text
npm test -- --run src/cnx348-effective-runtime-provenance.test.ts
```

Exact result:

```text
npm notice run openclaw-plugin-cogentnexus-openclaw@0.9.5 test
npm notice run vitest run --config ./vitest.config.ts --run src/cnx348-effective-runtime-provenance.test.ts
'vitest' is not recognized as an internal or external command,
operable program or batch file.
exit 1
```

This is an environment/dependency limitation (`vitest` is unavailable in the existing checkout), not evidence of a runtime defect. Dependencies were not installed because installation would exceed the read-only investigation scope.

## Classification

**UNRESOLVED / BLOCKED — no trustworthy process-scoped Gateway introspection boundary found.**

- **D PROVEN:** No. There is no Gateway-side exact mismatch between the loaded CNX module and the expected module.
- **E PROVEN:** No. No provider execution was performed and no Gateway-side evidence shows Dashboard/WebChat execution without `before_agent_run`.
- **OBSERVABILITY BOUNDARY FOUND:** No qualifying registration/hook introspection boundary. `gateway call health` is a Gateway-owned coarse health seam, but it cannot attribute registration state beyond the broad `plugins.loaded` list.

## Production changes and hard-fence verification

Production source, build output, installed plugin, runtime/configuration, database, provider routing, UI, and Gateway process were not changed. No plugin install/reinstall, Gateway restart/stop/start, provider call, semantic request, Dashboard/WebChat interaction, replay/resend, runtime/config/database mutation, admission/timeout change, v0.9.5 history/tag mutation, force-push, or self-acceptance was performed.

Only this documentation report is added.

## Smallest next probe

Obtain separately authorized read-only `operator.read` access, if supported by the deployment, and test the documented Gateway methods without mutating state. If no method then exposes process-local plugin state, the smallest useful future OpenClaw-owned seam is an operator-scoped Gateway diagnostic RPC that returns, for the existing Gateway PID:

1. loaded CNX module URL and module/cache identity;
2. plugin-manager instance/owner and registration entry/completion state;
3. effective `before_agent_run` handler identity, owner, priority, and registry membership.

The response must be correlated with the PID from `openclaw gateway status`; it must not restart, mutate, invoke a provider, or alter registration behavior.

## Closeout fields

- Final GitHub HEAD: `25c37244ad5589e6422d2e0b809373907d9ec148` (verified from `origin/cnx-353-gateway-side-introspection`).
- Report blob: `065c737316b5039996f42b5646f3405f98ef815f` (verified from the remote tree at the final tip).
- Changed paths: `A docs/operations/coordination/reports/CNX-20260915-353-gateway-side-introspection-report.md` only.
