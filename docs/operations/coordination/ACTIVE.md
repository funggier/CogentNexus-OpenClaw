# Active Coordination Task

Status: `READY_FOR_LUNA`
Execution mode: `TASK261_TASK260_DEPLOYMENT_TRANSITION_PROCESS_BOUNDARY_REPAIR`
Current disposition: `TASK260_ACCEPTED_BLOCKED__PROCESS_BOUNDARY_REPAIR_REQUIRED`
Task ID: `CNX-20260905-261`
Parent task: `CNX-20260905-260`
Parent umbrella: `CNX-20260831-188`
Updated: 2026-09-05 ICT

Assigned executor: `Luna`
Handoff from: `Musethree`
Next actor after report: `Musethree`
Coordination protocol: `docs/operations/coordination/HERMES_DUAL_AGENT_BATON_PROTOCOL.md`

## Accepted Task260 result

Reviewed report HEAD:

`74fc4ae713c8e61b9730942e2c4b2d37f5907eb6`

Independent review:

`docs/operations/coordination/reviews/CNX-20260905-260-task259-candidate-deployment-transition-safety-requalification-review.md`

Independent review verdict:

`ACCEPT_BLOCKED_TRANSITION_RISK__CI_GREEN_VERIFIED__REPAIR_SUCCESSOR_REQUIRED`

Task260 correctly failed closed: the install-over path has no mandatory
fresh Gateway process boundary after replacement, so a healthy predecessor
process can remain the observed runtime. Report-commit CI reached 9/9
success with no rerun. That forensic verdict is preserved.

## New repair authority

Task260 plus independent review authorizes repository/source/test repair
of the transition gap only. It is not authorization to run the installer
against the live installation, restart the live Gateway, mutate live
recovery state, redeliver or dispose the old Discord response, or perform
semantic acceptance.

## Active Task261

Execute:

`docs/operations/coordination/tasks/CNX-20260905-261-task260-deployment-transition-process-boundary-repair.md`

Add the mandatory post-replacement managed Gateway process boundary
(reusing the proven `activate_current_config()` contract or equivalent),
plus a regression test and candidate fingerprint binding, under TDD. The
live subject row remains strictly untouched.

## Cardinality / hard fences

```text
installer Scheduled Task registration/start = 0
scripts/install.ps1 live starts = 0
Gateway/controller/provider lifecycle mutation = 0
live DB/recovery row mutation = 0
recovery dispose/claim/replay/redeliver/resend = 0
semantic sends = 0
release/tag mutation = 0
force push/history rewrite = 0
```

## Stop boundary

Luna must publish:

`docs/operations/coordination/reports/CNX-20260905-261-task260-deployment-transition-process-boundary-repair.md`

Then hand the baton to Musethree and STOP for independent review.
Installer requalification remains parked until the repair is accepted.
