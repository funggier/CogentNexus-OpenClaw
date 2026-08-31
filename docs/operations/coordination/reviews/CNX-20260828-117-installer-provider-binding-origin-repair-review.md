# Independent Review — CNX-20260828-117

## Verdict

`REJECTED FOR CANDIDATE ADVANCEMENT — WINDOWS POWERSHELL REPAIR IS VALID, BUT THE INSTALLER SUBSYSTEM IS NOT YET PROVIDER-NEUTRAL`

Task 117 successfully repairs the exact Windows `scripts/install.ps1` parameter-binding surface exposed by Task 116. The TDD sequence is ordered correctly, the PowerShell production repair is narrow, the exact candidate CI reported by Task 117 is green, and no live Windows mutation was replayed.

However, the repository-level architectural invariant adopted before Task 117 execution is broader than one PowerShell file: installation must not own provider policy when provider information is not required to perform installation. The current exact candidate still violates that invariant through the POSIX installer `scripts/install.sh`.

The candidate must therefore not advance to a new real-Windows lifecycle acceptance yet. A source-only successor must make the installer subsystem consistently provider-neutral, re-run validation/CI/package proof, and return for independent review.

## Evidence accepted from Task 117

Report:

`docs/operations/coordination/reports/CNX-20260828-117-installer-provider-binding-origin-repair.md`

Task-117 TDD history:

- tests-only RED: `21f83753b6a94b31ecf98c60448c201756aebbd9`;
- PowerShell provider-neutral repair: `f079e4b2cde3dc9ed71fd873420274d9bd29b3a7`;
- exact candidate: `2a519904ce6f2ea22caa943529dc4710ccf7214c`;
- report-only closure: `efe51b0dd8b55c2d5e988b85ed2af30de6d0f4d1`.

The RED commit changed only `tests/test_provider_neutral_installer_boundary.py`. The production repair removed the PowerShell `Provider` parameter/ValidateSet/default, removed the direct `ollama` prerequisite from `install.ps1`, removed provider-specific install output, and changed the installer handoff from `enable --provider ollama` to generic `enable`.

Validate run `33181958320` is independently confirmed `completed / success` on exact candidate `2a519904ce6f2ea22caa943529dc4710ccf7214c`.

Task 117 correctly limits the deepest proven Task-116 origin to the PowerShell installer parameter-binding boundary; preserved evidence does not justify inventing a stronger caller-level origin for `3D Objects`.

## Blocking finding — POSIX installer still owns provider policy

Exact candidate `2a519904ce6f2ea22caa943529dc4710ccf7214c` still contains current production `scripts/install.sh` with all of the following provider coupling:

- `PROVIDER="ollama"`;
- public `--provider ollama` usage;
- `--provider` argument parsing and validation;
- `ollama` in the install prerequisite command loop;
- provider-specific output (`Ollama-only`, `Provider: ollama`);
- provider-specific migration comments/policy;
- final lifecycle handoff `enable --provider ollama`.

The Task-117 production commit also modifies `tests/test_v091_install_wiring.py` to continue asserting:

```python
self.assertIn('PROVIDER="ollama"', sh)
```

Therefore this is not merely an unobserved historical string. Current tests explicitly preserve provider ownership in another active installer.

## Why this blocks candidate advancement

The repository roadmap adopted the responsibility-locality rule before Task 117 execution:

> Every subsystem should define only information that is actually necessary to perform or verify that subsystem's own responsibility.

The same roadmap states that provider selection is not intrinsically installation-owned and that the installer should remain provider-neutral and use generic lifecycle handoff contracts.

Leaving `install.sh` provider-coupled while declaring the installer boundary repaired creates two different installation authority models in one candidate:

- Windows installer: provider-neutral;
- POSIX installer: provider-selecting / Ollama-hardcoded.

That is inconsistent with the repository-wide architecture and would make the frozen candidate describe different ownership boundaries by platform.

This review is not rejecting the Windows fix itself. It rejects advancement of `2a519904...` as the next full candidate because the known installer-subsystem inconsistency should be resolved before another source freeze and live acceptance.

## Required successor

Open a source/test/CI/package-only successor that:

1. preserves the accepted `install.ps1` provider-neutral repair;
2. writes tests-only RED proving `scripts/install.sh` still owns provider data/policy;
3. removes POSIX installer `PROVIDER` state and `--provider` API;
4. removes direct provider executable prerequisite from installation unless installation genuinely invokes it for an installation-owned operation;
5. removes provider-specific installation messages/comments that assert provider selection;
6. changes POSIX lifecycle handoff to generic `enable` with no provider argument;
7. updates current docs/tests/workflows that intentionally preserve POSIX installer provider coupling;
8. leaves runtime provider policy in runtime/configuration modules;
9. does not broaden runtime provider support as part of the installer repair;
10. re-runs focused/full validation and all exact-candidate CI/package proof.

No live lifecycle mutation is authorized by this review.

## Final review status

`TASK 117 SOURCE REPAIR PARTIALLY ACCEPTED; EXACT CANDIDATE 2a519904... NOT ACCEPTED FOR LIVE ADVANCEMENT`

The latest authoritative live-machine boundary remains Task 116 post-failure state. No Dashboard semantic Send is authorized.
