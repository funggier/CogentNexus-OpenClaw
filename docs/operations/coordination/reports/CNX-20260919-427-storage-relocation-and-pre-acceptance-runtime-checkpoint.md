# CNX-20260919-427 — Storage Relocation and Pre-Acceptance Runtime Checkpoint

Status: `STORAGE_RELOCATION_GREEN__WAITING_FOR_FINAL_DISCORD_ACCEPTANCE`

Date: 2026-09-19

Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`

Repository HEAD at checkpoint start:

`a84134d3229f51797ad8270520d506279734640c`

Active task:

`CNX-20260919-427 — External Ingress Run Identity and Tailscale Owner Profile Repair`

## Summary

The operator-requested C: -> T: CogentNexus backup relocation is complete and fidelity-verified. The original C: backup paths are preserved as NTFS junctions. Old rollback/report paths continue to resolve. The old duplicate data on C: was removed only after mirror, hash, reparse, and old-path verification.

The live OpenClaw 2026.9.5 runtime remained healthy throughout the relocation. CNX-427 is not final PASS yet because one new operator-originated Discord semantic turn is still required.

## Repository authority check

Before mutation:

- local branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`;
- local HEAD: `a84134d3229f51797ad8270520d506279734640c`;
- remote HEAD: `a84134d3229f51797ad8270520d506279734640c`;
- worktree clean.

## Backup relocation destination

Canonical T: destination:

`T:\CogentNexus\CogentNexus-OpenClaw`

Relocated trees:

- `backups`
- `plugin-generation-rollover-backups`

### Main backups mirror

Source:

`C:\Users\CDQ-P\AppData\Local\CogentNexus-OpenClaw\backups`

Destination:

`T:\CogentNexus\CogentNexus-OpenClaw\backups`

Initial completed copy summary:

- directories total: 40,670;
- files total: 509,383;
- bytes total: 9.479 GiB;
- files copied in the continuation pass: 419,217;
- bytes copied in the continuation pass: 8.077 GiB;
- mismatch: 0;
- failed: 0;
- extras: 0.

Post-copy dry mirror with `/MIR /L /COPY:DAT /DCOPY:DAT /SL /SJ`:

- copied: 0;
- mismatch: 0;
- failed: 0;
- extras: 0;
- all 509,383 files / 9.479 GiB skipped as identical.

### Plugin-generation rollover backup mirror

Source:

`C:\Users\CDQ-P\AppData\Local\CogentNexus-OpenClaw\plugin-generation-rollover-backups`

Destination:

`T:\CogentNexus\CogentNexus-OpenClaw\plugin-generation-rollover-backups`

Verified dry mirror:

- directories total: 9,956;
- files total: 159,271;
- bytes total: 1.408 GiB;
- copied: 0;
- mismatch: 0;
- failed: 0;
- extras: 0.

The destination exposes the four expected rollover generations.

## Fidelity evidence

Authoritative rollback snapshot:

`CNX-20260919-427-preupgrade95-20260919T172713`

Manifest SHA256 matched source -> target:

`9AEA5DE8B91DC38A97D707F2A969164A9C300B7F9073AA8BCAE3103FDDCE10FA`

The following source/target hashes were explicitly rechecked and matched:

- `openclaw.json`
- `gateway.cmd`
- `gateway.vbs`
- `state\openclaw.sqlite`
- `agents\main\agent\openclaw-agent.sqlite`
- `workspace\.cogentnexus-openclaw\runtime\cogentnexus-openclaw.sqlite3`
- `extensions\cogentnexus-openclaw\dist\index.js`

The authoritative snapshot's `openclaw-home-fidelity` reparse count matched:

- C: source: 10;
- T: destination: 10.

## Junction cutover

After fidelity verification, the original C: locations were renamed temporarily and replaced with NTFS junctions.

Current mappings:

`C:\Users\CDQ-P\AppData\Local\CogentNexus-OpenClaw\backups`

->

`T:\CogentNexus\CogentNexus-OpenClaw\backups`

and:

`C:\Users\CDQ-P\AppData\Local\CogentNexus-OpenClaw\plugin-generation-rollover-backups`

->

`T:\CogentNexus\CogentNexus-OpenClaw\plugin-generation-rollover-backups`

Both current C: paths report `LinkType=Junction`.

Old-path compatibility checks passed:

- authoritative manifest resolves through the old C: path;
- `ROLLBACK-README.txt` resolves through the old C: path;
- manifest hash through the old path equals the T: target hash.

## Reparse-safe source cleanup

The renamed main backup source still contained 20 reparse points. Those points were removed as links without traversing their targets before deleting regular backup content.

Evidence:

- reparse points before cleanup: 20;
- reparse points removed: 20;
- reparse points remaining: 0.

The renamed sources were then emptied with an empty-source robocopy mirror. Cleanup summaries:

Main backup source:

- deleted extras: 509,383 files / 9.479 GiB;
- failed: 0.

Rollover source:

- deleted extras: 159,271 files / 1.408 GiB;
- failed: 0.

Both temporary source roots were removed after becoming empty.

## Space recovery

Before relocation verification:

- C: free: ~13.43 GiB;
- T: free: ~641.19 GiB.

After completed relocation and cleanup:

- C: used: ~439.66 GiB;
- C: free: ~25.48 GiB;
- T: used: ~301.52 GiB;
- T: free: ~629.99 GiB.

C: free-space recovery is approximately 12.05 GiB.

## Post-relocation live runtime qualification

OpenClaw:

`OpenClaw 2026.9.5 (ec9c1a1)`

Gateway:

- health `ok=true`;
- event loop `degraded=false`;
- plugin errors: 0;
- listener: `127.0.0.1:18789`;
- PID: `29604`.

Discord:

- enabled: true;
- lifecycle: `ready`;
- running: true;
- connected: true;
- active runs: 0;
- last error: null.

CNX runtime attestation:

- `runnerReady=true`;
- `globalHookCount=7`;
- `classification=AMBIGUOUS` because the public SDK does not identify plugin ownership of the current global handlers.

Live CNX `dist/index.js` SHA256 remains:

`6D96AD5FC4F419105E7E6A82EC941926886A05937C143E599C47FE9143A8FBE3`

Supervisor:

- task state: Ready;
- LastTaskResult: 0.

Tailscale Serve:

`https://cdq-p.tail145b6c.ts.net:443/ -> http://127.0.0.1:12651`

Remote HTTPS probe:

- HTTP 200;
- content type `text/html; charset=utf-8`.

Memory/commit:

- free physical: ~9.63 GiB;
- free virtual/commit: ~20.57 GiB;
- pagefile used: ~2,117 MiB.

Ollama:

- `ollama ps` empty;
- qwen3.8:27b is not resident;
- no pre-acceptance memory-pressure blocker is present.

## Remaining gate

Storage and runtime maintenance gates are now satisfied.

CNX-427 still requires exactly one new operator-originated Discord turn on live OpenClaw 2026.9.5.

Required same-turn evidence:

1. authoritative OpenClaw runId;
2. exactly one CNX Ticket for that runId;
3. Ticket creation before inference authority;
4. exactly one model execution;
5. exactly one Discord delivery;
6. Ticket terminal completed/delivered state;
7. no stale lane;
8. no duplicate Ticket.

Until that proof is collected, final CNX-427 classification remains pending.
