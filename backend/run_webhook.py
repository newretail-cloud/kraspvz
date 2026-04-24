import asyncio
import os
import logging
from dotenv import load_dotenv
from maxapi import Bot, Dispatcher, types

# Загружаем переменные из .env
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("MAX_BOT_TOKEN")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")

if not BOT_TOKEN:
    raise ValueError("MAX_BOT_TOKEN не найден в .env")
if not WEBHOOK_SECRET:
    raise ValueError("WEBHOOK_SECRET не найден в .env")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Обработчик всех сообщений
@dp.message_created()
async def handle_message(event: types.MessageCreated):
    """Обработчик входящих сообщений"""
    # Получаем текст сообщения (правильный путь для MAX)
    if hasattr(event.message, 'body') and hasattr(event.message.body, 'text'):
        text = event.message.body.text
    else:
        text = ""
    
    logger.info(f"📨 Получено сообщение: {text}")
    
    if text.startswith("/start"):
        await event.message.answer(
            "👋 Добро пожаловать в **PVZ Work Bot**!\n\n"
            "Ваш webhook-сервер работает корректно с защитой!"
        )
    elif text.startswith("/help"):
        await event.message.answer(
            "📖 **Доступные команды:**\n"
            "/start — приветствие\n"
            "/help — справка\n"
            "/new_order — создать заказ (в разработке)"
        )
    else:
        await event.message.answer(
            "❓ Неизвестная команда. Используйте /help для списка команд."
        )

async def main():
    logger.info("🚀 Запуск webhook-сервера с проверкой секрета...")
    await dp.handle_webhook(
        bot=bot,
        host='0.0.0.0',
        port=8001,
        path='/max',
        secret=WEBHOOK_SECRET
    )

if __name__ == '__main__':
    asyncio.run(main())
