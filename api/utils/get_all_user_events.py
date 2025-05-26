import os
from dotenv import load_dotenv

from api.google_calendar import get_google_events
from api.apple_calendar import get_apple_events

from api.utils.combined_events import combined_events

load_dotenv()


def get_all_user_events(users):
    all_combined_events = {}

    for user_prefix in users:
        name = user_prefix.replace("_", " ").title()
        google_creds_data = {
            "client_id": os.getenv("GOOGLE_CLIENT_ID"),
            "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
            "refresh_token": os.getenv(f"{user_prefix}_GOOGLE_REFRESH_TOKEN"),
            "token": os.getenv(f"{user_prefix}_GOOGLE_ACCESS_TOKEN"),
            "token_uri": "https://oauth2.googleapis.com/token",
            "scopes": ["https://www.googleapis.com/auth/calendar.readonly"],
        }
        if not (
            google_creds_data["client_id"]
            and google_creds_data["client_secret"]
            and google_creds_data["refresh_token"]
            and google_creds_data["token"]
        ):
            google_calendar_events = {}
        else:
            google_calendar_events = get_google_events(google_creds_data, name)

        # Apple Credentials for current user
        icloud_username = os.getenv(f"{user_prefix}_ICLOUD_EMAIL")
        icloud_password = os.getenv(f"{user_prefix}_ICLOUD_PASSWORD")
        if not (icloud_username and icloud_password):
            apple_calendar_events = {}
        else:
            apple_calendar_events = get_apple_events(
                icloud_username, icloud_password, name
            )

        # Combine events for the current user
        user_events = combined_events(google_calendar_events, apple_calendar_events)

        # merge current user's events into the overall combined events
        for day, events_list in user_events.items():
            all_combined_events.setdefault(day, []).extend(events_list)
    return all_combined_events
