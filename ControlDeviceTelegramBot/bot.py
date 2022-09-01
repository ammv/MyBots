import logging
import asyncio
import configparser
from os import _exit

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from tg_bot.handlers.handlers import register_handlers
from tg_bot.handlers.control_device import command_sender_start
from server import Server

       
async def set_commands(bot: Bot):
    commands = [
        types.BotCommand(command="/start", description="Начать работу"),
        types.BotCommand(command="/help", description="Помощь"),
    ]
    await bot.set_my_commands(commands)
    
    
async def main():
    config = configparser.ConfigParser()
    config.read('bot.ini')
    
    API_TOKEN = config['tg_bot']['token']
    
    logging.basicConfig(level=logging.INFO)
    
    bot = Bot(token=API_TOKEN, parse_mode='HTML')
    
    dp = Dispatcher(bot, storage=MemoryStorage())
    
    server = Server(bot)
    server.run()
    
    command_sender_start()
        
    #registr all handlers from tg_bot\handlers
    register_handlers(dp)
    
    await set_commands(bot)

    await dp.start_polling()

if __name__ == "__main__":
    # Запуск бота
    asyncio.run(main())