# Hermes Executor / ChatGPT Review Model

Updated: 2026-09-05 ICT

## Purpose

Use one Hermes executor for routine technical work and ChatGPT as the independent reviewer/coordinator so work quality does not depend on a second Hermes peer being available or capable.

The authoritative transition rules are in `HERMES_CHATGPT_SINGLE_AGENT_PROTOCOL.md`.

## Core model

```text
Human / ChatGPT establishes goal or resolves authority
    -> Hermes investigates + implements + validates + reports
    -> ChatGPT independently reviews Hermes report
    -> if accepted and continuation is bounded/authorized:
         ChatGPT opens next task for Hermes
    -> if rework needed:
         ChatGPT opens rework for Hermes
    -> if fresh human authority needed:
         wait for human decision
    -> repeat
```

## Reviewer depth

ChatGPT reviews using progressive depth:

1. contract/lineage check;
2. targeted verification of critical claims;
3. focused technical expansion for weak/high-risk evidence;
4. full reconstruction only if required for a safe disposition.

PASS is never accepted solely because Hermes says PASS.

## Evidence-rich reporting

Hermes reports facts, evidence references, causal conclusions, material alternatives, uncertainty, risk, tests, hashes/runs, hard-fence compliance, and a compact verification packet. Do not publish private chain-of-thought.

## Successor decision

ChatGPT may continue the approved project by opening a bounded successor for Hermes when one continuation is clearly supported by evidence and existing authority.

ChatGPT must not infer missing human semantic intent or silently widen live/destructive authority. When fresh consent is required, surface the exact missing authority to the human operator.

## Asynchronous waits

Hermes retains ownership during queued/in-progress deterministic CI/external waits and follows `DELAYED_RECHECK_QUEUE.md`. Waiting does not create a ChatGPT review handoff until the required gate is terminal or a real decision boundary is reached.

## Historical compatibility

Historical tasks/reviews produced by Luna/Musethree remain valid. For future work, the single Hermes + ChatGPT review model supersedes the dual-agent peer-review model.
