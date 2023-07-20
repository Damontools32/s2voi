import os
from pyrogram import Client, filters
import yt_dlp

api_id = YOUR_API_ID
api_hash = 'YOUR_API_HASH'
bot_token = 'YOUR_TELEGRAM_BOT_TOKEN'

app = Client("bot", api_id, api_hash, bot_token=bot_token)

def download_video(url: str):
    ytdl_opts = {
        "format": "bestvideo[height<=360][ext=mkv]+bestaudio[ext=m4a]/best[height<=360][ext=mkv]",
        "outtmpl": "video.%(ext)s",
    }

    with yt_dlp.YoutubeDL(ytdl_opts) as ydl:
        try:
            ydl.download([url])
        except Exception as e:
            print(f'Error during download: {e}')

    video_file = None
    for file in os.listdir():
        if file.startswith("video."):
            video_file = file

    return video_file

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
        video_file = download_video(url)
        if video_file:
            await client.send_video(message.chat.id, video_file, supports_streaming=True)
            if os.path.exists(video_file):
                os.remove(video_file)
        else:
            await message.reply_text("مشکلی در دانلود ویدیو پیش آمده است.")

app.run()
