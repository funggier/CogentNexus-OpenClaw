# Review — CNX-20260824-049 Back Up and Remove Proven Legacy, Stop at Fresh

Decision: **ACCEPT**

Disposition: `ACCEPT_FRESH_WITH_EXPECTED_PREHOST_AGENTS_RESTORE`

Reviewed task: `CNX-20260824-049`

Reviewed start HEAD: `aa25dfa63a1e561676e25208cdf255acb205de9b`

Reviewed report commit: `6512a7c2c96ff7e6c67d75a4d1b06eabbbac2b67`

Reviewed report:

[`../reports/CNX-20260824-049-backup-remove-legacy-stop-at-fresh.md`](../reports/CNX-20260824-049-backup-remove-legacy-stop-at-fresh.md)

## Publication fence

The compare from the fetched Task 049 start HEAD to the report commit contains exactly one commit and exactly one changed path: the Task 049 report. The report publication fence passes.

## Accepted result

Task 049 achieved the authorized operational goal:

- a verified, access-restricted external legacy-removal backup exists;
- the legacy controller was handed off to PASSTHROUGH/native OpenClaw;
- the exact legacy plugin and exact legacy launcher/skill/state ownership were removed;
- the current classifier returns exact `mode=fresh`;
- no current CogentNexus-OpenClaw installer or equivalent installation path ran;
- OpenClaw/Gateway, Ollama, the four-model inventory, unrelated plugins, user data, and excluded projects were preserved;
- the final system is stopped at the required pre-install boundary.

The report result token `BLOCKED_FINAL_PRESERVATION` is accepted as a task-specification conflict, not a failed removal or damaged file.

## AGENTS.md adjudication

The final workspace `AGENTS.md` is accepted as the correct fresh-state baseline:

- size: `7,196` bytes;
- SHA-256: `C9A664B73200AE5D6B0DA0908DE3256CDB4DDA8BA6FE99F5E6C5115C3983604C`;
- it exactly matches the legacy pre-host backup `.cogent\install-backups\AGENTS.pre-host-change-20260822T101418Z.md`;
- the operator-provided copy independently has the same size and SHA-256 and contains no legacy CogentNexus managed-block marker.

Legacy source behavior confirms this result is intentional. In `skills/cogentnexus/scripts/host.py` at source commit `874dd8f8ce9c1ca5595b29207281430a86c074de`, `disable()` invokes `remove_policy(workspace)`; `remove_policy_text()` removes only the text between the legacy `<!-- cogentnexus:begin -->` and `<!-- cogentnexus:end -->` markers. `docs/BASELINE.md` likewise specifies that `cnx disable` removes the active managed workspace policy block and that disable removes only the active `AGENTS.md` block.

Therefore the pre-task hash `C9BFD028...` represented the still-managed legacy state. Preserving that hash after disable would have contradicted the intended PASSTHROUGH/fresh transition. No restoration or modification of `AGENTS.md` is authorized or required.

The operator accepted this interpretation with: `ผมว่าน่าจะปกติครับ`.

## Safety and next gate

Retain the external backup unchanged:

`C:\Users\CDQ-P\AppData\Local\CogentNexus-OpenClaw-Legacy-Removal-Backups\20260824T105507Z`

No Task 049 action may be repeated. No legacy restore is required.

The machine is accepted at the fresh, pre-install boundary. Installing the current CogentNexus-OpenClaw requires a new successor task and new explicit operator authorization. Until then, do not run `scripts/install.ps1`, `clean-reinstall.ps1`, a Release installer, or any equivalent installation path.
