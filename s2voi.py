import os
import speech_recognition as sr
from pyrogram import Client

# نصب TgCrypto
os.system("pip install tgcrypto")

api_id = 12345  
api_hash = 'your api hash'
bot_token = 'bot token' 

app = Client("my_bot", api_id, api_hash, bot_token=bot_token)

@app.on_message()
async def get_voice(client, message):

  if message.voice:
  
    # ذخیره voice note
    voice_note = message.voice  
    
    # دانلود voice note
    voice_note.download("voice.ogg")

    os.system("ffmpeg -i voice.ogg voice.wav")
            
    r = sr.Recognizer()
    with sr.AudioFile('voice.wav') as source:
      audio = r.record(source)

    text = r.recognize_google(audio, language='fa-IR')
    
    await app.send_message(message.chat.id, text)

app.run()
