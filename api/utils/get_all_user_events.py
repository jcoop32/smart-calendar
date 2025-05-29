import os
from dotenv import load_dotenv

from api.google_calendar import get_google_events
from api.apple_calendar import get_apple_events

from api.utils.combined_events import combined_events

# database
from api.utils.db_cache import save_events_to_cache, load_events_from_cache, init_db

import random
from colors import HIGHLIGHTED_COLORS

load_dotenv()


def get_all_user_events(users, target_year, target_month):
    all_combined_events = {}

    for user_prefix in users:
        name = user_prefix.replace("_", " ").title()

        cache_user_events = load_events_from_cache(
            user_prefix=user_prefix, year=target_year, month=target_month
        )

        if cache_user_events is not None:
            for day, events_list in cache_user_events.items():
                all_combined_events.setdefault(day, []).extend(events_list)
            continue

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
            google_calendar_events = get_google_events(
                google_creds_data, target_year, target_month
            )

        # Apple Credentials for current user
        icloud_username = os.getenv(f"{user_prefix}_ICLOUD_EMAIL")
        icloud_password = os.getenv(f"{user_prefix}_ICLOUD_PASSWORD")
        if not (icloud_username and icloud_password):
            apple_calendar_events = {}
        else:
            apple_calendar_events = get_apple_events(
                icloud_username, icloud_password, target_year, target_month
            )

        # Combine events for the current user
        user_events = combined_events(google_calendar_events, apple_calendar_events)

        user_color = (
            random.choice(list(HIGHLIGHTED_COLORS.values()))
            if name != "Tra My"
            else HIGHLIGHTED_COLORS["pink"]
        )

        formatted_user_events = {}
        # merge current user's events into the overall combined events
        for day, events_list_from_api in user_events.items():
            formatted_day_events = [
                {"title": f"{event_title} ({name})", "color": user_color}
                for event_title in events_list_from_api
            ]
            formatted_user_events[day] = formatted_day_events
            # all_combined_events.setdefault(day, []).extend(formatted_day_events)
        save_events_to_cache(
            user_prefix=user_prefix,
            year=target_year,
            month=target_month,
            events_by_day=formatted_user_events,
        )
        for day, events_list_to_add in formatted_user_events.items():
            all_combined_events.setdefault(day, []).extend(events_list_to_add)

    return all_combined_events
