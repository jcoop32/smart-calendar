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
        self.padding = 5
        self.spacing = 5
        self.current_year = current_year
        self.current_month = current_month
        self.current_day = current_day
        self.users = users

        calendar.setfirstweekday(calendar.SUNDAY)
        self.initialize_calendar_grid()
        threading.Thread(target=self._fetch_and_display_events, daemon=True).start()

    def initialize_calendar_grid(self):
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
                self.add_widget(day_cell)
        self.day_cells = self.children[:-7][::-1]

    def _fetch_and_display_events(self):
        all_events = get_all_user_events(self.users)
        # all_events = {
        #     16: [
        #         {
        #             "title": "Flight - 6:30 AM (Joshua)",
        #             "color": (0.25098, 0.87843, 0.81569, 0.5),
        #         },
        #         {
        #             "title": "Leave for Cancun - 5:00 AM (Joshua)",
        #             "color": (0.25098, 0.87843, 0.81569, 0.5),
        #         },
        #     ],
        #     21: [
        #         {
        #             "title": "Come back from mexico - 7:00 AM (Joshua)",
        #             "color": (0.25098, 0.87843, 0.81569, 0.5),
        #         },
        #         {
        #             "title": "Come back from Cancun  - 7:00 PM (Joshua)",
        #             "color": (0.25098, 0.87843, 0.81569, 0.5),
        #         },
        #     ],
        #     22: [
        #         {
        #             "title": "Chill with Tra My - All Day (Joshua)",
        #             "color": (0.25098, 0.87843, 0.81569, 0.5),
        #         },
        #         {
        #             "title": "Go to Costco - 4:15 PM (Joshua)",
        #             "color": (0.25098, 0.87843, 0.81569, 0.5),
        #         },
        #         {
        #             "title": "Eat dinner - 7:15 PM (Joshua)",
        #             "color": (0.25098, 0.87843, 0.81569, 0.5),
        #         },
        #     ],
        #     24: [
        #         {
        #             "title": "Go Back Home - 11:00 AM (Joshua)",
        #             "color": (0.25098, 0.87843, 0.81569, 0.5),
        #         }
        #     ],
        #     15: [
        #         {
        #             "title": "Moms birthday - All-day (Joshua)",
        #             "color": (0.25098, 0.87843, 0.81569, 0.5),
        #         },
        #         {
        #             "title": "Adams Birthday - 1:00 PM (Mom)",
        #             "color": (0.50196, 0.0, 0.50196, 0.5),
        #         },
        #     ],
        #     5: [
        #         {
        #             "title": "MATH 410  John T. Rettaliata Engg Center | Room 121 - 3:15 PM (Joshua)",
        #             "color": (0.25098, 0.87843, 0.81569, 0.5),
        #         }
        #     ],
        #     2: [
        #         {
        #             "title": "CS 485 Stuart Rm 108 - 10:00 AM (Joshua)",
        #             "color": (0.25098, 0.87843, 0.81569, 0.5),
        #         },
        #         {
        #             "title": "CS 430 Recitation PH 108 - 1:50 PM (Joshua)",
        #             "color": (0.25098, 0.87843, 0.81569, 0.5),
        #         },
        #     ],
        #     1: [
        #         {
        #             "title": "CS 430 Pritzker Rm 129 - 1:50 PM (Joshua)",
        #             "color": (0.25098, 0.87843, 0.81569, 0.5),
        #         },
        #         {
        #             "title": "Patho Final Exam - 4:15 PM (Tra My)",
        #             "color": (0.0, 1.0, 0.0, 0.5),
        #         },
        #     ],
        # }
        # Update UI on main thread
        self._update_calendar_with_events_on_mainthread(all_events)

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
