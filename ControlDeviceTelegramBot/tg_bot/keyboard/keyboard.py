from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove

#import sys
#sys.path.append("..")

from ..utils.utils import get_devices

back = 'Назад ⬅️'


def add_buttons(buttons, one=True):
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=one)
    for butt in buttons:
        kb.add(butt)
    
    return kb

menu_buttons = ('Устройства 💻', 'Добавить устройство ❇️')

menu_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
menu_kb.add(*menu_buttons)

add_device_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
add_device_kb.add(back)

confirm_add_device_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
confirm_add_device_kb.add('Отменить ❌', 'Подтвердить ✅')

devices_kb = add_buttons(get_devices(), False)


#[Курсор ][ Камера]
#[Проводник][Экран]
#[     Прочее     ]
#[     Назад ⬅️    ]

control_device_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
control_device_kb.add('Курсор', 'Камера')
control_device_kb.add('Проводник', 'Экран')
control_device_kb.add('Прочее')
control_device_kb.add(back)

cd_other_kb = ReplyKeyboardMarkup(resize_keyboard=True)
cd_other_kb.add('Ping').add(back)

cd_cursor_kb = ReplyKeyboardMarkup(resize_keyboard=True)
cd_cursor_kb.add('CursorPanel').add('SetCursor').add(back)

cd_camera_kb = ReplyKeyboardMarkup(resize_keyboard=True)
cd_camera_kb.add('GetImage').add(back)

cd_explorer_kb = ReplyKeyboardMarkup(resize_keyboard=True)
cd_explorer_kb.add('..').add(back)

cd_desktop_kb = ReplyKeyboardMarkup(resize_keyboard=True)
cd_desktop_kb.add('GetScreenshot').add(back)

cd_kbs = {'Прочее': cd_other_kb, 'Курсор': cd_cursor_kb, 'Камера': cd_camera_kb,
    'Экран': cd_desktop_kb, 'Проводник': cd_explorer_kb}




remove_kb = ReplyKeyboardRemove()