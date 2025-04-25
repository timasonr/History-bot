import os
import logging
import requests
import random
from datetime import datetime
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.filters.command import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv
from deep_translator import GoogleTranslator

# Load environment variables (if .env file exists)
load_dotenv()

# Configuration
TELEGRAM_API_TOKEN = "enter your token here"
LOGGING_LEVEL = "INFO"
WIKIPEDIA_API_BASE_URL = "https://en.wikipedia.org/api/rest_v1/feed/onthisday"  # Using English version of the API

# Configure logging
logging.basicConfig(level=getattr(logging, LOGGING_LEVEL))

# Initialize bot and dispatcher
bot = Bot(token=TELEGRAM_API_TOKEN)
dp = Dispatcher()

# Months in English
MONTHS_EN = {
    1: "January", 2: "February", 3: "March", 4: "April",
    5: "May", 6: "June", 7: "July", 8: "August",
    9: "September", 10: "October", 11: "November", 12: "December"
}

# Function to translate text from Russian to English
def translate_to_english(text):
    try:
        # Use deep_translator library for translation
        translator = GoogleTranslator(source='ru', target='en')
        translated_text = translator.translate(text)
        return translated_text
    except Exception as e:
        logging.error(f"Error translating text: {e}")
        return text  # Return original text in case of error

# Function to create the main keyboard
def get_main_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="🗓 Events on this day"))
    builder.add(KeyboardButton(text="5️⃣ Five events"))
    builder.add(KeyboardButton(text="🔟 Ten events"))
    builder.add(KeyboardButton(text="ℹ️ Help"))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

# Function to get data from Wikipedia API
def get_events_on_this_day(count=1):
    today = datetime.now()
    month = today.month
    day = today.day
    
    # Form URL for Wikipedia API request (English version)
    url = f"{WIKIPEDIA_API_BASE_URL}/events/{month}/{day}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        
        data = response.json()
        
        if 'events' in data and len(data['events']) > 0:
            # If requested events count is greater than available in API,
            # limit the number to available events
            events_count = min(count, len(data['events']))
            
            # Select random events from the list
            selected_events = random.sample(data['events'], events_count)
            
            result = []
            for event in selected_events:
                year = event.get('year', 'Unknown year')
                text = event.get('text', 'Description unavailable')
                
                # Format the message (no need to translate as API returns English)
                event_text = f"📅 Year {year}: {text}"
                result.append(event_text)
            
            # Format date for output in English
            english_month = MONTHS_EN.get(month, str(month))
            header = f"🗓 Events on {english_month} {day}:\n\n"
            
            # Join all events into one message with separators
            return header + "\n\n".join(result)
        else:
            return "Unfortunately, I couldn't find information about events that happened on this day."
            
    except Exception as e:
        logging.error(f"Error getting data from Wikipedia API: {e}")
        return "An error occurred while retrieving historical data. Please try again later."

# Test function to check API
def test_wikipedia_api():
    """Test function to check Wikipedia API availability"""
    try:
        today = datetime.now()
        month = today.month
        day = today.day
        
        url = f"{WIKIPEDIA_API_BASE_URL}/events/{month}/{day}"
        
        print(f"Test request to API: {url}")
        
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()
        
        if 'events' in data and len(data['events']) > 0:
            event = data['events'][0]  # Take the first event for testing
            text = event.get('text', 'Description unavailable')
            year = event.get('year', 'Year not specified')
            
            print(f"API is working! Example event: {year} - {text}")
            
            # We don't need to test translation for English version
            return True
        else:
            print("API returned an empty list of events")
            return False
            
    except Exception as e:
        print(f"Error testing API: {e}")
        return False

# Handler for /start command
@dp.message(Command('start'))
async def send_welcome(message: types.Message):
    """Sends a welcome message and explains how to use the bot"""
    await message.answer(
        "👋 Hello! I'm the 'This Day in History' bot.\n\n"
        "I can tell you interesting events "
        "that happened on this day in the past.\n\n"
        "Use the buttons below to learn about events.",
        reply_markup=get_main_keyboard()
    )

# Handler for "Events on this day" button
@dp.message(F.text == "🗓 Events on this day")
async def send_one_event(message: types.Message):
    """Sends information about one event that happened on this day"""
    await message.answer("Looking for an interesting event for you...", reply_markup=get_main_keyboard())
    event_info = get_events_on_this_day(1)
    await message.answer(event_info)

# Handler for "Five events" button
@dp.message(F.text == "5️⃣ Five events")
async def send_five_events(message: types.Message):
    """Sends information about five events that happened on this day"""
    await message.answer("Looking for five interesting events for you...", reply_markup=get_main_keyboard())
    events_info = get_events_on_this_day(5)
    await message.answer(events_info)

# Handler for "Ten events" button
@dp.message(F.text == "🔟 Ten events")
async def send_ten_events(message: types.Message):
    """Sends information about ten events that happened on this day"""
    await message.answer("Looking for ten interesting events for you...", reply_markup=get_main_keyboard())
    events_info = get_events_on_this_day(10)
    await message.answer(events_info)

# Handler for help button
@dp.message(F.text == "ℹ️ Help")
@dp.message(Command('help'))
async def send_help(message: types.Message):
    """Sends help information about the bot"""
    await message.answer(
        "🤖 'This Day in History' Bot\n\n"
        "This bot provides information about events that happened on this day in different years. "
        "Data is retrieved from Wikipedia.\n\n"
        "Available buttons:\n"
        "🗓 Events on this day - get information about one random event\n"
        "5️⃣ Five events - get five random events\n"
        "🔟 Ten events - get ten random events\n"
        "ℹ️ Help - show this help message\n\n"
        "Commands available:\n"
        "/start - start the bot\n"
        "/help - show help information",
        reply_markup=get_main_keyboard()
    )

# Handler for /today command (for backward compatibility)
@dp.message(Command('today'))
async def send_event_command(message: types.Message):
    """Command handler for compatibility with older version"""
    await send_one_event(message)

# Handler for all other messages
@dp.message()
async def echo(message: types.Message):
    await message.answer(
        "I don't understand this message. Please use the buttons at the bottom of the screen.",
        reply_markup=get_main_keyboard()
    )

# Bot launch
async def main():
    # Instructions for the user at startup
    print("="*50)
    print("'This Day in History' bot is starting...")
    
    # Test API at startup
    print("\nChecking Wikipedia API availability...")
    test_wikipedia_api()
    
    print("\nToken needed for bot operation:", TELEGRAM_API_TOKEN)
    print("="*50)
    
    # Start the bot
    logging.info("Bot has been started")
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main()) 