#!/usr/bin/env python3
from pathlib import Path

path = Path(__file__).with_name("apply_delivery_compaction_patch.py")
text = path.read_text(encoding="utf-8")
old1 = '''    text, count = re.subn(\n        r"function markCompletionDelivered\\([\\s\\S]*?\\nexport function ticketOutboxTag",\n        delivery_block + "\\nexport function ticketOutboxTag",\n        text,\n        count=1,\n    )'''
new1 = '''    text, count = re.subn(\n        r"function markCompletionDelivered\\([\\s\\S]*?\\nexport function ticketOutboxTag",\n        lambda _match: delivery_block + "\\nexport function ticketOutboxTag",\n        text,\n        count=1,\n    )'''
old2 = '''    text, count = re.subn(\n        r"export async function deliverTicketOutbox\\([\\s\\S]*?\\n}\\n\\nexport function enforcementDecision",\n        ticket_delivery + "\\nexport function enforcementDecision",\n        text,\n        count=1,\n    )'''
new2 = '''    text, count = re.subn(\n        r"export async function deliverTicketOutbox\\([\\s\\S]*?\\n}\\n\\nexport function enforcementDecision",\n        lambda _match: ticket_delivery + "\\nexport function enforcementDecision",\n        text,\n        count=1,\n    )'''
for label, old, new in (("workflow", old1, new1), ("ticket", old2, new2)):
    if old not in text:
        raise SystemExit(f"missing {label} replacement anchor")
    text = text.replace(old, new, 1)
path.write_text(text, encoding="utf-8")
print("patch helper escaping fixed")
