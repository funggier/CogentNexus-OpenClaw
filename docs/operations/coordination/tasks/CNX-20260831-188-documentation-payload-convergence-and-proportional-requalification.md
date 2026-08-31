# CNX-20260831-188 — Documentation Payload Convergence and Proportional Requalification

Status: `READY_CHATGPT`

Repository: `funggier/CogentNexus-OpenClaw`

Branch: `agent/v0.9.3-full-stabilization`

Pre-task authority HEAD: `fa3c89d93b506f2e7ccfb167cc665e593ebf1373`

Frozen previously accepted implementation candidate: `f6392da3e4112ce441526d5ef19925c90a872b0b`

## Goal

Make all current v0.9.3 documentation/instruction surfaces truthful and current, freeze the resulting documentation-only artifact as a new candidate, prove that executable/runtime behavior bytes remain unchanged, proportionally requalify the corrected artifact, and then return directly to the authorized v0.9.3 publication path.

## User authorization

The user has explicitly clarified that documentation should be corrected to the current state first and then v0.9.3 should be released. Routine continuation through repository validation, proportional requalification, PR/merge, exact-SHA Release workflow, tag, assets and checksum verification is authorized when gates pass.

## Allowed repository changes

Documentation/instruction-only changes required for current-state convergence, including:

- `plugins/cogentnexus-openclaw/README.md`;
- `skills/cogentnexus-openclaw/SKILL.md`;
- stale installed references such as `skills/cogentnexus-openclaw/references/architecture.md`;
- safe root/docs/coordination/release notes needed to describe the corrected candidate and publication state.

Additional installed documentation may be corrected only when audit proves it contains stale current-facing guidance.

## Forbidden changes

Do not change under this task merely to make release pass:

- production/runtime/plugin executable source;
- tests;
- dependency versions/behavior;
- workflow behavior;
- provider/runtime semantics;
- durable schema or lifecycle semantics.

If such a change becomes necessary, block publication and report a product defect.

No force push.

## Repository candidate gates

1. Freshly re-read remote HEAD before every mutation batch.
2. Audit the full current plugin README + installed skill/reference documentation surface for stale version/status claims.
3. Apply the minimal documentation-only corrections.
4. Compare the corrected candidate against `f6392da3...` and prove all non-documentation executable/runtime/test/dependency/workflow bytes intended to remain stable are unchanged.
5. Explicitly prove `skills/cogentnexus-openclaw/scripts/cnxclaw.py` remains the accepted facade bytes (`aa747f8f30080ef839a8d2cbf5758f9981a007ca01f41a988576f42edea8682f`) unless a separately authorized product task intervenes.
6. Compute/freeze the new package payload-v2 identity and an exact installed skill-tree identity/hash manifest.
7. Run exact-candidate primary CI/package validation. All required jobs must pass.
8. Create a durable checkpoint before Windows mutation.

## Proportional Windows requalification

Because the implementation has already passed the full v0.9.3 stabilization lifecycle sequence and this candidate changes documentation/instruction bytes only, the default requalification is intentionally bounded:

1. fresh read-only live baseline/provenance/health;
2. exactly one supported install-over of the exact corrected candidate;
3. prove installed plugin/package/skill documentation identity matches the corrected candidate;
4. prove active facade/runtime executable identity remains unchanged;
5. prove MANAGED + Ollama + Gateway + delivery/recovery + SQLite health;
6. one human Dashboard semantic turn only, proving one Ticket -> one session/run -> one Ollama call -> one durable delivery -> one logical Dashboard assistant result, with no retry/recovery/duplicate;
7. post-turn health/provenance proof.

Do **not** repeat reset/uninstall/fresh-reinstall by default. Repeat those destructive lifecycle boundaries only if evidence from the corrected candidate demonstrates a plausible lifecycle impact or a gate failure requires re-proving them.

## Publication gates after requalification

If proportional requalification passes:

1. update safe living docs from requalification-in-progress to accepted/publication-ready state;
2. run exact final candidate validation again if those safe docs change;
3. open a fresh current release PR from `agent/v0.9.3-full-stabilization` to `main`;
4. verify PR topology/diff/checks and merge when green;
5. freeze exact merged `main` SHA;
6. dispatch `.github/workflows/release.yml` with `version=0.9.3` and that exact merged SHA;
7. require successful Release workflow;
8. verify tag `v0.9.3` targets the exact merged SHA;
9. verify GitHub Release notes and assets:
   - `cogentnexus-openclaw-v0.9.3.tar.gz`
   - `cogentnexus-openclaw-v0.9.3.zip`
   - `SHA256SUMS.txt`
10. independently verify published checksums/assets;
11. publish final Task-188 report and stop for ChatGPT review only after publication verification is complete.

## Recovery/checkpoint requirement

Create durable coordination checkpoints at major boundaries: corrected candidate freeze, CI green, pre-Windows mutation, Windows acceptance, pre-merge, and post-release verification. Each checkpoint must include exact HEAD, completed proof, remaining gates, and next exact action.
