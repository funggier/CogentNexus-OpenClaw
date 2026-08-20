# CogentNexus lifecycle launchers

The generated `cnx.cmd`/shell launchers forward operator commands to the Host Controller.

Current mode semantics:

- `enable` -> transactionally enter MANAGED after activation checks;
- `disable` -> restore native OpenClaw and enter PASSTHROUGH;
- `stop` -> deliberate MAINTENANCE stop with durable state preserved;
- `start` / `restart` -> reconcile desired managed runtime and resume eligible durable work;
- `gateway start|stop|restart` -> lifecycle action under Host desired-state rules.

Do not treat a deliberate stop as a crash or allow the supervisor to immediately undo it.

The accepted recovery baseline is v0.9.1 on OpenClaw 2026.7.1-2; see root `docs/CURRENT_STATE.md`.
