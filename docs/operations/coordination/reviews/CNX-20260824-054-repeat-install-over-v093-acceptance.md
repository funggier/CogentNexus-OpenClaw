# Review — CNX-20260824-054 Repeat v0.9.3 Install-Over

Decision: `ACCEPT`

Disposition: `ACCEPT_BLOCKER_PLUGIN_GENERATION_AMBIGUITY`

Reviewed report:

`docs/operations/coordination/reports/CNX-20260824-054-repeat-install-over-v093-acceptance.md`

Report commit:

`4310dcac4de90a383a85e0c48d45914c18cf6f76`

Report result:

`BLOCKED_INSTALLER_EXIT_UNOBSERVED`

## Accepted findings

- Publication fence passed: the report commit added exactly the Task 054 report path.
- Essential preflight proved a coherent healthy Task 050-prefix upgrade state.
- The installer was invoked exactly once and entered its supported install-over body.
- The Task 051 skill and corrected help files were installed successfully.
- OpenClaw `plugins install --force` created a new generated npm project while the prior manifest-owned project remained.
- Ownership resolution correctly rejected the resulting two exact v0.9.3 payload roots as ambiguous.
- The installer stopped before ownership recreation and MANAGED re-enable, leaving a safe partial PASSTHROUGH/startup-disabled state.
- Gateway, Ollama, four models, SQLite, policy, Task 049 backup, unrelated plugins/data, and excluded systems remained healthy/preserved.
- No retry, manual repair, destructive action, or unrelated mutation occurred.
- The retained wrapper failed to preserve a numeric child exit code and must not be reused.

## Root cause

The product defect is in plugin generation rollover, not in the ownership ambiguity guard. The installer assumes `openclaw plugins install --force` replaces or removes the prior managed npm project. On the observed OpenClaw version it creates a new generation and leaves the prior payload root. The subsequent exact resolver therefore sees two valid candidates and fails closed as designed.

The evidence-wrapper defect is independent: its terminated process record contains `observedExitCode: null`. Installer failure semantics are proved by stderr and partial state, but the numeric child exit must remain unasserted.

## Decision

Accept the blocker report. Do not weaken `resolve_installed_plugin`, accept equal-fingerprint duplicates, delete both roots, or rerun the installer in the current ambiguous state.

The next repository task must implement and test an ownership-safe generation rollover plus a narrowly gated recovery primitive for the current exact two-root partial state. Live repair will be a separate task after review.

