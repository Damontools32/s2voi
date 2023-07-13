import os
import asyncio
from telethon import TelegramClient, events
import yt_dlp
from moviepy.editor import *
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

api_id = YOUR_API_ID
api_hash = 'YOUR_API_HASH'
bot_token = 'YOUR_TELEGRAM_BOT_TOKEN'

client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

def download_video_and_thumbnail(url: str):
    ytdl_opts = {
        "format": "bestvideo[height<=360]+bestaudio/best[height<=360]",
        "outtmpl": "video.%(ext)s",
        "writethumbnail": True,
    }

    with yt_dlp.YoutubeDL(ytdl_opts) as ydl:
        ydl.download([url])

    video_path, thumb_path = None, None
    for file in os.listdir():
        if file.startswith("video."):
            video_path = file
        elif file.startswith("video_thumbnail."):
            thumb_path = file

    return video_path, thumb_path

def add_thumbnail_to_video(video_path, thumb_path):
    video = VideoFileClip(video_path)
    thumbnail = ImageClip(thumb_path, duration=video.duration)
    final = CompositeVideoClip([thumbnail.set_opacity(0.6), video.set_opacity(0.4)])
    final_path = "final_" + video_path
    final.write_videofile(final_path, codec="libx264", audio_codec="aac")
    return final_path

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.reply("لطفا لینک ویدیوی یوتیوب خود را بفرستید.")

@client.on(events.NewMessage)
async def handle_url(event):
    if event.text.startswith('/'):
        return

    url = event.text
    await event.reply("در حال دانلود ویدیو...")

    video_path, thumb_path = download_video_and_thumbnail(url)
    if video_path and thumb_path:
        final_video_path = add_thumbnail_to_video(video_path, thumb_path)
        await client.send_file(
            event.chat_id,
            final_video_path,
            supports_streaming=True,
        )
        os.remove(video_path)
        os.remove(thumb_path)
        os.remove(final_video_path)
    else:
        await event.reply("مشکلی در دانلود ویدیو پیش آمده است.")

with client:
    client.run_until_disconnected()
