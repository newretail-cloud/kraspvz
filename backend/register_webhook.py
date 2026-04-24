import os
import requests
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("MAX_BOT_TOKEN")
WEBHOOK_URL = "https://kraspvz.ru/webhook/max"  # Ваш публичный HTTPS адрес

headers = {"Authorization": BOT_TOKEN, "Content-Type": "application/json"}
data = {"url": WEBHOOK_URL}

response = requests.post("https://platform-api.max.ru/subscriptions", headers=headers, json=data)
print(f"Статус: {response.status_code}")
print(f"Ответ: {response.text}")
