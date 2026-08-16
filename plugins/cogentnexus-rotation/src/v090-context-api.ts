export function createContextMaintenanceApi(api:any) {
  const proxy=Object.create(api);
  const runtime=Object.create(api.runtime??{});
  const originalGateway=api.runtime?.gateway;
  if(originalGateway?.request) {
    const gateway=Object.create(originalGateway);
    gateway.request=async(method:string,params?:any,options?:any)=>{
      const result=await originalGateway.request(method,params,options);
      if(method!=="sessions.describe"||!result?.session)return result;
      // OpenClaw may rotate the physical transcript/sessionId during manual or
      // model-backed compaction. That is not a CogentNexus ownership boundary.
      // Reset/Delete/Stop are represented by the CNX session generation and
      // remain authoritative. Hide only the physical id from the maintenance
      // guard so a user-initiated Compact cannot be mistaken for Reset.
      const {sessionId:_physicalRevision,...session}=result.session;
      return {...result,session};
    };
    runtime.gateway=gateway;
  }
  proxy.runtime=runtime;
  return proxy;
}
