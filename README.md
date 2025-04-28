

---

# Sophia AI Chatbot in Python

Welcome to my **AI Chatbot** project!  
This chatbot is built using **Python** and several libraries like **NLTK**, **BeautifulSoup**, and **Requests**.  
It can chat, solve math problems, remember facts about you, tell jokes, manage reminders, and even detect your emotions!

---

## Features
- **Basic Chatting** (greeting, farewell, etc.)
- **Intent Detection** without using any external API
- **Math Solver** (basic arithmetic)
- **Reminders** (save and list tasks)
- **Memory Storage** (remembers your name and facts)
- **Emotion Detection** (sad, happy, angry, lonely, etc.)
- **Fun Facts, Jokes, Quotes**
- **Web Search** (uses DuckDuckGo if no intent is matched)
- **Countdown** (example: "How many days until NEET?")
- **Personality Switching** (Friendly, Sarcastic, Nerdy, Chill)
- **Offline Learning** (auto learn your facts like your favorite song)

---

## Setup Instructions
1. **Clone the repository**
   ```bash
   git clone https://github.com/Darkhero766/Sophia-1.0-chatbot-
   cd Sophia-1.0-chatbot-
   ```

2. **Install required libraries**
   ```bash
   pip install nltk requests beautifulsoup4
   ```

3. **Download NLTK data**
   Inside your Python script or separately:
   ```python
   import nltk
   nltk.download('punkt')
   nltk.download('wordnet')
   nltk.download('omw-1.4')
   ```

4. **Run the chatbot**
   ```bash
   python chatbot.py
   ```

---

## File Structure
- **chatbot.py** → Main Python file containing the chatbot logic
- **user_memory.json** → Stores user facts like name, favorites, reminders (auto created)
- **README.md** → This documentation file

---

## Example Usage
```text
You: Hello
Bot: Hello how can I help you today?

You: My favorite color is blue
Bot: Okay, I remember that your favorite color is blue.

You: What is my favorite color?
Bot: Your favorite color is blue.

You: Solve 5 plus 7
Bot: The result of 5+7 is 12.

You: Tell me a joke
Bot: Why don’t scientists trust atoms? Because they make up everything!

You: Remind me to study at 5 PM
Bot: Reminder noted: study at 5 PM
```

---

## Future Improvements
- Add voice input/output
- Improve web search scraping
- Support complex math solving
- Advanced natural language understanding (NLU)

---

## License
This project is free to use for learning and personal projects.

---

