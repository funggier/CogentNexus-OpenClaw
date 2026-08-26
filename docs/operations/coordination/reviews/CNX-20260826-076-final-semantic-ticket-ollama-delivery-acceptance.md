# Review — CNX-20260826-076 Final Semantic Ticket → Ollama → Delivery Acceptance

Decision: `ACCEPT`

Disposition: `ACCEPT_BLOCKER_SEMANTIC_ENTRY_PATH_OWNER_SIGNAL_COVERAGE`

Reviewed report result: `BLOCKED_SEMANTIC_ENTRY_PATH`

Report HEAD: `4dc5dbba9b5933f6f2ca274cbea0c1eee0fe446d`

Execution starting HEAD: `d9ac3ed08562cebcd2af69f19d110bf89cd41ab9`

Accepted live source remains: `79b51ed06363f6e8862c491ee0a313ddb412c806`

## Independent findings

1. The executor used exactly one real Gateway-backed OpenClaw agent/session CLI message and did not resend it after timeout.
2. The correlated OpenClaw run reached provider `ollama`, model `qwen3.5:9b`, and then terminated with a provider-stage idle timeout.
3. The authoritative Ticket database remained empty before and after the run: zero Tickets, zero Ticket events and zero Ticket outbox rows. Therefore the required Ticket-first semantic admission did not occur before provider execution.
4. Because Ticket admission must precede inference, the provider timeout cannot explain the absence of the Ticket. The semantic-entry failure exists independently of the later Ollama timeout.
5. The accepted production source gates admission through `durableAdmissionEligible({sessionKey,senderIsOwner})`. It accepts ordinary non-subagent sessions when `senderIsOwner !== false`, and when `senderIsOwner === false` it permits only the canonical dashboard namespace `agent:<agent>:dashboard:<id>`.
6. The production unit tests explicitly prove that a dashboard session with `senderIsOwner=false` is eligible while an arbitrary CLI session with `senderIsOwner=false` is rejected. The Task-076 selected session `agent:main:main` therefore cannot be assumed to be an eligible owner-entry merely because the CLI targets a real session key.
7. The current evidence does not yet distinguish whether the failed run is:
   - a surface-selection mismatch, where `openclaw agent` is intentionally not an owner-trusted semantic input under OpenClaw 2026.7.1-2; or
   - a product admission-coverage gap, where a legitimate normal owner surface reaches `before_agent_run` with metadata that current CogentNexus policy rejects.
8. No source or live repair should be made until that OpenClaw owner-signal contract is traced from exact 2026.7.1-2 runtime/source behavior.

## Publication fence

`d9ac3ed08562cebcd2af69f19d110bf89cd41ab9 -> 4dc5dbba9b5933f6f2ca274cbea0c1eee0fe446d` is exactly one commit and changes only:

`docs/operations/coordination/reports/CNX-20260826-076-final-semantic-ticket-ollama-delivery-acceptance.md`

Publication fence: `PASS_REPORT_ONLY`

## Review conclusion

Task 076 correctly reported a blocker and preserved the one-message safety fence. Do not resend the Task-076 nonce and do not manually create or repair Ticket state.

The next task must diagnose the exact OpenClaw owner-entry metadata/surface contract without another live semantic message. If a product gap is proven, repair it by TDD with the narrowest trusted-owner rule. If the existing policy is correct, prove the exact supported owner surface that must be used by the next live semantic acceptance.
