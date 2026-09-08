# CNX-20260906-277 — ChatGPT Read-Only Preflight Review

## Verdict

`ACCEPT_PREFLIGHT__EXACT_CANDIDATE_INSTALL_OVER_AUTHORITY_REQUIRED`

Task277 is accepted as a read-only live preflight.

The accepted source/test/CI candidate remains:

`36cd4c800ded28bdb7165fcad6e0bfb48b4e933b`

The installed runtime does not match the accepted candidate. Installed runtime `dist` fingerprint is `f0c15e0fcb58223f40d3c329d40a4e1c9a506c4a905b6fb0780c2e4c6ba2166a` (192 files), while the supported candidate build fingerprint is `0891007136c454efc51fe087225055be8a6f9ab9664e76750fbec6699ac1acb9` (198 files). The installed payload therefore cannot be used to requalify the Task273-275 Discord Direct repair.

Fresh runtime probes are healthy enough for a bounded install-over: Gateway is reachable on `127.0.0.1:18789`, OpenClaw is `2026.7.1-2`, Ollama is reachable with `qwen3.5:9b`, supervisor is enabled/Ready with last result 0, and SQLite integrity is `ok`.

The protected old Ticket `CNXT-dc11c9a0-8a89-4df5-9c48-345260725be4` remains accepted and untouched and its owner session remains excluded from disposable-session operations.

The Task272 sacrificial session `agent:main:discord:channel:1366635842554036314` / sessionId `68ad6250-1d3a-4dac-a1b1-f1da84a10cda` is not clean: it has a later accepted/interrupted Ticket with unconfirmed direct delivery. This is expected evidence from the pre-repair Discord delivery boundary. Do not Delete/reset or dispose it before deploying and requalifying the accepted candidate.

## Required next boundary

A fresh human authorization is required for exactly one supported install-over of candidate `36cd4c800ded28bdb7165fcad6e0bfb48b4e933b`, including only installer-owned managed Gateway transition required by the supported installer.

After install-over, Hermes must verify installed fingerprint and live health read-only. No Discord semantic send, sacrificial-session Delete/reset, Ticket/recovery disposition, manual SQLite mutation, Scheduled Task mutation, uninstall/reset, release promotion, or force push is implied.

Task272's older Delete/test-message authority remains parked and unconsumed; it does not cover this install-over.
