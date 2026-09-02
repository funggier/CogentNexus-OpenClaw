# Independent Review — CNX-20260902-230 Scheduler Identity Recovery + Bounded-Retry Installer Re-entry

Date: 2026-09-03 ICT  
Coordinator / final reviewer: ChatGPT

## Verdict

`ACCEPT_PASS_ALREADY_EXACT_INSTALLER_REENTRY__MANAGED_CONVERGENCE_PROVEN__RETRY_POLICY_EFFECTIVE__REPORTING_GAP_NONBLOCKING`

Task 230 is accepted as a successful already-exact Windows installer re-entry and managed-runtime convergence proof.

## Exact report authority

Report HEAD:

`f36b5c0f8409880949c460d47757584b9e0afd28`

Parent Task-230 activation HEAD:

`384da6395ee1787f17d9f1d24dac8da7eed49c34`

Fresh compare proves the report closure is one coordination/report-only commit and introduces no product/source/test/workflow drift.

Accepted repaired source remains:

`9a8510f1317c8e53c01c233b080ec20357cd22df`

Accepted plugin payload fingerprint remains:

`e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386`

Public `v0.9.3` remains immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

No public Release replay is authorized by this review.

## Accepted scheduler/retry recovery

Task 230 recovered the canonical current-user scheduler identity and proved a harmless direct Scheduled Task canary before installer execution.

Accepted current identity evidence:

```text
WindowsIdentity.Name = CDQ-P\CDQ-P
SID = S-1-5-21-1723981734-2946015581-220292090-1001
principal shape = Interactive / Limited
```

The canary registered once, started once, reached its intended terminal code `23`, propagated `LastTaskResult=23`, and was removed cleanly.

The installer-task registration budget was used once and the task was started once. No installer execution retry occurred.

A pre-start read-only/probe tooling anomaly was handled by switching to deterministic task inspection while the installer had not started. That is accepted as evidence-driven tooling adaptation under the Task-230 bounded retry policy.

Normalized retry-policy classification for this review:

`RETRY_POLICY_EFFECTIVE__NO_INSTALLER_EXECUTION_RETRY`

## Installer success accepted

The exact repaired installer was invoked exactly once.

Accepted terminal evidence:

```text
INSTALLER_INVOCATION_START utc=2026-09-02T15:38:30.4864500Z
CogentNexus-OpenClaw validation: PASS
CogentNexus-OpenClaw v0.9.3 installation completed successfully.
INSTALLER_INVOCATION_END utc=2026-09-02T15:44:34.4043723Z exit_code=0
Scheduled Task LastTaskResult=0
```

Required already-exact plugin/rollover mutation counts were preserved:

```text
installer invocations: 1
openclaw plugins install: 0
rollover-prepare: 0
rollover-finalize: 0
installer execution retries: 0
```

## Managed convergence accepted

Post-install runtime evidence proves coherent managed state:

```text
controller mode: managed
generation: 38
startup policy: enabled
startup adapter: installed / Ready / LastTaskResult=0
provider: ollama
Gateway: healthy at 127.0.0.1:18789
Delivery: READY, pending=0
Recovery: READY
SQLite integrity_check: ok
```

The live workspace ownership implementation matches the accepted Task-226 repair and contains the fail-closed backup project-tree attestation contract.

No manual lifecycle repair, plugin repair, ownership edit, SQLite mutation, process termination, provider substitution, or Discord semantic traffic was required.

## Historical evidence preservation

Task-223 retained evidence remained unchanged:

```text
transaction SHA-256:
ec1b32ec2813e1b4e2c220679f39c6922789b7d77e88ec9ca4ad6ba82ccac510

matching inventory SHA-256:
1a7299f926cda4e3f936577204c50059e0e4e716f8594535d4b3c40c40e51477

backup project-tree SHA-256:
7394401cb0ae9791c1c9b98661a9bf9df47ecb83c0b139b46cd742b17ee7342a

backup payload fingerprint:
f82674172a3946e00ddcb3a94fd14c8476bf91abc11ed7d44b5fa53acb74eaf1
```

No new rollover transaction was created. Historical evidence cleanup remains separately gated.

## Exact report-HEAD CI

All required workflows for `f36b5c0f8409880949c460d47757584b9e0afd28` are successful:

```text
Validate:                      33651641144  SUCCESS
Windows Installer Pack Smoke: 33651641321  SUCCESS
PS5.1 Acceptance Smoke:        33651641056  SUCCESS
```

## Nonblocking reporting gap

Task 230 required an explicit retry-policy usefulness classification and normalized attempt ledger. The report contains sufficient raw method/count/budget evidence to independently reconstruct the retry behavior, but it does not present the exact formal `RETRY_POLICY_*` label or a fully normalized attempt-ledger table.

This is accepted as a documentation/reporting gap, not a product or execution failure, because:

- all tooling adaptation happened before installer start;
- the canary and installer task each registered on their first successful authorized method;
- installer start/invocation remained exactly one;
- no post-start execution retry occurred;
- product state and historical evidence are fully accounted for.

Successor reports should explicitly normalize retry classification and attempt ledgers.

## Successor authorization

Task 188 and Task 223 require semantic/durable-delivery acceptance to remain separate from installer qualification.

A successor may authorize exactly one human Dashboard semantic turn on this repaired managed runtime and prove:

`one Ticket -> one session/run -> one Ollama call -> one durable delivery -> one logical Dashboard assistant result`

with payload provenance, no retry/recovery duplicate, and exactly-once observable delivery for that lineage.

The semantic submission itself must have a one-attempt budget. Tooling/observer retries may be bounded and evidence-driven, but once the Dashboard submission is accepted/started the semantic retry gate must close permanently for that task.

Still not authorized:

- stale Task-223 evidence cleanup/finalization;
- installer/reinstall/reset/uninstall repetition;
- manual lifecycle or SQLite repair;
- provider/model substitution;
- source/test/workflow product edits;
- public Release/tag/asset mutation;
- force push/history rewrite.

Task-230 Discord budget and actual semantic Sends: `0`.
