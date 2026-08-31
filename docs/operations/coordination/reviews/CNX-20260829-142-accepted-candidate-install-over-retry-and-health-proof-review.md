# CNX-20260829-142 — Accepted Candidate Install-Over Retry and Health Proof Review

- **Task:** `CNX-20260829-142`
- **Report:** `docs/operations/coordination/reports/CNX-20260829-142-accepted-candidate-install-over-retry-and-health-proof.md`
- **Reviewed report commit:** `6120bc068c6665b60042b0efa2fcd92821507b39`
- **Deployment candidate:** `138759d111fe27a0cda75f59ad108d11caf19120`
- **Disposition:** **ACCEPT**
- **Accepted execution verdict:** `FAIL_INSTALL_OVER`
- **Review date:** 2026-08-29 ICT

## Review verdict

Task 142 is accepted as a correctly controlled failed deployment attempt. This is **not** acceptance of a successful install-over and does not authorize Dashboard semantic acceptance.

The executor performed the one authorized supported `scripts/install.ps1` invocation, stopped after the first installer failure, and preserved the resulting live state for review. The failure evidence is coherent and materially narrows the remaining product defect.

## Accepted execution evidence

The following are accepted:

1. Read-only preflight matched the accepted Task-139 predecessor boundary: controller `passthrough`, one disabled canonical plugin identity, old plugin fingerprint, healthy Gateway/Ollama, recovery/delivery READY, SQLite integrity `ok`, pending outbox `0`, and unchanged semantic counts.
2. The exact detached source candidate was `138759d111fe27a0cda75f59ad108d11caf19120`.
3. Candidate package provenance and source attestation were captured before mutation.
4. Exactly one supported installer invocation occurred.
5. There was no manual pre-normalization, alternate plugin installation path, retry, reset, cleanup, uninstall, or Dashboard semantic Send.
6. The installer advanced farther than Task 139: the direct extension payload was replaced with the exact candidate plugin fingerprint and the installed `namespace_ownership.py` matched the exact candidate source hash.
7. The installer then failed at ownership rollover finalization with:

```text
RuntimeError: replacement still points to the retired generation
ownership-safe plugin generation rollover finalization failed
```

8. After failure, the plugin identity remained singular, the candidate payload remained at the canonical direct extension path, the plugin remained disabled, controller remained `passthrough`, Gateway/Ollama remained healthy, recovery/delivery remained read-only READY, SQLite remained `ok`, and semantic database counts remained unchanged.

## Source-level root cause boundary

The failure is now narrow enough to prove the source-level contradiction that must be repaired offline.

For Task 142's accepted direct-extension topology:

```text
<openclawState>/extensions/cogentnexus-openclaw
```

`rollover-prepare` snapshots the retired payload and records that canonical path as `retiredPluginPath`. The supported `openclaw plugins install <package> --force` then replaces the plugin payload **at that same direct path**. Task-142 post-failure evidence proves the payload at that path changed from the old fingerprint to the exact candidate fingerprint.

`finalize_plugin_rollover_transaction()` first proves that the active replacement fingerprint equals `expectedReplacementFingerprint`, then unconditionally rejects when:

```python
_canonical(replacement["root"]) == transaction["retiredPluginPath"]
```

with `replacement still points to the retired generation`.

That inequality is valid for distinct managed npm generation roots, but it is not a valid generation-identity proof for the accepted direct-extension storage form where OpenClaw performs an in-place payload replacement at one canonical path.

Therefore the direct-storage prepare contract added in Tasks 140/141 is incomplete at finalization: prepare now recognizes a real canonical direct retired root, while finalize still assumes every valid replacement must have a different path.

## Important containment rule

The repair must **not** be implemented by simply deleting the path-inequality guard.

Same-path finalization may be authorized only for a rigorously proven canonical direct-storage transition. At minimum the implementation/test contract must preserve all of these facts:

- retired storage was the exact canonical real direct extension root;
- root-level symlink/junction/reparse indirection is rejected;
- the pre-install backup exactly attests the retired payload/tree;
- the current active registration is singular and canonical;
- the current payload fingerprint equals the expected source fingerprint;
- the expected/current replacement fingerprint is a real transition from the retired fingerprint when a rollover transaction exists;
- the ownership manifest has not changed since prepare;
- conflicting product storage evidence remains rejected;
- managed npm generation rollover retains its distinct-generation ownership rules.

## Live-state disposition

Task 142 left a partially transitioned but observed state:

- plugin payload: exact Task-142 candidate fingerprint `12c6d1b5b6ffd938353dd60c5d6190c34a609663369f619ff4fc7cbd176119e0`;
- installed `namespace_ownership.py`: exact Task-142 candidate hash `e51f03553a24ea67037a3131b5ff4edb8aa435fbbc82b19974ae18f0d03df666`;
- one canonical plugin identity, disabled;
- controller `passthrough`;
- existing ownership manifest preserved, with pre-attempt `installedAt` value;
- Gateway/Ollama healthy;
- recovery/delivery READY and pending outbox `0`;
- semantic database counts unchanged;
- Dashboard semantic Send count `0`.

This state must **not** be manually normalized or opportunistically replayed while the finalizer defect remains uncorrected. A future supported installer run may classify the plugin payload as already exact, but using that as a workaround would leave the direct in-place finalization bug present for subsequent upgrades.

## Required successor

Open the narrow offline task:

`CNX-20260829-143 — Direct in-place rollover finalization repair`.

It must produce a genuine RED for the Task-142 same-path replacement sequence before production edit, make the smallest ownership-safe repair, prove negative containment cases, verify the Task-142 partial-state re-entry classification offline, run the complete relevant installer/ownership/package/build/CI surface, publish its report, and stop for independent review.

## Deployment disposition

No new live install-over, normalization, recovery mutation, or Dashboard semantic Send is authorized by this review. The next step is offline source repair only.
