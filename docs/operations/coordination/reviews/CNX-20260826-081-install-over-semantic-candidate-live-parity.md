# Review — CNX-20260826-081 Install-Over Semantic Candidate Live Parity

Decision: `ACCEPT`

Disposition: `ACCEPT_BLOCKER_SUPPORTED_INSTALL_OVER_NPM_PACK_PARSER`

Reviewed report HEAD: `ade320d2c32dde1143c2e8dc4ffbf8f3580e44a1`

Coordination execution HEAD: `27e9726d765ef3719dd5abebbde04fd1e897bc0e`

Accepted semantic candidate attempted by Task 081:

`70d02e76233ca1084da445d488f88b628455f4aa`

## Publication fence

Independent comparison proves:

`27e9726d765ef3719dd5abebbde04fd1e897bc0e -> ade320d2c32dde1143c2e8dc4ffbf8f3580e44a1`

is exactly one commit and changes only:

`docs/operations/coordination/reports/CNX-20260826-081-install-over-semantic-candidate-live-parity.md`

No source/test or coordination mutation is hidden in the Task-081 report fence.

## Accepted live facts

Task 081 correctly obeyed the one-attempt and semantic fences:

- exactly one supported normal install-over was invoked from the exact accepted candidate checkout;
- preflight ownership verification passed;
- recovery preflight returned `OWNERSHIP_PRESENT`;
- install classification was `upgrade`;
- no fresh-install transaction was started;
- no semantic user prompt, Dashboard/WebChat turn, CLI semantic run, direct Ollama probe, Ticket creation, nonce consumption, manual SQLite edit, uninstall/reset/cleanup/retry, reboot, merge, tag or release occurred;
- the installer returned nonzero and was not retried.

The live post-failure state is accepted as a real supported-installer partial state and must not be normalized manually:

- Gateway remains healthy and dashboard HTTP remains `200`;
- Ollama remains healthy with the accepted four-model inventory unchanged;
- authoritative product SQLite integrity remains `ok`, with zero Tickets and zero outbox rows;
- the candidate skill tree copied before failure matches the accepted candidate source tree (86 considered files, excluding `__pycache__`);
- the prior ownership manifest remains readable and verification passes;
- controller is `passthrough`;
- startup policy is disabled;
- Supervisor Scheduled Task is absent;
- AGENTS managed block is absent;
- the prior canonical plugin generation remains registered but disabled;
- launcher remains present and points at the previously owned runtime.

This partial state is not a Task-081 success and does not satisfy source/live plugin parity, MANAGED runtime acceptance, no-flash acceptance or Dashboard semantic readiness.

## Independent source diagnosis

The failure occurred at the production installer boundary after:

`npm pack --json`

when `scripts/install.ps1` parsed the output and required exactly one item with `.filename`.

The candidate installer currently performs:

```powershell
$packOutput = (& npm pack --json | Out-String)
$packed = $packOutput | ConvertFrom-Json
$packedItems = @($packed)
if ($packedItems.Count -ne 1 -or -not $packedItems[0].filename) {
    throw "npm pack did not return exactly one package artifact"
}
```

The repository already contains independent compatibility evidence in:

`plugins/cogentnexus-openclaw/scripts/verify-package-contents.mjs`

which explicitly normalizes two supported npm JSON shapes:

1. an array result; and
2. npm >= 12 single-entry object keyed by package name, normalized via `Object.values(...)`.

That verifier passed in Task 081 while the installer parser failed later. The installer therefore has a real packaging-boundary compatibility gap: it does not implement the already-recognized npm-shape normalization used by package verification.

Task 081 did not record the exact raw `npm pack --json` stdout and npm version at the failing command, so independent review does not claim a specific runtime shape as an observed fact. The successor must reproduce and record the exact Windows/PowerShell/npm shape before editing production.

## Decision

`BLOCKED_SUPPORTED_INSTALL_OVER` is accepted as the correct Task-081 result.

Do not retry the live installer from the current source and do not manually restore Supervisor/AGENTS/plugin/controller state.

A source-only successor must first repair and executable-test the `npm pack --json` artifact boundary across the supported npm 11/npm 12 paths and Windows PowerShell 5.1. Only after independent acceptance may a separate live recovery task perform one supported install-over from the corrected source to restore MANAGED/source-live parity/no-flash state.
