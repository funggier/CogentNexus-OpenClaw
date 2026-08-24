# Review — CNX-20260824-046 Remove Proven Legacy and Fresh-Install Current

Decision: **ACCEPT_SAFE_PREMUTATION_STOP**  
Reviewed result: `BLOCKED_NATIVE_PLUGIN_INVENTORY_TIMEOUT`  
Reviewed report commit: `c96c3cfcbdc477187133ca2b5da7fff142b02851`  
Reviewed start HEAD: `d4747b6ec0ce034aee2cca15017c80f1c823942d`

## Publication verification

The report commit is exactly one commit ahead of the declared start HEAD and changes exactly one path:

`docs/operations/coordination/reports/CNX-20260824-046-remove-legacy-and-fresh-install-current.md`

No executable, installer, test, coordination pointer, or unrelated file was mixed into the report publication.

## Accepted evidence

Task 046 correctly stopped at its mandatory native plugin-inventory gate:

- `openclaw plugins list --json` exceeded the single authorized 120-second bound and returned no valid JSON;
- the bounded execution wrapper left zero matching diagnostic command processes;
- ownership of the native plugin registration, package root, config entry, and load paths therefore remained unproved;
- every destructive or lifecycle count remained zero;
- no backup, disable, uninstall, config cleanup, scheduled-task removal, path deletion, installer invocation, retry, or restore occurred;
- legacy CogentNexus remained managed at generation 32;
- Gateway, Ollama, four local models, OpenClaw user data, HermesAgent, unrelated workspace data, the primary repository, Ecosystem, staged-capability-loop, and retained Procmon evidence were preserved.

This is the required fail-closed behavior. Task 046 destructive authority is consumed and must not be reused.

## Source-directed diagnosis boundary

The installed OpenClaw build identifies itself as `2026.7.1-2 (0790d9f)`. At that exact upstream commit:

- `runPluginsListCommand` obtains config and synchronously calls `buildPluginRegistrySnapshotReport`;
- the snapshot path first calls `loadPluginRegistrySnapshotWithMetadata`, then constructs metadata and per-plugin dependency status;
- `OPENCLAW_PLUGIN_LIFECYCLE_TRACE=1` emits a bounded phase timing for `plugin registry snapshot`;
- `OPENCLAW_DISABLE_PERSISTED_PLUGIN_REGISTRY=1` is a process-local compatibility switch that can distinguish persisted-registry reads from derived discovery without editing live state;
- dependency inspection walks ordinary ancestor `node_modules` paths with synchronous existence checks and does not import plugin runtime code.

These source facts narrow the next proof surface, but they do not establish the live root cause. No fix or registry refresh is justified yet.

## Disposition

Accept Task 046 as a safe pre-mutation stop. Open a separate read-only diagnostic task to localize the hang across config load, persisted registry, derived discovery/manifest metadata, root fingerprinting, and dependency-status projection.

The diagnostic task may create temporary scripts/logs outside live OpenClaw/CogentNexus paths and may terminate only its own verified bounded CLI process after timeout. It must not refresh/repair the registry, edit config, load plugin runtime, invoke Procmon, or perform any CogentNexus lifecycle action.

A later removal/fresh-install retry requires a new task and new explicit operator authorization.
