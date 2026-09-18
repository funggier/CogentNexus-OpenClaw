# CNX-20260918-410 — ChatGPT Review

## Decision

`ACCEPTED_BLOCKED`

Accepted classification:

`BLOCKED_DELIVERY_HAZARD`

## Independent review

The authoritative branch and CNX-410 report were re-read from GitHub.

Verified:

- remote HEAD after CNX-410 publication: `4b47e88cf8d5d851086f385de8cadadeec46d98e`;
- report blob: `fd4e232774f67b58c1b7f1a5658c31c1c6f707c9`;
- ACTIVE/STATUS: `WAITING_FOR_CHATGPT_REVIEW`;
- installer invocation count: 0;
- runtime-attestation RPC calls: 0;
- semantic/model/provider requests: 0;
- no manual durable-state mutation occurred.

Stopping at the hazard gate was correct.

## Hazard evidence

The read-only recovery check found an active marker:

- `active=true`
- reason: `CogentNexus-OpenClaw external supervisor confirmed an unresponsive Gateway`
- owner: `operator`
- recovery policy: `healthy-runtime`

At the same observation boundary:

- Gateway was healthy/reachable;
- controller was active/managed with desired Gateway running;
- supervisor snapshot reported healthy;
- provider incident was closed;
- pending outbox was 0;
- SQLite integrity was OK.

This is therefore not evidence that the Gateway is currently unhealthy. It is evidence that a recoverable restart marker has failed to retire after runtime health returned.

## Source root-cause review

The current v0.9.5 periodic Supervisor composition ultimately reuses:

`skills/cogentnexus-openclaw/scripts/host_v091.py::supervisor_tick`

for the lightweight base path.

That function:

1. validates managed/desired-Gateway state;
2. probes Gateway health;
3. classifies durable wake authority;
4. returns `idle` immediately when no durable work is actionable.

It does **not** inspect the CNX runtime maintenance marker before that idle return.

The marker is created by the hard-hang restart path through:

`_restart_unresponsive_gateway -> lifecycle restart`

with:

`recoveryPolicy=healthy-runtime`

The lower runtime lifecycle already contains the supported retirement contract:

`skills/cogentnexus-openclaw/scripts/runtime.py`

- `lifecycle start` verifies Gateway health and clears maintenance;
- the legacy heavy supervisor also clears `healthy-runtime` maintenance after health verification.

However, after v0.9.5's idle/single-wake optimization, the healthy idle fast path can bypass those retirement paths entirely.

A plausible failure sequence fully supported by source and CNX-410 evidence is:

```text
Supervisor detects Gateway hard hang
 -> lifecycle restart writes healthy-runtime marker
 -> replacement Gateway becomes healthy
 -> current recovery tick/process ends before marker retirement
 -> next periodic tick sees Gateway healthy
 -> no durable work is actionable
 -> v0.9.5 fast path returns idle
 -> marker is never reconciled
 -> check recovery remains READY_WITH_WARNINGS
 -> install hazard gate blocks
```

This is a lifecycle convergence defect in the provider-neutral idle path, not a reason to manually delete the marker.

## Repair direction

Do not clear the marker manually.

Do not reintroduce the provider-aware/legacy heavy supervisor path merely to retire this marker.

The narrow repair is:

- detect an active `healthy-runtime` marker before the no-work idle return;
- when `execute_safe=false`, report recovery pending without mutation;
- when `execute_safe=true` and Gateway is already healthy, invoke the existing provider-neutral `lifecycle start` verification path without `--provider`;
- require that supported lifecycle verification retires the marker;
- then continue normal wake classification/idle behavior.

This preserves:

- OpenClaw provider/model ownership;
- no idle provider probing;
- the single-wake architecture;
- supported maintenance retirement semantics;
- no manual durable-state edits.

## Successor

Proceed with a repository TDD repair before any second install-over attempt.

No live mutation is authorized by this review itself.

## Reviewer

ChatGPT

Human final authority: Operator
