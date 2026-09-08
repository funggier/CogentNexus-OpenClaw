# CNX-20260907-302 — Live Quiescence and Enable Requalification

## Status

`READY_FOR_HERMES`

Parent: `CNX-20260907-301`  
Executor: `Hermes`  
Reviewer: `ChatGPT`

## Authority

ChatGPT authorizes one bounded live requalification of the accepted installed candidate, using the Task301 repair only if its exact wiring is proven present in the live installation. Hermes may decide technical verification details within this task.

This task authorizes exactly one canonical `cnxclaw enable` invocation after all preflight gates pass. It does not authorize semantic sends, Ticket/session mutation, replay/redelivery, manual state edits, installer/uninstall/reset, release promotion, force push, or changes to the protected state.

## Preconditions

- Fresh-fetch and bind all evidence to the exact current branch candidate and installed repair fingerprint.
- Prove `supervisor_quiescence.py` and Host/Supervisor wiring are present in the installed runtime.
- Prove target/protected Ticket and session state, health, and no competing writer.
- Confirm the supported lease boundary is observable and restore/readback checks are available.

## Procedure

1. Run read-only preflight and stop on any mismatch or ambiguity.
2. Invoke the existing canonical command exactly once:
   `C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd enable`
3. Verify lease restoration/absence, managed Host state, plugin/live worker identity, and Gateway/Ollama health.
4. Observe the exact pending Ticket and delivery state without retry, replay, redelivery, disposition, or manual settlement.
5. Publish evidence-rich report with exact command count, timestamps, fingerprints, state transitions, and PASS/FAIL/BLOCKED.

## Stop conditions

Stop before or during the procedure on missing wiring, lease conflict, restoration failure, config race, worker mismatch, health failure, ambiguous delivery, protected-state drift, or any request for an action outside this task.

## Hard fences

Do not touch protected Ticket `CNXT-dc11c9a0-8a89-4df5-9c48-345260725be4` or owner session `agent:main:discord:channel:1531199905673252946`. No semantic send, replay/redelivery/disposition, manual SQLite/Ticket/session/transcript/config mutation, installer/install-over/uninstall/reset, unrelated service/Scheduled Task mutation, credential action, release/tag/default-branch promotion, or force push.
