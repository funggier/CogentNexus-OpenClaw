# CNX-20260920-437 — Windows UTF-8 Subprocess Boundary and Gateway Temp Compatibility Repair Report

Status: `COMPLETE`

Classification:

`WINDOWS_UTF8_SUBPROCESS_AND_GATEWAY_TEMP_COMPAT_GREEN`

Branch:

`cnx-357-openai-dashboard-ticket-first-requalification-v2`

Implementation commit:

`d67e86ae212222e62bd6eba2e194c1fd78fcf785`

## Trigger

After CNX-436 crossed the prior readiness defect, a live `cnxclaw enable` attempt failed later with:

`the JSON object must be str, bytes or bytearray, not NoneType`

The same process emitted:

`UnicodeDecodeError: 'charmap' codec can't decode byte 0x81`

from Python's subprocess reader thread on Windows.

The transaction safely rolled back to PASSTHROUGH generation 108.

## Root cause

Nested captured subprocess boundaries used `text=True` without explicit encoding/error policy:

`cnxclaw.py -> host_control.py -> host_legacy_v094.py -> OpenClaw CLI`

Windows therefore used the locale ANSI decoder for output that can contain UTF-8. A UTF-8 continuation byte such as `0x81` can be invalid under CP1252, killing the background reader and leaving a captured stream as `None`. Direct `json.loads(result.stdout)` calls then produced the observed secondary TypeError.

## Repair

Changed:

- `skills/cogentnexus-openclaw/scripts/host_legacy_v094.py`;
- `skills/cogentnexus-openclaw/scripts/host_control.py`;
- `skills/cogentnexus-openclaw/scripts/cnxclaw.py`.

Captured subprocess boundaries now explicitly use:

- `encoding="utf-8"`;
- `errors="replace"`;
- `text=True`.

The Host also normalizes missing/bytes/text streams before JSON parsing for Gateway RPC, agent-list and session bootstrap outputs.

Interactive passthrough behavior is unchanged.

## TDD / repository validation

New test:

`tests/test_task437_windows_subprocess_utf8_boundary.py`

Initial RED:

- 4/4 expected failures, including the exact `json.loads(None)` TypeError.

GREEN:

- focused CNX-437: 5/5 PASS;
- includes a real child-process UTF-8 test writing Thai `ก`, whose UTF-8 byte sequence includes `0x81`;
- affected Host/session regression: 55 PASS, 2 deselected independent historical/non-hermetic cases;
- Python 3.11 py_compile: PASS;
- Python 3.14 py_compile: PASS;
- git diff --check: PASS.

Live/source SHA-256 parity:

- `host_legacy_v094.py`: `F0951D003542077C80AAE17E6E28FE2FCD782A2FBAE9021AF03C7D8F019A7817`;
- `host_control.py`: `6FB8FAFCF708CFE08D3A992ECF7F4F7950663853F9DDFE983149E808F9A3AB4E`;
- `cnxclaw.py`: `361444875D87288FF801C8E9222C716D1E881C4559B181C75B97E7DED1858E04`.

## OpenClaw Gateway temp compatibility

A separate live storage finding showed `C:\Users\CDQ-P\.openclaw\gateway.cmd` hardcoded its temp root to C:.

The live Gateway wrapper was backed up under:

`T:\CogentNexus\CogentNexus-OpenClaw\diagnostics\CNX-20260920-437\`

and its process-local `TMPDIR`, `TEMP`, and `TMP` were redirected to:

`T:\CogentNexus\CogentNexus-OpenClaw\temp\openclaw-gateway`

without changing Windows user/machine TEMP.

Post-install live proof:

- C: `openclaw-plugin-build-*` count = `0`;
- T Gateway temp contains current plugin-build directories;
- LConnect child TEMP/TMP remains on `T:\CogentNexus\CogentNexus-OpenClaw\temp\lconnect`;
- C: free space remains about 103.8 GB.

## Native restart-loop breaker

Repeated qualification restarts temporarily tripped OpenClaw 9.5's native crash-loop breaker.

Local OpenClaw implementation proved:

- threshold = 3 unclean boots;
- window = 300000 ms;
- breaker self-clears after the full window drains.

No DB row was manually deleted.

The breaker self-recovered through OpenClaw's supported logic; Discord then returned to ready/connected.

## Final live qualification

A supported install-over from exact candidate `d67e86ae...` completed with terminal exit `0`.

Live result:

- CNX-436 lifecycle start crossed 5 readiness attempts with `timeoutSeconds=180.0`;
- no UnicodeDecodeError;
- no `json.loads(None)`;
- no transactional rollback;
- MANAGED generation `109` remains committed;
- session bootstrap succeeded;
- CNX plugin enabled/activated and loaded by the Gateway;
- CNX supervisor enabled, hidden, LastTaskResult `0`;
- Gateway health GREEN;
- Discord ready/connected.

Post-install logs contain no new:

- `UnicodeDecodeError`;
- `the JSON object must be str, bytes or bytearray, not NoneType`;
- `transactional enable failed`;
- `native passthrough rollback executed`.

The only crash-loop-breaker log found is the earlier pre-install event at 08:58 local time.

## Result

The Windows subprocess decoding failure is repaired and live-qualified. Gateway/LConnect temporary build activity is also redirected away from C: while preserving OpenClaw's supported runtime behavior.

CNX-437 is COMPLETE.
