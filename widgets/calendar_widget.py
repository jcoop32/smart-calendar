from kivy.uix.gridlayout import GridLayout

import calendar

from colors import COLORS
from widgets.calendar_day_cell import DayCell
from kivy.uix.label import Label

import threading
from kivy.clock import mainthread

from api.utils.get_all_user_events import get_all_user_events

from widgets.event_label import EventLabel


class CalendarWidget(GridLayout):

    def __init__(self, current_year, current_month, current_day, users, **kwargs):
        super().__init__(**kwargs)
        self.cols = 7
        self.spacing = 3
        self.current_year = current_year
        self.current_month = current_month
        self.current_day = current_day
        self.users = users

        calendar.setfirstweekday(calendar.SUNDAY)
        self.init_calendar_grid()
        threading.Thread(target=self._fetch_and_display_events, daemon=True).start()

    def init_calendar_grid(self):
        self.clear_widgets()
        for day in ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]:
            self.add_widget(Label(text=day, bold=True, font_size=48))

        days = calendar.monthcalendar(self.current_year, self.current_month)
        for week in days:
            for day in week:
                bg_color = (
                    COLORS["lightgray"] if day == self.current_day else COLORS["white"]
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
                self.add_widget(day_cell)
        self.day_cells = self.children[:-7][::-1]

    def set_month_year(self, year, month, day_to_highlight):
        self.current_year = year
        self.current_month = month
        self.current_day = day_to_highlight

        self.init_calendar_grid()
        self._load_and_display_events_for_current_month()

    def _fetch_and_display_events(self):
        all_events = get_all_user_events(
            users=self.users,
            target_year=self.current_year,
            target_month=self.current_month,
        )

        # Update UI on main thread
        self._update_calendar_with_events_on_mainthread(all_events)

    def _load_and_display_events_for_current_month(self):
        all_events = get_all_user_events(
            users=self.users,
            target_year=self.current_year,
            target_month=self.current_month,
        )

        if all_events:
            self._update_calendar_with_events_on_mainthread(all_events)
        else:
            threading.Thread(
                target=self._fetch_and_display_events,
                args=(
                    self.current_year,
                    self.current_month,
                ),
                daemon=True,
            ).start()

    @mainthread
    def _update_calendar_with_events_on_mainthread(self, all_events):
        for day_cell_widget in self.day_cells:
            day_num = day_cell_widget.day_num
            day_cell_widget.event_box.clear_widgets()

            if day_num != 0 and day_num in all_events:
                for event_data in all_events[day_num]:
                    event_label = EventLabel(
                        event_title=event_data["title"], bg_color=event_data["color"]
                    )
                    day_cell_widget.event_box.add_widget(event_label)
