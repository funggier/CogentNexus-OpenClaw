# Independent Review — CNX-20260828-120 v0.9.3 Real-Windows Lifecycle Acceptance — Provider-Neutral Candidate

## Verdict

`ACCEPTED BLOCKED — HARD FENCE WORKED; BLOCK WAS CAUSED BY AN INCOMPLETE ACCEPTANCE-CLASSIFIER INVOCATION, NOT BY A PROVEN LIVE OWNERSHIP FAILURE`

Task 120 stopped correctly before any destructive phase. The fresh machine remained coherent and no install-over/reset/uninstall/reinstall/lifecycle/recovery action ran.

The blocking classifier result must not be treated as proof that the installed payload is corrupt. The acceptance task invoked `classify-install` with only `--workspace` and `--app-data`, but the current ownership classifier has an attested interrupted-rollover/re-entry path that requires both the current OpenClaw plugin inventory and the expected candidate plugin fingerprint.

## Accepted Task-120 evidence

Task-120 report:

`docs/operations/coordination/reports/CNX-20260828-120-v093-real-windows-lifecycle-acceptance-provider-neutral-candidate.md`

Accepted live facts:

- exact candidate/artifact provenance passed;
- Windows 10 Pro build `19045`;
- PowerShell `5.1.19041.6456`;
- OpenClaw exactly `2026.7.1-2 (0790d9f)`;
- CNX remained `passthrough`, generation `25`;
- Gateway healthy on loopback `127.0.0.1:18789`;
- current runtime/provider health remained READY;
- CNX system readiness reported READY and read-only;
- no destructive phase ran;
- no manual cleanup/normalization occurred;
- no Dashboard semantic Send occurred.

The fail-stop rule therefore worked as intended.

## Root cause of the Task-120 block

Task 120 instructed the executor to run the pinned classifier in this simplified shape:

```powershell
python .\skills\cogentnexus-openclaw\scripts\namespace_ownership.py classify-install --workspace "$HOME\.openclaw\workspace" --app-data "$env:LOCALAPPDATA\CogentNexus-OpenClaw"
```

That invocation omits two attestation inputs supported by the exact candidate:

- `--plugin-inventory-json`;
- `--expected-replacement-fingerprint`.

The classifier's interrupted-rollover/re-entry contract uses those inputs to prove that a replacement plugin generation is the currently registered candidate while the manifest may still point at a retired generation. Without them, execution can fall through to strict manifest/plugin exact-path verification and reject a state that requires the attested re-entry path.

The observed failure:

```text
RuntimeError: ownership manifest pluginPath does not match verified installed payload:
C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw
```

therefore proves only that the strict manifest path and the currently resolved plugin root differ. It does not prove payload corruption or unsafe ownership by itself.

## Production installer contract proves the missing acceptance inputs

The exact candidate `scripts/install.ps1` prepares classification by:

1. running candidate `npm ci` in the isolated candidate plugin directory;
2. running `npm run plugin:validate`;
3. calculating the candidate plugin fingerprint with `plugin-fingerprint`;
4. capturing `openclaw plugins list --json` into a temporary inventory file;
5. calling `classify-install` with both `--plugin-inventory-json` and `--expected-replacement-fingerprint` when the candidate plugin fingerprint is available.

This is the production-equivalent read-only ownership attestation boundary and must be mirrored by the acceptance preflight when testing an interrupted re-entry state.

## Classification of the defect

This is an **acceptance coordination/harness defect** in Task 120, not a demonstrated production-source defect.

No source repair is justified from this evidence. The exact candidate remains eligible for a successor live acceptance task because:

- Task 120 performed zero destructive mutations;
- the exact candidate/artifact identity remains unchanged;
- the missing inputs are already part of the candidate's supported classifier API and production installer behavior;
- the successor can reproduce the full attested classifier contract read-only before authorizing any mutation.

## Required successor

Open a new explicit live acceptance task using the same exact candidate/artifact.

Before any mutation, the successor must freshly:

1. verify exact artifact/source identity again;
2. capture current machine/OpenClaw/CNX/Gateway/SQLite/runtime state;
3. prepare the candidate plugin only inside the verified extracted candidate boundary (`npm ci`, `plugin:validate`);
4. compute the candidate plugin fingerprint with the exact candidate `namespace_ownership.py plugin-fingerprint` command;
5. capture the current `openclaw plugins list --json` inventory without mutation;
6. run `classify-install` with `--plugin-inventory-json` and `--expected-replacement-fingerprint`;
7. require the returned classification to be coherent with the fresh inventory/manifest/filesystem evidence.

Only if that attested read-only gate passes may the successor start install-over and the remaining one-shot lifecycle sequence.

Do not manually edit the manifest, move plugin roots, clean residue, or normalize state to make classification pass.

## Live boundary

Task 120 performed zero destructive phases. Therefore Task 120 did not consume any install-over/reset/uninstall/reinstall/stop/start/restart/recovery one-shot attempt.

A successor may authorize those phases once each under a new task, but must not replay or reinterpret the Task-120 simplified classifier result as a destructive-phase attempt.

No Dashboard semantic Send is authorized by this review.
