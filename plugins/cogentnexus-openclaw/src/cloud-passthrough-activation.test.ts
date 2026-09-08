import { describe, expect, it } from "vitest";
import { mkdtempSync, mkdirSync, readFileSync, writeFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { hostPluginAuthority } from "./v091-release-entry.js";

describe("Cloud pass-through activation boundary", () => {
  it("authorizes passive continuity hooks in passthrough without changing provider ownership", () => {
    const workspace = mkdtempSync(join(tmpdir(), "cnx-cloud-pass-") );
    try {
      const root = join(workspace, ".cogentnexus-openclaw");
      mkdirSync(join(root, "host"), { recursive: true });
      writeFileSync(join(root, "host", "controller.json"), JSON.stringify({
        schemaVersion: 1,
        mode: "passthrough",
        generation: 4,
      }));
      const api: any = {
        pluginConfig: { workspaceDir: workspace },
        config: { agents: { defaults: { workspace } } },
      };
      expect(hostPluginAuthority(api)).toMatchObject({
        authorized: true,
        reason: "passthrough",
        mode: "passthrough",
        generation: 4,
      });
    } finally {
      rmSync(workspace, { recursive: true, force: true });
    }
  });

  it("does not inspect or log the OpenClaw-owned provider or model", () => {
    const source = readFileSync(
      join(dirname(fileURLToPath(import.meta.url)), "v091-release-entry.ts"),
      "utf8",
    );
    expect(source).not.toContain("agents?.defaults?.model?.primary");
    expect(source).not.toContain("Cloud pass-through route accepted");
    expect(source).not.toContain("cloudPassThroughPolicy(");
  });
});
