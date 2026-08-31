# CogentNexus-OpenClaw Flexible Roadmap

**Updated:** 2026-08-31

This roadmap is directional, not contractual. Movement is evidence-driven: a phase advances because its gate passes, not merely because code was written.

## Architectural rule — responsibility-local data and policy

Every subsystem should define only information that is actually necessary to perform or verify that subsystem's own responsibility.

Before adding a parameter, default, configuration field, dependency check, or policy decision to a layer, ask:

1. does this layer need the value to perform its own operation?
2. does this layer need the value to verify its own postcondition?
3. is this layer the authority that owns the decision represented by that value?

If all three answers are no, the value should not exist in that layer.

For v0.9.3 this means, among other things, that installation remains provider-neutral while the current runtime/operator provider contract is Ollama only.

## Current position — corrected documentation-bearing v0.9.3 artifact

The implementation candidate `f6392da3e4112ce441526d5ef19925c90a872b0b` completed the bounded real-Windows lifecycle and final Dashboard semantic/durable-delivery acceptance sequence through Tasks 182–186.

Task 187 then found that full documentation convergence required edits inside artifact-sensitive product surfaces. Task 188 corrected the verified stale current guidance in four paths:

- `plugins/cogentnexus-openclaw/README.md`;
- `skills/cogentnexus-openclaw/SKILL.md`;
- `skills/cogentnexus-openclaw/references/architecture.md`;
- `skills/cogentnexus-openclaw/references/scheduler-adapters.md`.

The corrected package payload-v2 identity is `408167da1bfba7fa9723d1bd557f29d516ed27c27398b4e48abf9a4f294e6b5b` / 184 files. The installed skill tree is `a1e873ba404205507a1623961b49f1b1a0689f9f`. The executable scripts tree remains byte-identical at `3d9d323ba19443d46e970b87cef52ce878da274f`.

The next gate is therefore proportional changed-surface requalification, not another broad implementation stabilization cycle.

## Short term — proportional requalification and publication

### 1. Documentation-payload convergence — complete

Current product guidance has been corrected without changing production/runtime/plugin executable source, tests, dependencies, or workflow behavior. Historical technical notes remain historical.

### 2. Changed-surface identity — established

For the documentation-corrected artifact, preserve and verify:

- exact final source commit SHA at candidate freeze;
- unchanged executable/runtime source proof against `f6392da3...`;
- package payload-v2 `408167da1bfba7fa9723d1bd557f29d516ed27c27398b4e48abf9a4f294e6b5b` / 184 files;
- installed skill-tree identity `a1e873ba404205507a1623961b49f1b1a0689f9f`;
- executable scripts tree `3d9d323ba19443d46e970b87cef52ce878da274f`;
- facade Git blob `879083d6186589d4b2774b8fd87fa93692dd2dfc`;
- `VERSION`, package, plugin manifest, and lockfile version alignment;
- exact-candidate GitHub Actions/package evidence.

No moving branch name may substitute for candidate identity.

### 3. Bounded Windows requalification proportional to the change

Because the changed files are documentation/instruction-bearing rather than lifecycle executable code, do not automatically repeat every disruptive historical test. Requalification should prove the surfaces actually affected:

1. install-over the exact corrected candidate once and verify ownership plus package/installed skill identity;
2. verify the active facade and executable/runtime source remain the accepted byte identity;
3. verify controller/Gateway/Ollama/delivery/recovery/SQLite health;
4. because `SKILL.md`/references are runtime instruction surfaces, run one bounded Dashboard semantic/durable-delivery turn and prove one Ticket -> one session/run -> one Ollama call -> one durable delivery -> one logical Dashboard result;
5. repeat reset/uninstall/fresh-reinstall only if evidence from the changed candidate demonstrates a plausible lifecycle impact or a failing gate requires those boundaries to be re-proven.

The old Tasks 182–186 remain valid historical evidence for `f6392da3...`; the corrected candidate inherits only unchanged-surface claims justified by explicit proof.

### 4. Final v0.9.3 release publication

After the corrected candidate is accepted:

1. re-audit living documentation and product-identity boundaries;
2. create a current `agent/v0.9.3-full-stabilization` -> `main` release PR;
3. keep stale PR #24 closed rather than merging its old head/base path;
4. require green CI/checks;
5. merge without force push and freeze exact merged `main` SHA;
6. dispatch `.github/workflows/release.yml` with:

```text
version = 0.9.3
candidate_sha = <exact merged publication SHA>
```

7. require the Release workflow package and publish jobs to pass;
8. verify tag `v0.9.3`, exact target SHA, release notes, archives, and `SHA256SUMS.txt`.

Expected assets:

- `cogentnexus-openclaw-v0.9.3.tar.gz`
- `cogentnexus-openclaw-v0.9.3.zip`
- `SHA256SUMS.txt`

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
- each layer owns only the policy/data required for its responsibility;
- local failure must not silently redirect the original intent;
- completed/terminal evidence must fence duplicate work;
- external irreversible effects require explicit reconciliation evidence;
- coordination scale must not weaken artifact identity or proof requirements.

## Roadmap movement rule

Move an item forward because its **evidence gate passed**, not because code was written. When evidence reveals a blocker, moving backward to create a narrower candidate/requalification phase is correct behavior when it preserves the integrity of accepted evidence.
