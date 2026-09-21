import { readFileSync } from "node:fs";
import { join } from "node:path";
import { describe, expect, it } from "vitest";
import entry from "./v091-release-entry.js";

describe("CNX-383 hook-policy projection boundary", () => {
  it("projects allowConversationAccess through executable policy and supported installer config", () => {
    const executablePolicy = (entry as typeof entry & {
      hooks: { allowConversationAccess: boolean };
    }).hooks;
    expect(executablePolicy.allowConversationAccess).toBe(true);

    const install = readFileSync(
      join(import.meta.dirname, "..", "..", "..", "scripts", "install.ps1"),
      "utf8",
    );
    expect(install).toContain(
      "openclaw config set plugins.entries.cogentnexus-openclaw.hooks.allowConversationAccess true",
    );
    expect(install).toContain(
      "failed to enforce OpenClaw conversation-hook policy",
    );
  });
});
