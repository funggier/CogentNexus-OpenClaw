# CNX-20260920-437 — Windows UTF-8 Subprocess Boundary and Gateway Temp Compatibility Repair

Status: `COMPLETE`

Parent: `CNX-20260920-436`

## Trigger

The CNX-436 live `cnxclaw enable` attempt crossed the prior 30-second lifecycle-start readiness defect and committed MANAGED generation `109`, but later failed and rolled back safely to PASSTHROUGH generation `108`.

Terminal cause:

`the JSON object must be str, bytes or bytearray, not NoneType`

The same process emitted a Python background reader failure:

`UnicodeDecodeError: 'charmap' codec can't decode byte 0x81 ...`

The failing reader was Python 3.11 `subprocess.py::_readerthread`, using the Windows ANSI/CP1252 text decoder.

The rollback remained safe:

- startup disable: PASS;
- plugin disable: PASS;
- lifecycle cancel: PASS;
- policy restore: PASS;
- native Gateway restore: healthy after 5 attempts / approximately 72.032 seconds;
- controller restored to PASSTHROUGH generation `108`.

## Root cause

The active command chain contains nested captured subprocess boundaries:

`cnxclaw.py -> host_control.py -> host_legacy_v094.py -> OpenClaw CLI`

Those boundaries used:

`subprocess.run(..., capture_output=True, text=True)`

without an explicit encoding/error policy.

On Windows, the parent reader can therefore use the locale ANSI codec even though OpenClaw/Node and the nested Python surfaces emit UTF-8.

A UTF-8 continuation byte `0x81` is undefined in CP1252. The reader thread can fail, leaving a captured stream as `None`.

The Host then had direct parser calls such as:

`json.loads(result.stdout)`

so a decode failure became the observed secondary `TypeError` on `NoneType`.

## TDD RED

Added:

`tests/test_task437_windows_subprocess_utf8_boundary.py`

Initial result:

- legacy Host runner explicit UTF-8 contract: FAIL;
- host-control runner explicit UTF-8 contract: FAIL;
- cnxclaw host runner explicit UTF-8 contract: FAIL;
- missing stdout controlled JSON failure: FAIL with the exact live `TypeError`.

Total initial RED: `4 failed`.

## Production repair

Changed:

- `skills/cogentnexus-openclaw/scripts/host_legacy_v094.py`;
- `skills/cogentnexus-openclaw/scripts/host_control.py`;
- `skills/cogentnexus-openclaw/scripts/cnxclaw.py`.

Captured command boundaries now explicitly use:

- `encoding="utf-8"`;
- `errors="replace"`;
- `text=True`.

The legacy Host also normalizes `str | bytes | None` before JSON parsing for:

- Gateway RPC output;
- default agent list;
- configured main session key;
- session list;
- session verification.

The cnxclaw boundary normalizes absent stdout/stderr before relaying/parsing.

Interactive passthrough remains unchanged.

## Real-byte regression

A regression test executes a child that writes the Thai character:

`ก`

as raw UTF-8 bytes.

Its UTF-8 representation contains byte `0x81`, the same byte class that triggered the live CP1252 reader failure.

The repaired runner decodes it correctly as `ก` without a reader-thread exception.

Focused GREEN:

- `5/5 PASS`.

Affected Host/session regression:

- `55 PASS`;
- `2 deselected`.

The two deselected cases are independent current-repository issues:

1. a non-hermetic gateway-hang unit test observes the live OpenClaw `gateway_boot_lifecycle` database and sees active startup grace;
2. a historical wiring test expects `startup_v091.py` while current production is already wired to `startup_v092.py`.

Neither affected file is changed by CNX-437.

Static gates:

- Python 3.11 compile: PASS;
- Python 3.14 compile: PASS;
- `git diff --check`: PASS.

## Gateway temp/storage continuation

During the same qualification, OpenClaw Gateway was found to hardcode:

`TMPDIR=C:\Users\CDQ-P\AppData\Local\Temp`

in:

`C:\Users\CDQ-P\.openclaw\gateway.cmd`

The live Gateway service wrapper was backed up to T: and its process-local:

- `TMPDIR`;
- `TEMP`;
- `TMP`

were redirected to:

`T:\CogentNexus\CogentNexus-OpenClaw\temp\openclaw-gateway`

without changing Windows user/machine TEMP.

Live storage proof after Gateway restart:

- C: `openclaw-plugin-build-*` count: `0`;
- T: new `openclaw-plugin-build-*` directories are created under the redirected root.

The backup is under:

`T:\CogentNexus\CogentNexus-OpenClaw\diagnostics\CNX-20260920-437\`

## Restart-loop breaker observation

Repeated qualification restarts caused OpenClaw 9.5's native Gateway crash-loop breaker to suppress Discord/channel auto-start.

Local OpenClaw source documents:

- threshold: 3 unclean boots;
- window: 300000 ms;
- self-clear only after the full window drains;
- supported manual recovery surface: `openclaw gateway call channels.start`.

No OpenClaw DB rows will be manually deleted to bypass the breaker.

## Live qualification plan

1. freeze exact CNX-437 implementation commit;
2. allow the native 5-minute restart-loop window to drain with no further restarts;
3. recover/verify Discord through supported OpenClaw channel start behavior;
4. deploy the exact candidate through the supported install path;
5. rerun `cnxclaw enable`;
6. require:
   - no CP1252/reader-thread exception;
   - no `json.loads(None)` failure;
   - CNX-436 lifecycle start uses 180-second bounded readiness;
   - MANAGED state remains committed;
   - plugin active;
   - supervisor active;
   - Gateway/Discord healthy;
7. continue final Discord Ticket-first acceptance only after runtime qualification is GREEN.

## Live qualification result

Supported install-over from exact candidate `d67e86ae212222e62bd6eba2e194c1fd78fcf785` completed with terminal exit `0`.

Observed live evidence:

- no CP1252/reader-thread exception;
- no `json.loads(None)` failure;
- no transactional rollback;
- CNX-436 lifecycle start used the 180-second bounded readiness contract;
- MANAGED generation `109` remained committed;
- session bootstrap succeeded;
- CNX plugin loaded in the live Gateway;
- supervisor enabled with `LastTaskResult=0`;
- Gateway healthy;
- Discord ready/connected;
- C: `openclaw-plugin-build-*` count remained `0` while new build temp was created on T:.

Report:

`docs/operations/coordination/reports/CNX-20260920-437-windows-utf8-subprocess-and-gateway-temp-compatibility-repair-report.md`

## Final classification

`WINDOWS_UTF8_SUBPROCESS_AND_GATEWAY_TEMP_COMPAT_GREEN`
