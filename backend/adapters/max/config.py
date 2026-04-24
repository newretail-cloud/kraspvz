import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("MAX_BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("MAX_BOT_TOKEN не найден! Проверьте .env файл")
