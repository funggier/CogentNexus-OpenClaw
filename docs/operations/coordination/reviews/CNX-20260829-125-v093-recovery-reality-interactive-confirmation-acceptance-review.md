# Independent Review — CNX-20260829-125

## Verdict

**ACCEPTED FAIL — GATEWAY-CRASH RECOVERY PASSED, BUT PROVIDER-CRASH RECOVERY FAILED TO REACH THE REVIEWED DURABLE-READY CONTRACT WITHIN 420 SECONDS; SOURCE/HARNESS ROOT-CAUSE DIAGNOSIS IS REQUIRED BEFORE ANY REPLAY.**

## Accepted evidence

Task-125 report:

`docs/operations/coordination/reports/CNX-20260829-125-v093-recovery-reality-interactive-confirmation-acceptance.md`

Report commit:

`2d694573eb8b10bc85ba6bc566dd7c289be12950`

The report is accepted as authoritative for this failure boundary because:

- the exact frozen candidate remained `01d08cd7c82f542c821e3a60f7fffa036efb1d75`;
- the exact reviewed recovery harness blob remained `80da4a2a23f5b5e936d725dcbd695a631bad1cb6`;
- Task 125 used a true PTY;
- the exact `Type y to continue:` prompt appeared;
- exactly one lowercase `y` plus Enter was supplied after the prompt;
- `explicit-disruptive-confirmation` recorded `PASS`;
- prechecks passed for OpenClaw `2026.7.1-2`, OpenClaw config validation, and Ollama `0.32.15`;
- `gateway-crash` completed `PASS`;
- `provider-crash` was actually injected;
- `converge-provider-after` failed because the reviewed durable READY predicate was not satisfied inside `RecoveryFuseSeconds=420`;
- harness exit code was `1`;
- `operator-stop` did not execute because fail-stop worked;
- the suite was not replayed;
- harness-owned cleanup returned the machine to a healthy managed state;
- no Dashboard semantic Send occurred.

## Failure classification

This is no longer an acceptance-shell, PTY, confirmation, argument-forwarding, or evidence-decoding ambiguity.

The first failing product/acceptance boundary is:

`provider hard crash -> provider listener recovery path -> durable convergence polling -> no accepted READY convergence within 420 seconds`

The exact harness durable convergence predicate requires, for the provider-crash case:

- host mode `managed`;
- host selected provider `ollama`;
- provider status selected provider `ollama`;
- recovery verdict `READY`;
- exactly one `Provider event adapter` row with `details.expected == false`;
- Gateway listener present;
- Ollama listener present;
- exactly one `Provider recovery incident` row with `details.circuitOpen == false`.

The Task-125 report does not identify which one or more of those fields prevented convergence. Therefore the next task must diagnose the retained observation series before changing source or acceptance semantics.

## One-shot ledger

Consumed and forbidden to replay without a new explicit post-repair acceptance authorization:

- Task-121 install-over: `1 / 1`;
- Task-124 reset: `1 / 1`;
- Task-124 uninstall: `1 / 1`;
- Task-124 fresh reinstall: `1 / 1`;
- Task-124 stop: `1 / 1`;
- Task-124 start: `1 / 1`;
- Task-124 restart: `1 / 1`;
- Task-125 recovery suite execution: `1 / 1`;
- Task-125 gateway-crash scenario: `1 / 1 PASS`;
- Task-125 provider-crash scenario: `1 / 1 FAIL at durable convergence`;
- Task-125 operator-stop scenario: `0`, not reached.

Task-126 must not replay any of these live operations.

## Required successor

Open a repository/source diagnosis-and-repair task that:

1. reads the retained Task-125 JSON/log evidence without mutating live runtime;
2. extracts the first, last, and representative `converge-provider-after` observations and identifies the exact unsatisfied predicate(s) over the 420-second window;
3. correlates those observations with the provider recovery state machine, provider event adapter, recovery incident/circuit state, supervisor behavior, and recovery-check verdict construction;
4. determines whether the defect belongs to product recovery logic or the reviewed acceptance predicate/harness; do not assume either in advance;
5. writes a focused RED regression test reproducing the observed failure before production changes;
6. applies the smallest responsibility-local fix at the owning layer;
7. runs focused tests, full Python/plugin suites, static checks, exact-SHA CI, and package proof;
8. publishes a new candidate only if all repository/source/CI/package gates pass.

No live Windows lifecycle or recovery replay is authorized by this review.

## Dashboard fence

The final Dashboard durable-delivery acceptance remains unopened and prohibited until real-Windows recovery acceptance passes on a repaired exact candidate.