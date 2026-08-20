import { describe, expect, it } from "vitest";
import { launchV093DirectRecovery } from "./v093-direct-recovery.js";
import { launchV096DirectRecovery } from "./v096-direct-recovery.js";

describe("v0.9.3 Direct Recovery compatibility boundary", () => {
  it("routes the already-wired v0.9.3 service entry through the v0.9.6 internal-admission executor", () => {
    expect(launchV093DirectRecovery).toBe(launchV096DirectRecovery);
  });
});
