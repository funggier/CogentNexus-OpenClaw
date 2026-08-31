# Independent Review — CNX-20260828-107

- Review status: COMPLETE
- Review verdict: **ACCEPTED FAIL — SOURCE DEFECT CONFIRMED**
- Reviewed task: `CNX-20260828-107-v093-real-windows-lifecycle-acceptance-retry`
- Reviewed report commit: `582acb72dd09d1e3753452afcb5f76aa72929d5d`
- Acceptance candidate source: `b14a711f24b3fd1cd0aaa51ce636c8502ba42404`
- OpenClaw baseline: `2026.7.1-2`
- Managed provider: Ollama only
- Reviewer: ChatGPT
- Review date: 2026-08-28

## Reviewed candidate identity

Task 107 used the exact candidate authorized by its task contract:

- Version: `0.9.3`
- Source commit: `b14a711f24b3fd1cd0aaa51ce636c8502ba42404`
- Payload file count: `178`
- Payload-v2 fingerprint: `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`
- Inner ZIP SHA256: `3079ea8289d3ed465337b4621cb771eb1971d4ba7d86eb09d94d81875c049e1b`
- TAR.GZ SHA256: `5a010879d6effd3ee0ecbc449a6cffb30ecd26e91b90fb08765636c31d6a3b05`
- Package-proof artifact ID: `9677072214`
- Package-proof outer SHA256: `b02dc802e2ea71ed18a12071ab570236864cea5c72416b8fae6ac9607f710b76`
- Validate: run `33149370021` — success
- PS5.1 Acceptance Smoke: run `33149369996` — success
- Windows Installer Pack Smoke: run `33149369983` — success

The Task 105 pre-fix artifact remained excluded as required.

## Independent findings

### 1. Task 107 respected the acceptance gate

The report shows one authorized Phase 2 install-over attempt. After the first non-zero result, execution stopped. Reset, uninstall, fresh reinstall, normal lifecycle, and disruptive recovery phases were not replayed or started. No Dashboard semantic message was sent.

This is the correct behavior for a destructive single-attempt acceptance task.

### 2. The Task 105 npm-12 / `npm-pack:` defect is repaired at the previously failing boundary

The fixed candidate reached and successfully executed the local-package installation path:

```powershell
openclaw plugins install $packagePath --force
```

The Task 107 failure therefore does not reproduce the old npm-12 metadata defect. The previous repair remains supported by this real-Windows attempt.

### 3. A new source-level transaction defect is exposed

The Windows installer currently performs the external OpenClaw plugin mutation before asking the CogentNexus ownership layer to construct the rollover plan:

1. package the candidate plugin,
2. execute `openclaw plugins install $packagePath --force`,
3. query replacement plugin inventory,
4. execute `namespace_ownership.py rollover-plan`,
5. apply/verify the ownership transition.

On the baselined OpenClaw `2026.7.1-2`, the `plugins install --force` operation may replace/remove the previously installed plugin generation while registering the new generation. By the time `rollover-plan` runs, the ownership manifest can still refer to the previously owned installation path even though that path has already disappeared.

The ownership planner then correctly refuses to construct a rollover from an incomplete old owned installation.

### 4. The ownership fail-closed behavior is correct

The failure must not be repaired by weakening ownership checks, accepting a missing old generation, or manufacturing ownership state after the external mutation. A missing manifest-owned root is exactly the kind of ambiguity that the ownership boundary is intended to reject.

### 5. Naively moving `rollover-plan` before `plugins install` is also invalid

The current rollover model is defined around a transition in which the old owned generation and the replacement candidate can both be proven. Before the external install, the replacement candidate is not yet registered in the live OpenClaw inventory; after the external install, the old generation may already have been removed.

Therefore the defect is not simply one misplaced line. The integration requires a transaction contract that safely spans an externally mutating install operation.

## Root cause classification

**Windows plugin-generation ownership rollover transaction contract mismatch with the actual OpenClaw 2026.7.1-2 install-over semantics.**

The current implementation assumes a coexistence window for old and replacement plugin generations that the external `openclaw plugins install --force` operation does not guarantee.

## Required repair direction

The next source repair must preserve the existing fail-closed ownership invariant while explicitly bridging the external mutation boundary. At minimum the repaired contract must support the equivalent of:

1. **Pre-install prepare/proof** — validate and snapshot the currently owned manifest/root/inventory and immutable identity needed to authorize a specific transition.
2. **Single external install mutation** — invoke the exact local `.tgz` package once.
3. **Post-install replacement proof** — validate the newly registered candidate and prove that it is the expected successor to the prepared old state.
4. **Atomic ownership commit** — switch durable ownership only after the post-install proof succeeds.
5. **Failure after mutation remains fail-closed** — do not falsely restore/reassert the old manifest when the external command has already removed that generation.

The exact implementation is a Task 108 TDD concern. This review does not pre-authorize a particular code patch.

## Gate decision

Task 107 is closed as **FAIL, independently accepted as valid evidence**.

The following are prohibited from this review boundary:

- retrying Task 107 with the same candidate or artifact,
- replaying the failed install-over,
- running reset/uninstall/fresh-reinstall/lifecycle/recovery phases from Task 107,
- manually cleaning Task 105/107 live residue,
- weakening ownership validation,
- sending the final Dashboard semantic message.

The next authorized work is a new **source-only TDD repair task** for the rollover transaction contract. A new package-proof candidate must be built and independently reviewed before any new real-Windows lifecycle acceptance task is authorized.

## Review conclusion

**Task 107 review: COMPLETE — ACCEPTED FAIL.**

The executor stopped at the correct safety boundary. The evidence is sufficient to open the next source-repair task without replaying live side effects.
