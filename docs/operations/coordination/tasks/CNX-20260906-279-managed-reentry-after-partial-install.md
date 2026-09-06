# CNX-20260906-279 — Managed Re-entry After Partial Install

## Status

`WAITING_FOR_HUMAN_AUTHORIZATION`

Parent: `CNX-20260906-278`
Executor after authorization: `Hermes`
Reviewer: `ChatGPT`

## Accepted candidate

`36cd4c800ded28bdb7165fcad6e0bfb48b4e933b`

## Starting state

Task278 consumed exactly one authorized install-over. Terminal completion was not proven because the external runner timed out, but readback proved:

- installed plugin fingerprint exactly matches the accepted candidate;
- plugin is present but disabled;
- Host controller is PASSTHROUGH;
- Gateway and Ollama are reachable;
- protected durable state remained intact.

Task278 must not be retried.

ChatGPT review:

`docs/operations/coordination/reviews/CNX-20260906-278-chatgpt-partial-install-review.md`

Verdict:

`ACCEPT_EXACT_PAYLOAD_INSTALLED__MANAGED_ACTIVATION_INCOMPLETE__FRESH_ENABLE_AUTHORITY_REQUIRED`

## Requested live authority

After fresh explicit human approval, Hermes may perform exactly one supported MANAGED re-entry through the installed canonical launcher:

```text
C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd enable
```

No installer invocation is authorized.

## Mandatory read-only preconditions

Immediately before enable, prove all of the following:

1. installed plugin fingerprint still exactly equals the accepted candidate;
2. ownership verification passes against the installed canonical plugin/skill/launcher;
3. plugin is still disabled and controller remains PASSTHROUGH;
4. Gateway and Ollama are reachable;
5. SQLite integrity is `ok`;
6. protected old Ticket `CNXT-dc11c9a0-8a89-4df5-9c48-345260725be4` is untouched;
7. Task272 sacrificial lineage remains untouched/non-clean and is not selected for any mutation.

If any precondition fails or is ambiguous, do not invoke enable; publish BLOCKED evidence and stop.

## Authorized action if approved

- invoke `cnxclaw.cmd enable` exactly once;
- allow only lifecycle effects owned by that supported enable command;
- if enable returns nonzero or fails to produce trustworthy terminal evidence, do not retry and do not repair manually.

## Post-action proof

Read-only verify:

- exact candidate fingerprint unchanged;
- plugin `enabled=true` and `status=loaded` at the canonical root;
- Host controller mode `managed`;
- Gateway reachable/healthy;
- Ollama reachable/ready with configured model;
- CogentNexus supervisor present/enabled/healthy as expected by MANAGED mode;
- SQLite integrity `ok`;
- protected old Ticket unchanged;
- Task272 sacrificial lineage unchanged except for installer/enable-owned non-semantic runtime bookkeeping, with no Ticket disposition/replay/redelivery/Delete/reset;
- no semantic send occurred.

Publish PASS/FAIL/BLOCKED and stop for ChatGPT review.

## Not authorized

- rerun `install.ps1` or any installer;
- Discord/Dashboard semantic sends;
- OpenClaw session Delete/reset;
- Ticket cancellation/disposition/replay/redelivery;
- manual SQLite mutation;
- uninstall/reset;
- ad-hoc process kills;
- Scheduled Task mutation outside the supported `enable` lifecycle;
- release/tag/default-branch promotion;
- force push/history rewrite.

Task272's earlier Delete/test-message authority remains parked and separate and must not be consumed during Task279.
