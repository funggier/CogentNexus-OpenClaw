import { TicketStore, type TicketLease } from "./ticket-store.js";
import { installTicketAdmissionContentionRetry } from "./v198-ticket-admission-contention.js";

installTicketAdmissionContentionRetry();

export type TicketLaunch = (lease: TicketLease) => void;
export type TicketAdmission = (candidate: {ticketId:string;attemptCount:number;maxAttempts:number}) => boolean;

export class TicketDispatcher {
  constructor(private readonly store: TicketStore, private readonly workerPrefix = "ticket-worker") {}

  dispatch(input: { limit: number; leaseMs: number; launch: TicketLaunch; admit?: TicketAdmission; now?: Date }): TicketLease[] {
    const limit = Number.isFinite(input.limit) ? Math.max(0,Math.min(Math.trunc(input.limit),32)) : 0;
    const claimed: TicketLease[] = [];
    if (limit === 0) return claimed;
    for (const candidate of this.store.ready(limit)) {
      if (input.admit && !input.admit(candidate)) break;
      const lease = this.store.claim({ticketId:candidate.ticketId,workerId:`${this.workerPrefix}-${candidate.ticketId}`,leaseMs:input.leaseMs,now:input.now});
      if (!lease) continue;
      try {
        input.launch(lease);
        claimed.push(lease);
      } catch (error) {
        this.store.failAttempt({...lease,classification:"transient",message:error instanceof Error ? error.message : String(error),now:input.now});
      }
    }
    return claimed;
  }
}
