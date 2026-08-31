# CNX-20260827-087 — Live Attested Pending-Rollover Recovery and Parity

Result: `BLOCKED_SUPPORTED_PENDING_RECOVERY_INSTALL_OVER`

## Execution

Task 087 was authorized for exactly one supported normal install-over from exact source:

`71f48c1a134ee9b2646b4cc7f077abe9cae59ebb`

Fresh evidence directory:

`C:\Users\CDQ-P\AppData\Local\Temp\cnx-next-20260827T002454Z`

Coordination execution HEAD:

`e55414f690046f4562aaae148b1c4d0339756d38`

Exact deployment checkout:

`C:\Users\CDQ-P\AppData\Local\Temp\cnx-next-20260827T002454Z\deploy-71f48c1`

The deployment checkout was clean at exact accepted source HEAD before the supported invocation.

Versions:

- Windows: `10.0.19045.6466`
- Windows PowerShell: `5.1.19041.6456`
- Node: `v24.18.0`
- npm: `11.16.0`
- OpenClaw: `2026.7.1-2 (0790d9f)`

## Pre-mutation attested preflight

The preflight was read-only and passed the required baseline:

- recovery preflight: `OWNERSHIP_PRESENT`
- controller: `passthrough`, generation `13`
- startup disabled
- Supervisor absent
- AGENTS managed markers: `0`
- ownership manifest points to prior generation `g-5593cbcfff5b35d5`
- canonical generations: exactly `2`
- old fingerprint:
  `7e9189f81eeda728a35a0722f69cfd4a3b48e0fac36fde8d846a188072577332`
- replacement fingerprint:
  `8fd911e3b8f6326c8907b7d92c11028d931df203dcaafdb59cc1e6d0a3b56360`
- exact source fingerprint:
  `8fd911e3b8f6326c8907b7d92c11028d931df203dcaafdb59cc1e6d0a3b56360`
- replacement equals exact source
- old differs from replacement
- OpenClaw registration pointed to `g-7257c4555ca8ad21`, disabled, version `0.9.3`
- attested classifier:
  - `mode=upgrade`
  - `pendingRollover=true`
  - `pluginAlreadyExact=false`
  - manifest path = prior generation
  - replacement path = newer generation
  - expected replacement fingerprint = exact source fingerprint
- lifecycle actions:
  - `installPlugin=false`
  - `rolloverPlugin=true`
- Gateway read-only status: running, connectivity probe `ok`
- no semantic/provider run active

Candidate source-only validation also passed before the live invocation:

- `npm ci`: passed
- `npm run plugin:validate`: passed
- mixed-plugin artifact verification: passed
- Ticket DB bootstrap validation: passed
- package contents validation: passed
- production AST helper: corrected sibling rollover gate verified

No direct Ollama probe was performed, as forbidden by the coordination fence; accepted provider readiness evidence was preserved.

## Exactly one supported live invocation

The only live-changing command was invoked exactly once:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1 -Workspace C:\Users\CDQ-P\.openclaw\workspace -Provider ollama
```

The command ran from the exact `71f48c1...` deployment checkout with PATH pinned to `C:\Program Files\nodejs`.

Invocation count:

`1`

Retry count:

`0`

Installer exit status:

`1`

Complete captured installer log:

`C:\Users\CDQ-P\AppData\Local\Temp\cnx-next-20260827T002454Z\a06-installer.log`

Failure:

```text
install.ps1 : Cannot validate argument on parameter 'Mode'.
The argument "-Mode" does not belong to the set "fresh,legacy,upgrade" specified by the ValidateSet attribute.
FullyQualifiedErrorId : ParameterArgumentValidationError,install.ps1
```

The failure occurred after source-side `npm ci` and `plugin:validate` output, before the live pending rollover completed. The command did not reach a successful installer result.

## Required no-retry disposition

Because the single supported installer invocation returned nonzero, Task 087 requires immediate stop. No installer retry, manual repair, uninstall, reset, cleanup, manual rollover, generation edit, controller edit, AGENTS edit, Supervisor edit, provider/model change, semantic message, or direct Ollama probe was performed after failure.

## Post-failure read-only state

Post-failure evidence was captured without mutation:

- controller remains `passthrough`
- controller generation remains `13`
- controller SHA-256:
  `84684c86e2af0653062a6ea27e283b8a4d188cf5f50de2049747f57df035558f`
- ownership manifest remains bound to prior generation `g-5593cbcfff5b35d5`
- ownership manifest SHA-256:
  `3428c74b9f51389de7a1934630102896bae90c060b2b65e51fd2dbc1380b3bed`
- canonical generation count remains `2`
- old fingerprint remains:
  `7e9189f81eeda728a35a0722f69cfd4a3b48e0fac36fde8d846a188072577332`
- newer replacement fingerprint remains:
  `8fd911e3b8f6326c8907b7d92c11028d931df203dcaafdb59cc1e6d0a3b56360`
- OpenClaw plugin inventory command exit: `0`
- OpenClaw inventory contains `72` plugin records total
- CogentNexus registration remains one disabled `0.9.3` registration at `g-7257c4555ca8ad21`
- no third canonical generation observed
- AGENTS managed markers remain `0`
- Supervisor remains absent
- Gateway remains running and connectivity probe remains `ok`
- semantic messages generated: `0`
- provider probes generated: `0`
- installer retry count: `0`

Raw post-failure inventory:

`C:\Users\CDQ-P\AppData\Local\Temp\cnx-next-20260827T002454Z\a08-postfailure-inventory.json`

Structured post-failure snapshot:

`C:\Users\CDQ-P\AppData\Local\Temp\cnx-next-20260827T002454Z\a07-postfailure.json`

## Mutation accounting

The authorized installer did execute and returned nonzero; therefore the live mutation accounting is not claimed as zero globally. No separate/manual mutation was performed.

- supported installer invocations: `1`
- installer retries: `0`
- separate manual repair/cleanup/rollover: `0`
- separate uninstall/reset/clean reinstall: `0`
- separate plugin generation mutation: `0`
- separate controller/startup/Supervisor/AGENTS/ownership/config/runtime/SQLite/session mutation: `0`
- semantic messages: `0`
- Dashboard/WebChat/CLI sends: `0`
- direct Ollama/provider probes: `0`
- provider/model/timeout changes: `0`
- restart/reboot: `0`

## Reason for blocker and successor scope

The source/control-plane task was accepted and the live preflight was correct. The supported installer still failed at its own parameter-boundary invocation:

```text
Cannot validate argument on parameter 'Mode': argument "-Mode" is not in fresh,legacy,upgrade
```

This is a production installer orchestration defect exposed by the one authorized live attempt. Do not retry this installer command under Task 087.

A successor source repair must correct the action-resolver invocation boundary, add a regression through the real installer invocation path, and be independently reviewed before any further live attempt is considered. The preserved two-generation live topology must not be manually normalized.

## Publication fence

Task 087 is blocked and publishes only this report.

No product source was changed by Task 087. The exact source used was:

`71f48c1a134ee9b2646b4cc7f077abe9cae59ebb`

Final result token:

`BLOCKED_SUPPORTED_PENDING_RECOVERY_INSTALL_OVER`
