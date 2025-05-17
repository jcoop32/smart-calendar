from datetime import datetime, timezone
import os
from dotenv import load_dotenv
import calendar

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

load_dotenv()

creds_data = {
    "client_id": os.getenv("GOOGLE_CLIENT_ID"),
    "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
    "refresh_token": os.getenv("GOOGLE_REFRESH_TOKEN"),
    "token": os.getenv("GOOGLE_ACCESS_TOKEN"),
    "token_uri": "https://oauth2.googleapis.com/token",
    "scopes": ["https://www.googleapis.com/auth/calendar.readonly"],
}

# If modifying these scopes, delete the file token.json.

today = datetime.today()
year = today.year
month = today.month

total_days_in_month = calendar.monthrange(year, month)[1]

remaining_days = total_days_in_month - today.day


def main():
    creds = Credentials.from_authorized_user_info(creds_data)
    max_events = remaining_days

    try:
        service = build("calendar", "v3", credentials=creds)
        # Call the Calendar API
        now = datetime.now(tz=timezone.utc).isoformat()
        print(f"Getting the upcoming {max_events} events")
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                maxResults=max_events,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            print("No upcoming events found.")
            return

        # Prints the start and name of the next 10 events
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            print(start, event["summary"])

    except HttpError as error:
        print(f"An error occurred: {error}")


main()
