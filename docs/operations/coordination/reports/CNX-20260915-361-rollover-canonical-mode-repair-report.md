# CNX-20260915-361 — Rollover canonical-mode repair report

## Classification

`SOURCE REPAIR PASS; EXACT REPAIRED CANDIDATE ACTIVATION PASS; DASHBOARD NOT RUN`

CNX-361 repaired and validated the canonical-mode rollover boundary. The supported activation lifecycle completed once on the repaired candidate. No Dashboard control, request, model inference, `CNX359-DONE`, or `CNX360-DONE` was performed.

## Authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Remote exact commit after source repair: `2d31dc6feaffb54f6a385ec537271310502b65c0`
- Parent: `CNX-20260915-360`
- Source checkout: `C:\Users\CDQ-P\.hermes\workspace\cnx361-remote`
- Remote ref verification: `git ls-remote` returned `2d31dc6feaffb54f6a385ec537271310502b65c0`

## Root cause

`CANONICAL_MODE_SCHEMA_MISMATCH_AT_ROLLOVER_BOUNDARY` was confirmed. `scripts/install.ps1` accepts canonical `cnxMode=disabled` by deriving legacy `mode=passthrough`, while the rollover ownership consumer read only `controller.get("mode")`. A canonical-only controller therefore reached `_require_passthrough()` with an effective `None` and failed closed before candidate activation.

## RED evidence

Test added before production repair:

`tests/test_fresh_transaction_failure_coverage.py::test_require_passthrough_accepts_canonical_disabled_mode`

Exact result against the unmodified implementation:

```text
FAILED ... RuntimeError: plugin generation rollover requires PASSTHROUGH mode; observed None
1 failed in 1.90s
exit 1
```

The failure was the expected product assertion at `namespace_ownership.py:783`, not a harness or dependency failure.

## GREEN and regression evidence

Changed source:

- `skills/cogentnexus-openclaw/scripts/namespace_ownership.py`

Changed tests:

- `tests/test_fresh_transaction_failure_coverage.py`

The repaired boundary:

- accepts `cnxMode=disabled` as `passthrough`;
- accepts legacy `mode=passthrough`;
- rejects `active`/`managed`;
- rejects `maintenance`;
- rejects unknown, missing, malformed, and conflicting mode state.

Results:

- focused transaction/rollover/finalization tests: `106 passed`;
- full Python suite: `670 passed, 5 skipped, 5 failed`.
- The five full-suite failures were pre-existing documentation/version contract failures in `test_install_docs_authority.py`, `test_release_version_094_contract.py`, and `test_v094_current_docs_contract.py`; none touched the repaired source boundary. No unrelated documentation repair was bundled.
- plugin `npm test`: `76 test files, 338 tests passed`;
- plugin `npm run build`: exit `0`;
- `npm run plugin:validate`: exit `0`, artifact verification PASS, ticket DB bootstrap PASS, packed file count `246`.

## Static source consistency check

Direct mode consumers found outside the repaired boundary include the legacy/read-only compatibility code in:

- `skills/cogentnexus-openclaw/scripts/checks_v092.py`
- `skills/cogentnexus-openclaw/scripts/namespace_ownership.py`

The installer and canonical host facade already translate `cnxMode` using the repository vocabulary. The additional legacy consumer was not changed because it is outside the exact CNX-360 rollover path; no unrelated repair was bundled.

## Artifact identity

- source commit: `2d31dc6feaffb54f6a385ec537271310502b65c0`
- package: `openclaw-plugin-cogentnexus-openclaw-0.9.5.tgz`
- package SHA-256: `210e890278485e7e4ad31458923b633cbedee5ab1ea5dcd11367402fabfe6945`
- package npm pack shasum: `d6f5bcf1410840572a8dda85b9790de14dd281e8`
- source payload fingerprint: `3a889d6ef3bd0ba0f957cac00ff86868c315527bde0d3d87607eb91daca089e5`

## Activation evidence

Supported lifecycle command, invoked exactly once:

```text
powershell.exe -NoProfile -ExecutionPolicy Bypass -File C:/Users/CDQ-P/.hermes/workspace/cnx361-remote/scripts/install.ps1
```

It completed with exit `0` and printed `CogentNexus-OpenClaw v0.9.5 installation completed successfully.` The repaired `plugin-rollover-prepare` and `plugin-rollover-finalize` stages both completed with exit `0`.

Installed artifact/runtime binding:

- installed root: `C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw`
- installed payload fingerprint: `3a889d6ef3bd0ba0f957cac00ff86868c315527bde0d3d87607eb91daca089e5`
- source and installed fingerprint: equal
- source `dist/v091-release-entry.js` SHA-256: `da8e810e88547ef866e2279fde86195f02557a9ca0a35a8771a0e646a1f6a7ef`
- installed `dist/v091-release-entry.js` SHA-256: `da8e810e88547ef866e2279fde86195f02557a9ca0a35a8771a0e646a1f6a7ef`
- source and installed entry module bytes: equal
- `openclaw plugins list --json`: plugin version `0.9.5`, source installed root `...extensions\cogentnexus-openclaw\dist\v091-release-entry.js`, `enabled=true`, `status=loaded`.
- controller after activation: `cnxMode=active`, `desiredGateway=running`, generation `103`, schema version `2`.

This proves:

```text
SOURCE COMMIT -> PACKAGE -> INSTALLED ARTIFACT -> ACTIVE RUNTIME
```

for the repaired candidate identity. The runtime inventory reported `hookCount=0` and `configSchema=false`; this is recorded evidence, not silently upgraded to a semantic or Dashboard claim.

## Changed paths

- `docs/operations/coordination/tasks/CNX-20260915-361-rollover-canonical-mode-repair.md`
- `skills/cogentnexus-openclaw/scripts/namespace_ownership.py`
- `tests/test_fresh_transaction_failure_coverage.py`
- this report

## Remaining proof gap / stop boundary

OpenAI Ticket-first live semantic acceptance remains unproven and is a separate question. CNX-361 stops before Dashboard. Operator may now open a **new** Dashboard session, select `OpenAI / gpt-5.6-luna`, reset/new session, and send exactly one request: `Reply exactly with CNX361-DONE.` Hermes must not control Dashboard.
