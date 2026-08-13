#!/usr/bin/env python3
import argparse, json, os, shutil, subprocess, sys, time
from datetime import datetime, timezone
from pathlib import Path

TASK="CogentNexus Supervisor"
HERE=Path(__file__).resolve()
SKILL=HERE.parents[1]
WORKSPACE=SKILL.parents[1]
DEFAULT_ROOT=WORKSPACE/".cogent"

def emit(v): print(json.dumps(v,ensure_ascii=False,indent=2))
def run(cmd,timeout=60):
    flags=subprocess.CREATE_NO_WINDOW if os.name=="nt" else 0
    return subprocess.run(cmd,capture_output=True,text=True,timeout=timeout,creationflags=flags)
def policy_path(root): return root/"runtime"/"startup-policy.json"
def load_policy(root):
    try: return json.loads(policy_path(root).read_text(encoding="utf-8"))
    except FileNotFoundError: return {"policy":"unset"}
    except Exception: return {"policy":"invalid"}
def save_policy(root,value):
    p=policy_path(root); p.parent.mkdir(parents=True,exist_ok=True)
    q=p.with_suffix(".tmp")
    q.write_text(json.dumps({"schemaVersion":1,"policy":value,"updatedAt":datetime.now(timezone.utc).isoformat()},indent=2),encoding="utf-8")
    os.replace(q,p)
def python_background():
    p=Path(sys.executable)
    q=p.with_name("pythonw.exe")
    return q if os.name=="nt" and q.exists() else p
def ps(script):
    exe=shutil.which("powershell.exe") or shutil.which("powershell")
    if not exe: raise RuntimeError("PowerShell not found")
    return run([exe,"-NoProfile","-NonInteractive","-Command",script])
def win_status():
    r=ps(f"$t=Get-ScheduledTask -TaskName '{TASK}' -ErrorAction SilentlyContinue;if(!$t){{exit 3}};$i=Get-ScheduledTaskInfo -TaskName '{TASK}';[pscustomobject]@{{State=[string]$t.State;Enabled=$t.Settings.Enabled;Execute=$t.Actions.Execute;Arguments=$t.Actions.Arguments;Hidden=$t.Settings.Hidden;LastTaskResult=$i.LastTaskResult;NextRunTime=$i.NextRunTime}}|ConvertTo-Json -Compress")
    if r.returncode==3:return {"installed":False}
    if r.returncode:raise RuntimeError(r.stderr.strip())
    return {"installed":True,**json.loads(r.stdout)}
def backup_windows(root):
    if not win_status().get("installed"):return None
    d=root/"runtime"/"startup-backups";d.mkdir(parents=True,exist_ok=True)
    p=d/(datetime.now().strftime("%Y%m%d-%H%M%S")+"-windows-task.xml")
    r=ps(f"Export-ScheduledTask -TaskName '{TASK}'|Set-Content -LiteralPath '{str(p).replace(chr(39),chr(39)*2)}' -Encoding UTF8")
    if r.returncode:raise RuntimeError(r.stderr.strip())
    return str(p)
def win_enable(root):
    before=win_status(); backup=backup_windows(root)
    template=(SKILL/"templates"/"supervisor"/"windows-task.xml").read_text(encoding="utf-8")
    values={"{{PYTHON}}":str(python_background()),"{{RUNTIME}}":str(HERE.with_name("runtime.py")),"{{ROOT}}":str(root)}
    for k,v in values.items():template=template.replace(k,v)
    definition=root/"runtime"/"cogentnexus-supervisor.xml";definition.parent.mkdir(parents=True,exist_ok=True)
    definition.write_text(template,encoding="utf-8")
    if before.get("installed"):
        run(["schtasks.exe","/End","/TN",TASK])
    r=run(["schtasks.exe","/Create","/TN",TASK,"/XML",str(definition),"/F"])
    if r.returncode:raise RuntimeError(r.stderr.strip() or r.stdout.strip())
    r=run(["schtasks.exe","/Run","/TN",TASK])
    if r.returncode:raise RuntimeError(r.stderr.strip() or r.stdout.strip())
    time.sleep(4)
    state=win_status()
    expected=str(python_background()).lower()
    if not state.get("installed") or str(state.get("Execute","")).lower()!=expected or not state.get("Hidden"):
        raise RuntimeError("background task verification failed")
    return {"result":"updated" if before.get("installed") else "installed","backup":backup,"adapter":state,"mode":"hidden-background-logon"}
def win_disable(root):
    backup=backup_windows(root)
    r=run(["schtasks.exe","/Delete","/TN",TASK,"/F"])
    if r.returncode and win_status().get("installed"):raise RuntimeError(r.stderr.strip() or r.stdout.strip())
    return {"result":"disabled","backup":backup,"adapter":win_status()}
def systemd_paths():
    d=Path.home()/".config/systemd/user"
    return d/"cogentnexus-supervisor.service",d/"cogentnexus-supervisor.timer"
def unix_status():
    service,timer=systemd_paths()
    return {"installed":service.exists() and timer.exists(),"service":str(service),"timer":str(timer)}
def unix_enable(root):
    if sys.platform=="darwin":raise RuntimeError("launchd adapter is not yet packaged")
    if not shutil.which("systemctl"):raise RuntimeError("no supported native startup manager")
    service,timer=systemd_paths();service.parent.mkdir(parents=True,exist_ok=True)
    service.write_text(f"[Unit]\nDescription=CogentNexus hidden background supervisor\n[Service]\nType=oneshot\nExecStart={sys.executable} {HERE.with_name('runtime.py')} --root {root} supervisor tick --execute-safe\nStandardInput=null\n",encoding="utf-8")
    timer.write_text("[Unit]\nDescription=CogentNexus every minute\n[Timer]\nOnBootSec=1min\nOnUnitActiveSec=1min\nPersistent=true\n[Install]\nWantedBy=timers.target\n",encoding="utf-8")
    for cmd in (["systemctl","--user","daemon-reload"],["systemctl","--user","enable","--now",timer.name]):
        r=run(cmd)
        if r.returncode:raise RuntimeError(r.stderr.strip())
    return {"result":"enabled","adapter":unix_status(),"mode":"systemd-user"}
def unix_disable(root):
    service,timer=systemd_paths()
    if shutil.which("systemctl"):run(["systemctl","--user","disable","--now",timer.name])
    service.unlink(missing_ok=True);timer.unlink(missing_ok=True)
    return {"result":"disabled","adapter":unix_status()}
def status():
    return win_status() if os.name=="nt" else unix_status()
def command(args):
    root=Path(args.root).resolve();p=load_policy(root).get("policy","unset")
    if args.action=="status":emit({"policy":p,"adapter":status(),"background":True});return
    if args.action=="enable":
        result=win_enable(root) if os.name=="nt" else unix_enable(root);save_policy(root,"enabled");emit({"policy":"enabled",**result});return
    if args.action=="disable":
        result=win_disable(root) if os.name=="nt" else unix_disable(root);save_policy(root,"disabled");emit({"policy":"disabled",**result});return
    if p=="enabled":
        result=win_enable(root) if os.name=="nt" else unix_enable(root);emit({"policy":"enabled",**result});return
    emit({"policy":p,"result":"disabled" if p=="disabled" else "choice-required","adapter":status()})
def main():
    p=argparse.ArgumentParser();p.add_argument("--root",default=str(DEFAULT_ROOT));p.add_argument("action",choices=["status","enable","disable","ensure"]);a=p.parse_args()
    try:command(a);return 0
    except Exception as e:emit({"result":"error","error":str(e)});return 1
if __name__=="__main__":raise SystemExit(main())
