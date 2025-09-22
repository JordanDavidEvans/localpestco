from pathlib import Path

location_dir = Path('content/locations')
for path in location_dir.glob('*.md'):
    text = path.read_text()
    updated = text
    updated = updated.replace(
        'Same or next-day service across',
        'Visits are scheduled around regular service runs across'
    )
    updated = updated.replace(
        'Same or next-day support across',
        'Support is booked around regular service runs across'
    )
    updated = updated.replace(
        'Most jobs happen the same or next day. I’ll confirm timing when you call or email. If weather slows things down, I’ll keep you updated.',
        'Bookings are slotted into my existing run so I can cover the region efficiently. I’ll confirm the first available time when you call or email and keep you updated if weather or other jobs shift the plan.'
    )
    updated = updated.replace(
        'I aim to provide same or next-day service where possible.',
        'I schedule work around existing runs and will let you know the first available time when you get in touch.'
    )
    if updated != text:
        path.write_text(updated)

services_page = Path('content/services.md')
if services_page.exists():
    text = services_page.read_text()
    updated = text.replace(
        'Yes, I strive to offer same-day or next-day visits across the Tweed Coast.',
        'I book jobs into planned runs across the Tweed Coast and will confirm the first available slot when you call or email.'
    )
    if updated != text:
        services_page.write_text(updated)
