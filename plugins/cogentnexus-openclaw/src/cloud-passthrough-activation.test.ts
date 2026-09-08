import { describe, expect, it } from "vitest";
import { mkdtempSync, mkdirSync, writeFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
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
});
