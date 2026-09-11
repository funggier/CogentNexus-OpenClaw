import { mkdtempSync, rmSync } from "node:fs";
import { join } from "node:path";
import { tmpdir } from "node:os";
import { describe, expect, it, vi } from "vitest";
import { TicketStore } from "./ticket-store.js";

const shouldAdvanceSessionGeneration = vi.fn(() => true);

vi.mock("./v095-session-generation.js", () => ({
  shouldAdvanceSessionGeneration,
}));

describe("v0.9.5 session generation wiring", () => {
  it("routes physical session deletion through the canonical generation contract", async () => {
    const v090 = await import("./v090.js");
    v090.patchTicketStore();

    const root = mkdtempSync(join(tmpdir(), "cnx-v090-generation-wiring-"));
    try {
      const path = join(root, "tickets.sqlite3");
      const store = new TicketStore(path);
      store.accept({
        runId: "delete-wire",
        ownerSessionKey: "agent:main:dashboard:wiring",
        prompt: "delete wiring",
      });

      const before = v090.sessionAuthority(path, "agent:main:dashboard:wiring");
      v090.deleteSessionByKey(path, {
        sessionKey: "agent:main:dashboard:wiring",
        message: "delete wiring",
        sessionId: "lifecycle-A",
      });

      expect(shouldAdvanceSessionGeneration).toHaveBeenCalledWith("delete", false);
      expect(v090.sessionAuthority(path, "agent:main:dashboard:wiring").generation)
        .toBe(before.generation + 1);
    } finally {
      rmSync(root, { recursive: true, force: true });
      shouldAdvanceSessionGeneration.mockClear();
    }
  });
});
