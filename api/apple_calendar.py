from caldav import DAVClient
from datetime import datetime, timedelta
import os
import logging

from dotenv import load_dotenv

from api.utils.apple_events_formatter import group_apple_events_by_day

# from utils.apple_events_formatter import group_apple_events_by_day

# Suppress warnings from the root logger
# This will prevent messages with severity WARNING or lower from being displayed.
logging.getLogger().setLevel(logging.ERROR)

load_dotenv()

today = datetime.today()
year = today.year
month = today.month

# Calculate the first day of the current month
start_of_month = datetime(year, month, 1)

# Calculate the last day of the current month
if month == 12:
    end_of_month = datetime(year + 1, 1, 1) - timedelta(days=1)
else:
    end_of_month = datetime(year, month + 1, 1) - timedelta(days=1)

# icloud username and an app-specific password
client = DAVClient(
    url="https://caldav.icloud.com/",
    username=os.getenv("josh_icloud"),
    password=os.getenv("josh_icloud_password"),
)

principal = client.principal()
calendars = principal.calendars()


def get_apple_events():
    all_raw_events = []
    for calendar_obj in calendars:
        events = calendar_obj.date_search(start=start_of_month, end=end_of_month)
        all_raw_events.extend(events)  # collect all events from all calendars

    formatted_events = group_apple_events_by_day(all_raw_events)
    return formatted_events
