#!/usr/bin/env python3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
host=ROOT/"skills/cogentnexus/scripts/host.py"
text=host.read_text(encoding="utf-8")
old='''        ("autoResume", "true"),\n        ("ticketDispatchLimit", "1"),'''
new='''        ("autoResume", "true"),\n        ("workspaceDir", str(WORKSPACE)),\n        ("ticketDispatchLimit", "1"),'''
if text.count(old)!=1: raise SystemExit(f"host workspace config anchor count={text.count(old)}")
host.write_text(text.replace(old,new,1),encoding="utf-8",newline="\n")
index=ROOT/"plugins/cogentnexus-rotation/src/index.ts"
text=index.read_text(encoding="utf-8")
old='''    const workspaceDir=resolve(ctx.workspaceDir ?? config.workspaceDir ?? process.cwd());\n    try {\n      const store=new TicketStore(config.ticketDatabasePath ?? defaultTicketDatabase(workspaceDir));\n      const rebound=rebindSessionSuccessor'''
new='''    const workspaceDir=resolve(config.workspaceDir ?? process.cwd());\n    try {\n      const store=new TicketStore(config.ticketDatabasePath ?? defaultTicketDatabase(workspaceDir));\n      const rebound=rebindSessionSuccessor'''
if text.count(old)!=1: raise SystemExit(f"session hook context anchor count={text.count(old)}")
index.write_text(text.replace(old,new,1),encoding="utf-8",newline="\n")
print("bound session lifecycle hook to Host-configured workspace")
