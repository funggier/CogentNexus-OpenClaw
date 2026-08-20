import { describe, expect, it } from "vitest";
import { launchV093DirectRecovery } from "./v093-direct-recovery.js";
import { launchV094DirectRecovery } from "./v094-direct-recovery.js";

describe("v0.9.3 Direct Recovery compatibility boundary", () => {
  it("routes the already-wired v0.9.3 service entry through the v0.9.4 embedded executor", () => {
    expect(launchV093DirectRecovery).toBe(launchV094DirectRecovery);
  });
});
