# CNX-20260918-412 — ChatGPT Review

## Decision

`ACCEPTED`

Accepted classification:

`MAINTENANCE_CONVERGENCE_LOCAL_VALIDATION_GREEN`

## Independent verification

GitHub authority was re-read after CNX-412 publication.

Verified:

- remote HEAD: `e173ff9702dbd623928b31d53a6040109c482d09`;
- report blob: `a751647ec2241883d6a4a09637d24360e0c295d3`;
- ACTIVE/STATUS: `WAITING_FOR_CHATGPT_REVIEW`;
- focused CNX-411 regression: 10 tests GREEN;
- required regression group: 26 tests GREEN with the repository script directory on `PYTHONPATH`;
- bounded broader suite: 301 tests GREEN, 1 skipped;
- no additional source/test repair;
- no production/live mutation.

## Review of the unfiltered-suite exclusions

The unfiltered discover result does not invalidate CNX-411.

### 1. `test_host_v091_single_authority::test_plugin_authority_has_no_policy_marker_bypass`

The failing assertion searches for the obsolete literal:

`if (mode === "managed" || mode === "passthrough") ...`

Current `v091-release-entry.ts` performs the same authority decision against the canonical/legacy-normalized `effectiveMode`:

`if (effectiveMode === "managed" || effectiveMode === "passthrough") ...`

The assertion is stale source-string coupling. CNX-411 does not touch this TypeScript authority surface.

Classification:

`NON_CAUSAL_STALE_TEST_ASSERTION`

### 2. `test_supervisor_quiescence`

The excluded failures are Windows `multiprocessing.get_context("spawn")` readiness/timing failures around cross-process Events/joins.

CNX-411 changes neither:

- `supervisor_quiescence.py`;
- operation-lock semantics;
- multiprocessing helpers;
- quiescence lease ownership.

The CNX-411 focused and provider-neutral supervisor suites pass.

Classification:

`NON_CAUSAL_PLATFORM_TIMING_BASELINE`

### 3. `test_manage_agents_policy`

The failure is an invocation/import-layout issue for:

`from scripts.manage_agents_policy import ...`

It is unrelated to:

- Host Supervisor;
- maintenance marker lifecycle;
- provider-neutral runtime;
- wake authority.

Classification:

`NON_CAUSAL_TEST_IMPORT_LAYOUT_BASELINE`

## Repair acceptance

CNX-411 correctly preserves the architectural constraints:

- no manual marker deletion;
- no provider routing/lifecycle authority;
- no Ollama-specific recovery requirement;
- no legacy heavy Supervisor merely to clear a marker;
- read-only tick remains non-mutating;
- execute-safe tick uses existing provider-neutral `lifecycle start` health verification;
- marker retirement is verified before convergence is claimed.

## Production sequencing consequence

The installed production runtime still predates CNX-411 and currently has the stale `healthy-runtime` marker observed by CNX-410.

Therefore the new repair cannot clear that already-existing marker until it is installed, while the install hazard gate requires the marker to be absent.

The successor must break this bootstrap deadlock using the narrowest already-supported old-runtime primitive:

```text
installed runtime.py lifecycle start
(no --provider)
```

exactly once, and only after re-proving:

- Gateway healthy;
- marker is active with `recoveryPolicy=healthy-runtime`;
- pending outbox = 0;
- no active provider incident;
- SQLite integrity = OK;
- no actionable durable recovery/delivery hazard.

This command is preferable to public `cnxclaw start` for this one-time bootstrap because the public Host start path can perform terminal/session/direct-recovery reconciliation beyond what is needed to retire the marker.

After the narrow lifecycle command:

- marker must be absent;
- recovery must be `READY`;
- delivery must remain `READY` / pending 0;
- SQLite integrity must remain OK.

Only then may the exact repaired candidate be installed.

## Reviewer

ChatGPT

Human final authority: Operator
