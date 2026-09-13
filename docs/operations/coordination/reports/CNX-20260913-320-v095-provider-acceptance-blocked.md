# CNX-20260913-320 — v0.9.5 Provider Acceptance Blocked

## Result

```text
Candidate:              fc3f4bc0b1946815fb9063fb7a9d0675e1eb5a23
Runtime health:         PASS
Ollama reply path:      PASS
OpenAI reply path:      PASS
LM Studio reply path:   FAIL / UNAVAILABLE
Provider Switch:        INDETERMINATE
Idle Quiescence:        INDETERMINATE
Controlled Wake:        INDETERMINATE
Finalization:           BLOCKED
```

## Runtime evidence

```text
CogentNexus-OpenClaw: v0.9.5
CNX mode: active / managed
Generation: 99
Provider ownership: openclaw
Gateway: healthy
Ticket store: integrity ok
Supervisor: healthy
Pending outbox: 0
```

## Provider results

Ollama:

```text
Model: ollama/qwen3.8:27b
Result: PASS
```

OpenAI:

```text
Model shown in UI: GPT-5.6 Luna
Result: PASS
```

The OpenAI payload did not expose provider routing directly; the UI displayed GPT-5.6 Luna. This is recorded as the observed evidence and is not strengthened beyond that evidence.

LM Studio:

```text
Model: Qwen3.5 9B via LM Studio
Result: FAIL
Endpoint: http://127.0.0.1:1234
Reachable: false
Healthy: false
Model count: 0
Error: WinError 10061 — connection refused
```

## Gate interpretation

The LM Studio provider path is unavailable at the acceptance endpoint. Therefore full Provider Switch Acceptance cannot be claimed PASS. Idle Quiescence and Controlled Actionable Wake were not executed and remain INDETERMINATE.

No provider/model restoration or unrelated runtime mutation was performed to force the gate to PASS.

## Release state

```text
PR #38: OPEN / unchanged
Merge: None
Tag v0.9.5: None
GitHub Release: Not published
```

## Stop condition

Task 320 stops at the acceptance boundary. A successor authority is required before another live acceptance attempt. Any successor must not permit unrelated provider/model mutation merely to satisfy the acceptance gate.
