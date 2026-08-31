# CogentNexus-OpenClaw Flexible Roadmap

**Updated:** 2026-08-31

This roadmap is directional, not contractual. Movement is evidence-driven: a phase advances because its gate passes, not merely because code was written.

## Architectural rule — responsibility-local data and policy

Every subsystem should define only information actually necessary to perform or verify that subsystem's own responsibility.

Before adding a parameter, default, configuration field, dependency check, or policy decision to a layer, ask:

1. does this layer need the value to perform its own operation?
2. does this layer need the value to verify its own postcondition?
3. is this layer the authority that owns the decision represented by that value?

If all three answers are no, the value should not exist in that layer.

For v0.9.3 this means, among other things, that installation remains provider-neutral while the current managed runtime/operator provider contract is Ollama only.

## Current position — repaired v0.9.3 candidate accepted

The broad lifecycle implementation baseline completed the bounded real-Windows sequence through Tasks 182–186.

Task 187 then found stale current guidance inside artifact-sensitive product surfaces. Task 188 corrected those documentation/instruction bytes.

A proportional human Dashboard requalification subsequently exposed a narrow direct-result defect: bare OpenClaw `NO_REPLY` could be marker-staged into durable visible output. Task 191 repaired that executable plugin boundary with TDD, producing frozen repaired candidate:

`050ab53f4b593ab538143084d6bbdbf7e1672e34`

Current candidate identities include:

- package payload-v2 `b1ca9f3b42009cf4b1ae0a04f0e75add8d2ff9bd5dc97fce4040dc4753562d93` / 186 files;
- plugin tree `eeab5fb8c67e5c16284d5df49ec413a53c251a13`;
- repaired Dashboard source blob `aa97d7a5411f799c612cd0aeece050085298a8bb`;
- installed skill tree `a1e873ba404205507a1623961b49f1b1a0689f9f`;
- executable skill scripts tree `3d9d323ba19443d46e970b87cef52ce878da274f`;
- facade Git blob `879083d6186589d4b2774b8fd87fa93692dd2dfc`.

Task 192 then performed exactly one supported install-over of that candidate on the accepted Windows host and exactly one genuine human Dashboard Send. The real runtime produced one Ticket, one logical run, one Ollama model call, one durable delivery, and one logical visible nonce result with no duplicate, no recovery, no pending outbox, and no bare `NO_REPLY`. Task 192 is accepted `PASS`.

The next gate is final repository reconciliation and publication, not another lifecycle test cycle.

## Short term — final v0.9.3 publication

### 1. Task-191/192 repaired candidate — complete

Repository RED/GREEN and real-Windows requalification are accepted for exact candidate `050ab53f...`.

### 2. Reconcile current `main` history — in progress

Fresh `main` contains two documentation-only commits beyond the stabilization merge base. The stabilization branch independently added/changed the same transient-stall documentation surface, so final publication must reconcile those histories explicitly rather than relying on an ambiguous PR conflict.

Requirements:

- no force push;
- preserve the current v0.9.3/Ollama-only semantics;
- preserve useful historical transient-stall evidence;
- keep Task-191/192 product candidate identity separate from later living-document/coordination commits;
- rerun CI/package proof on the reconciled branch HEAD.

### 3. Reconciled-HEAD validation

Require:

- full Validate workflow success;
- Windows Installer Pack Smoke success;
- PS5.1 Acceptance Smoke success where triggered/required;
- package dry-run success;
- package-sensitive payload identity remains `b1ca9f3b...` / 186 files unless an explicitly product-bearing change is discovered;
- no new executable/runtime/test/dependency/workflow behavior change.

If the package-sensitive identity unexpectedly changes, publication stops and the changed surface must be classified before continuing.

### 4. Final release PR

After reconciled-HEAD validation:

1. create a fresh `agent/v0.9.3-full-stabilization` -> `main` release PR;
2. keep stale PR #24 closed;
3. inspect exact topology, changed files, mergeability, and checks;
4. merge only when green and only with the expected head SHA;
5. no force push.

### 5. Release workflow and public verification

Freeze exact merged `main` SHA, then dispatch `.github/workflows/release.yml` with:

```text
version = 0.9.3
candidate_sha = <exact merged publication SHA>
```

Require successful package/publish jobs and verify:

- tag `v0.9.3` targets the exact merged SHA;
- GitHub Release is public and non-draft/non-prerelease unless intentionally specified otherwise;
- `cogentnexus-openclaw-v0.9.3.tar.gz`;
- `cogentnexus-openclaw-v0.9.3.zip`;
- `SHA256SUMS.txt`;
- published archive checksums independently match `SHA256SUMS.txt`.

## Medium term — extend continuity evidence

After v0.9.3 publication, continue proving work continuity rather than only process recovery.

Priority scenarios include:

- abrupt machine power loss and cold-boot continuation;
- high-concurrency/long-soak behavior;
- disk-full and database-corruption handling;
- stronger external side-effect adapters with idempotency/receipt/read-after-write evidence;
- explicit compatibility qualification for OpenClaw versions newer than `2026.7.1-2`.

A healthy listener is not sufficient proof that durable recovery is complete, and elapsed time alone is never recovery authority.

## Long term — durable intent across replaceable intelligence/runtime

The architectural destination is broader than a watchdog or process supervisor:

```text
human intent
-> durable accepted work
-> replaceable runtime/intelligence workers
-> failure/interruption
-> durable reconciliation
-> resume only incomplete work
-> deliver without duplicating completed effects
```

Preserve these invariants recursively as the system scales:

- durable intent outranks transient model memory;
- each layer owns only policy/data required for its responsibility;
- local failure must not silently redirect original intent;
- completed/terminal evidence must fence duplicate work;
- external irreversible effects require explicit reconciliation evidence;
- coordination scale must not weaken artifact identity or proof requirements.

## Roadmap movement rule

Move an item forward because its **evidence gate passed**, not because code was written. When evidence reveals a blocker, moving backward to create a narrower repair/requalification phase is correct behavior when it preserves the integrity of accepted evidence.
