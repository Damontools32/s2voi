import asyncio
import requests

from telethon import TelegramClient, events

# جایگزین کردن توکن‌های مربوط به ربات تلگرام و Wit.ai
API_ID = "YOUR_API_ID"
API_HASH = "YOUR_API_HASH"
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
WIT_AI_SERVER_ACCESS_TOKEN = "YOUR_WIT_AI_SERVER_ACCESS_TOKEN"


async def voice_to_text(voice_file) -> str:
    api_url = "https://api.wit.ai/speech"
    headers = {
        "Content-Type": "audio/ogg; codecs=opus",
        "Authorization": f"Bearer {WIT_AI_SERVER_ACCESS_TOKEN}",
    }

    response = requests.post(api_url, headers=headers, data=voice_file)

    if response.status_code == 200:
        result = response.json()
        return result["text"]
    else:
        raise Exception(f"Error: {response.text}")


async def main():
    client = TelegramClient("bot", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

    @client.on(events.NewMessage(pattern="/start"))
    async def start_command_handler(event):
        await event.reply("سلام! لطفا ویس خود را بفرستید تا آن را به متن تبدیل کنم.")

    @client.on(events.NewMessage(func=lambda e: e.voice))
    async def voice_message_handler(event):
        voice = event.voice
        voice_file = await client.download_file(voice)

        try:
            text = await voice_to_text(voice_file)
            await event.reply(f"متن شناسایی شده: {text}")
        except Exception as e:
            await event.reply(f"مشکلی رخ داد: {e}")

    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
