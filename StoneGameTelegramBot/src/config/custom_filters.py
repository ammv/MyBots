from aiogram.dispatcher.filters import BoundFilter

from ..keyboard.keyboard import menu_buttons

class IsIncorrect(BoundFilter):
    key = 'is_incorrect'
    
    async def check(self, msg):
        return msg.text not in menu_buttons
        
class IsInt(BoundFilter):
    key = 'is_int'
    
    async def check(self, msg):
        return msg.text.isdecimal()
        
FILTERS = (IsIncorrect, IsInt)