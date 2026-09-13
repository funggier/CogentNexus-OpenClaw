# v0.9.5 Post-release Baseline

This document is the current-facing operational baseline for the published v0.9.5 release.

## Release identity

- Repository: `funggier/CogentNexus-OpenClaw`
- Version: `0.9.5`
- Main merge SHA: `50be0b973c30fd8d1528aaac3497c0fc3b0b4d95`
- Git tag: `v0.9.5`
- Tag target: `50be0b973c30fd8d1528aaac3497c0fc3b0b4d95`
- GitHub Release: `CogentNexus-OpenClaw v0.9.5`
- Release state: published, non-draft, non-prerelease

## Operational validation

The published release has been independently verified from the exact `v0.9.5` tag:

```text
v0.9.5 tag
  -> exact detached clone
  -> VERSION 0.9.5
  -> package/plugin version 0.9.5
  -> installer success
  -> installed plugin loaded
  -> Gateway healthy
  -> Ollama ready
  -> Ticket store healthy
  -> supervisor healthy
  -> pending outbox 0
```

The exact-tag source `dist` tree and installed plugin `dist` tree matched in file count and tree fingerprint during post-release verification.

## Runtime/provider baseline

- CNX mode: `active`
- Operator mode: `managed`
- OpenClaw plugin: loaded, version `0.9.5`
- Managed provider: Ollama
- OpenAI: accepted as a required pass-through provider path and live-tested successfully
- Cloud provider ownership: OpenClaw-owned pass-through for authentication, routing/model selection, runtime, probing, lifecycle, and recovery
- LM Studio: not required by the v0.9.5 release gate
- Pending outbox: `0`

## Continuity and execution baseline

The release acceptance chain demonstrated the intended durable execution path:

```text
human intent
  -> durable Ticket admission
  -> logical session/run ownership
  -> model execution
  -> durable result
  -> delivery confirmation
  -> settled state
```

Controlled actionable wake was verified with exactly one durable work item, preserved ticket/session/run identity, generation and ownership semantics, and returned to idle without duplicate ownership.

The continuity invariant remains:

> Once eligible work is durably accepted, it must not silently disappear. It must eventually become delivered/completed, cancelled, or explicitly failed with durable evidence.

## CI and release evidence

For the merge SHA `50be0b973c30fd8d1528aaac3497c0fc3b0b4d95`, post-release verification observed completed check-runs with the exact same `head_sha`; all observed completed check-runs had successful conclusions.

The legacy commit-status collection may be empty. An empty legacy status collection is not interpreted as CI pass/fail.

## Known diagnostic discrepancy

`cnxclaw.cmd check system` may still report a contradictory provider-selection diagnostic on the validated host even while `cnxclaw.cmd status` reports an active managed runtime and healthy Ollama/Gateway path.

This is retained as a **known checker anomaly** and is not silently promoted to PASS or treated as proof that the runtime is inactive. It remains outside the immutable v0.9.5 release and should be repaired only through a new development candidate and normal validation/release process.

## Release protection

The published v0.9.5 tag and GitHub Release are immutable release references for operational purposes. Post-release documentation changes on `main` must not rewrite or move the tag, alter the published Release target, or imply that the published release contains documentation changes made later on `main`.

Historical v0.9.4/v0.9.3/v0.9.2 reports remain historical evidence and should not be rewritten merely to make their wording current.

## Next development baseline

Future work must branch from the post-release `main` baseline. v0.9.5 remains the stable published reference and must not be retroactively modified.
