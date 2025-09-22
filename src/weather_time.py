import requests
from datetime import datetime
import pytz
from config import WEATHER_API_KEY, CITY_TIMEZONE_MAP

time_cache = {}

def get_weather(city):
    city = city.strip()
    try:
        # Step 1: Search for city key
        location_url = f"http://dataservice.accuweather.com/locations/v1/cities/search"
        params = {"apikey": WEATHER_API_KEY, "q": city}
        location_response = requests.get(location_url, params=params)
        
        if location_response.status_code != 200:
            return f"Error: Could not fetch city info (status code {location_response.status_code})"
        
        location_data = location_response.json()
        if not location_data:
            return f"Sorry, I couldn't find the city '{city}'."

        location_key = location_data[0].get("Key")
        if not location_key:
            return f"Sorry, no location key found for '{city}'."

        # Step 2: Get current weather
        weather_url = f"http://dataservice.accuweather.com/currentconditions/v1/{location_key}"
        weather_response = requests.get(weather_url, params={"apikey": WEATHER_API_KEY})

        if weather_response.status_code != 200:
            return f"Error: Could not fetch weather (status code {weather_response.status_code})"

        weather_data = weather_response.json()
        if not weather_data:
            return "Sorry, no weather data returned."

        temp = weather_data[0]["Temperature"]["Metric"]["Value"]
        weather_text = weather_data[0]["WeatherText"]
        return f"The current temperature in {city.title()} is {temp}°C with {weather_text}."

    except Exception as e:
        return f"Error fetching weather: {e}"


def get_time(city):
    global time_cache
    city = city.lower().strip()
    if city in time_cache:
        return time_cache[city]

    try:
        timezone = CITY_TIMEZONE_MAP.get(city)
        if not timezone:
            return f"Sorry, I couldn't find the timezone for '{city.title()}'."

        tz = pytz.timezone(timezone)
        now = datetime.now(tz)
        
        # Format: 22 September 2025, 5:23 PM
        formatted_time = now.strftime("%-d %B %Y, %-I:%M %p")  # %-d removes leading 0 on day, %-I removes leading 0 on hour

        time_cache[city] = f"The current time in {city.title()} is {formatted_time}."
        return time_cache[city]

    except Exception as e:
        return f"Error fetching time: {e}"