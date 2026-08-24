# `cnxclaw check` — read-only system pre-flight

CogentNexus-OpenClaw v0.9.2 groups diagnostic inspection under the `check` namespace.

`status` answers **what state is recorded now**. `check` actively verifies whether that state and its dependencies are coherent/ready, but never repairs or mutates them.

## Full system check

```powershell
.\cnxclaw.cmd check system
```

This is the aircraft-style pre-flight inspection. It evaluates, in dependency order:

1. CogentNexus-OpenClaw installation/core files;
2. Host controller state and interrupted provider transitions;
3. CNX/OpenClaw configuration validity;
4. OpenClaw installation;
5. provider discovery and persisted/requested provider;
6. selected provider endpoint/readiness;
7. OpenClaw model routing/catalog visibility;
8. Gateway health;
9. Ticket database integrity/readability and disk headroom;
10. maintenance/recovery fences and supervisor snapshot;
11. delivery/outbox state;
12. memory/resource headroom.

It returns one readiness verdict:

- `READY`
- `READY_WITH_WARNINGS`
- `NOT_READY`
- `INDETERMINATE`

Exit codes are stable for scripts:

| Exit | Verdict |
| ---: | --- |
| 0 | `READY` |
| 1 | `READY_WITH_WARNINGS` |
| 2 | `NOT_READY` |
| 3 | `INDETERMINATE` |

## Provider-specific hypothetical preflight

You can ask whether the machine is ready for a provider without changing the persisted selection:

```powershell
.\cnxclaw.cmd check system --provider lmstudio
```

The report records both the requested preflight provider and the persisted selection. The command is observational only.

## Component checks

```powershell
.\cnxclaw.cmd check cogentnexus
.\cnxclaw.cmd check config
.\cnxclaw.cmd check openclaw
.\cnxclaw.cmd check gateway
.\cnxclaw.cmd check provider
.\cnxclaw.cmd check provider ollama
.\cnxclaw.cmd check provider lmstudio
.\cnxclaw.cmd check model
.\cnxclaw.cmd check storage
.\cnxclaw.cmd check recovery
.\cnxclaw.cmd check delivery
.\cnxclaw.cmd check resources
```

`check system` is not merely `check all`: it can identify cross-component inconsistency that individual components cannot establish by themselves.

## Read-only invariant

Every `cnxclaw check ...` command must remain read-only.

A check must not:

- start/stop/restart Gateway;
- start/stop Ollama or LM Studio;
- change `selectedProvider`;
- clear or repair `providerTransition`;
- rewrite OpenClaw configuration;
- repair or migrate the Ticket database;
- clear recovery/outbox state;
- execute model inference.

Reports explicitly include:

```text
No state was changed.
```

The Ticket database is opened read-only for integrity/delivery inspection.

## Preflight reuse by lifecycle

The operator-visible checker and lifecycle preflight use the same provider/config/install primitives. `start --provider ...` first performs read-only provider preflight; only after that succeeds may it write a durable provider-transition marker and begin lifecycle mutation.

This avoids a split-brain diagnostic design in which `check` says one thing while `start` uses unrelated readiness rules.

## `PASS`, `WARN`, `FAIL`, `INDETERMINATE`

Component rows use four diagnostic states:

- `PASS` — evidence establishes the check passed;
- `WARN` — usable but attention is warranted (for example a provider is installed but currently stopped);
- `FAIL` — evidence establishes a required condition is not met;
- `INDETERMINATE` — the checker could not establish either healthy or failed state safely.

`INDETERMINATE` is intentionally distinct from `FAIL`; uncertainty is not converted into an invented failure claim.
