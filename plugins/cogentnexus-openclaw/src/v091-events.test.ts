import { mkdtempSync, readFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { afterEach, describe, expect, it } from "vitest";
import { TicketStore } from "./ticket-store.js";
import { PRE_RUNTIME_FENCE } from "./v090-entry.js";
import { STARTUP_RECOVERY_FENCE } from "./v090-final-entry.js";
import { ACTIVE_WORK_WAKE_MS, installTicketMutationPulses, nextActiveTicketWakeMs } from "./v091-final-entry.js";

const originalQueueMicrotask = globalThis.queueMicrotask;
afterEach(() => { globalThis.queueMicrotask = originalQueueMicrotask; });

describe("v0.9.1 event-driven boundaries", () => {
  it("wakes deadline workers after Ticket COMMIT and adds a durable-dispatch wake only for workflow routing", () => {
    installTicketMutationPulses();
    const root = mkdtempSync(join(tmpdir(), "cnx-v091-route-pulse-"));
    try {
      const callbacks: VoidFunction[] = [];
      globalThis.queueMicrotask = ((callback: VoidFunction) => { callbacks.push(callback); }) as typeof queueMicrotask;
      const store = new TicketStore(join(root, "tickets.sqlite3"));
      const direct = store.accept({ runId:"run-direct", ownerSessionKey:"agent:main:dashboard:test", prompt:"hello" });
      const durable = store.accept({ runId:"run-durable", ownerSessionKey:"agent:main:dashboard:test", prompt:"do durable work" });

      expect(callbacks).toHaveLength(2);
      expect(store.route(direct.ticketId, false)).toBe(true);
      expect(callbacks).toHaveLength(2);

      expect(store.route(durable.ticketId, true)).toBe(true);
      expect(callbacks).toHaveLength(3);
    } finally {
      rmSync(root, { recursive:true, force:true });
    }
  });

  it("uses no active timer at true idle but preserves lease and deadline wakes while work exists", () => {
    expect(nextActiveTicketWakeMs({ linkedRunning:0, durableWorkPending:false, leaseMs:60_000 })).toBeUndefined();
    expect(nextActiveTicketWakeMs({ linkedRunning:0, durableWorkPending:true, leaseMs:60_000 })).toBe(ACTIVE_WORK_WAKE_MS);
    expect(nextActiveTicketWakeMs({ linkedRunning:1, durableWorkPending:true, leaseMs:60_000 })).toBe(20_000);
    expect(nextActiveTicketWakeMs({ linkedRunning:1, durableWorkPending:true, leaseMs:15_000 })).toBe(5_000);
  });

  it("keeps both pre-runtime and crash-start fences explicit across service replacement", () => {
    const pre = async () => undefined;
    const crash = async () => undefined;
    const lower = { id:"service", [PRE_RUNTIME_FENCE]:pre };
    const upper = { ...lower, [STARTUP_RECOVERY_FENCE]:crash };

    expect(upper[PRE_RUNTIME_FENCE]).toBe(pre);
    expect(upper[STARTUP_RECOVERY_FENCE]).toBe(crash);

    const v090Entry = readFileSync(new URL("./v090-entry.ts", import.meta.url), "utf8");
    const v090Final = readFileSync(new URL("./v090-final-entry.ts", import.meta.url), "utf8");
    const v091Final = readFileSync(new URL("./v091-final-entry.ts", import.meta.url), "utf8");
    expect(v090Entry).toContain("[PRE_RUNTIME_FENCE]:ensurePreRuntimeFence");
    expect(v090Final).toContain("[STARTUP_RECOVERY_FENCE]:ensureStartupRecovery");
    expect(v091Final).toContain("service?.[PRE_RUNTIME_FENCE]");
    expect(v091Final).toContain("service?.[STARTUP_RECOVERY_FENCE]");
  });
});
