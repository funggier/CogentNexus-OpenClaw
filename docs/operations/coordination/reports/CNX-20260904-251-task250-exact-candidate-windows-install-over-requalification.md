# CNX-20260904-251 — Task 250 exact-candidate Windows install-over requalification

- Authority: fresh remote `agent/v0.9.3-full-stabilization`, Task 251 read from the exact fetched branch tip immediately before execution.
- Candidate: detached checkout at `9c3c4e0fe0afbedf9233c25c0dd36e4209fb9d96`.
- Candidate source binding: installer `scripts/install.ps1`; SHA-256 was verified before registration/start. Manifest-bound runner pointed to this exact checkout and installer path. Pre-start action/manifest readback passed.
- Expected candidate plugin fingerprint: `1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`.

## Preflight

Fresh read-only preflight passed the hazard gate:

- controller `passthrough`, generation `39`;
- selected provider `ollama`;
- Gateway/provider/model/storage/recovery/delivery checks returned READY;
- Delivery pending terminal deliveries: `0`;
- SQLite `integrity_check`: `ok`;
- canonical installed plugin remained predecessor fingerprint `e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386`;
- Task-251 was absent before registration;
- Task-223/233/248/249 retained evidence roots were not edited.

The unsupported local `plugins list --json` probe returned usage error; it was not used as product evidence and caused no state change.

## Attempt ledger

| Item | Result |
|---|---|
| Scheduled Task registration | `1` successful registration; readback completed |
| Installer successful starts | `1` |
| Installer invocations | `1` |
| Installer retry after start | `0`; retry gate closed immediately |
| Start time | `2026-09-04T17:22:05.4068237Z` |
| Runner child start | `2026-09-04T17:22:05.7455411Z`, identity `CDQ-P\\CDQ-P` |
| Task terminal state | `Ready` |
| `LastTaskResult` | `267014` (`0x41306`) |
| Runner result | absent |
| Child stdout/stderr | absent |
| Complete runner transcript | absent; observer log only records Running samples |
| Manual process termination | `0` |

The first registration-shell attempt failed before task creation due harness quoting. A file-based registration retry was used once; subsequent readback confirmed the task and binding. A later observer shell attempt also failed from quoting; it did not start or retry the installer. Read-only file-based observation then continued.

The task remained Running until the Windows task execution limit, then became Ready with `LastTaskResult=267014 (0x41306)`. Because the manifest runner did not persist child terminal evidence, the installer stage, exit code, rollover result, and any diagnostic output are unproven. This is not classified as an attestation mismatch.

## Postflight

Read-only postflight after task termination:

- controller remained `passthrough`, generation `39`;
- selected provider remained `ollama`;
- `status --json` exit `0`;
- Delivery READY, pending `0`;
- Recovery READY;
- storage READY, SQLite integrity `ok`;
- gateway remained healthy;
- ownership manifest remained predecessor installation identity;
- historical committed transaction remained unchanged;
- no manual repair, plugin copy/delete/rename, database mutation, replay, resend, semantic send, or release operation occurred.

No PASS claim is made: candidate installation fingerprint and managed convergence were not established. No evidence authorizes retry, repair, recovery replay, semantic acceptance, release, or cleanup.

## Retry classification

`RETRY_POLICY_STOPPED_BY_PRODUCT_BOUNDARY`

The sole installer start was consumed. The terminal scheduler result and missing durable runner evidence do not authorize another installer execution under this task.

## Effect/cardinality ledger

- Dashboard semantic submissions: `0`
- Discord semantic submissions: `0`
- direct operator Discord/API sends: `0`
- semantic retries/resubmissions: `0`
- manual durable delivery: `0`
- manual Ticket/outbox/recovery/SQLite mutation: `0`
- manual provider/model substitution: `0`
- manual process termination: `0`
- manual Gateway/lifecycle repair: `0`
- manual plugin install/copy/delete/rename/manifest repair: `0`
- reset/uninstall/fresh reinstall: `0`
- Task-223 retained evidence mutation: `0`
- Task-248 retained backup mutation: `0`
- Task-249 forensic evidence mutation: `0`
- Task-233 replay/settlement/deletion: `0`
- release/tag/asset mutation: `0`
- production/source/test/workflow edits: `0`
- force-push/history rewrite: `0`

## Final disposition

`BLOCKED_EVIDENCE`

STOP at the independent-review boundary. No Dashboard semantic acceptance, Discord semantic testing, recovery replay/settlement, stale-evidence cleanup, reset/uninstall/reinstall, or release/tag/asset operation was performed.
