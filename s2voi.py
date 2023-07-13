import os
import asyncio
from telethon import TelegramClient, events
import yt_dlp

api_id = YOUR_API_ID
api_hash = 'YOUR_API_HASH'
bot_token = 'YOUR_TELEGRAM_BOT_TOKEN'

client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

def download_video(url: str) -> str:
    ytdl_opts = {
        "format": "bestvideo[height<=360]+bestaudio/best[height<=360]",
        "outtmpl": "video.%(ext)s",
    }

    with yt_dlp.YoutubeDL(ytdl_opts) as ydl:
        ydl.download([url])

    for file in os.listdir():
        if file.startswith("video."):
            return file
    return None

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.reply("لطفا لینک ویدیوی یوتیوب خود را بفرستید.")

@client.on(events.NewMessage)
async def handle_url(event):
    if event.text.startswith('/'):
        return

    url = event.text
    await event.reply("در حال دانلود ویدیو...")

    video_path = download_video(url)
    if video_path:
        await client.send_file(event.chat_id, video_path, supports_streaming=True)
        os.remove(video_path)
    else:
        await event.reply("مشکلی در دانلود ویدیو پیش آمده است.")

with client:
    client.run_until_disconnected()
