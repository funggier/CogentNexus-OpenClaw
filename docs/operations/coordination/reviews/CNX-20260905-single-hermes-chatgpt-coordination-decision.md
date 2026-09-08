# CNX-20260905 — Human Coordination Decision: Single Hermes + ChatGPT

**Decision:** `ADOPT_SINGLE_HERMES_EXECUTOR__CHATGPT_ROUTINE_REVIEW`

**Repository:** `funggier/CogentNexus-OpenClaw`
**Branch:** `agent/v0.9.3-full-stabilization`
**Authority:** Human operator, expressed directly to ChatGPT on 2026-09-05 ICT

## Decision

The human operator determined that the latest Musethree workload is likely beyond what that bot can reliably handle and requested a return to the earlier operating style: one Hermes executor working together with ChatGPT.

Prospective coordination model:

```text
Hermes executes assigned task
  -> self-rechecks deterministic CI/external waits
  -> publishes report
  -> WAITING_FOR_CHATGPT_REVIEW
ChatGPT independently reviews
  -> accept + open bounded successor for Hermes
  -> or open rework for Hermes
  -> or surface missing human authority
```

Luna/Musethree alternation is discontinued for new work. Historical reports and reviews remain valid evidence and retain their original actor names.

## Scope

This is a coordination-policy change only. It does not itself authorize any new installer, Gateway, DB/recovery, OpenClaw session deletion/reset, Discord/Dashboard semantic send, release/tag/default-branch promotion, or other live/destructive side effect.

## Task263 transition

Task263 source repair report already exists and remains valid historical Luna execution evidence. Under the new policy it no longer waits for Musethree. It transitions to ChatGPT independent review.

Candidate remains:

`4a5907af212c0b8c6f913036c6853523d7bab872`

Report:

`docs/operations/coordination/reports/CNX-20260905-263-discord-manual-session-delete-recreation-source-repair.md`

The existing Task263 hard fences remain unchanged until ChatGPT review publishes a new bounded successor/decision.
