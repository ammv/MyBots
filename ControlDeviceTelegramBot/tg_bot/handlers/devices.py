from .states import States
from threading import Thread
from time import sleep
# import sys
# sys.path.append("..")

from ..config.config import MESSAGES
from ..keyboard.keyboard import add_buttons, devices_kb, menu_kb, control_device_kb
from ..utils.utils import get_devices, get_device_ip, update_status

devices = get_devices()

def update_devices_kb():
    global devices_kb, devices
    print('Start devices')
    def _update_devices_kb():
        while True:
            devices = get_devices()
            devices_kb = add_buttons(devices, False)
            sleep(0.1)
    
    Thread(target=_update_devices_kb).start()

async def start(message):
    await message.answer(MESSAGES['menu']['devices'], reply_markup=devices_kb)
    await States.SELECT_DEVICE.set()
    
async def select(message):
    if message.text in devices and message.text != devices[-1]:
        if message.text[-1] == '💤':
            await message.answer(MESSAGES['device']['no_connection'])
            
        elif message.text[-1] == '✅':          
            await message.answer(MESSAGES['device']['free'].format(
                    message.text[:-2], get_device_ip(message.text[:-2])),
                reply_markup=control_device_kb)
                
            await States.CONTROL_DEVICE.set()
            
            update_status(message.text[:-2], 2, False, message.from_user.id)
            
        else:
            await message.answer(MESSAGES['device']['occupied'])
            
    else:
        await message.answer(MESSAGES['device']['unknown_device'])
        
async def back(message):
    await message.answer(MESSAGES['menu']['back'], reply_markup=menu_kb)
    await States.IN_MENU.set()
    
def register_device(dp):
    update_devices_kb()
    dp.register_message_handler(start, text='Устройства 💻', state=States.IN_MENU)
    dp.register_message_handler(back, text='Назад ⬅️', state=States.SELECT_DEVICE)
    dp.register_message_handler(select, state=States.SELECT_DEVICE)
  
