# CNX-20260906-278 — ChatGPT Partial Install Review

## Verdict

`ACCEPT_EXACT_PAYLOAD_INSTALLED__MANAGED_ACTIVATION_INCOMPLETE__FRESH_ENABLE_AUTHORITY_REQUIRED`

Task278 consumed the single authorized supported install-over. The installer did not produce a proven terminal completion result before the external tool timeout, so Task278 is not accepted as a completed install-over.

However, the supported installer completed the replacement payload stages through `owned-runtime-ensure`, the installed plugin fingerprint exactly matches accepted candidate `36cd4c800ded28bdb7165fcad6e0bfb48b4e933b`, ownership/runtime artifacts were written, Gateway and Ollama are reachable, and the protected durable state was preserved.

The remaining state is a coherent partial activation boundary:

- installed plugin is the exact candidate;
- plugin is `enabled=false` / `status=disabled`;
- Host controller is `passthrough`;
- the installer did not reach the later MANAGED enable/final health/completion boundary;
- no second installer invocation is authorized or appropriate.

## Source adjudication

Exact-candidate `scripts/install.ps1` performs, after the observed payload/runtime boundary:

1. installed plugin identity/fingerprint resolution;
2. ownership create + exact verify;
3. managed policy apply;
4. `& $ownedPython $cliScript --root $cogentNexusOpenClawRoot enable` when Gateway restart is not skipped;
5. Gateway status, supervisor doctor, CNX status;
6. final installation-success message.

Therefore `plugin disabled + Host passthrough` is not a cosmetic terminal state. MANAGED activation remains incomplete.

Repository history contains a supported recovery pattern for this exact class of state: after proving a canonical replacement payload while remaining PASSTHROUGH, invoke the installed canonical launcher exactly once as `cnxclaw.cmd enable`, then prove MANAGED authority and runtime health. This is narrower and safer than rerunning the installer.

## Required next authority

Open Task279 as a fresh human authorization gate for exactly one supported MANAGED re-entry:

`C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd enable`

Before consuming that authority Hermes must re-read live state and prove:

- installed fingerprint still equals the accepted candidate;
- ownership verification passes;
- plugin remains disabled;
- controller remains PASSTHROUGH;
- Gateway/Ollama are reachable;
- protected old Ticket and Task272 sacrificial lineage remain untouched.

If those predicates hold, exactly one `enable` invocation may run. If enable fails, do not retry. Afterward perform read-only proof of plugin loaded/enabled, Host MANAGED, supervisor present/healthy, Gateway/Ollama healthy, SQLite integrity, and protected durable-state preservation.

No installer rerun, semantic send, session Delete/reset, Ticket/recovery disposition, manual SQLite mutation, uninstall/reset, release promotion, or force push is implied.

Task272's parked Delete/test-message authority remains separate and unconsumed.
