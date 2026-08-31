# CNX-20260829-140 — Installer Ownership-Boundary Rollover Diagnosis and Repair

- **Task:** CNX-20260829-140
- **Verdict:** `PASS`
- **Execution mode:** `OFFLINE_INSTALLER_OWNERSHIP_BOUNDARY_TDD_REPAIR_ONLY`
- **Owner/executor:** ChatGPT / Hermes
- **Fresh clone:** `C:\Users\CDQ-P\AppData\Local\Temp\cnx-continue7-20260829T132733Z\clone`
- **Fresh starting HEAD:** `b7caee9120337267987800405b8011e6ec337f4a` (branch tip before Task-140 repair; exact full ancestry is recorded by Git in the repair commit)
- **Branch:** `agent/v0.9.3-full-stabilization`
- **Exact Task-139 candidate context:** `16f5c396e9be0af8d1bd34824fe2993613501a6f`
- **Task-139 observed installed path:** `C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw`
- **Task-139 failure:** `plugin is not inside the managed npm projects boundary`

## 1. Authority and hard-fence confirmation

Fresh `ACTIVE.md` and `STATUS.md` identified Task 140 as active and unsuperseded with execution mode `OFFLINE_INSTALLER_OWNERSHIP_BOUNDARY_TDD_REPAIR_ONLY`. The accepted Task-139 report and review were inspected. Task 140 explicitly forbade live install/install-over/update/uninstall/reset, controller or plugin lifecycle mutation, runtime/database cleanup, provider/model/OpenClaw configuration changes, Dashboard Send/resend, semantic injection, recovery disruption, and merge/tag/release/force-push.

All work in this report was performed in the fresh offline clone. No live Windows installation command, lifecycle command, database write, Dashboard Send, semantic injection, or recovery disruption was performed during Task 140.

## 2. Reconstructed caller and ownership contract

The supported Windows installer is `scripts/install.ps1`. Its relevant caller chain is:

1. `$Workspace` defaults to `$HOME\\.openclaw\\workspace` and Task 139 passed `C:/Users/CDQ-P/.openclaw/workspace`.
2. `namespace_ownership.py expected_paths(workspace)` derives:
   - `stateRoot = workspace/.cogentnexus-openclaw`;
   - `openclawState = workspace.parent`, i.e. `C:/Users/CDQ-P/.openclaw`;
   - `skillPath = workspace/skills/cogentnexus-openclaw`.
3. The installer captures `openclaw plugins list --json`, computes the exact source plugin fingerprint, and calls `classify-install` read-only.
4. For the Task-139 existing installation, the classification selected upgrade/rollover, then the installer entered the documented native handoff by invoking the existing launcher `disable`.
5. The installer packages the candidate and calls:

```text
namespace_ownership.py rollover-prepare
  --root <workspace>/.cogentnexus-openclaw
  --workspace <workspace>
  --app-data <LOCALAPPDATA>/CogentNexus-OpenClaw
  --expected-replacement-fingerprint <candidate fingerprint>
  --backup-token <generated token>
  --transaction <stateRoot>/install-staging/plugin-rollover-transaction-<id>.json
```

6. Before the Task-140 repair, `prepare_plugin_rollover_transaction()` resolved the manifest's `pluginPath` and unconditionally called `_npm_project_for_plugin(retired_root, paths["openclawState"])`.
7. `_npm_project_for_plugin()` intentionally accepts only the exact managed layout `<openclawState>/npm/projects/<generation>/node_modules/openclaw-plugin-cogentnexus-openclaw` and rejects every other location.
8. The same ownership module already models a second supported storage form: `plugin_candidate_roots()` includes the direct path `<openclawState>/extensions/cogentnexus-openclaw`, and interrupted-rollover classification explicitly accepts that direct path as the sole allowed product evidence.

The factual Task-139 path was therefore not a boundary escape. It was the supported direct extension layout, but the prepare phase incorrectly routed it through the managed npm-project-only helper.

The categories were distinguished as follows:

- **Caller-supplied path mismatch:** not the root cause; installer passed the manifest-owned plugin path and the path matched the observed OpenClaw registration.
- **Incorrect managed-projects-root model:** not globally wrong; the npm boundary is correct for managed generation roots.
- **Path normalization/canonicalization:** not the root cause; the rejection occurred after both paths were resolved and compared with `relative_to()`.
- **Package-manager/OpenClaw layout mismatch:** the immediate contract mismatch; the prepare phase assumed npm storage while the installed payload used the direct OpenClaw extension layout.
- **Symlink/junction semantics:** not implicated; the fixture uses a real direct directory and no symlink/junction exception was added.
- **Stale generation/ownership metadata:** not implicated; the manifest points to the exact direct payload and its payload identity is valid.
- **Genuinely unmanaged path:** not the factual case; the direct path is the canonical product extension path already recognized by the product inventory/classification contract.

## 3. Genuine RED reproducer

A deterministic regression was added to `tests/test_plugin_generation_rollover.py` before the production repair.

Fixture topology:

```text
<tmp>/.openclaw/
  extensions/cogentnexus-openclaw/                    # retired direct payload
  npm/projects/<new-generation>/node_modules/
    openclaw-plugin-cogentnexus-openclaw/             # unrelated replacement fixture
  workspace/
    .cogentnexus-openclaw/ownership.json               # manifest points to direct payload
    skills/cogentnexus-openclaw/SKILL.md
    cnxclaw.cmd
  local-app-data/CogentNexus-OpenClaw/                # external backup boundary
```

The fixture uses a real directory at the direct extension path, no link/junction, controller mode `passthrough`, exact product/version metadata, and a manifest-owned retired plugin path equal to the canonical direct extension path. The expected replacement fingerprint is a valid 64-character attestation; no live state is involved.

Command run before any production edit:

```text
uv run --no-project --with pytest python -m pytest -q \
  tests/test_plugin_generation_rollover.py \
  -k prepare_accepts_supported_direct_retired_plugin_before_npm_replacement
```

The initial environment probe without pytest was recorded as a setup miss (`No module named pytest`). The ephemeral `uv` run then produced a genuine semantic RED:

```text
1 failed, 57 deselected
RuntimeError: plugin is not inside the managed npm projects boundary:
<tmp>/.openclaw/extensions/cogentnexus-openclaw
```

The stack reached `prepare_plugin_rollover_transaction()` and the unconditional `_npm_project_for_plugin()` call at the exact same ownership boundary as Task 139. This was not an unrelated fixture or cleanup failure.

## 4. Minimal production repair

Production repair commit:

```text
4d47629edeb8b4e0ab23f1fabee98c05f702d141
```

The owning boundary now uses a narrow helper:

```python
def _retired_storage_root(plugin_path, openclaw_state):
    direct_root = (openclaw_state / "extensions" / PRODUCT_ID).resolve(strict=False)
    resolved_plugin = plugin_path.resolve(strict=False)
    if resolved_plugin == direct_root:
        return resolved_plugin
    return _npm_project_for_plugin(resolved_plugin, openclaw_state)
```

Only `prepare_plugin_rollover_transaction()` uses this helper. Direct canonical retired storage is backed up as the retired storage root; every non-direct path still goes through the existing strict npm-project ownership proof. No boundary is broadened to arbitrary paths, no symlink/junction behavior is weakened, and no installer cleanup or manual normalization was added.

The production change is limited to `skills/cogentnexus-openclaw/scripts/namespace_ownership.py`. The regression fixture and assertion were added to `tests/test_plugin_generation_rollover.py`.

## 5. GREEN validation

Focused post-repair run:

```text
uv run --no-project --with pytest python -m pytest -q \
  tests/test_plugin_generation_rollover.py \
  -k 'prepare_accepts_supported_direct_retired_plugin_before_npm_replacement or task114_complete_direct_classify_install_matrix'
```

Result:

```text
18 passed, 40 deselected in 1.32s
```

Relevant complete Python ownership/installer surface:

```text
uv run --no-project --with pytest python -m pytest -q \
  tests/test_plugin_generation_rollover.py \
  tests/test_namespace_install_contract.py \
  tests/test_installer_transaction_wiring.py
```

Result:

```text
73 passed in 5.00s
```

Plugin validation surface:

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

Exact repair-SHA CI:

| Workflow | Run ID | SHA | Result |
|---|---:|---|---|
| Validate | `33255275802` | `4d47629edeb8b4e0ab23f1fabee98c05f702d141` | `completed / success` |
| Windows Installer Pack Smoke | `33255275809` | `4d47629edeb8b4e0ab23f1fabee98c05f702d141` | `completed / success` |
| PS5.1 Acceptance Smoke | `33255275804` | `4d47629edeb8b4e0ab23f1fabee98c05f702d141` | `completed / success` |

## 6. Safety and scope proof

- No live Windows install/install-over/update/uninstall/reset occurred in Task 140.
- No live controller, plugin, runtime, scheduled-task, service, provider, model, or OpenClaw configuration mutation occurred.
- No live SQLite/database/Ticket/workflow/outbox/ack/delivery/recovery mutation occurred.
- No Dashboard semantic Send, resend, alternate semantic injection, or Task-136/137 nonce/message reuse occurred.
- No credentials or secrets were accessed or included.
- No merge, tag, release, or force-push occurred.
- The Task-139 live state was not touched; the earlier `passthrough`/disabled state remains a separate accepted predecessor boundary and is not normalized by this task.

## 7. Disposition

The exact Task-139 failure is reproduced by a meaningful offline RED, the source-level root cause is proven, the smallest owning-boundary repair is applied, strict npm ownership and boundary rejection remain intact, all relevant offline validation is GREEN, and exact-SHA CI is GREEN.

```text
PASS
```

This offline PASS does **not** authorize another live install-over attempt or semantic acceptance. A separate reviewed deployment-proof task is required. Task 140 stops here for independent ChatGPT review.

## 8. Evidence and provenance

- Fresh clone and source/test evidence: `C:\Users\CDQ-P\AppData\Local\Temp\cnx-continue7-20260829T132733Z\clone`
- RED output: `C:\Users\CDQ-P\AppData\Local\Temp\cnx-continue7-20260829T132733Z\red.txt`
- Full verification output: `C:\Users\CDQ-P\AppData\Local\Temp\cnx-continue7-20260829T132733Z\full-python-tests.txt`, `npm-test.txt`, `npm-build.txt`, `npm-validate.txt`
- CI evidence: `C:\Users\CDQ-P\AppData\Local\Temp\cnx-continue7-20260829T132733Z\ci-final.json`
- Report path: `docs/operations/coordination/reports/CNX-20260829-140-installer-ownership-boundary-rollover-repair.md`
