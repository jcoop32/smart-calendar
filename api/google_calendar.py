from datetime import datetime, timezone
import os
from dotenv import load_dotenv

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from api.utils.google_events_formatter import group_google_events_by_day

# from utils.google_events_formatter import group_google_events_by_day

load_dotenv()

creds_data = {
    "client_id": os.getenv("GOOGLE_CLIENT_ID"),
    "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
    "refresh_token": os.getenv("GOOGLE_REFRESH_TOKEN"),
    "token": os.getenv("GOOGLE_ACCESS_TOKEN"),
    "token_uri": "https://oauth2.googleapis.com/token",
    "scopes": ["https://www.googleapis.com/auth/calendar.readonly"],
}


today = datetime.now(tz=timezone.utc)
year = today.year
month = today.month

# Start of current month
start_of_month = datetime(year, month, 1, tzinfo=timezone.utc)

# Start of next month
if month == 12:
    next_month = datetime(year + 1, 1, 1, tzinfo=timezone.utc)
else:
    next_month = datetime(year, month + 1, 1, tzinfo=timezone.utc)

# Format to ISO 8601
time_min = start_of_month.isoformat()
time_max = next_month.isoformat()


def get_google_events():
    creds = Credentials.from_authorized_user_info(creds_data)

    try:
        service = build("calendar", "v3", credentials=creds)
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=time_min,
                timeMax=time_max,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        formatted_events = group_google_events_by_day(events)

        return formatted_events

    except HttpError as error:
        print(f"An error occurred: {error}")
