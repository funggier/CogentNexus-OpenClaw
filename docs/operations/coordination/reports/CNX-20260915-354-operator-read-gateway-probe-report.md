# CNX-354 — Operator-Read Gateway Probe Report

## Authority and ancestry

- Repository: `funggier/CogentNexus-OpenClaw`
- Remote branch: `cnx-354-operator-read-gateway-probe`
- Starting verified HEAD: `4862e9152de6084600e27b0b50be95e997273842`
- Parent baseline: `ad7bf9beed945d756b8d4ddbde732a2671a71432`
- Ancestry: verified; `git merge-base --is-ancestor ...` exit `0`.
- Final GitHub HEAD and report blob are recorded after publication below.

Preflight was run against the fetched remote ref, before investigation:

```text
git remote -v
origin https://github.com/funggier/CogentNexus-OpenClaw.git (fetch)
origin https://github.com/funggier/CogentNexus-OpenClaw.git (push)

git fetch origin

git rev-parse origin/cnx-354-operator-read-gateway-probe
4862e9152de6084600e27b0b50be95e997273842

git merge-base --is-ancestor ad7bf9beed945d756b8d4ddbde732a2671a71432 origin/cnx-354-operator-read-gateway-probe
exit 0
```

The fresh checkout was clean at preflight. No local-only state was used as authority.

## Gateway process identity

Read-only command: `openclaw gateway status`.

```text
Gateway: bind=loopback (127.0.0.1), port=18789
Command: C:\\Program Files\\nodejs\\node.exe C:\\Users\\CDQ-P\\AppData\\Roaming\\npm\\node_modules\\openclaw\\dist\\index.js gateway --port 18789
Runtime: running (pid 17080, state Ready, Gateway process detected for gateway port 18789.)
Connectivity probe: ok
Capability: connected-no-operator-scope
Listening: 127.0.0.1:18789
```

The PID is OpenClaw's Gateway-owned status identity, not an inferred port or arbitrary `node.exe` process. No JavaScript module-cache or hook-registry identity was exposed by status.

## Exact live commands and results

### Version, status, and probe

```text
$ openclaw --version
OpenClaw 2026.7.1-2 (0790d9f)
EXIT=0

$ openclaw gateway probe
Reachable: yes
Capability: connected-no-operator-scope
Warning:
- Read-probe diagnostics are limited by gateway scopes (missing operator.read).
  Connection succeeded, but read-only status calls are incomplete.
Targets
Local loopback ws://127.0.0.1:18789
  Connect: ok (37ms) · Capability: connect-only · Read probe: limited - missing scope: operator.read
EXIT=0
```

This is an exact authorization boundary observation. The current CLI connection is `connect-only`; `operator.read` is absent. No scope, token, credential, config, or Gateway lifecycle state was changed. The probe's own remediation hint (pair identity or use credentials with `operator.read`) was not acted on because privilege broadening is fenced.

### Documented Gateway method inventory

```text
$ openclaw gateway call --help
Usage: openclaw gateway call [options] <method>
Arguments:
  method  Method name (health/status/system-presence/cron.*)
Options:
  --expect-final  Wait for final response (agent)
  --json
  --params <json>
  --timeout <ms>
  --token <token>
  --password <password>
  --url <url>
EXIT=0
```

The documented method surface contains `health`, `status`, `system-presence`, and `cron.*`; it contains no documented plugin-registration, runtime-module, hook-registry, or operator introspection method.

Read-only `gateway call health` succeeded despite the limited probe and returned Gateway-owned health data. Relevant output:

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

`gateway call status` also succeeded and returned runtime version, heartbeat, channel summary, task summary, session counts, and event-loop health. It returned no module identity, registration owner/count, or effective hook registry.

Classification of documented methods:

| Surface | Classification | Reason |
|---|---|---|
| `gateway probe` | B / authorization boundary | Gateway connectivity/capability result; no process-local plugin state |
| `gateway call health` | A, Gateway-owned but coarse | Gateway response includes loaded IDs/errors; no module or effective registry identity |
| `gateway call status` | A, Gateway-owned but coarse | Gateway runtime/status summary; no plugin registration state |
| `gateway call --help` | C | CLI help/argument inventory |
| `system-presence`, `cron.*` | D for this objective | Documented method names but not plugin/runtime introspection |

Only a process-local Gateway response carrying plugin/runtime state could satisfy the primary objective. `health` and `status` do not do so.

### CLI plugin inspection comparison

These were inspected only as comparison controls:

```text
$ openclaw plugins list --json
registry.source = persisted
cogentnexus-openclaw:
  version = 0.9.5
  source = C:\\Users\\CDQ-P\\.openclaw\\extensions\\cogentnexus-openclaw\\dist\\v091-release-entry.js
  status = loaded
  hookNames = []
  hookCount = 0
  services = []
EXIT=0

$ openclaw plugins inspect cogentnexus-openclaw --json --runtime
plugin.source = C:\\Users\\CDQ-P\\.openclaw\\extensions\\cogentnexus-openclaw\\dist\\v091-release-entry.js
activated = true
status = loaded
hookCount = 42
services = 6
before_agent_run entries include priority 2000
imported = true
Gateway methods = []
EXIT=0
```

`plugins list --json` is persisted/inventory-derived. `plugins inspect --runtime` loads and inspects the plugin in the CLI inspection process. Its output contains no Gateway PID, process binding, module-cache identity, Gateway plugin-manager identity, or Gateway effective-registry owner. `plugins inspect --help` exposes only `--runtime`; it exposes no PID/process-binding option.

Classification: both are **Level 1 / CLI-local or persisted**, not Level 3 Gateway process-local evidence.

## Scope and source boundary

The repository source was searched and relevant lifecycle files inspected:

- `plugins/cogentnexus-openclaw/src/v091-release-entry.ts`
- `plugins/cogentnexus-openclaw/src/v091-final-entry.ts`
- `plugins/cogentnexus-openclaw/src/v090-final-entry.ts`
- `plugins/cogentnexus-openclaw/src/index.ts`

Static source shows the release entry invokes legacy `register(runtimeApi)` and handles `void | Promise<void>`. `index.ts` registers `before_agent_run` at priority `2000` when `preInferenceAdmission !== false`. The source does not expose a supported Gateway read path for the Gateway's loaded module URL/cache, plugin-manager object, registration owner/counter, or effective hook registry. Static source is not process-scoped evidence.

The implemented scope state machine observed live is:

- connect-only: **available**;
- read-only `operator.read`: **not available to the current connection**;
- admin/other elevated scopes: **not requested, not changed, and not used**.

No permission or authorization mutation was attempted.

## Process-local registration and module evidence

| Required observation | Gateway PID 17080 result |
|---|---|
| Actual loaded CNX module URL/path | Not exposed |
| JS `require.cache` / ESM identity | Not exposed |
| plugin-manager instance/owner | Not exposed |
| `releaseEntry.register()` entered | Not exposed |
| legacy `register(runtimeApi)` invoked | Not exposed |
| registration count | Not exposed |
| Promise pending/returned | Not exposed |
| Promise resolved | Not exposed |
| `installManagedRuntimeGuards` completed | Not exposed |
| effective `before_agent_run` membership | Not exposed |
| handler identity/owner/priority in Gateway | Not exposed |

The CLI result `hookCount=42` and `before_agent_run` priority `2000` is Level 1. The Gateway `health` result containing `plugins.loaded` is Level 2. No Level 3 process-local registration evidence was obtained.

## Async registration visibility

The production seam inspected is:

```ts
const registered = register(runtimeApi);
if (registered && typeof (registered as Promise<void>).then === "function") {
  return Promise.resolve(registered).then(installManagedRuntimeGuards);
}
installManagedRuntimeGuards();
```

Static source establishes the possible synchronous and Promise-returning paths only. No supported Gateway read surface reports states A through F:

- A `releaseEntry.register` entered: unobservable;
- B legacy register invoked: unobservable;
- C Promise pending/returned: unobservable;
- D Promise resolved: unobservable;
- E guard installation completed: unobservable;
- F effective `before_agent_run` membership: unobservable.

No registration was initiated or changed by this investigation.

## Three-level distinction

1. **Level 1 — CLI inspection:** `plugins list --json` and `plugins inspect ... --runtime`; persisted or CLI-process data.
2. **Level 2 — Gateway-owned coarse observation:** `gateway call health` and `gateway call status`; responses originate from the Gateway, but do not expose process-local registration state.
3. **Level 3 — Gateway process-local introspection:** an operator-read Gateway response carrying the loaded module identity and effective registration/hook state. **No such supported method was found or exercised.**

## Classification

- **OPERATOR-READ BOUNDARY FOUND:** **No.** The existing connection lacks `operator.read`, and the documented Gateway methods that can be called remain too coarse. No supported operator-read process-local plugin/runtime surface was demonstrated.
- **D PROVEN:** **No.** No exact Gateway-process module identity mismatch was observed.
- **E PROVEN:** **No.** No provider invocation, Dashboard/WebChat interaction, or semantic request was performed, and no Gateway-side evidence shows execution without `before_agent_run`.
- **UNRESOLVED / BLOCKED:** **Yes.** Exact missing boundary: the current authorized connection is `connect-only` with `missing scope: operator.read`; the documented Gateway method surface has no plugin/runtime/hook introspection method; `health`/`status` expose only coarse Gateway-owned data. This is an observability limitation, not a production defect.

## Production changes and hard-fence verification

Production changes: **none**. Only this report is added. No production source, instrumentation, build output, installed plugin, config, token, permission, authorization, database, runtime, provider, UI, or Gateway process was changed.

The following hard-fenced actions were not performed: scope/permission broadening; token creation or mutation; Gateway restart/stop/start; plugin install/reinstall; provider invocation/routing change; Dashboard/WebChat interaction; semantic request; CNX-344 replay/resend; runtime/database mutation; `durableAdmissionEligible` or timeout-authority change; new admission owner; v0.9.5 history/tag mutation; force-push; history rewrite; self-acceptance.

## Testing

No focused repository test was run: the task allowed it only if the existing environment supported it, and the previously recorded repository environment reports `vitest` unavailable. Dependencies were not installed, consistent with the read-only fence. Live investigation commands above were executed directly and returned the exact results recorded here.

## Smallest next probe

Only under a separately authorized read-only credential/scope, exercise an already-supported `operator.read` connection. If the documented method set remains unchanged, the smallest useful OpenClaw-owned boundary would be an operator-scoped Gateway diagnostic method returning, for the PID from `gateway status`: loaded CNX module URL/cache identity, registration invocation/completion state, plugin-manager owner, and effective `before_agent_run` handler identity/priority/registry membership. That would be a new capability and is explicitly outside CNX-354; it must not be created as part of this task.

## Publication closeout

This report is the only changed path in the publication history from the verified starting HEAD. The exact final GitHub commit and report blob are intentionally verified from the remote branch/tree after publication rather than embedded as self-referential values: changing this report changes both its containing commit and its Git blob.

Final closeout verification command:

```text
git fetch origin
git rev-parse origin/cnx-354-operator-read-gateway-probe
git ls-tree origin/cnx-354-operator-read-gateway-probe -- docs/operations/coordination/reports/CNX-20260915-354-operator-read-gateway-probe-report.md
git diff --name-status 4862e9152de6084600e27b0b50be95e997273842 origin/cnx-354-operator-read-gateway-probe
```

The final values are reported from that remote read-back, not inferred from a stale value embedded in the report itself.
