# CNX-20260907-299 — Diagnose Enable Config Mutation Race

## Disposition

`NEEDS_CHATGPT__CONFIG_WRITE_RACE_CONFIRMED__ACTOR_NOT_UNIQUELY_ATTRIBUTED__QUIESCENCE_AUTHORITY_REQUIRED__NO_RETRY`

Task298's `ConfigMutationConflictError` is confirmed as an optimistic-concurrency conflict in the native OpenClaw config writer. The config changed during the bounded `cnxclaw enable` transaction. The evidence does not uniquely identify one writer. No enable retry, restart/reload, installer, config edit, service/task mutation, or live repair was performed under Task299.

## Authority

- task: `CNX-20260907-299`; parent: `CNX-20260907-298`
- branch: `agent/v0.9.3-full-stabilization`
- remote authority at final pre-write re-anchor: `860def0fc26ec2f8367d426656cf7991ac9904c4`
- candidate: `36cd4c800ded28bdb7165fcad6e0bfb48b4e933b`
- executor: Hermes; reviewer: ChatGPT

## Evidence

Installed OpenClaw source implements `assertBaseHashMatches(snapshot, expectedHash)` and throws `ConfigMutationConflictError("config changed since last load", { currentHash })` when the current config hash differs from the snapshot hash at commit. Its queue/file lock protects cooperating writers but cannot prevent an external writer after snapshot.

Task298 enable window:

```text
start 2026-09-07T09:28:42.567668+00:00
end   2026-09-07T09:29:42.085829+00:00
```

Read-only postflight stat of `C:\Users\CDQ-P\.openclaw\openclaw.json`:

```text
size 5583 bytes
mtime 2026-09-07T09:29:40.413126+00:00
```

The mtime is inside the enable window, proving an in-window config write.

Read-only `host-control-events.jsonl` entries in that interval:

```text
2026-09-07T09:28:47.730959+00:00 watchdog-compat-applied changed=false
2026-09-07T09:29:30.851517+00:00 managed-plugin-activation-repair-failed
2026-09-07T09:29:40.394471+00:00 watchdog-compat-restored restored=true
2026-09-07T09:29:40.394471+00:00 watchdog-compat-enable-rollback delegateExitCode=1
```

Read-only scheduler inspection showed `\\CogentNexus-OpenClaw-Supervisor` was `Enabled`, `Ready`, and configured to run `host_control_v092.py ... supervisor` recurrently while Task298 ran. This is a credible concurrent-writer source, but the ledger records no writer PID.

Read-only WMI showed the restored Gateway as `C:\Program Files\nodejs\node.exe ... openclaw ... gateway --port 18789`, PID `12196`, created at `2026-09-07 16:29:22 +07`. This proves restoration, not writer attribution.

Post-state: controller `mode=passthrough`, `generation=62`, route transaction null, Gateway HTTP 200, Ollama HTTP 200 with `qwen3.5:9b`, SQLite integrity `ok`. Target Ticket remained accepted/pending; protected Ticket/session remained untouched.

## Root-cause boundary

Confirmed: native snapshot/commit conflict; config mutation during enable; multiple host/config stages overlapped a recurring Supervisor; rollback restored passthrough and Gateway health.

Not proven: unique writer PID; whether Supervisor, nested Gateway/config lifecycle, or another host-control operation performed the conflicting write; that the Node resolver caused it; or that durable Discord delivery is repaired.

## Safe recovery boundary

A successor deployment task must explicitly authorize a supported quiescence mechanism preventing the recurring Supervisor and other config writers during the transaction, or a reviewed shared coordinator lock. It must require read-only proof of no competing writer, one bounded enable invocation, and postflight proof of managed mode, plugin activation, live resolver identity, and worker requalification. Do not manually edit `openclaw.json`, disable the Scheduled Task ad hoc, retry `enable`, or infer success from Gateway health.

## Hard-fence accounting

```text
enable retry: 0
restart/reload: 0
installer/install-over/uninstall/reset: 0
config mutation: 0
Scheduled Task mutation: 0
service/provider mutation: 0
semantic send: 0
replay/redelivery/disposition: 0
manual Ticket/SQLite/session/transcript mutation: 0
session create/delete: 0
protected state mutation: 0
release/tag/force push: 0
```
