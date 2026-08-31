# CNX-20260831-182 — ChatGPT Review

- **Task:** `CNX-20260831-182`
- **Executor disposition:** `PASS — REPAIRED_CANDIDATE_INSTALL_OVER_ACTIVE_FACADE_PROVEN`
- **Reviewer disposition:** `ACCEPTED_PASS`
- **Reviewer label:** `PASS — REPAIRED_CANDIDATE_INSTALL_OVER_ACCEPTED`
- **Accepted repository repair candidate:** `f6392da3e4112ce441526d5ef19925c90a872b0b`
- **Task-182 report publication:** `8c1015b6b4cb5846e71bc972501b300d2418f6c0`

## Independent verification

Task-182 publication is report-only relative to activation commit `fc9f52ca8d56013731f9f123d5093c83817f5183`.

Accepted evidence:

- clean observer/lifecycle process boundary immediately before mutation;
- exactly one supported `scripts/install.ps1` invocation;
- installer exit code `0` and successful v0.9.3 completion output;
- active installed `cnxclaw.py` reached by `cnxclaw.cmd` is byte-identical to the accepted candidate;
- installed active-facade SHA-256 is `aa747f8f30080ef839a8d2cbf5758f9981a007ca01f41a988576f42edea8682f`;
- release `0.9.3`, OpenClaw `2026.7.1-2 (0790d9f)`, plugin loaded/enabled, ownership coherent, legacy namespace empty;
- controller remains MANAGED, selected provider is Ollama, Gateway/Ollama healthy;
- delivery/recovery READY, pending outbox `0`;
- SQLite integrity `ok` and durable row counts unchanged;
- Task-171 historical pre-reset durable state remains present;
- reset `0`, uninstall `0`, second installer/retry `0`, semantic/model/recovery action `0`.

The npm warnings and historical ticket summary in installer output do not contradict install acceptance because installer completion, independent post-state, active facade identity, and durable-count preservation all passed.

## Fresh reset implementation correlation

The exact accepted candidate was re-read before opening the successor:

- `cnxclaw_v093.py` injects `--provider ollama` for `reset` when no explicit provider is supplied;
- repaired `cnxclaw.py` routes `reset`/`uninstall` through direct interactive stdin/stdout/stderr delegation;
- `host_control_v092.py` routes destructive lifecycle into `lifecycle_v092`;
- `lifecycle_v092.reset()` performs ownership/provider/route/plugin-payload preflight before confirmation;
- explicit confirmation remains `input("Continue? [y/N]: ")`, and only exact `y` crosses the destructive boundary;
- reset owns disable/native-route restoration, startup/config cleanup, CNX state recreation, DB bootstrap, policy, Ollama route transition, enable, Gateway activation, health verification, and final commit.

## Decision

Task 182 is accepted. The Task-179 repaired facade is now proven active on the Windows installation.

A new reset acceptance may be authorized as a distinct task. It must use the previously qualified character-prompt/concurrent-drain/incremental-ledger harness architecture, permit exactly one reset invocation and exactly one literal `y`, forbid retry, and preserve evidence if the supervisory shell/session loses contact.

Uninstall remains unauthorized until reset fresh-state acceptance is independently reviewed.
