# CogentNexus-OpenClaw lifecycle launchers

The generated `cnxclaw.cmd`/shell launchers forward operator commands to the Host Controller.

Current mode semantics:

- `enable` -> transactionally enter MANAGED after activation checks;
- `disable` -> restore native OpenClaw and enter PASSTHROUGH;
- `stop` -> deliberate MAINTENANCE stop with durable state preserved;
- `start` / `restart` -> reconcile desired managed runtime and resume eligible durable work;
- `gateway start|stop|restart` -> lifecycle action under Host desired-state rules.

Do not treat a deliberate stop as a crash or allow the supervisor to immediately undo it.

Historical recovery-core evidence began on v0.9.1/OpenClaw 2026.7.1-2; current physical acceptance is recorded in root `docs/CURRENT_STATE.md`.
