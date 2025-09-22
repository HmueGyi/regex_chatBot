import os
import json
from dotenv import load_dotenv

# Load .env file
load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
TIME_API_KEY = os.getenv("TIME_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Load timezone data
try:
    with open("cities_timezones.json", "r") as file:
        CITY_TIMEZONE_MAP = json.load(file)
except FileNotFoundError:
    CITY_TIMEZONE_MAP = {}
    print("Error: 'cities_timezones.json' file not found.")
