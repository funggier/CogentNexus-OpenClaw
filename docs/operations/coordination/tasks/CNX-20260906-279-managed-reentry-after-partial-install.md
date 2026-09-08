# CNX-20260906-279 — Managed Re-entry After Partial Install

## Status

`READY_FOR_HERMES`

Parent: `CNX-20260906-278`
Executor: `Hermes`
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

Task278's one-shot installer authority is consumed and must not be replayed as Task278.

ChatGPT review:

`docs/operations/coordination/reviews/CNX-20260906-278-chatgpt-partial-install-review.md`

Verdict:

`ACCEPT_EXACT_PAYLOAD_INSTALLED__MANAGED_ACTIVATION_INCOMPLETE__FRESH_ENABLE_AUTHORITY_REQUIRED`

Human authorization:

`docs/operations/coordination/reviews/CNX-20260906-279-human-recovery-and-final-release-authorization.md`

## Preferred recovery path

Hermes must use root-cause-first / smallest-supported-action ordering.

Immediately before mutation, prove read-only:

1. installed plugin fingerprint still exactly equals the accepted candidate;
2. ownership verification passes against the installed canonical plugin/skill/launcher;
3. plugin is still disabled and controller remains PASSTHROUGH;
4. Gateway and Ollama are reachable;
5. SQLite integrity is `ok`;
6. protected old Ticket `CNXT-dc11c9a0-8a89-4df5-9c48-345260725be4` is untouched;
7. Task272 sacrificial lineage remains untouched/non-clean and is not selected for mutation.

If these predicates establish that canonical MANAGED re-entry is valid, invoke exactly once:

```text
C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd enable
```

Allow only lifecycle effects owned by that supported command. Capture trustworthy terminal evidence. Do not blindly retry `enable`.

## Supported reinstall fallback authority

The human explicitly authorized reinstall if necessary.

A supported reinstall/install-over of the same exact accepted candidate is authorized only if evidence proves one of these conditions:

- the preconditions show that `enable` alone is not a valid/sufficient supported recovery from the Task278 partial state; or
- the single supported `enable` attempt fails and post-failure readback proves a coherent state for supported reinstall.

If fallback is necessary:

- perform at most one supported reinstall/install-over;
- bind it to exact candidate `36cd4c800ded28bdb7165fcad6e0bfb48b4e933b`;
- use the repository-supported installer path only;
- allow installer-owned lifecycle transitions only;
- capture terminal evidence with a runner boundary long enough for the known Windows install duration;
- do not combine this with uninstall/reset, broad cleanup, manual plugin repair, manual SQLite mutation, or ad-hoc process kills.

Reinstall is a fallback, not the default.

## Post-action proof

After whichever supported recovery path succeeds, verify read-only:

- exact candidate fingerprint unchanged/matched;
- plugin `enabled=true` and `status=loaded` at the canonical root;
- Host controller mode `managed`;
- Gateway reachable/healthy;
- Ollama reachable/ready with configured model;
- CogentNexus supervisor present/enabled/healthy as expected by MANAGED mode;
- SQLite integrity `ok`;
- protected old Ticket unchanged;
- Task272 sacrificial lineage not disposed/replayed/redelivered/Deleted/reset;
- no semantic send occurred.

Publish PASS/FAIL/BLOCKED and stop for ChatGPT review.

## Not authorized in Task279

- Discord/Dashboard semantic sends;
- OpenClaw session Delete/reset;
- Ticket cancellation/disposition/replay/redelivery;
- manual SQLite mutation;
- clean uninstall/reset;
- broad cleanup or manual plugin mutation;
- ad-hoc process kills;
- release/tag/default-branch promotion during Task279;
- force push/history rewrite.

Task272's earlier Delete/test-message authority remains parked and separate and must not be consumed during Task279.

## Conditional final release direction

The human has explicitly directed that after all stabilization/final-acceptance gates are independently accepted, release is the final closing action and no additional yes/no release confirmation is required. The release must be a later bounded task after final acceptance; Task279 itself does not perform it.
