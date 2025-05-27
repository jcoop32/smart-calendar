from datetime import datetime


def group_google_events_by_day(events):
    events_by_day = {}

    for event in events:
        start = event.get("start", {})
        summary = event.get("summary", "No title")

        # support both dateTime and all-day events
        if "dateTime" in start:
            dt = datetime.fromisoformat(start["dateTime"])
        elif "date" in start:
            dt = datetime.fromisoformat(start["date"])
        else:
            continue

        formatted_time = dt.strftime("%-I:%M %p")
        if formatted_time == "12:00 AM":
            formatted_time = "All Day"

        day = dt.day
        events_by_day.setdefault(day, []).append(f"{summary} - {formatted_time}")

    return events_by_day
