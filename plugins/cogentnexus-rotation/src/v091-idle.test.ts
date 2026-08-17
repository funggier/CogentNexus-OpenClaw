import { describe, expect, it } from "vitest";
import { ACTIVE_RECONCILE_MS, DEEP_RECONCILE_MS, IDLE_RECONCILE_MS, managedIdleConfig } from "./v091-final-entry.js";

describe("v0.9 release idle quiescence", () => {
  it("raises managed polling floors away from the 5 second hot loop", () => {
    const config = managedIdleConfig({
      ticketFirst: true,
      enforcedMode: true,
      ticketRecoveryPollMs: 5000,
      ticketOutboxPollMs: 5000,
      ticketDispatchPollMs: 5000,
      completionPollMs: 5000,
      contextMaintenancePollMs: 3000,
    });
    expect(config.ticketRecoveryPollMs).toBe(60_000);
    expect(config.ticketOutboxPollMs).toBe(60_000);
    expect(config.ticketDispatchPollMs).toBe(60_000);
    expect(config.completionPollMs).toBe(60_000);
    expect(config.contextMaintenancePollMs).toBe(30_000);
  });

  it("does not rewrite standalone/non-managed plugin timing", () => {
    const original = { ticketFirst: true, enforcedMode: false, ticketRecoveryPollMs: 5000 };
    expect(managedIdleConfig(original)).toBe(original);
  });

  it("uses bounded active recovery and a much longer idle cadence", () => {
    expect(ACTIVE_RECONCILE_MS).toBeGreaterThanOrEqual(15_000);
    expect(IDLE_RECONCILE_MS).toBeGreaterThanOrEqual(120_000);
    expect(DEEP_RECONCILE_MS).toBeGreaterThanOrEqual(10 * 60_000);
    expect(IDLE_RECONCILE_MS).toBeGreaterThan(ACTIVE_RECONCILE_MS);
  });
});
