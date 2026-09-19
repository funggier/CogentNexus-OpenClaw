# CNX-20260920-435 — Temp Storage Recovery Report

Classification: `CNX_OPENCLAW_TEMP_STORAGE_RECOVERY_GREEN`

The C: storage incident was traced primarily to stale CNX/OpenClaw-generated Temp trees accumulated during repeated build, validation, model-catalog, qualification, clone, and installer activity.

## Outcome

- junction-safe full Temp scan: `109.576 GiB`, `3,403,807` files;
- CNX/OpenClaw-authorized cleanup set: `73.275 GiB`, `3,039,244` files, `1,408` top-level entries;
- deletion result: `1,408 success / 0 failed / 0 skipped`;
- C: free before: `18,948,087,808 bytes`;
- C: free after: `103,925,612,544 bytes`;
- `Temp\cnx*` after cleanup: `0`;
- `Temp\openclaw-*` after cleanup: `0`.

Unrelated Temp content, including the `random-dot` group, was deliberately preserved.

## Evidence on T:

- `diagnostics/TEMP-SPACE-20260920/temp-top-level-scan.json`
- `diagnostics/TEMP-SPACE-20260920/cnx-openclaw-cleanup-inventory.json`
- `diagnostics/TEMP-SPACE-20260920/cnx-openclaw-cleanup-report.json`

## Ongoing local policy

For the active LConnect process, `TEMP` and `TMP` are redirected to:

`T:\CogentNexus\CogentNexus-OpenClaw\temp\lconnect`

This prevents further LConnect-launched CNX/OpenClaw temporary work from consuming C: during the current tool session without changing system-wide Windows Temp configuration.
