from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button  # Import Button for the new customization button
from kivy.uix.label import Label

import datetime

from colors import COLORS
from calendar_widget import CalendarWidget
from customization_popup import CustomizationPopup  # Import the new popup class

from kivy.config import Config

Config.set("graphics", "width", "1920")
Config.set("graphics", "height", "1080")


current_datetime = datetime.datetime.now()
month_name = current_datetime.strftime("%B")
current_year = current_datetime.year
current_month = current_datetime.month
current_day = current_datetime.day


class CalendarApp(App):
    # Store a reference to the CalendarWidget instance so we can update it
    calendar_widget_instance = None

    def build(self):
        month_year = f"{month_name} {current_year}"
        root = BoxLayout(orientation="vertical", padding=10, spacing=10)

        # Create a top bar layout for the month/year label and the customize button
        top_bar = BoxLayout(orientation="horizontal", size_hint_y=0.1)
        top_bar.add_widget(Label(text=str(month_year), font_size=48, size_hint_x=0.8))

        # Add the Customize button
        customize_button = Button(
            text="Customize", size_hint_x=0.2, on_release=self.open_customization_popup
        )
        top_bar.add_widget(customize_button)
        root.add_widget(top_bar)

        # Create and store the CalendarWidget instance
        self.calendar_widget_instance = CalendarWidget(
            current_year=current_year,
            current_month=current_month,
            current_day=current_day,
        )
        root.add_widget(self.calendar_widget_instance)
        return root

    def open_customization_popup(self, instance):
        # Create an instance of your custom popup
        popup = CustomizationPopup(apply_callback=self.apply_customization_changes)
        popup.open()  # Show the popup

    def apply_customization_changes(self, selected_colors):
        # This method is called by the CustomizationPopup when "Apply" is pressed.
        # 'selected_colors' is a dictionary like {"Element Name": "color_key_string"}

        # Pass the selected color keys to the CalendarWidget instance
        if self.calendar_widget_instance:
            self.calendar_widget_instance.update_colors(selected_colors)


if __name__ == "__main__":
    CalendarApp().run()
