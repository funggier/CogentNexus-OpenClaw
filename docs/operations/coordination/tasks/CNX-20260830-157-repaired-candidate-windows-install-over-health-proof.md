# CNX-20260830-157 — Repaired-Candidate Windows Install-Over + Live Health Proof

Status: `READY_FOR_HERMES`
Execution mode: `LIVE_WINDOWS_REPAIRED_CANDIDATE_INSTALL_OVER_HEALTH_PROOF`
Current authorization: `CNX-20260830-157_REPAIRED_CANDIDATE_WINDOWS_INSTALL_OVER_HEALTH_PROOF`
Task ID: `CNX-20260830-157`
Updated: 2026-08-30 ICT
Owner / coordinator / reviewer: ChatGPT
Executor: Hermes on the operator's real Windows/OpenClaw environment

## Purpose

Install the already-repaired CogentNexus-OpenClaw candidate over the existing live Windows installation, then collect enough provenance, lifecycle, loader, and health evidence to establish that the repaired candidate is actually installed and running cleanly before any Dashboard semantic delivery reacceptance is attempted.

This is a narrow live-environment proof task. It does **not** authorize new product/runtime repair work and it does **not** authorize a Dashboard semantic Send.

## Authorization lineage

The production repair accepted for this live checkpoint is rooted at exact production repair commit:

`1ec8cfc81b8a21a178200c33816427f9abfd31b9`

Task-155 durable report:

`docs/operations/coordination/reports/CNX-20260830-155-dashboard-public-hook-duplicate-durable-authority-rework.md`

Task-155 review disposition is `ACCEPT`, recorded on branch `agent/v0.9.3-full-stabilization` by commit:

`d4a4d6b0b14d18eee47d608edd66917eb27b9a68`

Later coordination/documentation-only commits may be present on the branch. They do not authorize a different production payload. The installed candidate must be demonstrably derived from the accepted repaired production state and must contain no unreviewed production/source change beyond the accepted repair lineage.

## Objective

Hermes must, using the repository-established packaging/install process:

1. capture the live pre-state before mutation;
2. identify/build/select the repaired candidate with exact provenance;
3. perform an **install-over** of that candidate on the existing Windows installation;
4. perform only the lifecycle actions necessary for that install-over and subsequent health proof;
5. verify the installed plugin/runtime identity and provenance;
6. verify that the relevant CogentNexus/OpenClaw components load and remain healthy;
7. capture sufficient command/output/log evidence for ChatGPT to review the live checkpoint independently of Hermes' conclusion;
8. publish the required Task-157 report and stop.

## Required pre-state evidence

Before install-over, record at minimum what is available from the established tooling for:

- current date/time and Windows/PowerShell context;
- repository branch and exact source/candidate identity used for the operation;
- currently installed CogentNexus-OpenClaw package/plugin identity and provenance;
- OpenClaw/gateway/controller/plugin lifecycle state relevant to installation;
- relevant health/status output;
- any established install metadata or package proof that will allow before/after comparison.

Do not manufacture missing evidence. If an established command is unavailable or fails, preserve the exact failure and continue only if the task can still be evaluated safely.

## Candidate/provenance gate

Before mutating the live installation, prove which artifact is going to be installed.

The proof must establish that:

- production repair `1ec8cfc81b8a21a178200c33816427f9abfd31b9` is included;
- no later unreviewed production/source modification is silently introduced;
- package/archive/plugin identity is attributable to the authorized branch/candidate by the repository's existing provenance mechanism;
- the artifact is the one actually passed to the install-over path.

If candidate provenance cannot be established, **STOP as BLOCKED before install-over** and publish the report with the exact blocker.

## Authorized live actions

Only the following live actions are authorized:

- read-only status, provenance, version, package, health, and log inspection;
- creation/use of the candidate package/artifact through the existing repository packaging workflow;
- install-over of the repaired candidate using the established install-over workflow;
- stop/start/restart or equivalent lifecycle actions only where the established install-over workflow requires them or where they are necessary to prove post-install health;
- read-only post-install validation and log collection;
- writing/pushing the Task-157 evidence report to the coordination repository.

Use the smallest live mutation surface required to complete the install-over proof.

## Hard fence

Task 157 does **not** authorize any of the following:

- Dashboard semantic Send;
- Dashboard click/focus/type/paste for semantic delivery testing;
- sending a new semantic user message through OpenClaw/CogentNexus to test delivery;
- manual Ticket, workflow, outbox, delivery, database, or semantic-state mutation;
- reset;
- clean uninstall;
- fresh reinstall after uninstall;
- arbitrary deletion of live state;
- manual production/source patching on the Windows machine;
- dependency upgrades;
- OpenClaw source patching;
- a new CogentNexus runtime/product behavior change;
- merge to the release/default branch;
- tag, GitHub Release, package publication, or promotion;
- force push.

If the install-over or health proof exposes a new product/source defect, capture evidence and stop `BLOCKED`/`FAIL`; do not repair it inside this live Task unless a new durable coordination Task explicitly authorizes that repair.

## Post-install acceptance evidence

The Task-157 report must contain enough raw evidence to evaluate each item below:

1. **Install-over result** — the established install-over command/process completed with its exact outcome and exit status where available.
2. **Installed identity** — the installed CogentNexus-OpenClaw/plugin/package identity is visible after installation.
3. **Provenance** — the installed payload is demonstrably tied to the authorized repaired candidate lineage.
4. **Lifecycle health** — required OpenClaw/gateway/controller/plugin components start or remain running as expected after install-over.
5. **Loader health** — no relevant package/schema/plugin-loader failure is present in the inspected post-install output/log window.
6. **Command health** — established non-semantic status/health commands relevant to the installed candidate succeed or their exact failure is preserved.
7. **No semantic test** — Dashboard semantic Sends performed by this task = `0`.
8. **No prohibited mutation** — explicitly enumerate any live mutations performed and confirm whether they stayed inside the authorized list.

Do not infer PASS from process exit alone. Reconcile installation, provenance, lifecycle, and inspected logs together.

## Required report

Hermes must publish exactly:

`docs/operations/coordination/reports/CNX-20260830-157-repaired-candidate-windows-install-over-health-proof.md`

The report must include:

- `PASS`, `FAIL`, or `BLOCKED` disposition;
- exact source/candidate/artifact identity;
- exact installed identity/provenance evidence;
- commands/actions performed in execution order;
- relevant command output, exit status, timestamps, and log excerpts/paths;
- before/after lifecycle and health state;
- every live mutation performed;
- explicit count of Dashboard semantic Sends (`0` required);
- exact report commit SHA after push;
- any remaining uncertainty or next required action.

## Stop condition

After publishing/pushing the Task-157 report, **STOP**.

Do not proceed to Dashboard reacceptance, Phase-Q work, release work, or another live mutation. ChatGPT will fresh-read the durable GitHub state and perform the next review/coordination checkpoint. A separate explicit Task is required before any Dashboard semantic Send.

## Expected successor on PASS

A Task-157 `PASS` does not by itself make Phase P pass. It only establishes the repaired candidate on the real Windows environment.

After ChatGPT reviews and accepts the Task-157 evidence, the next expected live checkpoint is a separate, tightly scoped Dashboard durable-delivery reacceptance Task with its own explicit semantic-Send authorization.
