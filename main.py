from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

import datetime

from widgets.calendar_widget import CalendarWidget

from kivy.uix.label import Label

from kivy.config import Config

Config.set("graphics", "width", "1920")
Config.set("graphics", "height", "1080")


current_datetime = datetime.datetime.now()
month_name = current_datetime.strftime("%B")
current_year = current_datetime.year
current_month = current_datetime.month
current_day = current_datetime.day
# user names from .env
users = ["JOSHUA", "TRA_MY", "MOM", "KAYLA"]


class CalendarApp(App):
    def build(self):
        month_year = f"{month_name} {current_year}"
        root = BoxLayout(orientation="vertical", padding=10, spacing=10)
        root.add_widget(Label(text=str(month_year), font_size=48, size_hint_y=0.1))
        root.add_widget(
            CalendarWidget(
                current_year=current_year,
                current_month=current_month,
                current_day=current_day,
                users=users,
            )
        )
        return root


if __name__ == "__main__":
    CalendarApp().run()
