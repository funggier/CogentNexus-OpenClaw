# Independent Review — CNX-20260828-121 v0.9.3 Real-Windows Lifecycle Acceptance — Attested Re-entry

## Verdict

`ACCEPTED INCOMPLETE — INSTALL-OVER SUCCEEDED ONCE; POST-INSTALL VERIFICATION HARNESS FAILED; PRODUCT FAILURE NOT PROVEN; INSTALL-OVER IS CONSUMED AND MUST NOT BE REPLAYED`

## Accepted evidence

Task 121 correctly used the production-equivalent attested classifier. The candidate plugin fingerprint matched the exact accepted candidate and the classifier returned a coherent interrupted-rollover/re-entry upgrade shape:

- `mode=upgrade`;
- `pendingRollover=false`;
- `pluginAlreadyExact=true`;
- `interruptedRolloverReentry=true`;
- no legacy namespace.

The provider-neutral install-over command then ran exactly once and returned exit code `0` with `CogentNexus-OpenClaw v0.9.3 installation completed successfully.` The installer runtime handoff/reload also returned success according to the Task-121 report.

## First failed acceptance boundary

The failure occurred after the installer returned success, in an executor-created post-install verification wrapper. The wrapper used commands that could enter interactive modes in the non-TTY execution environment:

- an incorrectly resolved Python invocation entered the Python REPL;
- an OpenClaw invocation selected the TUI and reported that an interactive TTY was required;
- an Ollama invocation likewise entered an interactive surface and timed out.

This is a verification-harness failure. It is not evidence that the installer body, ownership convergence, Gateway, SQLite, provider runtime, or installed product state failed.

Because the required postconditions were not successfully verified, Task 121 correctly stopped before `reset` and all later disruptive phases.

## One-shot accounting

Consumed:

- install-over: **1 / 1** — consumed; never replay.

Not consumed:

- reset: `0`;
- uninstall: `0`;
- fresh reinstall after uninstall: `0`;
- stop: `0`;
- start: `0`;
- restart: `0`;
- recovery harness: `0`.

No Dashboard semantic Send occurred.

## Required successor

A successor must begin from the current post-install machine state and recover only the missing read-only proof. It must not run install-over again.

The successor should use only explicit non-interactive probes with fully resolved executable/script paths and bounded capture. Examples include:

- installed `cnxclaw.cmd status` and `cnxclaw.cmd check system`;
- `openclaw plugins list --json`;
- explicit Gateway status command, never bare `openclaw`;
- `ollama list` / `ollama ps`, never bare `ollama`;
- explicit `namespace_ownership.py verify` with a fully resolved script path;
- explicit Python `-c` for SQLite `PRAGMA integrity_check`, never bare `python`.

Only if those read-only probes prove the current post-install state coherent may the successor continue from the first unconsumed disruptive phase: `reset`.

If current state cannot be proven coherent, stop without mutation. Do not normalize, repair, or replay install-over.

## Candidate and live boundary

The exact candidate remains `01d08cd7c82f542c821e3a60f7fffa036efb1d75`, artifact `9691451156`. No source defect or candidate substitution is established by Task 121.
