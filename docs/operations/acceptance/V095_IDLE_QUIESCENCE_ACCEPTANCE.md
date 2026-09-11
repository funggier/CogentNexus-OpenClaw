# v0.9.5 Idle Quiescence Acceptance

## Purpose

Verify on Windows that a healthy CogentNexus-OpenClaw runtime remains quiescent when no durable work is actionable, while an exact durable wake is still observable when it exists.

This procedure is an acceptance protocol, not a performance benchmark. The expected property is absence of false-positive heavy work, not a particular scheduler cadence.

## Preconditions

- CogentNexus-OpenClaw is installed and in `MANAGED` mode.
- OpenClaw Gateway is healthy and its connectivity probe succeeds.
- No actionable Ticket, Direct recovery, or assistant-delivery item exists before the observation window.
- No explicit local Ollama recovery command is issued during the idle observation.
- The observation is performed on the target Windows machine under the same account/context used by the scheduled Supervisor.

## Idle observation

1. Record the current UTC time as the observation start.
2. Observe at least two scheduled Supervisor cadences.
3. Preserve the Host/Supervisor structured output or log records generated during that window.
4. Verify that idle records report `wakeReason=idle/no-actionable-work` and `heavyPath=false`.
5. Verify that no CNX-attributable repeated process chain, provider restart, configuration mutation, or Gateway lifecycle action occurs during the idle window.
6. Run the read-only evidence checker against the captured records:

```powershell
python scripts/check_v095_idle_quiescence.py `
  --root "$env:USERPROFILE\.cogentnexus-openclaw" `
  --log "C:\path\to\captured\host.log" `
  --json
```

## Expected idle result

The checker reports `verdict=PASS` with:

- `heavySupervisorCalls = 0`
- `providerRecoveryActions = 0`
- `configMutations = 0`
- `gatewayLifecycleActions = 0`
- `idleTicks >= 2`

A missing or unusable observation is `INDETERMINATE`; it must not be converted to PASS by inference.

## Controlled actionable wake

After the idle case is captured, introduce exactly one authorized durable work item in a controlled test environment. Capture the corresponding Supervisor record and run the checker again.

Expected behavior:

- exactly one wake is attributable to the durable authority;
- the record identifies the wake authority and work item where available;
- the checker records the heavy wake without treating the observation as evidence of a false-positive idle loop;
- no second independent wake owner is introduced for the same work item.

For delivery recovery, retain the delivery ID, Ticket ID, owner session key, owner generation, and claim/lease evidence in the acceptance record.

## Evidence retention

Archive:

- the exact command used to run the checker;
- the checker JSON output;
- the bounded observation log;
- the UTC start/end timestamps;
- the runtime state snapshot used for context, without modifying it during the check.

The checker itself is read-only and must not reset, claim, mutate, retry, restart, or otherwise repair runtime state.

## Verdict rules

`PASS` means the observation contains sufficient structured evidence and the measured counts satisfy the expected contract.

`FAIL` is reserved for an observed contract violation, such as repeated heavy activity or unauthorized provider/Gateway/configuration work during an idle observation.

`INDETERMINATE` means the evidence is absent, malformed, or insufficient to establish the contract. Never treat `INDETERMINATE` as PASS.
