import { TicketStore } from "./ticket-store.js";

const TICKET_ADMISSION_CONTENTION_PATCH = Symbol.for(
  "cogentnexus-openclaw.v198.ticket-admission-contention",
);

type SqliteErrorShape = {
  code?: unknown;
  errcode?: unknown;
  errstr?: unknown;
  message?: unknown;
};

export function isTransientSqliteWriterContention(error: unknown): boolean {
  if (!error || typeof error !== "object") return false;
  const sqlite = error as SqliteErrorShape;
  if (Number(sqlite.errcode) !== 5) return false;
  const detail = `${String(sqlite.errstr ?? "")} ${String(sqlite.message ?? "")}`;
  return sqlite.code === "ERR_SQLITE_ERROR" && /database is (?:locked|busy)/iu.test(detail);
}

/**
 * A fresh human turn is admitted inside OpenClaw's 30-second fail-closed
 * before_agent_run boundary. Session reset/delete bookkeeping can briefly own
 * SQLite's writer lock. The base TicketStore wait is five seconds; if that
 * exact transient SQLITE_BUSY condition expires at the boundary, retry the
 * idempotent Ticket accept once. The second call retains TicketStore's normal
 * five-second bound, so persistent contention still fails closed rather than
 * bypassing Ticket-first durability.
 */
export function installTicketAdmissionContentionRetry(): void {
  const prototype = TicketStore.prototype as any;
  if (prototype[TICKET_ADMISSION_CONTENTION_PATCH]) return;
  Object.defineProperty(prototype, TICKET_ADMISSION_CONTENTION_PATCH, { value: true });

  const accept = TicketStore.prototype.accept;
  TicketStore.prototype.accept = function(
    this: TicketStore,
    input: Parameters<TicketStore["accept"]>[0],
  ): ReturnType<TicketStore["accept"]> {
    try {
      return accept.call(this, input);
    } catch (error) {
      if (!isTransientSqliteWriterContention(error)) throw error;
      return accept.call(this, input);
    }
  };
}
