# CNX-20260829-143 — Direct In-Place Rollover Finalization Repair

- **Task:** `CNX-20260829-143`
- **Verdict:** `PASS`
- **Execution mode:** `OFFLINE_DIRECT_IN_PLACE_ROLLOVER_FINALIZATION_TDD_REPAIR_ONLY`
- **Repository:** `funggier/CogentNexus-OpenClaw`
- **Branch:** `agent/v0.9.3-full-stabilization`
- **Task-142 failure report:** `docs/operations/coordination/reports/CNX-20260829-142-accepted-candidate-install-over-retry-and-health-proof.md`
- **Accepted production repair candidate:** `59952167f51657ae2ff900a28aae528f835f9b6e`

## 1. Scope and live-state fence

Task 143 was executed as an offline source/test/CI repair only.

No live Windows install/install-over/update/uninstall/reset was run. No controller normalization, plugin enable/disable/delete/replace, ownership-manifest mutation, runtime/database/Ticket/workflow/outbox/delivery/recovery mutation, provider/model/OpenClaw configuration change, Dashboard semantic Send/resend, crash/recovery injection, reboot, release, tag, or force-push occurred.

The Task-142 partial live state was deliberately left untouched: the direct extension already contains the Task-142 candidate payload, the plugin remains disabled, the controller remains `passthrough`, and the pre-Task-142 ownership manifest remains the durable live ownership record until a separately authorized live completion task succeeds.

## 2. Exact root cause

Task 142 proved that OpenClaw's supported direct-extension upgrade behavior is an **in-place replacement**:

1. the old manifest-owned plugin generation A was at the canonical direct path:
   `<openclawState>/extensions/cogentnexus-openclaw`;
2. `rollover-prepare` backed up and attested generation A;
3. `openclaw plugins install <candidate.tgz> --force` replaced the payload at that **same canonical path** with candidate generation B;
4. post-install inventory still registered that same direct path, but its payload fingerprint was candidate B;
5. the Task-142 installed plugin fingerprint and installed `namespace_ownership.py` hash both matched the exact candidate;
6. `finalize_plugin_rollover_transaction()` nevertheless rejected the valid transition solely because replacement path identity equaled `retiredPluginPath`:

```text
RuntimeError: replacement still points to the retired generation
ownership-safe plugin generation rollover finalization failed
```

That path inequality is a valid invariant for managed npm rollover where retired and replacement generations occupy distinct project roots. It is not a valid generation-identity proof for the supported canonical direct-extension topology, where generation identity changes by attested payload fingerprint while path identity remains stable.

The correct authority therefore must distinguish:

- **managed storage:** same-path replacement remains invalid; from
- **canonical direct storage:** same-path A -> B is valid only when the transaction proves the retired direct generation, the backup remains exact, B matches the expected source fingerprint, the fingerprint actually changed, the direct root remains a real non-reparse directory, the ownership manifest did not drift, and no conflicting product storage evidence exists.

## 3. Genuine RED before production edit

A test-only regression was committed before the production repair:

- commit: `e46056ba35879757395aa6f3ef942104422b9275`
- file: `tests/test_task143_direct_in_place_finalization.py`
- message: `test: reproduce Task 142 same-path finalization failure`

The regression reproduces the Task-142 factual order:

1. create exact direct payload A at the canonical direct extension path;
2. create a coherent ownership manifest bound to A;
3. call the real `prepare_plugin_rollover_transaction()` and preserve its backup/transaction proof;
4. replace the payload at the same direct path with distinct candidate payload B;
5. provide OpenClaw inventory registering that same path;
6. require `finalize_plugin_rollover_transaction()` to complete the attested A -> B transition.

Exact test-only SHA CI:

- Validate run: `33260069334`
- observed failing job: `99120364101`

Pre-fix result:

```text
1 failed, 459 passed, 32 skipped, 4 subtests passed
```

The new test failed at the existing Task-142 boundary:

```text
RuntimeError: replacement still points to the retired generation
```

This is a semantic RED for the production defect, not a fixture/setup failure.

## 4. Safety containment tests before production edit

Before changing production source, the Task-143 test surface was expanded in commit:

`b5ea37c89daa8cf6416379f640ee5aebc674fe01`

The tests require:

- valid canonical direct A -> B same-path finalization;
- A -> A / no fingerprint transition is rejected;
- managed npm same-path replacement remains rejected;
- backup-tree tampering is rejected;
- manifest drift is rejected;
- conflicting product storage evidence is rejected;
- a direct root changed to a symlink/Windows junction/reparse point after prepare is rejected;
- the factual Task-142 partial state classifies as `mode=upgrade`, `pluginAlreadyExact=true`, `pendingRollover=false` rather than demanding a blind plugin replay.

These tests were present before the accepted production repair.

## 5. Production repair

Accepted repair commit:

`59952167f51657ae2ff900a28aae528f835f9b6e`

Accepted production file:

`skills/cogentnexus-openclaw/scripts/namespace_ownership.py`

The accepted production diff is limited to `finalize_plugin_rollover_transaction()` (`+55/-4` relative to its clean parent). No installer flow, transaction schema, Dashboard code, runtime delivery code, provider behavior, or unrelated ownership function changed.

The finalizer now:

1. validates both expected and retired fingerprint attestations;
2. verifies the ownership manifest hash before same-path authorization;
3. verifies the backup tree still equals both the prepared backup hash and retired-generation tree hash;
4. identifies a direct transaction only when all three lexical bindings point to the canonical direct extension root:
   - `retiredPluginPath`;
   - `retiredProjectRoot`;
   - `manifestBefore.pluginPath`;
5. requires the currently registered direct root to remain a real, non-reparse directory with unchanged resolved identity;
6. preserves the old same-path rejection for every non-direct/managed transaction;
7. for direct same-path finalization only, requires:
   - expected fingerprint != retired fingerprint;
   - current replacement fingerprint == expected fingerprint;
   - backup payload fingerprint == retired fingerprint;
   - product storage inventory is exactly the one canonical direct plugin, with no competing npm/product evidence;
8. then uses the existing atomic manifest-write, verification, and fail-closed rollback/quarantine path unchanged.

The repair does not infer generation change from path alone and does not weaken managed npm ownership.

## 6. Rejected broad edit and restoration evidence

One intermediate editing attempt, commit:

`4a8423eb3e38bcdfa37b843b5cd606bd1c2bf8ef`

was inspected immediately and rejected because the file-replacement operation unintentionally removed unrelated comments/docstrings outside the intended finalizer boundary.

No claim of repair success was made from that commit. The source was restored byte-for-byte to the original pre-production-edit blob in:

`082eb4d74cc9d4faf0de088273297b167cc6f7c1`

The accepted repair `59952167...` was then made from that restored baseline and independently diff-checked to one production function only. The rejected broad edit is retained in Git history as transparent evidence, not as an accepted repair artifact.

## 7. GREEN validation on exact accepted SHA

Exact accepted SHA:

`59952167f51657ae2ff900a28aae528f835f9b6e`

### GitHub Actions

| Workflow | Run ID | Result |
|---|---:|---|
| Validate | `33260670314` | `completed / success` |
| Windows Installer Pack Smoke | `33260670376` | `completed / success` |
| PS5.1 Acceptance Smoke | `33260670357` | `completed / success` |

The full Validate matrix completed successfully on:

- Windows Python 3.11;
- Windows Python 3.14;
- Ubuntu Python 3.11;
- Ubuntu Python 3.14;
- macOS Python 3.11;
- macOS Python 3.14;
- package dry-run.

Windows Python 3.11 exact job `99121962580` recorded:

```text
498 passed, 1 skipped, 4 subtests passed
```

Additional exact-job evidence:

- PowerShell syntax checks: PASS;
- PowerShell 5.1 evidence serializer: PASS;
- PowerShell 5.1 root-process exit-code checks: PASS;
- plugin tests: `50` files / `269` tests passed;
- evaluation: PASS;
- `npm audit --omit=dev`: `found 0 vulnerabilities`;
- `npm run plugin:validate`: PASS;
- mixed-plugin artifact verification: PASS (`45` config properties, `5` tools);
- ticket DB bootstrap: PASS (`9` required tables + v095 registration fence);
- package verification: `packedFileCount: 178`.

The Windows Installer Pack Smoke and standalone PS5.1 Acceptance Smoke also completed successfully on the exact accepted repair SHA.

## 8. Preserved invariants

Task 143 preserves:

- no arbitrary same-path replacement authority;
- managed npm same-path rejection;
- source-fingerprint attestation;
- retired-generation backup proof;
- manifest drift detection;
- direct-root symlink/junction/reparse rejection;
- conflicting product-storage rejection;
- singular OpenClaw plugin registration proof;
- existing manifest final verification and rollback/quarantine semantics;
- Task-141 lexical direct-root safety repair;
- Task-138 Dashboard durable-capture repair lineage;
- zero Dashboard semantic side effects during this task.

## 9. Disposition

The Task-142 rollover-finalization defect is reproduced by a genuine pre-fix RED and repaired at the owning finalization boundary. The accepted repair authorizes a same-path transition only for an exactly attested canonical direct A -> B generation change while retaining fail-closed managed and unsafe-path behavior. The complete exact-SHA CI matrix is GREEN.

```text
PASS
```

This is **offline source/test/CI PASS only**.

It is **not** proof that the user's live installation is complete, managed, enabled, or healthy under the repaired finalizer. It does **not** authorize a Dashboard semantic acceptance run.

The Task-142 partial live state remains intentionally untouched. Task 143 stops here for independent ChatGPT review before any successor may authorize a supported live completion/install-over recovery proof.
