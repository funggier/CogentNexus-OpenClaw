# CNX-20260913-321 — v0.9.5 Idle Evidence Blocked

## Result

```text
Candidate: fc3f4bc0b1946815fb9063fb7a9d0675e1eb5a23
Candidate-sensitive validation: PASS
Runtime health: PASS
OpenAI: PASS
Ollama: PASS
Idle Quiescence: INDETERMINATE
Controlled Wake: NOT RUN
Finalization: BLOCKED
```

## Runtime snapshot

```text
cnxMode=active
Generation=99
Provider ownership=openclaw
Gateway=healthy
Ollama=healthy
```

## Idle checker evidence

```json
{
  "verdict": "INDETERMINATE",
  "heavySupervisorCalls": 0,
  "providerRecoveryActions": 0,
  "configMutations": 0,
  "gatewayLifecycleActions": 0,
  "idleTicks": 0,
  "observationRecords": 0,
  "parseErrors": 0,
  "reason": "no parseable evidence records in observation window"
}
```

The zero observation records mean the required idle contract cannot be proven. No PASS is inferred from runtime health or absence of failures.

## Decision

Task 321 stops at the evidence boundary. No code defect was identified and no candidate change is required.

A successor authority is required to diagnose the idle observation/evidence path using bounded read-only diagnostics, then collect the required two idle cadences before Controlled Wake.

## Release state

```text
PR #38: OPEN / unchanged
Merge: None
Tag v0.9.5: None
GitHub Release: Not published
```
