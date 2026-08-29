# CNX-20260829-141 — Direct Retired-Storage Indirection Safety Repair

- **Task:** CNX-20260829-141
- **Verdict:** `PASS`
- **Execution mode:** `OFFLINE_DIRECT_RETIRED_STORAGE_INDIRECTION_TDD_REPAIR_ONLY`
- **Owner/executor:** ChatGPT / Hermes
- **Branch:** `agent/v0.9.3-full-stabilization`
- **Fresh starting HEAD:** `9b6d9d6028372015894b020a209d7c9866d80538`
- **Task-140 repair under rework:** `4d47629edeb8b4e0ab23f1fabee98c05f702d141`
- **Task-141 repair commit:** `138759d111fe27a0cda75f59ad108d11caf19120`
- **Evidence root:** `C:\Users\CDQ-P\AppData\Local\Temp\cnx-continue8-20260829T140100Z`

## 1. Authority and scope

A fresh clone was fetched from the authoritative branch. Fresh `ACTIVE.md` and `STATUS.md` identified Task 141 as active and unsuperseded with execution mode `OFFLINE_DIRECT_RETIRED_STORAGE_INDIRECTION_TDD_REPAIR_ONLY`. The Task-140 report and independent review were inspected.

Task 141 authorizes only offline RED-first diagnosis/repair and validation of root-level direct retired-storage filesystem indirection. It explicitly forbids live install/install-over, controller/plugin/runtime mutation, cleanup/reset/uninstall, database/Ticket mutation, provider/model/OpenClaw configuration changes, Dashboard Send/resend, semantic injection, recovery disruption, and force-push.

No live Windows runtime, controller, plugin, database, or semantic state was touched during Task 141. No Dashboard semantic Send occurred.

## 2. Exact root cause

Task 140 correctly routed a canonical real direct retired plugin directory around the managed npm-project helper. However, its `_retired_storage_root()` compared the direct root only after `Path.resolve()`. In `prepare_plugin_rollover_transaction()`, the manifest-owned path was also resolved before that check.

Consequently, this topology was indistinguishable from an ordinary real direct directory:

```text
<openclawState>/extensions/cogentnexus-openclaw  ->  <another directory inside <openclawState>>
```

The direct root could be a symlink or Windows junction/reparse point. Resolving first erased the lexical root's indirection identity, allowing the ownership code to proceed to backup creation. The managed npm-project ownership helper itself was not weakened and was not the root cause.

## 3. Genuine RED

The regression fixture recreated the accepted Task-140 direct-retired layout:

```text
<tmp>/.openclaw/
  extensions/cogentnexus-openclaw                  # canonical direct root
  extensions/redirected-retired-payload            # in-state target
  npm/projects/<generation>/node_modules/...        # managed fixture
  workspace/.cogentnexus-openclaw/ownership.json    # coherent manifest
```

The direct payload was first created as a normal real directory, and a coherent manifest bound it. The payload was then moved to `redirected-retired-payload`, and the canonical direct path was replaced with a Windows junction. The fixture asserted that the junction/reparse primitive was detected and that backup creation must not occur.

The first attempt to create a portable symlink recorded a Windows privilege error (`WinError 1314`). The fixture then used the supported unprivileged `cmd.exe /c mklink /J` fallback. The resulting junction was created successfully; the subsequent RED was semantic rather than setup-related.

RED command:

```text
uv run --no-project --with pytest python -m pytest -q \
  tests/test_plugin_generation_rollover.py \
  -k rejects_indirected_direct_retired_root_before_backup
```

RED result against Task-140 code:

```text
1 failed, 58 deselected
Failed: DID NOT RAISE RuntimeError
```

The current code proceeded through `prepare_plugin_rollover_transaction()` and created/authorized the backup transaction for the redirected direct root, proving the exact missing invariant.

## 4. Minimal owning-boundary repair

The repair adds `_is_reparse_point(path)`, which checks without resolving first:

- `Path.is_symlink()`;
- `os.path.isjunction()` when available;
- on Windows, `FILE_ATTRIBUTE_REPARSE_POINT` through `GetFileAttributesW`.

`prepare_plugin_rollover_transaction()` now preserves the manifest's lexical plugin path until `_retired_storage_root()` performs the direct-root attestation. The canonical direct root is accepted only when it is itself a real directory and its resolved identity remains inside the OpenClaw state boundary. Non-direct paths continue through the existing strict `_npm_project_for_plugin()` proof.

The repair does not broaden arbitrary extension-directory authorization, does not weaken `..` containment, does not permit symlink/junction escapes, and does not change Dashboard delivery behavior.

Changed implementation/test files:

```text
skills/cogentnexus-openclaw/scripts/namespace_ownership.py
tests/test_plugin_generation_rollover.py
```

## 5. GREEN validation

Focused regression and preservation tests:

```text
uv run --no-project --with pytest python -m pytest -q \
  tests/test_plugin_generation_rollover.py \
  -k 'rejects_indirected_direct_retired_root_before_backup or accepts_supported_direct_retired_plugin_before_npm_replacement or rollover_transaction or task114_complete_direct_classify_install_matrix'
```

Result:

```text
21 passed, 38 deselected
```

This covers:

- Windows junction/reparse root rejection before backup;
- accepted normal real direct retired directory;
- valid managed npm-project rollover;
- complete negative ownership matrix.

Relevant complete Python ownership/installer surface:

```text
uv run --no-project --with pytest python -m pytest -q \
  tests/test_plugin_generation_rollover.py \
  tests/test_namespace_install_contract.py \
  tests/test_installer_transaction_wiring.py
```

Result:

```text
74 passed in 4.34s
```

Plugin validation:

```text
npm ci --ignore-scripts
npm test
npm run build
npm run plugin:validate
```

Results:

- plugin tests: `50` files passed, `269` tests passed;
- TypeScript build: passed;
- mixed-plugin artifact verification: `PASS (45 config properties, 5 tools)`;
- ticket DB bootstrap: `PASS (9 required tables + v095 registration fence)`;
- package verification: `packedFileCount: 178`;
- `git diff --check`: passed.

## 6. Exact-SHA CI

All required workflows completed successfully on exact repair SHA `138759d111fe27a0cda75f59ad108d11caf19120`:

| Workflow | Run ID | Result |
|---|---:|---|
| PS5.1 Acceptance Smoke | `33256641609` | `completed / success` |
| Windows Installer Pack Smoke | `33256641648` | `completed / success` |
| Validate | `33256641615` | `completed / success` |

CI evidence was captured in:

`C:\Users\CDQ-P\AppData\Local\Temp\cnx-continue8-20260829T140100Z\ci-final.json`

## 7. Safety and semantic accounting

- No live Windows install/install-over/update/uninstall/reset occurred.
- No controller-mode normalization or plugin enable/disable/delete/replace occurred.
- No live runtime/database/Ticket/workflow/outbox/ack/delivery/recovery mutation occurred.
- No provider/model/OpenClaw configuration mutation occurred.
- No Dashboard Send, resend, alternate semantic injection, or Task-136/137 reuse occurred.
- No credentials or secrets were accessed or published.
- No merge, tag, release, or force-push occurred.
- Task-139's post-failure live state was not touched.

## 8. Disposition

The Task-140 functional direct-layout repair was re-tested with a meaningful root-level junction/reparse RED. The exact safety gap was proven, the lexical direct-root attestation was repaired at the owning boundary, ordinary real direct-directory and managed npm-project behavior remained GREEN, unsafe ownership cases remained rejected, and exact-SHA CI passed.

```text
PASS
```

This is an offline source-evidence PASS only. It does not authorize a live install-over retry or Dashboard semantic acceptance. A separate reviewed deployment-proof task is required.

Task 141 stops here for independent ChatGPT review.
