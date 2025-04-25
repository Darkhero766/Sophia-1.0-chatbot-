import random as r
import requests
from bs4 import BeautifulSoup
import json
import os
import datetime
import nltk
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('wordnet')
nltk.download('omw-1.4')


from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

memory_file = "user_memory.json"
user_memory = {}
reminders = {}
personality = "friendly"

fun_facts = [
    "Honey never spoils. Archaeologists have found pots of it in ancient tombs!",
    "Octopuses have three hearts.",
    "Bananas are berries, but strawberries aren't!",
    "Your brain uses 20% of your body’s oxygen and calories.",
    "Cats can’t taste sweetness."
]

jokes = [
    "Why don’t scientists trust atoms? Because they make up everything!",
    "Why did the robot go on vacation? It needed to recharge.",
    "I told my AI friend a joke... it still hasn’t stopped buffering.",
    "Parallel lines have so much in common… it’s a shame they’ll never meet."
]

quotes = [
    "“The best way to predict the future is to invent it.” – Alan Kay",
    "“Whether you think you can or you think you can’t, you’re right.” – Henry Ford",
    "“Success is not final, failure is not fatal: It is the courage to continue that counts.” – Winston Churchill",
    "“Your time is limited, don’t waste it living someone else’s life.” – Steve Jobs"
]


    
def detect_intent(tokens):
  text = ' '.join(tokens)
  if "time" in tokens:
    return "time"
  elif any(op in text for op in ["+", "-", "*", "/"]):
    return "math"
  elif "bored" in text or "something funny " in text or "tell me a joke" in text:
    return "random_fun"
  elif  "reminders" in text or "tasks" in text:
    return "get_reminders"
  elif "date" in text:
    return "date"
  elif "day" and "today" in text:
    return get_date()
  elif "how many days" in text or "days till" in text:
    return "countdown"

  return "unknown" 
def set_personality(user_input):
  global personality
  if "sarcastic" in user_input.lower():
    personality = "sarcastic"
  elif "friendly" in user_input.lower():
    personality = "friendly"
    return "yay back to being your friend"
  elif "nerdy" in user_input.lower():
    personality = "nerdy"
    return "okay i will be nerdy"
  elif "chill" in user_input.lower():
    personality = "chill"
    return "Whatever man, let’s keep it low-key."
  else:
    return "I don't understand that personality. I can be sarcastic, friendly, nerdy, or chill."

def apply_personality(response):
  if personality == "sarcastic":
    return response + " (Wow, what a revelation.)"
  elif personality == "friendly":
    return response + " (Let's be friends!"
  elif personality == "nerdy":
    return response + " (Did you know that...?"
  elif personality == "chill":
    return response + " (chill vibes only.)"
def store_reminder(user_input):
  match = re.search(r"remind me to (.+?)(?: at| on| in| tomorrow|$)", user_input.lower())
  if match:
    task = match.group(1).strip()
    time_match = re.search(r"(at (.+)", user_input.lower())
    time = time_match.group(1).strip() if time_match else None
    reminders.append((task, time))
    return f" Reminder noted: {task} at {time}"
  return "Can you say it like 'Remind me to [task] at [time]'?"


def list_reminders():
  if not reminders:
    return "You have no reminder."
  return "\n".join([f"- {task} at {time}" for task, time in reminders])

      
def math_solver(user_input):
  try:
   expr = user_input.lower()
   expr = expr.replace("plus", "+").replace("minus", "-").replace("times", "*").replace("multiplied by", "*")
   expr = expr.replace("divided by", "/").replace("over", "/").replace("into", "*").replace("x", "*")
   numbers = re.findall(r"[0-9\.\+\-\*/]+", expr)
   if numbers:
        expr = eval(numbers[0])
        return f"The result of {numbers[0]} is {expr}"
   else:
     return "hmm there is no operation in your input"
  except Exception as e:
        return "That looks like an invalid math expression!"
    
def random_fun():
  category = r.choice(["fun_facts","jokes","quotes"])
  if category == "fun_facts":
    return r.choice(fun_facts)
  elif category == "jokes":
    return r.choice(jokes)
  else:
    return r.choice(quotes)
    
def time ():
  now = datetime.datetime.now()
  return f"The current time is {now.strftime('%I:%M %p')}"


def date():
  now = datetime.date.today()
  return f"Today's date is {now.strftime('%B %d, %Y')}"

def countdown(user_input):
  try:
    if "neet" in user_input.lower():
      target_date = datetime.date(2025, 5, 4)
    else:
      return "please mention specific date for countdown "

    today = datetime.date.today()
    delta = target_date - today

    if delta.days > 0:
      return f"there are {delta.days} days left "
    elif delta.days == 0:
      return "Today is the day!"
    else:
      return f"the day has passed {abs(delta.days)} days ago"

  except Exception:
    return "sorry i didn't catch that"
def web_search(query):


  
  search_url = f"https://duckduckgo.com/html/?q={query}"

  try:
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, "html.parser")
    search_results = soup.find_all('a', class_='result__a')
    if search_results:
      first_result = search_results[0]
      title = first_result.get_text()
      link = first_result['href']

      snippet = first_result.find_next('a').text if first_result.find_next('a') else "No snippet available."
      return f"Here's what I found: {title}\n{snippet}\nFor more details, visit: {link}"

    else:
      return "I couldn't find any relevant information "
  except Exception as e:
    return f"An error occurred while searching: {e}"
          

      

  
def load_memory():
  try:
    if os.path.exists(memory_file):
      with open(memory_file, "r") as file:
        data = file.read()
        return json.loads(data) if data else {}
    return {}
  except json.JSONDecodeError:
    return {}

def save_memory(memory):
  with open(memory_file, "w") as file:
    json.dump(memory, file)
  
def preprocess(text):
  tokens = word_tokenize(text.lower())
  return [lemmatizer.lemmatize(token) for token in tokens]


emotion_keywords= {
  "sad": ["sad", "depressed", "unhappy", "down", "cry"],
    "happy": ["happy", "excited", "joy", "glad", "yay"],
    "angry": ["angry", "mad", "furious", "annoyed"],
    "stressed": ["stressed", "anxious", "worried", "tired", "burnt out"],
    "confused": ["confused", "lost", "don’t understand", "what", "huh"],
    "lonely": ["lonely", "alone", "isolated"]
}
intents = {
  "greeting": ["hello", "hi", "hey", "greetings"],
  "farewell": ["bye", "goodbye", "see you later"],
  "ask name": ["what is my name", "who am i "],
  
  "recall_fact": [['what','my']],
  "learn_fact": [['my','is']],
  "tell name": ["my name is ", "i am", "i'm"]
    
  }

def detect_emotion(user_input):
  lower_input = user_input.lower()
  for emotion, keywords in emotion_keywords.items():
    if any(keyword in lower_input for keyword in keywords):
        return emotion
  return None

def respond_to_emotion(emotion):
  responses = {
    "sad": "I'm here for you. Do you want to talk about what's bothering you?",
        "happy": "That’s awesome! Want to share what made you feel this way?",
        "angry": "Take a deep breath. Want to vent it out?",
        "stressed": "Try to take a short break. Want me to suggest something relaxing?",
        "confused": "Let me help. What exactly are you confused about?",
        "lonely": "I'm always here to chat with you. You're not alone."
  
  }
  return responses.get(emotion,"I am here to help you")
  
def match_intents(tokens):
    for intent, patterns in intents.items():
        for pattern in patterns:
            if all(word in tokens for word in pattern):
                return intent
    return "unknown"


user_memory = load_memory()
def response(user_input):
  tokens = preprocess(user_input)
  intent = match_intents(tokens)

  
  if intent == "greeting":
    return "Hello how i can help you today?"
  elif intent == "random_fun":
    return random_fun()
  elif intent == " emotion":
    return respond_to_emotion(detect_emotion(user_input))
      
  elif intent == "farewell":
    return "Goodbye have a nice day"
    
      
  elif intent=="ask name":
    if "name" in user_memory:
      return f"i am {user_memory['name']}"

    else: return "I dont know your name yet"
  elif intent=="tell name":
    name = tokens[-1]
    user_memory["name"] = name
    save_memory(user_memory)
    return f"Nice to meet you {name}"

  elif intent == "learn_fact":
    try:
     my_index = tokens.index("my")
     is_index = tokens.index("is")
     key_tokens = tokens[my_index + 1: is_index]
     value_tokens = tokens[is_index + 1:]
     key = " ".join(key_tokens)
     value = " ".join(value_tokens)
     if key and value:
       user_memory[key] = value
       save_memory(user_memory)
       return f"Okay, I remember that your {key} is {value}."
     else:
       return "Sorry i didn't catch that"
    except :
      return "Sorry i didn't catch that"

  elif intent == "recall_fact":
    try:
      my_index = tokens.index("my")
      key_tokens = tokens[my_index + 1:]
      key = " ".join(key_tokens)
      if key in user_memory:
        return f"Your {key} is {user_memory[key]}."
      else:
        return f"Sorry, I don't know your {key}."
    

    except:
      return "Sorry i didn't remember that"
  elif intent == "math":
    return solve_math(user_input)
    
  elif intent == "unknown":
    return web_search(user_input)
  elif intent == "remind me":
    return store_reminder(user_input)
  elif intent == "get_reminders":
    return list_reminders()
  
  elif intent == "get_time":
        return time()
  elif intent == "get_date":
        return date()
  
  elif intent == "countdown":
        return countdown(user_input)
  else:
    return"Hmm... I am still learning starting to understand you."

while True:

  inp = input("You: ")
  if inp == "exit":
    break
  print("Bot: ", response(inp))
