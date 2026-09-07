# CNX-20260907-300 — Quiesce Supervisor and Requalify Enable

## Disposition

`BLOCKED_UNSUPPORTED_SUPERVISOR_QUIESCENCE_MECHANISM__NO_ENABLE__NO_MUTATION`

Task300 could not proceed safely. The task authorizes Supervisor quiescence only through a supported mechanism, and explicitly requires stopping if the only available mechanism is an ad-hoc Scheduled Task mutation. The CLI and repository source expose no canonical `quiesce`, `maintenance`, or Supervisor pause/restore operation. The visible Windows Scheduled Task can only be changed through direct scheduler mutation, which is outside the allowed supported boundary.

Consequently:

- `cnxclaw enable`: 0 invocations in Task300
- Supervisor quiescence: 0
- Supervisor restore: 0
- no retry was attempted

## Re-anchor and preflight

- remote HEAD at preflight: `6fb888c4125fa4cf194853b5f2b8028212177b20`
- branch: `agent/v0.9.3-full-stabilization`
- task: `CNX-20260907-300`
- accepted candidate: `36cd4c800ded28bdb7165fcad6e0bfb48b4e933b`
- live controller: `mode=passthrough`, `generation=62`
- live resolver: `4847` bytes, SHA-256 `a93161416558c566d2227a0c8abaeb1cbf747ef73e39bc4c8bdc4299195d4d61`
- target Ticket: `CNXT-87fc2030-884f-4943-bb6e-864cc621d5dc`
- target session key: `agent:main:discord:channel:1391855033993138217`
- target generation: `2`
- protected Ticket: `CNXT-dc11c9a0-8a89-4df5-9c48-345260725be4`

Read-only health/state checks passed:

- Gateway: healthy, reachable, HTTP 200
- Ollama: reachable/healthy/ready, model `qwen3.5:9b`
- SQLite: `PRAGMA integrity_check = ok`
- no maintenance marker
- Supervisor health snapshot: healthy
- target Ticket: `accepted`, delivery `pending`, `delivery_confirmed_at=null`
- protected Ticket has no delivery row and was not modified

The Task296 test file was not present at the live workspace path inspected; this does not authorize deployment and is recorded as a preflight limitation. Repository candidate identity remained bound to the accepted SHA above.

## Quiescence mechanism investigation

CLI help lists lifecycle operations (`start`, `stop`, `restart`, `enable`, `disable`, `reset`, `uninstall`) and read-only checks, but no Supervisor quiesce/pause/restore operation.

Repository inspection found:

- `host.py` supports an internal `maintenance` state for lifecycle stop, but this is a Host state/lifecycle mutation, not a supported bounded Supervisor-quiescence command for Task300.
- Supervisor execution is registered as a recurring Windows Scheduled Task running `host_control_v092.py ... supervisor`.
- No canonical task-scoped quiescence token, pause API, or paired supported restore command was exposed by the inspected launcher/source.

Directly disabling and re-enabling `\\CogentNexus-OpenClaw-Supervisor` would therefore be an ad-hoc Scheduled Task mutation. Task300's precondition and stop rule prohibit proceeding in that case.

## Decision

Stopped before the first permitted mutation. The prior Task298 failure remains the active deployment blocker. A successor task must introduce or explicitly authorize a supported, bounded Supervisor quiescence mechanism and its exact restore/readback contract. It must not rely on an unbounded `schtasks` disable/enable pair.

## Hard-fence accounting

```text
Supervisor quiescence: 0
Supervisor restore: 0
cnxclaw enable: 0
retry enable: 0
restart/reload: 0
installer/install-over/uninstall/reset: 0
Scheduled Task mutation: 0
config mutation: 0
service/provider mutation: 0
semantic send: 0
replay/redelivery/disposition: 0
manual Ticket/SQLite/session/transcript mutation: 0
session create/delete: 0
protected state mutation: 0
release/tag/force push: 0
```
