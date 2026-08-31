# ChatGPT Review — CNX-20260831-187

Executor disposition: `BLOCKED — DOCUMENTATION_BEARING_PRODUCT_PAYLOAD_REQUALIFICATION_REQUIRED`

Reviewer disposition: `ACCEPTED_BLOCKER — PROCEED_WITH_DOCUMENTATION_ONLY_REQUALIFICATION`

## Review conclusion

Task 187 classified the release blocker correctly. The remaining stale current-facing text is not merely external prose: `plugins/cogentnexus-openclaw/README.md` participates in package payload identity, while `skills/cogentnexus-openclaw/SKILL.md` and installed references participate in the installed runtime instruction surface. Updating those bytes creates a new artifact identity and the previously accepted Windows artifact must not be silently relabeled as the corrected artifact.

The blocker does **not** imply that v0.9.3 must repeat the entire stabilization program. The frozen `v0.9.3-full-stabilization` implementation has already passed repository validation plus bounded real-Windows install-over, reset, uninstall, fresh reinstall, and final semantic/durable-delivery acceptance. A documentation-only successor should therefore use proportional requalification.

## Approved successor boundary

The user has authorized continuing to publication after documentation is made current and the corrected documentation-bearing artifact is proportionally requalified.

The successor may:

1. correct stale current-facing documentation/instruction bytes in the plugin/installed skill surfaces;
2. correct safe living documentation to describe the new exact candidate and requalification state;
3. freeze and record new package/skill identities;
4. run exact-candidate repository/package CI;
5. perform one supported Windows install-over of the corrected candidate, verify installed provenance/health and exact documentation bytes, and perform one bounded Dashboard semantic/durable-delivery turn;
6. repeat reset/uninstall/fresh-reinstall only if changed-candidate evidence reveals a lifecycle reason to do so;
7. after requalification passes, proceed to the current PR -> `main` -> exact merged SHA -> Release workflow -> `v0.9.3` tag/GitHub Release path already authorized by the user.

## Hard fence

The successor must not change production/runtime/plugin executable source, tests, dependencies, or workflow behavior merely to obtain release success. Any such need is a new product defect and must block publication for separate handling.

No force push is authorized.
