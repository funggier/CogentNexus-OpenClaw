# Review — CNX-20260827-085 Correct Attested Classification and Pending-Rollover Control Flow

Decision: `REWORK`

Disposition: `REWORK_PENDING_ROLLOVER_STILL_NESTED_UNDER_INSTALL_GATE`

Reviewed report HEAD:

`d8951eb1b724fc60236e458a78da0cef2926868d`

Implementation HEAD:

`6b5c9d56a48d4affe67c2bb718898378edee6e8a`

Execution coordination HEAD:

`0f67bdbd9e23cf1ea2761630f3dc05d36cc637eb`

## Publication fence

Accepted.

- `0f67bdb... -> 6b5c9d5...`: exactly one implementation commit.
- Implementation files are exactly:
  - `scripts/install.ps1`
  - `scripts/resolve-plugin-lifecycle-actions.ps1`
  - `skills/cogentnexus-openclaw/scripts/namespace_ownership.py`
  - `tests/test_plugin_generation_rollover.py`
- No file under `plugins/cogentnexus-openclaw/**` changed.
- `6b5c9d5... -> d8951eb...`: exactly one report-only commit adding the Task-085 report.

## Evidence accepted and preserved

The following Task-085 work is sound enough to preserve as the rework base:

1. The classification truth table now distinguishes a single manifest-owned old generation from an already-source-exact generation:
   - old fingerprint != expected source -> `upgrade`, `pendingRollover=false`, `pluginAlreadyExact=false`;
   - old fingerprint == expected source -> `upgrade`, `pendingRollover=false`, `pluginAlreadyExact=true`.
2. Explicit expected source equality is now enforced in `_exact_rollover_state()` regardless of whether retired and replacement fingerprints are equal to one another.
3. Unattested changed replacement remains rejected; explicit wrong source fingerprint remains rejected.
4. Generic two-candidate unique resolution remains fail-closed/ambiguous.
5. `scripts/resolve-plugin-lifecycle-actions.ps1` correctly returns:
   - fresh/legacy -> install=true, rollover=false;
   - ordinary upgrade -> install=true, rollover=true;
   - pending recovery -> install=false, rollover=true;
   - already exact -> install=false, rollover=false;
   - SkipPlugin -> install=false, rollover=false;
   and rejects `pending=true + exact=true`.
6. Ticket DB bootstrap was moved outside the package-install action gate for non-SkipPlugin installs.
7. Task-084 plan/apply attestation, manifest/inventory/tree/hash fencing, atomic retirement and rollback remain present.
8. No plugin payload source or live state was mutated.

These accepted pieces should not be rewritten unnecessarily.

## Blocking finding — production rollover remains nested under installPlugin

The Task-085 report states that package installation and rollover are now independent gates. The production source does not satisfy that claim.

Current `scripts/install.ps1` has the effective structure:

```powershell
if ($actions.installPlugin) {
    # npm-pack / OpenClaw plugin install
    ...

    if ($classification.mode -eq "upgrade") {
        if ($actions.rolloverPlugin) {
            # rollover-plan / rollover-apply
            ...
        }
    }
}
```

Therefore for the exact pending-recovery action tuple:

```text
installPlugin=false
rolloverPlugin=true
```

the outer `if ($actions.installPlugin)` is false, so the rollover block is unreachable.

The installer would then continue to the later strict `resolve-plugin` call while the old and newer canonical generations are both still present. Unique resolution should fail ambiguous, reproducing the same live blocker that Tasks 084/085 were intended to remove.

This is a direct violation of Task-085 Gate I2/I3 and the successor gate. No live recovery may be authorized from implementation `6b5c9d56...`.

## Why the tests missed it

The new tests execute `resolve-plugin-lifecycle-actions.ps1` directly and correctly prove the action truth table. They do not execute or structurally prove how `install.ps1` consumes those two booleans.

Thus the production helper is correct while the production caller still nests the rollover operation inside the install operation.

A source/wiring regression must inspect or execute the actual production control-flow boundary, not only the helper output.

## Required successor direction

Preserve implementation `6b5c9d56...` as the base and make the smallest source-only correction:

1. Keep the package-install block under:

```powershell
if ($actions.installPlugin) { ... }
```

2. Close that block before the rollover block.
3. Place upgrade rollover under an independent sibling gate such as:

```powershell
if ($classification.mode -eq "upgrade" -and $actions.rolloverPlugin) {
    ... rollover-plan / rollover-apply ...
}
```

4. Pending recovery must therefore execute rollover with `installPlugin=false`.
5. Ordinary upgrade must execute package install first and rollover second.
6. Already-exact must execute neither.
7. Fresh/legacy behavior must remain unchanged.
8. Rollover must finish before later strict `resolve-plugin` and ownership publication.
9. Add a PowerShell 5.1 production-AST regression against the real `scripts/install.ps1` that:
   - locates the production rollover-plan/apply commands;
   - proves they are controlled by `$actions.rolloverPlugin`;
   - proves they are **not descendants** of an `if` whose condition depends on `$actions.installPlugin`;
   - proves the package-install commands remain under `$actions.installPlugin`;
   - proves rollover source order precedes the later strict `resolve-plugin` call.
10. Keep the existing executable action-helper truth table and all classification/security tests.
11. Keep zero diff under `plugins/cogentnexus-openclaw/**`.
12. Re-run full Python, npm 11/npm 12, PowerShell 5.1, installer, recovery, semantic/delivery and baseline gates.

## Live disposition

The Task-083 two-generation PASSTHROUGH installation remains the accepted live baseline and must stay read-only.

No live install/install-over, generation cleanup, controller/ownership/AGENTS/Supervisor mutation, semantic message or Ollama probe is authorized until the successor source repair is independently accepted.
