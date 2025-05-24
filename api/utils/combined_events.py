from collections import defaultdict


def combined_events(google_events, apple_events):
    combined_events_raw = defaultdict(list)

    for day, events_list in google_events.items():
        combined_events_raw[day].extend(events_list)

    for day, events_list in apple_events.items():
        combined_events_raw[day].extend(events_list)

    return combined_events_raw
