# CNX-20260828-122 — Post-Install Verification Recovery and Lifecycle Continuation

## Verdict

**BLOCKED — the required explicit non-interactive read-only recovery gate could not prove the current post-install state; no new destructive mutation was executed.**

Task-121 install-over remains consumed and was not replayed.

## Task-121 boundary accepted

The prior independent review accepted that:

- the attested classifier passed;
- install-over executed exactly once and returned exit code `0`;
- reset, uninstall, reinstall, stop/start/restart, and recovery did not execute;
- the Task-121 verification wrapper was the first incomplete boundary.

Task 122 therefore began with read-only recovery only.

## Fresh read-only evidence

Evidence root:

`C:\Users\CDQ-P\AppData\Local\Temp\cnx122-readonly-recovery-20260828`

Primary evidence:

`a01-explicit-readonly-probes.txt`

The probe used explicit executable paths and did not call the consumed install-over or any lifecycle mutation:

- `C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd`
- `C:\Users\CDQ-P\AppData\Roaming\npm\openclaw.cmd`
- `C:\Users\CDQ-P\AppData\Local\Programs\Ollama\ollama.exe`
- owned runtime Python path under `C:\Users\CDQ-P\AppData\Local\CogentNexus-OpenClaw\runtime\python\Scripts\python.exe`

## Read-only gate results

### CNX launcher

The explicit `cnxclaw.cmd` calls returned exit code `0`, but the installed launcher output contained:

```text
CogentNexus-OpenClaw v0.9.3 (Ollama-only)
Ollama is the only supported inference provider in v0.9.3.
Explicit '--provider ollama' remains accepted for compatibility.
```

This is inconsistent with the frozen provider-neutral candidate and prevents treating the current post-install state as proven coherent.

### OpenClaw probes

The explicit `openclaw.cmd` calls for `--version`, `plugins list --json`, and `gateway status` did not yield the required non-interactive evidence. They reported:

```text
OpenClaw TUI needs an interactive TTY. Use `openclaw agent --local ...` for automation.
```

### Ollama probes

The explicit Ollama executable was resolved, but the selected invocation entered an interactive UI and the bounded probe did not complete. No provider mutation was attempted.

### Complete post-install proof

Because the required non-interactive probes did not produce authoritative version, inventory, gateway, provider, ownership, and SQLite evidence, the current state cannot be accepted as coherent under Task-122's gate. This report does not claim that the live installation is corrupt; it records that the required proof was not obtained.

## Mutation ledger

| Operation | Task-122 executions |
|---|---:|
| Task-121 install-over replay | 0 |
| reset | 0 |
| uninstall | 0 |
| fresh reinstall | 0 |
| stop | 0 |
| start | 0 |
| restart | 0 |
| recovery harness | 0 |
| manual cleanup/normalization | 0 |
| provider/runtime/config mutation | 0 |
| Dashboard semantic Send | 0 |

The only live mutation preceding this task is the already-consumed Task-121 install-over, which is not replayed here.

## Required successor work

A successor task must resolve the explicit-command and installed-launcher verification boundary using known non-interactive entry points and must explain the provider-neutral versus Ollama-only launcher discrepancy without manually editing or normalizing live state. It must not proceed to reset, uninstall, reinstall, or lifecycle controls until a fresh authoritative read-only gate passes.

## Publication

This report is the only file in the report commit. Execution stops here for independent review. The final Dashboard durable-delivery task was not created or executed.
