from datetime import datetime, timezone

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.exceptions import RefreshError


from api.utils.google_events_formatter import group_google_events_by_day

# from utils.google_events_formatter import group_google_events_by_day


def get_google_events(creds_data, target_year, target_month):
    creds = Credentials.from_authorized_user_info(creds_data)
    try:
        # Calculate start and end of the target month based on parameters
        start_of_month = datetime(target_year, target_month, 1, tzinfo=timezone.utc)
        if target_month == 12:
            next_month = datetime(target_year + 1, 1, 1, tzinfo=timezone.utc)
        else:
            next_month = datetime(target_year, target_month + 1, 1, tzinfo=timezone.utc)

        time_min = start_of_month.isoformat()
        time_max = next_month.isoformat()
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

    except RefreshError as error:
        print(
            f"Google Token Refresh Error: {error}. Please ensure your Google credentials are valid and up-to-date, and that your Client ID/Secret are correctly configured."
        )
        return {}
    except HttpError as error:
        print(f"An HTTP error occurred with Google Calendar: {error}")
        return {}
    except Exception as error:
        print(
            f"An unexpected error occurred while fetching Google Calendar events: {error}"
        )
        return {}


# print(get_google_events())
