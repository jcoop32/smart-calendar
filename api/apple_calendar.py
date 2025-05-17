from caldav import DAVClient
from datetime import datetime, timedelta
import os
import calendar

from dotenv import load_dotenv

load_dotenv()

today = datetime.today()
year = today.year
month = today.month

total_days_in_month = calendar.monthrange(year, month)[1]

remaining_days = total_days_in_month - today.day

# Your iCloud username and an app-specific password
client = DAVClient(
    url="https://caldav.icloud.com/",
    username=os.getenv("josh_icloud"),
    password=os.getenv("josh_icloud_password"),
)

principal = client.principal()
calendars = principal.calendars()

print(f"Found {len(calendars)} calendars")

for calendar in calendars:
    events = calendar.date_search(
        start=datetime.now(), end=datetime.now() + timedelta(days=remaining_days)
    )
    for event in events:
        curr_event = event.vobject_instance.vevent
        event_name = curr_event.summary.value
        start_date = curr_event.dtstart.value

        end_date = curr_event.dtend.value

        if isinstance(start_date, datetime):
            end_time = end_date.strftime("%I:%M %p")
            formatted_time = f'{start_date.strftime("%I:%M %p")} (ends at {end_time})'
        else:
            formatted_time = "All-day"

        print(f"{event_name} - {formatted_time}\n")
