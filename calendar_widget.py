from kivy.uix.gridlayout import GridLayout

import calendar

from colors import COLORS
from calendar_day_cell import DayCell
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle  # Ensure Color and Rectangle are imported


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

        # Initialize color attributes for customization
        self.current_day_bg_color = COLORS["lightgray"]
        self.default_day_bg_color = COLORS["white"]
        self.date_text_color = COLORS["black"]
        self.event_bg_color = COLORS["gray"]
        self.event_text_color = COLORS["black"]

        self.build_calendar()

    def build_calendar(self):
        # Clear existing widgets before rebuilding
        self.clear_widgets()

        year = self.current_year
        month = self.current_month
        current_day = self.current_day
        for day in ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]:
            self.add_widget(Label(text=day, bold=True, font_size=48))

        days = calendar.monthcalendar(year, month)
        for week in days:
            for day in week:
                bg_color = (
                    self.current_day_bg_color
                    if day == current_day
                    else self.default_day_bg_color
                )
                day_cell = (
                    DayCell(
                        day_num=day,
                        bg_color=bg_color,
                        date_text_color=self.date_text_color,
                    )
                    if day != 0
                    else DayCell(
                        day_num="",
                        bg_color=bg_color,
                        date_text_color=self.date_text_color,  # Use date_text_color here too for empty cells
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
                            font_size="16sp",
                            color=self.event_text_color,  # Use event_text_color
                            halign="left",
                            valign="top",  # Ensure this is uncommented
                            size_hint_y=None,  # Ensure this is uncommented
                            padding=(5, 2),  # Ensure this is uncommented
                        )
                        # This correctly binds the Label's size to its text_size for wrapping
                        event_label.bind(size=event_label.setter("text_size"))

                        # Add background color
                        with event_label.canvas.before:
                            Color(*self.event_bg_color)  # Use event_bg_color
                            event_label.rect = Rectangle(
                                size=event_label.size, pos=event_label.pos
                            )
                        # Corrected binding: use lambda functions to directly set rectangle properties
                        event_label.bind(
                            pos=lambda instance, value: setattr(
                                event_label.rect, "pos", value
                            )
                        )
                        event_label.bind(
                            size=lambda instance, value: setattr(
                                event_label.rect, "size", value
                            )
                        )

                        day_cell.event_box.add_widget(event_label)

                self.add_widget(day_cell)

    def update_colors(self, new_color_settings):
        # Update the color attributes based on selections from the popup
        self.current_day_bg_color = COLORS[new_color_settings["Current Day Background"]]
        self.default_day_bg_color = COLORS[new_color_settings["Default Day Background"]]
        self.date_text_color = COLORS[new_color_settings["Date Text Color"]]
        self.event_bg_color = COLORS[new_color_settings["Event Background Color"]]
        self.event_text_color = COLORS[new_color_settings["Event Text Color"]]

        # Rebuild the calendar with the new colors
        self.build_calendar()
