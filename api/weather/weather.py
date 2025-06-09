import requests

# from get_location import get_ip_coordinates

# from conditions_map import conditions

from api.weather.get_location import get_ip_coordinates
from api.weather.conditions_map import conditions

import os
from dotenv import load_dotenv


load_dotenv()

lat, lon = get_ip_coordinates()


API_KEY = os.getenv("WEATHER_API_KEY")

location = f"{lat},{lon}"


api_url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={location}"


def get_weather():
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        weather_data = response.json()

        if weather_data:
            loc_info = weather_data["location"]
            current_info = weather_data["current"]

            city = loc_info["name"]
            region = loc_info["region"]
            # country = loc_info["country"]
            # local_time = loc_info["localtime"]  # Local date and time

            temp_f = int(current_info["temp_f"])
            condition_text = current_info["condition"]["text"]
            humidity = current_info["humidity"]
            wind_speed = current_info["wind_mph"]
            wind_dir = current_info["wind_dir"]
            feels_like_f = int(current_info["feelslike_f"])
            uv = int(current_info["uv"])
            icon_file = conditions[condition_text]

            return (
                temp_f,
                condition_text,
                humidity,
                wind_speed,
                wind_dir,
                feels_like_f,
                uv,
                icon_file,
                city,
                region,
            )

            # print(f"--- Current Weather for {city}, {region}, {country} ---")
            # print(f"Local Time: {local_time}")
            # print(f"Conditions: {condition_text}")
            # print(f"Conditions Icon: {icon_file}")
            # print(f"Temperature: {temp_f}°F")
            # print(f"Feels like: {feels_like_f}°F")
            # print(f"Humidity: {humidity}%")
            # print(f"Wind: {wind_speed} mph {wind_dir}")
            # print(f"UV Index: {uv}")

        else:
            print("No weather data found in the response.")

    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        print(f"Response content: {response.text}")
        print("Please check your API key and location parameter.")
    except requests.exceptions.ConnectionError as e:
        print(f"Connection Error: {e}")
        print(
            "Could not connect to the WeatherAPI.com. Check your internet connection."
        )
    except requests.exceptions.RequestException as e:
        print(f"An unexpected error occurred: {e}")
