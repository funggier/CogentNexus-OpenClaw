import { afterEach, describe, expect, it, vi } from "vitest";
import { existsSync, mkdtempSync, mkdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { spawn, spawnSync } from "node:child_process";
import entry, { activeWorkflowForRequest, autoResumeTag, completionMessage, deliverTicketOutbox, deliverWorkflowCompletion, dispatchTicketWorkflows, durableAdmissionEligible, enforcementDecision, isResumableInterruption, pendingWorkflowCompletions, reconcileTicketWorkflows, rotationCandidates, rotationIdentity, scheduleInterruptedResume, ticketOutboxTag, ticketResourceAdmission, workflowCompletionTag } from "./index.js";
import { classifyDurableRequest, compileDurableIntake, durableRequestFingerprint } from "./admission.js";
import { assessSession, selectActiveDescendant } from "./context-guard.js";
import { getToolPluginMetadata } from "openclaw/plugin-sdk/tool-plugin";
import { TicketStore } from "./ticket-store.js";

afterEach(() => vi.useRealTimers());

describe("cogentnexus-rotation", () => {
  it("admits an explicit multi-phase request before inference", () => {
    const prompt = `ทำงานจนเสร็จ ห้ามข้าม phase และต้องตรวจสอบ dependency\n\nPHASE 1\nออกแบบระบบ\n\nPHASE 2\nสร้างอย่างน้อย 40 services\n\nPHASE 3\nสร้างอย่างน้อย 30 tables`;
    const decision = classifyDurableRequest(prompt);
    expect(decision.lane).toBe("durable");
    expect(decision.sections).toHaveLength(3);
    expect(decision.reasons).toContain("explicit-components:3");
  });

  it("does not capture simple or internal continuation turns", () => {
    expect(classifyDurableRequest("ช่วยอธิบายคำว่า cache").lane).toBe("direct");
    expect(classifyDurableRequest("CogentNexus workflow X reached terminal status completed.").lane).toBe("direct");
    expect(classifyDurableRequest("#cogent-direct PHASE 1\nA\nPHASE 2\nB\nPHASE 3\nC").lane).toBe("direct");
  });

  it("admits the Thai multi-artifact Chiang Mai regression request", () => {
    const prompt="ช่วยสร้างแผนเที่ยวเชียงใหม่ โดยทำไฟล์ plan.md, budget.csv และ README.md ให้ยอดรวมไม่เกินงบ 5,000 บาท และตรวจสอบความสอดคล้องของตัวเลขทุกไฟล์";
    const decision=classifyDurableRequest(prompt);
    expect(decision.lane).toBe("durable");
    expect(decision.reasons).toContain("named-artifacts:3");
    expect(decision.reasons).toContain("cross-artifact-budget-validation");
  });

  it("admits owner WebChat dispatches without depending on channel-specific trigger names", () => {
    expect(durableAdmissionEligible({sessionKey:"agent:main:dashboard:test",senderIsOwner:true})).toBe(true);
    expect(durableAdmissionEligible({sessionKey:"agent:main:dashboard:test"})).toBe(true);
    expect(durableAdmissionEligible({sessionKey:"agent:main:subagent:test",senderIsOwner:true})).toBe(false);
    expect(durableAdmissionEligible({sessionKey:"agent:main:dashboard:test",senderIsOwner:false})).toBe(true);
    expect(durableAdmissionEligible({sessionKey:"agent:main:cli:test",senderIsOwner:false})).toBe(false);
  });

  it("compiles a bounded owner-startable manifest without invoking a model", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-admission-"));
    const prompt = `PHASE 1\nDesign\nPHASE 2\nBuild\nPHASE 3\nVerify`;
    const request = `${prompt}\nDo this until complete with validators and at least 3 artifacts.`;
    const decision = classifyDurableRequest(request);
    const intake = compileDurableIntake({workspaceDir:root,prompt:request,runId:"run/one",decision,model:"qwen3.5:9b-32k"});
    const manifest = JSON.parse(readFileSync(join(root, intake.manifestPath), "utf8"));
    expect(manifest.taskId).toBe("CNX-AUTO-run-one");
    expect(manifest.steps.map((step:any)=>step.id)).toEqual(["component-01","component-02","component-03","assemble"]);
    expect(manifest.steps[0].executor.includeFiles).toEqual([`.cogent/intake/${manifest.taskId}/request.txt`]);
    expect(manifest.steps[0].executor.timeoutSeconds).toBe(1800);
    expect(manifest.steps[0].executor.inactivityTimeoutSeconds).toBe(180);
    expect(manifest.admission.requestHash).toBe(durableRequestFingerprint(request));
    expect(manifest.steps.at(-1).executor.type).toBe("concat");
  });

  it("compiles arbitrary named artifacts with an external format validator", () => {
    const root=mkdtempSync(join(tmpdir(),"cnx-artifact-intake-"));
    try {
      const prompt="สร้าง plan.md, budget.csv, README.md สำหรับเชียงใหม่ งบไม่เกิน 5,000 บาท และตรวจสอบความสอดคล้อง";
      const intake=compileDurableIntake({workspaceDir:root,prompt,runId:"thai-travel",decision:classifyDurableRequest(prompt),model:"fixture"});
      const manifest=JSON.parse(readFileSync(join(root,intake.manifestPath),"utf8"));
      expect(manifest.steps.map((step:any)=>step.id)).toEqual(["artifact-01","artifact-02","artifact-03","validate-artifacts"]);
      expect(manifest.steps.at(-1).validator.argv[1]).toMatch(/validate_artifacts\.py$/);
      expect(manifest.steps.slice(0,3).map((step:any)=>step.outputs[0])).toEqual(["plan.md","budget.csv","README.md"]);
      writeFileSync(join(root,"plan.md"),"# Plan\nA complete Chiang Mai itinerary with transport and meals.\n");
      writeFileSync(join(root,"budget.csv"),"item,category,amount\ntransport,travel,1000\nfood,meal,500\n");
      writeFileSync(join(root,"README.md"),"# Overview\nSee plan.md and budget.csv. Total: 1,500 THB; remaining: 3,500 THB.\n");
      const validation=spawnSync("python",manifest.steps.at(-1).validator.argv.slice(1),{cwd:root,encoding:"utf8"});
      expect(validation.status,validation.stderr).toBe(0);
      expect(validation.stdout).toContain("validated artifacts=3");
    } finally { rmSync(root,{recursive:true,force:true}); }
  });

  it.each([
    ["software","ช่วยพัฒนาระบบ API และทดสอบ integration ให้ครบ"],
    ["trading","สร้าง EA Trader สำหรับ MetaTrader พร้อม backtest และตรวจ risk limits"],
    ["files","จัดการไฟล์หลายไฟล์และตรวจสอบความครบถ้วนทั้งหมด"],
    ["analysis","วิเคราะห์ข้อมูลหลายขั้นให้ครบถ้วนและตรวจสอบผลลัพธ์"],
    ["fiction","เขียนนิยายทั้งเล่มและตรวจ continuity ตัวละคร"],
    ["design","ออกแบบ UI ทั้งระบบหลายหน้าจอพร้อม accessibility review"],
    ["translation","แปลภาษาทั้งเล่มให้ครบถ้วนและตรวจคำศัพท์เฉพาะ"],
  ] as const)("detects the %s work domain",(domain,prompt)=>{
    const decision=classifyDurableRequest(prompt);
    expect(decision.domain).toBe(domain);
    expect(decision.lane).toBe("durable");
  });

  it("prioritizes translation when translated material also mentions analysis data",()=>{
    const decision=classifyDurableRequest("แปลเอกสารวิเคราะห์ข้อมูลทั้งชุดให้ครบถ้วนเป็นภาษาอังกฤษ");
    expect(decision.domain).toBe("translation");
    expect(decision.lane).toBe("durable");
  });

  it("uses translation-specific durable components",()=>{
    const root=mkdtempSync(join(tmpdir(),"cnx-translation-intake-"));
    try {
      const prompt="ช่วยแปลภาษาทั้งเล่มให้ครบถ้วนและตรวจคำศัพท์เฉพาะ";
      const intake=compileDurableIntake({workspaceDir:root,prompt,runId:"translation",decision:classifyDurableRequest(prompt),model:"fixture"});
      const manifest=JSON.parse(readFileSync(join(root,intake.manifestPath),"utf8"));
      expect(manifest.domain).toBe("translation");
      expect(manifest.steps.map((step:any)=>step.id)).toEqual(["translation-brief","translate","bilingual-qa","assemble"]);
    } finally { rmSync(root,{recursive:true,force:true}); }
  });

  it("deduplicates the same active durable request across owner sessions", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-dedup-"));
    const hash = durableRequestFingerprint("same durable request");
    const flow = join(root, ".cogent", "workflows", "WF-ACTIVE");
    mkdirSync(flow, { recursive: true });
    writeFileSync(join(flow, "manifest.json"), JSON.stringify({admission:{requestHash:hash}}));
    writeFileSync(join(flow, "state.json"), JSON.stringify({status:"running",controllerPid:123}));
    expect(activeWorkflowForRequest(root, hash)).toEqual({taskId:"WF-ACTIVE",status:"running",controllerPid:123});
    rmSync(root, { recursive: true, force: true });
  });

  it("declares the rotation tool", () => {
    expect(getToolPluginMetadata(entry)?.tools.map((tool) => tool.name)).toEqual(["cogent_rotation", "cogent_workflow_start", "cogent_ticket_status", "cogent_knowledge"]);
  });

  it("uses a deterministic generation-fenced identity", () => {
    expect(rotationIdentity("CNX-PHASE4-001", 3)).toEqual({
      runId: "cogent-rotate-cnx-phase4-001-3",
      childSessionKey: "agent:main:cogent-rotate-cnx-phase4-001-3",
    });
  });

  it("blocks conversational unbound workflow creation but permits the trusted start tool", () => {
    const direct = enforcementDecision("shell_command", {command:"python workflow.py init manifest.json --operator-unbound"}, "agent:main:owner");
    expect(direct.block).toBe(true);
    expect(enforcementDecision("cogent_workflow_start", {manifestPath:"manifest.json"}, "agent:main:owner").block).toBe(false);
    expect(enforcementDecision("shell_command", {command:"python workflow.py init manifest.json --operator-unbound"}, undefined).block).toBe(false);
    expect(enforcementDecision("openclaw__skill_workshop", {proposal_content:"document workflow.py init behavior"}, "agent:main:owner").block).toBe(false);
  });

  it("selects only verified rotation observations for the current owner session", () => {
    const output = JSON.stringify({ observations: [
      { taskId: "T1", sessionKey: "owner", status: "observed", rotationRequired: true },
      { taskId: "T2", sessionKey: "other", status: "observed", rotationRequired: true },
      { taskId: "T3", sessionKey: "owner", status: "observed", rotationRequired: false },
    ] });
    expect(rotationCandidates(output, "owner")).toEqual(["T1"]);
  });

  it("rotates before token pressure when the raw transcript is large", () => {
    expect(assessSession({
      key: "old",
      totalTokens: 128231,
      totalTokensFresh: true,
      contextTokens: 372000,
      transcriptBytes: 7_973_463,
    }).action).toBe("ROTATE");
  });

  it("rotates immediately after context overflow or repeated compaction", () => {
    expect(assessSession({ key: "s", contextLengthExceeded: true }).action).toBe("ROTATE");
    expect(assessSession({ key: "s", compactionCount: 2 }).action).toBe("ROTATE");
  });

  it("follows the newest running descendant instead of a completed binding", () => {
    const selected = selectActiveDescendant("owner", [
      { key: "owner", status: "done", updatedAt: 1 },
      { key: "child-1", parentSessionKey: "owner", status: "done", updatedAt: 2 },
      { key: "child-2", parentSessionKey: "child-1", status: "running", updatedAt: 3 },
    ]);
    expect(selected?.key).toBe("child-2");
  });

  it("classifies only resumable terminal failures", () => {
    expect(isResumableInterruption(false, "CLI transcript compaction failed: context_length_exceeded")).toBe(true);
    expect(isResumableInterruption(false, "Interrupted while waiting on model work")).toBe(true);
    expect(isResumableInterruption(true, "Interrupted")).toBe(false);
    expect(isResumableInterruption(false, "permission denied")).toBe(false);
  });

  it("builds a scheduler-safe deterministic resume tag", () => {
    expect(autoResumeTag("run:abc/123")).toBe("cogent-resume-run-abc-123");
  });

  it("schedules exactly one continuation turn for an interrupted run", async () => {
    const unscheduled: unknown[] = [];
    const scheduled: Array<Record<string, unknown>> = [];
    const scheduledRuns = new Set<string>();
    const workflow = {
      async unscheduleSessionTurnsByTag(input: unknown) { unscheduled.push(input); },
      async scheduleSessionTurn(input: Record<string, unknown>) { scheduled.push(input); },
    };
    const input = {
      success: false,
      error: "Interrupted while waiting on model work",
      runId: "run:fixture/1",
      sessionKey: "agent:main:fixture",
      workflow,
      scheduledRuns,
    };
    await expect(scheduleInterruptedResume(input)).resolves.toBe(true);
    await expect(scheduleInterruptedResume(input)).resolves.toBe(false);
    expect(unscheduled).toHaveLength(1);
    expect(scheduled).toHaveLength(1);
    expect(scheduled[0]).toMatchObject({
      sessionKey: "agent:main:fixture",
      deleteAfterRun: true,
      deliveryMode: "announce",
      tag: "cogent-resume-run-fixture-1",
    });
  });

  it("discovers only pending terminal workflow outboxes", () => {
    const root = mkdtempSync(join(tmpdir(), "cogent-completion-"));
    try {
      const base = join(root, ".cogent", "workflows", "WF-1");
      mkdirSync(base, { recursive: true });
      const notice = {schemaVersion:1,taskId:"WF-1",ownerSessionKey:"agent:main:owner",workflowStatus:"completed",stateRevision:7,createdAt:new Date().toISOString(),deliveryStatus:"pending"};
      writeFileSync(join(base,"completion.json"), JSON.stringify(notice));
      const found = pendingWorkflowCompletions(root);
      expect(found).toHaveLength(1);
      expect(workflowCompletionTag(found[0].notice)).toBe("cogent-workflow-result-WF-1-7");
      expect(completionMessage(found[0].notice)).toContain("terminal status completed");
    } finally { rmSync(root, { recursive:true, force:true }); }
  });

  it("finishes TaskFlow, schedules the owner once by tag, and commits delivery", async () => {
    const root = mkdtempSync(join(tmpdir(), "cogent-delivery-"));
    try {
      const path = join(root,"completion.json");
      const notice = {schemaVersion:1,taskId:"WF-2",ownerSessionKey:"agent:main:owner",workflowStatus:"completed",stateRevision:9,createdAt:new Date().toISOString(),deliveryStatus:"pending"};
      writeFileSync(path, JSON.stringify(notice));
      const scheduled: any[] = [], finished: any[] = [];
      const flow = {flowId:"flow-1",syncMode:"managed",revision:1};
      const taskFlow = {list:()=>[],createManaged:()=>flow,get:()=>flow,finish:(value:any)=>finished.push(value),fail:()=>{ throw new Error("unexpected fail"); }};
      const api = {runtime:{tasks:{managedFlows:{bindSession:()=>taskFlow}}},session:{workflow:{unscheduleSessionTurnsByTag:async()=>{},scheduleSessionTurn:async(value:any)=>scheduled.push(value)}}};
      await deliverWorkflowCompletion(api,path,notice);
      expect(finished).toHaveLength(1);
      expect(scheduled[0]).toMatchObject({sessionKey:"agent:main:owner",tag:"cogent-workflow-result-WF-2-9",deliveryMode:"announce"});
      expect(JSON.parse(readFileSync(path,"utf8")).deliveryStatus).toBe("delivered");
      expect(JSON.parse(readFileSync(path,"utf8")).deliveryAttempts).toBe(1);
    } finally { rmSync(root, { recursive:true, force:true }); }
  });

  it("keeps failed completion delivery pending with durable retry evidence", async () => {
    const root = mkdtempSync(join(tmpdir(), "cogent-delivery-retry-"));
    try {
      const path = join(root,"completion.json");
      const notice = {schemaVersion:1,taskId:"WF-3",ownerSessionKey:"agent:main:owner",workflowStatus:"completed",stateRevision:2,createdAt:new Date().toISOString(),deliveryStatus:"pending"};
      writeFileSync(path, JSON.stringify(notice));
      const flow = {flowId:"flow-1",syncMode:"managed",revision:1};
      const taskFlow = {list:()=>[],createManaged:()=>flow,get:()=>flow,finish:()=>{},fail:()=>{}};
      const api = {runtime:{tasks:{managedFlows:{bindSession:()=>taskFlow}}},session:{workflow:{unscheduleSessionTurnsByTag:async()=>{},scheduleSessionTurn:async()=>{throw new Error("gateway unavailable");}}}};
      await expect(deliverWorkflowCompletion(api,path,notice)).rejects.toThrow("gateway unavailable");
      const saved = JSON.parse(readFileSync(path,"utf8"));
      expect(saved).toMatchObject({deliveryStatus:"pending",deliveryAttempts:1,lastDeliveryError:"gateway unavailable"});
    } finally { rmSync(root, { recursive:true, force:true }); }
  });

  it("delivers a terminal Ticket outbox idempotently to its owner", async () => {
    const root = mkdtempSync(join(tmpdir(),"cogent-ticket-delivery-"));
    try {
      const store = new TicketStore(join(root,"tickets.sqlite3"));
      const ticket = store.accept({runId:"delivery",ownerSessionKey:"agent:main:owner",prompt:"work"});
      const lease = store.claim({ticketId:ticket.ticketId,workerId:"worker",leaseMs:5000})!;
      store.complete({...lease,result:{ok:true}});
      const item = store.pendingOutbox()[0];
      const scheduled:any[] = [];
      const api = {session:{workflow:{
        unscheduleSessionTurnsByTag:async()=>{},
        scheduleSessionTurn:async(value:any)=>scheduled.push(value),
      }}};
      await deliverTicketOutbox(api,store,item);
      expect(ticketOutboxTag(item)).toBe(`cogent-ticket-result-${ticket.ticketId}`);
      expect(scheduled[0]).toMatchObject({sessionKey:"agent:main:owner",tag:ticketOutboxTag(item),deliveryMode:"announce"});
      expect(store.pendingOutbox()).toEqual([]);
      await deliverTicketOutbox(api,store,item);
      expect(store.pendingOutbox()).toEqual([]);
    } finally { rmSync(root,{recursive:true,force:true}); }
  });

  it("keeps failed Ticket delivery pending with persistent attempt and error evidence", async () => {
    const root = mkdtempSync(join(tmpdir(),"cogent-ticket-delivery-retry-"));
    try {
      const path = join(root,"tickets.sqlite3");
      const store = new TicketStore(path);
      const ticket = store.accept({runId:"delivery-retry",ownerSessionKey:"agent:main:owner",prompt:"work"});
      const lease = store.claim({ticketId:ticket.ticketId,workerId:"worker",leaseMs:5000})!;
      store.complete({...lease,result:{ok:true}});
      const item = store.pendingOutbox()[0];
      const api = {session:{workflow:{
        unscheduleSessionTurnsByTag:async()=>{},
        scheduleSessionTurn:async()=>{throw new Error("gateway unavailable");},
      }}};
      await expect(deliverTicketOutbox(api,store,item)).rejects.toThrow("gateway unavailable");
      expect(store.pendingOutbox()[0]).toMatchObject({outboxId:item.outboxId,deliveryAttempts:1});
      const db = new DatabaseSync(path,{readOnly:true});
      expect(db.prepare("SELECT delivery_status,delivery_attempts,last_delivery_error FROM ticket_outbox WHERE outbox_id=?").get(item.outboxId))
        .toEqual({delivery_status:"pending",delivery_attempts:1,last_delivery_error:"gateway unavailable"});
      db.close();
    } finally { rmSync(root,{recursive:true,force:true}); }
  });

  it("registers the opt-in Ticket recovery service and reclaims an expired lease on start", async () => {
    vi.useFakeTimers();
    vi.setSystemTime(new Date("2026-08-13T00:00:02.000Z"));
    const root = mkdtempSync(join(tmpdir(),"cogent-ticket-recovery-"));
    try {
      const databasePath = join(root,"tickets.sqlite3");
      const store = new TicketStore(databasePath);
      const ticket = store.accept({runId:"recovery-service",ownerSessionKey:"agent:main:owner",prompt:"work"});
      store.route(ticket.ticketId,true);
      store.claim({ticketId:ticket.ticketId,workerId:"worker-a",leaseMs:1000,now:new Date("2026-08-13T00:00:00.000Z")});

      const services:any[] = [];
      const warnings:string[] = [];
      const api:any = {
        pluginConfig:{ticketFirst:true,ticketDatabasePath:databasePath,autoWorkflowCompletion:false},
        registerTool:()=>{},
        registerService:(service:any)=>services.push(service),
        on:()=>{},
        logger:{warn:(message:string)=>warnings.push(message),error:()=>{}},
        session:{workflow:{}},
        runtime:{tasks:{managedFlows:{}}},
      };
      entry.register?.(api);
      expect(services.map(service=>service.id)).toEqual(["cogentnexus-ticket-recovery"]);

      await services[0].start({config:{agents:{defaults:{workspace:root}}}});
      expect(store.snapshot().tickets.waiting).toBe(1);
      expect(warnings.some(message=>message.includes(`recovered expired Ticket ${ticket.ticketId}`))).toBe(true);
      await services[0].stop();
      expect(vi.getTimerCount()).toBe(0);
    } finally { rmSync(root,{recursive:true,force:true}); }
  });

  it("defers Ticket dispatch before claim when resource admission fails", () => {
    const root = mkdtempSync(join(tmpdir(),"cogent-ticket-resource-"));
    try {
      const store = new TicketStore(join(root,"tickets.sqlite3"));
      const ticket = store.accept({runId:"resource",ownerSessionKey:"owner",prompt:"PHASE 1\nA\nPHASE 2\nB\nPHASE 3\nC"});
      store.route(ticket.ticketId,true);
      expect(ticketResourceAdmission({freeMemoryBytes:1,freeDiskBytes:1,running:0},{} as any)).toMatchObject({admitted:false,reasons:["memory","disk"]});
      const result = dispatchTicketWorkflows({workspaceDir:root,store,config:{} as any,snapshot:{freeMemoryBytes:1,freeDiskBytes:1,running:0}});
      expect(result.leases).toEqual([]);
      expect(store.snapshot().tickets.accepted).toBe(1);
    } finally { rmSync(root,{recursive:true,force:true}); }
  });

  it("commits and routes a durable Ticket before returning the queued inference gate", async () => {
    const root = mkdtempSync(join(tmpdir(),"cogent-ticket-gate-"));
    try {
      const databasePath = join(root,"tickets.sqlite3");
      const hooks = new Map<string,any>();
      const api:any = {pluginConfig:{ticketFirst:true,ticketDatabasePath:databasePath,autoWorkflowCompletion:false},registerTool:()=>{},registerService:()=>{},
        on:(name:string,callback:any)=>hooks.set(name,callback),logger:{warn:()=>{},error:()=>{},info:()=>{}},session:{workflow:{}},runtime:{tasks:{managedFlows:{}}}};
      entry.register?.(api);
      const prompt = "PHASE 1\nA\nPHASE 2\nB\nPHASE 3\nC";
      const decision = await hooks.get("before_agent_run")({prompt,senderIsOwner:true},{sessionKey:"agent:main:owner",runId:"gate-run",workspaceDir:root});
      expect(decision).toMatchObject({outcome:"block",category:"cogentnexus_ticket_admission"});
      const store = new TicketStore(databasePath);
      expect(store.ready()).toHaveLength(1);
      expect(existsSync(join(root,".cogent","intake"))).toBe(false);
    } finally { rmSync(root,{recursive:true,force:true}); }
  });

  it("compiles, starts, links, heartbeats, and completes an admitted Ticket workflow", () => {
    const root = mkdtempSync(join(tmpdir(),"cogent-ticket-bridge-"));
    try {
      const store = new TicketStore(join(root,"tickets.sqlite3"));
      const prompt = "PHASE 1\nA\nPHASE 2\nB\nPHASE 3\nC";
      const ticket = store.accept({runId:"bridge",ownerSessionKey:"agent:main:owner",prompt});
      store.route(ticket.ticketId,true);
      const compiled:any[] = [], started:any[] = [];
      const now = new Date("2026-08-13T00:00:00.000Z");
      const result = dispatchTicketWorkflows({workspaceDir:root,store,config:{ticketLeaseMs:5000} as any,now,
        snapshot:{freeMemoryBytes:2**30,freeDiskBytes:2**30,running:0},
        compile:(input:any)=>{compiled.push(input);return {taskId:"WF-BRIDGE",manifestPath:".cogent/intake/WF-BRIDGE/manifest.json",componentCount:3,assembledOutput:"out",requestHash:"hash"};},
        start:(input:any)=>{started.push(input);return {taskId:"WF-BRIDGE",status:"started",controllerPid:123,ownerBound:true,idempotentReplay:false};},
      });
      expect(result.leases).toHaveLength(1);
      expect(compiled[0]).toMatchObject({runId:"bridge",prompt});
      expect(started[0]).toMatchObject({ownerSessionKey:"agent:main:owner",manifestPath:".cogent/intake/WF-BRIDGE/manifest.json"});
      expect(store.get(ticket.ticketId)).toMatchObject({workflowId:"WF-BRIDGE",manifestPath:".cogent/intake/WF-BRIDGE/manifest.json"});

      const workflow = join(root,".cogent","workflows","WF-BRIDGE");
      mkdirSync(workflow,{recursive:true});
      writeFileSync(join(workflow,"state.json"),JSON.stringify({taskId:"WF-BRIDGE",status:"running",revision:2}));
      expect(reconcileTicketWorkflows({workspaceDir:root,store,config:{ticketLeaseMs:5000} as any,now:new Date("2026-08-13T00:00:01.000Z")}))
        .toEqual([{ticketId:ticket.ticketId,action:"heartbeat"}]);
      writeFileSync(join(workflow,"state.json"),JSON.stringify({taskId:"WF-BRIDGE",status:"completed",revision:3}));
      expect(reconcileTicketWorkflows({workspaceDir:root,store,config:{ticketLeaseMs:5000} as any,now:new Date("2026-08-13T00:00:02.000Z")}))
        .toEqual([{ticketId:ticket.ticketId,action:"completed"}]);
      expect(store.snapshot()).toMatchObject({tickets:{completed:1},pendingOutbox:1});
    } finally { rmSync(root,{recursive:true,force:true}); }
  });

  it("reclaims a killed worker and relinks the existing workflow after service restart", async () => {
    const root = mkdtempSync(join(tmpdir(),"cogent-ticket-kill-"));
    const child = spawn(process.execPath,["-e","setInterval(()=>{},1000)"],{stdio:"ignore",windowsHide:true});
    try {
      const store = new TicketStore(join(root,"tickets.sqlite3"));
      const prompt = "PHASE 1\nA\nPHASE 2\nB\nPHASE 3\nC";
      const ticket = store.accept({runId:"kill-restart",ownerSessionKey:"agent:main:owner",prompt});
      store.route(ticket.ticketId,true);
      const decision = classifyDurableRequest(prompt);
      const intake = compileDurableIntake({workspaceDir:root,prompt,runId:"kill-restart",decision,model:"fixture"});
      const workflow = join(root,".cogent","workflows",intake.taskId);
      mkdirSync(workflow,{recursive:true});
      writeFileSync(join(workflow,"manifest.json"),readFileSync(join(root,intake.manifestPath)));
      writeFileSync(join(workflow,"state.json"),JSON.stringify({taskId:intake.taskId,status:"running",revision:1,controllerPid:child.pid}));
      const first = store.claim({ticketId:ticket.ticketId,workerId:`worker-${child.pid}`,leaseMs:1000,now:new Date("2026-08-13T00:00:00.000Z")})!;
      store.linkWorkflow({...first,workflowId:intake.taskId,manifestPath:intake.manifestPath,now:new Date("2026-08-13T00:00:00.000Z")});
      child.kill();
      await new Promise<void>((resolveExit)=>child.once("exit",()=>resolveExit()));

      expect(store.recoverExpired({now:new Date("2026-08-13T00:00:02.000Z")})).toHaveLength(1);
      let starts = 0;
      const restarted = dispatchTicketWorkflows({workspaceDir:root,store,config:{ticketLeaseMs:5000} as any,now:new Date("2026-08-13T00:00:02.000Z"),
        snapshot:{freeMemoryBytes:2**30,freeDiskBytes:2**30,running:0},start:()=>{starts++;throw new Error("existing workflow must be reused");}});
      expect(restarted.leases).toHaveLength(1);
      expect(restarted.leases[0].leaseGeneration).toBe(2);
      expect(starts).toBe(0);
      expect(store.get(ticket.ticketId)).toMatchObject({workflowId:intake.taskId,manifestPath:`.cogent/workflows/${intake.taskId}/manifest.json`});
    } finally { if (!child.killed) child.kill(); rmSync(root,{recursive:true,force:true}); }
  });
});
