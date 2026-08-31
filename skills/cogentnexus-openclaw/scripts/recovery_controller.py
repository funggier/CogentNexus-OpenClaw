#!/usr/bin/env python3
import hashlib,json,re
from datetime import datetime,timezone
FAILURES={"oom","timeout","tool-failure","permission","invalid-output","process-killed","verification-failure","dependency-missing","network","unknown"}
POLICIES={
"oom":("reduce-resource-pressure",{"chunkScale":0.5,"concurrency":1,"useDiskIntermediate":True},["runtime.state"],[]),
"timeout":("inspect-before-retry",{"inspectSurvivorBeforeRetry":True},["process.execute"],["Confirm whether process or artifact survived"]),
"invalid-output":("repair-smallest-invalid-unit",{"repairSmallestUnit":True},["runtime.verify"],[]),
"verification-failure":("repair-from-validator-evidence",{"repairSmallestUnit":True},["runtime.verify"],[]),
"process-killed":("resume-last-committed-checkpoint",{"resumeCheckpoint":True},["runtime.state"],[]),
"tool-failure":("change-tool-path",{},[],["Select a different available capability"]),
"dependency-missing":("request-or-install-dependency",{},[],["Obtain authorization before installing dependencies"]),
"permission":("request-authorization",{},[],["Do not bypass permission"]),
"network":("verify-network-before-retry",{"probeNetworkBeforeRetry":True},[],[]),
"unknown":("collect-more-evidence",{},[],["Inspect latest failure evidence"])}
def now(): return datetime.now(timezone.utc).isoformat()
def classify(records):
 failures=[x for x in records if x.get("type")=="FAILURE"]
 if not failures:return {"class":"unknown","confidence":0.0,"source":None}
 latest=failures[-1]; data=latest.get("data") or {}; explicit=str(data.get("class","")).lower()
 if explicit in FAILURES:return {"class":explicit,"confidence":1.0,"source":latest.get("sequence")}
 text=(latest.get("summary","")+" "+json.dumps(data)).lower()
 for kind,pattern in [("oom",r"out of memory|\boom\b|memoryerror|cannot allocate"),("timeout",r"timed? ?out|timeout"),("permission",r"permission|access denied|forbidden|unauthorized"),("process-killed",r"process killed|terminated|signal"),("dependency-missing",r"not found|no module named|missing dependency"),("network",r"network|connection|dns|tls|http 5\d\d"),("verification-failure",r"verification fail|assertionerror|test failed"),("invalid-output",r"invalid output|parse error|schema")]:
  if re.search(pattern,text):return {"class":kind,"confidence":0.8,"source":latest.get("sequence")}
 return {"class":"tool-failure","confidence":0.5,"source":latest.get("sequence")}
def recovery_state(state):
 value=dict(state.get("recovery") or {}); value.setdefault("retryBudget",{"used":0,"maximum":3}); value.setdefault("currentStrategy",None)
 value.setdefault("strategyHistory",[]); value.setdefault("failureClass",None); value.setdefault("status","not-required"); value.setdefault("settings",{}); value.setdefault("circuitOpen",False)
 return value
def make_plan(state,classification,capabilities):
 kind=classification["class"]; strategy,settings,required,manual=POLICIES.get(kind,POLICIES["unknown"]); recovery=recovery_state(state)
 same=sum(x.get("strategy")==strategy for x in recovery["strategyHistory"][-2:]); budget=recovery["retryBudget"]
 circuit=same>=2 or int(budget.get("used",0))>=int(budget.get("maximum",3)); missing=[x for x in required if not capabilities.get(x,False)]
 plan={"taskId":state.get("taskId"),"stateRevision":state.get("revision"),"failureClass":kind,"strategy":strategy,"safeSettings":settings,
 "manualActions":manual,"requiredCapabilities":required,"missingCapabilities":missing,"retryBudget":budget,"circuitOpen":circuit,
 "autoApplicable":bool(settings) and not missing and not circuit}
 plan["planId"]=hashlib.sha256(json.dumps(plan,sort_keys=True,separators=(",",":")).encode()).hexdigest()[:16]; plan["createdAt"]=now(); return plan
def apply_to_state(state,plan):
 if plan["circuitOpen"]:raise ValueError("circuit breaker is open")
 if not plan["autoApplicable"]:raise ValueError("recovery plan requires manual action or unavailable capability")
 new=dict(state); recovery=recovery_state(state); budget=dict(recovery["retryBudget"]); budget["used"]=int(budget.get("used",0))+1
 settings=dict(recovery["settings"]); settings.update(plan["safeSettings"]); history=list(recovery["strategyHistory"]); history.append({"strategy":plan["strategy"],"planId":plan["planId"],"appliedAt":now()})
 recovery.update({"retryBudget":budget,"currentStrategy":plan["strategy"],"strategyHistory":history,"failureClass":plan["failureClass"],"status":"applied","settings":settings,"circuitOpen":budget["used"]>=int(budget.get("maximum",3))})
 new.update({"recovery":recovery,"status":"executing","currentStep":f"recover:{plan['strategy']}"}); return new
