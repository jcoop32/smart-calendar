from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.properties import StringProperty, NumericProperty
from kivy.metrics import dp  # For density-independent pixels
import os
from colors import COLORS

from api.weather.weather import get_weather


class WeatherWidget(BoxLayout):
    # Kivy Properties to hold and update the weather data
    city_name = StringProperty("N/A")
    region_name = StringProperty("")
    current_temperature = NumericProperty(0)
    feels_like_temperature = NumericProperty(0)
    condition_text = StringProperty("Loading...")
    uv_index = NumericProperty(0)
    wind_direction = StringProperty("")
    humidity_value = NumericProperty(0)
    wind_speed_value = NumericProperty(0)
    icon_name = StringProperty("/api/weather/condition_icons/sunny.png")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint_y = None  # Don't take full height
        self.height = dp(90)  # Fixed height, adjust as needed for compactness
        self.padding = dp(10)
        self.spacing = dp(10)

        # Fetch weather data from the API
        weather_data = get_weather()

        # Pass the weather data into the update function
        self.update_weather_data(*weather_data)

        self.set_background()

        self.add_weather_icon()

        self.add_weather_details()

    def set_background(self):
        """Set background color for the widget"""
        with self.canvas.before:
            from kivy.graphics import Color, Rectangle

            Color(0.1, 0.1, 0.1, 1)  # Dark background
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_rect, size=self._update_rect)

    def add_weather_icon(self):
        """Add the weather icon to the widget"""
        self.weather_icon = Image(
            source="/api/weather/condition_icons/sunny.png",  # Binds to the icon_name property
            size_hint_x=None,
            width=dp(70),
            allow_stretch=True,
            keep_ratio=True,
        )
        self.add_widget(self.weather_icon)

    def add_weather_details(self):
        """Add the weather details such as city, temperature, condition, etc."""
        details_layout = BoxLayout(
            orientation="vertical",
            padding=(dp(5), 0),  # Left/Right padding, 0 for top/bottom
            spacing=dp(2),
        )

        # City Name
        self.lbl_city = Label(
            text=f"{self.city_name}, {self.region_name}",
            font_size="20sp",
            color=COLORS["white"],  # White text
            # halign="left",
            # valign="top",
            size_hint_y=None,
            height=dp(25),
        )
        details_layout.add_widget(self.lbl_city)
        self.bind(city_name=self.lbl_city.setter("text"))
        self.lbl_city.bind(size=self.lbl_city.setter("text_size"))

        # Temperature and Feels Like
        temp_feels_layout = BoxLayout(
            orientation="horizontal", size_hint_y=None, height=dp(25)
        )
        self.lbl_temp = Label(
            text=f"{self.current_temperature:.1f}°F",
            font_size="18sp",
            color=COLORS["orange"],  # Orange text
            halign="left",
            valign="middle",
        )
        temp_feels_layout.add_widget(self.lbl_temp)
        self.bind(current_temperature=self._update_temp_labels)

        self.lbl_feels_like = Label(
            text=f"(Feels like {self.feels_like_temperature:.1f}°F)",
            font_size="14sp",
            color=COLORS["gray"],  # Gray text
            halign="left",
            valign="middle",
        )
        temp_feels_layout.add_widget(self.lbl_feels_like)
        self.bind(feels_like_temperature=self._update_temp_labels)

        details_layout.add_widget(temp_feels_layout)

        # Condition Text
        self.lbl_condition = Label(
            text=self.condition_text,
            font_size="16sp",
            color=COLORS["lightgray"],  # Light gray text
            halign="left",
            valign="top",
            size_hint_y=None,
            height=dp(25),
        )
        details_layout.add_widget(self.lbl_condition)
        self.bind(condition_text=self.lbl_condition.setter("text"))

        # Humidity and Wind Speed
        hum_wind_layout = BoxLayout(
            orientation="horizontal", size_hint_y=None, height=dp(25)
        )
        self.lbl_humidity = Label(
            text=f"Hum: {self.humidity_value}%",
            font_size="14sp",
            color=COLORS["light_blue"],  # Light blue text
            halign="left",
            valign="middle",
        )
        hum_wind_layout.add_widget(self.lbl_humidity)
        self.bind(humidity_value=self.lbl_humidity.setter("text"))

        self.lbl_uv_index = Label(
            text=f"UV: {self.uv_index}",
            font_size="14sp",
            color=COLORS["light_blue"],  # Light blue text
            halign="left",
            valign="middle",
        )
        hum_wind_layout.add_widget(self.lbl_uv_index)
        self.bind(uv_index=self.lbl_uv_index.setter("text"))

        self.lbl_wind = Label(
            text=f"Wind: {self.wind_speed_value:.1f} mph {self.wind_direction}",
            font_size="14sp",
            color=COLORS["light_green"],  # Light green text
            halign="left",
            valign="middle",
        )
        hum_wind_layout.add_widget(self.lbl_wind)
        self.bind(wind_speed_value=self.lbl_wind.setter("text"))

        details_layout.add_widget(hum_wind_layout)

        self.add_widget(details_layout)

    def update_weather_data(
        self,
        temp,
        condition,
        humidity,
        wind_speed,
        wind_dir,
        feels_like_f,
        uv,
        icon_file,
        city,
        region,
    ):
        """Update the widget with new weather data"""
        self.city_name = city
        self.current_temperature = temp
        self.feels_like_temperature = feels_like_f
        self.condition_text = condition
        self.humidity_value = humidity
        self.wind_speed_value = wind_speed
        self.wind_dir = wind_dir
        self.uv_index = uv
        self.icon_name = icon_file
        self.region_name = region

        # Ensure the image path is correct, assuming 'images' folder
        self.icon_source = os.path.join("/api/weather/condition_icons/", icon_file)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def _update_temp_labels(self, instance, value):
        """Update text of temperature labels when respective properties change"""
        self.lbl_temp.text = f"{self.current_temperature:.1f}°F"
        self.lbl_feels_like.text = f"(Feels like {self.feels_like_temperature:.1f}°F)"
