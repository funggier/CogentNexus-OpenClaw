# CNX-20260906-268 — ChatGPT Causal Root Review

## Verdict

`ACCEPT_CAUSAL_PROOF__SOURCE_ACTIONABILITY_REPAIR_REQUIRED`

Task268 is accepted as sufficient proof that the user's recurring Windows APPSTARTING/busy cursor is caused by the natural `CogentNexus-OpenClaw-Supervisor` process wave.

Accepted evidence:

- 6/6 natural `PT1M` supervisor ticks aligned with APPSTARTING transitions;
- each APPSTARTING run began within roughly 0.5 s of the minute boundary and lasted roughly 8.0–8.3 s;
- no APPSTARTING state occurred off-cycle;
- foreground application identity remained substantially unchanged;
- Gateway and Ollama PIDs remained stable, excluding service restart as the trigger;
- hard fences were respected.

## Narrowed root cause

The Scheduled Task cadence itself is not the semantic defect. The current Host already has a quiescent fast path in `host_v091.py::supervisor_tick()` that returns without launching the heavy reconciliation path when Gateway/provider are healthy and `durable_work_hint(root)` is false.

The defect is that `durable_work_hint()` treats overly broad durable state as immediately actionable. In particular it returns true for any nonterminal Ticket and for broad direct-recovery states without applying the same owner/session-generation/liveness/due fences used by the plugin's event-driven Direct recovery worker.

This conflicts with the accepted Direct-recovery contract in `plugins/cogentnexus-openclaw/src/v091-direct-recovery.ts`:

- `DIRECT_RECOVERY_SESSION_LIVENESS_MS = 15 * 60_000`;
- `dueDirectRecovery()` requires pending recovery, accepted Direct lane, active owner session, exact owner generation, owner session freshness inside that window, due `next_attempt_at`, and the model-call recovery fence.

The live stale Ticket/recovery therefore is intentionally not due for Direct recovery, but Host `durable_work_hint()` still forces the heavy path every minute. That path creates short-lived OpenClaw/Node status-command process waves and is now proven to align with the APPSTARTING cursor symptom.

## Safety conclusion

Do not disable or lengthen the supervisor interval as the primary repair. That would weaken recovery responsiveness while leaving the semantic mismatch intact.

Do not cancel/redeliver/dispose/replay the old Ticket to make the cursor disappear. Owner intent remains unproven and the stale Ticket is evidence of the defect, not authority to mutate it.

The correct next step is a source/test/CI repair so Host wake hints mean *actionable work*, not merely *stored nonterminal state*.

Installed-vs-candidate mismatch, open `ollama:1` recovery incident, exact-candidate deployment, old Ticket handling, live Delete/recreate acceptance, and semantic message sends remain separately gated.
