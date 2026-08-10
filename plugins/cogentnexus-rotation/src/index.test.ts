import { describe, expect, it } from "vitest";
import entry, { rotationIdentity } from "./index.js";
import { getToolPluginMetadata } from "openclaw/plugin-sdk/tool-plugin";

describe("cogentnexus-rotation", () => {
  it("declares the rotation tool", () => {
    expect(getToolPluginMetadata(entry)?.tools.map((tool) => tool.name)).toEqual(["cogent_rotation"]);
  });

  it("uses a deterministic generation-fenced identity", () => {
    expect(rotationIdentity("CNX-PHASE4-001", 3)).toEqual({
      runId: "cogent-rotate-cnx-phase4-001-3",
      childSessionKey: "agent:main:cogent-rotate-cnx-phase4-001-3",
    });
  });
});
