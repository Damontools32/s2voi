import os
import aiohttp
from pyrogram import Client, filters
import yt_dlp

api_id = YOUR_API_ID
api_hash = 'YOUR_API_HASH'
bot_token = 'YOUR_TELEGRAM_BOT_TOKEN'

app = Client("bot", api_id, api_hash, bot_token=bot_token)

def download_video(url: str) -> str:
    ytdl_opts = {
        "format": "bestvideo[height<=360][ext=webm]+bestaudio[ext=m4a]/best[height<=360][ext=mp4]",
        "outtmpl": "video.%(ext)s",
    }

    with yt_dlp.YoutubeDL(ytdl_opts) as ydl:
        ydl.download([url])

    for file in os.listdir():
        if file.startswith("video."):
            return file
    return None

async def upload_url(chat_id, url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                file_name = url.split("/")[-1]
                with open(file_name, "wb") as file:
                    while True:
                        chunk = await response.content.read(1024)
                        if not chunk:
                            break
                        file.write(chunk)
                await app.send_message(chat_id, "در حال آپلود فایل...")
                await app.send_document(chat_id, file_name)
                os.remove(file_name)
            else:
                await app.send_message(chat_id, "مشکلی در دانلود فایل پیش آمده است.")

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("لطفا لینک ویدیوی یوتیوب خود را بفرستید یا لینک مستقیم فایل را برای آپلود به تلگرام ارسال کنید.")

@app.on_message(filters.text)
async def handle_url(client, message):
    url = message.text

    # Ignore commands
    if url.startswith('/'):
        return

    if "youtube.com" in url or "youtu.be" in url:
        await message.reply_text("در حال دانلود ویدیو...")
        video_path = download_video(url)
        if video_path:
            await client.send_video(message.chat.id, video_path)
            os.remove(video_path)
        else:
            await message.reply_text("مشکلی در دانلود ویدیو پیش آمده است.")
    else:
        await message.reply_text("در حال دانلود فایل...")
        await upload_url(message.chat.id, url)

app.run()
