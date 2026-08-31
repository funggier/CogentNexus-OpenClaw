# Independent Review — CNX-20260828-122 Post-Install Verification Recovery and Lifecycle Continuation

## Verdict

`ACCEPTED BLOCKED — NO NEW MUTATION; THE BLOCK IS A VERIFICATION-CONTRACT/ARGUMENT-FORWARDING DEFECT, NOT A PROVEN PRODUCT FAILURE`

Task 122 correctly preserved the Task-121 one-shot boundary: the consumed install-over was not replayed and reset/uninstall/reinstall/lifecycle/recovery all remained at zero executions.

## Accepted evidence

- Task-121 install-over remains consumed at `1 / 1` and returned exit code `0`.
- Task 122 performed read-only probing only.
- No reset, uninstall, fresh reinstall, stop/start/restart, recovery harness, cleanup/normalization, provider/runtime mutation, OpenClaw rebaseline, Dashboard semantic Send, reboot, merge/tag/release, or force push occurred.
- The Task-122 report commit contains only the Task-122 report path.

## Finding 1 — `Ollama-only` launcher text is expected runtime policy, not installer coupling

Task 122 treated the installed launcher text

`CogentNexus-OpenClaw v0.9.3 (Ollama-only)`

as inconsistent with the provider-neutral installer candidate. That interpretation is incorrect.

At exact candidate `01d08cd7c82f542c821e3a60f7fffa036efb1d75`, `skills/cogentnexus-openclaw/scripts/cnxclaw_v093.py` is explicitly the `v0.9.3 Ollama-only CLI facade` and its help text intentionally states that Ollama is the only supported inference provider in v0.9.3 and that explicit `--provider ollama` remains accepted for compatibility.

The architectural contract accepted in Tasks 117–119 is:

- installation itself is provider-neutral;
- runtime/provider policy remains runtime-owned;
- current v0.9.3 runtime support may remain Ollama-only.

Therefore Ollama-only runtime help text must not block post-install acceptance by itself.

## Finding 2 — the three interactive outcomes strongly indicate lost command arguments

Task 122 reports three superficially different probe failures:

- `cnxclaw.cmd` produced its help/banner output rather than the requested status/check output;
- `openclaw.cmd` selected its TUI path;
- `ollama.exe` selected an interactive UI.

Those are all behaviors consistent with invoking the executable/launcher with no effective command arguments. The pattern therefore points to the executor-created generalized probe/capture wrapper dropping or mis-forwarding arguments, rather than three independent CLI product failures.

The next probe must not reuse that wrapper or a `Start-Process` abstraction whose argument serialization has not itself been proven.

## Finding 3 — deterministic non-interactive proof surfaces already exist

The exact candidate's reviewed Windows recovery harness already demonstrates a safer read-only pattern:

- invoke `cnxclaw.cmd` directly with a PowerShell call operator and an explicit string-array argument list;
- read the OpenClaw config only for non-sensitive fields needed for gateway facts;
- verify listener/process identity directly;
- use runtime/provider state through CNX JSON commands;
- avoid depending on interactive provider/OpenClaw launchers for baseline proof.

For independent OpenClaw proof, a successor may invoke the installed OpenClaw Node entrypoint directly with `node.exe` and separate CLI arguments, and may also read the installed OpenClaw `package.json` for the exact version. For Ollama, use loopback HTTP API/listener evidence rather than the desktop executable UI.

## Required successor

Open a read-only-only successor. It must:

1. perform no reset/uninstall/reinstall/lifecycle/recovery mutation;
2. keep Task-121 install-over permanently consumed and forbidden to replay;
3. avoid the Task-121/122 generalized probe wrapper;
4. invoke each command directly with explicit argument arrays;
5. treat Ollama-only CNX runtime text as expected v0.9.3 runtime policy, not installer coupling;
6. use direct Node/package metadata and listener/config evidence for OpenClaw where needed;
7. use Ollama loopback REST API/listener evidence rather than interactive `ollama.exe` commands;
8. run ownership verification and SQLite integrity checks with explicit resolved Python/script paths;
9. prove plugin/root uniqueness and exact installed candidate attribution;
10. publish a read-only report and stop for independent review.

Only after that read-only gate independently passes should a later task authorize `reset -> uninstall -> fresh reinstall -> lifecycle -> recovery`.
