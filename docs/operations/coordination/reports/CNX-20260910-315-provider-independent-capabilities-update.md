# CNX-20260910-315 — Provider-independent capability repair

## Scope

Task315 continued from the lifecycle-hardening checkpoint. This update repairs the remaining provider-mode capability gates without changing OpenClaw provider/model/auth ownership.

## Root cause

The v0.9.5 compatibility path still treated `providerMode=passthrough` as a capability kill-switch. In particular, the release entry:

- suppressed `registerService` in passthrough;
- forced `autoResume=false`, `autoRotate=false`, and `autoWorkflowCompletion=false`;
- filtered core hooks to a reduced subset;
- skipped native restart ownership fencing;
- skipped Direct recovery startup-liveness;
- installed only a reduced managed-runtime guard set.

The legacy `index.ts` also contains provider-mode gates around durable admission, compaction continuation, interrupted resume, workflow completion, and Ticket recovery. The release entry now neutralizes `providerMode` for that legacy capability decision so the provider setting remains metadata rather than capability authority.

## Repair

Commit: `c35194cffe4a3aaf37e03c6d2cb75c5a580ce82b`

Changed:

- `passthrough` keeps `providerMode` as compatibility metadata but passes `undefined` into the legacy capability decision;
- the legacy registration API is no longer replaced with a service-blocking/hook-filtering shim;
- native restart ownership fence is installed for both managed and passthrough Host-authorized modes;
- Direct recovery startup-liveness is installed for both modes;
- durable delivery boundary, Direct model-call lease, dashboard delivery, and Direct recovery lane fence are installed for both modes;
- Host authorization remains the activation boundary; provider/auth/routing remain OpenClaw-owned.

## Tests

Added `plugins/cogentnexus-openclaw/tests/v0.9.5-provider-independent-capabilities.test.ts` covering:

- no service suppression in passthrough;
- no auto-resume/workflow completion suppression;
- no provider-mode conditional recovery fences;
- providerMode retained only as compatibility metadata.

## Verification

Source was fetched from the exact working branch after the repair and the commit diff was inspected. GitHub Actions currently reports no workflow run for the repair commit, so full CI GREEN is not claimed.

## Next

Proceed to fresh verification of Direct `agent_end(false)` / model-call terminal-error behavior and cross-provider capability tests. Do not release/tag v0.9.5 until the full validation matrix produces fresh evidence.
