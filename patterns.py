import re

# Define patterns
greeting_pattern = re.compile(
    r'.*?\b(?:hi|hello|hey|hiya|howdy|what\'s up|good (morning|afternoon|evening))\b',
    re.IGNORECASE
)

name_pattern = re.compile(
    r'.*?\b(?:what(?:\'s| is) your name|how can I call you|who are you|tell me your name|your name please|may I know your name)\b',
    re.IGNORECASE
)

feel_pattern = re.compile(
    r'\b(?:how are you|your name please|may I know your name)\b',
    re.IGNORECASE
)

# Compliments (Bot Responds Happily)
compliment_pattern = re.compile(
    r'.*?\b(?:'
    r'(?:you\s*look|you\s*are|you\'re)\s*'
    r'(?:pretty|beautiful|gorgeous|amazing|wonderful|cute|adorable|stunning|lovely|charming|radiant|attractive|smart|intelligent|kind|sweet|thoughtful|awesome|perfect)'
    r'|i like you|i love you|(you\'re|you are) the best'
    r')\b',
    re.IGNORECASE
)

# Insults (Bot Sulks or Gets Sad)
insult_pattern = re.compile(
    r'.*?\b(?:'
    r'(?:you\s*look|you\s*are|you\'re)\s*'
    r'(?:ugly|stupid|dumb|annoying|boring|horrible|terrible|gross|weird|disgusting|creepy|lame|useless|pathetic|idiot|awful)'
    r'|i hate you|shut up bot'
    r')\b',
    re.IGNORECASE
)

# Emotional Patterns
happiness_pattern = re.compile(r'.*?\b(?:I am happy|I feel happy|happy|joyful|excited|fantastic|awesome|wonderful|great|ecstatic|elated|thrilled|cheerful|delighted|overjoyed)\b', re.IGNORECASE)
sadness_pattern = re.compile(r'.*?\b(?:I am sad|I feel sad|sad|depressed|unhappy|miserable|crying|lonely|hopeless|heartbroken|downcast|melancholy|blue|despondent)\b', re.IGNORECASE)
fear_pattern = re.compile(r'.*?\b(?:I am scared|I feel scared|scared|afraid|terrified|fearful|worried|anxious|nervous|panicked|petrified|uneasy|apprehensive)\b', re.IGNORECASE)
anger_pattern = re.compile(r'.*?\b(?:I am angry|I feel angry|angry|mad|furious|frustrated|annoyed|irritated|outraged|resentful|fuming|infuriated|enraged)\b', re.IGNORECASE)
surprise_pattern = re.compile(r'.*?\b(?:I am surprised|I feel surprised|shocked|surprised|amazed|incredible|unbelievable|stunned|astonished|dumbfounded|flabbergasted|astounded)\b', re.IGNORECASE)
disgust_pattern = re.compile(r'.*?\b(?:I am disgusted|I feel disgusted|disgusting|gross|revolting|sickening|repulsive|vile|nauseating|abhorrent|horrid)\b', re.IGNORECASE)
thanks_pattern = re.compile(r'.*?\b(?:thank you|thanks|appreciate it|grateful)\b', re.IGNORECASE)

self_intro_pattern = re.compile(r'.*?\b(?:i am|i\'m|my name is)\s+([\w\s]+)\b', re.IGNORECASE)

# Weather inquiries
weather_patterns = [
    r'(?:.*?\b(?:what(?:\'?s|\s*is)?\s+the\s+weather\s+like\s+in\s+([\w\s]+))\b.*)',
    r'(?:.*?\b(?:weather\s+in\s+([\w\s]+))\b.*)',
    r'(?:.*?\b(?:tell\s+me\s+the\s+weather\s+for\s+([\w\s]+))\b.*)',
    r'(?:.*?\b(?:current\s+weather\s+in\s+([\w\s]+))\b.*)'
]

# Time inquiries
time_patterns = [
    r'.*?\b(?:what(?:\'?s|\s*is)?\s+the\s+time\s+in\s+([\w\s]+))\b',
    r'.*?\b(?:current\s+time\s+in\s+([\w\s]+))\b',
    r'.*?\b(?:tell\s+me\s+the\s+time\s+in\s+([\w\s]+))\b',
    r'.*?\b(?:time\s+in\s+([\w\s]+))\b'
]

# Calculation inquiries
calc_patterns = [
    r'\b(?:.*?\s)?'
    r'(?:what(?:\'?s|\s+is)?|calculate|solve|compute|evaluate|find|the\s+result\s+of|can\s+you\s+calculate|'
    r'how\s+much|what\s+is|is\s+it|give\s+me|tell\s+me)?\s*'
    r'((?:\s*-?\d+(?:\.\d+)?\s*([-+*/^]\s*-?\d+(?:\.\d+)?\s*)?)'
    r'|(?:\s*(?:sqrt|sin|cos|tan|log|ln|exp)\s*\(\s*-?\d+(?:\.\d+)?\s*\))?)\s*'
    r'(\s*(?:and|plus|minus|times|divided\s+by)\s*'
    r'(?:\s*-?\d+(?:\.\d+)?\s*([-+*/^]\s*-?\d+(?:\.\d+)?\s*)?)?)?\s*'
    r'(\s*(?:equal|=|equals)\s*)?\s*$'
]