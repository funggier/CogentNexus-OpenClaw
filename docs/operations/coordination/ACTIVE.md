# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `TASK218_CROSS_PLATFORM_PAYLOAD_DETERMINISM_TDD_REPAIR`
Current disposition: `TASK217_NEWLINE_VARIANCE_ACCEPTED__TDD_DETERMINISTIC_PAYLOAD_REPAIR_REQUIRED`
Task ID: `CNX-20260901-218`
Parent task: `CNX-20260901-217`
Repair parent: `CNX-20260831-198`
Parent umbrella: `CNX-20260831-188`
Updated: 2026-09-01 ICT
Executor: Hermes / repository engineer
Coordinator / final reviewer: ChatGPT

## Published authority

Public `v0.9.3` remains immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

No Release/tag/asset mutation is authorized.

## Repair base

Task-207 semantic repair base remains:

`27fe0181b3b65d555a3b0cc8354f6f7945c21c0b`

Historical payload identities:

```text
Ubuntu CI / retained Task-207 payload: d0677581d60d3d5535c65e3261dae6f50d7aeb245b8680adac0cace4c040643b
Windows Task-216 payload:             3b86b13f6d39996f18687510ab65aa4bba46bdf8d80b1aaeef14fe8d199eb3ed
```

These are diagnostic references only. Task 218 must establish a **new exact candidate SHA and package fingerprint** after the deterministic-build repair.

## Task 217 accepted result

Report:

`reports/CNX-20260901-217-task216-cross-platform-plugin-fingerprint-provenance-adjudication.md`

Review:

`reviews/CNX-20260901-217-task216-cross-platform-plugin-fingerprint-provenance-adjudication-review.md`

Accepted disposition:

`ACCEPT_PASS_NEWLINE_VARIANCE_PROVEN__TDD_DETERMINISTIC_PAYLOAD_REPAIR_REQUIRED`

Accepted facts:

- CI and Windows installable path sets were equal at 192 files;
- exactly 43 generated `dist` files differed;
- all differences were CRLF/LF-normalizable byte differences;
- normalizing Windows generated payload bytes to LF reproduced historical CI `d0677581...` exactly;
- explicit `tsc --newLine lf` alone did not change the Windows build, so a compiler-flag-only repair is not accepted;
- the fingerprint algorithm remains byte-exact and must not be weakened;
- live Windows product remained PASSTHROUGH on the old generation, Gateway healthy, delivery/recovery READY, with no installer/lifecycle/SQLite/Discord mutation.

## Active Task 218

Hermes must execute:

`tasks/CNX-20260901-218-task217-cross-platform-payload-determinism-tdd-repair.md`

Task 218 is repository/build repair only.

Required flow:

1. create a platform-independent RED regression that builds logically identical LF-source and CRLF-source fixtures through the real build/package path and requires identical payload identity;
2. prove the pre-fix test fails for generated newline variance and commit the test alone;
3. implement minimal post-emit `dist` LF canonicalization without modifying fingerprint semantics;
4. prove focused GREEN + full plugin/build/validation GREEN;
5. obtain authoritative CI for the exact new GREEN candidate and retain a new package proof;
6. fresh-build that exact candidate on Windows and require exact fingerprint/path/byte equality with the new CI package proof;
7. preserve live runtime read-only and publish the Task-218 report.

A `.gitattributes`-only fix is insufficient. Do not accept multiple fingerprints. Do not normalize inside `_plugin_payload()`.

## Discord budget

Task 218 authorizes `0 Discord Sends`.

## Hard fence

No installer/install-over, no `cnxclaw` lifecycle action, no live OpenClaw plugin/config mutation, no Gateway restart, no live ownership/staging/transaction/SQLite mutation, no provider/model substitution, no Release/tag mutation, no force push, and no Discord traffic. Repository test/build/package repair and isolated build validation only.
