# CNX-20260831-180 — ChatGPT Review

- **Task:** `CNX-20260831-180`
- **Executor report:** `docs/operations/coordination/reports/CNX-20260831-180-hermes-repaired-candidate-windows-install-over-provenance-health.md`
- **Disposition:** `ACCEPTED_BLOCKED`
- **Label:** `BLOCKED — PREINSTALL_TASK178_OUTER_OBSERVER_CLEANUP_REQUIRED`
- **Reviewed repository candidate:** `f6392da3e4112ce441526d5ef19925c90a872b0b`
- **Reviewed report tip:** `ed649ed1496f3c1cd10c0d9179f01953ac20da69`

## Reviewer conclusion

Task 180 correctly stopped before install-over. The report and its later impact addendum establish that no installer invocation occurred, no reset/uninstall/reinstall was attempted, no semantic/model/recovery action occurred, and no live product state was mutated. The only blocking condition is the still-running historical Task-178 outer observer chain.

The actual Task-178 reset command and lifecycle descendants had already been retired in Task 179. The remaining chain is an evidence/observer wrapper (`run_reset178.py` under its bash wrappers), not a live `cnxclaw reset` child. The retained Task-178 ledger still records zero prompt/input events. This makes the condition primarily an operational/preflight blocker rather than evidence of product corruption.

Task 180 did not authorize killing that observer, so refusing to start the supported install-over was the correct fence behavior.

## Independent verification

1. **Publication scope:** `a7918285... -> ed649ed1...` is two commits but the effective changed path is only the Task-180 report. The second commit is an impact addendum to that same report. No source/product/test/workflow drift occurred.
2. **Installer boundary:** Task-180 reports installer invocation count `0`; therefore active-facade post-install equality and post-install runtime health remain unproven, not failed.
3. **Candidate identity:** exact repository candidate remains `f6392da3e4112ce441526d5ef19925c90a872b0b`; clean candidate facade SHA-256 is `aa747f8f30080ef839a8d2cbf5758f9981a007ca01f41a988576f42edea8682f`.
4. **Installed baseline:** current installed facade SHA-256 remains `e15e8af49e18925fb569cd405b18fe5c57172d1a0e4644e359703b692cacb032`, confirming the Task-179 repair has not yet been installed.
5. **Reset descendants:** historical reset command/lifecycle descendants are absent; the remaining observer chain is reported as bash `14196 -> 22832 -> Python 17052 -> Python 17444` with `run_reset178.py` identities.
6. **Input boundary:** retained Task-178 ledger remains zero prompt/input events; no new confirmation input was sent.
7. **Runtime preservation:** controller/Gateway/Ollama/delivery/recovery/ownership remained healthy/read-only and Task-171 historical durable state remained present.
8. **Impact addendum:** fresh scan after report publication still found the same observer and no actual reset child, strengthening the cleanup requirement without changing product state.

## Acceptance matrix

| Criterion | Verdict |
|---|---|
| Fresh Task-180 authority/preflight | PASS |
| Report-only publication scope | PASS |
| Exactly zero installer invocations | PASS |
| No reset/uninstall/reinstall/helper action | PASS |
| No semantic/model/recovery action | PASS |
| Runtime/durable baseline preserved | PASS |
| Task-178 actual reset descendants absent | PASS |
| Historical outer observer absent | BLOCKED |
| Repaired facade installed | UNPROVEN |
| Post-install provenance/health | UNPROVEN |

## Residual work

Open a narrow successor that authorizes only identity-checked retirement of the historical Task-178 outer observer chain and read-only verification of a clean process/runtime/durable boundary. It must not install, reset, uninstall, restart providers/Gateway, or change repository product source.

Only after that cleanup is independently accepted should a later task authorize one supported install-over of `f6392da3...`. Another reset remains unauthorized until active installed facade byte identity and post-install health are proven.
