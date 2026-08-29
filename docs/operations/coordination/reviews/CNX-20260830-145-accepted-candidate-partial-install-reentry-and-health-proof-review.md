# CNX-20260830-145 — Independent Review

Disposition: **ACCEPT**

Reviewed: 2026-08-30 ICT
Reviewer: ChatGPT

## Scope

Independent review of:

- Task: `docs/operations/coordination/tasks/CNX-20260830-145-accepted-candidate-partial-install-reentry-and-health-proof.md`
- Report: `docs/operations/coordination/reports/CNX-20260830-145-accepted-candidate-partial-install-reentry-and-health-proof.md`
- Accepted implementation/deployment SHA: `fb5781c1abd68280760bd5b3b4a65fabd8a60e58`
- Report publication commit: `2f72544e277c8e828f438513728c63a20d2a1db6`

The publication commit changes only the matching Task-145 report. No product source, installer, configuration, or coordination authority was modified by the executor while publishing the result.

## Findings

Task 145 satisfies the authorized live re-entry contract.

1. **Fresh authority and exact candidate provenance**
   - Execution began from the Task-145 coordination HEAD `729b1d6478cda8736eda44cab670e195f03a990d` and rechecked it before publication.
   - Deployment used a fresh detached checkout of exact accepted implementation SHA `fb5781c1...`.
   - Candidate package, plugin fingerprint, `namespace_ownership.py` hash, and `install.ps1` hash were recomputed rather than inherited from Task 142.

2. **Read-only drift/classification gate was coherent**
   - Exactly one plugin identity existed at the canonical direct root.
   - The direct root was a normal non-reparse directory.
   - Controller was `passthrough`; Gateway/Ollama/recovery/delivery/SQLite were healthy; pending delivery count was `0`.
   - Installed plugin fingerprint already equaled the accepted candidate plugin fingerprint.
   - Candidate-aware production classification returned `mode=upgrade`, `pluginAlreadyExact=true`, `pendingRollover=false`.
   - Lifecycle resolution correctly returned `installPlugin=false`, `rolloverPlugin=false`; no redundant plugin replay was authorized.

3. **Exactly one supported installer invocation**
   - One normal `scripts/install.ps1` invocation was executed from the detached accepted source.
   - Exit code was `0`.
   - No retry, alternate installer, manual plugin operation, reset, uninstall, cleanup, or state normalization occurred.

4. **Post-success provenance and health**
   - Plugin remained singular and canonical, became `enabled=true`, `status=loaded`, version `0.9.3`.
   - Installed plugin fingerprint exactly matched the candidate.
   - Installed `namespace_ownership.py` hash exactly matched the accepted candidate source, proving the newer Task-143/144 ownership logic was installed even though the plugin payload itself was already exact.
   - Ownership verification passed and `installedAt` refreshed.
   - Controller returned to `managed`; desired Gateway/provider are running.
   - Gateway, Ollama, recovery, delivery, scheduled tasks, and SQLite were healthy; pending terminal deliveries remained `0`.
   - Durable history counts remained unchanged from the Task-142 boundary.
   - No stale rollover transaction remained.
   - Dashboard semantic Send count remained `0`.

## Harness corrections

The report records three harness mistakes: a wrong repository-root package path, a BOM-producing read-only inventory write, and a PowerShell variable-name collision in a post-read probe. They are accepted as executor-harness corrections because they did not mutate product state, did not create an additional installer invocation, and the affected read-only probes were rerun successfully before the PASS claim.

## Accepted conclusion

The previously preserved Task-142 partial installation can be safely re-entered by the supported installer after the accepted Task-143/144 repairs. The installer reaches coherent normal MANAGED operation without manual normalization or duplicate plugin lifecycle work.

Task 145 therefore closes the partial-install re-entry failure chain.

## Still unproven

Task 145 does **not** prove:

- operator-facing `cnxclaw.cmd uninstall` on the accepted installed candidate;
- a truly clean fresh install after that uninstall;
- `cnxclaw.cmd reset` acceptance;
- final start/stop/restart/disable/enable runtime lifecycle acceptance;
- final real Dashboard durable-delivery acceptance;
- public GitHub Release download/install distribution smoke.

## Next task

Open the narrowest destructive successor: one real operator-facing uninstall with explicit `y`, prove clean native OpenClaw state, then one fresh install of the exact accepted candidate and prove fresh MANAGED health. No reset and no Dashboard semantic Send in that task.
