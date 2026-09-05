# Dual-Agent Executor / Peer-Review Model

Updated: 2026-09-05 ICT

## Purpose

Use Luna and Musethree as an alternating executor/reviewer pair so routine technical work can continue without routing every completed task through ChatGPT, while preserving independent evidence review and hard safety boundaries.

The authoritative detailed transition rules are in `HERMES_DUAL_AGENT_BATON_PROTOCOL.md`.

## Core model

```text
Human / ChatGPT establishes goal or resolves escalation
    -> Luna normally receives the first baton
    -> assigned actor investigates + implements + validates + reports
    -> peer actor independently reviews predecessor report
    -> if clear/authorized: peer opens and executes next bounded task
    -> peer reports and hands back
    -> repeat
    -> ambiguity/new authority/final completion -> ChatGPT
```

## Reviewer depth

The receiving peer reviews using progressive depth:

1. contract/lineage check;
2. targeted verification of critical claims;
3. focused technical expansion for weak/high-risk evidence;
4. full reconstruction only if required for a safe disposition.

PASS is never accepted solely because the predecessor says PASS.

## Evidence-rich reporting

Reports state facts, evidence references, causal conclusions, material alternatives, uncertainty, risk, tests, hashes/runs, hard-fence compliance, and a small verification packet. Do not publish private chain-of-thought.

## Peer successor decision

After review, the receiving peer may continue automatically when a single bounded successor is clearly supported by evidence and existing authority. It may also open bounded rework or diagnostics.

It must not autonomously choose among materially different architecture/semantic directions, infer missing user intent, or widen live/destructive authority.

## Escalation

When no safe uniquely authorized continuation exists, publish the review/decision packet and set `WAITING_FOR_CHATGPT`. At terminal project completion set `GOAL_COMPLETE_PENDING_CHATGPT_FINAL`. In either case tell the human operator to notify ChatGPT.

## Historical compatibility

Historical tasks and reviews remain governed by the policy under which they were produced. For future work, any older statement that ChatGPT is required to review every task or create every successor is superseded by the dual-agent baton protocol.
