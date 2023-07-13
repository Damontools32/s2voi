import logging
import requests

from telegram import Update, Voice
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# جایگزین کردن توکن‌های مربوط به ربات تلگرام و Wit.ai
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
WIT_AI_SERVER_ACCESS_TOKEN = "YOUR_WIT_AI_SERVER_ACCESS_TOKEN"


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("سلام! لطفا ویس خود را بفرستید تا آن را به متن تبدیل کنم.")


def voice_to_text(voice: Voice) -> str:
    api_url = "https://api.wit.ai/speech"
    headers = {
        "Content-Type": "audio/ogg; codecs=opus",
        "Authorization": f"Bearer {WIT_AI_SERVER_ACCESS_TOKEN}",
    }

    response = requests.post(api_url, headers=headers, data=voice.get_file().download_as_bytearray())

    if response.status_code == 200:
        result = response.json()
        return result["text"]
    else:
        raise Exception(f"Error: {response.text}")


def handle_voice(update: Update, context: CallbackContext) -> None:
    try:
        text = voice_to_text(update.message.voice)
        update.message.reply_text(f"متن شناسایی شده: {text}")
    except Exception as e:
        update.message.reply_text(f"مشکلی رخ داد: {e}")


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    updater = Updater(TELEGRAM_BOT_TOKEN)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.voice, handle_voice))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
