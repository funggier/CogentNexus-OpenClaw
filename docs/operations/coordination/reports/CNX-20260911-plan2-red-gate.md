# CNX-20260911 — Plan 2 RED Gate

The first Plan 2 change is intentionally test-only.

## Expected failing contract

`plugins/cogentnexus-openclaw/src/v095-session-generation.test.ts` imports `shouldAdvanceSessionGeneration()` from `v095-session-generation.ts`, which does not yet exist on the base.

## Required RED evidence

The focused Vitest invocation must fail because the implementation module/function is absent or otherwise because the intended contract is not implemented. Fixture/setup failures are not acceptable RED evidence.

## Next step

After the RED failure is observed, add the minimal pure helper without modifying `cnx_sessions` storage or provider routing, then rerun the focused test for GREEN.
