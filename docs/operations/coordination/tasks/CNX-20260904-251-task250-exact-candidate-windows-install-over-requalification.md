# CNX-20260904-251 — Task-250 Exact-Candidate Windows Install-Over Requalification

Status: `READY_FOR_HERMES`  
Executor: Hermes / authenticated Windows operator  
Coordinator / independent reviewer: ChatGPT  
Parent task: `CNX-20260904-250`  
Parent review commit: `86f7596f7f2836744b2f653b1deda0174090fe5d`  
Parent review verdict: `ACCEPT_PASS_EXACT_HASH_INPUT_SNAPSHOT_DIAGNOSTIC_TDD__TASK226_FAIL_CLOSED_PRESERVED__EXACT_CANDIDATE_READY_FOR_ONE_LIVE_INSTALL_REQUALIFICATION`  
Exact-source topology precedent: `CNX-20260904-237` / `CNX-20260902-230`  
Prior terminal live attempt: `CNX-20260904-248`  
Read-only forensic parent: `CNX-20260904-249`  
Parent umbrella: `CNX-20260831-188`  
Updated: 2026-09-04 ICT

## Objective

Perform exactly one bounded Windows install-over requalification of the Task-250 exact candidate. This task is the first live execution allowed after the Task-250 hash-input snapshot diagnostic repair.

The purpose is twofold:

1. determine whether the exact candidate now completes installation and returns the machine to coherent managed state; and
2. if the Task-248 full-tree attestation mismatch recurs, preserve the new **same-hash-input per-path diagnostic** emitted by Task 250 so the transient changed path is no longer lost.

This is an installer/runtime requalification task only. It stops before any Dashboard/Discord semantic acceptance.

## Exact candidate authority

Exact source commit:

`9c3c4e0fe0afbedf9233c25c0dd36e4209fb9d96`

Expected plugin payload fingerprint:

`1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`

Exact candidate `scripts/install.ps1` SHA-256 reported by Task 250:

`c0779d9bae69d850a44073134e7799a48a1856935b09aae1ae8c7da9f57e0629`

Public `v0.9.3` must remain immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

Fresh exact-SHA deployment gates already verified by the independent review:

```text
Validate                      33896622009 = SUCCESS
Windows Installer Pack Smoke 33896622084 = SUCCESS
PS5.1 Acceptance Smoke        33896621985 = SUCCESS
```

Fresh GitHub authority immediately before execution supersedes this summary if newer product/source/test/workflow drift appears.

## Accepted live boundary before Task 251

Tasks 248–250 did not successfully install the candidate. The accepted last live product boundary is therefore still based on the Task-248 failure plus Task-249 read-only forensic evidence:

```text
controller = passthrough generation 39
candidate installed = no
live canonical plugin = predecessor payload e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386
Task248 terminal stage = plugin-rollover-prepare
Task248 terminal exception = RuntimeError: pre-install backup project-tree attestation mismatch
semantic sends since that boundary = 0 by Tasks 249–250
```

Task-249 resolved the retired project root as:

`C:/Users/CDQ-P/.openclaw/extensions/cogentnexus-openclaw`

and retained the Task-248 rollover backup:

`C:/Users/CDQ-P/AppData/Local/CogentNexus-OpenClaw/plugin-generation-rollover-backups/cogentnexus-openclaw-fc6fb357dd4a4c9688e4eb0116c10033`

At Task-249 observation time both hashed to:

`900ac13f85a6de75e40a632a534f2b0ceef53def1e8387fc3530c02a7413de58`

That equality was post-failure only. Task 251 must freshly verify current live state and must not assume these values remain unchanged.

## Safety invariants

Task 251 MUST preserve all of the following:

- Task-226 full-tree fail-closed attestation;
- Task-247 native child stderr/stdout preservation;
- Task-250 same-scan hash-input snapshot diagnostic;
- exact-source binding from the verified detached checkout;
- installer retry gate closes immediately when the installer actually starts;
- no manual plugin/lifecycle/DB repair after start;
- no semantic submission in this task.

Do not weaken, bypass, exclude, retry-until-equality, or reinterpret an attestation mismatch as success.

## Phase A — fresh GitHub authority

Immediately before live work:

1. fetch current branch HEAD;
2. re-read this Task, Task-250 report/review, `ACTIVE.md`, and `STATUS.md`;
3. require Task 251 remains the active `READY_FOR_HERMES` task;
4. verify candidate `9c3c4e0...` remains an ancestor of coordination HEAD;
5. compare candidate -> current HEAD and require only expected coordination/report/review drift;
6. verify exact-candidate Actions remain terminal SUCCESS for Validate, Windows Installer Pack Smoke, and PS5.1 Acceptance Smoke;
7. verify public `v0.9.3` remains exactly `26ce64a...`;
8. verify no newer coordination task supersedes Task 251.

Unexpected product/source/test/workflow drift:

`BLOCKED_PREFLIGHT_DRIFT`

No live mutation after that classification.

## Phase B — exact detached source binding

Use the corrected Task-237 topology. Do not invent an install-source-commit parameter.

Required flow:

```text
fresh fetch
-> one disposable checkout under %LOCALAPPDATA%\Temp
-> checkout exact 9c3c4e0fe0afbedf9233c25c0dd36e4209fb9d96
-> prove exact detached/pinned HEAD
-> prove clean source
-> invoke that checkout's scripts/install.ps1 directly
```

Record and require:

```text
git rev-parse HEAD = 9c3c4e0fe0afbedf9233c25c0dd36e4209fb9d96
git diff --quiet = success
git diff --cached --quiet = success
no relevant untracked source mutation
VERSION = 0.9.3
plugin fingerprint = 1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f
scripts/install.ps1 SHA-256 = c0779d9bae69d850a44073134e7799a48a1856935b09aae1ae8c7da9f57e0629
```

Also prove from the exact checkout that `namespace_ownership.py` contains:

- Task-226 fail-closed mismatch prefix;
- `_project_tree_snapshot()`;
- `_project_tree_snapshot_delta()`;
- source/backup snapshots captured before comparison;
- `diagnostic=` emission on mismatch.

If exact source binding cannot be proven:

`BLOCKED_SOURCE_BINDING`

Do not register/start the installer.

Explicitly prohibited:

```text
--install-source-commit
-InstallSourceCommit
InstallSourceCommit
```

## Phase C — read-only Windows preflight

Before scheduler registration or installer start, capture fresh live evidence:

- controller mode/generation;
- startup policy and startup adapter state / LastTaskResult;
- Supervisor/doctor;
- installed plugin id/version/path/source/enabled/status/fingerprint;
- live ownership manifest path/hash/coherence;
- live `namespace_ownership.py` identity;
- Gateway endpoint/health;
- provider remains Ollama and exact configured model is unchanged;
- Delivery READY and pending outbox count;
- Recovery READY and unresolved/emittable recovery state;
- SQLite integrity and relevant durable residue;
- Task-233 historical lineage remains non-emittable and is not modified;
- relevant OpenClaw/CogentNexus/Ollama process inventory;
- Task-223 retained evidence unchanged;
- Task-248 retained rollover backup still present and unchanged;
- Task-249 forensic evidence still present and unchanged.

Create Task-251 evidence only outside protected source/backup trees, for example:

`%LOCALAPPDATA%/CogentNexus-OpenClaw/forensics/CNX-20260904-251/`

Do not modify live state during preflight.

## Phase D — delivery/recovery hazard gate

Require before installer start:

```text
Delivery READY
pending outbox = 0
Recovery READY
no emittable unresolved recovery capable of producing a delivery during this task
no unexplained active/nonterminal semantic lineage likely to emit
```

If unsafe or ambiguous:

`BLOCKED_DELIVERY_HAZARD`

Do not edit/delete Ticket, outbox, recovery, session, or SQLite state to make the gate pass.

## Phase E — scheduler / installer execution

Use the authenticated Windows Scheduled Task topology proven by Task 230/237 unless fresh host evidence requires a bounded evidence-driven launcher adaptation before product start.

The scheduled task action MUST invoke the exact `scripts/install.ps1` inside the verified Task-251 checkout.

Do not use:

- `-SkipPlugin`
- `-SkipGatewayRestart`
- `-SkipAgentsPolicy`
- `-LinkPlugin`

Record:

- exact checkout path;
- exact HEAD immediately before task registration and immediately before start;
- exact installer path/hash;
- exact supported PowerShell command line;
- task principal/logon/run-level/settings;
- registration/readback evidence;
- start request timestamp;
- earliest installer process timestamp;
- transcript/stdout/stderr paths;
- terminal task state / LastTaskResult;
- installer exit code and terminal timestamps.

### Cardinality / retry gate

Before actual installer execution:

- scheduler registration: maximum 2 attempts only if attempt 1 is a genuine registration/tooling failure and there is proof the installer never started;
- successful installer start requests: maximum 1;
- installer invocations: maximum 1.

The instant the installer task/process starts:

`INSTALLER_RETRY_GATE=CLOSED`

After that:

```text
installer execution retries = 0
second installer start = 0
second installer invocation = 0
manual plugin repair = 0
manual lifecycle repair = 0
manual DB/recovery repair = 0
```

Observer failures after product start never reopen the retry gate.

## Phase F — rollover attestation diagnostic capture

Plugin replacement / generation rollover is authorized only as part of the single installer invocation.

If `plugin-rollover-prepare` fails with the Task-226 prefix:

`pre-install backup project-tree attestation mismatch`

Task 251 MUST preserve the complete raw child stdout/stderr/transcript before any further analysis.

If a Task-250 `diagnostic=` JSON object is present, retain it byte-for-byte and separately parse/report, without modifying either attested tree:

- `sourceTreeSha256`;
- `backupTreeSha256`;
- `changedPaths` exactly as emitted;
- each emitted `differences[]` entry with source/backup digest-relevant identity;
- whether an entry is missing on either side (`null`);
- object/type/size/content-SHA/symlink identity where present;
- exact count of emitted differences.

The diagnostic is bounded. Do not infer that the emitted list is exhaustive beyond the producer's bound.

After a terminal mismatch:

- do not re-run installer;
- do not retry hashes until equality;
- do not exclude the reported path;
- do not mutate/copy/lock/rename/delete the retired tree to force convergence;
- do not claim an actor/process solely from the path;
- optionally capture immediate **read-only** process/log/USN evidence around the now-known path after the terminal boundary, but no product mutation.

Preferred disposition when exact Task-250 mismatch evidence is retained:

`FAIL_INSTALLER_TERMINAL_ATTESTATION_MISMATCH_DIAGNOSTIC_CAPTURED`

If the installer fails terminally for another reason:

`FAIL_INSTALLER_TERMINAL`

In either case, stop product execution.

## Phase G — successful installer identity proof

Only if the single installer invocation returns success, require:

```text
installer exit code = 0
LastTaskResult = 0 where applicable
installer invocation count = 1
installer execution retries = 0
```

Then prove live canonical plugin:

- id/version/path/source correct;
- enabled and healthy;
- payload fingerprint exactly `1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`;
- live Task-250 `namespace_ownership.py` diagnostic repair corresponds to candidate;
- Task-235 Dashboard delivery repair remains in installed payload;
- ownership manifest is coherent with the installed generation;
- any new rollover transaction/inventory/backup artifacts are captured with exact paths/hashes/timestamps and self-consistency evidence.

If installer reports success but exact identity cannot be proven:

`FAIL_PLUGIN_IDENTITY`

No manual repair.

## Phase H — managed convergence and health

Allow only normal installer/runtime convergence. Prove:

- controller coherently `managed`;
- generation internally coherent;
- startup policy enabled as intended;
- startup adapter installed/Ready with successful result where applicable;
- Supervisor/doctor healthy;
- Gateway healthy at intended loopback endpoint;
- provider/model remain Ollama + configured model;
- Delivery READY, pending outbox = 0;
- Recovery READY, no replay/resend introduced;
- SQLite integrity OK;
- no unexpected duplicate/nonterminal Ticket/session/run residue;
- process inventory coherent;
- Task-223, Task-233, Task-248, and Task-249 retained evidence preserved;
- semantic submissions = 0.

If exact plugin identity is correct but managed convergence fails:

`FAIL_MANAGED_CONVERGENCE`

If material runtime health remains unhealthy:

`FAIL_POST_INSTALL_HEALTH`

## Read-only retry policy

Read-only observation/query failures may use up to 2 additional attempts per logical observation only when retry cannot create product or semantic side effects.

Every retry must record:

```text
logical operation
attempt number
UTC time
method
result/error
could state change?
remaining retry budget
changed rationale/method
```

No blind repeats. No observer retry can authorize another installer execution.

Final classification:

- `RETRY_POLICY_EFFECTIVE`
- `RETRY_POLICY_NOT_NEEDED`
- `RETRY_POLICY_EXHAUSTED_WITHOUT_RECOVERY`
- `RETRY_POLICY_STOPPED_BY_PRODUCT_BOUNDARY`

## Effect / mutation budget

```text
Dashboard semantic submissions = 0
Discord semantic submissions = 0
direct operator Discord/API sends = 0
semantic retries/resubmissions = 0
manual durable delivery = 0
manual Ticket/outbox/recovery/SQLite mutation = 0
manual provider/model substitution = 0
manual process termination = 0
manual Gateway/lifecycle repair = 0
manual plugin install/copy/delete/rename/manifest repair = 0
reset = 0
uninstall = 0
fresh reinstall = 0
installer successful starts <= 1
installer invocations <= 1
installer execution retries after start = 0
Task223 retained evidence mutation = 0
Task248 retained backup mutation = 0
Task249 forensic evidence mutation = 0
Task233 replay/settlement/deletion = 0
release/tag/asset mutation = 0
production/source/test/workflow edits = 0
force push/history rewrite = 0
```

Installer-owned plugin replacement/rollover and normal installer-owned lifecycle/convergence are the only authorized live product mutations.

## PASS cardinality

A PASS requires:

```text
exact detached candidate checkout = 1
source HEAD = 9c3c4e0... immediately before registration/start
installer invocation = exactly 1
installer retry after start = 0
installed fingerprint = 1ff69c459...
controller final mode = managed
manual plugin/lifecycle/DB repair = 0
Dashboard/Discord/API semantic submissions = 0
recovery replay/resend = 0
```

## Allowed dispositions

- `PASS_EXACT_CANDIDATE_WINDOWS_INSTALL_OVER_REQUALIFIED`
- `BLOCKED_PREFLIGHT_DRIFT`
- `BLOCKED_SOURCE_BINDING`
- `BLOCKED_DELIVERY_HAZARD`
- `FAIL_INSTALLER_REGISTRATION`
- `FAIL_INSTALLER_TERMINAL_ATTESTATION_MISMATCH_DIAGNOSTIC_CAPTURED`
- `FAIL_INSTALLER_TERMINAL`
- `FAIL_PLUGIN_IDENTITY`
- `FAIL_MANAGED_CONVERGENCE`
- `FAIL_POST_INSTALL_HEALTH`
- `BLOCKED_EVIDENCE`

## Required report

Publish:

`docs/operations/coordination/reports/CNX-20260904-251-task250-exact-candidate-windows-install-over-requalification.md`

The report must include:

- fresh GitHub authority;
- exact detached checkout/source-binding proofs;
- preflight and delivery/recovery hazard gate;
- scheduler/installer attempt ledger;
- exact installer command/path/hash/timestamps;
- terminal task/result/exit evidence;
- complete retained stdout/stderr/transcript identities;
- rollover classification and artifacts;
- exact Task-250 `diagnostic=` evidence if mismatch occurs;
- exact installed fingerprint and candidate identity if successful;
- managed convergence/final health if successful;
- preservation of historical Task-223/233/248/249 evidence;
- effect/cardinality ledger;
- retry classification;
- semantic/direct-send counts explicitly zero;
- final disposition.

Then **STOP for independent ChatGPT review**.

Even on PASS, do not proceed to Dashboard semantic acceptance, Discord semantic testing, recovery replay/settlement, stale-evidence cleanup, reset/uninstall/fresh reinstall, or release/tag/asset mutation without a separate successor task.
