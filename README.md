# This Day in History Bot

A Telegram bot that sends information about random historical events that happened on the current date in the past. The bot uses the Wikipedia API to retrieve data.

## Features

- Send random historical events that occurred on the current date
- Request one, five, or ten random events
- Simple interface with keyboard buttons and commands
- English language interface

## Installation and Setup

1. Install dependencies:
```
pip install -r requirements.txt
```

2. Create a bot in Telegram via [@BotFather](https://t.me/BotFather) and get the API token.

3. Configure the bot token in the `main.py` file:
```python
TELEGRAM_API_TOKEN = "your_telegram_bot_token_here"
```

4. Run the bot:
```
python main.py
```

## Required Packages

Create a `requirements.txt` file with the following dependencies:
```
aiogram>=3.0.0
python-dotenv>=1.0.0
requests>=2.28.0
deep-translator>=1.11.0
```

## Usage

After launching the bot in Telegram, you can use the following options:

### Keyboard Buttons
- **🗓 Events on this day** - Get information about one random event
- **5️⃣ Five events** - Get five random events
- **🔟 Ten events** - Get ten random events
- **ℹ️ Help** - Show help information

### Commands
- `/start` - Start the bot and get a welcome message
- `/today` - Get information about a random event that occurred on the current date
- `/help` - Show help information and list of available commands

## Technical Details

- Programming language: Python 3.7+
- Telegram Bot API library: aiogram
- Data source: Wikipedia API (On This Day) 
