import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

describe("v0.9.5 provider-independent capabilities", () => {
  const sourcePath = resolve(process.cwd(), "src", "v091-release-entry.ts");
  const source = readFileSync(sourcePath, "utf8");

  it("does not suppress CNX registration surfaces in provider pass-through mode", () => {
    expect(source).not.toContain('registerService: () => undefined');
    expect(source).not.toContain('autoResume:false, autoRotate:false, autoWorkflowCompletion:false');
  });

  it("does not condition core recovery fences on provider mode", () => {
    expect(source).not.toContain('if (authority.reason !== "passthrough") installV099NativeRestartOwnershipFence(api, config);');
    expect(source).not.toContain('if (authority.reason !== "passthrough") installV097DirectRecoveryStartupLiveness(api, config);');
    expect(source).toContain('installV099NativeRestartOwnershipFence(api, config);');
    expect(source).toContain('installV097DirectRecoveryStartupLiveness(api, config);');
  });

  it("keeps providerMode as metadata while removing it from the legacy capability decision", () => {
    expect(source).toContain('providerMode?: "managed" | "passthrough";');
    expect(source).toContain('pluginConfig: {...config, providerMode: undefined}');
  });
});
