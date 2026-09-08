# CNX-20260907-311 — Exact candidate live spinner requalification

Disposition: `BLOCKED_RESIDUAL_DURABLE_HINT_HEAVY_WAKE`
Observed UTC: 2026-09-07T21:35Z–21:48Z
Exact installed candidate: `79ddec2190b226b2f5cc906144a04859b3eca748`

## Supported install

- detached candidate worktree HEAD verified exact and clean;
- supported `scripts/install.ps1` invocation count: `1`;
- retry count: `0`;
- exit: `0`.

## Installed parity and health

- candidate/installed plugin fingerprint: `9af4712dd3265afc577a233b4716279901b9eab1128ad6640c63e0ba846f0f33`;
- repaired `host_control.py`, `host_control_v091.py`, `host_control_v092.py` and Task309 `supervisor_quiescence.py`: byte-exact;
- all retained owner files exact;
- Gateway and Ollama HTTP: `200`;
- Scheduled Task: enabled, Ready after cycles, result `0`;
- quiescence lease absent.

## Durable safety

Pre-install, post-install, and post-observation normalized durable SHA-256 remained:

`6779f2dcd573526e8aea67bc2499355d2096ab34805906e632cb23835bd42e1f`

SQLite integrity remained `ok`; protected promotion/delivery-due predicates remained false. No protected row or semantic transport was mutated.

## Spinner/process observation

A 135-second read-only fallback sampler covered three distinct Scheduled Task last-run values. WMI ProcessStartTrace was attempted first but Windows returned `Access denied`; no privilege/configuration change was made.

Observed after Task310 repair:

- delegated standalone `host_v092.py` child starts: `0` (repair proven);
- `host_control_v092.py` scheduled entry processes: present;
- `runtime.py lifecycle status`: present each cycle;
- `runtime.py supervisor tick --execute-safe`: present each cycle;
- `openclaw.cmd gateway status`: present each cycle.

Therefore Task310 materially removed one delegate layer but did not close the user-visible PT1M process-chain symptom.

## Deeper root cause

Fresh predicates were:

```text
gatewayFast=true
providerFast=true
durableWorkHint=true
```

Read-only aggregate evidence found one pending assistant-delivery row whose owner session is exact-generation/active but approximately 69,140 seconds stale; it is a Direct ticket and is not the protected Ticket. The row is not actionable under the existing 15-minute delivery-due authority, yet `durable_work_hint()` treats any pending assistant delivery as an unconditional wake. It has accumulated 685 attempts. This broad wake forces the heavy legacy supervisor every minute.

## Safety disposition

No database/Ticket/session/manual transport mutation is authorized as a workaround. Task312 must repair the wake predicate in source with TDD, independent review and exact-SHA CI before another supported install.

Evidence root:

`C:\Users\CDQ-P\AppData\Local\Temp\cnx-release-20260907T134252Z\task311-evidence`
