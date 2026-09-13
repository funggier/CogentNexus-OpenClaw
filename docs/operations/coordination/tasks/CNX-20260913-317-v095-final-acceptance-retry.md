# CNX-20260913-317 — v0.9.5 Final Acceptance Retry

Status: `READY_FOR_HERMES`
Executor: `Hermes`
Reviewer: `ChatGPT`

Current repaired candidate: `434b27185f7afd17d8cffeede9c016378df0a6aa`
Repair branch: `fix/v0.9.5-final-acceptance-installer-cli`

The previous candidate `a986f3261b1570d1bcb1574d2458fe7068207a9c` exposed a real installer defect. The repaired candidate must now be verified independently.

Hermes is authorized to diagnose the prior Gateway restart/probe timeout using bounded diagnostics first, then use the minimum supported recovery path, install-over the exact repaired candidate, verify installed provenance/fingerprint, enable the plugin, and execute Provider Switch Acceptance, Idle Quiescence (>=2 supervisor cadences), and Controlled Actionable Wake with exactly one durable work item.

Required idle evidence: wakeReason=idle/no-actionable-work; heavyPath=false; heavySupervisorCalls=0; providerRecoveryActions=0; configMutations=0; gatewayLifecycleActions=0; idleTicks>=2. Missing evidence remains INDETERMINATE.

Hard fences: no PR #38 modification or merge; no v0.9.5 tag or GitHub Release; no force push; no secrets exposure/change; no unrelated service/Scheduled Task/Gateway/provider/configuration mutation; no manual Ticket/SQLite/session/transcript/delivery mutation outside documented normal acceptance. Stop BLOCKED for broader/destructive actions.

Every result must bind to `434b27185f7afd17d8cffeede9c016378df0a6aa` and include environment, fingerprint, commands/procedure, timestamps, identity/ownership evidence, checker output, verdicts, and evidence locations.
