#!/usr/bin/env python3
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

(ROOT/"tests/test_host_session_bootstrap.py").write_text(r'''from __future__ import annotations

import importlib.util
import subprocess
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
HOST=ROOT/"skills"/"cogentnexus"/"scripts"/"host.py"
spec=importlib.util.spec_from_file_location("cnx_host_session_bootstrap",HOST)
cnx_host=importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(cnx_host)


def completed(stdout: str):
    return subprocess.CompletedProcess(["openclaw"],0,stdout=stdout,stderr="")


class HostSessionBootstrapTests(unittest.TestCase):
    def test_empty_store_bootstraps_default_main_session_through_gateway_rpc(self):
        before='{"sessions":[],"count":0}'
        after='{"sessions":[{"key":"agent:main:main"}],"count":1}'
        with patch.object(cnx_host,"gateway_status",return_value={"healthy":True}), \
             patch.object(cnx_host,"default_agent_id",return_value="main"), \
             patch.object(cnx_host,"configured_main_key",return_value="main"), \
             patch.object(cnx_host,"openclaw_executable",return_value="openclaw"), \
             patch.object(cnx_host,"run",side_effect=[completed(before),completed(after)]), \
             patch.object(cnx_host,"gateway_rpc",return_value={"key":"agent:main:main"}) as rpc:
            result=cnx_host.reconcile_default_session()
        self.assertTrue(result["ok"])
        self.assertTrue(result["created"])
        self.assertEqual(result["sessionKey"],"agent:main:main")
        rpc.assert_called_once_with("sessions.create",{"key":"main","agentId":"main"},timeout=30)

    def test_existing_default_main_session_is_idempotent(self):
        existing='{"sessions":[{"key":"agent:main:main"}],"count":1}'
        with patch.object(cnx_host,"gateway_status",return_value={"healthy":True}), \
             patch.object(cnx_host,"default_agent_id",return_value="main"), \
             patch.object(cnx_host,"configured_main_key",return_value="main"), \
             patch.object(cnx_host,"openclaw_executable",return_value="openclaw"), \
             patch.object(cnx_host,"run",return_value=completed(existing)), \
             patch.object(cnx_host,"gateway_rpc") as rpc:
            result=cnx_host.reconcile_default_session()
        self.assertTrue(result["ok"])
        self.assertFalse(result["created"])
        rpc.assert_not_called()

    def test_unhealthy_gateway_does_not_mutate_sessions(self):
        with patch.object(cnx_host,"gateway_status",return_value={"healthy":False}), patch.object(cnx_host,"gateway_rpc") as rpc:
            result=cnx_host.reconcile_default_session()
        self.assertTrue(result["skipped"])
        rpc.assert_not_called()


if __name__=="__main__":
    unittest.main()
''',encoding="utf-8",newline="\n")

(ROOT/"tests/test_workflow_session_rebind.py").write_text(r'''from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
WORKFLOW=ROOT/"skills"/"cogentnexus"/"scripts"/"workflow.py"
spec=importlib.util.spec_from_file_location("cnx_workflow_session_rebind",WORKFLOW)
workflow=importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(workflow)


class WorkflowSessionRebindTests(unittest.TestCase):
    def test_pending_owner_and_completion_follow_exact_successor(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/"workspace"; root.mkdir()
            manifest=root/"manifest.json"
            manifest.write_text(json.dumps({
                "schemaVersion":1,"taskId":"WF-REBIND","steps":[{
                    "id":"one","executor":{"type":"command","argv":[sys.executable,"-c","print('ok')"]},"outputs":[]
                }]
            }),encoding="utf-8")
            workflow.initialize(root,manifest,owner_session_key="agent:main:main")
            flow=workflow.Workflow(root,"WF-REBIND")
            workflow.atomic_json(flow.completion_path,{
                "schemaVersion":1,"taskId":"WF-REBIND","ownerSessionKey":"agent:main:main",
                "workflowStatus":"completed","createdAt":workflow.now(),"deliveryStatus":"pending"
            })
            result=workflow.rebind_session_owner(root,"agent:main:main","agent:main:dashboard:new")
            self.assertEqual(len(result["workflows"]),1)
            self.assertEqual(flow.read(flow.owner_path)["ownerSessionKey"],"agent:main:dashboard:new")
            self.assertEqual(flow.read(flow.completion_path)["ownerSessionKey"],"agent:main:dashboard:new")
            events=[json.loads(line) for line in flow.ledger_path.read_text(encoding="utf-8").splitlines()]
            self.assertEqual(events[-1]["type"],"WORKFLOW_OWNER_REBOUND")

    def test_rebind_is_exact_and_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/"workspace"; root.mkdir()
            manifest=root/"manifest.json"
            manifest.write_text(json.dumps({
                "schemaVersion":1,"taskId":"WF-EXACT","steps":[{
                    "id":"one","executor":{"type":"command","argv":[sys.executable,"-c","print('ok')"]},"outputs":[]
                }]
            }),encoding="utf-8")
            workflow.initialize(root,manifest,owner_session_key="agent:other:main")
            untouched=workflow.rebind_session_owner(root,"agent:main:main","agent:main:dashboard:new")
            self.assertEqual(untouched["workflows"],[])
            flow=workflow.Workflow(root,"WF-EXACT")
            self.assertEqual(flow.read(flow.owner_path)["ownerSessionKey"],"agent:other:main")


if __name__=="__main__":
    unittest.main()
''',encoding="utf-8",newline="\n")

plugin_test=ROOT/"plugins/cogentnexus-rotation/src/session-succession.test.ts"
plugin_test.write_text(r'''import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { afterEach, describe, expect, it } from "vitest";
import { TicketStore } from "./ticket-store.js";

const roots:string[]=[];
afterEach(()=>{for(const root of roots.splice(0)) rmSync(root,{recursive:true,force:true});});

function store(){const root=mkdtempSync(join(tmpdir(),"cnx-session-successor-"));roots.push(root);return new TicketStore(join(root,"tickets.sqlite3"));}

describe("session succession",()=>{
  it("rebinds unfinished tickets and pending terminal delivery to the trusted successor",()=>{
    const tickets=store();
    const accepted=tickets.accept({runId:"run-old",ownerSessionKey:"agent:main:main",prompt:"continue this"});
    const db=new DatabaseSync(tickets.databasePath);
    db.prepare(`INSERT INTO ticket_outbox(ticket_id,owner_session_key,terminal_status,payload_json,delivery_status,delivery_attempts,created_at) VALUES (?,?,?,?,'pending',0,?)`)
      .run(accepted.ticketId,"agent:main:main","completed","{}",new Date().toISOString());
    db.close();
    const rebound=tickets.rebindSessionOwner({fromSessionKey:"agent:main:main",toSessionKey:"agent:main:dashboard:new"});
    expect(rebound.ticketIds).toEqual([accepted.ticketId]);
    expect(rebound.outboxCount).toBe(1);
    expect(tickets.get(accepted.ticketId)?.ownerSessionKey).toBe("agent:main:dashboard:new");
    const verify=new DatabaseSync(tickets.databasePath);
    expect((verify.prepare("SELECT owner_session_key FROM ticket_outbox WHERE ticket_id=?").get(accepted.ticketId) as any).owner_session_key).toBe("agent:main:dashboard:new");
    expect((verify.prepare("SELECT event_type FROM ticket_events WHERE ticket_id=? ORDER BY event_id DESC LIMIT 1").get(accepted.ticketId) as any).event_type).toBe("owner_session_rebound");
    verify.close();
  });

  it("does not move a different owner",()=>{
    const tickets=store();
    const accepted=tickets.accept({runId:"run-other",ownerSessionKey:"agent:other:main",prompt:"leave this"});
    const rebound=tickets.rebindSessionOwner({fromSessionKey:"agent:main:main",toSessionKey:"agent:main:dashboard:new"});
    expect(rebound.ticketIds).toEqual([]);
    expect(tickets.get(accepted.ticketId)?.ownerSessionKey).toBe("agent:other:main");
  });
});
''',encoding="utf-8",newline="\n")
print("wrote session continuity regression tests")
