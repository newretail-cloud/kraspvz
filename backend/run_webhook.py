import asyncio
import logging
from maxapi import Bot, Dispatcher, types

from adapters.max.config import BOT_TOKEN

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Обработчик ВСЕХ сообщений
@dp.message_created()
async def handle_message(event: types.MessageCreated):
    message = event.message
    # Правильный путь к тексту сообщения в MAX
    text = message.body.text if hasattr(message.body, 'text') else ""
    
    logger.info(f"📨 Получено сообщение: {text}")
    
    if text.startswith("/start"):
        await event.message.answer(
            "👋 Добро пожаловать в **PVZ Work Bot**!\n\n"
            "Ваш webhook-сервер работает корректно!"
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
    logger.info("🚀 Запуск webhook-сервера...")
    await dp.handle_webhook(
        bot=bot,
        host='0.0.0.0',
        port=8001,
        path='/max',
    )

if __name__ == '__main__':
    asyncio.run(main())
