# CNX-20260825-061 — Review

Decision: `ACCEPT`

Disposition: `ACCEPT_BLOCKER_MANAGED_REENTRY_ACCEPTANCE_MODEL_MISMATCH`

Reviewed report commit:

`3029ca88d4814f7da2c6e6a088a85692452dc453`

Accepted report result:

`BLOCKED_POST_ENABLE_VERIFICATION`

## Review conclusion

The Task 061 report is accepted as an accurate bounded execution record. Hermes followed the task fence: one supported `cnxclaw enable` invocation was observed with numeric exit code `0`, the resulting MANAGED state was inspected, the two mandatory Task 061 postconditions that did not match were reported, and no retry, manual repair, disable, rollback, config edit, AGENTS edit, plugin mutation, or second lifecycle transition was performed.

The blocker is not accepted as proof that MANAGED re-entry itself failed. Independent source review after the report shows that Task 061 modeled several postconditions against the wrong execution layer. The installed v0.9.3 operator path is a compatibility stack, not a direct call to the base `host.py` lifecycle.

## Publication fence verification

Independent comparison from Task 061 fetched execution HEAD:

`504dad20f1122c29e77321982980e7d3de72a4de`

to report commit/current branch before this review found exactly one descendant commit and exactly one changed path:

`docs/operations/coordination/reports/CNX-20260825-061-return-managed-lifecycle.md`

Direct commit inspection confirms report commit `3029ca88d4814f7da2c6e6a088a85692452dc453` adds only that matching report.

## Accepted execution facts at report time

Task 061 durably reports that, immediately after its one supported `cnxclaw enable` invocation:

- the command exited `0` and returned `result: ok`;
- controller mode was MANAGED;
- desired Gateway/provider were running;
- the canonical v0.9.3 replacement plugin was enabled and loaded;
- startup policy was enabled and the CogentNexus supervisor Scheduled Task existed, enabled and hidden;
- Gateway and Ollama were healthy;
- SQLite integrity was `ok` with bounded ticket/event/outbox/session counts zero;
- ownership remained bound to the accepted replacement generation with SHA-256 `0667004DC9D6483450A3C99DDA6F34BB7F384F0261F43813763019E2C3BA0341`;
- the accepted replacement tree and retired-generation rollover-backup tree were unchanged;
- exactly one canonical v0.9.3 payload remained under OpenClaw state;
- no manual repair or repeated lifecycle side effect occurred.

These are historical report-time facts only. The operator subsequently reported an unexpected machine power loss. Therefore no Task 061 runtime observation may be treated as the current live state without a fresh post-boot inspection.

## Root-cause review: Task 061 acceptance-model mismatch

### 1. Actual v0.9.3 operator path is layered

`skills/cogentnexus-openclaw/scripts/cnxclaw_v093.py` is explicitly the v0.9.3 Ollama-only facade over the accepted v0.9.2 implementation. Lifecycle commands including `enable` are forced toward Ollama and delegated to the v0.9.2 facade.

`skills/cogentnexus-openclaw/scripts/cnxclaw.py` is that v0.9.2 operator facade and binds:

`HOST_CONTROL = host_control_v092.py`

Its provider transition does more than the base Host transition: it opens/commits provider-route state, runs the Host lifecycle, performs a Gateway process boundary for `enable`, and commits provider selection. Those operations can update controller generation independently.

Therefore Task 061's requirement that generation must be exactly `8` after one operator-level `enable` is not a valid invariant for the actual v0.9.3 execution path. The reported final generation `12` is evidence that must be accounted for against the real layered path, not treated as a base-Host single-transition failure.

### 2. Scheduled Task target in Task 061 was specified against the wrong layer

`skills/cogentnexus-openclaw/scripts/startup_v092.py` intentionally overrides the startup Host control path to:

`host_control_v092.py`

The Task 061 report observed the Scheduled Task invoking `host_control_v092.py`. That is consistent with the current v0.9.2 compatibility architecture used by v0.9.3. The Task 061 requirement that its arguments point directly to `host_control.py` was therefore incorrect and must not be carried into a remediation task.

### 3. Managed config timing values in Task 061 were specified from the base Host, not the active overlay

The active transactional v0.9.1 Host compatibility layer (`host_v091.py`), which is retained under the v0.9.2/v0.9.3 path, defines managed settings including:

- `ticketFirst=true`;
- `preInferenceAdmission=true`;
- `autoWorkflowCompletion=true`;
- `enforcedMode=true`;
- `autoResume=true`;
- `workspaceDir=<workspace>`;
- `ticketDispatchLimit=1`;
- `ticketMaximumRunning=1`;
- `ticketMaximumAttempts=5`;
- `ticketRecoveryPollMs=60000`;
- `ticketDispatchPollMs=60000`;
- `ticketOutboxPollMs=60000`;
- `completionPollMs=60000`;
- `contextMaintenancePollMs=30000`.

Task 061 instead required several `5000` millisecond values from the base `host.py`. Those exact values are not authoritative for the real v0.9.3 operator path.

## Findings that remain unresolved

### F1 — AGENTS non-managed content drift remains a real diagnostic question

The report shows the managed block itself matched the registered policy, but removing that block from the post-enable `AGENTS.md` did not reproduce the accepted pre-enable baseline hash.

The repository has a simple policy round-trip unit test, but that test does not prove byte-exact round-trip behavior for the actual 7,196-byte workspace baseline, including its real newline and boundary whitespace shape.

No AGENTS edit is authorized from this review. The successor must identify the exact byte/line-ending/whitespace delta from retained evidence or bounded backups before any repair is proposed.

### F2 — managed plugin config persistence remains potentially genuine

The current plugin schema contains the reported managed configuration keys, and the active transactional `host_v091.enable` path explicitly stages managed configuration and validates it before enabling the plugin. Therefore the Task 061 observation that most bounded keys read empty after an exit-0 enable cannot be dismissed merely because some Task 061 expected values were wrong.

The successor must determine read-only whether those keys were never persisted, were later overwritten/normalized by the provider-route/process-boundary stack, were read from an incorrect config surface, or changed after execution. No `config set`, `config unset`, plugin toggle, or lifecycle retry is authorized until this is bounded.

## Power-loss boundary

After Task 061 publication the operator reported an unexpected power loss. This creates a new evidence boundary.

The successor must begin with fresh post-boot observation before relying on any current runtime assumptions. The power loss is also directly relevant to CogentNexus continuity goals, so startup task execution, controller timestamps/generation, Gateway/provider recovery, Ticket/session/recovery rows, and ownership preservation must be inspected without forcing recovery actions.

## Safety disposition

This review does **not** authorize:

- another `cnxclaw enable`, `disable`, `start`, `stop`, or `restart`;
- OpenClaw plugin enable/disable/install/uninstall;
- OpenClaw config mutation;
- AGENTS mutation or reconstruction;
- startup Scheduled Task mutation;
- installer, reset, uninstall, rollover plan/apply, generation cleanup, or ownership rewrite;
- Gateway/Ollama/provider/model mutation;
- process termination;
- primary repository mutation;
- merge, tag, release, or archive publication.

## Next gate

Create a diagnosis-only successor that treats the reboot as a fresh live-state boundary, reconstructs the exact v0.9.3 operator execution chain, accounts for generation/startup semantics against that chain, and diagnoses F1/F2 with read-only evidence.

A repair task may be created only after that diagnostic report is reviewed.
