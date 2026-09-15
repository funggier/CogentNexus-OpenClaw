# CNX-364 — Path-Bound Runtime Provenance

Parent: `CNX-20260915-363`
Status: `READY_FOR_HERMES`
Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`

## Objective

Prove whether CNX-361 and CNX-362 used the same Host authority state file. If not, identify the differing state roots and establish the strongest durable provenance available for the controller observed by CNX-362. This is an evidence-gap investigation, not a runtime repair.

## Exact evidence gap

```text
CNX-361 controller read
       ?
same physical file?
       ?
CNX-362 controller read
```

## Hard fences

- Do not open Dashboard or send any model request.
- Do not send `CNX361-DONE`, `CNX362-DONE`, or any new semantic test.
- Do not manually edit `controller.json`.
- Do not enable/start/restart/disable/stop, reinstall, modify routing/auth/provider, admission hook, main, or the v0.9.5 tag/release.
- Do not force-push or rewrite history.
- Diagnostic actions must be read-only; do not normalize runtime state.

## Required investigation

Resolve Workspace, stateRoot, controllerPath, legacyRoot, applicationDataRoot, launcherPath, and runtimeAuthorityPath from source. Trace CNX-361 and CNX-362 checkout/workspace/installer/preflight/runtime provenance; inspect every Host-root computation and relevant process/runtime ownership. Use read-only physical path, hash, metadata, manifest, launcher, and runtime-authority evidence where available. Explain timestamp and generation possibilities without inventing semantics. State one primary hypothesis and test only that hypothesis; remain BLOCKED if provenance cannot be established. Add a RED test only if a deterministic current source defect is proven.

## Deliverable

Publish `docs/operations/coordination/reports/CNX-20260915-364-path-bound-runtime-provenance-report.md` with exact branch/head, both provenances, root/path calculations, hashes and ownership evidence, timestamp/generation analysis, process/runtime findings, one hypothesis and result, remaining gap, and explicit zero Dashboard/model requests and zero runtime mutations. Do not claim OpenAI PASS, CURRENT_RED, or runtime repaired.
