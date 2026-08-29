# CNX-20260830-149 — Proven-Launcher Product Reset Fresh-State Retry

## Verdict

`PASS`

Task 149 completed one real installed `cnxclaw.cmd reset` invocation using the launcher command shape proven by Task 147. Reset recreated the CNX state while preserving the installed program, skill and plugin release payload.

## Remote authority

- Repository: `https://github.com/funggier/CogentNexus-OpenClaw.git`
- Branch: `agent/v0.9.3-full-stabilization`
- Remote HEAD before execution: `341b2fef821288bfc898f9b8dc63f65c762f632f`
- State: `READY_FOR_HERMES`
- Task: `CNX-20260830-149`
- Execution mode: `LIVE_WINDOWS_PROVEN_LAUNCHER_RESET_FRESH_STATE_ACCEPTANCE`
- Accepted production SHA: `fb5781c1abd68280760bd5b3b4a65fabd8a60e58`
- Matching report was absent before publication.

`ACTIVE.md`, `STATUS.md`, and the complete Task-149 authority were read from a fresh GitHub checkout. The GitHub branch was the coordination authority; no stale local checkout was used for task decisions.

## Phase A — pre-reset read-only proof

Evidence root:

```text
C:/Users/CDQ-P/AppData/Local/Temp/cnx149-live-20260829T195649Z/evidence
```

The pre-reset live gate was coherent:

- installed launcher present;
- controller `MANAGED`, generation `6`, selected provider `ollama`;
- ownership verification passed;
- one canonical accepted CNX plugin, version `0.9.3`, enabled/loaded;
- Gateway healthy on `127.0.0.1:18789`;
- OpenClaw `2026.7.1-2`;
- Ollama installed/reachable/healthy/ready with four models;
- recovery and delivery checks `READY`, read-only, pending outbox `0`;
- SQLite `integrity_check=ok`;
- semantic counts all zero: `tickets=0`, `ticket_events=0`, `cnx_direct_model_call=0`, `cnx_direct_recovery=0`, `cnx_assistant_delivery=0`, `ticket_outbox=0`, `cnx_sessions=0`;
- Dashboard semantic Sends `0`.

Pre-reset durable file evidence:

- controller creation UTC: `2026-08-29T18:33:32.6108197Z`;
- controller last-write UTC: `2026-08-29T18:33:32.6108197Z`;
- controller length: `432` bytes;
- controller SHA-256: `84B923F37D0E48CD0B077DA1F675E99D356A6CC1E5CBDF0A3B7078EBBC67414B`;
- controller file ID: `0x0000000000000000000500000037b8f1`;
- SQLite creation UTC: `2026-08-29T18:29:40.7071888Z`;
- SQLite last-write UTC: `2026-08-29T18:32:30.8598807Z`;
- SQLite length: `159744` bytes;
- SQLite SHA-256: `5641415b27d49829401fecc4f016be515f1d93fb5229b29d7afd77461ccdaacc`;
- SQLite file ID: `0x0000000000000000000300000037b8f4`.

Installed provenance captured before reset:

- plugin fingerprint: `12c6d1b5b6ffd938353dd60c5d6190c34a609663369f619ff4fc7cbd176119e0`;
- installed `namespace_ownership.py` SHA-256: `10DDA985E6D4553A73A8CDD3EF7F660937482C3EF0C2D2DA8D15BCBFE8D39B66`;
- launcher SHA-256: `F53DF28F2A7EE7FC43C65BA2C48770ED9B7ED3E7B14D3C762F957BD017B90F10`.

## Phase B — harmless stdin qualification

The exact non-PTY process mechanism planned for reset was qualified with a temporary harmless Python child:

- `subprocess.Popen` with redirected stdin/stdout/stderr;
- exactly one lowercase `y` line written;
- stdin closed after the line;
- captured stdout contained `received=y`;
- captured stderr empty;
- true child exit code `0`;
- child did not import or mutate CNX/OpenClaw state.

Evidence: `b01-harness-qualification.json`.

## Phase C — product reset

The installed launcher was invoked exactly once using the required command form:

```text
cmd.exe /d /c C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd reset
```

Execution evidence:

- reset invocation count: `1`;
- confirmation input: exactly one lowercase `y` line;
- stdin closed after the line;
- stdout/stderr captured;
- product prompt reached: `true`;
- confirmation accepted: `true`;
- exit code: `0`;
- output: `COGENTNEXUS-OPENCLAW RESET: PASS`;
- reported state: `fresh-install MANAGED`;
- provider: `ollama`;
- no second reset;
- no uninstall, install, reinstall, clean-reinstall helper or manual deletion.

The reset output showed the expected transactional passthrough handoff, state reset, return to `MANAGED`, startup adapter installation, Gateway restart and healthy Ollama-preserving lifecycle. Ollama was already healthy and was not changed.

Evidence: `c01-reset-run.json`.

## Phase D — post-reset fresh-state proof

Post-reset read-only evidence proved program/provenance preservation:

- launcher remained present with unchanged SHA-256;
- workspace skill remained present;
- canonical plugin remained present and singular;
- plugin inventory contained exactly one `cogentnexus-openclaw` identity;
- plugin version remained `0.9.3`, `enabled=true`, `status=loaded`;
- plugin root remained canonical/non-reparse;
- plugin fingerprint remained exactly `12c6d1b5b6ffd938353dd60c5d6190c34a609663369f619ff4fc7cbd176119e0`;
- installed ownership-helper SHA-256 remained exactly `10dda985e6d4553a73a8cdd3ef7f660937482c3ef0c2d2da8d15bcbfe8d39b66`;
- ownership verification passed.

State recreation evidence:

- controller generation changed from `6` to `3`;
- controller `updatedAt` became `2026-08-29T20:01:34.926614+00:00`;
- controller creation UTC became `2026-08-29T20:02:35.5728719Z`;
- controller file ID changed from `0x0000000000000000000500000037b8f1` to `0x0000000000000000000800000037b8f2`;
- controller post-reset SHA-256: `562B945C29073E8FB0AD2B9F11044E89E097AFC5BDFE2E1C025518384CE4F111`;
- SQLite creation UTC became `2026-08-29T19:59:42.3579762Z`;
- SQLite last-write UTC became `2026-08-29T20:01:40.1192091Z`;
- SQLite file ID changed from `0x0000000000000000000300000037b8f4` to `0x0000000000000000000400000037b8f0`;
- SQLite post-reset SHA-256: `a95553884f53bffd1d7569d5efa9c5a1c8e34dbe0e3bb5fa079c3ad4ea6ad163`;
- SQLite length remained `159744` bytes;
- `integrity_check=ok`;
- all semantic counts remained zero: `tickets=0`, `ticket_events=0`, `cnx_direct_model_call=0`, `cnx_direct_recovery=0`, `cnx_assistant_delivery=0`, `ticket_outbox=0`, `cnx_sessions=0`.

Runtime and native preservation proof:

- controller returned to `MANAGED`;
- desired Gateway/provider state was `running`;
- selected provider was Ollama with selection source `reset`;
- Gateway was healthy, loopback-only on `127.0.0.1:18789`;
- OpenClaw remained `2026.7.1-2`;
- Ollama remained installed/reachable/healthy/ready with four models;
- recovery check was `READY`, read-only, with no active incident;
- delivery check was `READY`, read-only, pending outbox `0`;
- expected CNX supervisor and OpenClaw Gateway tasks remained coherent;
- transaction/residue scan found `0` matching reset/install/rollover transaction files;
- Dashboard semantic Sends remained `0`.

## Side-effect accounting

- reset invocations: `1`;
- reset confirmations: `1` lowercase `y` line;
- uninstall invocations: `0`;
- install/reinstall invocations: `0`;
- Dashboard semantic Sends: `0`;
- manual semantic/database mutation: `0`;
- manual state deletion: `0`;
- manual plugin/controller/ownership normalization: `0`;
- reset retries: `0`;
- crash/recovery injection: `0`;
- unrelated process/service/task mutation: `0`;
- credentials/secrets disclosed: `0`;
- merge/tag/release/force-push: `0`.

## Unproven items

None of the Task-149 PASS criteria remain unproven. This task did not perform semantic Dashboard acceptance, by explicit authorization.

## Completion

All Task-149 gates passed. This is the only requested report publication. Stop for independent ChatGPT review.
