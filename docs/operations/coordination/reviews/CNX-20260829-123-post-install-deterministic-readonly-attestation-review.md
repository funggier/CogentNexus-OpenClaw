# CNX-20260829-123 — Independent Review — Post-Install Deterministic Read-Only Attestation

## Verdict

**ACCEPTED PASS — CURRENT POST-INSTALL STATE IS COHERENT; REMAINING ONE-SHOT LIFECYCLE MAY ADVANCE FROM RESET WITHOUT REPLAYING INSTALL-OVER.**

## Reviewed report

`docs/operations/coordination/reports/CNX-20260829-123-post-install-deterministic-readonly-attestation.md`

Report commit:

`d386d856d5a03a042863f9ad9fe3c82a9b991859`

## Accepted facts

The report proves the Task-121 install-over result using deterministic read-only probes after earlier executor-side probe-wrapper defects were isolated.

Accepted current machine facts:

- frozen candidate source remains `01d08cd7c82f542c821e3a60f7fffa036efb1d75`;
- artifact ID remains `9691451156`;
- payload/plugin fingerprint remains `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`;
- CNX is `managed`, desired Gateway/provider are running, selected provider is `ollama`, and recovery verdict is `READY`;
- installed plugin fingerprint exactly matches the frozen candidate;
- installed critical script hashes match the exact candidate extraction;
- OpenClaw remains exactly `2026.7.1-2`;
- exactly one current `cogentnexus-openclaw` plugin registration is loaded/enabled from the canonical extension root;
- Gateway is healthy on loopback `127.0.0.1:18789` with a verified OpenClaw Node process;
- Ollama remains reachable on loopback, version `0.32.15`, with four models preserved and no provider/model mutation;
- CNX SQLite `PRAGMA integrity_check` returned exactly `ok`;
- supervisor/OpenClaw scheduled-task evidence is coherent;
- no active conflicting legacy/current product root was found;
- historical install backups/staging/transaction residue was preserved rather than manually normalized;
- Task 123 performed zero product/runtime lifecycle mutation and zero Dashboard semantic Send.

## Harness-defect interpretation

The earlier Task-121/122 failures are not product failures. The final Task-123 evidence correctly avoids the generalized wrapper/automatic `$args` collision and uses argument-safe direct invocations, direct Node entrypoints, process/listener proof, and Ollama loopback REST.

The v0.9.3 `Ollama-only` CLI/runtime text is expected current runtime policy and is compatible with a provider-neutral installer. It must not be treated as an installer regression.

## Repository fence

From Task-123 activation commit `3177e019557f55a90e556b52b830590719be2417` to report commit `d386d856d5a03a042863f9ad9fe3c82a9b991859`, the branch advanced by exactly one commit and added only the Task-123 report. No source, test, package, or candidate drift occurred.

## One-shot ledger carried forward

Consumed and forbidden to replay:

- Task-121 install-over: **1 / 1**.

Still unconsumed:

- reset: `0 / 1`;
- uninstall: `0 / 1`;
- fresh reinstall after successful uninstall: `0 / 1`;
- stop: `0 / 1`;
- start: `0 / 1`;
- restart: `0 / 1`;
- recovery harness: `0 / 1`.

## Advancement decision

The exact candidate may advance to a separately authorized remaining real-Windows lifecycle acceptance beginning at **reset**, not install-over.

The successor must:

- preserve the consumed install-over fence;
- use the same deterministic post-phase verification discipline that passed Task 123;
- execute each remaining disruptive phase at most once;
- stop immediately on first non-zero, failed postcondition, ambiguity, or integrity mismatch;
- preserve external OpenClaw/provider/models/unrelated workspace data;
- not manually normalize residue to force continuation;
- keep the final Dashboard durable-delivery acceptance out of scope until lifecycle acceptance passes and is independently reviewed.
