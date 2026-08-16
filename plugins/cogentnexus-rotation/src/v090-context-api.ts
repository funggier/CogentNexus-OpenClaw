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
      // remain authoritative.
      //
      // maxLines/manual trimming may also intentionally invalidate token
      // metadata while leaving the old numeric totalTokens value in the row.
      // Never feed that stale number back into context admission/maintenance.
      const {
        sessionId:_physicalRevision,
        totalTokens:_reportedTotalTokens,
        totalTokensFresh,
        ...rest
      }=result.session;
      const session=totalTokensFresh===true
        ? {...rest,totalTokens:_reportedTotalTokens,totalTokensFresh:true}
        : {...rest,totalTokensFresh:false};
      return {...result,session};
    };
    runtime.gateway=gateway;
  }
  proxy.runtime=runtime;
  return proxy;
}
