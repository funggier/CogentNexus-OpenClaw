# `cnxclaw check` — read-only system pre-flight

CogentNexus-OpenClaw v0.9.3 groups diagnostic inspection under the `check` namespace. The current managed provider contract is **Ollama only**.

`status` answers what state is recorded now. `check` actively verifies whether that state and its dependencies are coherent/ready, but never repairs or mutates them.

## Full system check

```powershell
.\cnxclaw.cmd check system
```

The system check evaluates, in dependency order:

1. CogentNexus-OpenClaw installation/core files;
2. Host controller state and interrupted owned transitions;
3. CNXCLAW/OpenClaw configuration validity;
4. OpenClaw installation and validated compatibility baseline;
5. Ollama discovery/readiness;
6. OpenClaw Ollama model routing/catalog visibility;
7. Gateway health;
8. Ticket database integrity/readability and disk headroom;
9. maintenance/recovery fences and supervisor snapshot;
10. delivery/outbox state;
11. memory/resource headroom.

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

## Provider checks

Current v0.9.3 provider checks target Ollama:

```powershell
.\cnxclaw.cmd check provider
.\cnxclaw.cmd check provider ollama
```

The report is observational only. Unsupported provider names are outside the v0.9.3 managed contract.

## Component checks

```powershell
.\cnxclaw.cmd check cogentnexus-openclaw
.\cnxclaw.cmd check config
.\cnxclaw.cmd check openclaw
.\cnxclaw.cmd check gateway
.\cnxclaw.cmd check provider
.\cnxclaw.cmd check provider ollama
.\cnxclaw.cmd check model
.\cnxclaw.cmd check storage
.\cnxclaw.cmd check recovery
.\cnxclaw.cmd check delivery
.\cnxclaw.cmd check resources
```

`check system` is not merely `check all`: it can identify cross-component inconsistency that individual component checks cannot establish independently.

## Read-only invariant

Every `cnxclaw check ...` command must remain read-only.

A check must not:

- start/stop/restart Gateway;
- start/stop Ollama;
- change managed provider state;
- clear or repair transition state;
- rewrite OpenClaw configuration;
- repair or migrate the Ticket database;
- clear recovery/outbox state;
- execute model inference.

Reports explicitly include:

```text
No state was changed.
```

The Ticket database is opened read-only for integrity/delivery inspection where applicable.

## Preflight reuse by lifecycle

The operator-visible checker and lifecycle preflight must use the same supported Ollama/config/install primitives. Lifecycle mutation is allowed only after its read-only preflight succeeds.

This prevents a split-brain diagnostic design in which `check` reports one state while lifecycle logic relies on unrelated readiness rules.

## `PASS`, `WARN`, `FAIL`, `INDETERMINATE`

Component rows use four diagnostic states:

- `PASS` — evidence establishes the check passed;
- `WARN` — usable but attention is warranted;
- `FAIL` — evidence establishes a required condition is not met;
- `INDETERMINATE` — the checker could not establish either healthy or failed state safely.

`INDETERMINATE` is intentionally distinct from `FAIL`; uncertainty is not converted into an invented failure claim.

## Historical compatibility note

Frozen v0.9.2 source/evidence may describe provider-neutral checks, including LM Studio. That history remains valid historical evidence, but it is not current v0.9.3 operator guidance.
