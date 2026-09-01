# Independent Review — CNX-20260901-211 Task-210 Interrupted Rollover Re-entry Adjudication

## Verdict

`ACCEPT_CLASSIFICATION__NORMAL_UPGRADE_RECOVERY_BOUNDARY_PROVEN__FRESH_INSTALL_OVER_AUTHORIZATION_REQUIRED`

Task 211 is accepted as a read-only adjudication. It correctly proves that the Task-210 interruption did **not** leave the Task-207 candidate installed and did **not** leave a candidate-bound interrupted-rollover transaction that can be finalized or resumed as an already-exact replacement.

The current Windows state is instead a recoverable ordinary upgrade boundary: the prior live plugin generation remains present at its pre-Task-210 fingerprint, the controller is in PASSTHROUGH, the candidate classifier returns `mode=upgrade`, `pendingRollover=false`, `pluginAlreadyExact=false`, and no replacement path is active.

This review does not accept Task 211's label `BLOCKED_PARTIAL_FOREIGN_OR_MISMATCHED_STATE` as evidence of foreign ownership. The observed mismatch is specifically **old accepted generation versus new candidate generation**. No foreign plugin/package/version, legacy namespace, unrelated wrapper, or competing replacement was demonstrated.

## Accepted evidence

Task-207 candidate remains:

`27fe0181b3b65d555a3b0cc8354f6f7945c21c0b`

Candidate plugin fingerprint:

`d0677581d60d3d5535c65e3261dae6f50d7aeb245b8680adac0cace4c040643b`

Fresh live plugin fingerprint:

`f82674172a3946e00ddcb3a94fd14c8476bf91abc11ed7d44b5fa53acb74eaf1`

The live fingerprint equals the retained pre-Task-210 installed generation and differs from the Task-207 candidate. OpenClaw still registers the canonical product id/version/root, but the plugin is disabled and the controller remains PASSTHROUGH with startup adapter absent.

The exact candidate classifier returned:

```text
mode = upgrade
pendingRollover = false
pluginAlreadyExact = false
manifestPluginPath = canonical direct extension path
replacementPluginPath = null
legacy = []
```

Task 211 also found no Task-210 rollover transaction whose expected replacement fingerprint equals `d0677581...`.

These facts mean there is no candidate replacement transaction to finalize and no candidate generation to accept as already converged.

## Source-contract interpretation

At the exact Task-207 installer source, a normal upgrade:

1. enters the native/PASSTHROUGH install boundary;
2. stages and validates the skill/controller payload;
3. runs ticket DB bootstrap;
4. packs the candidate plugin;
5. creates a **new UUID-bound rollover transaction** only inside `plugin-rollover-prepare`;
6. requires that rollover transaction file to exist before external plugin replacement;
7. installs the local package;
8. disables the just-installed plugin while ownership finalization runs;
9. finalizes the rollover transaction;
10. restores managed runtime authority later in the installer.

Task 210 recorded `plugin-rollover-prepare` START but Task 211 proves no candidate-bound transaction file was persisted and no candidate plugin replacement occurred. Therefore Task 210 was interrupted before the durable pre-install rollover proof completed.

A new successor may authorize a **fresh normal upgrade attempt** only after a fresh read-only gate proves the same state remains coherent. This is a new explicitly authorized recovery attempt, not an implicit retry inside Task 210.

## Observer defect accepted from Task 210

Historical accepted Windows install-over evidence shows `plugin-rollover-prepare` can legitimately take approximately 430–434 seconds, while whole successful installs have taken roughly 13–14 minutes.

Task 210's executor observation timed out approximately 420 seconds after installer start, so it did not provide enough time for the historically slow rollover-prepare stage after earlier installer work had already consumed part of that budget.

The next install observer must not use a single blocking executor call whose timeout can terminate or orphan the installer. It must launch one exact installer root process, return its PID immediately, and poll that exact PID and retained streams from separate bounded probes until natural termination.

## Safety requirements for successor

Before a new installer action, require fresh proof that:

- no Task-210 installer/lifecycle process remains;
- live plugin fingerprint is still exactly `f82674172...` unless another explicitly explained product action occurred;
- candidate fingerprint is still exactly `d0677581...`;
- ownership manifest/current inventory remain coherent and unique;
- classifier still returns ordinary `upgrade`, `pendingRollover=false`, `pluginAlreadyExact=false`, no replacement path, no legacy namespace;
- no candidate-bound pending rollover transaction exists;
- Task-205 cancellation remains durable and no emittable recovery/outbox residue exists;
- SQLite integrity is `ok`;
- OpenClaw remains `2026.7.1-2` and Ollama/Gateway are healthy enough for the supported installer path.

The successor must use exactly one installer invocation. If the installer process is still alive when an individual observation call ends, continue observing the same PID; do not launch another installer. Never kill the installer merely because an observation command times out.

## Discord boundary

Task 211 consumed no Discord Send. The Task-207 semantic requalification remains deferred until a recovered install is independently proven converged. The next install-recovery task should authorize zero Discord Sends and stop for review after provenance/health proof.

## Publication boundary

Public `v0.9.3` remains immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

No tag, Release, asset, version, or product-source mutation is authorized by this review.
