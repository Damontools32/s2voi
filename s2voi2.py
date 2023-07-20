import os
import aiohttp
from pyrogram import Client, filters
import yt_dlp

api_id = YOUR_API_ID
api_hash = 'YOUR_API_HASH'
bot_token = 'YOUR_TELEGRAM_BOT_TOKEN'

app = Client("bot", api_id, api_hash, bot_token=bot_token)

def download_video_and_thumbnail(url: str):
    ytdl_opts = {
        "format": "bestvideo[height<=360][ext=webm]+bestaudio[ext=webm]/best[height<=360][ext=webm]",
        "outtmpl": "video.%(ext)s",
        "writethumbnail": True
    }

    with yt_dlp.YoutubeDL(ytdl_opts) as ydl:
        ydl.download([url])

    video_file = None
    thumbnail_file = None
    for file in os.listdir():
        if file.startswith("video."):
            video_file = file
        elif file.endswith((".jpg", ".png")):
            thumbnail_file = file

    return video_file, thumbnail_file

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("لطفا لینک ویدیوی یوتیوب خود را بفرستید.")

@app.on_message(filters.text)
async def handle_url(client, message):
    url = message.text

    # Ignore commands
    if url.startswith('/'):
        return

    if "youtube.com" in url or "youtu.be" in url:
        await message.reply_text("در حال دانلود ویدیو...")
        video_file, thumbnail_file = download_video_and_thumbnail(url)
        if video_file and thumbnail_file:
            await client.send_video(message.chat.id, video_file, thumb=thumbnail_file)
            if os.path.exists(video_file):
                os.remove(video_file)
            if os.path.exists(thumbnail_file):
                os.remove(thumbnail_file)
        else:
            await message.reply_text("مشکلی در دانلود ویدیو یا تصویر شاخص پیش آمده است.")

app.run()
