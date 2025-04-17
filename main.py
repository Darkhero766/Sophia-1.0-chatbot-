import random as r
import json
import os
import time
import nltk
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('wordnet')
nltk.download('omw-1.4')

from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()


user_memory = {}

def preprocess(text):
  tokens = word_tokenize(text.lower())
  return [lemmatizer.lemmatize(token) for token in tokens]

  

def response(user_input):
  tokens = preprocess(user_input)

  
  if "name" in tokens and "is" in tokens:
    try:
      name_index = tokens.index("name") +2 if "is" in tokens else -1
      if 0 <= name_index < len(tokens):
        user_memory["name"] = tokens[name_index].capitalize()
        return f"Nice to meet you, {user_memory['name']}!"
      else:
        return "I didn't catch your name. Could you please repeat it?"
    except:
      return "I didn't catch your name. Could you please repeat it?"
      
  elif "what" in tokens and "my" in tokens and "name" in tokens:
    if "name" in user_memory:
      return f"Your name is {user_memory['name']}."
    else:
      return "Sorry i dont know your name."
      
  elif "your" in tokens and "name" in tokens:
    return "I am sophia An ai chatbot."
  elif "Hello" in tokens:
    return "Hey there!"
  elif "bye" in tokens:
    return "Goodbye , have a nice day."
  else:
    return"Hmm... I am still learning starting to understand you."

while True:

  inp = input("You: ")
  if inp == "exit":
    break
  print("Bot: ", response(inp))
