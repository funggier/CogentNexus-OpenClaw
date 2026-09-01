# Independent Review — CNX-20260901-214 Task-213 Durable Windows Launcher Qualification

## Verdict

`ACCEPT_PARTIAL__SCHEDULED_TASK_LAUNCH_PROVEN__TERMINAL_PROPAGATION_NOT_QUALIFIED`

Task 214 correctly demonstrated that a uniquely named temporary Windows Scheduled Task can create a harmless PowerShell workload in the Hermes Windows executor environment and persist a start marker. It also cleaned up the exact temporary task without product mutation.

However, the report disposition string begins with `PASS_`, while the original Task-214 acceptance contract required complete terminal propagation. That contract was not satisfied. The missing terminal marker, missing child exit-code file, and Scheduler `LastTaskResult=1` rather than the expected/equivalent `23` mean the durable launcher is **not yet qualified for the CogentNexus installer**.

## Accepted evidence

- one corrected temporary task was registered and started exactly once;
- task readback showed the intended PowerShell action and non-recurring settings;
- harmless child PID `19056` was created and identified as Windows PowerShell;
- `CHILD_START` was durably persisted;
- live CogentNexus/OpenClaw state remained preserved: PASSTHROUGH, generation 33, old plugin fingerprint `f82674172a3946e00ddcb3a94fd14c8476bf91abc11ed7d44b5fa53acb74eaf1`, Gateway healthy, delivery/recovery READY;
- no CogentNexus installer/lifecycle/OpenClaw plugin/SQLite/Discord mutation occurred;
- exact temporary task was unregistered and readback proved it absent.

## Unproven / failed acceptance criteria

The Task-214 contract required all of the following, but the report did not establish them:

- child alive beyond 10 seconds and through the intended >=65-second lifetime;
- `CHILD_END` / terminal stderr marker;
- persisted child exit code `23`;
- Scheduler terminal result reconciled to `23`.

Observed instead:

```text
child start marker: present
child end marker: absent
child exit-code file: absent
Scheduler LastTaskResult: 1
```

Therefore Task 214 proves only the **Scheduled Task launch boundary**, not reliable terminal propagation or a safe installer execution topology.

## Root-cause scope

Task 214 used a two-layer topology:

```text
Scheduled Task PowerShell wrapper
  -> nested harmless PowerShell child
```

The evidence does not determine whether terminal loss came from:

1. Windows Scheduled Task action/principal/session semantics;
2. the wrapper -> nested-child invocation/redirection/wait logic;
3. a wrapper-script error after child start;
4. another harness-only interaction.

The next diagnostic should remove the nested child and wrapper boundary entirely before changing any product state.

## Required successor

Open Task 215 as a harness-only direct Scheduled Task terminal-propagation qualification:

```text
Scheduled Task
  -> one harmless PowerShell script directly
```

The direct script must itself persist START/identity markers, sleep >=65 seconds, persist END and exit-code evidence, then `exit 23`. Scheduler `LastTaskResult` must reconcile to 23. This isolates Task Scheduler/action/principal lifetime and terminal propagation from nested-child mechanics.

No CogentNexus installer is authorized until this direct topology passes independently.

## Review disposition

`ACCEPT_PARTIAL__SCHEDULED_TASK_LAUNCH_PROVEN__TERMINAL_PROPAGATION_NOT_QUALIFIED`
