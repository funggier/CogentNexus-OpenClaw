# Output Verification and Delivery

Do not equate model text with completed work.

## Direct response boundary

1. verify runtime/provider provenance required by the recovery contract;
2. commit `response_ready` once;
3. persist one durable `direct_result`;
4. deliver/transport that result;
5. confirm delivery receipt/history marker;
6. only then complete the Ticket.

If delivery is uncertain after a durable result exists, retransport the durable result. Do not regenerate inference solely to obtain another copy of the same answer.

External side effects require their own idempotency/receipt/reconciliation contract; CNXCLAW delivery exactly-once-ish semantics do not automatically make every external system exactly-once.
