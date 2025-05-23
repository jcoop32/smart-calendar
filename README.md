# Smart Calendar Application

This is a desktop calendar application built with Kivy, designed to provide a customizable monthly view with integration for Google Calendar and Apple Calendar events.

## Features

* **Monthly Calendar View**: Displays a clear monthly calendar with highlighted current day.
* **Google Calendar Integration**: Fetches and displays events from your primary Google Calendar.
* **Apple Calendar (iCloud) Integration**: Connects to iCloud calendars to fetch events (currently prints to console; not integrated into UI).
* **Customizable Colors**: Easy modification of UI colors through a dedicated `colors.py` file.
* **Dynamic Event Display**: Event text is positioned under the date number, with adjustable spacing between multiple events on the same day.
* **Event Backgrounds**: Events can have a configurable background color for better visual distinction.
* **Responsive Layout**: Designed for a 1920x1080 resolution.

## Prerequisites

Before running the application, ensure you have the following installed:

* Python 3.x
* The required Python libraries listed in `requirements.txt`

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd smart-calendar
    ```
    *(Note: Replace `<repository_url>` with the actual URL if this project is hosted.)*

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```


## Configuration

This application uses environment variables for API keys. Create a `.env` file in the root directory (where `main.py` is located) with the following content:

```ini
GOOGLE_CLIENT_ID="YOUR_GOOGLE_CLIENT_ID"
GOOGLE_CLIENT_SECRET="YOUR_GOOGLE_CLIENT_SECRET"
GOOGLE_REFRESH_TOKEN="YOUR_GOOGLE_REFRESH_TOKEN"
GOOGLE_ACCESS_TOKEN="YOUR_GOOGLE_ACCESS_TOKEN"
josh_icloud="YOUR_ICLOUD_USERNAME"
josh_icloud_password="YOUR_ICLOUD_APP_SPECIFIC_PASSWORD"
```


* **Google Calendar API**:
    * Follow the Google Calendar API Python quickstart guide to enable the API and obtain your `CLIENT_ID`, `CLIENT_SECRET`.
    * For `REFRESH_TOKEN` and `ACCESS_TOKEN`, you'll typically get these after the initial OAuth 2.0 authorization flow. The provided code assumes you have these already.
* **Apple Calendar (iCloud) API**:
    * `josh_icloud`: Your Apple ID (iCloud username).
    * `josh_icloud_password`: An app-specific password generated from your Apple ID account settings.

## Usage

To run the application, execute `main.py`:

```bash
python main.py
```


The calendar window should appear, displaying the current month and fetching events.

## Project Structure

```
smart-calendar/
├── api/
│   ├── utils/
│   │   └── google_events_formatter.py   # Formats Google Calendar events
│   ├── apple_calendar.py              # Handles Apple Calendar (iCloud) API interactions
│   └── google_calendar.py             # Handles Google Calendar API interactions
├── colors.py                          # Defines a dictionary of colors used in the application
├── main.py                            # Main application entry point and Kivy App setup
├── calendar_widget.py                 # Kivy widget for the overall calendar grid and event population
├── calendar_day_cell.py               # Kivy widget for individual day cells in the calendar grid
├── test.py                            # A simple test Kivy application (for development/testing purposes)
└── requirements.txt                   # List of Python dependencies
```

## Customization

* **Colors**: Modify the `COLORS` dictionary in `colors.py` to change the application's color scheme. Remember to use normalized RGBA values (0.0-1.0).
* **Event Text Styling**:
    * In `calendar_widget.py`, you can adjust the `font_size`, `color`, `halign`, `valign`, and `padding` of the `event_label`.
    * The background color for events can be changed by modifying `Color(*COLORS["lightgray"])` to any other color defined in `colors.py`.
* **Day Cell Layout**: In `calendar_day_cell.py`, you can modify `padding` and `spacing` of the `DayCell` and its internal `event_box` to adjust the layout and spacing of elements within each day cell. The `height` of the `date_anchor` can also be adjusted for date number spacing.

## Notes and Future Enhancements

* The Apple Calendar integration in `api/apple_calendar.py` currently only prints event details to the console. To fully integrate it into the UI, you would need to adapt the `group_events_by_day` logic (similar to Google Calendar) and add the fetched Apple events to the `DayCell`'s `event_box`.
* Error handling for API calls could be made more robust (e.g., displaying user-friendly messages for network issues or authentication failures).
