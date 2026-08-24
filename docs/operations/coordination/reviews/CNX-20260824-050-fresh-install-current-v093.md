# Review — CNX-20260824-050 Fresh-Install Current CogentNexus-OpenClaw v0.9.3

Decision: **ACCEPT_WITH_FOLLOWUP_REQUIRED**

Disposition: `ACCEPT_INSTALLED_RUNTIME_WITH_HELP_DEFECT`

Reviewed task: `CNX-20260824-050`

Reviewed start HEAD: `0b71bf28aaa15650460939276c94cf472d5aa4cb`

Reviewed report commit: `ab0264c11481ad2f31224e376da9b9b51d2fd1c8`

Reviewed report:

[`../reports/CNX-20260824-050-fresh-install-current-v093.md`](../reports/CNX-20260824-050-fresh-install-current-v093.md)

## Publication fence

The compare from the fetched Task 050 start HEAD to the report commit is exactly one commit and exactly one changed path: the Task 050 report. The publication fence passes.

## Accepted live installation boundary

The report result `BLOCKED_POSTINSTALL_RUNTIME` is correct under the literal Task 050 acceptance contract because one required command failed and the terminated installer child exit code was not retained.

Those two facts do not justify reinstalling or treating the durable installation as absent. The following independently bounded postconditions are accepted:

- the single installer body reached its terminal success stage and no second invocation occurred;
- classifier is exact `mode=upgrade`, with current evidence and `legacy=[]`;
- installed ownership verification exited `0`;
- the ownership manifest identifies canonical CogentNexus-OpenClaw v0.9.3 paths and `migrationSource: null`;
- native inventory contains exactly one enabled/loaded canonical plugin v0.9.3 and preserves the 71 unrelated plugins;
- canonical launcher, skill, state, plugin, and supervisor exist;
- controller is MANAGED with Ollama selected and desired Gateway/provider running;
- Gateway and Ollama are healthy and the same four-model inventory remains;
- AGENTS has exactly one canonical marker pair, no legacy marker, and reproduces the exact accepted baseline when the canonical block is removed;
- the Task 049 external backup and unrelated/excluded systems remain preserved;
- there are no installer/lifecycle/Procmon orphans.

The terminated installer's exact process exit code is permanently unobserved. It must not be invented or “recaptured” by rerunning the installer. Durable terminal output and exhaustive poststate are sufficient to accept the live machine as installed, while the review retains that evidence gap explicitly.

No reinstall, clean reinstall, manual installed-file edit, enable, restart, repair, or legacy restore is authorized by this review.

## Root cause of the failed check

The failed `cnxclaw.cmd check cogentnexus` is not merely a Task 050 typo. It exposes a repository help/usage defect:

- `skills/cogentnexus-openclaw/scripts/checks.py` maps the canonical component key `cogentnexus-openclaw`;
- the same mapping correctly rejects unknown key `cogentnexus`;
- `skills/cogentnexus-openclaw/scripts/cnxclaw.py` still advertises `check cogentnexus` in its usage/error and help text;
- `skills/cogentnexus-openclaw/scripts/cnxclaw_v093.py` also still advertises `check cogentnexus`;
- Task 050 copied the stale advertised command;
- the canonical read-only command `cnxclaw.cmd --json check cogentnexus-openclaw` exited `0` with verdict `READY`.

Therefore the runtime check engine is behaving consistently with the canonical namespace contract; the defect is stale operator-facing command documentation in the CLI facade and any current non-historical documentation that repeats it.

## Required bounded successor design

A repository-only successor should:

1. add a failing regression test proving all current CLI help/usage surfaces advertise `check cogentnexus-openclaw` and do not advertise the invalid generic command;
2. prove the test fails against this reviewed report HEAD for the expected stale-help reason;
3. minimally update the base and v0.9.3 CLI facade help/usage strings;
4. inventory and correct the same exact invalid command only in current non-historical operator documentation;
5. keep historical coordination tasks/reports/reviews and immutable release notes unchanged;
6. run the focused test, full Python suite, namespace lint, baseline consistency, compile/self-tests, and relevant plugin validation;
7. publish a repository-only implementation commit plus report.

Do not add a compatibility alias for `cogentnexus`. The canonical component name must remain explicit as `cogentnexus-openclaw`, consistent with coexistence requirements for CogentNexus-HermesAgent.

After that repository fix is reviewed, a separate human decision is required before updating the already-installed copy. The update must use a reviewed ownership-preserving path; do not edit installed files manually.

Human decision required: **YES** — approve the bounded repository-only help/usage correction described above.
