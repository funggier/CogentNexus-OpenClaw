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

## Current position — accepted candidate, blocked publication

The exact candidate `f6392da3e4112ce441526d5ef19925c90a872b0b` completed the bounded real-Windows lifecycle and final Dashboard semantic/durable-delivery acceptance sequence through Tasks 182–186.

Task 187 then found that full documentation convergence requires edits inside artifact-sensitive product surfaces:

- `plugins/cogentnexus-openclaw/README.md` participates directly in the npm payload-v2 fingerprint;
- `skills/cogentnexus-openclaw/SKILL.md` and references are copied into the installed skill tree and form part of the runtime instruction surface;
- current wording in those surfaces still reflects pre-acceptance state.

Changing them creates a different product/artifact identity. Publication is therefore blocked until a corrected exact candidate receives the qualification appropriate to that changed surface.

## Short term — documentation-payload repair and requalification

### 1. Correct only the stale product documentation surface

Allowed repair scope should be tightly bounded to documentation/instruction text that must become current. Do not change production/runtime/plugin executable source, tests, dependencies, or workflow behavior merely to make release publication easier.

Required convergence includes:

- plugin package README current status;
- installed skill `SKILL.md` current status;
- stale installed skill references such as `references/architecture.md`;
- any other current guidance inside the same installed/payload tree discovered by the audit.

Historical technical notes must remain historical.

### 2. Prove changed-surface identity exactly

For the corrected candidate, record:

- exact source commit SHA;
- unchanged executable/runtime source proof against `f6392da3...`;
- new plugin payload-v2 fingerprint and file count;
- deterministic identity/hash for the installed skill tree or exact changed paths;
- `VERSION`, package, plugin manifest, and lockfile version alignment;
- release archive SHA256 values;
- GitHub Actions validation/package evidence for that exact SHA.

No moving branch name may substitute for candidate identity.

### 3. Bounded Windows requalification proportional to the change

Because the changed files are documentation/instruction-bearing rather than lifecycle executable code, do not automatically repeat every disruptive historical test. Requalification should prove the surfaces actually affected:

1. install/install-over the exact corrected candidate and verify ownership plus the new plugin fingerprint/skill bytes;
2. verify facade/controller/Gateway/Ollama/delivery/recovery health remains unchanged;
3. because `SKILL.md`/skill references are runtime instruction surfaces, run one bounded Dashboard semantic/durable-delivery turn to prove Ticket-first and single-delivery behavior remains intact;
4. repeat reset/uninstall/fresh-reinstall only if the changed candidate or installation path introduces evidence requiring those lifecycle boundaries to be re-proven.

The old Tasks 182–186 remain valid historical evidence for `f6392da3...`; the corrected candidate may inherit only unchanged-surface claims justified by explicit proof.

### 4. Final v0.9.3 release publication

After the corrected candidate is accepted:

1. re-audit living documentation and product-identity boundaries;
2. create a current `agent/v0.9.3-full-stabilization` (or successor exact candidate branch) -> `main` release PR;
3. supersede stale PR #24 rather than merging its old head/base path;
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
