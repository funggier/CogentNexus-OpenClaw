# Review — CNX-20260826-072 Bounded Cleanup, Fresh Install, Owned Runtime and No-Flash Live Acceptance

Decision: `ACCEPT`

Disposition: `ACCEPT_LIVE_INSTALL_OWNED_RUNTIME_NO_FLASH_WITH_PREFLIGHT_FOLLOWUP`

Reviewed report HEAD: `19d3ae6bf090e58aaf9b45da52fe3ae6f4f7d11a`

Accepted install source: `9df671670908241486afe2badf8a7f221410c6f8`

## Accepted live evidence

1. Task-066 residue was re-proven before mutation and attributed to exactly the two pre-marker failed-install roots.
2. Cleanup deleted exactly those two roots once and preserved shared parents/unrelated OpenClaw state.
3. One normal fresh install from exact accepted source `9df6716...` completed with no skip/link shortcuts and no source edit.
4. The fresh transaction began before fresh residue-capable mutation, recorded bounded paths, ownership creation/verification completed, and the transaction reached committed state.
5. Durable runtime authority is under `%LOCALAPPDATA%\CogentNexus-OpenClaw\runtime\python`; launcher uses the owned foreground `python.exe`; Scheduled Task uses the owned background `pythonw.exe`; durable Hermes/Codex/temp bindings were absent.
6. Five distinct natural PT1M ticks were observed with `LastTaskResult=0`, no CNX-causal `conhost.exe`, no console-Python trampoline, and no cmd/PowerShell scheduled wrapper. Flash classification `NO_FLASH_MULTI_TICK_PROVEN` satisfies the >=3 natural-tick gate.
7. Final state is MANAGED, Gateway/dashboard healthy, Ollama inventory unchanged, exactly one v0.9.3 plugin active, accepted managed config present, ownership verification passes, AGENTS managed block appears exactly once with the accepted stripped baseline, and SQLite integrity is `ok`.
8. No product semantic user-message/LLM smoke occurred.
9. Publication fence passes: coordination HEAD `37b5597...` to report HEAD `19d3ae6...` is one report-only commit adding only the Task-072 report.

## Independent follow-up finding — not a Task-072 live acceptance blocker

The Task-072 report describes the install log's recovery-preflight error as refusing the old Task-066 residue. The phase ordering shows that residue had already been removed in Phase B before the Phase-C installer invocation.

Independent source inspection explains the message:

- `namespace_ownership.py::recovery_preflight()` raises whenever there is no transaction marker, before distinguishing a truly clean fresh inventory from unmarked partial residue.
- Therefore a clean markerless fresh state emits `no valid incomplete install transaction marker...` even when there is no residue.
- `scripts/install.ps1` invokes `recovery-preflight` but currently only handles exit code 0; a nonzero recovery result is not explicitly rejected before classification.

The later production classifier still returned coherent `fresh`, the fresh transaction began, the installation completed, ownership verified, and the installed runtime/no-flash evidence is unaffected. Therefore this source correctness issue does not invalidate Task 072's live-runtime acceptance.

However, it is a known installer defect and must be corrected before final semantic/release-parity acceptance. A clean fresh state should be an explicit successful preflight outcome, while unmarked partial residue and any genuine recovery failure must remain fail-closed and must stop the installer rather than being silently ignored.

## Successor

Open a source-only TDD correction task before semantic acceptance. After that correction is accepted, perform a bounded supported install-over so the live machine matches the corrected release source, re-prove runtime/no-flash health, then perform the final semantic Ticket -> Ollama -> durable delivery gate.