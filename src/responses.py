import re
from src.weather_time import get_weather, get_time
from src.calculator import calculate_expression

def chatbot_response(user_input, user_id="default"):
    user_input = user_input.lower().strip()

    greeting_pattern = re.compile(r'\b(?:hi|hello|hey|hiya|howdy|what\'s up|good (morning|afternoon|evening))\b', re.IGNORECASE)
    name_pattern = re.compile(r'\b(?:what(?:\'s| is) your name|how can I call you|who are you|tell me your name|your name please|may I know your name)\b', re.IGNORECASE)
    feel_pattern = re.compile(r'\b(?:how are you|your name please|may I know your name)\b', re.IGNORECASE)
    compliment_pattern = re.compile(r'\b(?:you look|you are|you\'re).*? (pretty|beautiful|amazing|cute|awesome)|i like you|i love you\b', re.IGNORECASE)
    insult_pattern = re.compile(r'\b(?:you look|you are|you\'re).*?(ugly|stupid|dumb|horrible)|i hate you|shut up bot\b', re.IGNORECASE)
    thanks_pattern = re.compile(r'\b(?:thank you|thanks|appreciate it|grateful)\b', re.IGNORECASE)

    # Greeting & Emotion Responses
    if greeting_pattern.search(user_input):
        return "Hello! How can I assist you today?"
    if name_pattern.search(user_input):
        return "Hello! I'm PyChat. What is your day!"
    if feel_pattern.search(user_input):
        return "I'm good! How about you?"
    if compliment_pattern.search(user_input):
        return "Aww, thank you! That made my day!"
    if insult_pattern.search(user_input):
        return "That hurts... Why would you say that?"
    if thanks_pattern.search(user_input):
        return "You're very welcome! I'm happy to help. 😊"

    # Weather patterns
    weather_patterns = [
        r'weather in ([\w\s]+)',
        r'what(?:\'s| is)? the weather (?:like )?in ([\w\s]+)',
        r'tell me the weather for ([\w\s]+)',
        r'current weather in ([\w\s]+)'
    ]
    for pattern in weather_patterns:
        match = re.search(pattern, user_input)
        if match:
            city = match.group(1).strip()
            return get_weather(city)

    # Time patterns
    time_patterns = [
        r'time in ([\w\s]+)',
        r'what(?:\'s| is)? the time in ([\w\s]+)',
        r'current time in ([\w\s]+)',
        r'tell me the time in ([\w\s]+)'
    ]
    for pattern in time_patterns:
        match = re.search(pattern, user_input)
        if match:
            city = match.group(1).strip()
            return get_time(city)

    # Calculation fallback
    return calculate_expression(user_input)
