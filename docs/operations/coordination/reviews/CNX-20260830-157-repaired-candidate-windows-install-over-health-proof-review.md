# CNX-20260830-157 Review — Repaired-Candidate Windows Install-Over + Live Health Proof

Disposition: **BLOCKED**

Reviewer: ChatGPT

Reviewed branch: `agent/v0.9.3-full-stabilization`

Reviewed Task:

`docs/operations/coordination/tasks/CNX-20260830-157-repaired-candidate-windows-install-over-health-proof.md`

Reviewed report:

`docs/operations/coordination/reports/CNX-20260830-157-repaired-candidate-windows-install-over-health-proof.md`

Report publication commit reviewed:

`d14cf89caf2cb3a5d5da2c40287c9e76b0f76d1e`

## Review conclusion

Task 157 cannot be accepted because the repaired-candidate install-over did not reach a proven completion boundary. The single established installer invocation exceeded the executor's `420s` window, produced no proven installer completion line or exit status, and the subsequent read-only inspection showed that the installed plugin fingerprint remained the pre-existing fingerprint rather than the repaired candidate fingerprint.

This is a **BLOCKED** live checkpoint rather than a proven product/source failure. The durable evidence does not establish which installer subprocess or internal stage consumed the execution window, so this review does not infer a root cause and does not authorize a speculative installer behavior change.

## Evidence accepted

The report provides adequate evidence that the pre-mutation candidate/provenance gate was satisfied:

- fresh remote candidate HEAD: `ee3c6422fe2bab9b52036b5ec67b2e212a3c88fe`;
- accepted production repair `1ec8cfc81b8a21a178200c33816427f9abfd31b9` was an ancestor;
- the reported production/install/runtime diff from repair SHA to candidate HEAD was empty for `plugins scripts skills package.json package-lock.json`;
- candidate package SHA-256 and candidate plugin fingerprint were recorded before mutation;
- candidate validation/package checks passed.

The report also adequately records the live safety result:

- the established install-over workflow entered the native handoff boundary;
- Gateway remained reachable after the handoff;
- post-state was `passthrough`;
- the CNX plugin was disabled rather than falsely reported as the repaired managed payload;
- SQLite integrity remained `ok` and the reported durable counts were unchanged;
- Dashboard semantic Sends performed by Task 157 = `0`;
- no reset, clean uninstall, fresh reinstall, manual semantic/database mutation, Dashboard interaction, or source patch was reported.

## Acceptance criteria review

1. **Install-over result — NOT SATISFIED.** No installer completion boundary or exit status was captured before the executor timeout.
2. **Installed identity — NOT SATISFIED for the repaired candidate.** Post-state fingerprint remained `12c6d1b5b6ffd938353dd60c5d6190c34a609663369f619ff4fc7cbd176119e0`, while the candidate fingerprint was `07ac85dcc4eddca65d2107bac9123bedaf14751bedc66d2e8c5a12d88cf82d96`.
3. **Installed provenance — NOT SATISFIED.** Candidate provenance before mutation was good, but the candidate was not proven installed.
4. **Lifecycle health — PARTIAL ONLY.** Gateway/provider/SQLite remained healthy, but repaired managed/plugin lifecycle health was not established because the system remained in passthrough with the plugin disabled.
5. **Loader health — PARTIAL ONLY.** No inspected CNX loader diagnostic was reported, but the repaired plugin was not proven installed or loaded.
6. **Command health — PARTIAL ONLY.** Read-only post-state checks succeeded, but they do not substitute for repaired-candidate installation and managed-state proof.
7. **No semantic test — SATISFIED.** Dashboard semantic Sends = `0`.
8. **No prohibited mutation — SATISFIED by the durable report.** Reported mutations remained within the established install-over handoff before timeout.

## Log/evidence limitation

The report names the raw installer capture at:

`C:/Users/CDQ-P/AppData/Local/Temp/cnx157-install-over-20260830T0610/install-over.txt`

and names the associated pre/post-state files on the real Windows machine. Those raw local files were not published into the GitHub coordination repository with Task 157. The reviewer therefore had access to the report's durable summary/excerpts and file paths, but **not to the complete raw `install-over.txt` contents**.

Accordingly, this review does not claim that the `420s` delay originated in `npm`, `openclaw plugins install`, package replacement, OpenClaw plugin loading, or any other specific subprocess. Root cause remains unproven.

## Required next action

Do **not** retry the same live install-over blindly and do **not** proceed to Dashboard semantic reacceptance.

The next checkpoint should be repository-side diagnosis of the established Windows install-over path and its existing tests/logging. If current instrumentation cannot durably identify the long-running boundary/subprocess, add the minimum diagnosability needed under TDD while preserving existing rollover/native-handoff safety semantics. If the repository already emits sufficient raw evidence and the deficiency was only evidence retention, fix the evidence-capture contract rather than product behavior.

A later, separate live Windows retry must preserve raw installer/subprocess evidence durably enough for review and must remain fenced from Dashboard semantic Send until repaired-candidate installation and health are accepted.

## Phase gate

Task 157: **BLOCKED**.

Phase P remains pending/not accepted.

No Dashboard semantic Send is authorized by this review.
