from .states import States
from ..config.config import MESSAGES

# import sys
#sys.path.append(".")

from ..keyboard.keyboard import menu_kb
    
async def start(message):
    await message.answer(MESSAGES['start'], reply_markup=menu_kb)
    await States.IN_MENU.set()
    
async def help(message):
    await message.answer(MESSAGES['help'])
    
async def shutdown(message):
    await message('Прекращаю работу хозяин')
    
    
async def not_state(message):
    await message.answer('Мы не смогли отследить где вы находились до этого. Поэтому перебросим вас в меню!', reply_markup=menu_kb)
    await States.IN_MENU.set()
    
def register_menu(dp):
    dp.register_message_handler(start, commands=['start'], state='*')
    dp.register_message_handler(help, commands=['help'], state='*')
    dp.register_message_handler(not_state, state=None)
