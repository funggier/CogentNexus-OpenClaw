from __future__ import annotations

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
