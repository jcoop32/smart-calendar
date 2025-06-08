from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.properties import StringProperty, NumericProperty
from kivy.metrics import dp  # For density-independent pixels
import os


class WeatherWidget(BoxLayout):
    # Kivy Properties to hold and update the weather data
    city_name = StringProperty("N/A")
    current_temperature = NumericProperty(0.0)
    feels_like_temperature = NumericProperty(0.0)
    condition_text = StringProperty("Loading...")
    humidity_value = NumericProperty(0)
    wind_speed_value = NumericProperty(0.0)
    icon_source = StringProperty("images/default.png")  # Default icon path

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint_y = None  # Don't take full height
        self.height = dp(90)  # Fixed height, adjust as needed for compactness
        self.padding = dp(10)
        self.spacing = dp(10)

        # Set a background color for the widget using canvas instructions
        with self.canvas.before:
            from kivy.graphics import Color, Rectangle

            Color(0.1, 0.1, 0.1, 1)  # Dark background
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_rect, size=self._update_rect)

        # --- Left Section: Weather Icon ---
        self.weather_icon = Image(
            source=self.icon_source,  # Binds to the icon_source property
            size_hint_x=None,
            width=dp(70),
            allow_stretch=True,
            keep_ratio=True,
        )
        self.add_widget(self.weather_icon)
        # Bind the Image source to the property so it updates automatically
        self.bind(icon_source=self.weather_icon.setter("source"))

        # --- Right Section: Weather Details (Vertical BoxLayout) ---
        details_layout = BoxLayout(
            orientation="vertical",
            padding=(dp(5), 0),  # Left/Right padding, 0 for top/bottom
            spacing=dp(2),
        )

        # Row 1: City Name
        self.lbl_city = Label(
            text=self.city_name,
            font_size="20sp",
            color=(1, 1, 1, 1),  # White text
            halign="left",
            valign="top",
            size_hint_y=None,
            height=dp(25),  # Give it a fixed height or let it auto-size
        )
        details_layout.add_widget(self.lbl_city)
        self.bind(
            city_name=self.lbl_city.setter("text")
        )  # Update Label when property changes
        self.lbl_city.bind(
            size=self.lbl_city.setter("text_size")
        )  # Ensure text wraps/aligns correctly

        # Row 2: Temperature & Feels Like (Horizontal BoxLayout)
        temp_feels_layout = BoxLayout(
            orientation="horizontal", size_hint_y=None, height=dp(25)
        )
        self.lbl_temp = Label(
            text=f"{self.current_temperature:.1f}°F",
            font_size="18sp",
            color=(1, 0.8, 0, 1),  # Orange text
            halign="left",
            valign="middle",
        )
        temp_feels_layout.add_widget(self.lbl_temp)
        self.bind(current_temperature=self._update_temp_labels)
        self.lbl_temp.bind(size=self.lbl_temp.setter("text_size"))

        self.lbl_feels_like = Label(
            text=f"(Feels {self.feels_like_temperature:.1f}°F)",
            font_size="14sp",
            color=(0.7, 0.7, 0.7, 1),  # Gray text
            halign="left",
            valign="middle",
        )
        temp_feels_layout.add_widget(self.lbl_feels_like)
        self.bind(feels_like_temperature=self._update_temp_labels)
        self.lbl_feels_like.bind(size=self.lbl_feels_like.setter("text_size"))

        details_layout.add_widget(temp_feels_layout)

        # Row 3: Condition Text
        self.lbl_condition = Label(
            text=self.condition_text,
            font_size="16sp",
            color=(0.9, 0.9, 0.9, 1),  # Light gray text
            halign="left",
            valign="top",
            size_hint_y=None,
            height=dp(25),
        )
        details_layout.add_widget(self.lbl_condition)
        self.bind(condition_text=self.lbl_condition.setter("text"))
        self.lbl_condition.bind(size=self.lbl_condition.setter("text_size"))

        # Row 4: Humidity & Wind (Horizontal BoxLayout)
        hum_wind_layout = BoxLayout(
            orientation="horizontal", size_hint_y=None, height=dp(25)
        )
        self.lbl_humidity = Label(
            text=f"Hum: {self.humidity_value}%",
            font_size="14sp",
            color=(0.8, 0.8, 1, 1),  # Light blue text
            halign="left",
            valign="middle",
        )
        hum_wind_layout.add_widget(self.lbl_humidity)
        self.bind(humidity_value=self.lbl_humidity.setter("text"))
        self.lbl_humidity.bind(size=self.lbl_humidity.setter("text_size"))

        self.lbl_wind = Label(
            text=f"Wind: {self.wind_speed_value:.1f} mph",
            font_size="14sp",
            color=(0.8, 1, 0.8, 1),  # Light green text
            halign="left",
            valign="middle",
        )
        hum_wind_layout.add_widget(self.lbl_wind)
        self.bind(wind_speed_value=self.lbl_wind.setter("text"))
        self.lbl_wind.bind(size=self.lbl_wind.setter("text_size"))

        details_layout.add_widget(hum_wind_layout)

        self.add_widget(details_layout)

        # Set initial dummy data for demonstration
        self.update_weather_data(
            city="Chicago",
            temp=75.5,
            feels_like=78.2,
            condition="Partly Cloudy",
            humidity=65,
            wind_speed=12.3,
            icon_name="cloudy.png",  # Assuming you have images/cloudy.png
        )

    # --- Helper methods for updating ---
    def _update_rect(self, instance, value):
        # Callback to update the background rectangle's position and size
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def _update_temp_labels(self, instance, value):
        # Update text of temperature labels when respective properties change
        self.lbl_temp.text = f"{self.current_temperature:.1f}°F"
        self.lbl_feels_like.text = f"(Feels {self.feels_like_temperature:.1f}°F)"
        # Note: These setters might be automatically handled if you bind directly,
        # but sometimes it's clearer to have a method update multiple labels.

    def update_weather_data(
        self, city, temp, feels_like, condition, humidity, wind_speed, icon_name
    ):
        """
        Method to update all weather data displayed by the widget.
        icon_name should be just the filename (e.g., "sunny.png"),
        the method will prepend the 'images/' path.
        """
        self.city_name = city
        self.current_temperature = temp
        self.feels_like_temperature = feels_like
        self.condition_text = condition
        self.humidity_value = humidity
        self.wind_speed_value = wind_speed
        # Ensure the image path is correct, assuming 'images' folder
        self.icon_source = os.path.join("images", icon_name)
