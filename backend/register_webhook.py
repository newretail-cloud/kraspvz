import os
import requests
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

BOT_TOKEN = os.getenv("MAX_BOT_TOKEN")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")

# Ваш публичный URL вебхука (должен совпадать с тем, что в Nginx)
WEBHOOK_URL = "https://kraspvz.ru/max"

headers = {
    "Authorization": BOT_TOKEN,
    "Content-Type": "application/json"
}

# Тело запроса с секретом
data = {
    "url": WEBHOOK_URL,
    "secret": WEBHOOK_SECRET
}

print("🔄 Регистрация webhook...")
response = requests.post("https://platform-api.max.ru/subscriptions", headers=headers, json=data)

print(f"Статус: {response.status_code}")
print(f"Ответ: {response.text}")

if response.status_code == 200:
    print("✅ Webhook успешно зарегистрирован с секретом!")
else:
    print("❌ Ошибка регистрации. Проверьте токен и URL.")
