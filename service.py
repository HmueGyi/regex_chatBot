import speech_recognition
import pyttsx3
import re
import requests
import json
from datetime import datetime
import pytz
import openai
from sympy import sympify
from sympy.core.sympify import SympifyError
from patterns import *
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Access API keys
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
TIME_API_KEY = os.getenv("TIME_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

recognizer = speech_recognition.Recognizer()
engine = pyttsx3.init()

time_cache = {}

openai.api_key = OPENAI_API_KEY

# Load timezone data
try:
    with open("cities_timezones.json", "r") as file:
        city_timezone_map = json.load(file)
except FileNotFoundError:
    city_timezone_map = {}
    print("Error: 'cities_timezones.json' file not found.")


def ask_openai(question):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": question}]
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"Error calling OpenAI: {e}")
        return "Sorry, I'm having trouble connecting to my brain right now."


def chatbot_response(user_input, user_id="default"):
    user_input = user_input.lower().strip()
    mode = "neutral"  # Default mode

    intro_match = self_intro_pattern.search(user_input)
    if intro_match:
        name = intro_match.group(1).strip().title()
        return f"Hello {name}!", mode
    
    # Emotion-based responses
    if greeting_pattern.search(user_input):
        return "Hello! How can I assist you today?", mode
    if name_pattern.search(user_input):
        return "Hello! I'm Learner_bot. What is your day?", mode
    if feel_pattern.search(user_input):
        return "I'm good! How about you?", mode
    if compliment_pattern.search(user_input):
        mode = "happiness"
        return "Aww, thank you! That made my day!", mode
    if insult_pattern.search(user_input):
        mode = "sadness"
        return "That hurts... Why would you say that?", mode
    if happiness_pattern.search(user_input):
        return "That sounds great! Keep up the positive vibes!", mode
    if sadness_pattern.search(user_input):
        return "I'm sorry to hear that. I'm here for you.", mode
    if fear_pattern.search(user_input):
        return "That sounds scary. Stay strong, you're not alone.", mode
    if anger_pattern.search(user_input):
        mode = "angry"
        return "I understand your frustration. Take a deep breath, let's talk.", mode
    if surprise_pattern.search(user_input):
        return "Wow! That sounds shocking! Tell me more.", mode
    if disgust_pattern.search(user_input):
        return "That sounds awful. I hope things get better.", mode
    if thanks_pattern.search(user_input):
        return "You're very welcome! I'm happy to help. 😊", mode

    # Weather and time inquiries
    if re.search(r'.*?\b(weather\s+today|today\'?s?\s+weather|current\s+weather)\b', user_input, re.IGNORECASE):
        DEFAULT_CITY = "pathein"
        return get_weather_today(DEFAULT_CITY), mode

    if re.search(r'.*?\b(time\s+now|what\s+time\s+is\s+it)\b', user_input, re.IGNORECASE):
        DEFAULT_CITY = "pathein"
        return get_time_today(DEFAULT_CITY), mode

    if re.search(r'.*?\bplay\s*:? ?(?:game|games|a game|the game)\b', user_input, re.IGNORECASE):
        mode = "game"
        return "Let's play", mode

    for pattern in weather_patterns:
        match = re.search(pattern, user_input, re.IGNORECASE)
        if match:
            city = match.group(1).strip()
            return get_weather(city), mode

    for pattern in time_patterns:
        match = re.search(pattern, user_input, re.IGNORECASE)
        if match:
            city = match.group(1).strip()
            return get_time(city), mode

    for pattern in calc_patterns:
        match = re.fullmatch(pattern, user_input, re.IGNORECASE)
        if match:
            expression = match.group(1).strip().replace('=', '')
            return calculate_expression(expression), mode

    other_response = ask_openai(user_input)
    return other_response, mode


def get_weather(city):
    try:
        location_url = f"http://dataservice.accuweather.com/locations/v1/cities/search?apikey={WEATHER_API_KEY}&q={city}"
        location_response = requests.get(location_url)
        location_data = location_response.json()

        if location_response.status_code == 200 and location_data:
            location_key = location_data[0]['Key']
            weather_url = f"http://dataservice.accuweather.com/currentconditions/v1/{location_key}?apikey={WEATHER_API_KEY}"
            weather_response = requests.get(weather_url)
            weather_data = weather_response.json()

            if weather_response.status_code == 200 and weather_data:
                temp = weather_data[0]['Temperature']['Metric']['Value']
                weather_text = weather_data[0]['WeatherText']
                return f"The current temperature in {city} is {temp}°C with {weather_text}."
        return "Sorry, I couldn't fetch the weather data."
    except Exception as e:
        return f"An error occurred while fetching weather info: {e}"


def get_time(city):
    global time_cache
    city = city.lower()
    if city in time_cache:
        return time_cache[city]

    try:
        timezone = city_timezone_map.get(city)
        if not timezone:
            return "Sorry, I couldn't find the timezone for the specified city."

        tz = pytz.timezone(timezone)
        now = datetime.now(tz)
        formatted_time = now.strftime("%d/%m/%Y %I:%M %p")

        time_cache[city] = f"The current time in {city.title()} is {formatted_time}."
        return time_cache[city]
    except Exception as e:
        return f"An error occurred while fetching the time: {e}"


def get_weather_today(city):
    try:
        location_url = f"http://dataservice.accuweather.com/locations/v1/cities/search?apikey={WEATHER_API_KEY}&q={city}"
        location_response = requests.get(location_url)
        location_data = location_response.json()

        if location_response.status_code == 200 and location_data:
            location_key = location_data[0]['Key']
            weather_url = f"http://dataservice.accuweather.com/currentconditions/v1/{location_key}?apikey={WEATHER_API_KEY}"
            weather_response = requests.get(weather_url)
            weather_data = weather_response.json()

            if weather_response.status_code == 200 and weather_data:
                temp = weather_data[0]['Temperature']['Metric']['Value']
                weather_text = weather_data[0]['WeatherText']
                return f"Today's current temperature is {temp}°C with {weather_text}."
        return "Sorry, I couldn't fetch the weather data."
    except Exception as e:
        return f"An error occurred while fetching weather info: {e}"


def get_time_today(city):
    global time_cache
    city = city.lower()
    if city in time_cache:
        return time_cache[city]

    try:
        timezone = city_timezone_map.get(city)
        if not timezone:
            return "Sorry, I couldn't find the timezone for the specified city."

        tz = pytz.timezone(timezone)
        now = datetime.now(tz)
        formatted_time = now.strftime("%d/%m/%Y %I:%M %p")

        time_cache[city] = f"Today's current time is {formatted_time}."
        return time_cache[city]
    except Exception as e:
        return f"An error occurred while fetching the time: {e}"


def calculate_expression(expression):
    try:
        # Replace words with operators
        expression = expression.replace(' plus ', '+')
        expression = expression.replace(' minus ', '-')
        expression = expression.replace(' times ', '*')
        expression = expression.replace(' divided by ', '/')
        
        result = sympify(expression, evaluate=True)

        if result.is_number and result.is_rational:
            if not result.is_integer:
                result = float(result)
                return f"The result of {expression} is {result:.10g}"
            else:
                result = int(result)

        return f"The result of {expression} is {result}."
    
    except SympifyError:
        return "I couldn't understand the mathematical expression. Please try again with a valid format."
    except Exception as e:
        return f"An error occurred: {str(e)}"


if __name__ == "__main__":
    print("Learner_bot is running! Type 'exit' to quit.")
    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() == 'exit':
                print("Goodbye!")
                break
            
            response, mode = chatbot_response(user_input)
            print(f"Learner_bot: {response}")

            # Optional: Uncomment to enable text-to-speech
            # engine.say(response)
            # engine.runAndWait()

        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break
