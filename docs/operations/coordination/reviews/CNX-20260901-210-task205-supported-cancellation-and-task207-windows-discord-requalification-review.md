# Independent Review — CNX-20260901-210 Task-205 Supported Cancellation + Task-207 Windows Discord Requalification

## Verdict

`ACCEPTED PARTIAL — TASK205 CANCELLATION PASS; TASK207 INSTALL-OVER INTERRUPTED/TERMINAL UNPROVEN; READ-ONLY REENTRY ADJUDICATION REQUIRED`

## Accepted Task-205 cleanup evidence

Task 210 correctly revalidated the exact owner-session scope before mutation and found only the historical Task-205 Ticket/recovery pair. It then invoked the product's supported `cancelSessionTickets(...)` surface exactly once with historical run:

`b79dbb65-15eb-4b3e-8ffb-4084125e6cb5`

The returned result identified the expected owner session, advanced generation from `0` to `1`, and cancelled exactly:

`CNXT-f23e2c11-e630-4319-84c2-c57ed7e7edf6`

Fresh read-only post-state proved the historical Ticket and direct-recovery row are `cancelled`, the production-equivalent recovery scheduler selects no row, there is no same-session emittable residue, and SQLite integrity is `ok`.

This portion is accepted as PASS. The old Task-205 delayed-output hazard is closed.

## Task-207 package provenance

Task 210 independently verified the retained Task-207 package proof before install-over:

- source commit `27fe0181b3b65d555a3b0cc8354f6f7945c21c0b`;
- payload-v2 `d0677581d60d3d5535c65e3261dae6f50d7aeb245b8680adac0cace4c040643b`;
- payload files `192`;
- ZIP SHA-256 `0321028fc6214e18dbc965ad79a6d04328a05a84dce6a9efc058fb1122237986`;
- tar.gz SHA-256 `0ab3884621a518b4cfd46949e3c8e3e7f9f52995bee257743960dd7636794dcf`.

No candidate substitution is established.

## Installer evidence classification

The one supported install-over was launched exactly once as standalone PowerShell PID `23248` at `2026-09-01T09:24:39.539Z`.

Retained stdout proves:

1. plugin artifact verification PASS;
2. Ticket DB bootstrap PASS;
3. pre-install native handoff PASS;
4. skill installation reached;
5. CogentNexus validation PASS;
6. `ticket-db-bootstrap` stage complete exit `0`;
7. `plugin-npm-pack` stage complete exit `0`;
8. `plugin-rollover-prepare` stage START at `2026-09-01T09:26:08.1703412Z`;
9. no matching stage COMPLETE is retained.

The outer Hermes terminal observation timed out after roughly 420 seconds from installer start. Wrapper terminal metadata did not contain an end timestamp or exit code. PID `23248` was later absent. Process disappearance alone is not proof of installer success or failure.

The post-state is not converged: controller mode is `passthrough`, startup adapter is not installed/enabled, Gateway remains healthy, and semantic acceptance was not attempted.

Therefore the report's `BLOCKED_INSTALLER_TERMINAL` disposition is accepted.

## Independent timing analysis

The Task-210 observer budget is shorter than already accepted real-Windows installer behavior.

Historical accepted Task 170 recorded `plugin-rollover-prepare` from `22:36:08.768785Z` to `22:43:23.209080Z`, approximately 434.4 seconds, before subsequent stages completed successfully.

Historical Task 189 recorded a successful installer duration of approximately 818.99 seconds and `plugin-rollover-prepare` alone at approximately 430.3 seconds.

Task 210's outer terminal timeout occurred roughly 420 seconds after installer launch, while `plugin-rollover-prepare` did not start until roughly 88.6 seconds after launch. The stage therefore had only about 331 seconds of observation time before the outer terminal timeout — substantially less than the previously accepted ~430–434 second stage duration.

This makes an observation/executor timeout mismatch a strong explanation for the interruption. It is not evidence of a new Task-207 product-source defect.

However, because retained stage output stopped permanently and the runtime remains in rollover `passthrough`, Task 210 cannot be upgraded to success merely from historical timing.

## Existing interrupted-rollover contract

The repository already contains an attested interrupted-rollover re-entry contract. Historical accepted live evidence requires the production classifier itself to prove a coherent re-entry shape using candidate fingerprint and exact OpenClaw plugin inventory. The accepted shape is exemplified by:

- `mode=upgrade`;
- `pendingRollover=false`;
- `pluginAlreadyExact=true`;
- `interruptedRolloverReentry=true`;
- no conflicting legacy/foreign ownership evidence.

No such classifier evidence was captured after Task 210's interruption.

## Required successor

Do **not** blindly replay install-over and do **not** manually edit/move/delete ownership, backup, staging, transaction, plugin, or controller state.

A read-only successor must first:

1. capture current manifest, plugin registration/inventory, live plugin root/fingerprint, install-staging and rollover transaction/backup residue;
2. verify SQLite and runtime state without mutation;
3. use the exact Task-207 candidate ownership tool and exact candidate plugin fingerprint;
4. run production-equivalent attested `classify-install` with exact live plugin inventory;
5. determine whether state is a supported interrupted-rollover re-entry, a still-pending transaction, already-converged-but-unverified state, or unsafe/indeterminate partial state;
6. stop for coordinator review without installer replay, lifecycle enable, Discord Send, or manual normalization.

Only an evidence-backed supported re-entry classification may authorize another installer invocation in a later task.

## One-shot accounting

Task-205 supported cancellation: consumed and PASS; never repeat.

Task-210 install-over attempt: consumed as an interrupted attempt. It is not a completed successful install and must not be blindly replayed. A future invocation requires explicit authorization based on interrupted-rollover re-entry evidence.

Discord Send: `0`; still unconsumed.

## Review disposition

`ACCEPT_PARTIAL__TASK205_CLOSED__TASK207_INTERRUPTED_ROLLOVER_READONLY_ADJUDICATION_REQUIRED`
