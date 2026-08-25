#!/usr/bin/env python3
import argparse, json, os, shutil, subprocess, sys, time
from datetime import datetime, timezone
from pathlib import Path

TASK="CogentNexus-OpenClaw-Supervisor"
LAUNCHD_LABEL="ai.cogentnexus.openclaw.supervisor"
HERE=Path(__file__).resolve()
SKILL=HERE.parents[1]
WORKSPACE=SKILL.parents[1]
DEFAULT_ROOT=WORKSPACE/".cogentnexus-openclaw"

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
    """Return the CogentNexus-owned background interpreter.

    Durable execution authority must never be registration-time
    ``sys.executable`` (which can be an executor venv such as a coding
    agent's). Delegate to the owned runtime authority; fall back to the
    transient bootstrap sibling only when the owned runtime is not yet
    provisioned (first install), so the installer can enable startup only
    after provisioning succeeds.
    """
    try:
        import runtime_authority
        owned = runtime_authority.require_background_interpreter()
        if owned.exists():
            return owned
    except Exception:
        pass
    p=Path(sys.executable)
    q=p.with_name("pythonw.exe")
    return q if os.name=="nt" and q.exists() else p
def host_control_path(): return HERE.with_name("host_control.py")
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
def write_windows_definition(path,template):
    document=template.replace('encoding="UTF-8"','encoding="UTF-16"',1)
    path.write_text(document,encoding="utf-16")
def win_enable(root):
    before=win_status(); backup=backup_windows(root)
    template=(SKILL/"templates"/"supervisor"/"windows-task.xml").read_text(encoding="utf-8")
    values={"{{PYTHON}}":str(python_background()),"{{RUNTIME}}":str(host_control_path()),"{{ROOT}}":str(root)}
    for k,v in values.items():template=template.replace(k,v)
    definition=root/"runtime"/"cogentnexus-openclaw-supervisor.xml";definition.parent.mkdir(parents=True,exist_ok=True)
    write_windows_definition(definition,template)
    if before.get("installed"): run(["schtasks.exe","/End","/TN",TASK])
    r=run(["schtasks.exe","/Create","/TN",TASK,"/XML",str(definition),"/F"])
    if r.returncode:raise RuntimeError(r.stderr.strip() or r.stdout.strip())
    r=run(["schtasks.exe","/Run","/TN",TASK])
    if r.returncode:raise RuntimeError(r.stderr.strip() or r.stdout.strip())
    time.sleep(4)
    state=win_status(); expected=str(python_background()).lower()
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
    return d/"cogentnexus-openclaw-supervisor.service",d/"cogentnexus-openclaw-supervisor.timer"
def systemd_status():
    service,timer=systemd_paths()
    return {"installed":service.exists() and timer.exists(),"service":str(service),"timer":str(timer)}
def systemd_enable(root):
    if not shutil.which("systemctl"):raise RuntimeError("no supported systemd user manager")
    service,timer=systemd_paths();service.parent.mkdir(parents=True,exist_ok=True)
    service.write_text(f"[Unit]\nDescription=CogentNexus-OpenClaw hidden background supervisor\n[Service]\nType=oneshot\nExecStart={sys.executable} {host_control_path()} --root {root} supervisor tick --execute-safe\nStandardInput=null\n",encoding="utf-8")
    timer.write_text("[Unit]\nDescription=CogentNexus-OpenClaw every minute\n[Timer]\nOnBootSec=1min\nOnUnitActiveSec=1min\nPersistent=true\n[Install]\nWantedBy=timers.target\n",encoding="utf-8")
    for cmd in (["systemctl","--user","daemon-reload"],["systemctl","--user","enable","--now",timer.name]):
        r=run(cmd)
        if r.returncode:raise RuntimeError(r.stderr.strip())
    return {"result":"enabled","adapter":systemd_status(),"mode":"systemd-user"}
def systemd_disable(root):
    service,timer=systemd_paths()
    if shutil.which("systemctl"):run(["systemctl","--user","disable","--now",timer.name])
    service.unlink(missing_ok=True);timer.unlink(missing_ok=True)
    return {"result":"disabled","adapter":systemd_status()}

def launchd_path(): return Path.home()/"Library/LaunchAgents"/f"{LAUNCHD_LABEL}.plist"
def launchd_domain(): return f"gui/{os.getuid()}"
def launchd_service(): return f"{launchd_domain()}/{LAUNCHD_LABEL}"
def launchd_loaded():
    if not shutil.which("launchctl"): return False
    return run(["launchctl","print",launchd_service()],timeout=20).returncode==0
def launchd_status():
    p=launchd_path()
    return {"installed":p.exists(),"loaded":launchd_loaded(),"plist":str(p),"label":LAUNCHD_LABEL}
def backup_launchd(root):
    p=launchd_path()
    if not p.exists(): return None
    d=root/"runtime"/"startup-backups";d.mkdir(parents=True,exist_ok=True)
    q=d/(datetime.now().strftime("%Y%m%d-%H%M%S")+"-launchd.plist")
    shutil.copy2(p,q); return str(q)
def launchd_enable(root):
    if not shutil.which("launchctl"):raise RuntimeError("launchctl not found")
    before=launchd_status(); backup=backup_launchd(root)
    template=(SKILL/"templates"/"supervisor"/"ai.cogentnexus.openclaw.supervisor.plist").read_text(encoding="utf-8")
    values={"{{PYTHON}}":str(python_background()),"{{RUNTIME}}":str(host_control_path()),"{{ROOT}}":str(root)}
    for k,v in values.items():template=template.replace(k,v)
    p=launchd_path();p.parent.mkdir(parents=True,exist_ok=True);p.write_text(template,encoding="utf-8")
    if before.get("loaded"): run(["launchctl","bootout",launchd_service()],timeout=30)
    r=run(["launchctl","bootstrap",launchd_domain(),str(p)],timeout=30)
    if r.returncode:raise RuntimeError(r.stderr.strip() or r.stdout.strip() or "launchctl bootstrap failed")
    run(["launchctl","kickstart","-k",launchd_service()],timeout=30)
    time.sleep(1)
    state=launchd_status()
    if not state.get("installed") or not state.get("loaded"):raise RuntimeError("launchd supervisor verification failed")
    return {"result":"updated" if before.get("installed") else "installed","backup":backup,"adapter":state,"mode":"launchd-user"}
def launchd_disable(root):
    backup=backup_launchd(root)
    if launchd_loaded(): run(["launchctl","bootout",launchd_service()],timeout=30)
    launchd_path().unlink(missing_ok=True)
    return {"result":"disabled","backup":backup,"adapter":launchd_status()}

def status():
    if os.name=="nt": return win_status()
    if sys.platform=="darwin": return launchd_status()
    return systemd_status()
def enable_adapter(root):
    if os.name=="nt": return win_enable(root)
    if sys.platform=="darwin": return launchd_enable(root)
    return systemd_enable(root)
def disable_adapter(root):
    if os.name=="nt": return win_disable(root)
    if sys.platform=="darwin": return launchd_disable(root)
    return systemd_disable(root)

def command(args):
    root=Path(args.root).resolve();p=load_policy(root).get("policy","unset")
    if args.action=="status":emit({"policy":p,"adapter":status(),"background":True});return
    if args.action=="enable":
        result=enable_adapter(root);save_policy(root,"enabled");emit({"policy":"enabled",**result});return
    if args.action=="disable":
        result=disable_adapter(root);save_policy(root,"disabled");emit({"policy":"disabled",**result});return
    if p=="enabled":
        result=enable_adapter(root);emit({"policy":"enabled",**result});return
    emit({"policy":p,"result":"disabled" if p=="disabled" else "choice-required","adapter":status()})
def main():
    p=argparse.ArgumentParser();p.add_argument("--root",default=str(DEFAULT_ROOT));p.add_argument("action",choices=["status","enable","disable","ensure"]);a=p.parse_args()
    try:command(a);return 0
    except Exception as e:emit({"result":"error","error":str(e)});return 1
if __name__=="__main__":raise SystemExit(main())
