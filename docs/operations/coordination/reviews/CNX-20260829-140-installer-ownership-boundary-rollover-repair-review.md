# CNX-20260829-140 — Installer Ownership-Boundary Rollover Repair Review

- **Task:** `CNX-20260829-140`
- **Report:** `docs/operations/coordination/reports/CNX-20260829-140-installer-ownership-boundary-rollover-repair.md`
- **Reviewed report commit:** `d9fbd1be4a6f33f3b3a3750a34551226364123d6`
- **Reviewed production repair:** `4d47629edeb8b4e0ab23f1fabee98c05f702d141`
- **Disposition:** **REWORK**
- **Review date:** 2026-08-29 ICT

## Review verdict

Task 140 correctly proved the Task-139 direct-extension-vs-managed-npm ownership mismatch and its positive regression is meaningful. The exact-SHA CI evidence is also real and GREEN.

However, the proposed repair cannot yet be accepted because it broadens mutation authorization to the canonical direct extension path without proving the required root-level filesystem-indirection safety invariant.

## Accepted findings

The following Task-140 findings are accepted:

1. Task 139's observed retired plugin path was the canonical direct OpenClaw extension path `.../.openclaw/extensions/cogentnexus-openclaw`.
2. Before the repair, `prepare_plugin_rollover_transaction()` unconditionally routed that retired path through `_npm_project_for_plugin()`, which only accepts the isolated managed npm-project layout.
3. The new direct-directory RED reproduced that exact failure boundary before production edit.
4. The minimal functional change in `4d47629e...` makes an ordinary real direct extension directory eligible as retired storage while retaining `_npm_project_for_plugin()` for every other resolved path.
5. Targeted Python tests, full relevant Python tests, plugin tests/build/validation, and all three exact-SHA workflows reported GREEN.

These findings establish the functional root cause and the intended ordinary-direct-directory behavior.

## Blocking safety finding

The new helper is:

```python
def _retired_storage_root(plugin_path: Path, openclaw_state: Path) -> Path:
    direct_root = (openclaw_state / "extensions" / PRODUCT_ID).resolve(strict=False)
    resolved_plugin = plugin_path.resolve(strict=False)
    if resolved_plugin == direct_root:
        return resolved_plugin
    return _npm_project_for_plugin(resolved_plugin, openclaw_state)
```

This performs the direct-layout authorization only **after** resolving filesystem indirection.

The surrounding ownership module explicitly treats symlink/reparse indirection as non-attestable at payload-file boundaries, but the direct retired root itself is not lstat/reparse-attested before resolution. `verify_manifest(..., verify_plugin=False)` proves that the resolved plugin remains contained by the OpenClaw state boundary; it does not prove that the lexical manifest-owned direct root itself is a real directory rather than a symlink/junction/reparse point.

Therefore a canonical direct path that is replaced by an indirection to another directory **inside** `.openclaw` can satisfy both:

- the manifest containment check after resolution; and
- `resolved_plugin == direct_root` after both sides resolve to the same target.

That state was rejected by the pre-Task-140 prepare path because every direct path failed the strict npm-project boundary. The Task-140 repair therefore introduces a new mutation-authorized case without the negative RED/GREEN proof required by Task 140's own safety contract.

An escape outside `.openclaw` remains rejected by manifest containment, so this review is not claiming an arbitrary outside-state deletion path. The narrower issue is **root-level filesystem indirection inside the state boundary**.

## Why CI GREEN is insufficient

The exact repair-SHA workflows are GREEN, including Windows validation. The new test only covers a real direct directory. No Task-140 test demonstrates that a direct retired root which is itself a symlink/junction/reparse point is rejected before backup/rollover mutation.

GREEN therefore proves the covered functional contract, not the missing ownership-safety invariant.

## Required rework

Open the narrowest offline successor:

`CNX-20260829-141 — Direct retired-storage filesystem-indirection safety repair`.

The successor must:

1. add a deterministic RED showing the current `4d47629e...` behavior incorrectly authorizes root-level filesystem indirection at the canonical direct extension path;
2. cover at least a portable symlink-to-another-in-state-directory case;
3. cover Windows junction/reparse semantics through a real Windows test where reliable, or through a narrowly testable root-attestation helper plus Windows CI evidence;
4. make the smallest repair at the direct retired-root attestation boundary;
5. preserve Task-139's legitimate ordinary real direct-directory topology;
6. preserve managed npm-project rollover behavior;
7. preserve rejection of outside-state paths, arbitrary siblings, wrapper ambiguity, and malformed ownership evidence;
8. run focused RED/GREEN, the full relevant installer/ownership surface, plugin validation/build, `git diff --check`, and exact-repair-SHA CI;
9. remain entirely offline with respect to the user's live Windows runtime.

## Deployment disposition

No live install-over retry is authorized. The repaired Dashboard candidate remains not proven live-installed. The Task-139 post-failure runtime state must remain untouched until this rework is reported and independently accepted.
