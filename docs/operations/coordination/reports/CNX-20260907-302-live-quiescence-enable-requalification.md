# CNX-20260907-302 — Live Quiescence and Enable Requalification

## Disposition

`BLOCKED_MISSING_INSTALLED_QUIESCENCE_WIRING__NO_ENABLE__NO_MUTATION`

Task302 stopped at the mandatory preflight gate. The Task301 quiescence repair is not present in the live installation, so the canonical `cnxclaw enable` was not invoked. No live mutation was performed.

## Authority and preflight anchor

- task: `CNX-20260907-302`
- parent: `CNX-20260907-301`
- branch: `agent/v0.9.3-full-stabilization`
- remote preflight HEAD: `9c96d3867132b444ea12c008c988072da177f889`
- accepted candidate: `36cd4c800ded28bdb7165fcad6e0bfb48b4e933b`
- target Ticket: `CNXT-87fc2030-884f-4943-bb6e-864cc621d5dc`
- target session key: `agent:main:discord:channel:1391855033993138217`
- protected Ticket/session: `CNXT-dc11c9a0-8a89-4df5-9c48-345260725be4` / `agent:main:discord:channel:1531199905673252946`

## Installed-wiring gate

Candidate-vs-live read-only comparison:

```text
supervisor_quiescence.py
candidate: exists, 4316 bytes, SHA-256 d52f51a6aaa4fa8fd8361d684c1cf73462c93b3a083132f769374edcb4dd8d4a
live:     MISSING

host.py
candidate: 35445 bytes, SHA-256 f4ac6f7acfe4f570108a9fd486669312dad3a115315fd9235a00096ad9478f45
live:     35985 bytes, SHA-256 5d5cb5d473547ed7b1912b60ee98521f740168d1d8a4c459f8cdabb273a354c8

host_authority_v091.py
candidate: 11265 bytes, SHA-256 2350652b080a2ab2283532892d7375c39d56ad4c50c299dd8a6570bcbcd98194
live:     11192 bytes, SHA-256 b1b0f212f07853b0a8784c5f3a21aca3e9f743aa1f150a02ef4e27ad19a3a0b9
```

Because the new lease module is absent and both owning files differ, the exact installed Task301 wiring is not proven. This is a hard stop; no attempt was made to install or copy it.

## Read-only state and health

```text
controller mode: passthrough
generation: 62
supervisor-quiescence lease: absent
Gateway: HTTP 200
Ollama: HTTP 200
SQLite PRAGMA integrity_check: ok
```

The target Ticket remained:

```text
status: accepted
failure_class: interrupted
delivery: pending
attempt_count: 685
delivery_confirmed_at: null
delivered_at: null
last_error: OpenClaw Gateway RPC chat.history returned no JSON output (exit=0, stdout=none, stderr=empty)
```

The protected Ticket remained separate and unchanged; its delivery query returned no row. No Ticket/session/delivery/recovery operation was issued.

## Supervisor readback

Read-only scheduler inspection showed:

```text
Task: \\CogentNexus-OpenClaw-Supervisor
Status: Ready
Scheduled Task State: Enabled
Last Result: 0
Task action: ...host_control_v092.py ... supervisor
```

This confirms the recurring Supervisor remains active, but no scheduler mutation was attempted because the installed-wiring gate failed.

## Method used

1. Fresh-fetch and reset a disposable repository worktree to the exact remote coordination HEAD.
2. Read Task302 and bind the accepted candidate.
3. Hash candidate `supervisor_quiescence.py`, `host.py`, and `host_authority_v091.py`.
4. Hash the corresponding live files and check module existence without modifying them.
5. Read Host controller/lease state, Gateway/Ollama endpoints, SQLite in read-only mode, target/protected Ticket rows, and Supervisor Scheduled Task metadata.
6. Apply the missing-wiring stop condition before any lifecycle command.
7. Publish this report and coordination state only.

## Hard-fence accounting

```text
cnxclaw enable: 0
Supervisor quiescence: 0
Supervisor restore: 0
Scheduled Task mutation: 0
service restart/reload: 0
installer/install-over/uninstall/reset: 0
config mutation: 0
semantic send: 0
replay/redelivery/disposition: 0
manual Ticket/SQLite/session/transcript mutation: 0
session create/delete: 0
protected-state mutation: 0
force push: 0
```

## Required successor authority

A successor task must authorize installation/adoption of the exact Task301 repair through a canonical supported installer or managed activation mechanism, and require a fresh installed-vs-candidate identity gate before any enable attempt. Task302 does not authorize copying files manually or retrying `enable`.
