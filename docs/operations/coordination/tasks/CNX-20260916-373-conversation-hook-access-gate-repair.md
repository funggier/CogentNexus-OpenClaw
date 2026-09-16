# CNX-20260916-373 — Conversation Hook Access Gate Verification and Minimal Repair

## Task identity

- **Task ID:** CNX-20260916-373
- **Parent:** CNX-20260916-372
- **State:** `CNX373_CONVERSATION_HOOK_ACCESS_GATE_REPAIR`
- **Executor:** Hermes
- **Reviewer:** ChatGPT
- **Human final authority:** Operator
- **Branch:** `cnx-357-openai-dashboard-ticket-first-requalification-v2`

## Objective

Determine whether OpenClaw's non-bundled-plugin conversation-hook permission gate is preventing the CogentNexus `before_agent_run` hook from entering the Dashboard runner's effective hook registry, and implement the smallest supported repair only if the live configuration evidence proves that condition.

CNX-370 proved the Dashboard semantic path bypasses Ticket-first despite the repaired plugin artifact being active. CNX-371 established the Dashboard Gateway → agent → embedded selection path and the static `before_agent_run` dispatch site. CNX-372 showed that supported runtime diagnostics expose the plugin as loaded/enabled but expose no process-local hook registry. Existing repository evidence documents `hooks.allowConversationAccess=true` as a managed configuration requirement for the CogentNexus lifecycle surface. fileciteturn80file1L17-L24

## Phase 1 — Live configuration diagnosis

1. Synchronize with the current remote branch.
2. Read the authoritative `ACTIVE.md`, `STATUS.md`, this task, and the CNX-372 report.
3. On the real machine, inspect the effective OpenClaw configuration for:
   - `plugins.entries.cogentnexus-openclaw.hooks.allowConversationAccess`
   - relevant `plugins.entries.cogentnexus-openclaw.config` values, especially `ticketFirst`, `preInferenceAdmission`, and `enforcedMode`
4. Prefer supported `openclaw config get` / `openclaw config get --json` or an equivalent read-only effective-config surface. If a supported command reports the path as absent, inspect the raw authoritative OpenClaw config read-only to distinguish absent/default from explicitly false.
5. Record the exact effective value and source of truth.

### Required diagnosis

Classify exactly one:

- `ACCESS_GATE_DISABLED` — effective `allowConversationAccess` is false or otherwise explicitly denies conversation hook access.
- `ACCESS_GATE_MISSING` — effective permission is absent and host defaults deny it for this plugin.
- `ACCESS_GATE_GRANTED` — permission is definitely true and another boundary must explain the bypass.
- `INCONCLUSIVE` — the effective permission cannot be determined safely.

Do not infer from `plugins list --json hookCount: 0` alone.

## Phase 2 — Minimal repair, only if proven

If and only if Phase 1 proves `ACCESS_GATE_DISABLED` or `ACCESS_GATE_MISSING`, apply the smallest supported configuration repair to grant:

`plugins.entries.cogentnexus-openclaw.hooks.allowConversationAccess=true`

Do not alter provider/auth/routing/model settings.
Do not alter Ticket policy.
Do not change `durableAdmissionEligible()`.
Do not add another admission path.
Do not modify Dashboard UI.

Use the existing supported Host/configuration mechanism if one exists. Do not hand-edit generated or transient config unless that is the documented authoritative configuration surface.

## Phase 3 — Deterministic validation

After a proven configuration repair:

- verify effective config is `true`;
- verify the plugin remains loaded/enabled;
- run the smallest relevant configuration/plugin registration regression checks;
- run relevant plugin tests/build/validation required by repository convention;
- record pre/post configuration evidence.

Do not claim Ticket-first restoration yet.

## Phase 4 — Runtime activation

If required to make the configuration effective, use the supported OpenClaw reload/restart mechanism and record exact before/after process identity.

Do not perform a semantic Dashboard request as part of this task unless one minimum-necessary controlled request is genuinely required solely to verify that the configuration is effective. Prefer a separate later semantic requalification task.

## If permission is already granted

If live evidence proves `allowConversationAccess=true`, **do not modify it** and do not search by trial-and-error through unrelated settings. Publish the evidence as a negative finding indicating that the access gate is not the cause, and stop for a separate diagnosis task.

## Hard fences

- No provider/auth/routing/model changes.
- No semantic-contract changes.
- No changes to Dashboard UI/provider layer.
- No duplicate Ticket admission path.
- No changes to `durableAdmissionEligible()` or TicketStore merely to make the semantic test pass.
- No historical edits to CNX-360 through CNX-372.
- No release/tag/main changes.
- No force-push/history rewrite.
- No broad refactor.
- No semantic requalification by default.
- No guessed repair.
- If the effective permission cannot be proven, report `INCONCLUSIVE` and stop.

## Reporting

Publish:

`docs/operations/coordination/reports/CNX-20260916-373-conversation-hook-access-gate-repair-report.md`

Report must include:

- starting/final remote HEAD;
- exact effective config evidence;
- diagnosis classification;
- source/config files changed, if any;
- pre/post values and hashes where applicable;
- validation/test/build results;
- runtime lifecycle mutation evidence, if any;
- semantic request count;
- hard-fence compliance;
- remaining uncertainty;
- recommendation for the next separately authorized task.

After publishing the report, transition coordination to `WAITING_FOR_CHATGPT_REVIEW` and stop.
