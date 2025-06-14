from caldav import DAVClient
from datetime import datetime, timezone, timedelta
import logging


from api.utils.apple_events_formatter import group_apple_events_by_day

# from utils.apple_events_formatter import group_apple_events_by_day

# Suppress warnings from the root logger
# This will prevent messages with severity WARNING or lower from being displayed.
logging.getLogger().setLevel(logging.ERROR)


def get_apple_events(icloud_email, icloud_password, target_year, target_month):
    try:
        # Make datetimes timezone-aware (UTC)
        start_of_month = datetime(target_year, target_month, 1, tzinfo=timezone.utc)
        if target_month == 12:
            end_of_month = datetime(
                target_year + 1, 1, 1, tzinfo=timezone.utc
            ) - timedelta(days=1)
        else:
            end_of_month = datetime(
                target_year, target_month + 1, 1, tzinfo=timezone.utc
            ) - timedelta(days=1)
        client = DAVClient(
            url="https://caldav.icloud.com/",
            username=icloud_email,
            password=icloud_password,
        )

        principal = client.principal()
        calendars = principal.calendars()

        all_raw_events = []
        for calendar_obj in calendars:
            events = calendar_obj.date_search(start=start_of_month, end=end_of_month)
            all_raw_events.extend(events)

        formatted_events = group_apple_events_by_day(all_raw_events)
        return formatted_events
    except Exception as e:
        print(f"An error occurred with Apple Calendar for user {icloud_email}: {e}")
        return {}


# print(get_apple_events())
