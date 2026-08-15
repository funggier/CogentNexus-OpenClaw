#!/usr/bin/env python3
from pathlib import Path
p=Path(__file__).with_name("apply_session_continuity_v083.py")
text=p.read_text(encoding="utf-8")
old='''patch(\n    host,\n    \'\'\'    return {"state": state, "lifecycle": parse_json_output(result.stdout), "recoveredTickets": recovered}\\n\'\'\',\n    \'\'\'    return {"state": state, "lifecycle": parse_json_output(result.stdout), "sessionBootstrap": session_bootstrap, "recoveredTickets": recovered}\\n\'\'\',\n    "host start session bootstrap result",\n)'''
new='''patch(\n    host,\n    \'\'\'    recovered = promote_interrupted_direct(root, started, "Gateway resumed by CogentNexus Host after interruption")\\n    runtime(root, "supervisor", "tick", "--execute-safe", timeout=180, check=False)\\n    return {"state": state, "lifecycle": parse_json_output(result.stdout), "recoveredTickets": recovered}\\n\'\'\',\n    \'\'\'    recovered = promote_interrupted_direct(root, started, "Gateway resumed by CogentNexus Host after interruption")\\n    runtime(root, "supervisor", "tick", "--execute-safe", timeout=180, check=False)\\n    return {"state": state, "lifecycle": parse_json_output(result.stdout), "sessionBootstrap": session_bootstrap, "recoveredTickets": recovered}\\n\'\'\',\n    "host start session bootstrap result",\n)'''
if text.count(old)!=1:
    raise SystemExit(f"expected one helper anchor block, found {text.count(old)}")
p.write_text(text.replace(old,new,1),encoding="utf-8",newline="\n")
print("fixed unique start_managed result anchor")
