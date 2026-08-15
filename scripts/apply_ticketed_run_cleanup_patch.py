#!/usr/bin/env python3
from pathlib import Path

path=Path("plugins/cogentnexus-rotation/src/index.ts")
text=path.read_text(encoding="utf-8")
replacements=[
('''  const runSessions = new Map<string,string>();
  const dispatcherObservedRuns = new Set<string>();
  const deliveryTimers = new Map<string,ReturnType<typeof setTimeout>>();
  const earlyDeliveryReceipts = new Map<string,{success:boolean;error?:string}>();
''','''  const runSessions = new Map<string,string>();
  const ticketedRuns = new Set<string>();
  const dispatcherObservedRuns = new Set<string>();
  const deliveryTimers = new Map<string,ReturnType<typeof setTimeout>>();
  const earlyDeliveryReceipts = new Map<string,{success:boolean;error?:string}>();
''','run ownership'),
('''    runSessions.delete(runId);
    dispatcherObservedRuns.delete(runId);
    earlyDeliveryReceipts.delete(runId);
''','''    runSessions.delete(runId);
    ticketedRuns.delete(runId);
    dispatcherObservedRuns.delete(runId);
    earlyDeliveryReceipts.delete(runId);
''','cleanup'),
('''    if(!target && directResult === "unchanged") {
      earlyDeliveryReceipts.set(runId,{success,error});
      return;
    }
''','''    if(!target && directResult === "unchanged" && ticketedRuns.has(runId)) {
      earlyDeliveryReceipts.set(runId,{success,error});
      return;
    }
''','early receipt'),
('''      acceptedTicket = ticketStore.accept({
        runId:ctx.runId ?? randomUUID(),
        ownerSessionKey,
        prompt:event.prompt,
        maxAttempts:config.ticketMaximumAttempts,
      });
''','''      const ticketRunId=ctx.runId ?? randomUUID();
      acceptedTicket = ticketStore.accept({
        runId:ticketRunId,
        ownerSessionKey,
        prompt:event.prompt,
        maxAttempts:config.ticketMaximumAttempts,
      });
      ticketedRuns.add(ticketRunId);
''','Ticket intake run'),
('        } else if(!visible) cleanupRunDelivery(runId);','        } else if(!visible || directState === "unchanged") cleanupRunDelivery(runId);','agent_end cleanup'),
]
for old,new,label in replacements:
    if old not in text:
        raise SystemExit(f"{label} anchor missing")
    text=text.replace(old,new,1)
path.write_text(text,encoding="utf-8")
print("Ticket-run ownership cleanup patch applied")
