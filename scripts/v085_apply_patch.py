from pathlib import Path


root = Path(__file__).resolve().parents[1]
host_path = root / "skills" / "cogentnexus" / "scripts" / "host.py"
ticket_path = root / "plugins" / "cogentnexus-rotation" / "src" / "ticket-store.ts"

host = host_path.read_text(encoding="utf-8")
marker = "# v0.8.5: Direct Recovery owns its Ticket until it releases or settles it."
if marker not in host:
    old_select = '''        rows = db.execute(
            "SELECT ticket_id FROM tickets WHERE status='accepted' AND workflow_eligible=0 AND created_at<? ORDER BY created_at,ticket_id",
            (cutoff_iso,),
        ).fetchall()
        updated = []
'''
    new_select = '''        # v0.8.5: Direct Recovery owns its Ticket until it releases or settles it.
        # Apply the same NOT EXISTS fence at candidate selection and mutation time so a
        # Host lifecycle reconciliation cannot race an active plugin recovery claim.
        direct_guard = ""
        if table_exists(db, "cnx_direct_recovery"):
            direct_guard = (
                " AND NOT EXISTS (SELECT 1 FROM cnx_direct_recovery r "
                "WHERE r.ticket_id=tickets.ticket_id "
                "AND r.state IN ('pending','running','awaiting_delivery'))"
            )
        rows = db.execute(
            "SELECT ticket_id FROM tickets WHERE status='accepted' AND workflow_eligible=0 "
            f"AND created_at<?{direct_guard} ORDER BY created_at,ticket_id",
            (cutoff_iso,),
        ).fetchall()
        updated = []
'''
    if old_select not in host:
        raise SystemExit("host.py promotion SELECT baseline not found")
    host = host.replace(old_select, new_select, 1)

    old_update = '''            changed = db.execute(
                "UPDATE tickets SET status='waiting',workflow_eligible=1,failure_class='interrupted',failure_message=?,updated_at=? WHERE ticket_id=? AND status='accepted' AND workflow_eligible=0",
                (reason[:2000], stamp, ticket_id),
            )
'''
    new_update = '''            changed = db.execute(
                "UPDATE tickets SET status='waiting',workflow_eligible=1,failure_class='interrupted',failure_message=?,updated_at=? "
                f"WHERE ticket_id=? AND status='accepted' AND workflow_eligible=0{direct_guard}",
                (reason[:2000], stamp, ticket_id),
            )
'''
    if old_update not in host:
        raise SystemExit("host.py promotion UPDATE baseline not found")
    host = host.replace(old_update, new_update, 1)
    host_path.write_text(host, encoding="utf-8", newline="\n")


ticket = ticket_path.read_text(encoding="utf-8")
old_fence = '''export function ticketIntakeEligible(prompt: string) {
  return !/\\[(?:CogentNexus|Subagent) Context\\]|\\[CogentNexus (?:Delivery|Continuation):|cogent-workflow-result-|cogent-resume-|The previous run was interrupted\\./iu.test(prompt);
}
'''
new_fence = '''export function ticketIntakeEligible(prompt: string) {
  return !/#cogent-direct\\b|\\[(?:CogentNexus|Subagent) Context\\]|\\[CogentNexus (?:Delivery|Continuation):|cogent-workflow-result-|cogent-resume-|The previous run was interrupted\\./iu.test(prompt);
}
'''
if "#cogent-direct\\b" not in ticket:
    if old_fence not in ticket:
        raise SystemExit("ticketIntakeEligible baseline not found")
    ticket = ticket.replace(old_fence, new_fence, 1)
    ticket_path.write_text(ticket, encoding="utf-8", newline="\n")
