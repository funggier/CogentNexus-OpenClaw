# Independent Review — CNX-20260902-223 Exact Candidate Windows Install-Over Requalification

Date: 2026-09-02 ICT  
Coordinator / final reviewer: ChatGPT

## Verdict

`ACCEPT_FAIL_INSTALLER_TERMINAL__ROLLOVER_FINALIZE_ROOT_CAUSE_ADJUDICATION_REQUIRED`

Task 223 is accepted as a valid failed installer requalification. The exact Task-222 candidate was proven before launch and its payload was installed successfully, but the installer terminated nonzero during `plugin-rollover-finalize`. The resulting rollover transaction remains unresolved, so no installer retry, lifecycle action, Discord semantic traffic, or manual finalization is authorized yet.

## Accepted candidate and launcher evidence

Exact candidate:

`a812f27815b3c87b7ca748dc2dea88f987601f70`

Accepted payload fingerprint:

`e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386`

Task 223 correctly re-established exact-first Windows source provenance before launch and reproduced the accepted 192-file payload identity. It did not use the failed detached `Popen` topology from Tasks 212–213.

The direct Scheduled Task boundary behaved observably:

- one successfully registered temporary Task-223 Scheduled Task;
- one Scheduled Task start;
- top-level PowerShell runner PID `5960`;
- sustained execution for roughly eight and a half minutes;
- terminal Scheduler state `Ready`;
- `LastTaskResult=1`, agreeing with the runner failure;
- exact temporary task removed after terminal evidence;
- no process termination or installer retry.

The two failed registration attempts occurred before a task was created and before installer invocation. The failed wrapper command occurred before `Start-ScheduledTask` and therefore did not consume a second start. These are harness setup deviations, but the successful one-start installer evidence remains coherent.

## Accepted installer boundary

The installer stage ledger proves successful completion through:

```text
ticket-db-bootstrap                  exit 0
plugin-npm-pack                      exit 0
plugin-rollover-prepare              exit 0
plugin-install-local-package         exit 0
plugin-disable-post-install          exit 0
plugin-rollover-finalize             exit 1
```

No final installation-success marker exists. The runner persisted:

```text
RUNNER_FAILURE
error=ownership-safe plugin generation rollover finalization failed
```

Therefore `FAIL_INSTALLER_TERMINAL` is the correct Task-223 primary disposition.

## Important positive post-failure evidence

The installed canonical plugin payload itself matches the accepted candidate exactly:

```text
plugin id: cogentnexus-openclaw
version: 0.9.3
installed fingerprint: e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386
```

The Task-223 rollover transaction also records:

```text
expectedReplacementFingerprint: e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386
retiredFingerprint: f82674172a3946e00ddcb3a94fd14c8476bf91abc11ed7d44b5fa53acb74eaf1
controllerMode: passthrough
```

This establishes that candidate installation occurred before finalization failure. It does **not** establish ownership commit success.

Post-failure health also remained preserved and non-emitting: controller `passthrough` generation 33, startup adapter absent, Gateway healthy, Ollama healthy, Delivery READY, Recovery READY, SQLite integrity `ok`, and Discord Send count zero.

## Why no production fix is authorized yet

`install.ps1` converts any nonzero `namespace_ownership.py rollover-finalize` result into the generic PowerShell error:

`ownership-safe plugin generation rollover finalization failed`

The owning Python finalizer has multiple independent fail-closed predicates before and during ownership commit, including:

- expected/replacement fingerprint attestation;
- ownership-manifest hash stability;
- retired backup tree exactness;
- canonical direct transaction classification;
- canonical active registration;
- direct-root real/non-reparse identity;
- A -> B fingerprint transition;
- retired backup fingerprint proof;
- conflicting product-storage rejection;
- final manifest write and verification/rollback behavior.

Task 223 reports the generic terminal failure but does not identify which exact predicate raised first.

Historical Tasks 143 and 144 repaired two direct same-path finalization defects, but their existence is not evidence that either defect has regressed. The current candidate contains those repair lineages. A successor must compare the retained Task-223 transaction/inventory/live evidence against the current finalizer predicate-by-predicate rather than re-applying an old fix by analogy.

## Required successor

Open Task 224 as a **read-only retained-state rollover-finalization adjudication**.

It must:

1. preserve the current partial live state exactly;
2. read the complete Task-223 installer transcript/stderr and recover the first specific Python exception/traceback if retained;
3. read the exact Task-223 transaction JSON and matching inventory JSON;
4. read the current ownership manifest and installed plugin identity without mutation;
5. evaluate every pre-write finalizer predicate in source order using read-only calculations only;
6. compare the result against Tasks 143/144 accepted invariants;
7. identify the first exact failed predicate and the data values that caused it;
8. determine whether the failure is a source defect, stale/invalid transaction evidence, inventory-shape/canonical-registration issue, manifest drift, backup drift, conflicting storage evidence, or another proven class;
9. publish a report and stop.

Task 224 must **not** call `rollover-finalize`, must not write the ownership manifest or transaction, must not run the installer, and must not perform lifecycle or Discord actions.

## Runtime boundary

Until Task 224 is independently reviewed:

- installer retry: unauthorized;
- manual rollover finalize: unauthorized;
- `cnxclaw` lifecycle actions: unauthorized;
- Gateway restart: unauthorized;
- plugin/config/ownership/SQLite mutation: unauthorized;
- Discord semantic Sends: `0`;
- Release/tag/asset mutation: unauthorized.

## Disposition

`ACCEPT_FAIL_INSTALLER_TERMINAL__ROLLOVER_FINALIZE_ROOT_CAUSE_ADJUDICATION_REQUIRED`
