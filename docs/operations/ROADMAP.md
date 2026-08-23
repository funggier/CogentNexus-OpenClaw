# CogentNexus Flexible Roadmap

**Updated:** 2026-08-22

This roadmap is directional, not contractual. Items may move, split, merge, or be abandoned when better evidence or architecture appears.

## Short term — close the process-recovery reality layer

### 1. Gateway durable convergence

**Goal:** determine whether durable recovery state returns to `READY` naturally after a hard-killed Gateway has already returned healthy.

Success criteria:

- exact Gateway PID is validated before kill;
- replacement Gateway PID appears;
- no process-tree kill;
- no operator `cnx start` during observation;
- `cnx check recovery --json` is polled read-only;
- result clearly classifies natural convergence vs stuck durable marker.

### 2. Full process-level Recovery Reality suite

Once Gateway convergence semantics are correct, prove these in sequence:

- Gateway hard crash → automatic runtime recovery;
- Ollama hard crash → provider incident/recovery behavior;
- `cnx stop` → intentional stopped state with no automatic recovery;
- `cnx start` → verified return to MANAGED running state.

Success means every scenario produces durable evidence and the suite exits cleanly without using the harness to make recovery decisions for CogentNexus.

### 3. Freeze a process-level v0.9.3 candidate

Before moving upward into Ticket continuity:

- CI green for the exact candidate head;
- Windows live evidence reviewed;
- safety invariants preserved;
- no unresolved state-transition ambiguity;
- v0.9.2 Golden Baseline remains untouched.


### 4. Prove the v1.0.0 real-machine consumer lifecycle

After the process-level candidate is accepted, exercise the exact release candidate on the real Windows target through the consumer-facing path.

Required sequence and evidence gates:

1. record the candidate source commit, version, release artifact URL/path, and SHA256;
2. install from the actual release/consumer path and verify MANAGED/Ollama/Gateway readiness;
3. install the same candidate over an existing CogentNexus deployment and verify safe, idempotent convergence without first uninstalling;
4. run the documented `cnx reset` flow, answer its explicit `y` confirmation, and verify CogentNexus state returns to the documented fresh-install baseline;
5. run `cnx uninstall`, answer its explicit `y` confirmation, and verify CogentNexus-owned tasks, launchers, plugin/package state, and managed artifacts are cleanly removed;
6. verify external OpenClaw and Ollama installations and user data remain intact;
7. reinstall from the same actual release/consumer path after uninstall;
8. verify post-reinstall MANAGED/Ollama state, Gateway on 127.0.0.1:18789, Ollama on 127.0.0.1:11434, and recovery verdict `READY`;
9. require all applicable CI to be green for the exact artifact/source head and review every Windows evidence file and hash.

Every destructive or state-changing phase must have a duplicate-execution fence. A completed phase may not be repeated merely because the watcher runs again.

### 5. Prepare v1.0.0 for final review

When process recovery, install-over-existing, reset, clean uninstall, reinstall, post-reinstall readiness, artifact provenance, and CI are all accepted:

- update version/release notes and consumer installation documentation for `v1.0.0`;
- keep PR #24 Draft until its documented acceptance gates are complete;
- prepare the exact release candidate and PR for final human review;
- do not merge, tag, or publish automatically from the coordination loop.


## Medium term — prove work continuity, not only process recovery

The medium-term objective is to prove that replacing failed processes does not lose or duplicate user work.

### Active-call Gateway death

Scenario:

```text
Ticket committed
→ LLM work active
→ Gateway dies
→ Gateway returns
→ durable work state reconciled
→ only incomplete work continues
```

### Active-call Ollama death

Required distinctions:

- actual provider failure must open/advance the correct provider incident;
- a healthy but slow inference must **not** be restarted merely because it is quiet;
- Gateway failure while Ollama stays healthy must not be misclassified as provider failure.

### Host/supervisor death

Prove that CogentNexus control-plane failure itself is recoverable:

```text
Host dies
→ startup/supervisor returns
→ reads durable state
→ reconciles desired runtime/work state
```

### Delivery interruption

If a result is already durably committed but delivery is interrupted:

- reuse/redeliver the committed result;
- do not re-run inference merely to reproduce the same result;
- retain terminal/delivery fences.

### Ticket and workflow recovery matrix

Create deterministic fixtures for:

- accepted-but-not-started work;
- started-but-not-committed work;
- response-ready committed work;
- delivery pending;
- delivered/completed;
- cancelled/failed terminal work.

Each state must define what recovery is allowed to repeat and what must never repeat.

## Long term — durable intent across machine/runtime failure

The long-term destination is broader than a watchdog or process supervisor.

### Power loss and reboot continuation

Prove recovery across abrupt machine failure:

```text
user intent accepted
→ work partially progresses
→ power loss / reboot
→ runtime returns
→ durable state is authoritative
→ incomplete work resumes
```

### External side-effect safety

For operations outside CogentNexus, support or require reconciliation mechanisms such as:

- idempotency keys;
- durable receipts;
- read-after-write verification;
- external transaction identifiers;
- explicit effect adapters.

A completed Ticket alone must never be treated as proof that an arbitrary irreversible external effect may safely be repeated.

### Replaceable intelligence/runtime boundary

Move toward an architecture where OpenClaw, Ollama, individual model calls, agents, and eventually other intelligent workers are replaceable execution resources.

Continuity authority should remain in durable intent, committed work state, evidence, generation/ownership fences, and reconciliation.

### Multi-agent / large-scale direction

As CogentNexus expands, preserve the same invariant recursively:

- one intent may flow through many intelligence/execution units;
- local failures must not silently redirect the original intent;
- each layer should be able to prove what it owns, what it completed, and what remains incomplete;
- coordination scale must not weaken durable evidence or duplicate-effect safety.

## Non-goals for the current phase

These may become future work, but should not distract from current recovery proof:

- reintroducing multi-provider complexity into v0.9.3;
- optimizing cosmetic internals of the frozen v0.9.2 core;
- treating timeouts/cooldowns as recovery authority;
- claiming arbitrary exactly-once external effects without reconciliation evidence;
- expanding platform/version support before the current Windows/Ollama continuity boundary is understood.

## Roadmap movement rule

Move an item forward because its **evidence gate passed**, not because code was written.

When evidence reveals a new blocker, it is acceptable for the roadmap to move backward, split a milestone, or introduce a diagnostic phase. That is considered progress when it reduces uncertainty about the real system.