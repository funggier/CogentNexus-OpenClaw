#!/usr/bin/env python3
from pathlib import Path

path=Path("plugins/cogentnexus-rotation/src/index.ts")
text=path.read_text(encoding="utf-8")
old='''  const runSessions = new Map<string,string>();
  const dispatcherObservedRuns = new Set<string>();
  const deliveryTimers = new Map<string,ReturnType<typeof setTimeout>>();
  const earlyDeliveryReceipts = new Map<string,{success:boolean;error?:string}>();
'''
new='''  const runSessions = new Map<string,string>();
  const ticketedRuns = new Set<string>();
  const dispatcherObservedRuns = new Set<string>();
  const deliveryTimers = new Map<string,ReturnType<typeof setTimeout>>();
  const earlyDeliveryReceipts = new Map<string,{success:boolean;error?:string}>();
'''
if old not in text: raise SystemExit("run ownership anchor missing")
text=text.replace(old,new,1)
old='''    runSessions.delete(runId);
    dispatcherObservedRuns.delete(runId);
    earlyDeliveryReceipts.delete(runId);
'''
new='''    runSessions.delete(runId);
    ticketedRuns.delete(runId);
    dispatcherObservedRuns.delete(runId);
    earlyDeliveryReceipts.delete(runId);
'''
if old not in text: raise SystemExit("cleanup anchor missing")
text=text.replace(old,new,1)
old='''    if(!target && directResult === "unchanged") {
      earlyDeliveryReceipts.set(runId,{success,error});
      return;
    }
'''
new='''    if(!target && directResult === "unchanged" && ticketedRuns.has(runId)) {
      earlyDeliveryReceipts.set(runId,{success,error});
      return;
    }
'''
if old not in text: raise SystemExit("early receipt anchor missing")
text=text.replace(old,new,1)
old='''      acceptedTicket = ticketStore.accept({
        runId:ctx.runId ?? randomUUID(),
        ownerSessionKey,
        prompt:event.prompt,
        maxAttempts:config.ticketMaximumAttempts,
      });
'''
new='''      const ticketRunId=ctx.runId ?? randomUUID();
      acceptedTicket = ticketStore.accept({
        runId:ticketRunId,
        ownerSessionKey,
        prompt:event.prompt,
        maxAttempts:config.ticketMaximumAttempts,
      });
      ticketedRuns.add(ticketRunId);
'''
if old not in text: raise SystemExit("Ticket intake run anchor missing")
text=text.replace(old,new,1)
old='''        } else if(directState === "awaiting_delivery" && earlyReceipt){
          earlyDeliveryReceipts.delete(runId);
          settleRunDelivery(runId,earlyReceipt.success,earlyReceipt.error);
        } else if(!visible) cleanupRunDelivery(runId);
'''
new='''        } else if(directState === "awaiting_delivery" && earlyReceipt){
          earlyDeliveryReceipts.delete(runId);
          settleRunDelivery(runId,earlyReceipt.success,earlyReceipt.error);
        } else if(!visible || directState === "unchanged") cleanupRunDelivery(runId);
'''
if old not in text: raise SystemExit("agent_end cleanup anchor missing")
text=text.replace(old,new,1)
path.write_text(text,encoding="utf-8")
print("Ticket-run ownership cleanup patch applied")
