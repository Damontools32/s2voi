import os
import speech_recognition as sr 
from pyrogram import Client

api_id = 12345
api_hash = 'your api hash'
bot_token = '12345:YOUR_BOT_TOKEN' 

bot = Client("my_bot", api_id, api_hash, bot_token=bot_token)

# دریافت ویس از کاربر
message = bot.ask("لطفا یک پیام صوتی بفرستید")  
voice_note = message.voice
voice_note.download("voice.ogg")
os.system("ffmpeg -i voice.ogg voice.wav")

# تبدیل ویس به متن   
r = sr.Recognizer()
with sr.AudioFile('voice.wav') as source:
    audio = r.record(source)

text = r.recognize_google(audio, language='fa-IR')

# ارسال متن به کاربر
bot.send_message(message.chat.id, text)
