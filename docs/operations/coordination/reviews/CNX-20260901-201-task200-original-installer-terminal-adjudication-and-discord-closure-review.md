# CNX-20260901-201 Review — Task 200 Original Installer Terminal Adjudication and Discord Closure

Disposition: `ACCEPT_BLOCKED_INSTALLER_STILL_RUNNING__ROOT_CAUSE_DIAGNOSIS_REQUIRED`

## Authority

Reviewed from fresh GitHub state on 2026-09-01 ICT.

Task report:

`docs/operations/coordination/reports/CNX-20260901-201-task200-original-installer-terminal-adjudication-and-discord-closure.md`

Frozen repaired product candidate remains:

`9f4eaa429b2540540e7d6f6c2af99067960e45fb`

Expected installed plugin fingerprint:

`f82674172a3946e00ddcb3a94fd14c8476bf91abc11ed7d44b5fa53acb74eaf1`

Published `v0.9.3` remains immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

## Accepted Task-201 findings

Task 201 correctly remained read-only and established that:

1. PID `11704` is still the same PowerShell process observed during Task 200, based on PID, executable path, parent relation, command line, and exact retained creation time.
2. The original installer has not produced its terminal success line and no exit artifact exists.
3. The stdout/stderr streams have not advanced past the late install boundary recorded after `owned-runtime-ensure`, launcher creation, and a passthrough policy result.
4. The exact repaired plugin bytes are installed and fingerprint-match the frozen candidate.
5. Ownership verification passes.
6. OpenClaw/Gateway/Ollama/delivery/recovery/SQLite remain healthy.
7. Host authority remains `passthrough`, startup policy is disabled, and the plugin remains disabled; managed convergence therefore did not complete.
8. No human Discord Send occurred. The Task-198/200/201 human-send budget remains `0 / 1` consumed.
9. No installer replay, process termination, enable/disable/restart, reset, uninstall, reinstall, provider change, state mutation, source change, or publication mutation occurred.

Task-201 disposition `BLOCKED_INSTALLER_STILL_RUNNING` is therefore accepted.

## Source comparison

A known-good Task-159 install-over using the same late installer structure reached the same passthrough-policy output and then returned a successful `cnxclaw enable` result roughly three minutes later before completing the remaining gateway/supervisor/status checks.

Task 201 instead observed no additional output for an extended interval while the same root PowerShell process remained alive. This is now a genuine terminal-stall investigation, not merely a short observer window.

The exact installer invokes after the last observed policy output:

`cnxclaw_v093.py --root <state-root> enable`

The enable facade then traverses nested captured subprocess boundaries through `cnxclaw.py`, `host_control_v092.py`, `host_control_v091.py`, `host_control.py`, Host/Gateway/OpenClaw commands, and a forced Gateway process boundary.

The repository already contains a separate Windows acceptance lesson: `Start-Process -Wait` can wait on long-lived descendants rather than only the requested root process. That precedent is relevant as a process-wait hypothesis, but Task 201 does not contain enough descendant-tree evidence to accept that as this stall's root cause.

## Minimum next evidence

Before killing the stale installer or proposing a production fix, collect the process wait topology around the exact original PID:

- recursive descendants, not only the known conhost;
- command line/executable/creation time/parent for every descendant;
- two bounded samples of root/descendant CPU time, thread state/wait reason where available, handle count, stdout/stderr size/hash/mtime;
- current runtime state read-only;
- mapping of any surviving Python/Node/OpenClaw command line back to the exact source boundary.

No lifecycle or semantic mutation is needed for that diagnosis.

## Review result

Task 201 is accepted as a correct blocked stop. Task 198 remains open. A dedicated read-only Task 202 is required to locate the live wait boundary before any termination, cleanup, source repair, or Discord Send is authorized.
