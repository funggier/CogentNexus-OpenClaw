import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { describe, expect, it } from "vitest";
import { TicketStore } from "./ticket-store.js";
import { hasLegacyDirectPromotion } from "./v084-entry.js";

describe("v0.8.4 Host reconciliation", () => {
  it("detects only legacy interrupted Tickets whose original intent is Direct", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v084-host-"));
    try {
      const path = join(root, "tickets.sqlite3");
      const store = new TicketStore(path);
      const direct = store.accept({ runId: "direct", ownerSessionKey: "owner", prompt: "สวัสดีครับ" });
      store.route(direct.ticketId, false);
      const db = new DatabaseSync(path);
      db.prepare("UPDATE tickets SET status='waiting',workflow_eligible=1,failure_class='interrupted' WHERE ticket_id=?").run(direct.ticketId);
      db.close();
      expect(hasLegacyDirectPromotion(path)).toBe(true);

      const update = new DatabaseSync(path);
      update.prepare("UPDATE tickets SET status='cancelled' WHERE ticket_id=?").run(direct.ticketId);
      const durable = store.accept({ runId: "durable", ownerSessionKey: "owner", prompt: "PHASE 1\nA\nPHASE 2\nB\nPHASE 3\nC\nทำจนเสร็จและตรวจสอบทุก phase" });
      store.route(durable.ticketId, true);
      update.prepare("UPDATE tickets SET status='waiting',failure_class='interrupted' WHERE ticket_id=?").run(durable.ticketId);
      update.close();
      expect(hasLegacyDirectPromotion(path)).toBe(false);
    } finally {
      rmSync(root, { recursive: true, force: true });
    }
  });
});
