from .states import BaseStates
from ..config.config import MESSAGES
from ..keyboard.keyboard import menu_kb

from src.config.custom_filters import IsIncorrect
    
async def start(message):
    await message.answer(MESSAGES['start'], reply_markup=menu_kb)
    await BaseStates.IN_MENU.set()
    
async def help_(message):
    await message.answer(MESSAGES['help'])
    
async def stop(message):
    await message.answer(MESSAGES['menu']['back_error'])
    
async def not_state(message):
    await message.answer(MESSAGES['not_state'], reply_markup=menu_kb)
    await BaseStates.IN_MENU.set() 
    
async def incorrect_input(message):
    await message.answer(MESSAGES['menu']['input_error'], reply_markup=menu_kb)
    
def register_menu(dp):
    dp.register_message_handler(start, commands='start', state=None)
    dp.register_message_handler(help_, commands='help', state='*')
    dp.register_message_handler(stop, commands='stop', state=BaseStates.IN_MENU)
    dp.register_message_handler(incorrect_input, IsIncorrect(), state=BaseStates.IN_MENU)
    dp.register_message_handler(not_state, state=None)
    
