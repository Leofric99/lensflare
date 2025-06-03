import requests
import time

def get_coordinates(location_name, retries=1, delay=2):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": location_name,
        "format": "json",
        "limit": 1
    }

    headers = {
        "User-Agent": "LocationScript/1.0 (your_email@example.com)"  # Replace with your contact email
    }

    attempt = 0
    while attempt <= retries:
        try:
            response = requests.get(url, params=params, headers=headers)
            data = response.json()
            if data:
                lat = data[0]['lat']
                lon = data[0]['lon']
                return float(lat), float(lon)
            else:
                print(f"Location '{location_name}' not found.")
                return None
        except requests.RequestException as e:
            print(f"Error fetching data for '{location_name}': {e}")
            if attempt < retries:
                time.sleep(delay)
            else:
                return None
        attempt += 1
