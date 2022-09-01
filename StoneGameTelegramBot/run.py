'''
Description: Hello! You can play in **Stone Game**
/start - [["Play with computer"]|["Play with user"]]

"Play with computer" -> "Input count of stones: "
'''
import asyncio
import logging
import configparser

from aiogram.utils import executor
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from src.handlers.handlers import register_handlers
from src.config.custom_filters import FILTERS

from bot import BOT


def get_api_token():
    config = configparser.ConfigParser()
    config.read('bot.ini')
    return config['tg_bot']['token']


async def set_commands(bot):
    commands = [
        types.BotCommand(command="/start", description="Start play in the game"),
        types.BotCommand(command="/help", description="Get help")
    ]
    await bot.set_my_commands(commands)
    
async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()
    
def main():
    logging.basicConfig(level=logging.INFO)
    
    dp = Dispatcher(BOT, storage=MemoryStorage())    
    dp.middleware.setup(LoggingMiddleware())
    
    for filt in FILTERS:
        dp.bind_filter(filt)
    
    @dp.message_handler(state='*', commands='mystate')
    async def get_user_state(message):
        state = await dp.current_state(user=message.from_user.id).get_state()
        await message.answer('Your state is ' + state, parse_mode='HTML')

    register_handlers(dp)
    
    executor.start_polling(dp, on_shutdown=shutdown)
    
    
if __name__ == "__main__":
    # Запуск бота
    main()