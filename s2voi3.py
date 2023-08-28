import re
import os
import gdown
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import SendMessageRequest

# تنظیمات API تلگرام
api_id = '20307428'
api_hash = 'db1b2a38958c06bc4e99b01d4cfd485c'

# تنظیمات توکن ربات تلگرام
bot_token = '6242144866:AAE_l_3X2o6vqSo34qZz5k1u3lGngT70ovQ'

# تابع برای دانلود فایل از لینک گوگل درایو و ارسال آن به تلگرام
async def process_google_drive_link(link):
    # از انتهای لینک بین /d/ و /view را برداریم
    file_id = re.search(r"/d/(.*?)/view", link).group(1)
    
    # اجرای دستور gdown بر روی لینک گوگل درایو در سرور
    os.system(f"gdown {link}")

    # اتصال به API تلگرام
    client = TelegramClient('anon', api_id, api_hash)
    await client.start(bot_token=bot_token)

    # آپلود فایل به تلگرام
    await client.send_file('me', 'downloaded_file')
    
    # ارسال پیام به کاربر با اطلاعات دانلود
    await client.send_message('me', f'فایل از گوگل درایو با شناسه {file_id} دانلود شد و به تلگرام ارسال شد.')

    # پس از ارسال فایل به تلگرام، فایل محلی را حذف کنید
    os.remove('downloaded_file')

if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    link = input("لینک گوگل درایو را وارد کنید: ")
    loop.run_until_complete(process_google_drive_link(link))
