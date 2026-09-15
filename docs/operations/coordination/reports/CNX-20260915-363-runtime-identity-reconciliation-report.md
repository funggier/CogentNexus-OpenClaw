# CNX-20260915-363 — Runtime identity reconciliation report

## Classification

`BLOCKED`

The regression boundary is explained at the code-semantics level, but the available durable evidence does not establish the actual writer, event, or exact path that produced the live CNX-362 controller. No runtime state was normalized and no source repair was made.

This is a Host runtime-state reconciliation problem. It is not classified as a Dashboard or OpenAI defect.

## Authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Remote HEAD inspected: `d09762bf4559b16d410db01089fdcfc9744c414f`
- Parent task: `CNX-20260915-362`
- Investigation checkout: `C:\Users\CDQ-P\cnx363-work`
- Checkout status before report: clean at the detached exact remote HEAD, apart from this task/report creation

## Accepted and observed identities

CNX-361 accepted:

```text
schemaVersion=2
cnxMode=active
desiredGateway=running
generation=103
```

CNX-362 read-only preflight observed:

```text
schemaVersion=1
mode=passthrough
desiredGateway=running
generation=1
updatedAt=2026-08-29T01:36:31.541994+00:00
```

Exact transition:

```text
CNX-361:
schemaVersion=2
cnxMode=active
generation=103

        ↓

CNX-362:
schemaVersion=1
mode=passthrough
generation=1
```

The CNX-362 installed plugin identity remained:

```text
version       = 0.9.5
enabled       = true
status        = loaded
installed root= C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw
entry SHA-256  = da8e810e88547ef866e2279fde86195f02557a9ca0a35a8771a0e646a1f6a7ef
hookCount      = 0
configSchema   = false
```

## Controller writers discovered

### Canonical v0.9.5 Host state

`skills/cogentnexus-openclaw/scripts/host_state_v095.py` is the canonical writer:

- `default_state()` — initialization value: schema 2, `cnxMode=active`, `desiredGateway=running`, generation 1.
- `migrate_v094_state()` — read/translation only; it returns canonical schema-2 state and does not persist the file.
- `load_state()` — read/translation only; missing-file fallback is in-memory only.
- `save_state()` — canonical persistence; calls migration with schema 2 and atomically replaces `host/controller.json`.
- `transition_mode()` — lifecycle/authority transition writer; increments generation only when mode or desired gateway changes.

`skills/cogentnexus-openclaw/scripts/host.py` is a compatibility façade over that canonical implementation:

- `default_state()` — in-memory compatibility view only.
- `load_state()` — read-only canonical load plus derived legacy `mode`.
- `save_state()` — writes through the canonical v0.9.5 writer and explicitly forces schema 2.
- `transition()` — lifecycle/authority transition writer through canonical `save_state()`.

These v0.9.5 paths cannot legitimately persist the observed schema-1 shape.

### Legacy compatibility Host

`skills/cogentnexus-openclaw/scripts/host_legacy_v094.py` contains the exact legacy writer capable of the observed shape:

- `default_state()` — schema 1, legacy `mode`, desired gateway running, generation 1.
- `load_state()` — legacy schema-1 read-only validation.
- `save_state()` — forcibly persists `schemaVersion=1` and legacy fields.
- `transition()` — lifecycle writer; increments generation and persists through legacy `save_state()`.
- `initialize()` — writes the legacy default only when the controller is absent.
- `disable()` — lifecycle transition to `mode=passthrough`, desired gateway running, then restart/lifecycle side effects.
- `enable()` / `start_managed()` / `stop_managed()` — legacy lifecycle transition writers.

`host_v091.py` and `host_v091_legacy_v094.py` embed or call this legacy implementation. The installed plugin entry `v091-release-entry.ts` is also a legacy schema-1 reader: it requires `schemaVersion=1` and `mode` and does not write the controller.

### Installer

`scripts/install.ps1` directly reads the controller to derive an installer boundary mode (`Get-ExistingCnxMode`) and passes the Host root to `host_v091.py init`. The installer itself does not contain a direct JSON write of `controller.json`; its Host `init` delegation can invoke the legacy initialization path when the controller is absent. The installer also invokes plugin rollover ownership/recovery tools, but no direct controller writer was found in the inspected installer path.

### Recovery / ownership / service / supervisor

- `namespace_ownership.py` reads controller state for rollover ownership and does not write it in the inspected `controller.json` path.
- `reset_v095.py` and legacy lifecycle/recovery helpers can remove a root and invoke Host `init`, then use legacy lifecycle writers; they are mutation paths, not read-only observers.
- `lifecycle_v092.py` has legacy provider metadata writers (`seed_transition`, `commit_selection`) and lifecycle callers, but it does not itself establish the CNX-361-to-CNX-362 event.
- `host_control.py` reads legacy `mode` and writes audit/watchdog compatibility files, not `controller.json`; its delegated lifecycle commands can reach legacy Host transitions.
- The plugin runtime `v091-release-entry.ts` reads `controller.json` only.
- No separate service/supervisor direct writer of `host/controller.json` was established from repository source. Supervisor code can call lifecycle behavior, but no live process provenance was available.

## State-root and identity-chain evidence

The installer computes the expected Host authority root as:

```text
Workspace                         = %USERPROFILE%\.openclaw\workspace
stateRoot / CNX root              = <Workspace>\.cogentnexus-openclaw
controllerPath                    = <stateRoot>\host\controller.json
legacy compatibility root         = <Workspace>\.cogent
applicationData                  = %LOCALAPPDATA%\CogentNexus-OpenClaw
installed plugin root             = %USERPROFILE%\.openclaw\extensions\cogentnexus-openclaw
launcher                          = <Workspace>\cnxclaw.cmd
runtime authority                 = <targetSkill>\scripts\runtime_authority.py
```

CNX-361 proves the installed plugin root and candidate module identity, and records the controller values after activation, but its report does not preserve a separately hashed/absolute `controllerPath`, workspace, stateRoot, launcher, or application-data manifest bound to that controller read.

CNX-362 records the installed plugin root and module hash and the controller contents, but does not record the absolute controller path, workspace, stateRoot, launcher, runtime-authority identity, or application-data root used for that read. Therefore the evidence does not prove that CNX-361 and CNX-362 read the same controller file merely because both reports use the same filenames/concepts.

The repository also contains prior durable evidence of a fresh-install residue controller with `passthrough, generation 1` (CNX-20260826-072), but that is historical evidence of a possible stale state root, not proof that it is the file read by CNX-362.

## Timestamp and provenance evidence

Available durable timestamps are:

- CNX-362 controller `updatedAt`: `2026-08-29T01:36:31.541994+00:00`.
- CNX-361 activation/report and CNX-362 preflight were recorded on the September 15 coordination sequence.
- CNX-361 report records the accepted controller after activation as canonical schema 2, active, running, generation 103.
- No installer stage log, Gateway restart log, service/supervisor start record, file-system journal, controller backup/quarantine manifest, or process handle identifying a writer was included in the CNX-361/CNX-362 durable evidence.

The August 29 `updatedAt` predates the September 15 CNX-361 activation evidence. This is consistent with a stale/alternate state root or an old legacy controller being read later, but it does not by itself prove which.

## Offline replay evidence

No lifecycle or external command was run. An isolated temporary directory was used to call only the legacy state functions:

```text
legacy.initialize(root)
legacy.transition(root, mode="passthrough", desiredGateway="running", desiredProvider="unchanged")
```

The persisted result was schema 1 with legacy `mode=passthrough` and desired gateway running (generation 2 after the initialization transition). This proves that the legacy implementation can produce the observed schema family and fields. It does not prove that this path wrote the live CNX-362 file, nor does it reproduce generation 1 exactly.

Relevant canonical state tests passed:

```text
python -m pytest -q tests/test_host_state_v095.py tests/test_host_state_integration_v095.py tests/test_v095_upgrade_migration.py
21 passed in 0.20s
```

No RED test was created because a current source defect causing the live regression was not proven. No source repair was made.

## Single primary hypothesis

I think CNX-362 read a stale or alternate Host state root containing a legacy controller because the controller timestamp is from 2026-08-29, the exact controller path/state-root binding is absent from both live reports, and the repository has an older fresh-install residue with the same passthrough/generation-1 identity; however, this remains unproven because no durable path/provenance record binds that file to CNX-361 or identifies its writer.

The smallest offline test supports only the compatibility half of this hypothesis: the legacy Host implementation can write schema 1 / passthrough state. It does not establish the live root, write event, or process.

## Alternative classification result

- A installer overwrite: not proven; no direct installer controller writer found.
- B initialization reset: possible only through a missing/stale root or legacy Host delegation; not proven on the live root.
- C migration/compatibility legacy write: legacy compatibility code can write schema 1; live invocation not proven.
- D startup/enable/disable lifecycle: legacy `disable()` and related transitions can write passthrough; no authorized/live event evidence identifies one.
- E stale/alternate workspace or state root: primary hypothesis, not proven.
- F recovery/restore/quarantine copy: no matching durable copy provenance found.
- G another process/service writer: no process/service evidence available.
- H runtime read a different controller than CNX-361 activation wrote: possible and materially unresolved; exact path binding is missing.

## Required outcome and successor

`BLOCKED`: the actual write origin/time cannot be established from available evidence. Do not normalize the controller to active/generation 103. Do not claim runtime repaired.

No source repair is required or authorized from this evidence. A separate successor repair task is not yet justified; first obtain path-bound provenance or a controlled, separately authorized reproduction that identifies the writer. Semantic requalification must remain stopped until that boundary is explained.

## Dashboard boundary

Explicitly: no Dashboard request was sent by CNX-363. No Dashboard handoff was sent. No prompt, model request, provider-routing/auth change, reinstall, lifecycle mutation, hook-registration change, `main`/tag change, force-push, or history rewrite occurred.

This report makes no OpenAI PASS claim and no CURRENT_RED admission claim.
