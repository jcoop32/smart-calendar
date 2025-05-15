from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

import calendar
import datetime

from kivy.uix.label import Label
from kivy.uix.button import Button

from kivy.config import Config

Config.set("graphics", "width", "1920")
Config.set("graphics", "height", "1080")


current_datetime = datetime.datetime.now()
month_name = current_datetime.strftime("%B")
current_month = current_datetime.month
current_year = current_datetime.year


class CalendarWidget(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 7
        self.padding = 5
        self.spacing = 5
        calendar.setfirstweekday(calendar.SUNDAY)
        self.build_calendar()

    def build_calendar(self, year=current_year, month=current_month):
        for day in ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]:
            self.add_widget(Label(text=day, bold=True, font_size=48))

        days = calendar.monthcalendar(year, month)
        for week in days:
            for day in week:
                if day != 0:
                    label = str(day)
                else:
                    label = ""
                self.add_widget(Button(text=label, font_size=48))


class CalendarApp(App):
    def build(self):
        month_year = f"{month_name} {current_year}"
        root = BoxLayout(orientation="vertical", padding=10, spacing=10)
        root.add_widget(Label(text=str(month_year), font_size=48, size_hint_y=0.1))
        root.add_widget(CalendarWidget())
        return root


if __name__ == "__main__":
    CalendarApp().run()
