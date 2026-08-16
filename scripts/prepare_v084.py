from pathlib import Path

path = Path('docs/BASELINE.md')
text = path.read_text(encoding='utf-8')
old_failed = '- A failed delivery receipt promotes unfinished direct work to durable recovery.'
new_failed = '- A failed delivery receipt queues bounded DIRECT redelivery/recovery for unfinished direct work; interruption alone does not require STAGED execution.'
old_timeout = '- A `RESPONSE_READY` Ticket with no delivery confirmation before the receipt deadline is promoted to durable recovery rather than silently completed.'
new_timeout = '- A `RESPONSE_READY` DIRECT Ticket with no delivery confirmation before the receipt deadline enters bounded DIRECT redelivery/recovery rather than being silently completed or automatically promoted to STAGED execution.'
if old_failed not in text or old_timeout not in text:
    raise SystemExit('Delivery Commit Gate wording anchors not found')
text = text.replace(old_failed, new_failed, 1).replace(old_timeout, new_timeout, 1)
path.write_text(text, encoding='utf-8')
