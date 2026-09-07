# CNX-20260907-305 — Bounded Staging Installer Retry

## Disposition

`PASS_STAGING_INSTALLER_RETRY_GREEN__MANAGED_ENABLE_NOT_AUTHORIZED`

The one authorized repaired staging-installer retry completed successfully with exit code 0. Task305 stopped before `cnxclaw enable` as required.

## Candidate and preflight

The branch was freshly fetched and re-anchored before execution at:

```text
Candidate/remote HEAD: 113974b1ec28f50506b1fd2dcbd18d37d638f6d7
```

Read-only preflight showed:

- Host mode `passthrough`, generation `62`
- Gateway HTTP `200`
- Ollama HTTP `200`
- SQLite `pragma integrity_check`: `ok`
- no overlapping installer process
- target and protected Ticket/session owners distinct
- Task301 wiring already installed and byte-exact before retry

The initial combined health probe had a client output error while writing response bytes. It was not treated as evidence; the probes were rerun with Python and both returned HTTP 200.

## Exact invocation

The supported repository installer was invoked exactly once:

```text
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "<exact checkout>\\scripts\\install.ps1" -Workspace "C:\\Users\\CDQ-P\\.openclaw\\workspace" -SkipPlugin -SkipGatewayRestart -SkipAgentsPolicy
```

No second invocation was made.

## Installer result

```text
exit code: 0
owned-runtime-ensure: exit_code=0
skill validation: PASS
SkipPlugin staging postcondition: emitted
Host enable: skipped by -SkipGatewayRestart
Gateway status: healthy
Supervisor doctor: success
CogentNexus-OpenClaw status: success
final: CogentNexus-OpenClaw v0.9.3 installation completed successfully
```

The installer created a new backup under:

```text
C:\\Users\\CDQ-P\\.openclaw\\workspace\\.cogentnexus-openclaw\\install-backups\\cogentnexus-openclaw-20260907-203124
```

The plugin was not installed or replaced. Read-only plugin inventory after the retry reported `cogentnexus-openclaw` version `0.9.3`, `enabled=false`, `status=disabled`.

## Postflight identity

The following installed skill files matched the exact candidate byte-for-byte:

```text
supervisor_quiescence.py
4316 bytes
SHA-256: d52f51a6aaa4fa8fd8361d684c1cf73462c93b3a083132f769374edcb4dd8d4a

host.py
36284 bytes
SHA-256: 6fd58b5ee9a039a82c59826287850564446ab631300e2b0930e3fda39dc1f2c0

host_authority_v091.py
11531 bytes
SHA-256: 6e70eda45fbf61cfa6f345a32aaf3cc6592c7b9aa10bbb56d12356fc1edce310

host_control_v092.py
5733 bytes
SHA-256: f8a0234e07ab9000fa3ea9810156051522db1fba1c3bce992bb1729ad0543d77

cnxclaw_v093.py
3829 bytes
SHA-256: 994078bc4c79bc5f653744a9ba08ccdf10fb60d0366e186df0f4b561a8957a85
```

The canonical launcher exists at `C:\\Users\\CDQ-P\\.openclaw\\workspace\\cnxclaw.cmd` and was written by the supported installer. The Supervisor Scheduled Task remained registered/Ready with Last Result `0`; it was not mutated by this task. The quiescence lease file was absent after the staging operation, as expected because no enable transaction ran.

## Live health and durable state

```text
Gateway: HTTP 200
Ollama: HTTP 200
Host mode: passthrough
Host generation: 62
Supervisor: Enabled / Ready / Last Result 0
SQLite integrity: ok
```

The actual SQLite schema was discovered before the durable readback. `ticket_outbox` had no row for the target. The exact target `cnx_assistant_delivery` row remained:

```text
ticket_id: CNXT-87fc2030-884f-4943-bb6e-864cc621d5dc
owner_session_key: agent:main:discord:channel:1391855033993138217
owner_generation: 2
kind: direct_result
idempotency_key: cnxclaw-direct-result:CNXT-87fc2030-884f-4943-bb6e-864cc621d5dc:g2
status: pending
attempt_count: 685
last_error: OpenClaw Gateway RPC chat.history returned no JSON output (exit=0, stdout=none, stderr=empty)
delivered_at: null
```

The protected Ticket `CNXT-dc11c9a0-8a89-4df5-9c48-345260725be4` had no delivery row and remained untouched. No Ticket/session/SQLite mutation, replay, redelivery, disposition, or semantic send occurred.

## Completion boundary

### Proven

- repaired `-SkipPlugin` staging contract executes to terminal success
- exact Task301 wiring remains installed
- plugin remains disabled and was not replaced
- Host remains safely in `passthrough`
- Gateway, Ollama, Supervisor, and SQLite are healthy

### Not authorized/not proven

- managed activation
- `cnxclaw enable`
- durable Discord delivery settlement
- detached-worker requalification

## Safety accounting

```text
staging installer invocation: 1
staging installer retry within Task305: 0
second installer invocation: 0
cnxclaw enable: 0
plugin install/replace: 0
Gateway restart/reload: 0
Scheduled Task/service mutation: 0
manual config/Ticket/SQLite/session mutation: 0
semantic send: 0
replay/redelivery/disposition: 0
protected-state mutation: 0
force push: 0
```

## Next bounded task

A separate successor task must authorize managed activation and live requalification. It must require a fresh exact installed-candidate identity gate, quiescence lease preflight, one bounded `cnxclaw enable`, and exact post-readback. It must not settle the existing pending Discord delivery without an exact Ticket/session-generation/idempotency-bound durable receipt.
