#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def patch(path: Path, old: str, new: str, label: str) -> None:
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected one match, found {count}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8", newline="\n")
    print(f"patched {label}")


host = ROOT / "skills/cogentnexus/scripts/host.py"
patch(
    host,
    '''def plugin_enabled(enabled: bool) -> None:\n    run([openclaw_executable(), "plugins", "enable" if enabled else "disable", PLUGIN_ID], timeout=60, check=True)\n''',
    '''def gateway_rpc(method: str, params: dict[str, Any] | None = None, timeout: int = 30) -> Any:\n    command = [openclaw_executable(), "gateway", "call", method, "--params", json.dumps(params or {}, separators=(",", ":")), "--json"]\n    result = run(command, timeout=timeout, check=True)\n    value = result.stdout.strip()\n    if not value:\n        return None\n    try:\n        return json.loads(value)\n    except json.JSONDecodeError as error:\n        raise RuntimeError(f"OpenClaw Gateway RPC {method} returned invalid JSON: {value[:500]}") from error\n\n\ndef default_agent_id() -> str:\n    result = run([openclaw_executable(), "agents", "list", "--json"], timeout=30, check=True)\n    try:\n        agents = json.loads(result.stdout)\n    except json.JSONDecodeError as error:\n        raise RuntimeError("OpenClaw agents list returned invalid JSON") from error\n    if not isinstance(agents, list) or not agents:\n        raise RuntimeError("OpenClaw has no configured agents")\n    selected = next((item for item in agents if isinstance(item, dict) and item.get("isDefault") is True), None)\n    selected = selected or next((item for item in agents if isinstance(item, dict) and item.get("id")), None)\n    agent_id = selected.get("id") if isinstance(selected, dict) else None\n    if not isinstance(agent_id, str) or not agent_id.strip():\n        raise RuntimeError("OpenClaw default agent id could not be resolved")\n    return agent_id.strip()\n\n\ndef configured_main_key() -> str:\n    result = run([openclaw_executable(), "config", "get", "session.mainKey"], timeout=20)\n    if result.returncode != 0:\n        return "main"\n    value = result.stdout.strip()\n    if not value:\n        return "main"\n    try:\n        decoded = json.loads(value)\n        if isinstance(decoded, str) and decoded.strip():\n            return decoded.strip()\n    except json.JSONDecodeError:\n        pass\n    return value.strip('"').strip() or "main"\n\n\ndef reconcile_default_session() -> dict[str, Any]:\n    status = gateway_status()\n    if not status.get("healthy"):\n        return {"ok": False, "skipped": True, "reason": "gateway not healthy"}\n    agent_id = default_agent_id()\n    main_key = configured_main_key()\n    expected = f"agent:{agent_id}:{main_key}"\n    result = run([openclaw_executable(), "sessions", "--json"], timeout=30, check=True)\n    try:\n        snapshot = json.loads(result.stdout)\n    except json.JSONDecodeError as error:\n        raise RuntimeError("OpenClaw sessions list returned invalid JSON") from error\n    sessions = snapshot.get("sessions", []) if isinstance(snapshot, dict) else []\n    if any(isinstance(item, dict) and item.get("key") == expected for item in sessions):\n        return {"ok": True, "created": False, "sessionKey": expected, "reason": "already present"}\n    created = gateway_rpc("sessions.create", {"key": main_key, "agentId": agent_id}, timeout=30)\n    created_key = created.get("key") if isinstance(created, dict) else None\n    if not isinstance(created_key, str) or not created_key.strip():\n        raise RuntimeError(f"OpenClaw sessions.create returned no session key: {created!r}")\n    verify = run([openclaw_executable(), "sessions", "--json"], timeout=30, check=True)\n    try:\n        verified = json.loads(verify.stdout)\n    except json.JSONDecodeError as error:\n        raise RuntimeError("OpenClaw sessions verification returned invalid JSON") from error\n    verified_sessions = verified.get("sessions", []) if isinstance(verified, dict) else []\n    if not any(isinstance(item, dict) and item.get("key") == created_key for item in verified_sessions):\n        raise RuntimeError(f"OpenClaw created session {created_key} but it was not persisted")\n    return {"ok": True, "created": True, "sessionKey": created_key, "expectedMainSessionKey": expected}\n\n\ndef plugin_enabled(enabled: bool) -> None:\n    run([openclaw_executable(), "plugins", "enable" if enabled else "disable", PLUGIN_ID], timeout=60, check=True)\n''',
    "host session bootstrap helpers",
)
patch(
    host,
    '''    lifecycle = runtime(root, "lifecycle", "start", "--provider", timeout=240, check=True)\n    recovered = promote_interrupted_direct(root, started, "CogentNexus Host enabled after an interrupted OpenClaw runtime")\n''',
    '''    lifecycle = runtime(root, "lifecycle", "start", "--provider", timeout=240, check=True)\n    session_bootstrap = reconcile_default_session()\n    recovered = promote_interrupted_direct(root, started, "CogentNexus Host enabled after an interrupted OpenClaw runtime")\n''',
    "host enable session bootstrap",
)
patch(
    host,
    '''        "lifecycle": parse_json_output(lifecycle.stdout),\n        "recoveredTickets": recovered,\n''',
    '''        "lifecycle": parse_json_output(lifecycle.stdout),\n        "sessionBootstrap": session_bootstrap,\n        "recoveredTickets": recovered,\n''',
    "host enable session bootstrap result",
)
patch(
    host,
    '''    result = runtime(root, "lifecycle", "start", *(["--provider"] if provider else []), timeout=240, check=True)\n    recovered = promote_interrupted_direct(root, started, "Gateway resumed by CogentNexus Host after interruption")\n''',
    '''    result = runtime(root, "lifecycle", "start", *(["--provider"] if provider else []), timeout=240, check=True)\n    session_bootstrap = reconcile_default_session()\n    recovered = promote_interrupted_direct(root, started, "Gateway resumed by CogentNexus Host after interruption")\n''',
    "host start session bootstrap",
)
patch(
    host,
    '''    return {"state": state, "lifecycle": parse_json_output(result.stdout), "recoveredTickets": recovered}\n''',
    '''    return {"state": state, "lifecycle": parse_json_output(result.stdout), "sessionBootstrap": session_bootstrap, "recoveredTickets": recovered}\n''',
    "host start session bootstrap result",
)

workflow = ROOT / "skills/cogentnexus/scripts/workflow.py"
patch(
    workflow,
    '''def initialize(root, manifest_file, owner_session_key=None, operator_unbound=False, operator_reason=None):\n''',
    '''def rebind_owner(flow, from_session_key, to_session_key):\n    if not isinstance(from_session_key, str) or not from_session_key.strip(): raise ValueError("valid previous owner session key required")\n    if not isinstance(to_session_key, str) or not to_session_key.strip() or len(to_session_key) > 512: raise ValueError("valid successor owner session key required")\n    old_key, new_key = from_session_key.strip(), to_session_key.strip()\n    if old_key == new_key: return {"taskId":flow.task_id,"changed":False,"ownerSessionKey":new_key}\n    with lock(flow.lock_path):\n        if not flow.owner_path.is_file(): return {"taskId":flow.task_id,"changed":False,"reason":"unbound"}\n        owner = flow.read(flow.owner_path)\n        current = owner.get("ownerSessionKey")\n        if current == new_key: return {"taskId":flow.task_id,"changed":False,"ownerSessionKey":new_key,"idempotent":True}\n        if current != old_key: return {"taskId":flow.task_id,"changed":False,"reason":"different-owner","ownerSessionKey":current}\n        rebound = dict(owner); rebound["ownerSessionKey"] = new_key; rebound["reboundAt"] = now(); rebound["previousOwnerSessionKey"] = old_key\n        atomic_json(flow.owner_path,rebound)\n        if flow.completion_path.is_file():\n            completion = flow.read(flow.completion_path)\n            if completion.get("deliveryStatus") != "delivered" and completion.get("ownerSessionKey") == old_key:\n                completion["ownerSessionKey"] = new_key; completion["ownerReboundAt"] = now(); atomic_json(flow.completion_path,completion)\n        flow.event("WORKFLOW_OWNER_REBOUND","Workflow owner session advanced to its OpenClaw successor",{"fromSessionKey":old_key,"toSessionKey":new_key})\n        return {"taskId":flow.task_id,"changed":True,"ownerSessionKey":new_key}\n\n\ndef rebind_session_owner(root, from_session_key, to_session_key):\n    base = Path(root).resolve() / ".cogent" / "workflows"\n    if not base.exists(): return {"fromSessionKey":from_session_key,"toSessionKey":to_session_key,"workflows":[]}\n    results=[]\n    for item in sorted(base.iterdir()):\n        if item.is_dir() and TASK_ID.fullmatch(item.name):\n            flow=Workflow(root,item.name)\n            if flow.owner_path.is_file():\n                result=rebind_owner(flow,from_session_key,to_session_key)\n                if result.get("changed") or result.get("idempotent"): results.append(result)\n    return {"fromSessionKey":from_session_key,"toSessionKey":to_session_key,"workflows":results}\n\n\ndef initialize(root, manifest_file, owner_session_key=None, operator_unbound=False, operator_reason=None):\n''',
    "workflow owner succession",
)
patch(
    workflow,
    '''    b=sub.add_parser("bind-owner"); b.add_argument("task_id"); b.add_argument("--session-key",required=True)\n    s=sub.add_parser("supervise"); s.add_argument("--execute",action="store_true"); s.add_argument("--maximum",type=int,default=4)\n''',
    '''    b=sub.add_parser("bind-owner"); b.add_argument("task_id"); b.add_argument("--session-key",required=True)\n    rb=sub.add_parser("rebind-session-owner"); rb.add_argument("--from-session-key",required=True); rb.add_argument("--to-session-key",required=True)\n    s=sub.add_parser("supervise"); s.add_argument("--execute",action="store_true"); s.add_argument("--maximum",type=int,default=4)\n''',
    "workflow succession CLI parser",
)
patch(
    workflow,
    '''    if args.command=="bind-owner": emit(bind_owner(args.root,args.task_id,args.session_key)); return\n    if args.command=="supervise": emit(supervise_workflows(args.root,args.execute,args.maximum)); return\n''',
    '''    if args.command=="bind-owner": emit(bind_owner(args.root,args.task_id,args.session_key)); return\n    if args.command=="rebind-session-owner": emit(rebind_session_owner(args.root,args.from_session_key,args.to_session_key)); return\n    if args.command=="supervise": emit(supervise_workflows(args.root,args.execute,args.maximum)); return\n''',
    "workflow succession CLI dispatch",
)

ticket_store = ROOT / "plugins/cogentnexus-rotation/src/ticket-store.ts"
patch(
    ticket_store,
    '''  get(ticketId: string): TicketRecord | undefined {\n''',
    '''  rebindSessionOwner(input:{fromSessionKey:string;toSessionKey:string;now?:Date}) {\n    const fromSessionKey=input.fromSessionKey.trim(),toSessionKey=input.toSessionKey.trim();\n    if(!fromSessionKey || !toSessionKey) throw new Error("valid session succession keys required");\n    if(fromSessionKey===toSessionKey) return {ticketIds:[],workflowIds:[],outboxCount:0};\n    const db=this.open(),nowIso=(input.now??new Date()).toISOString();\n    try {\n      db.exec("BEGIN IMMEDIATE");\n      const rows=db.prepare(`SELECT ticket_id,workflow_id FROM tickets WHERE owner_session_key=? AND status NOT IN ('completed','failed','cancelled') ORDER BY created_at,ticket_id`).all(fromSessionKey) as any[];\n      const ticketIds:string[]=[],workflowIds:string[]=[];\n      for(const row of rows){\n        const changed=db.prepare(`UPDATE tickets SET owner_session_key=?,updated_at=? WHERE ticket_id=? AND owner_session_key=? AND status NOT IN ('completed','failed','cancelled')`).run(toSessionKey,nowIso,row.ticket_id,fromSessionKey);\n        if(changed.changes!==1) continue;\n        ticketIds.push(row.ticket_id); if(typeof row.workflow_id==="string" && row.workflow_id) workflowIds.push(row.workflow_id);\n        this.event(db,row.ticket_id,"owner_session_rebound",{fromSessionKey,toSessionKey},nowIso);\n      }\n      const outbox=db.prepare(`UPDATE ticket_outbox SET owner_session_key=? WHERE owner_session_key=? AND delivery_status='pending'`).run(toSessionKey,fromSessionKey);\n      db.exec("COMMIT");\n      return {ticketIds,workflowIds:[...new Set(workflowIds)],outboxCount:Number(outbox.changes)};\n    } catch(error){try{db.exec("ROLLBACK");}catch{}throw error;} finally{db.close();}\n  }\n\n  get(ticketId: string): TicketRecord | undefined {\n''',
    "ticket owner succession",
)

index = ROOT / "plugins/cogentnexus-rotation/src/index.ts"
patch(
    index,
    '''export function reconcileTicketWorkflows(input:{workspaceDir:string;store:TicketStore;config:RotationConfig;now?:Date}) {\n''',
    '''export function rebindSessionSuccessor(input:{workspaceDir:string;store:TicketStore;fromSessionKey:string;toSessionKey:string;pythonCommand?:string}) {\n  const fromSessionKey=input.fromSessionKey.trim(),toSessionKey=input.toSessionKey.trim();\n  if(!fromSessionKey || !toSessionKey || fromSessionKey===toSessionKey) return {ticketIds:[],workflowIds:[],outboxCount:0,workflowRebind:{workflows:[]}};\n  const ticketRebind=input.store.rebindSessionOwner({fromSessionKey,toSessionKey});\n  const workflowRebind=runWorkflowCli(input.pythonCommand ?? "python",workflowRuntime(input.workspaceDir),["--root",input.workspaceDir,"rebind-session-owner","--from-session-key",fromSessionKey,"--to-session-key",toSessionKey]);\n  return {...ticketRebind,workflowRebind};\n}\n\nexport function reconcileTicketWorkflows(input:{workspaceDir:string;store:TicketStore;config:RotationConfig;now?:Date}) {\n''',
    "bridge session succession helper",
)
patch(
    index,
    '''  if (config.ticketFirst === true) api.on("reply_dispatch", (event, ctx) => {\n''',
    '''  if (config.ticketFirst === true) api.on("session_end", (event, ctx) => {\n    if(event.reason!=="new" || !event.sessionKey || !event.nextSessionKey || event.sessionKey===event.nextSessionKey) return;\n    const workspaceDir=resolve(ctx.workspaceDir ?? config.workspaceDir ?? process.cwd());\n    try {\n      const store=new TicketStore(config.ticketDatabasePath ?? defaultTicketDatabase(workspaceDir));\n      const rebound=rebindSessionSuccessor({workspaceDir,store,fromSessionKey:event.sessionKey,toSessionKey:event.nextSessionKey,pythonCommand:config.pythonCommand});\n      api.logger.info?.(`CogentNexus rebound session continuity ${event.sessionKey} -> ${event.nextSessionKey}: ${rebound.ticketIds.length} tickets, ${rebound.outboxCount} pending outbox deliveries`);\n    } catch(error) { api.logger.error(`CogentNexus session successor rebind failed: ${error instanceof Error?error.message:String(error)}`); }\n  }, { priority: 500, timeoutMs: 10_000 });\n\n  if (config.ticketFirst === true) api.on("reply_dispatch", (event, ctx) => {\n''',
    "bridge session_end succession hook",
)

release = ROOT / "docs/releases/v0.8.3.md"
text = release.read_text(encoding="utf-8")
needle = "- A requested provider that remains healthy makes lifecycle stop return a non-zero status instead of falsely reporting a safe shutdown.\n"
addition = needle + "- Host MANAGED start/enable now bootstraps the canonical default main OpenClaw session through official Gateway RPC when the persisted session store does not contain it, preventing stale `agent:<id>:main` Control UI parents from blocking New Session.\n- `/new` session succession now rebinds unfinished Tickets, pending terminal outbox delivery, and workflow owner bindings from the exact previous session key to OpenClaw's trusted `nextSessionKey`.\n"
if text.count(needle) != 1:
    raise SystemExit("release note anchor missing")
release.write_text(text.replace(needle,addition,1),encoding="utf-8",newline="\n")
print("patched v0.8.3 release notes")
