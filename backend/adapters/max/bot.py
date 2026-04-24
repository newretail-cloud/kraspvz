# adapters/max/bot.py
import logging
from maxapi import Bot, Dispatcher, types

from adapters.max.config import BOT_TOKEN

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# =============== ФУНКЦИЯ-ОБРАБОТЧИК ===============

async def handle_message(event: types.MessageCreated):
    """Обработчик всех входящих сообщений"""
    message = event.message
    text = message.text or ""
    
    logger.info(f"📨 Получено сообщение: {text}")
    
    if text.startswith("/start"):
        await message.answer(
            "👋 Добро пожаловать в **PVZ Work Bot**!\n\n"
            "Этот бот помогает находить сотрудников на ПВЗ и подработку.\n\n"
            "Используйте /help для списка команд."
        )
    elif text.startswith("/help"):
        await message.answer(
            "📖 **Справка по командам:**\n\n"
            "/start — начать работу\n"
            "/help — эта справка\n"
            "/new_order — создать новое объявление\n"
            "/my_orders — мои объявления\n"
            "/profile — мой профиль\n"
            "/find_jobs — найти слоты\n"
            "/my_shifts — мои смены"
        )
    elif text.startswith("/new_order"):
        await message.answer(
            "📝 **Создание нового объявления**\n\n"
            "Функция в разработке. Скоро здесь будет пошаговый мастер!"
        )
    elif text.startswith("/my_orders"):
        await message.answer(
            "📋 **Ваши объявления**\n\n"
            "Пока нет активных объявлений.\n"
            "Создайте новое через /new_order."
        )
    elif text.startswith("/profile"):
        await message.answer(
            "👤 **Ваш профиль**\n\n"
            "Имя: не указано\n"
            "Роль: не выбрана\n"
            "Телефон: не указан\n\n"
            "Используйте /start для выбора роли."
        )
    elif text.startswith("/find_jobs"):
        await message.answer(
            "🔍 **Поиск слотов**\n\n"
            "Функция поиска активных заказов в разработке."
        )
    elif text.startswith("/my_shifts"):
        await message.answer(
            "📅 **Мои смены**\n\n"
            "У вас пока нет назначенных смен."
        )
    else:
        await message.answer(
            "❓ Неизвестная команда.\n"
            "Используйте /help для списка доступных команд."
        )

# =============== РЕГИСТРАЦИЯ ОБРАБОТЧИКА ===============
dp.event_handlers.append((handle_message, types.MessageCreated))

# =============== ЗАПУСК ===============

async def main():
    logger.info("🚀 Запуск MAX-бота...")
    await dp.start_polling(bot)

def run():
    import asyncio
    asyncio.run(main())
