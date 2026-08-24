# Runtime Lifecycle

CogentNexus-OpenClaw lifecycle is driven by persisted operator intent.

## Modes

- MANAGED: CNXCLAW owns continuity/recovery and expected managed runtime state.
- PASSTHROUGH: CNXCLAW ownership/interception disabled; native OpenClaw remains usable.
- MAINTENANCE: deliberate stop; state preserved and automatic recovery must not fight the stop.

## Commands

`start`, `stop`, `restart`, Gateway lifecycle commands, `disable`, and `enable` must update durable desired state before deterministic reconciliation.

Manual stop is not a crash. A later explicit start/restart may resume eligible durable work.

Transactional enable must not commit MANAGED until plugin/policy/runtime health stages succeed. Disable must restore native surfaces before PASSTHROUGH is considered complete.

Compatibility baseline: OpenClaw 2026.7.1-2. Newer versions require a new compatibility check before claiming identical lifecycle/recovery behavior.
