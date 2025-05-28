from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

import datetime


from kivy.uix.label import Label

from kivy.config import Config

Config.set("graphics", "width", "1920")
Config.set("graphics", "height", "1080")


# user names from .env
users = ["JOSHUA", "TRA_MY", "MOM", "KAYLA"]


class CalendarApp(App):
    def build(self):
        self.current_datetime = datetime.datetime.now()
        self.current_year = self.current_datetime.year
        self.current_month = self.current_datetime.month
        self.current_day = self.current_datetime.day
        self.current_month_name = self.current_datetime.strftime("%B")
        month_year = f"{self.current_month_name} {self.current_year}"
        root = BoxLayout(orientation="vertical", padding=10, spacing=10)

        # --- Month Navigation and Display ---
        nav_layout = BoxLayout(size_hint_y=0.1, spacing=10)

        # Left arrow button for previous month
        self.prev_month_btn = Button(text="<", font_size=48, size_hint_x=0.1)
        self.prev_month_btn.bind(on_press=self.go_to_previous_month)
        nav_layout.add_widget(self.prev_month_btn)

        # Month and Year display label
        self.month_year_label = Label(text=month_year, font_size=48, size_hint_x=0.8)
        nav_layout.add_widget(self.month_year_label)

        # Right arrow button for next month
        self.next_month_btn = Button(text=">", font_size=48, size_hint_x=0.1)
        self.next_month_btn.bind(on_press=self.go_to_next_month)
        nav_layout.add_widget(self.next_month_btn)

        root.add_widget(nav_layout)

        self.calendar_widget_instance = CalendarWidget(
            current_year=self.current_year,
            current_month=self.current_month,
            current_day=self.current_day,
            users=users,
        )
        root.add_widget(self.calendar_widget_instance)
        return root

    def update_month_display(self):
        """Updates the month/year label and triggers calendar widget update."""
        month_name = datetime.date(self.current_year, self.current_month, 1).strftime(
            "%B"
        )
        self.month_year_label.text = f"{month_name} {self.current_year}"

        # Trigger the calendar_widget to update for the new month
        self.calendar_widget_instance.set_month_year(
            self.current_year, self.current_month, self.current_day
        )

    def go_to_previous_month(self, instance):
        """Calculates previous month and updates display."""
        if self.current_month == 1:  # January
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.update_month_display()

    def go_to_next_month(self, instance):
        """Calculates next month and updates display."""
        if self.current_month == 12:  # December
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.update_month_display()


if __name__ == "__main__":
    from widgets.calendar_widget import CalendarWidget

    CalendarApp().run()
