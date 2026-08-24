import { readFileSync } from "node:fs";
import { describe, expect, it } from "vitest";

describe("v0.9.7 release wiring", () => {
  it("registers the Direct Recovery startup liveness bridge after the legacy event services", () => {
    const source = readFileSync(new URL("./v091-release-entry.ts", import.meta.url), "utf8");
    expect(source).toContain('from "./v097-direct-recovery-liveness.js"');
    expect(source).toContain("installV097DirectRecoveryStartupLiveness(api, config)");
    expect(source.indexOf("const registered = register(api)")).toBeLessThan(
      source.indexOf("installV097DirectRecoveryStartupLiveness(api, config)"),
    );
  });

  it("keeps startup liveness event-driven instead of adding setInterval polling", () => {
    const source = readFileSync(new URL("./v097-direct-recovery-liveness.ts", import.meta.url), "utf8");
    expect(source).not.toContain("setInterval(");
    expect(source).toContain("setTimeout(check");
    expect(source).toContain("r.state='pending'");
    expect(source).toContain("s.generation=r.owner_generation");
    expect(source).toContain("m.state IN ('active','recovering')");
  });
});
