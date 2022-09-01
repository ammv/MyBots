from .states import States
# import sys
# sys.path.append("..")

from ..config.config import MESSAGES
from ..utils.utils import add_device, check_device_ip, get_devices
from ..keyboard.keyboard import add_device_kb, confirm_add_device_kb, menu_kb
#saving the user ID and his device during the addition
data = dict()
    
async def add(message):
    await message.answer(MESSAGES['menu']['add_device'], reply_markup=add_device_kb)
    await States.ADD_DEVICE.set()
    
async def confirm(message):
    res = check_device_ip(message.text)
    if res == True:
        devices = get_devices(keys=True)
        device, ip = message.text.split(':')
        if device not in get_devices(keys=True):
            data[message.from_user.id] = message.text
            await message.answer(MESSAGES['add_device']['confirm'].format(device, ip), reply_markup=confirm_add_device_kb)
            await States.CONFIRM_ADD_DEVICE.set()
        else:
            await message.answer('Ошибка! Данное название занято, придумайте другое')
    else:
        await message.answer('Ошибка! ' + res)
    
async def end(message):
    device, ip = data[message.from_user.id].split(':')
    add_device(device, ip)
    await message.answer(MESSAGES['add_device']['finish'], reply_markup=menu_kb)
    await States.IN_MENU.set()
    
async def cancel(message):
    del data[message.from_user.id]
    await message.answer(MESSAGES['add_device']['cancel'], reply_markup=add_device_kb)
    await States.ADD_DEVICE.set()
    
async def back(message):
    await message.answer(MESSAGES['menu']['back'], reply_markup=menu_kb)
    await States.IN_MENU.set()
    
def register_add_device(dp):
    dp.register_message_handler(add, text='Добавить устройство ❇️', state=States.IN_MENU)
    dp.register_message_handler(back, text='Назад ⬅️', state=States.ADD_DEVICE)
    
    dp.register_message_handler(confirm, state=States.ADD_DEVICE)
    dp.register_message_handler(end, text='Подтвердить ✅', state=States.CONFIRM_ADD_DEVICE)
    dp.register_message_handler(cancel, text='Отменить ❌', state=States.CONFIRM_ADD_DEVICE)
