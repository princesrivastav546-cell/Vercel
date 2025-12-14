import os
import json
import requests
import logging
from datetime import datetime
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")

API_BASE = "https://anishexploits.site/api/api.php?key=exploits&num="

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

logging.basicConfig(level=logging.INFO)

# ================= HANDLERS =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[KeyboardButton("📞 ENTER NUMBER")]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "👋 *WELCOME TO OLIVER EXPLOITS*",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "📞 ENTER NUMBER":
        await update.message.reply_text(
            "📤 *Send Your 10-digit Number Without +91:*",
            parse_mode="Markdown"
        )
    else:
        await process_number(update, context)

async def process_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    number = update.message.text.strip()

    if not number.isdigit() or len(number) != 10:
        await update.message.reply_text("❌ Invalid number")
        return

    result = await search_number_api(number)
    await update.message.reply_text(result, parse_mode="Markdown")

async def search_number_api(number):
    try:
        r = requests.get(f"{API_BASE}{number}", headers=HEADERS, timeout=20)
        if r.status_code != 200:
            return "❌ Server Error"

        data = r.json()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"📞 *Number:* {number}\n⏰ *Time:* {now}\n\n```json\n{json.dumps(data, indent=2)}```"

    except Exception:
        return "❌ API Error"

# ================= VERCEL WEBHOOK =================

app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

async def handler(request):
    body = await request.json()
    update = Update.de_json(body, app.bot)
    await app.process_update(update)
    return {
        "statusCode": 200,
        "body": json.dumps({"ok": True})
    }