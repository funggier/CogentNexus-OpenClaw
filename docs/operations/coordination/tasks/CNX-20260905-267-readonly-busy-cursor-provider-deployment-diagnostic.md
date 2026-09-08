# CNX-20260905-267 — Read-Only 60-Second Busy-Cursor / Provider / Deployment Diagnostic

## Objective

Perform a bounded read-only live diagnostic that explains the user's approximately one-minute Windows busy-circle cursor symptom, diagnoses the current `ollama:1` recovery warning, and refines exact-candidate deployment prerequisites without mutating live runtime or durable state.

## Authority

This task authorizes read-only inspection and temporary diagnostic monitoring only.

Allowed examples:

- inspect current processes, parent/child relationships, command lines, creation times, CPU/disk counters;
- inspect Windows Scheduled Tasks and their triggers/actions/last/next run times;
- inspect relevant Windows event logs read-only;
- inspect OpenClaw/CogentNexus/Ollama logs and status read-only;
- capture bounded process-creation activity for several minutes using a read-only monitoring method (for example WMI/CIM event tracing or Process Monitor if already available), then stop only the diagnostic capture that this task started;
- create temporary evidence files and repository report/state commits.

## Hard fences

```text
installer/install-over/uninstall/reset           = 0
Gateway/provider/service lifecycle mutation      = 0
live OpenClaw session delete/reset                = 0
live Discord/Dashboard/API semantic send         = 0
manual live Ticket/session/SQLite mutation       = 0
recovery replay/redelivery/disposition            = 0
Scheduled Task enable/disable/create/delete       = 0
stop/kill/restart unrelated live processes        = 0
release/tag/default-branch promotion             = 0
force push/history rewrite                       = 0
```

The only process stop allowed is terminating a temporary diagnostic capture process started by this task itself after evidence collection completes.

## Required diagnostic A — busy-circle cadence

The user reports the Windows cursor briefly showing a busy circle approximately every one minute.

Collect enough evidence to cover at least several expected cycles, preferably 4-6 minutes if practical without blocking coordination.

Determine:

1. whether any process is created/terminated on a ~60-second cadence;
2. exact timestamps and interval distribution;
3. process name, PID, parent PID/name, command line, executable path, start/end where observable;
4. whether the parent is Task Scheduler (`taskeng.exe`, `svchost.exe` Schedule service), PowerShell/cmd, Node, Python, OpenClaw, CogentNexus, Hermes-related tooling, Defender (`MsMpEng.exe`), SearchIndexer, Explorer/dllhost, or something else;
5. whether a Scheduled Task trigger/action matches the observed cadence;
6. whether CPU/disk activity spikes align with the cadence;
7. whether the evidence supports, weakly suggests, or rules against CogentNexus/OpenClaw as the cause.

Do not claim the cursor symptom itself was directly observed unless a reliable observation/correlation mechanism exists. Distinguish temporal correlation from causation.

## Required diagnostic B — provider incident

Read-only investigate why recovery reports `READY_WITH_WARNINGS`, incident `ollama:1`, classification `provider_unreachable`, attempts 3/3 despite current Ollama probe being healthy.

Determine whether this is:

- a stale historical incident/circuit that no longer reflects current provider health;
- an actively failing periodic probe;
- a state-machine/recovery bookkeeping issue;
- or another evidence-backed cause.

Record timestamps, current provider reachability, incident state, and any relevant logs. Do not reset/clear/retry provider recovery or restart Ollama/Gateway.

## Required diagnostic C — exact-candidate deployment qualification

Reconfirm read-only:

- accepted candidate SHA `ec1fdbb2ea036c6dcd1c375b8171868335d63fc8` unless GitHub authority has changed;
- installed payload fingerprint/current runtime identity;
- whether an exact install-over would require a Gateway process boundary to load candidate code;
- precise post-deployment checks required before live Delete/recreate acceptance.

Do not deploy in Task267.

## Old Ticket hard boundary

Ticket:

`CNXT-dc11c9a0-8a89-4df5-9c48-345260725be4`

Owner intent is unproven. Task267 must not redeliver, cancel, dispose, replay, edit, or otherwise mutate this Ticket or its direct recovery. Generic continuation does not authorize semantic disposition.

Only read-only recheck is allowed to determine whether its state changed independently.

## Report requirements

Publish:

`docs/operations/coordination/reports/CNX-20260905-267-readonly-busy-cursor-provider-deployment-diagnostic.md`

Include:

- opening/final exact HEAD;
- diagnostic method and observation window;
- process-creation timeline/cadence table;
- parent/command-line evidence;
- Scheduled Task findings;
- correlation verdict for CogentNexus/OpenClaw vs Windows/other process;
- provider incident root-cause classification with evidence;
- candidate/installed identity and deployment prerequisites;
- old Ticket state read-only check;
- evidence paths/hashes where available;
- hard-fence ledger;
- PASS / BLOCKED / INCONCLUSIVE disposition;
- exact recommended successor.

After publication set `ACTIVE.md` and `STATUS.md` to `WAITING_FOR_CHATGPT_REVIEW` and stop mutation.
