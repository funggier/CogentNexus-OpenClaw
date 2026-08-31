# CNX-20260831-188 Checkpoint 02 — Pre-Windows Requalification Freeze

Status: `DURABLE_CHECKPOINT`
Parent task: `CNX-20260831-188`
Execution subtask: `CNX-20260831-189`
Date: 2026-08-31 ICT

## Exact product candidate

The documentation-corrected v0.9.3 product/repository candidate is frozen at:

`604569c286e930f1a596362ab926b065b56d486e`

This SHA remains the Windows requalification candidate even after later coordination-only commits advance the working branch.

## Candidate identity

- version: `0.9.3`
- package payload-v2: `408167da1bfba7fa9723d1bd557f29d516ed27c27398b4e48abf9a4f294e6b5b` / `184` files
- installed skill-tree Git tree: `a1e873ba404205507a1623961b49f1b1a0689f9f`
- executable scripts-tree Git tree: `3d9d323ba19443d46e970b87cef52ce878da274f`
- accepted facade Git blob: `879083d6186589d4b2774b8fd87fa93692dd2dfc`
- accepted facade SHA-256: `aa747f8f30080ef839a8d2cbf5758f9981a007ca01f41a988576f42edea8682f`

## Intentional documentation-bearing product changes

Only these installed/payload product docs changed under Task 188:

- `plugins/cogentnexus-openclaw/README.md`
- `skills/cogentnexus-openclaw/SKILL.md`
- `skills/cogentnexus-openclaw/references/architecture.md`
- `skills/cogentnexus-openclaw/references/scheduler-adapters.md`

Executable/runtime/plugin source, tests, dependencies, and workflow behavior were not changed.

## Exact-candidate repository validation

All required push-triggered repository gates for `604569c286e930f1a596362ab926b065b56d486e` completed successfully:

- Validate run `33382417045` — `success`
- Windows Installer Pack Smoke run `33382417032` — `success`
- PS5.1 Acceptance Smoke run `33382417028` — `success`

Package proof:

- artifact ID: `9754267508`
- payload-v2: `408167da1bfba7fa9723d1bd557f29d516ed27c27398b4e48abf9a4f294e6b5b`
- fileCount: `184`
- dry-run tar.gz SHA-256: `16523b0226aed0aa1eb58a3e335bfadb34abdc027777806bd7c74133c07c3457`
- dry-run zip SHA-256: `e273a967771f281c895402dd8b2078bd1ec6c1944d9a8e817cf73f467e38fc06`

## Requalification boundary

Because the implementation already passed the full Windows stabilization/lifecycle sequence, Task 189 is intentionally bounded to:

`one exact-candidate install-over -> installed provenance/health/byte proof -> one human Dashboard semantic/durable-delivery turn`

Reset, uninstall, and fresh reinstall are excluded by default. If new evidence suggests those boundaries must be repeated, Task 189 must stop and request scope expansion rather than performing destructive actions automatically.

## Execution transport note

This ChatGPT session does not expose an installed Hermes/LConnect/Windows remote-execution connector. Therefore publishing Task 189 in the repository is the durable handoff boundary. Windows requalification must not be represented as executed until Hermes or the Windows operator publishes real evidence.

## Resume point

1. Hermes reads Task 189 and fresh GitHub authority.
2. Hermes performs read-only preflight.
3. Hermes installs over exactly `604569c286e930f1a596362ab926b065b56d486e` once.
4. Hermes proves installed docs/executable identity/health.
5. Hermes performs or requests exactly one human Dashboard semantic send.
6. Hermes publishes the Task-189 report and stops.
7. ChatGPT reviews the report and resumes Task 188 publication path if PASS.

This checkpoint is not a final Task-188 report and does not authorize release publication by itself.
