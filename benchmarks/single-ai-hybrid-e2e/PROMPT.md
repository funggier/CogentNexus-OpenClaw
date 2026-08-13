# Task: build and execute a single-AI hybrid workflow

Work inside the empty directory supplied as `SUBMISSION_DIR`. You are the sole
AI executor and reviewer. Build the workflow, execute it end to end, repair the
required failure, and leave independently verifiable evidence. Do not merely
describe a plan.

## Leaf units

Create three JSON candidates with exactly the keys `id` and `score`:

- `candidates/EAST/east.json`: `{"id":"east","score":55}`
- `candidates/WEST/west.json`: first create score as the string `"65"`; the
  deterministic gate must reject it, then repair only this file to integer `65`
- `candidates/ISLANDS/islands.json`: `{"id":"islands","score":90}`

Create `contracts/EAST.json`, `contracts/WEST.json`, and
`contracts/ISLANDS.json`. Each contract must state the objective, exact output
path, allowed write scope, acceptance criteria, and deterministic validation
rules. Create `contracts/INTEGRATION.json` with the integration requirements
below.

## Required workflow

1. Write `manifest.json` identifying the model, single-reviewer mode, the four
   units, deterministic gates, and a maximum of three repairs per unit.
2. Write `config/review-policy.json`. It must use single-reviewer mode and
   require deterministic gates.
3. Create and validate EAST and ISLANDS. Record deterministic evidence and a
   single-reviewer verdict for each.
4. Before creating WEST, record SHA-256 hashes of the accepted EAST and ISLANDS
   candidate files.
5. Create the intentionally invalid WEST candidate with score `"65"`. Preserve
   evidence showing the deterministic type failure.
6. Repair only `candidates/WEST/west.json`, validate it again, and preserve a
   repair record containing its before/after hashes and the before/after hashes
   of EAST and ISLANDS. The sibling hashes must remain unchanged.
7. Produce final reviewer verdicts for every leaf. A PASS verdict must refer to
   deterministic evidence; prose alone is insufficient.
8. Checkpoint each accepted leaf. A checkpoint represents a post-PASS accepted
   state, not the failed WEST attempt.
9. Integrate only accepted leaves into `integration/report.json` with exactly:
   `{"total_leaf_count":3,"sum_total":210,"average_value":70}`.
10. Validate the integration and write `checkpoints/INTEGRATION.json` with root
    status `SUCCESS` and evidence references.

## Evidence and event requirements

Use these directories:

- `evidence/deterministic/`
- `evidence/repairs/`
- `evidence/reviews/`
- `checkpoints/`

Write `events.jsonl` as valid JSON Lines. Every row must contain a monotonically
increasing integer `sequence`, an ISO-8601 `timestamp`, `event`, and `unit_id`.
The log must include, in truthful execution order:

- `candidate_created` for all three leaves;
- `deterministic_gate_passed` for EAST, ISLANDS, repaired WEST, and INTEGRATION;
- `deterministic_gate_failed` for the initial WEST candidate;
- `repair_started` and `repair_completed` for WEST;
- `review_requested` and `review_verdict_received` for every leaf;
- `integration_passed` and `root_gate_passed` for INTEGRATION.

Also create `runner.py` that can reproduce the workflow from a clean submission
directory. It must use only the Python standard library and must not fabricate a
PASS when a deterministic check fails.

Before stopping, run your own root gate and report its command and exit code.
