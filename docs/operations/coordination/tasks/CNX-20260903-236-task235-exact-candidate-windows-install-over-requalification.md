# CNX-20260903-236 — Task235 Exact-Candidate Windows Install-Over Requalification

Status: `READY_FOR_HERMES`  
Executor: Hermes / authenticated Windows operator  
Coordinator / independent reviewer: ChatGPT  
Parent task: `CNX-20260903-235`  
Parent review verdict: `ACCEPT_PASS_REPOSITORY_TDD_EVIDENCE_CLOSED__CANDIDATE_READY_FOR_LIVE_REQUALIFICATION`  
Parent umbrella: `CNX-20260831-188`  
Installer safety / attestation repair parent: `CNX-20260902-226`  
Known-good scheduler/install re-entry precedent: `CNX-20260902-230`  
Historical installer failure lineage: `CNX-20260902-223`  
Updated: 2026-09-03 ICT

## Objective

Install-over the exact Task-235 candidate on the authenticated Windows host **once**, through the repaired installer path, then prove that the live system converges to a coherent managed state with the exact expected plugin identity and no duplicate/recovery hazard.

This task is **installer-only live requalification**. It deliberately stops before the one-human Dashboard semantic/durable-delivery acceptance required later by Task 188.

## Exact candidate authority

Exact source commit:

`ffb0dd4ed47affe2e496c17b74ca74d358905bd7`

Expected installed plugin payload fingerprint:

`1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`

Public `v0.9.3` must remain immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

Task-235 review:

`docs/operations/coordination/reviews/CNX-20260903-235-task234-exact-topology-tdd-evidence-closure-review.md`

Task-235 report:

`docs/operations/coordination/reports/CNX-20260903-235-task234-exact-topology-tdd-evidence-closure.md`

Exact candidate Actions already independently accepted:

- Validate `33688878141` — SUCCESS
- Windows Installer Pack Smoke `33688878183` — SUCCESS
- PS5.1 Acceptance Smoke `33688878240` — SUCCESS

Fresh GitHub authority still wins if any newer coordination state exists before execution.

## Non-negotiable sequencing

Task 188 authorizes the proportional sequence:

```text
exact candidate install-over
-> prove managed/runtime identity and health
-> independent review
-> later, exactly one human Dashboard semantic/durable-delivery requalification
```

Task 236 covers only the first two steps.

**Do not submit any Dashboard or Discord semantic message in Task 236.**

A PASS from this task is not semantic acceptance and does not authorize Hermes to continue into a semantic turn without a separate successor task opened after independent ChatGPT review.

## Phase A — fresh repository authority

Immediately before live work, capture fresh GitHub evidence for:

1. branch HEAD;
2. `ACTIVE.md` and `STATUS.md` naming Task 236 as active `READY_FOR_HERMES`;
3. Task-235 report and independent review;
4. exact candidate `ffb0dd4...` remains an ancestor of current coordination HEAD;
5. no unexpected product/source/test/workflow drift after the exact candidate;
6. exact candidate Actions remain terminal SUCCESS for all three required workflows;
7. public `v0.9.3` remains `26ce64a...`;
8. no newer coordination authority supersedes Task 236.

If authority drift is ambiguous or product/source/test/workflow content has changed after the accepted candidate, stop:

`BLOCKED_PREFLIGHT_DRIFT`

Do not install from a guessed or reconstructed SHA.

## Phase B — read-only Windows preflight

Before installer registration/start, collect read-only evidence for the current live system:

- controller mode and generation;
- startup policy and startup adapter state / `LastTaskResult`;
- Supervisor / doctor state;
- managed-policy / AGENTS identity;
- installed plugin id, version, canonical path, source, enabled/status, and payload fingerprint;
- live `namespace_ownership.py` identity and confirmation that the Task-226 fail-closed attestation repair remains present;
- ownership manifest identity/hash where available;
- Gateway health and endpoint;
- active provider, form, and exact model; prove Ollama remains selected;
- Delivery state and pending outbox count;
- Recovery state and any emittable unresolved recovery;
- SQLite integrity, relevant durable counts/max IDs, and pending/nonterminal Ticket residue;
- relevant session/run/model residue where safely observable;
- process inventory relevant to OpenClaw/CogentNexus/Ollama;
- retained Task-223 transaction/inventory/backup artifact identities/hashes.

The pre-install plugin fingerprint may legitimately be the previously installed payload, including the earlier accepted `e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386`. Do not treat a known prior healthy payload as drift merely because it differs from the new candidate. Treat unexplained identity/newer mutation as drift.

## Phase C — delivery/recovery hazard gate

Before installer execution require a coherent quiet boundary:

```text
Delivery READY
pending outbox = 0
Recovery READY
no emittable unresolved recovery capable of producing an acceptance-channel delivery
no unexplained nonterminal duplicate semantic lineage likely to emit during installation
```

Do not repair contamination by deleting/editing Ticket, outbox, recovery, session, or SQLite state.

If this gate is not provably clean:

`BLOCKED_DELIVERY_HAZARD`

No installer start is authorized after that disposition.

## Phase D — installer execution topology

Use the known-good authenticated Windows scheduled-task/PowerShell topology proven by Task 230 unless fresh host evidence requires a materially justified harmless registration-method change.

The installer invocation must use the exact candidate and the temporary source-commit override required by the installer contract, including:

`--install-source-commit ffb0dd4ed47affe2e496c17b74ca74d358905bd7`

Record:

- task registration parameters and principal identity;
- task registration result;
- task start timestamp;
- earliest reliable installer process/invocation timestamp;
- exact command/source commit;
- installer stdout/stderr/log identities;
- scheduled-task terminal state / `LastTaskResult`;
- installer process exit code;
- start/end timestamps.

### Installer retry gate

Before any installer task/process starts:

- installer-task registration: maximum 2 attempts total, and attempt 2 is allowed only after a genuine tooling/registration failure with a materially different evidence-driven method;
- installer task start: maximum 1 successful start request;
- installer invocation: maximum 1.

As soon as the installer task/process is observed to have started:

`INSTALLER_RETRY_GATE=CLOSED`

After that boundary:

- installer execution retries: **0**;
- no second task start;
- no second installer invocation;
- no manual plugin repair to convert a failed install into PASS.

If installer execution or installer-owned rollover/finalization fails after start, collect read-only evidence and stop fail-closed.

## Phase E — plugin replacement / rollover rules

Unlike the Task-230 already-exact re-entry, the installed live payload is expected to differ from `ffb0dd4...`. Therefore the installer may legitimately classify this as requiring installer-owned plugin replacement / generation rollover.

Do **not** require plugin-install or rollover count to be zero.

Instead prove:

- only the one authorized installer invocation initiated product mutation;
- plugin install/replacement/rollover, if required, was installer-owned;
- Task-226 fail-closed prepare attestation contract remains in force;
- rollover finalization, if invoked, succeeds;
- no manual `openclaw plugins install`, copy/delete/rename, manifest editing, or plugin-path repair was used outside the installer;
- any new rollover transaction/inventory/backup artifacts are captured with paths, identities, hashes, timestamps, and self-consistency evidence;
- Task-223 retained forensic artifacts remain unchanged and are not deleted/rewritten.

A rollover/finalizer terminal failure after installer start is:

`FAIL_INSTALLER_TERMINAL`

Do not retry the installer.

## Phase F — exact installed candidate identity

After installer terminal success, prove all of the following from the live host:

- installer exit code = 0;
- scheduled-task `LastTaskResult` = 0 where applicable;
- installer log reports successful completion;
- installer source is exact commit `ffb0dd4...`;
- canonical installed plugin path/source is correct;
- plugin is enabled/healthy;
- installed plugin payload fingerprint equals exactly:

  `1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`

- live `v091-dashboard-verified-delivery.ts` corresponds to the accepted candidate payload;
- live `namespace_ownership.py` still contains the accepted Task-226 fail-closed attestation repair;
- ownership manifest is coherent with the resulting generation/installation.

If the installer reports success but exact live plugin identity cannot be proven:

`FAIL_PLUGIN_IDENTITY`

Do not manually repair identity.

## Phase G — managed convergence / post-install health

Wait only as needed for normal installer/runtime convergence; do not perform manual lifecycle mutation merely to force a healthy state.

Then prove:

- controller is in coherent `managed` mode;
- resulting generation is internally coherent; do not require a historical fixed generation number;
- startup policy is enabled as expected;
- startup adapter is installed/Ready with successful last result where applicable;
- Supervisor/doctor state is healthy/coherent;
- Gateway is healthy at its intended local endpoint;
- provider remains Ollama and exact configured model remains unchanged;
- Delivery returns to READY with pending outbox = 0;
- Recovery is READY with no unexpected replay/resend;
- SQLite integrity is OK;
- no unexplained duplicate/nonterminal Ticket/session/run residue was introduced;
- relevant process inventory is coherent;
- no direct operator Discord/API Send occurred;
- no semantic turn occurred.

If installer identity is correct but managed convergence cannot be established:

`FAIL_MANAGED_CONVERGENCE`

If convergence initially occurs but final health is materially unhealthy:

`FAIL_POST_INSTALL_HEALTH`

## Read-only retry policy

Read-only observer/query/evidence-collection operations may use up to **2 additional attempts per logical observation** only when the failure is attributable to tooling, transport, query shape, quoting, transient command behavior, or evidence-collection mechanics.

Every retry must change the method/hypothesis or directly address the observed failure. Blind repetition is prohibited.

A failed observer command never authorizes another installer start or another product mutation.

Required attempt ledger columns:

```text
logical operation
attempt number
method
result/error
could semantic/product state change?
remaining retry budget
next rationale / changed method
```

Final report must classify the retry handling as exactly one of:

- `RETRY_POLICY_EFFECTIVE`
- `RETRY_POLICY_NOT_NEEDED`
- `RETRY_POLICY_EXHAUSTED_WITHOUT_RECOVERY`
- `RETRY_POLICY_STOPPED_BY_PRODUCT_BOUNDARY`

## Effect / mutation budget

```text
Dashboard human semantic submissions: 0
Discord-origin semantic submissions: 0
direct operator Discord/API Sends: 0
semantic retries/resubmissions: 0
manual durable delivery: 0
manual Ticket/outbox/recovery/SQLite mutation: 0
manual provider/model substitution: 0
manual process termination: 0
manual Gateway/lifecycle repair: 0
manual plugin install/copy/delete/rename/manifest repair: 0
reset: 0
uninstall: 0
fresh reinstall: 0
installer task successful starts: <= 1
installer invocations: <= 1
installer execution retries after start: 0
Task-223 retained forensic evidence mutation: 0
Release/tag/asset mutation: 0
source/test/workflow production edits: 0
force push/history rewrite: 0
```

Installer-owned plugin replacement/rollover and normal installer-owned lifecycle/convergence operations are the only authorized live product mutations.

## Accepted PASS cardinality

A PASS requires a mutation/cardinality ledger proving:

```text
exact source candidate used: 1
installer successful start lineage: 1 maximum
installer invocation lineage: 1 exactly
installer execution retry after start: 0
manual plugin mutation: 0
Dashboard semantic submission: 0
direct operator Discord/API Send: 0
semantic/durable acceptance effect: 0
recovery replay/resend introduced by operator: 0
```

If the installer determines no plugin replacement is required despite a candidate fingerprint difference, preserve the evidence and treat that as an identity anomaly until explained; do not assume success from exit code alone.

## Allowed dispositions

Use one of:

- `PASS_EXACT_CANDIDATE_WINDOWS_INSTALL_OVER_REQUALIFIED`
- `BLOCKED_PREFLIGHT_DRIFT`
- `BLOCKED_DELIVERY_HAZARD`
- `FAIL_INSTALLER_REGISTRATION`
- `FAIL_INSTALLER_TERMINAL`
- `FAIL_PLUGIN_IDENTITY`
- `FAIL_MANAGED_CONVERGENCE`
- `FAIL_POST_INSTALL_HEALTH`
- `BLOCKED_EVIDENCE`

When evidence is incomplete after installer start, fail/block from the existing execution evidence. Do not run the installer again to improve observability.

## Required report

Publish:

`docs/operations/coordination/reports/CNX-20260903-236-task235-exact-candidate-windows-install-over-requalification.md`

The report must include:

- fresh authority and exact source SHA;
- pre-install live state;
- hazard gate result;
- scheduler/installer attempt ledger;
- exact installer command/source override, timestamps, exit/task result, and logs;
- plugin classification/replacement/rollover evidence;
- exact post-install fingerprint and live-file identity;
- any new rollover transaction/inventory/backup identities/hashes;
- proof Task-223 retained artifacts are unchanged;
- managed convergence and final health;
- mutation/effect/cardinality ledger;
- retry-policy classification;
- explicit confirmation that semantic submission count is zero;
- final disposition.

Then **STOP for independent ChatGPT review**.

Even on PASS, Hermes must not send the one-human Dashboard acceptance message, run a Discord semantic test, replay/settle an old lineage, clean Task-223 evidence, reset/uninstall/reinstall, or mutate public Release/tag/assets. The semantic/durable-delivery successor is opened only after Task 236 is independently accepted.