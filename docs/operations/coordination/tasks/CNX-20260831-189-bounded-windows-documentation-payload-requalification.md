# CNX-20260831-189 — Bounded Windows Documentation-Payload Requalification

Status: `READY_FOR_HERMES`
Parent task: `CNX-20260831-188`
Executor: Hermes on the already accepted Windows host
Coordinator / final reviewer: ChatGPT
Repository: `funggier/CogentNexus-OpenClaw`
Working branch: `agent/v0.9.3-full-stabilization`

## Purpose

Requalify the documentation-corrected v0.9.3 artifact on the real Windows host without needlessly repeating destructive lifecycle acceptance that already passed during full stabilization.

This is an execution subtask under Task 188. It is **not** a new release umbrella and it does not authorize PR merge, tag creation, GitHub Release publication, reset, uninstall, or fresh reinstall.

## Exact product candidate — immutable for this task

Use exactly:

`604569c286e930f1a596362ab926b065b56d486e`

Any later coordination-only commit on `agent/v0.9.3-full-stabilization` does **not** redefine this candidate. Do not install or test branch HEAD unless `git rev-parse HEAD` is exactly the SHA above.

### Candidate identity

- version: `0.9.3`
- package payload-v2 fingerprint: `408167da1bfba7fa9723d1bd557f29d516ed27c27398b4e48abf9a4f294e6b5b`
- payload file count: `184`
- installed skill-tree Git tree SHA: `a1e873ba404205507a1623961b49f1b1a0689f9f`
- executable scripts-tree Git tree SHA: `3d9d323ba19443d46e970b87cef52ce878da274f`
- accepted `skills/cogentnexus-openclaw/scripts/cnxclaw.py` Git blob: `879083d6186589d4b2774b8fd87fa93692dd2dfc`
- accepted `cnxclaw.py` SHA-256: `aa747f8f30080ef839a8d2cbf5758f9981a007ca01f41a988576f42edea8682f`

### Exact-candidate repository gates already PASS

- Validate: run `33382417045` — `success`
- Windows Installer Pack Smoke: run `33382417032` — `success`
- PS5.1 Acceptance Smoke: run `33382417028` — `success`
- package-proof artifact ID: `9754267508`
- dry-run tar.gz SHA-256: `16523b0226aed0aa1eb58a3e335bfadb34abdc027777806bd7c74133c07c3457`
- dry-run zip SHA-256: `e273a967771f281c895402dd8b2078bd1ec6c1944d9a8e817cf73f467e38fc06`

## Why requalification is bounded

The implementation/runtime already passed the v0.9.3 full-stabilization Windows sequence, including install-over, reset/fresh-state, uninstall/external-preservation, fresh reinstall, and final Dashboard semantic/durable-delivery acceptance. Task 188 changed documentation/instruction-bearing product files while preserving executable scripts/runtime bytes.

Therefore the proportional boundary is:

`one exact-candidate install-over -> provenance/health/installed-byte proof -> one bounded semantic durable-delivery turn`

Do not repeat reset, uninstall, or fresh reinstall unless new evidence demonstrates that a lifecycle boundary has actually drifted.

## Changed product surface to requalify

Task 188 intentionally changed only these installed/payload documentation files:

1. `plugins/cogentnexus-openclaw/README.md`
2. `skills/cogentnexus-openclaw/SKILL.md`
3. `skills/cogentnexus-openclaw/references/architecture.md`
4. `skills/cogentnexus-openclaw/references/scheduler-adapters.md`

Safe root/living documentation was also converged, but executable/runtime/plugin source, tests, dependencies, and workflow behavior were not changed.

## Phase A — read-only preflight

Before any mutation:

1. Record UTC/local timestamp and Windows host identity sufficient to tie evidence to this run.
2. Record current OpenClaw version. Expected accepted line: `2026.7.1-2 (0790d9f)` unless the host has intentionally changed; unexpected drift is a review signal, not permission to repair unrelated software.
3. Record current CogentNexus/OpenClaw status and managed provider. Expected provider: Ollama.
4. Record current active facade path and SHA-256.
5. Record current installed plugin inventory/fingerprint using the repository's supported provenance/identity tooling where available.
6. Record enough current state to prove install-over did not erase unrelated runtime state.
7. Do not send a Dashboard semantic message in preflight.

If preflight reveals material host/runtime drift from the previously accepted environment, stop with `BLOCKED_HOST_DRIFT` and report evidence. Do not broaden scope silently.

## Phase B — acquire the exact candidate

Use an isolated temporary checkout/source directory.

Required proof before installation:

- repository is `funggier/CogentNexus-OpenClaw`;
- `git rev-parse HEAD` (or equivalent exact source provenance) equals `604569c286e930f1a596362ab926b065b56d486e`;
- `VERSION` is `0.9.3`;
- source `cnxclaw.py` matches accepted executable identity;
- source changed documentation files are present.

Do not substitute a moving branch tip, `main`, an old release archive, or a different candidate SHA.

## Phase C — exactly one supported install-over

Perform one normal supported **install-over** from the exact candidate using the repository's documented development-candidate/source installation path.

Hard boundaries:

- no `reset`;
- no `uninstall`;
- no clean/fresh reinstall;
- no manual deletion of CogentNexus/OpenClaw state;
- no provider replacement;
- no source/test/dependency/workflow edits;
- no repair of unrelated machine configuration unless required merely to execute the already-supported install path; if such repair would alter acceptance meaning, BLOCK and report instead.

Capture installer command, exit code, relevant stdout/stderr, and provenance.

## Phase D — post-install provenance and byte proof

After install-over, prove all of the following:

1. CogentNexus/OpenClaw reports healthy enough for the supported runtime path.
2. Managed provider remains Ollama.
3. Active facade still resolves to the accepted `cnxclaw.py` executable identity; SHA-256 must remain `aa747f8f30080ef839a8d2cbf5758f9981a007ca01f41a988576f42edea8682f` unless a path-normalization detail is proven irrelevant and bytes remain exact.
4. Installed plugin/package provenance corresponds to v0.9.3 exact candidate and the documentation-corrected payload.
5. For each of the four changed documentation files, compute source and installed SHA-256 and prove byte-for-byte equality where that file is part of the installed surface.
6. Prove `SKILL.md` and the two changed references installed into the active skill tree match the exact candidate.
7. Prove install-over did not unintentionally erase durable state or alter unrelated provider/runtime configuration.
8. Record post-install plugin inventory/fingerprint. A changed live inventory fingerprint is expected if its identity domain includes the corrected plugin README; classify the domain correctly instead of comparing it blindly to the historical live fingerprint.

Historical accepted live installed-plugin inventory fingerprint for reference only:

`e7d7d6c115040368e35232c83cacec315f6667c92452a5641f7a48a6947baf19`

This historical live fingerprint is a different identity domain from the repository package payload-v2 fingerprint and is **not** required to remain equal after the plugin README correction.

## Phase E — one bounded Dashboard semantic/durable-delivery turn

Only after Phases A-D pass, perform exactly one human Dashboard semantic turn to validate the changed installed instruction surface.

Required accepted shape:

`1 human Send -> 1 Ticket -> 1 session/run -> 1 Ollama model call -> 1 durable assistant delivery -> 1 logical Dashboard assistant result`

Verify from durable evidence, not visual impression alone:

- exactly one Ticket attributable to the human send;
- one logical execution/session/run for that turn;
- one Ollama model call attributable to the turn;
- one durable assistant delivery;
- one logical Dashboard assistant result;
- no retry/direct-recovery path unless explicitly surfaced as a failure signal;
- no duplicate assistant result;
- no unexpected outbox residue after terminal delivery.

If Hermes cannot itself perform the genuinely human Dashboard Send, stop after Phase D with `WAITING_HUMAN_SEMANTIC_SEND`, provide the exact one-message boundary, and do not simulate extra sends.

## Failure / escalation rules

- If a changed documentation file fails installed-byte proof: `FAIL_DOCUMENTATION_INSTALL_IDENTITY`.
- If executable facade/runtime bytes changed unexpectedly: `BLOCKED_EXECUTABLE_IDENTITY_DRIFT`.
- If host/OpenClaw/provider materially drifted before install: `BLOCKED_HOST_DRIFT`.
- If install-over fails: `FAIL_INSTALL_OVER` with exact evidence; do not fall back to uninstall/reinstall automatically.
- If semantic turn duplicates, retries unexpectedly, loses durable delivery, or leaves residue: `FAIL_SEMANTIC_DURABLE_DELIVERY`.
- If evidence suggests reset/uninstall/fresh-reinstall must be repeated, stop with `REQUALIFICATION_SCOPE_EXPANSION_REQUIRED` and explain why. ChatGPT/user must review before destructive expansion.

## Required Hermes report

Publish a durable report under:

`docs/operations/coordination/reports/CNX-20260831-189-bounded-windows-documentation-payload-requalification.md`

The report must contain:

- exact candidate SHA used;
- host/OpenClaw/provider preflight;
- exact installation source/provenance;
- install-over command/result;
- source-vs-installed SHA-256 proof for changed docs;
- active facade path/hash after install;
- pre/post plugin inventory/fingerprint with identity-domain explanation;
- health/status evidence;
- semantic-turn Ticket/session/model-call/delivery/Dashboard evidence, or `WAITING_HUMAN_SEMANTIC_SEND` if that is the only remaining human boundary;
- anomalies;
- explicit `PASS`, `FAIL`, `BLOCKED`, or `WAITING_HUMAN_SEMANTIC_SEND` disposition;
- statement that reset/uninstall/fresh-reinstall were **not** performed unless a separately authorized scope expansion occurred.

## Stop boundary

Hermes stops after publishing the Task-189 report. Hermes does **not** create or merge a release PR, dispatch Release workflow, create `v0.9.3`, or publish GitHub Release assets. ChatGPT reviews Task 189 and resumes Task 188 release publication only after acceptance evidence is sufficient.
