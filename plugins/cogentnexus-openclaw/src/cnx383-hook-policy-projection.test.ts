import { describe, expect, it } from "vitest";
import entry from "./v091-release-entry.js";

type Normalized = { entries: Record<string, { hooks?: { allowConversationAccess?: boolean } }> };

/**
 * CNX-383 RED regression at the proven CNX-382 boundary.
 *
 * The host loader does not use the executable definition for hookPolicy. It
 * evaluates normalized.entries[pluginId] and passes that entry's hooks to
 * createApi. This test intentionally fails until an authorized projection is
 * implemented at that boundary: the executable declaration is true, while
 * the normalized runtime entry used by the host is empty.
 */
describe("CNX-383 hook-policy projection boundary", () => {
  it("projects executable allowConversationAccess into the host policy input", () => {
    const normalized: Normalized = { entries: { [entry.id]: {} } };
    const executablePolicy = (entry as typeof entry & {
      hooks: { allowConversationAccess: boolean };
    }).hooks;
    const hostHookPolicy = normalized.entries[entry.id]?.hooks;

    expect(executablePolicy.allowConversationAccess).toBe(true);
    // RED on the pre-repair source: the host reads normalized entry hooks,
    // not entry.hooks. This is the exact CNX-382 loss boundary.
    expect(hostHookPolicy?.allowConversationAccess).toBe(true);
  });
});
