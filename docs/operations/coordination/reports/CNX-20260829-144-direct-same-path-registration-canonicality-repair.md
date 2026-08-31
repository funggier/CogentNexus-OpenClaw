# CNX-20260829-144 — Direct Same-Path Registration Canonicality Repair

- Task ID: `CNX-20260829-144`
- Status / final verdict: `PASS`
- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`
- Fresh authority HEAD at start: `b4ff7ea6bea1dea2e7d161bdecc5bcfebe94e797`
- Production repair commit: `fb5781c1abd68280760bd5b3b4a65fabd8a60e58`
- Evidence root: `C:\Users\CDQ-P\AppData\Local\Temp\cnx144-offline-20260829T170123Z`
- Live runtime/Dashboard mutation: `0`

## Authority and scope

Fresh remote fetch confirmed the exact requested branch and HEAD `b4ff7ea6bea1dea2e7d161bdecc5bcfebe94e797`. Remote `ACTIVE.md` and `STATUS.md` both identified Task 144 as `READY_FOR_HERMES` with execution mode `OFFLINE_DIRECT_REGISTRATION_CANONICALITY_TDD_REPAIR_ONLY`.

All work was performed in a fresh detached offline clone. No live runtime, live ownership state, controller, database, provider, Gateway, or Dashboard surface was inspected or mutated.

The existing test-only RED commit was retained and used; no duplicate RED test was created.

## Genuine RED before production edit

Existing test `tests/test_task144_registration_canonicality.py` was run before editing production code. The Windows junction test failed as required against the Task-143 implementation:

```text
FAILED tests/test_task144_registration_canonicality.py::test_direct_same_path_rejects_windows_junction_registration_alias
E       Failed: DID NOT RAISE RuntimeError
1 failed, 1 skipped in 0.18s
```

The test created a distinct junction registration alias resolving to the canonical direct plugin root, while keeping the canonical root itself real. The failure demonstrated that the noncanonical lexical `rootDir` was incorrectly authorized.

Evidence: `b02-existing-red-uv.txt`.

The first attempt using the Hermes Python environment lacked `pytest` (`No module named pytest`); this setup miss is preserved in `b01-existing-red.txt`. The RED was then run successfully using an ephemeral `uv run --no-project` environment.

## Root cause

`_active_registered_plugin()` resolves the inventory `rootDir` before returning replacement identity. The finalizer still retained the raw lexical `rootDir` in `replacement["record"]` and computed a lexical `registration_key`, but only used equality with the canonical direct key to decide whether to run direct-root attestation.

A noncanonical alias/junction could therefore:

- have a lexical path different from the canonical direct root;
- resolve to the canonical direct root;
- pass payload, version, fingerprint, containment, and singular-product checks;
- obtain direct same-path finalization authority.

This violated the required canonical active-registration invariant.

## Minimal production repair

The owning finalization boundary now rejects a noncanonical lexical registration before granting direct same-path authority:

```python
if direct_transaction and registration_key != direct_key:
    raise RuntimeError("direct same-path rollover requires canonical active registration")
```

The existing direct-root real-directory/reparse attestation remains unchanged and still runs for canonical registration. Managed npm rollover rules, backup/fingerprint/manifest proofs, product-storage uniqueness, and Task-141 reparse protections were not weakened.

Production diff scope was exactly one file with two added lines:

```text
skills/cogentnexus-openclaw/scripts/namespace_ownership.py
```

## GREEN validation

Focused ownership/installer suite after the fix:

```text
83 passed, 1 skipped in 4.80s
```

The skipped test is the POSIX symlink variant on Windows. The required Windows junction alias test executed and passed.

Full Python suite with corrected repository-root import environment:

```text
497 passed, 4 skipped, 4 subtests passed in 93.85s
```

Plugin validation after `npm ci`:

- `npm test`: PASS after complete PATH restoration;
- build (`tsc -p tsconfig.json`): PASS;
- `plugin:validate`: PASS;
- mixed-plugin artifact verification: PASS (`45 config properties`, `5 tools`);
- ticket DB bootstrap verification: PASS (`9 required tables + v095 registration fence`);
- package verification: PASS (`packedFileCount=178`);
- `git diff --check`: PASS.

An earlier plugin test run failed because the child test could not resolve bare `python` after an incomplete PATH pin; the failure was preserved in `e01-plugin-validation.txt` and corrected without source changes in `e04-plugin-test-corrected.txt`.

An earlier full Python collection run failed because `PYTHONPATH` did not include the repository root; that harness issue was preserved in `d01-full-python-tests.txt` and corrected in `d02-full-python-tests-corrected.txt`.

## Exact-SHA CI

All required workflows ran against exact production SHA `fb5781c1abd68280760bd5b3b4a65fabd8a60e58` and completed successfully:

- Validate — run `33264956365`: `success`
  - https://github.com/funggier/CogentNexus-OpenClaw/actions/runs/33264956365
- Windows Installer Pack Smoke — run `33264956369`: `success`
  - https://github.com/funggier/CogentNexus-OpenClaw/actions/runs/33264956369
- PS5.1 Acceptance Smoke — run `33264956375`: `success`
  - https://github.com/funggier/CogentNexus-OpenClaw/actions/runs/33264956375

Each run reported `status=completed`, `conclusion=success`, and the exact required `headSha`.

## Publication and safety

The production repair was pushed fast-forward after the remote branch advanced from `b4ff7ea6…` to `58fb5b8…`; no force-push was used. The final production SHA is `fb5781c1…`.

No live installer, install-over, recovery, controller, ownership-manifest, database, provider, Gateway, or Dashboard action was performed. Dashboard semantic Send count is `0`.

## Conclusion

Task 144 PASS is limited to offline source/test/package/CI evidence. The canonical direct same-path A -> B path remains accepted, while lexical alias/junction registration is rejected. Managed same-path rejection and prior direct-root indirection protections remain covered.

Task 144 is complete. Stop for independent ChatGPT review; no live install completion or Dashboard durable-delivery acceptance is authorized by this task.
