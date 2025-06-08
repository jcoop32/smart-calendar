import requests


def get_ip_coordinates():
    try:
        ip_response = requests.get("https://api.ipify.org?format=json")
        ip_data = ip_response.json()
        public_ip = ip_data["ip"]

        # Use ipinfo.io for latitude and longitude
        location_response = requests.get(f"https://ipinfo.io/{public_ip}/json")
        location_data = location_response.json()

        if "loc" in location_data:
            latitude, longitude = map(float, location_data["loc"].split(","))
            return latitude, longitude
        else:
            print(f"Could not determine coordinates for IP {public_ip}.")
            return None, None

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None, None
