import asyncio
import logging
from aiogram import Dispatcher, Bot
from handlers import userHandlers
from config_data.config import load_config
import os

logger = logging.getLogger(__name__)

logger_handler = logging.StreamHandler()
logs_filepath = "storage/logs/"
os.makedirs(logs_filepath, exist_ok=True)
logger_handler = logging.FileHandler(f'{logs_filepath}/logs.txt')

logger.addHandler(logger_handler)

# logging.basicConfig(
#     level=logging.DEBUG,
#     format='[{asctime}] #{levelname:8} {filename}:' '{lineno} - {name} - {message}',
#     style='{'
#   )

async def main() -> None:
  config = load_config()
  bot = Bot(config.tg_bot.token)
  if bot == None:
    logger.error("Bot instance is not initialized")
    return
  
  dp = Dispatcher()


  
  dp.include_router(userHandlers.router)


  await bot.delete_webhook(drop_pending_updates=True)

  logger.info('Бот был успешно запущен')
  
  await dp.start_polling(bot)

if __name__ == '__main__':
  asyncio.run(main())