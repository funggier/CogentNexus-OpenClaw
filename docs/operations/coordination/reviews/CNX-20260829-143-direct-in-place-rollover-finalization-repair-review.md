# CNX-20260829-143 — Direct In-Place Rollover Finalization Repair Review

- **Task:** `CNX-20260829-143`
- **Report:** `docs/operations/coordination/reports/CNX-20260829-143-direct-in-place-rollover-finalization-repair.md`
- **Reviewed report commit:** `5ca9692da01e000ab91d67ca4a0d18e4afabf34e`
- **Reviewed production repair:** `59952167f51657ae2ff900a28aae528f835f9b6e`
- **Disposition:** **REWORK**
- **Review date:** 2026-08-29 ICT

## Review verdict

Task 143 correctly reproduces the Task-142 same-path direct-extension finalization failure and the production repair substantially narrows same-path authority. The genuine pre-production RED and exact-SHA CI evidence are accepted.

However, the repair cannot yet be accepted because the direct same-path authorization does not actually enforce the task's required **canonical active registration** invariant at the lexical inventory boundary.

## Accepted findings

The following Task-143 findings are accepted:

1. Task 142's direct extension replacement is an in-place A -> B payload transition at the canonical path `<openclawState>/extensions/cogentnexus-openclaw`.
2. The original unconditional path-inequality guard is invalid for that storage form but remains meaningful for managed npm generation rollover.
3. A genuine pre-production RED reproduced the exact `replacement still points to the retired generation` failure.
4. The repair preserves fingerprint transition proof, backup-tree proof, manifest-drift detection, managed same-path rejection, direct-root symlink/junction/reparse rejection, and conflicting product-storage rejection for the covered cases.
5. Exact repair SHA `59952167f51657ae2ff900a28aae528f835f9b6e` has GREEN Validate, Windows Installer Pack Smoke, and PS5.1 Acceptance Smoke runs.

These establish that the functional same-path root cause and most of the intended containment model are correct.

## Blocking canonical-registration finding

`_active_registered_plugin()` reads the raw OpenClaw inventory `rootDir`, then immediately resolves it:

```python
root_text = record.get("rootDir")
active_root = Path(root_text).resolve(strict=False)
```

The returned payload therefore uses the resolved root as `replacement["root"]`, while the original lexical inventory path survives only in `replacement["record"]["rootDir"]`.

The Task-143 finalizer computes both values:

```python
registration_root = replacement["record"].get("rootDir")
registration_key = os.path.normcase(os.path.abspath(str(registration_root)))
...
if direct_transaction and registration_key == direct_key:
    # direct-root real-directory / reparse checks
    ...

same_path = _canonical(replacement["root"]) == transaction["retiredPluginPath"]
if same_path:
    if not direct_transaction:
        raise ...
    # authorize direct same-path transition
```

The critical problem is that `registration_key == direct_key` is used only as a condition for performing the direct-root attestation. A noncanonical lexical `rootDir` is **not rejected**.

Therefore an inventory record whose `rootDir` is an alias/symlink/junction path that resolves to the canonical direct plugin root can produce:

- `registration_key != direct_key`;
- `replacement["root"]` resolved to the canonical direct root;
- `same_path == True`;
- `direct_transaction == True`;
- exact expected candidate fingerprint;
- exact old backup/fingerprint proof;
- product inventory containing only `directPlugin`.

In that state the canonical-registration check is skipped, but the same-path transition can still be authorized.

This is especially important because `_active_registered_plugin()` performs containment **after resolution**. A lexical alias outside the intended canonical registration location that resolves back into the direct root can also lose its lexical identity before the containment/identity proof.

## Why current tests and CI do not close this

The Task-143 tests cover:

- canonical direct A -> B success;
- no-transition rejection;
- managed same-path rejection;
- backup tamper;
- manifest drift;
- conflicting product storage;
- the canonical direct root itself becoming a symlink/junction/reparse point;
- Task-142 partial-state re-entry classification.

They do not cover an **inventory registration alias** where the canonical direct root remains a real directory but `plugins[].rootDir` is a different lexical path resolving to it.

The exact-SHA CI is therefore genuinely GREEN for the current covered surface, but it does not prove the canonical-registration invariant required by Task 143.

## Required rework

Open the narrow successor:

`CNX-20260829-144 — Direct same-path registration canonicality repair`.

The successor must produce RED before production edit for a noncanonical `rootDir` alias resolving to the canonical direct plugin root, then make the smallest owning-boundary repair that rejects lexical noncanonical registration before granting direct same-path authority.

Required preservation:

- canonical real direct root + canonical inventory registration + exact A -> B transition remains accepted;
- managed npm rules remain unchanged;
- direct-root symlink/junction/reparse rejection remains strict;
- expected/retired fingerprint transition, backup proof, manifest immutability, product-storage singularity, package/version attestation, and rollback/quarantine semantics remain unchanged;
- Task-142 partial-state re-entry classification remains deterministic;
- no live Windows/runtime/Dashboard mutation occurs.

## Deployment disposition

No live install-over, recovery completion, normalization, plugin enablement, or Dashboard semantic Send is authorized. The Task-142 partial live state remains evidence and must stay untouched until this rework is independently accepted.
