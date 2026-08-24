# CNX-20260825-060 — Apply Approved Plugin Generation Rollover

Status: `READY_FOR_HERMES`

Execution mode: `MANUAL_WITH_HUMAN_GATE`

Current authorization: `PHASE_B_APPLY_AUTHORIZED`

Owner: ChatGPT

Executor: Hermes after the operator's manual continuation signal

## Goal

Apply exactly the accepted Task 059 CogentNexus-OpenClaw v0.9.3 plugin-generation rollover plan once, using the repository's accepted fail-closed `rollover-apply` primitive, then prove the installation has exactly one canonical v0.9.3 plugin payload and ownership now binds the active replacement generation while the controller remains PASSTHROUGH and startup remains disabled.

This task authorizes only the exact Phase B rollover mutation described below. It does not authorize returning CogentNexus-OpenClaw to MANAGED mode or changing lifecycle/startup/Gateway/Ollama state.

## Explicit operator authorization

At 2026-08-25 01:27 ICT, the operator explicitly approved:

`f81c60185b3e5ff5f7fd9ffdecda0760c53a5ce8d5aef1e7e2c84e8fd4fbf523`

with the instruction:

> อนุมัติ plan SHA-256 `f81c60185b3e5ff5f7fd9ffdecda0760c53a5ce8d5aef1e7e2c84e8fd4fbf523` ให้ดำเนิน Phase B ได้

This exact SHA-256 is the only apply authority for Task 060.

## Accepted predecessor checkpoint

Task 059 report commit:

`d832d5d9a0566f122817c32401d847739ba8ebb1`

Task 059 review decision:

`ACCEPT_ROLLOVER_PLAN_INPUT_BINDING_REPROVED`

Task 059 review commit:

`756a1f96164d95e82d694fd062878092f2ac74fe`

Accepted Task 059 plan path on the local machine:

`C:\Users\CDQ-P\AppData\Local\Temp\cnx059-rollover-plan-20260824T181054Z\task059-rollover-plan.json`

Accepted Task 059 plan SHA-256:

`f81c60185b3e5ff5f7fd9ffdecda0760c53a5ce8d5aef1e7e2c84e8fd4fbf523`

The rejected Task 058 plan SHA-256:

`360393b0ac8a9ffee0ad603e67efb23b48fe06a7f5e9719d0bc18d03ace76c2c`

is permanently ineligible and must not be read as apply authority, supplied to `rollover-apply`, or substituted for Task 059.

## Accepted plan bindings

Task 059 durably proved these exact values:

- normalized plugin inventory SHA-256: `f6305077bccb11f3572d4a42be2b48377161bb2b017e1d9d80f49b5f950083f5`;
- normalized active-registration SHA-256: `8cc399b12e2ab8fe0be352b8beea12fa093f19f97e07f62b6123c834ccda8c4d`;
- manifest-before SHA-256: `d299f290d508c783ae33124fcc7e582349bf9c7a73c47d07dd38207ebf2f4207`;
- Task 049 manifest SHA-256: `7525DAB74EE1801A26B4B1CF824CB22155E971BCB63697149580ED1B9F42BA3A`;
- retired payload fingerprint: `0e5746d063af1bf6d82e0901ce4e5f3def57a9ecb41ec2d4bdd70ffcd6599ddb`;
- replacement payload fingerprint: `0e5746d063af1bf6d82e0901ce4e5f3def57a9ecb41ec2d4bdd70ffcd6599ddb`;
- retired wrapper SHA-256: `26f2cec7d59b75e70912150a177e880a92c90b7301930c2a4b917d64f02053ef`;
- replacement wrapper SHA-256: `26f2cec7d59b75e70912150a177e880a92c90b7301930c2a4b917d64f02053ef`;
- retired wrapper-proof SHA-256: `b47da3bfd52abb5a01e3563a1a11ca3b445a0e9ddcfebe0dd4771725a1b0548c`;
- replacement wrapper-proof SHA-256: `892c59eb0f1f6df03e5f2a9a225d4c972b81aab1369375da57b45b564a4aea32`;
- retired project-tree SHA-256: `05981336d143a83b20d81803a29e66a849e845fe49064b8fd5c97cdecd3f94ee`;
- replacement project-tree SHA-256: `3621dbb46b6e6fadf5b0c0ecade860f1206640949804a26129612005202d1c7d`.

Exact retired plugin payload:

`C:\Users\CDQ-P\.openclaw\npm\projects\openclaw-plugin-cogentnexus-openclaw\node_modules\openclaw-plugin-cogentnexus-openclaw`

Exact retired npm project root:

`C:\Users\CDQ-P\.openclaw\npm\projects\openclaw-plugin-cogentnexus-openclaw`

Exact active replacement payload:

`C:\Users\CDQ-P\.openclaw\npm\projects\openclaw-plugin-cogentnexus-openclaw__openclaw-generation__g-bbc979095f8845a1\node_modules\openclaw-plugin-cogentnexus-openclaw`

Exact active replacement npm project root:

`C:\Users\CDQ-P\.openclaw\npm\projects\openclaw-plugin-cogentnexus-openclaw__openclaw-generation__g-bbc979095f8845a1`

Exact planned backup path:

`C:\Users\CDQ-P\AppData\Local\CogentNexus-OpenClaw\plugin-generation-rollover-backups\openclaw-plugin-cogentnexus-openclaw-20260824t181210832193z`

The accepted plan binds `manifestAfter.pluginPath` to the active replacement payload above.

## Required repository source

Use a new fresh isolated full clone of:

`funggier/CogentNexus-OpenClaw`

Branch:

`agent/v0.9.3-recovery-reality-tests`

Before any live inspection require:

- local HEAD equals remote coordination HEAD;
- fresh clone is clean;
- Task 055 accepted rollover implementation `6ad87e6f3ae65327a14bab4b5144dda4416d3645` is an ancestor;
- Task 057 accepted inventory-schema implementation `f379e5c5d8dddb144cb0d1991b645b16055e1303` is an ancestor;
- Task 059 report `d832d5d9a0566f122817c32401d847739ba8ebb1` is an ancestor;
- Task 059 accepted review `756a1f96164d95e82d694fd062878092f2ac74fe` is an ancestor;
- `ACTIVE.md`, `STATUS.md`, and this task all agree on `READY_FOR_HERMES` / `PHASE_B_APPLY_AUTHORIZED` and the exact approved SHA;
- no matching Task 060 report already exists.

Also require no source drift after the accepted Task 057 implementation in the two execution-critical files:

- `skills/cogentnexus-openclaw/scripts/namespace_ownership.py`;
- `scripts/invoke-root-process-exact.ps1`.

A documentation-only coordination descendant is allowed. Any change to either execution-critical file after `f379e5c5d8dddb144cb0d1991b645b16055e1303` blocks execution.

Never checkout, reset, clean, repair, commit from, or otherwise mutate the primary repository at:

`C:\Users\CDQ-P\.openclaw\workspace`

The only authorized changes under that workspace are the exact CogentNexus runtime-state changes performed internally by the reviewed `rollover-apply` primitive.

## Evidence boundary

Before any live inspection, create a new unique retained directory under:

`%LOCALAPPDATA%\Temp\cnx060-rollover-apply-<UTC-token>`

Retain at minimum:

- fetched repository HEAD and clean status;
- UTC transcript with exact commands and numeric exit codes;
- redacted preflight JSON/text;
- exact Task 059 plan path, byte size, and freshly recomputed SHA-256;
- one fresh pre-apply OpenClaw plugin inventory raw JSON file;
- its byte size and raw SHA-256;
- normalized pre-apply inventory and active-registration SHA-256 values;
- pre-apply exact product-root inventory and hashes;
- pre-apply unrelated plugin identity snapshot;
- root-process self-test output;
- apply stdout, stderr, and numeric poststate from `invoke-root-process-exact.ps1`;
- bounded post-apply verification JSON/text;
- at most one post-apply OpenClaw plugin inventory raw JSON file;
- report draft and publication verification.

Do not write secrets, tokens, API keys, full OpenClaw config, environment dumps, unrelated user files, or model contents into evidence.

Do not modify, overwrite, rename, normalize, regenerate, or delete the retained Task 059 plan.

## Duplicate and concurrency fence

Before the apply preflight prove zero concurrent:

- Task 060 executor;
- `rollover-apply` process;
- installer / plugin install / plugin uninstall;
- `cnxclaw` enable/disable/start/stop/restart/reset/uninstall;
- CogentNexus supervisor/lifecycle mutation;
- report publisher for Task 060;
- Procmon Task 027/038 capture;
- process acting on the retired or replacement npm project roots.

If concurrency cannot be bounded safely, stop as `BLOCKED_LIVE_STATE_DRIFT` with no apply invocation.

## Phase B1 — immutable approved-plan gate

The retained Task 059 plan must exist at exactly:

`C:\Users\CDQ-P\AppData\Local\Temp\cnx059-rollover-plan-20260824T181054Z\task059-rollover-plan.json`

Freshly compute its byte size and SHA-256. Require exact SHA-256:

`f81c60185b3e5ff5f7fd9ffdecda0760c53a5ce8d5aef1e7e2c84e8fd4fbf523`

Parse it read-only and require all exact identity/boundary fields from Task 059, including the exact retired/replacement roots, backup path, fingerprints, wrapper proofs, tree hashes, normalized inventory hash, active-registration hash, manifest-before hash, PASSTHROUGH controller mode, and replacement `manifestAfter.pluginPath`.

Require the exact planned backup path still does not exist.

If the plan is missing, unreadable, changed, substituted, or its backup destination already exists, stop as:

`BLOCKED_APPROVED_PLAN_UNAVAILABLE_OR_DRIFTED`

Do not regenerate a plan and do not substitute any other plan path or SHA.

## Phase B2 — fresh live preservation preflight

Before capturing apply-time inventory, freshly prove read-only:

- `cnxclaw.cmd --json status` reports mode exactly `passthrough`;
- generation remains `7` before apply;
- desired Gateway remains `running`;
- desired provider remains `unchanged` and selected provider remains `ollama`;
- startup remains `disabled`;
- CogentNexus adapter/supervisor remains absent;
- `openclaw gateway status --json` is healthy/reachable;
- `ollama list` contains the same four model identities proven by Task 059: `qwen3.5:9b`, `muse-glimmer:30b`, `qwen3.6:27b`, `qwen3.8:27b`;
- SQLite read-only integrity is `ok` and ticket/event/outbox/session counts remain `0`;
- ownership manifest SHA-256 is exactly `D299F290D508C783AE33124FCC7E582349BF9C7A73C47D07DD38207EBF2F4207`;
- controller SHA-256 remains `164F7FAC6081CA22AA6AD5391FB60E2EA57F26CF4A874CC4D19D50E02961EE7E`;
- registered policy SHA-256 remains `14EDEAD0180690C3D9565E864D2BDAAAE60E32DF9EF2C64EBD2A1238DF5CD8B4`;
- AGENTS baseline SHA-256 remains `C9A664B73200AE5D6B0DA0908DE3256CDB4DDA8BA6FE99F5E6C5115C3983604C`;
- launcher SHA-256 remains `8DB1F256BB56C298FFFB14E8A761CAA7DBEC56EA334B0F4558C3CDA563AA46EF`;
- startup policy SHA-256 remains `CDF092FE1D076F0727B10BCE7789D44DC0BD05768CE9F2F825C9E072F0E6B7BE`;
- Task 049 manifest SHA-256 remains `7525DAB74EE1801A26B4B1CF824CB22155E971BCB63697149580ED1B9F42BA3A`;
- exactly two canonical v0.9.3 product payload roots exist and they are the exact accepted retired/replacement roots;
- no third product-owned payload root exists;
- retired and replacement complete tree hashes still equal the accepted Task 059 values;
- replacement remains the active OpenClaw registration and remains disabled.

Capture a bounded pre-apply snapshot of unrelated plugin IDs/rootDirs/status values so Task 060 can prove they remain untouched after apply.

Any contradiction stops as `BLOCKED_LIVE_STATE_DRIFT` before `rollover-apply`.

## Phase B3 — one fresh apply-time OpenClaw inventory

Invoke exactly once before apply:

```powershell
openclaw plugins list --json
```

Redirect stdout to one uniquely named Task 060 pre-apply raw inventory file in the evidence directory.

Immediately record its exact byte size and raw SHA-256.

Parse that exact file without rewriting it. Using the accepted Task 057 code semantics, require:

- exactly one `cogentnexus-openclaw` active registration;
- version exactly `0.9.3`;
- rootDir exactly the accepted replacement payload;
- enabled `false` and status `disabled`;
- if `packageName` is present it equals `openclaw-plugin-cogentnexus-openclaw`;
- if `packageName` is absent, payload package identity is exact and normalized evidence is `payload-package-json`;
- normalized inventory SHA-256 exactly `f6305077bccb11f3572d4a42be2b48377161bb2b017e1d9d80f49b5f950083f5`;
- normalized active-registration SHA-256 exactly `8cc399b12e2ab8fe0be352b8beea12fa093f19f97e07f62b6123c834ccda8c4d`.

The raw byte hash may differ from Task 059 because OpenClaw JSON object key ordering is not the apply binding. The parsed normalized hashes above are the authoritative apply-time drift gates.

If either normalized hash differs, stop as:

`BLOCKED_APPLY_INPUT_INVENTORY_DRIFT`

Do not recapture and do not invoke apply.

## Phase B4 — root-process exit-code proof

Before the destructive invocation, run the accepted wrapper self-test from the fresh isolated clone:

```powershell
& <isolated-clone>\scripts\invoke-root-process-exact.ps1 -SelfTest
```

Require success proving numeric exit codes `0` and `7`, null rejection, and argument round-trip behavior.

Failure stops as `BLOCKED_LIVE_STATE_DRIFT`; do not bypass the wrapper and do not invoke apply directly.

## Phase B5 — execute the exact approved apply once

Invoke `rollover-apply` exactly **one** time through `scripts/invoke-root-process-exact.ps1` so stdout, stderr, and an observed numeric exit code are retained.

The child command must be semantically exactly:

```text
python <isolated-clone>\skills\cogentnexus-openclaw\scripts\namespace_ownership.py rollover-apply --plan "C:\Users\CDQ-P\AppData\Local\Temp\cnx059-rollover-plan-20260824T181054Z\task059-rollover-plan.json" --plan-sha256 "f81c60185b3e5ff5f7fd9ffdecda0760c53a5ce8d5aef1e7e2c84e8fd4fbf523" --inventory-json <task060-fresh-preapply-inventory.raw.json>
```

No other plan path, SHA, inventory file, helper copy, or command variant is authorized.

Do not invoke `rollover-plan` in Task 060.

Do not invoke `rollover-apply` a second time under any outcome.

The reviewed primitive itself must re-prove, before its first live mutation:

- exact plan SHA;
- exact plan schema/product/version/PASSTHROUGH mode;
- application-data and backup boundaries;
- backup destination nonexistent;
- exact manifest-before SHA;
- exact fresh normalized inventory SHA;
- exact active registration;
- exact retired/replacement roots, payload fingerprints, wrapper proofs and project-tree hashes;
- same-volume atomic rename feasibility.

The only authorized mutation effects are those internal to this one reviewed apply invocation:

1. creation of the exact product rollover-backup parent if needed;
2. atomic `os.replace` of the exact retired npm project root to the exact reviewed backup path;
3. atomic write/replace of `ownership.json` to the exact `manifestAfter` embedded in the accepted plan.

No manual move/delete/copy/manifest edit is authorized before, during, or after the invocation.

### Apply result handling

If the wrapper reports numeric exit code `0`, require child stdout to report:

- `status: ROLLOVER_APPLIED_PASSTHROUGH`;
- plan SHA-256 exactly `f81c60185b3e5ff5f7fd9ffdecda0760c53a5ce8d5aef1e7e2c84e8fd4fbf523`;
- backupPath exactly the accepted planned backup path;
- pluginPath exactly the accepted replacement payload.

Then continue only to read-only post-apply verification.

If the apply exits nonzero **before mutation** because a reviewed binding changed, classify as `BLOCKED_APPROVED_PLAN_UNAVAILABLE_OR_DRIFTED` or `BLOCKED_APPLY_INPUT_INVENTORY_DRIFT` as appropriate and stop. No retry.

If stderr reports `plugin rollover failed; rollback complete`, perform only bounded read-only proof that the retired project and manifest were restored to the pre-apply state, then return:

`BLOCKED_ROLLOVER_APPLY_ROLLED_BACK`

If stderr reports `plugin rollover failed and rollback is incomplete`, immediately stop all mutation and return:

`BLOCKED_ROLLOVER_APPLY_ROLLBACK_INCOMPLETE`

Capture the exact remaining paths/hashes read-only for ChatGPT. Do not manually repair, move, delete, rewrite, reinstall, or retry.

Any other nonzero outcome is a blocker. Preserve stdout/stderr/poststate and stop without improvisation.

## Phase B6 — mandatory read-only post-apply proof

After a successful apply, prove all of the following before declaring success:

### Ownership and generation

- exact retired npm project root no longer exists;
- exact planned backup path exists as a directory;
- backup complete project-tree SHA-256 equals `05981336d143a83b20d81803a29e66a849e845fe49064b8fd5c97cdecd3f94ee`;
- exact replacement npm project remains present;
- replacement complete project-tree SHA-256 remains `3621dbb46b6e6fadf5b0c0ecade860f1206640949804a26129612005202d1c7d`;
- ownership manifest parses exactly and equals the plan's `manifestAfter` object;
- ownership manifest `pluginPath` is the exact replacement payload;
- `namespace_ownership.py verify --root "C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw" --workspace "C:\Users\CDQ-P\.openclaw\workspace"` exits `0`;
- `namespace_ownership.py resolve-plugin --openclaw-state "C:\Users\CDQ-P\.openclaw" --version 0.9.3` exits `0` and resolves exactly the replacement payload/fingerprint;
- exactly one canonical v0.9.3 product payload candidate remains under OpenClaw state;
- no third or foreign product-owned candidate exists.

Record the new ownership-manifest SHA-256; it is expected to differ from the pre-apply hash because the accepted plan changes `pluginPath` and `installedAt`.

### Runtime preservation

Fresh read-only checks must prove:

- controller remains exactly `passthrough`;
- startup remains `disabled`;
- no CogentNexus supervisor/adapter was created;
- Gateway remains healthy/reachable;
- Ollama remains healthy with the same four model identities;
- SQLite integrity remains `ok` and ticket/event/outbox/session counts remain `0`;
- controller, registered policy, AGENTS baseline, launcher, startup policy, and Task 049 manifest hashes remain byte-identical to their pre-apply values.

### OpenClaw registration preservation

At most once after successful apply, capture:

```powershell
openclaw plugins list --json
```

into a distinct post-apply raw inventory file.

Require:

- exactly one canonical `cogentnexus-openclaw` registration;
- version `0.9.3`;
- rootDir remains the accepted replacement payload;
- enabled `false`, status `disabled`;
- package identity remains exact;
- the 71 unrelated plugin identities/rootDirs/status values match the bounded pre-apply snapshot.

Do not use a post-apply inventory capture as input to another apply.

If the apply returned success but any mandatory postcondition is unproven or contradicted, stop as:

`BLOCKED_POSTAPPLY_VERIFICATION`

Do not perform manual repair or a second apply. Preserve the live state and evidence for ChatGPT review.

## Phase B7 — report-only publication and mandatory stop

Publish only:

`docs/operations/coordination/reports/CNX-20260825-060-apply-approved-plugin-generation-rollover.md`

For a fully verified successful apply:

Status: `PASS`

Result:

`PASS_PLUGIN_GENERATION_ROLLOVER_APPLIED_PASSTHROUGH`

The report must include at minimum:

- fetched execution HEAD;
- exact operator-approved SHA;
- Task 059 accepted review commit `756a1f96164d95e82d694fd062878092f2ac74fe`;
- Task 059 plan path, byte size, and fresh SHA-256;
- pre-apply inventory raw path/size/SHA and normalized inventory/registration SHAs;
- exact root-process self-test result;
- `rollover-apply` invocation count = `1`;
- exact wrapper stdout/stderr/poststate paths and hashes;
- observed numeric child exit code;
- exact apply stdout result;
- before/after retired, replacement, backup and manifest paths/hashes;
- post-apply `verify` and `resolve-plugin` results;
- pre/post controller/startup/Gateway/Ollama/SQLite/preservation evidence;
- unrelated plugin preservation result;
- all live mutations actually observed;
- explicit statement that controller remains PASSTHROUGH and startup remains disabled;
- remaining uncertainty;
- exactly one result token.

For a blocker, publish the matching blocker token and the precise last proven state, including whether the reviewed primitive reported rollback complete or incomplete.

The report commit must add only the matching Task 060 report path relative to the fetched execution HEAD. Fetch and remote-verify the report commit and blob, then stop.

Hermes must not edit `ACTIVE.md`, `STATUS.md`, task files, review files, source code, tests, installer files, or any other repository path.

## Result tokens

Return exactly one:

- `PASS_PLUGIN_GENERATION_ROLLOVER_APPLIED_PASSTHROUGH`
- `BLOCKED_APPROVED_PLAN_UNAVAILABLE_OR_DRIFTED`
- `BLOCKED_LIVE_STATE_DRIFT`
- `BLOCKED_APPLY_INPUT_INVENTORY_DRIFT`
- `BLOCKED_ROLLOVER_APPLY_ROLLED_BACK`
- `BLOCKED_ROLLOVER_APPLY_ROLLBACK_INCOMPLETE`
- `BLOCKED_POSTAPPLY_VERIFICATION`
- `BLOCKED_EVIDENCE_PUBLICATION_UNSAFE`

## Hard fence

Task 060 authorizes no operation except the exact one-time reviewed `rollover-apply` and its required read-only proofs/report publication.

Specifically prohibited:

- `rollover-plan` regeneration;
- reuse of Task 058 plan/inventory/SHA;
- a second `rollover-apply` invocation;
- manual plugin-project move/copy/delete;
- manual ownership-manifest edit;
- OpenClaw plugin install/uninstall/enable/disable/link/unlink;
- CogentNexus installer, reset, uninstall, enable, disable, start, stop, restart;
- controller transition to MANAGED or MAINTENANCE;
- startup/supervisor/scheduler creation or change;
- Gateway start/stop/restart/config mutation;
- Ollama start/stop/restart/model pull/remove/config mutation;
- process termination or force-kill;
- primary Git repository checkout/reset/clean/source edit;
- Procmon/Task 027/038 action;
- mutation of the separate HermesAgent project/system;
- Ecosystem or staged-capability-loop work;
- merge, tag, release, archive publication, or broad cleanup.

A successful Task 060 must stop in `ROLLOVER_APPLIED_PASSTHROUGH`. Returning the controller to MANAGED, enabling startup/supervisor behavior, or performing install-over acceptance belongs to a separately reviewed successor task after ChatGPT accepts Task 060 evidence.

## Progress communication

Report meaningful progress approximately every 3 minutes and immediately after:

- duplicate/concurrency preflight;
- approved-plan hash gate;
- live preservation preflight;
- fresh apply-time inventory binding;
- root-process self-test;
- immediately before the authorized apply;
- immediately after the apply exits;
- post-apply ownership/runtime verification;
- report publication or any blocker.

Progress updates are not permission prompts. Once Hermes receives the operator's manual continuation signal, continue through the exact authorized Task 060 unless a stated stop gate fires.
