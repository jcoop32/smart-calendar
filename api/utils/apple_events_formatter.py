from datetime import datetime, date


def group_apple_events_by_day(events, name):
    events_by_day = {}

    for event in events:
        curr_event = event.vobject_instance.vevent

        summary_prop = getattr(curr_event, "summary", None)
        event_name = summary_prop.value if summary_prop else "No title"

        dtstart_prop = getattr(curr_event, "dtstart", None)

        if not dtstart_prop:
            continue

        start_date = dtstart_prop.value

        formatted_time = ""
        event_day = None

        # Determine if it's an all-day event or has specific times
        if isinstance(start_date, datetime):
            event_day = start_date.day
            formatted_time = start_date.strftime("%-I:%M %p")
        elif isinstance(start_date, date):
            # It's an all-day event (date object)
            event_day = start_date.day
            formatted_time = "All-day"
        else:
            continue

        if event_day is not None:
            events_by_day.setdefault(event_day, []).append(
                f"{event_name} - {formatted_time} ({name})"
            )

    return events_by_day
