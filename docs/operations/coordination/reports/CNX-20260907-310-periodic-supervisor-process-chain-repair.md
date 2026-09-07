# CNX-20260907-310 — Periodic supervisor process-chain repair

Disposition: `PASS_SOURCE_REPAIR_EXACT_SHA_CI_GREEN`
Completed UTC: 2026-09-07T21:31Z

## Candidate

- Exact source candidate: `79ddec2190b226b2f5cc906144a04859b3eca748`
- Branch: `agent/v0.9.3-full-stabilization`
- Production patch SHA-256 before commit: `26f1489795777ce4203c345e51dd848d6b945259cf8aab2dde2e4180bb78394a`
- Staged index tree: `2bf31fe7d4a4752ec2b61fde74069e6dbe691a6d`

## Root cause and repair

The PT1M Windows Scheduled Task entered `host_control_v092.py`, which delegated to another Python Host process even when the composed supervisor could execute in the existing process. The repair:

- adds a per-call periodic runner seam to `host_control_v091.py` while preserving standalone v0.9.1 delegation;
- routes only v0.9.2 `supervisor tick` through the stable composed `host_v092.base.supervisor_tick` function in-process;
- preserves Host JSON/error exit behavior;
- supports both `--root PATH` and argparse-supported `--root=PATH` pre-parsing;
- keeps absent-controller periodic initialization in-process and skips managed-plugin repair until controller state exists;
- leaves non-periodic lifecycle/controller behavior unchanged.

Changed production paths:

- `skills/cogentnexus-openclaw/scripts/host_control.py`
- `skills/cogentnexus-openclaw/scripts/host_control_v091.py`
- `skills/cogentnexus-openclaw/scripts/host_control_v092.py`

## TDD

RED commits:

- `bbd9bb0881ed3f6f5c770b76bfc8f28349d3b968`
- `4ff49b45a29db15989ffa0c91f23a2502d12498f`

Final local evidence:

- focused host/control tests: `32 passed`;
- full unittest: `259`, skipped `1`;
- pytest: `548 passed`, `5 skipped`, `6 subtests passed`;
- plugin: `298 passed`;
- namespace/baseline/skill validation: PASS;
- plugin package/evaluation/audit: PASS, audit `0 vulnerabilities`;
- final evaluation evidence SHA-256: `e2c75beceba52a5e07d288ad5d50c32ba7f56350b65d8ac1147a59c863103276`.

## Independent review

Fresh review of exact patch `26f148...` passed:

```json
{"passed":true,"security_concerns":[],"logic_errors":[],"suggestions":[]}
```

Earlier reviews failed closed and were not used for acceptance. Their defects (global mutation, cached mutable dispatch, `--root=` mismatch, absent-state delegation) were repaired and re-reviewed.

## Exact-SHA CI

- Validate `34162550062`: initial attempt failed only on Windows Python 3.14 in unrelated Task253 streaming-marker timeout; corrective failed-job rerun attempt `2` passed.
- Windows Installer Pack Smoke `34162550066`: success.
- PS5.1 Acceptance Smoke `34162550044`: success.

All accepted workflow evidence is bound to exact candidate `79ddec2190b226b2f5cc906144a04859b3eca748`.

## Safety

No installer, `enable`, release dispatch, tag/version mutation, semantic send, Ticket/session mutation, manual database mutation, replay, or redelivery occurred in Task310. Protected Ticket `CNXT-dc11c9a0-8a89-4df5-9c48-345260725be4` and owner session `agent:main:discord:channel:1531199905673252946` were not touched.
