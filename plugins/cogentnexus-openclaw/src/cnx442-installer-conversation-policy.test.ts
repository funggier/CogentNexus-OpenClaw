import { readFileSync } from "node:fs";
import { join } from "node:path";
import { describe, expect, it } from "vitest";

describe("CNX-442 managed conversational runtime policy", () => {
  it("persists followup serialization and immediate active-run typing through supported OpenClaw config", () => {
    const install = readFileSync(join(import.meta.dirname, "..", "..", "..", "scripts", "install.ps1"), "utf8");
    expect(install).toContain("openclaw config set messages.queue.mode followup");
    expect(install).not.toContain("openclaw config set agents.defaults.typingMode instant");
    expect(install).toContain("failed to enforce OpenClaw followup queue policy");
  });
});