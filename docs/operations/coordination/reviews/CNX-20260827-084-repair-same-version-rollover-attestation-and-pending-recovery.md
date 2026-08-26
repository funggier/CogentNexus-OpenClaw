# Review — CNX-20260827-084 Repair Same-Version Rollover Attestation and Pending Recovery

Decision: `REWORK`

Disposition: `REWORK_ATTESTED_CLASSIFICATION_AND_PENDING_ROLLOVER_CONTROL_FLOW`

Reviewed report HEAD:

`658eb55b5163c5d74a44ce75ca2c04f538a46ba3`

Implementation HEAD:

`0847a260d6f689f364bb096bd7857bb1dd4d58e1`

Execution coordination HEAD:

`e7acf12e354db056abb8ec39e6157fe0028e34c7`

## Publication fence

Accepted.

- `e7acf12... -> 0847a260...`: exactly one implementation commit.
- Implementation files are exactly:
  - `skills/cogentnexus-openclaw/scripts/namespace_ownership.py`
  - `scripts/install.ps1`
  - `tests/test_plugin_generation_rollover.py`
- No file under `plugins/cogentnexus-openclaw/**` changed.
- `0847a260... -> 658eb55...`: exactly one report-only commit adding the Task-084 report.

## Evidence accepted and preserved

The following Task-084 work is sound enough to preserve as the rework base:

1. The source and live Task-083 replacement fingerprints were independently measured using the existing `_plugin_payload()` four-file contract.
2. The live newer generation `g-7257c4555ca8ad21` matches the accepted source fingerprint `8fd911e3...`; the manifest-owned prior generation `g-5593cbcfff5b35d5` differs.
3. The new `plugin-fingerprint` production surface reuses `_plugin_payload()` rather than inventing another hash algorithm.
4. Rollover-plan/apply now carries an expected replacement fingerprint and re-enters `_exact_rollover_state()` at apply time.
5. Changed same-version replacement without attestation remains rejected; wrong attestation is rejected.
6. Generic two-candidate `resolve_installed_plugin()` remains ambiguous/fail-closed.
7. The existing atomic retirement, plan hash, manifest hash, inventory hash, wrapper proof, project-tree proof and rollback mechanisms remain present.
8. The report's source/test mutation accounting is consistent with the implementation diff; the live partial state was not mutated.

These items should not be reimplemented unnecessarily in the successor.

## Blocking finding 1 — pending recovery skips the rollover it is supposed to complete

Production `scripts/install.ps1` wraps both plugin installation **and the entire upgrade rollover block** under:

```powershell
if (-not $SkipPlugin -and -not $pendingRollover -and -not $pluginAlreadyExact) {
    ...
    if ($classification.mode -eq "upgrade") {
        ... rollover-plan / rollover-apply ...
    }
}
```

Therefore the exact recovery state Task 084 exists to handle — `pendingRollover=true` — makes the outer condition false. The installer skips both:

- creation of a third generation (correct), **and**
- the required attested rollover of the already-installed second generation (incorrect).

Execution then reaches the later unique `resolve-plugin` call while two canonical candidates still exist. That resolver is intentionally strict and should fail ambiguous.

This contradicts Task-084 Gate I2, which explicitly required pending recovery to skip `openclaw plugins install` **but still run rollover-plan/apply before unique resolution and ownership publication**.

## Blocking finding 2 — ordinary single-generation changed-source upgrade is rejected before install

The attested `classify_install()` path handles a single manifest-owned candidate as:

```python
if len(candidates) == 1 and manifest_owned:
    if candidates[0]["fingerprint"] != expected_replacement_fingerprint:
        raise RuntimeError(...)
    return pluginAlreadyExact=True
```

This rejects the ordinary supported install-over case where:

- one coherent manifest-owned old v0.9.3 generation exists;
- exact candidate source has intentionally changed while version remains 0.9.3.

Task-084 Gate P3/I4 required this case to return normal `upgrade` with:

- `pendingRollover=false`
- `pluginAlreadyExact=false`

so npm-pack/install can create the attested replacement and then roll it over.

The implementation instead prevents that path from starting.

## Blocking finding 3 — two equivalent old generations can bypass source-attestation equality

`_exact_rollover_state()` validates `expected_replacement_fingerprint` only when:

`replacement fingerprint != retired fingerprint`.

If two existing generations are equivalent to each other but both differ from the current candidate-source fingerprint, the explicit attested classifier can still accept the topology as pending because expected source equality is not checked in the equal-retired/replacement branch.

Task-084 Gate P2 required the **active replacement fingerprint to equal the expected source fingerprint** for attested pending recovery regardless of whether it equals the retired fingerprint.

Correct rule:

- when an explicit expected source fingerprint is supplied, the active replacement must equal it exactly;
- only legacy/unattested equivalent-generation rollover may rely solely on retired/replacement equivalence.

## Test coverage gap

The new deterministic fixture directly exercises `classify_install()`, `build_plugin_rollover_plan()` and `apply_plugin_rollover_plan()`, but does not execute or otherwise prove the production installer action branching.

Consequently it proves the ownership primitives can complete a pending rollover while missing that `install.ps1` never calls them when `pendingRollover=true`.

The successor must add a production-facing action truth-table regression so this control-flow class cannot regress silently.

## Required successor direction

Preserve Task-084 implementation as the base and make the smallest source-only repair:

1. Correct attested classification truth table:
   - single manifest-owned fingerprint == expected -> `upgrade`, exact=true, pending=false;
   - single manifest-owned fingerprint != expected -> `upgrade`, exact=false, pending=false;
   - exact two-candidate topology, active replacement == expected and all fences pass -> pending=true;
   - any attested two-candidate active replacement != expected -> fail closed.
2. Separate plugin-install and rollover decisions in `install.ps1`:
   - pending -> install=false, rollover=true;
   - already exact -> install=false, rollover=false;
   - ordinary upgrade needing replacement -> install=true, rollover=true;
   - fresh/legacy plugin creation -> preserve existing intended lifecycle without an upgrade rollover.
3. Pending recovery must run rollover-plan/apply before later unique `resolve-plugin` and ownership creation.
4. Add production-facing PowerShell 5.1-compatible tests/truth-table coverage that would fail on implementation `0847a260...`.
5. Preserve the critical fence: no changes under `plugins/cogentnexus-openclaw/**` and no live mutation.
6. Rerun all Task-084 focused/security/atomicity tests plus full Python, npm 11/npm 12 plugin, installer, semantic/delivery and baseline gates.

## Live disposition

No live recovery is authorized from Task-084 implementation.

The current Task-083 two-generation PASSTHROUGH state remains the accepted live baseline and must stay read-only until the successor source repair is independently accepted.
