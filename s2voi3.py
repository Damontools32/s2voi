import os
import asyncio
import aiohttp
from telethon import TelegramClient, events, Button
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

async def upload_url(event, url: str):
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
                try:                    
                    await event.reply("نام جدید فایل را وارد کنید:")
                    response = await client.wait_for(events.NewMessage(from_users=event.sender_id))
                    new_file_name = response.text + '.' + file_name.split('.')[-1]
                    os.rename(file_name, new_file_name)
                    file_name = new_file_name
                except Exception as e:
                    await event.reply(f"خطا در تغییر نام فایل: {str(e)}")
                await event.reply("در حال آپلود فایل...")
                await client.send_file(event.chat_id, file_name, supports_streaming=True)
                os.remove(file_name)
            else:
                await event.reply("مشکلی در دانلود فایل پیش آمده است.")

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.reply("لطفا لینک ویدیوی یوتیوب خود را بفرستید یا لینک مستقیم فایل را برای آپلود به تلگرام ارسال کنید.")

@client.on(events.NewMessage)
async def handle_url(event):
    if event.text.startswith('/'):
        return

    url = event.text

    if "youtube.com" in url or "youtu.be" in url:
        await event.reply("در حال دانلود ویدیو...")
        video_path = download_video(url)
        if video_path:
            await client.send_file(event.chat_id, video_path, supports_streaming=True)
            os.remove(video_path)
        else:
            await event.reply("مشکلی در دانلود ویدیو پیش آمده است.")
    else:
        await event.reply("در حال دانلود فایل...")
        await upload_url(event, url)

with client:
    client.run_until_disconnected()
