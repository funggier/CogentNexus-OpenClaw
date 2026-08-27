# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `SOURCE_TDD_COMPLETE_INSTALLABLE_PLUGIN_PAYLOAD_ATTESTATION`
Current authorization: `TASK093_DEPLOYMENT_ATTESTATION_REPAIR_AUTHORIZED`
Task ID: `CNX-20260827-094`
Updated: 2026-08-27 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260827-094-repair-complete-installable-plugin-payload-fingerprint.md`](tasks/CNX-20260827-094-repair-complete-installable-plugin-payload-fingerprint.md)

## Operator-approved bounded design

The operator approved replacing the current four-file sample fingerprint with a deterministic fingerprint over the complete installable plugin payload.

The fingerprint authority is the package-owned content selected by `package.json.files`, plus `package.json` itself, expanded safely and deterministically.

Required digest domain:

- complete shipped `dist/**` runtime;
- shipped manifest/bootstrap/README and other declared package files;
- normalized sorted relative paths plus exact file bytes;
- no absolute root path;
- explicit versioned fingerprint domain separator;
- fail closed on unsafe path traversal, symlink/path indirection, missing declared entries or unsupported package-file contract.

Development-only `src/**`, tests, `node_modules/**`, caches and transient tarballs are not fingerprinted unless they are explicitly part of the shipped package contract.

## Task 093 review carried forward

Task 093 implementation:

`a924157ecdedef1d4f166d5762529b0d59536fc9`

Task 093 report:

`62fdd69d2a4a27566c0e986171b949347cf0df68`

Independent disposition:

`REWORK_PLUGIN_FINGERPRINT_DOES_NOT_ATTEST_RUNTIME_PAYLOAD`

The Dashboard durable-staging source fix itself remains preserved and is not the current rework target.

## Blocking deployment-attestation defect

Current `namespace_ownership.py::_plugin_payload()` hashes only four files and omits most shipped runtime files, including `dist/v091-dashboard-verified-delivery.js` changed by Task 093.

Task 093 therefore produced the same legacy fingerprint as the currently installed pre-fix package even though runtime behavior differs.

Because `classify-install` uses this fingerprint to decide `pluginAlreadyExact`, a live successor could skip installing the Task-093 fix.

## Task 094 mandatory proof

Task 094 must RED first against the production helper and prove that changing only a non-ticket-store shipped runtime file currently leaves the fingerprint unchanged.

After GREEN it must prove:

1. any shipped runtime content/path add/remove/rename changes the v2 fingerprint;
2. the same installable payload copied to another absolute root hashes identically;
3. actual npm11/npm12 packed file sets are covered by the fingerprint file set;
4. unsafe/missing/ambiguous package paths fail closed;
5. Task-093 candidate and current pre-fix live payload differ under the new v2 fingerprint;
6. changed single-generation classification returns `pluginAlreadyExact=false` and production actions `installPlugin=true`, `rolloverPlugin=true`;
7. exact payload returns no-install/no-rollover;
8. two-generation pending rollover remains rollover-only with exact expected-source attestation;
9. all Task-084/085/086 rollover security/atomicity and Task-089 installer action boundaries remain green;
10. Task-093 Dashboard staging tests remain green.

## Hard live/semantic fence

Task 094 is source/test-only.

Read-only fingerprinting of the installed plugin root is allowed for candidate-vs-live attestation evidence.

No install/install-over/uninstall/reset/cleanup, plugin-generation mutation, controller/startup/Supervisor/AGENTS/config/runtime/SQLite edit, semantic message, provider probe, model/timeout change, reboot, merge, tag or release is authorized.

Task-092 semantic artifacts remain retired evidence and must not be repaired or reused.

## Successor gate

Only independent acceptance of:

`PASS_COMPLETE_INSTALLABLE_PLUGIN_PAYLOAD_ATTESTATION_REPAIRED`

may authorize a one-shot supported live install-over of the exact Task-093+094 source.

That future live task sends zero semantic messages. A new final authenticated fresh-session semantic attempt remains forbidden until the updated source is installed and live parity/MANAGED health are independently accepted.
