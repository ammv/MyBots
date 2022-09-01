import json
import socket

from threading import Thread
from time import sleep

from .states import States, CDStates
from ..config.config import MESSAGES
from ..keyboard.keyboard import control_device_kb, devices_kb, cd_kbs, add_buttons
from ..utils.utils import update_status, get_device, get_devices

command_sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

devices = get_devices()

def update_devices_kb():
    global devices_kb, devices
    print('start tut ')
    def _update_devices_kb():
        while True:
            devices = get_devices()
            devices_kb = add_buttons(devices, False)
            sleep(0.1)
    
    Thread(target=_update_devices_kb).start()

def command_sender_start():
    global command_sender
    print('[COMMAND SENDER] Connecting...')
    command_sender.connect(('localhost', 8888))
    
async def back(message):
    await message.answer(MESSAGES['menu']['devices'], reply_markup=devices_kb)
    await States.SELECT_DEVICE.set()
    update_status(None, 1, message.from_user.id)
    
async def select_section(message):
    if message.text in ('Прочее', 'Экран', 'Камера', 'Проводник', 'Курсор'):
        await message.answer(MESSAGES['control_device'][message.text], reply_markup=cd_kbs[message.text])
        await CDStates.ALL[message.text].set()
    else:
        await message.answer('Неизвестная команда')
        
async def ping(message):
    data = {'id': message.from_user.id, 'task': 'ping', 'addr': get_device(None, message.from_user.id)}
    command_sender.send(json.dumps(data).encode('utf-8'))
    
    await message.answer('Вы вызвали команду Ping, ожидайте ответа от устройства')
        
async def back_section(message):
    await message.answer('Вы в панели управлении устройством, выберите одно из действий',
        reply_markup=control_device_kb)
    await States.CONTROL_DEVICE.set()
    
def register_control_device(dp):
    update_devices_kb()
    
    dp.register_message_handler(back, text='Назад ⬅️', state=States.CONTROL_DEVICE)
    dp.register_message_handler(back_section, text='Назад ⬅️', state=lambda x: x in CDStates.ALL)
    dp.register_message_handler(select_section, state=States.CONTROL_DEVICE)
    dp.register_message_handler(ping, text='Ping', state=CDStates.OTHER)
  
