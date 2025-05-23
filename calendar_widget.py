from kivy.uix.gridlayout import GridLayout

import calendar

from colors import COLORS
from calendar_day_cell import DayCell
from kivy.uix.label import Label

from api.google_calendar import get_google_events


class CalendarWidget(GridLayout):

    def __init__(self, current_year, current_month, current_day, **kwargs):
        super().__init__(**kwargs)
        self.cols = 7
        self.padding = 5
        self.spacing = 5
        self.current_year = current_year
        self.current_month = current_month
        self.current_day = current_day

        calendar.setfirstweekday(calendar.SUNDAY)

        self.build_calendar()

    def build_calendar(self):
        year = self.current_year
        month = self.current_month
        current_day = self.current_day
        for day in ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]:
            self.add_widget(Label(text=day, bold=True, font_size=48))

        days = calendar.monthcalendar(year, month)
        for week in days:
            for day in week:
                bg_color = (
                    COLORS["lightgray"] if day == current_day else COLORS["white"]
                )
                day_cell = (
                    DayCell(
                        day_num=day, bg_color=bg_color, date_text_color=COLORS["black"]
                    )
                    if day != 0
                    else DayCell(
                        day_num="",
                        bg_color=bg_color,
                        date_text_color=COLORS["white"],
                    )
                )

                # google_calendar_events = get_google_events()
                google_calendar_events = {
                    16: ["Flight - 6:30 AM"],
                    21: ["Come back from mexico - 7:00 AM"],
                    22: [
                        "Chill with Tra My - 12:00 AM",
                        "Go to Costco - 4:15 PM",
                        "Eat dinner - 7:15 PM",
                    ],
                    24: ["Go Back Home - 11:00 AM"],
                }

                if day in google_calendar_events:
                    for event_title in google_calendar_events[day]:
                        event_label = Label(
                            text=event_title,
                            font_size="14sp",
                            color=COLORS["black"],
                            halign="left",
                            valign="top",
                            padding=(5, 0),
                            # size_hint_y=(1, 0),
                        )
                        event_label.bind(size=event_label.setter("text_size"))
                        day_cell.event_box.add_widget(event_label)

                self.add_widget(day_cell)
