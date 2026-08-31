# CNX-20260829-139 — Repaired Candidate Install-Over and Health Proof Review

- **Task:** `CNX-20260829-139`
- **Report:** `docs/operations/coordination/reports/CNX-20260829-139-repaired-candidate-install-over-and-health-proof.md`
- **Reviewed report commit:** `0141ed927d76c43f055abe48b8533551e5217c54`
- **Disposition:** **ACCEPT**
- **Accepted execution verdict:** `FAIL_INSTALL_OVER`
- **Review date:** 2026-08-29 ICT

## Review verdict

**ACCEPT the Task-139 execution evidence and its controlled `FAIL_INSTALL_OVER` classification.**

This review does **not** accept the installation as successful. The exact repaired Dashboard source candidate `16f5c396e9be0af8d1bd34824fe2993613501a6f` remains **not deployed** to the effective installed runtime.

Task 139 performed the one authorized supported install-over attempt and stopped at the first fail-closed installer boundary. The report proves that the candidate was built and packaged from the exact accepted repair commit, the pre-install baseline was safe, and the install procedure was invoked exactly once. The installer entered its native handoff, then ownership-safe generation rollover preparation rejected the effective installed plugin path before replacement with:

```text
RuntimeError: plugin is not inside the managed npm projects boundary:
C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw
ownership-safe plugin generation rollover pre-install proof failed
```

The installer exited `1`; the effective installed plugin fingerprint remained the old pre-repair value:

```text
3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4
```

The resulting controller mode is `passthrough` and the existing plugin identity is disabled, but Gateway/Ollama and read-only system/recovery/delivery checks remained healthy/READY. SQLite integrity remained `ok` and the historical Task-136/137 evidence was preserved.

## Evidence accepted

The report adequately proves all of the following:

1. the exact repaired candidate source was `16f5c396e9be0af8d1bd34824fe2993613501a6f`;
2. candidate build, plugin validation, packaging, and package provenance succeeded before the live attempt;
3. pre-install runtime state was safe enough for the single authorized install-over;
4. the supported `scripts/install.ps1` path was executed exactly once;
5. failure occurred before `openclaw plugins install` replaced the existing package;
6. the old installed fingerprint remained unchanged after failure;
7. no clean uninstall, reset, normalization, manual cleanup, or retry occurred;
8. no Dashboard semantic Send/resend, alternate semantic injection, or Task-136/137 semantic reuse occurred;
9. no new Ticket, outbox, assistant-delivery, or direct-recovery row was created;
10. Task-136/137 durable evidence and SQLite integrity were preserved.

## Root-cause boundary

The Task-139 report proves the **failure boundary**, but it does not yet prove the exact source-level root cause of the ownership mismatch.

The observed rejection is associated with the installer ownership/generation-rollover path involving `scripts/install.ps1` and `skills/cogentnexus-openclaw/scripts/namespace_ownership.py`. However, this review deliberately does not infer whether the defect is caused by caller-supplied path semantics, the expected managed npm projects root, path normalization/resolution, package-manager layout, junction/symlink handling, generation metadata, or another ownership-contract mismatch.

A production edit is therefore not authorized from the runtime symptom alone. The exact Task-139 topology and caller contract must first be represented by a deterministic offline RED test through the narrowest trustworthy ownership-rollover boundary.

## Safety disposition

The fail-closed behavior itself was correct for the unproven ownership condition. It prevented replacement when ownership could not be established. Any repair must preserve that safety property and must continue rejecting genuinely unmanaged paths and boundary escapes.

Because the failed live attempt left the controller in `passthrough` with the plugin disabled, the runtime must not be silently normalized or repaired outside a later explicitly authorized deployment task. Task 140 is offline-only and must not mutate this state.

## Next action

Open the narrowest successor:

`CNX-20260829-140 — Installer ownership-boundary rollover diagnosis and repair`

Task 140 is an **offline RED-first TDD task only**. It must prove the exact source root cause, implement the smallest repair consistent with ownership safety, validate it offline/CI, publish its report, and stop for independent review.

There is **no authorization** yet for another install-over attempt or for final Dashboard semantic re-acceptance.
