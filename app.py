import os
import requests
import json
import logging
import time
from datetime import datetime
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from flask import Flask  # Add Flask to host a web server

# ==================== CONFIGURATION ====================
API_BASE = "https://anishexploits.site/api/api.php?key=exploits&num="
# IMPORTANT: Use an environment variable for the token for security
BOT_TOKEN = os.environ.get('BOT_TOKEN', '8372266918:AAGMkYzH0QvmxGJVrrTXvF8nzT7KXjj1O40')
PORT = int(os.environ.get('PORT', 8080))  # Render provides a port via env variable

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 13; Termux) Gecko/117.0 Firefox/117.0",
    "Accept": "application/json,text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8",
    "Referer": "https://oliver-exploits.vercel.app/",
    "Connection": "keep-alive"
}

# ==================== BOT SETUP ====================
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Initialize Flask app
web_app = Flask(__name__)

# Your existing bot functions (start, handle_message, process_number, etc.) go here.
# ... [Paste all your bot functions from the original code here, starting with `async def start(...)` and ending with `def main():`] ...
# IMPORTANT: In the `main()` function, REMOVE the lines `application.run_polling()`.

# ==================== WEB SERVER ROUTE ====================
@web_app.route('/')
def home():
    return "Bot is running. Powered by Render."

# ==================== START BOT & SERVER ====================
def start_bot():
    """Function to start the Telegram bot."""
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("\n" * 2)
    print("=" * 50)
    print("🛡️ OLIVER EXPLOITS NUMBER SCANNER")
    print("📱 Status: OPERATIONAL")
    print("=" * 50)
    print("\n✅ Bot initialized successfully!")
    print("🔍 Waiting for scan requests...\n")
    
    # Start polling in a non-blocking way
    application.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    # This block runs on Render
    import threading
    # Start the bot in a separate thread
    bot_thread = threading.Thread(target=start_bot)
    bot_thread.daemon = True
    bot_thread.start()
    # Start the Flask web server on the main thread
    web_app.run(host='0.0.0.0', port=PORT, debug=False, use_reloader=False)
