import asyncio
import logging
from maxapi import Bot
from adapters.max.config import BOT_TOKEN

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)

async def main():
    logger.info("🚀 Запуск MAX-бота...")
    marker = None
    
    while True:
        try:
            # Используем параметры в соответствии с документацией MAX
            updates_data = await bot.get_updates(
                limit=100,
                timeout=30,
                marker=marker,
                types=['message_created']  # Получаем только сообщения
            )
            
            # Обрабатываем обновления
            updates = updates_data.get('updates', [])
            for update in updates:
                if update.get('type') == 'message_created':
                    message = update.get('message', {})
                    text = message.get('text', '')
                    logger.info(f"📨 Получено: {text}")
                    
                    if text.startswith("/start"):
                        await bot.send_message(
                            chat_id=message.get('chat', {}).get('id'),
                            text="👋 Добро пожаловать в **PVZ Work Bot**!\n\nИспользуйте /help для списка команд."
                        )
                    elif text.startswith("/help"):
                        await bot.send_message(
                            chat_id=message.get('chat', {}).get('id'),
                            text="📖 **Команды:**\n/start — приветствие\n/help — справка\n/new_order — создать заказ\n/profile — профиль"
                        )
                    elif text.startswith("/new_order"):
                        await bot.send_message(
                            chat_id=message.get('chat', {}).get('id'),
                            text="📝 Создание заказа в разработке."
                        )
                    elif text.startswith("/profile"):
                        await bot.send_message(
                            chat_id=message.get('chat', {}).get('id'),
                            text="👤 Профиль: данные не заполнены."
                        )
                    else:
                        await bot.send_message(
                            chat_id=message.get('chat', {}).get('id'),
                            text="❓ Неизвестная команда. /help"
                        )
            
            # Обновляем marker для следующего запроса
            if 'marker' in updates_data:
                marker = updates_data['marker']
                
        except Exception as e:
            logger.error(f"Ошибка: {e}")
            await asyncio.sleep(5)

def run():
    asyncio.run(main())
