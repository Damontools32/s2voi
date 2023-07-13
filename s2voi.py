import os
import asyncio
import logging
import requests

from telethon import TelegramClient, events

# جایگزین کردن اطلاعات مربوط به کلاینت تلگرام و Wit.ai
API_ID = YOUR_API_ID
API_HASH = "YOUR_API_HASH"
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
WIT_AI_SERVER_ACCESS_TOKEN = "YOUR_WIT_AI_SERVER_ACCESS_TOKEN"


async def voice_to_text(file_path):
    api_url = "https://api.wit.ai/speech"
    headers = {
        "Content-Type": "audio/ogg; codecs=opus",
        "Authorization": f"Bearer {WIT_AI_SERVER_ACCESS_TOKEN}",
    }

    with open(file_path, "rb") as file:
        response = requests.post(api_url, headers=headers, data=file.read())

    if response.status_code == 200:
        result = response.json()
        return result["text"]
    else:
        raise Exception(f"Error: {response.text}")


async def main():
    logging.basicConfig(level=logging.INFO)

    client = TelegramClient("voice_bot", API_ID, API_HASH)
    await client.start(bot_token=BOT_TOKEN)

    @client.on(events.NewMessage(pattern="/start"))
    async def start_handler(event):
        await event.respond("سلام! لطفا ویس خود را بفرستید تا آن را به متن تبدیل کنم.")

    @client.on(events.NewMessage)
    async def voice_handler(event):
        if event.message.voice:
            try:
                file_path = await event.message.download_media()
                text = await voice_to_text(file_path)
                os.remove(file_path)
                await event.reply(f"متن شناسایی شده: {text}")
            except Exception as e:
                await event.reply(f"مشکلی رخ داد: {e}")

    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
