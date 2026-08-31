# CNX-20260830-148 — Product Reset Fresh-State Acceptance

## Verdict

`FAIL_RESET`

The authorized reset attempt did not reach the installed product's confirmation prompt because the executor's Windows `cmd.exe` quoting was malformed. The task's no-retry fence is honored; no second reset, repair, reinstall, or manual normalization was performed.

## Remote authority

- Repository: `https://github.com/funggier/CogentNexus-OpenClaw.git`
- Branch: `agent/v0.9.3-full-stabilization`
- Remote HEAD before execution: `0c20302e9718aa243e830a00be44644997463566`
- Active task: `CNX-20260830-148`
- State: `READY_FOR_HERMES`
- Execution mode: `LIVE_WINDOWS_PRODUCT_RESET_FRESH_STATE_ACCEPTANCE`
- Accepted production SHA: `fb5781c1abd68280760bd5b3b4a65fabd8a60e58`
- Matching report was absent before publication.

`ACTIVE.md`, `STATUS.md`, and the complete Task-148 authority were read from the freshly fetched GitHub branch. The remote branch, not local/chat history, was used as coordination authority.

## Phase A — read-only pre-reset proof

Evidence root:

```text
C:/Users/CDQ-P/AppData/Local/Temp/cnx148-live-20260829T193321Z/evidence
```

The pre-reset gate was coherent:

- launcher existed and exposed `reset`;
- ownership verification passed;
- controller was `MANAGED`, generation `6`, with `updatedAt=2026-08-29T18:33:32.610819+00:00`;
- plugin identity was singular, canonical and enabled/loaded at version `0.9.3`;
- OpenClaw was `2026.7.1-2`;
- Gateway was healthy on loopback `127.0.0.1:18789`;
- Ollama was installed, reachable, healthy and ready with four models;
- recovery and delivery checks were `READY`, read-only, with pending outbox `0`;
- supervisor and Gateway scheduled tasks were coherent;
- SQLite was opened read-only and had `integrity_check=ok`;
- semantic counts were all zero: `tickets=0`, `ticket_events=0`, `cnx_direct_model_call=0`, `cnx_direct_recovery=0`, `cnx_assistant_delivery=0`, `ticket_outbox=0`, `cnx_sessions=0`;
- Dashboard semantic Sends were `0`.

Baseline durable file evidence:

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

Installed provenance baseline:

- plugin fingerprint: `12c6d1b5b6ffd938353dd60c5d6190c34a609663369f619ff4fc7cbd176119e0`;
- installed `namespace_ownership.py` SHA-256: `10dda985e6d4553a73a8cdd3ef7f660937482c3ef0c2d2da8d15bcbfe8d39b66`;
- launcher SHA-256: `F53DF28F2A7EE7FC43C65BA2C48770ED9B7ED3E7B14D3C762F957BD017B90F10`.

## Phase B — redirected-stdin qualification

A harmless temporary Python child was run with the exact non-PTY subprocess mechanism planned for reset:

- redirected stdin/stdout/stderr through `subprocess.Popen`;
- exactly one line `y` written;
- stdin closed by `communicate`;
- captured stdout contained `received=y` after the prompt;
- stderr was empty;
- child exit code was `0`;
- child did not import or mutate CNX/OpenClaw state.

The first qualification wrapper had an overly strict assertion because it compared the entire stdout against `received=y`, while Python's prompt was also captured. That assertion was corrected to check the semantic suffix. The harmless child was then run again and qualification passed. No product command was invoked during the failed assertion attempt.

Final qualification evidence: `b01-harness-qualification.json`.

## Phase C — reset attempt and first failure boundary

The installed launcher reset was attempted exactly once through the qualified non-PTY mechanism:

```text
cmd.exe /d /s /c call "C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd" reset
```

Execution evidence:

- reset attempt count: `1`;
- confirmation input written by harness: exactly one lowercase `y` line;
- stdout/stderr captured;
- exit code: `1`;
- product confirmation prompt reached: `false`;
- product reset accepted: `false`.

The actual failure was command resolution before the product launcher ran:

```text
'\"C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd\"' is not recognized as an internal or external command,
operable program or batch file.
```

The process did not reach `Continue? [y/N]:`. The full retained record is `c01-reset-run.json`.

Per Task 148, this is the first reset failure boundary. No retry was attempted.

## Post-failure read-only proof

Post-failure probes were run without lifecycle mutation. They show no evidence that reset began:

- controller remained generation `6` with the same `updatedAt`;
- controller creation time, last-write time, length, hash and file ID remained unchanged;
- SQLite creation time, last-write time, length, hash and file ID remained unchanged;
- SQLite remained `integrity_check=ok` with all semantic counts zero;
- launcher, workspace skill and canonical plugin remained present;
- ownership verification still passed;
- plugin remained version `0.9.3` and exact accepted provenance was preserved;
- controller remained `MANAGED` with Ollama selected/running;
- Gateway remained healthy and OpenClaw remained `2026.7.1-2`;
- recovery and delivery remained `READY`, with pending outbox `0`;
- Dashboard semantic Sends remained `0`.

The post-failure database record is `d09-post-db.json`; post-failure identities are in `d08-post-identities.json`.

## Side-effect accounting

- reset attempts: `1`;
- reset attempts reaching product prompt: `0`;
- reset confirmation lines: `1` written to failed command process;
- uninstall attempts: `0`;
- install/reinstall attempts: `0`;
- Dashboard semantic Sends: `0`;
- Ticket/workflow/outbox/delivery/recovery/database manual mutation: `0`;
- manual CNX live-state deletion: `0`;
- manual plugin/controller/ownership normalization: `0`;
- reset retry: `0`;
- crash/recovery injection: `0`;
- unrelated process/service/task mutation: `0`;
- credentials/secrets disclosed: `0`;
- merge/tag/release/force-push: `0`.

## Unproven items

Because reset did not reach the product:

- state-root or durable database recreation is not proven;
- changed post-reset file identity/timestamp is not available;
- reset-specific generation/state recreation is not proven;
- reset-specific preservation behavior is not proven beyond unchanged post-failure read-only state.

This report records the executor command-boundary failure honestly. No product reset defect is established by this attempt, and no retry is authorized by Task 148.
