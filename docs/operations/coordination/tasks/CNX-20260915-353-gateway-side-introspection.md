# CNX-353 — Gateway-Side Introspection

## Status
READY_FOR_HERMES

## Baseline
- Parent branch: `cnx-352-runtime-registration-observation-boundary`
- Starting HEAD: `596a02f640e05f9e74c85778adc2fcb2b6db8d57`

## Objective
Find the smallest read-only observation boundary that executes **inside the already-running OpenClaw Gateway process** (or uses an authoritative Gateway-owned RPC that reports process-local state) and can attribute CogentNexus registration to that process.

Required chain:

```text
Gateway PID
  -> Gateway-owned introspection
  -> plugin instance
  -> releaseEntry.register()
  -> legacy register(runtimeApi)
  -> before_agent_run registration
  -> effective hook registry
```

CNX-352 established a useful CLI-process seam:
`openclaw plugins inspect cogentnexus-openclaw --json --runtime`
which reports `hookCount=42`, `before_agent_run` priority `2000`, and CNX services. It does **not** bind those observations to Gateway PID `17080`.

## Required investigation

1. Verify GitHub remote branch and ancestry before any work. Local-only state is not evidence.
2. Read CNX-351/CNX-352 reports and the current plugin entry/lifecycle source.
3. Inventory existing Gateway-owned RPC/diagnostic/health/status surfaces for a read-only operator-scoped introspection path that executes in or reports from the Gateway process.
4. Determine whether any existing OpenClaw plugin API or gateway endpoint exposes process-local plugin instances, loaded module identity, registration state, hook registry, handler identity, owner, or priority.
5. Prefer existing seams over new instrumentation. Do not modify production behavior in this task.
6. If an existing safe diagnostic endpoint exists, invoke it read-only and correlate results to the exact Gateway PID from `openclaw gateway status`.
7. If an operator scope is required but unavailable, record the exact limitation and do not weaken security/scope controls.
8. Do not infer process-local registration from `plugins list`, CLI `plugins inspect --runtime`, static source, file hashes, or synthetic tests.
9. Test-only adapters are allowed only around an existing Gateway-owned seam and must not alter production behavior.

## Success criteria

### D PROVEN
Only if a Gateway-side/process-scoped observation shows the running process loaded a stale/different CogentNexus module identity than expected.

### E PROVEN
Only if a Gateway-side/process-scoped observation proves Dashboard/WebChat provider execution without `before_agent_run`.

### OBSERVATION BOUNDARY FOUND
If a trustworthy Gateway-side seam exists but D/E cannot yet be proven, record the exact seam, fields, correlation method, and how a future task can use it.

### UNRESOLVED
If the Gateway still exposes no trustworthy process-scoped boundary.

## Hard fences

No production behavior change, no install/reinstall, no Gateway restart, no provider invocation, no provider-routing change, no runtime/config/database mutation, no Dashboard/WebChat UI interaction, no CNX-344 replay/resend, no changes to `durableAdmissionEligible`, timeout authority, or admission ownership, no v0.9.5 tag/history mutation, no force-push/history rewrite, no self-acceptance.

## Testing

Run only read-only diagnostics and existing focused tests where dependencies are already available. If blocked, record the exact command and error. Do not install dependencies solely to obtain a green result.

## Final report

Create:
`docs/operations/coordination/reports/CNX-20260915-353-gateway-side-introspection-report.md`

The report must contain exact starting remote HEAD, exact final GitHub HEAD, ancestry, Gateway PID, Gateway-owned seam(s) examined, exact commands/results, process correlation, registration/hook observations, D/E/observation-boundary/unresolved classification, production-change declaration, hard-fence verification, and the smallest next probe.

## Completion contract

Commit and push the report to this branch. Verify the remote branch tip independently from GitHub. Read the final report back from that remote tip before declaring CNX-353 complete.
