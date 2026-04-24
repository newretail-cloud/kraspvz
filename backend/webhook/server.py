import asyncio
import os
import json
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from maxapi import Bot
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("MAX_BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MaxWebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        """Обработка POST-запросов от MAX"""
        if self.path == '/webhook/max':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            try:
                update = json.loads(post_data.decode('utf-8'))
                logger.info(f"Получено обновление: {update}")
                
                # Обрабатываем обновление
                asyncio.run(self.process_update(update))
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(b'{"status": "ok"}')
            except Exception as e:
                logger.error(f"Ошибка: {e}")
                self.send_response(500)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()
    
    async def process_update(self, update):
        """Обработка входящего обновления"""
        update_type = update.get('update_type')
        
        if update_type == 'message_created':
            message = update.get('message', {})
            text = message.get('text', '')
            chat_id = update.get('chat_id')
            
            logger.info(f"📨 Сообщение от {chat_id}: {text}")
            
            if text.startswith("/start"):
                await bot.send_message(chat_id=chat_id, text="👋 Добро пожаловать в PVZ Work Bot!")
            elif text.startswith("/help"):
                await bot.send_message(chat_id=chat_id, text="📖 /start /help /new_order")
            else:
                await bot.send_message(chat_id=chat_id, text="❓ Неизвестная команда")
    
    def log_message(self, format, *args):
        """Переопределяем логирование"""
        logger.info(f"Запрос: {args[0]}")

def run():
    port = 8001
    server = HTTPServer(('0.0.0.0', port), MaxWebhookHandler)
    logger.info(f"🚀 Веб-сервер запущен на порту {port}")
    server.serve_forever()

if __name__ == "__main__":
    run()
