import { DatabaseSync } from "node:sqlite";
import { resolve } from "node:path";
import { classifyDurableRequest } from "./admission.js";
import entry, { prepareV084RecoveryState } from "./v084.js";
import { defaultTicketDatabase, TicketStore } from "./ticket-store.js";

type Config = {
  workspaceDir?: string;
  ticketDatabasePath?: string;
  ticketRecoveryPollMs?: number;
  admissionMinimumScore?: number;
};

const WRAPPED = Symbol.for("cogentnexus-openclaw.v084.entry.host-reconciliation");

export function hasLegacyDirectPromotion(databasePath: string, admissionMinimumScore = 5): boolean {
  new TicketStore(databasePath).snapshot();
  const db = new DatabaseSync(databasePath, { readOnly: true });
  try {
    const rows = db.prepare(`SELECT prompt FROM tickets
      WHERE status IN ('waiting','failed')
        AND workflow_eligible=1
        AND workflow_id IS NULL
        AND failure_class='interrupted'
      ORDER BY created_at
      LIMIT 32`).all() as Array<{ prompt: string }>;
    return rows.some((row) => classifyDurableRequest(row.prompt, admissionMinimumScore).lane === "direct");
  } finally {
    db.close();
  }
}

function wrapEntry() {
  const target = entry as any;
  if (target[WRAPPED]) return;
  Object.defineProperty(target, WRAPPED, { value: true });
  const register = entry.register?.bind(entry);
  entry.register = (api: any) => {
    const config = (api.pluginConfig ?? {}) as Config;
    register?.(api);
    let interval: ReturnType<typeof setInterval> | undefined;
    let active = false;
    api.registerService?.({
      id: "cogentnexus-openclaw-v084-host-reconciliation",
      start: async (ctx: any) => {
        const workspaceDir = resolve(config.workspaceDir ?? ctx.config?.agents?.defaults?.workspace ?? process.cwd());
        const databasePath = resolve(config.ticketDatabasePath ?? defaultTicketDatabase(workspaceDir));
        const tick = () => {
          if (active) return;
          active = true;
          try {
            if (!hasLegacyDirectPromotion(databasePath, config.admissionMinimumScore ?? 5)) return;
            const result = prepareV084RecoveryState(workspaceDir, config);
            if (result.reopened > 0) {
              api.logger.info?.(`CogentNexus-OpenClaw v0.8.4 reconciled ${result.reopened} Host-promoted Direct Ticket(s) back to Direct recovery`);
            }
          } catch (error) {
            api.logger.warn(`CogentNexus-OpenClaw v0.8.4 Host reconciliation failed: ${error instanceof Error ? error.message : String(error)}`);
          } finally {
            active = false;
          }
        };
        tick();
        interval = setInterval(tick, Math.max(1000, Math.min(config.ticketRecoveryPollMs ?? 5000, 30_000)));
        interval.unref?.();
      },
      stop: async () => {
        if (interval) clearInterval(interval);
        interval = undefined;
      },
    });
  };
}

wrapEntry();
export default entry;
