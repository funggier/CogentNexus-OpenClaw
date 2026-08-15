#!/usr/bin/env python3
from pathlib import Path

path = Path("plugins/cogentnexus-rotation/src/index.ts")
text = path.read_text(encoding="utf-8")

old = '''  const dispatcherObservedRuns = new Set<string>();
  const deliveryTimers = new Map<string,ReturnType<typeof setTimeout>>();
  const settleRunDelivery = (runId:string,success:boolean,error?:string) => {
    const timer=deliveryTimers.get(runId); if(timer){clearTimeout(timer);deliveryTimers.delete(runId);}
    const workspaceDir=resolve(runWorkspaces.get(runId) ?? config.workspaceDir ?? process.cwd());
    const store=new TicketStore(config.ticketDatabasePath ?? defaultTicketDatabase(workspaceDir));
    if(success) store.confirmDirectDelivery({runId}); else store.failDirectDelivery({runId,message:error});
    const target=deliveryTargets.get(runId);
    if(target) settleDeliveryTarget({workspaceDir,store,target,success,error});
    deliveryTargets.delete(runId); runWorkspaces.delete(runId); runSessions.delete(runId); dispatcherObservedRuns.delete(runId);
  };
'''
new = '''  const dispatcherObservedRuns = new Set<string>();
  const deliveryTimers = new Map<string,ReturnType<typeof setTimeout>>();
  const earlyDeliveryReceipts = new Map<string,{success:boolean;error?:string}>();
  const cleanupRunDelivery = (runId:string) => {
    deliveryTargets.delete(runId);
    runWorkspaces.delete(runId);
    runSessions.delete(runId);
    dispatcherObservedRuns.delete(runId);
    earlyDeliveryReceipts.delete(runId);
  };
  const settleRunDelivery = (runId:string,success:boolean,error?:string) => {
    const timer=deliveryTimers.get(runId); if(timer){clearTimeout(timer);deliveryTimers.delete(runId);}
    const workspaceDir=resolve(runWorkspaces.get(runId) ?? config.workspaceDir ?? process.cwd());
    const store=new TicketStore(config.ticketDatabasePath ?? defaultTicketDatabase(workspaceDir));
    const target=deliveryTargets.get(runId);
    const directResult=success ? store.confirmDirectDelivery({runId}) : store.failDirectDelivery({runId,message:error});
    if(target) settleDeliveryTarget({workspaceDir,store,target,success,error});
    if(!target && directResult === "unchanged") {
      earlyDeliveryReceipts.set(runId,{success,error});
      return;
    }
    cleanupRunDelivery(runId);
  };
'''
if old not in text:
    raise SystemExit("delivery coordinator anchor missing")
text = text.replace(old,new,1)

old2 = '''        const visible=hasVisibleAssistantOutput(event.messages);
        store.finalizeDirectRun({runId,success:event.success,interrupted:isResumableInterruption(event.success,event.error),message:event.error??"",expectsDelivery:visible});
        if(!event.success){
          const timer=deliveryTimers.get(runId);if(timer)clearTimeout(timer);deliveryTimers.delete(runId);
          if(internalDelivery)settleRunDelivery(runId,false,event.error??"delivery run interrupted");
        } else if(internalDelivery && !visible) settleRunDelivery(runId,false,"delivery continuation produced no visible assistant output");
        else if(!visible){runWorkspaces.delete(runId);runSessions.delete(runId);}
'''
new2 = '''        const visible=hasVisibleAssistantOutput(event.messages);
        const directState=store.finalizeDirectRun({runId,success:event.success,interrupted:isResumableInterruption(event.success,event.error),message:event.error??"",expectsDelivery:visible});
        const earlyReceipt=earlyDeliveryReceipts.get(runId);
        if(!event.success){
          const timer=deliveryTimers.get(runId);if(timer)clearTimeout(timer);deliveryTimers.delete(runId);
          earlyDeliveryReceipts.delete(runId);
          if(internalDelivery)settleRunDelivery(runId,false,event.error??"delivery run interrupted");
          else cleanupRunDelivery(runId);
        } else if(internalDelivery && !visible) settleRunDelivery(runId,false,"delivery continuation produced no visible assistant output");
        else if(directState === "awaiting_delivery" && earlyReceipt){
          earlyDeliveryReceipts.delete(runId);
          settleRunDelivery(runId,earlyReceipt.success,earlyReceipt.error);
        } else if(!visible) cleanupRunDelivery(runId);
'''
if old2 not in text:
    raise SystemExit("agent_end delivery anchor missing")
text = text.replace(old2,new2,1)
path.write_text(text,encoding="utf-8")
print("early delivery receipt buffer patch applied")
