# CNX-352 — Runtime Registration Observation Boundary Report

Remote branch: `cnx-352-runtime-registration-observation-boundary`
Starting verified HEAD: `eab276e9c5c94583174f8af340a6b0bce2360a9b`
Parent baseline: `b4552f48fd733814afdf0523234103a158f7ac82`
Final GitHub HEAD: verified independently at closeout as the remote branch tip; the exact SHA is recorded in the final verification output below. This report was read back from that remote tip.

## Ancestry verification

The required preflight was executed against the fetched remote ref:

```text
git remote -v
origin https://github.com/funggier/CogentNexus-OpenClaw.git (fetch)
origin https://github.com/funggier/CogentNexus-OpenClaw.git (push)

git fetch origin

git rev-parse origin/cnx-352-runtime-registration-observation-boundary
eab276e9c5c94583174f8af340a6b0bce2360a9b

git merge-base --is-ancestor b4552f48fd733814afdf0523234103a158f7ac82 origin/cnx-352-runtime-registration-observation-boundary
true
```

The worktree was clean at start. No local branch was used as authority.

## Source seams inspected

Read from the starting remote checkout:

- `plugins/cogentnexus-openclaw/src/v091-release-entry.ts`
- `plugins/cogentnexus-openclaw/src/v091-final-entry.ts`
- `plugins/cogentnexus-openclaw/src/v090-final-entry.ts`
- `plugins/cogentnexus-openclaw/src/index.ts`
- existing test-only diagnostics in `src/cnx347-registration-boundary.test.ts` and `src/cnx348-effective-runtime-provenance.test.ts`

Static findings:

- `v091-release-entry.ts` calls the legacy `register(runtimeApi)` at A/B boundary, then calls `installV097DirectRecoveryStartupLiveness`, and either immediately calls `installManagedRuntimeGuards()` or returns `Promise.resolve(registered).then(installManagedRuntimeGuards)`.
- The legacy type explicitly permits `void | Promise<void>`, so a Promise-returning registration is supported by the seam.
- `v091-final-entry.ts` wraps the v0.9.0 entry and proxies `registerService`; it returns the legacy registration result.
- `v090-final-entry.ts` wraps the v0.9.0 entry, installs registration/service proxies, and does not expose a persistent process-scoped registration record.
- `index.ts` registers `before_agent_run` at priority `2000` when `preInferenceAdmission !== false`; it also registers multiple other hooks and services.
- Existing `cnx348-effective-runtime-provenance.test.ts` observes module URL, registration invocation, synthetic hook identity, and a synthetic effective registry only through a test loader. It is not evidence from the running Gateway.

Static source evidence is not process-scoped runtime evidence.

## OpenClaw runtime seams inspected

Exact read-only commands:

```text
openclaw --version
OpenClaw 2026.7.1-2 (0790d9f)

openclaw gateway status
Service: Scheduled Task (registered)
Command: C:\\Program Files\\nodejs\\node.exe C:\\Users\\CDQ-P\\AppData\\Roaming\\npm\\node_modules\\openclaw\\dist\\index.js gateway --port 18789
Runtime: running (pid 17080, state Ready)
Connectivity probe: ok
Listening: 127.0.0.1:18789

openclaw gateway probe
Reachable: yes
Capability: connected-no-operator-scope
Read probe: limited - missing scope: operator.read

openclaw gateway call health
ok=true; plugins.loaded includes cogentnexus-openclaw; errors=[]

openclaw gateway stability
Events include diagnostic.phase.completed, diagnostic.heartbeat, diagnostic.memory.sample, session.state, queue events, and message dispatch events. No registration boundary, module identity, or effective hook registry is exposed.

openclaw plugins list --json
cogentnexus-openclaw: status=loaded, source=C:\\Users\\CDQ-P\\.openclaw\\extensions\\cogentnexus-openclaw\\dist\\v091-release-entry.js, hookNames=[], hookCount=0.

openclaw plugins inspect cogentnexus-openclaw --json --runtime
activated=true, status=loaded, hookCount=42, typedHooks includes before_agent_run priority 2000, services include the CNX services. This command loads/inspects the plugin in the CLI inspection process; it does not identify the module cache or registry of Gateway PID 17080.

openclaw gateway call --help
Allowed documented methods shown: health/status/system-presence/cron.*. No plugin-registration or effective-hook-registry method is exposed.

openclaw plugins inspect --help
--runtime is available, but no PID/process binding option is provided.
```

`openclaw plugins inspect --json --runtime` is the smallest available **CLI-process** observation seam: it exposes `typedHooks`, priorities, services, and `hookCount=42`. It does not cross the boundary into the already-running Gateway process. The persisted inventory and CLI runtime inspection therefore remain distinct from process-scoped evidence.

## Gateway process identity

The actual Gateway PID was attributed using `openclaw gateway status`, not by selecting an arbitrary `node.exe`:

```text
PID 17080
state Ready
port 18789
command C:\\Program Files\\nodejs\\node.exe C:\\Users\\CDQ-P\\AppData\\Roaming\\npm\\node_modules\\openclaw\\dist\\index.js gateway --port 18789
parent PID 14104
```

Read-only native module inspection:

```text
powershell.exe ... Get-Process -Id 17080 -Module ...
```

returned `node.exe` and native DLLs only. It did not expose JavaScript module URLs, Node `require.cache`, the ES module registry, or the effective hook registry.

## Artifact/source hashes

```text
sha256sum C:/Users/CDQ-P/.openclaw/extensions/cogentnexus-openclaw/dist/v091-release-entry.js
c15b2f61a1596f301510e9cd392851ef99427c6c129d653d2d336cfefa79b3a8

git show origin/...:plugins/.../v091-release-entry.ts | sha256sum
a70b908fb31c2d6c2d36540b8ffda81f8c088de830c069e5dcae0a9b9709db86

git show origin/...:plugins/.../index.ts | sha256sum
6aa3726abfc412a019a92c6b4244ab82d6b79dd3abf82a06a4f0fa9f7983f333
```

The installed artifact hash is inventory/file evidence only and is not bound to PID 17080.

## Registration lifecycle observation

| Boundary | Finding |
|---|---|
| A — `releaseEntry.register()` entered | Static source and CLI-process inspection show the function exists and is invoked by the inspection loader. No Gateway-PID event/counter exposes entry in PID 17080. **UNOBSERVABLE process-scoped.** |
| B — legacy `register(runtimeApi)` invoked | Static source proves the call site and `void | Promise<void>` type. No process-scoped invocation count/owner/identity is exposed. **UNOBSERVABLE process-scoped.** |
| C — `before_agent_run` registration executed | CLI runtime inspection reports typed hook entries, including priority 2000, but this is not the Gateway registry. No live registration callback or process-scoped handler identity is exposed. **UNOBSERVABLE process-scoped.** |
| D — `installManagedRuntimeGuards` completed | Source shows synchronous and Promise-resolved paths. No Gateway diagnostic event, service-start record, completion marker, or process-scoped observation exposes completion. **UNOBSERVABLE.** |
| E — effective hook registry contains CNX handler | `plugins list` reports `hookCount=0`; `plugins inspect --runtime` reports a CLI-process `hookCount=42` and typed hooks. Neither is the effective registry inside PID 17080. **UNOBSERVABLE process-scoped.** |

## Async registration findings

The existing production seam accepts a Promise-returning legacy registration:

```ts
const registered = register(runtimeApi);
if (registered && typeof (registered as Promise<void>).then === "function") {
  return Promise.resolve(registered).then(installManagedRuntimeGuards);
}
installManagedRuntimeGuards();
```

Therefore:

- registration can return synchronously or return a Promise;
- the CNX entry observes the returned Promise locally and delays `installManagedRuntimeGuards` until resolution in the Promise branch;
- no evidence was found that the OpenClaw Gateway exposes A entered, B returned/pending, Promise resolved, or D completion as a read-only process-scoped diagnostic;
- no async flow was changed.

## Test result

Exact command:

```text
npm test -- --run src/cnx348-effective-runtime-provenance.test.ts
```

Exact result:

```text
npm notice run vitest run --config ./vitest.config.ts --run src/cnx348-effective-runtime-provenance.test.ts
'vitest' is not recognized as an internal or external command,
operable program or batch file.
EXIT=1
```

Dependencies were not installed because that is outside the read-only investigation scope. The test-only seam was inspected statically; no synthetic test result is claimed.

## Classification

**UNRESOLVED / BLOCKED.**

- **D PROVEN:** No. There is no exact process-scoped mismatch between loaded and expected CogentNexus module identity.
- **E PROVEN:** No. No Dashboard/WebChat provider execution was performed, and no process-scoped evidence shows execution without `before_agent_run`.
- The available CLI runtime inspection is useful for a separate CLI-process synthetic/runtime view, but it is not an authoritative Gateway-PID observation boundary.
- `hookCount=0` from plugin inventory is explicitly not treated as proof of an empty effective registry.

## Production changes

**NO production changes.** Only this report is added. No production source, build output, installed plugin, runtime/configuration, database, provider routing, UI, or Gateway process was changed.

## Hard-fence verification

- No plugin install/reinstall.
- No Gateway restart/start/stop.
- No provider call, routing change, semantic request, Dashboard/WebChat UI interaction, replay, or resend.
- No runtime/config/database mutation.
- No changes to `durableAdmissionEligible`, timeout authority, or admission ownership.
- No v0.9.5 tag/history mutation.
- No force-push or history rewrite.
- No self-acceptance.

## Smallest next probe

A separately authorized, read-only **Gateway-side** diagnostic boundary is still required. The smallest useful probe is an operator-scoped Gateway diagnostic/RPC (or equivalent support-only introspection) that returns, for the already-running Gateway PID:

1. loaded CogentNexus JavaScript module URL/cache identity;
2. release-entry and legacy registration invocation/completion state;
3. effective `before_agent_run` handler identity, owner, priority, and registry membership.

It must be correlated with the PID from `openclaw gateway status` and must not restart, mutate, invoke a provider, or alter registration behavior. Until that boundary exists, A–E process-scoped observations remain unresolved and D/E must not be inferred from inventory, static source, or CLI-process inspection.
