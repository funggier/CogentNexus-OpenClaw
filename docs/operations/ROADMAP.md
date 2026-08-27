# CogentNexus-OpenClaw Flexible Roadmap

**Updated:** 2026-08-28

This roadmap is directional, not contractual. Items may move, split, merge, or be abandoned when better evidence or architecture appears. Movement is evidence-driven: a phase advances because its gate passes, not merely because code was written.

## Short term — finish v0.9.3 repository stabilization and freeze the exact candidate

### 1. Phase I — living documentation cleanup

Keep current operational guidance aligned with the repository that will become the candidate:

- `docs/operations/STATUS.md`, `ROADMAP.md`, and `DECISIONS.md` reflect the current stabilization phase;
- clean-reinstall documentation matches the implementation-owned external backup boundary;
- current user command examples are checked programmatically against the v0.9.3 facade/delegated CLI surface where practical;
- historical release notes, completed coordination reports, and retained evidence remain historical and are not rewritten as current guidance.

### 2. Phase J — security and repository hygiene

Before candidate freeze:

- scan tracked files for accidental credentials/secrets and classify test placeholders separately;
- audit ignored/generated artifacts so runtime databases, logs, caches, local credentials, and unintended build residue are not tracked;
- run the current npm production dependency audit and perform an appropriate Python dependency review;
- review OpenClaw compatibility metadata against the actual validated guarantee of `2026.7.1-2` instead of silently promising a broader range than evidence supports.

Do not perform broad dependency upgrades merely to make audit output quieter during stabilization. Any change must have a concrete compatibility or security reason and its own verification evidence.

### 3. Phase K — final repository audit and exact-candidate freeze

Freeze one exact v0.9.3 candidate only after all repository gates are green.

Required identity/evidence includes:

- exact source commit SHA;
- package version;
- payload-v2 fingerprint;
- payload file count;
- archive SHA256 values;
- GitHub Actions matrix/package proof for that exact source;
- final review that current docs, release workflow policy, namespace isolation, and compatibility metadata all describe the same candidate.

After freeze, no source modification may be treated as the same candidate. Any source change creates a new candidate identity and requires re-verification.

### 4. Bounded real-Windows acceptance of the frozen candidate

Only after Phase K freezes the exact candidate, exercise the real Windows target through a separately authorized task.

Required lifecycle sequence remains:

1. record the frozen candidate identity and archive checksums before mutation;
2. install the exact candidate and verify MANAGED/Ollama/Gateway readiness;
3. install the same candidate over an existing CogentNexus-OpenClaw deployment and verify safe convergence;
4. run the documented `cnxclaw reset` flow with explicit `y` confirmation and verify fresh-state reconstruction;
5. run `cnxclaw uninstall` with explicit `y` confirmation and verify only CogentNexus-OpenClaw-owned surfaces are removed;
6. verify external OpenClaw, Ollama, models/data, and unrelated namespaces remain intact;
7. reinstall the same frozen candidate after uninstall;
8. verify post-reinstall MANAGED/Ollama state, Gateway on `127.0.0.1:18789`, Ollama on `127.0.0.1:11434`, and recovery readiness;
9. perform the final bounded Dashboard semantic/durable-delivery acceptance probe only after lifecycle readiness is proven;
10. retain commands, exit codes, artifact hashes, runtime evidence, and duplicate-execution fences for every disruptive phase.

A completed disruptive phase must never be repeated simply because a watcher or coordination loop runs again.

### 5. Explicit human release review and publication decision

Repository stabilization and live acceptance do not automatically publish a release.

After the frozen candidate and real-Windows evidence are accepted:

- review version/release notes and consumer installation guidance;
- review the exact source/artifact identity intended for publication;
- update or replace the older Draft PR path as appropriate for the accepted candidate;
- merge/tag/publish only as a separate explicit human-controlled action;
- never publish because a development or `release/v*` branch was merely pushed.

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

Prove that CogentNexus-OpenClaw control-plane failure itself is recoverable:

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

For operations outside CogentNexus-OpenClaw, support or require reconciliation mechanisms such as:

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

As CogentNexus-OpenClaw expands, preserve the same invariant recursively:

- one intent may flow through many intelligence/execution units;
- local failures must not silently redirect the original intent;
- each layer should be able to prove what it owns, what it completed, and what remains incomplete;
- coordination scale must not weaken durable evidence or duplicate-effect safety.

## Non-goals for the current repository-stabilization phase

These may become future work, but should not distract from the exact v0.9.3 candidate boundary:

- reintroducing multi-provider complexity into v0.9.3;
- rewriting the frozen v0.9.2 historical release;
- treating timeouts/cooldowns as recovery authority;
- claiming arbitrary exactly-once external effects without reconciliation evidence;
- broadening supported OpenClaw versions without corresponding evidence;
- starting live install/reset/uninstall/restart/semantic acceptance before Phase K freezes the candidate;
- publishing a release automatically from branch activity.

## Roadmap movement rule

Move an item forward because its **evidence gate passed**, not because code was written.

When evidence reveals a new blocker, it is acceptable for the roadmap to move backward, split a milestone, or introduce a diagnostic phase. That is progress when it reduces uncertainty about the real system.
