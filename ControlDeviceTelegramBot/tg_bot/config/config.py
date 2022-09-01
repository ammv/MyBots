MESSAGES = {
    'start': '''
Приветствую! Объясняю следующие кнопки на клавиатуре ниже:\n
<b>Добавить устройство</b> - добавление устройства с которым вы будете взаимодействовать\n
<b>Устройства</b> - Показывает добавленные устройства\n
Устройства будут помечены знаками:\n
💤 - Нет соеденения
✅ - Свободно, есть соеденение
❌ - Занято, есть соеденение''',

    'help': '''
<b>Добавить устройство</b> - добавление устройства с которым вы будете взаимодействовать\n
<b>Устройства</b> - Показывает добавленные устройства\n
Устройства будут помечены знаками:\n
💤 - Нет соеденения
✅ - Свободно, есть соеденение
❌ - Занято, есть соеденение''',

    'menu': {
        'back': 'Вы вернулись в главное меню',
        'unknown_command': 'Неизвестная команда!',
        'devices': 'Выберите устройство из списка',
        'add_device': 
'''Введите названия устройства и его IP (IPv4) в данном формате:
Название устройства:IP

Пример:
NotebookIvan:192.168.1.255'''
    },
    
    'add_device': {
        'confirm': 'Проверьте данные:\n<b>Название</b>: {0}\n<b>IP</b>: {1}',
        'finish': 'Устройство добавлено',
        'cancel': 'Введите новое Название:IP или вернитесь в меню - Назад ⬅️'
    },
    
    'device': {
    
    
        'unknown_device': 'Данное устройство отсутствует',
        'no_connection': 'Данное устройство недоступно. Нет соеденения',
        'occupied': 'Данное устройство недоступно. Его использует другой пользователь',
        'free': 'Вы выбрали устройство с названием {0}.\nЕго IP: {1}',
    },
    
    'control_device': {
        'Прочее': 
'''Доступны следующие команды:
<b>1. Ping</b> - отправить ping и получить pong от устройства
''',
        'Курсор': 
'''Доступны следующие команды:
<b>1. CursorPanel</b> - панель управления курсором мыши с транслированием изображения экрана
<b>2. Cursor</b> - установление позиции курсора за счёт ввода координат X и Y
''',
        'Камера': 
'''Доступны следующие команды:
<b>1. CameraImage</b> - получение изображения с камеры
''',
        'Экран': 
'''Доступны следующие команды:
<b>1. DesktopImage</b> - получение изображения с экрана
''',
        'Проводник': 
'''Доступны следующие команды:
<b>1. Иди нахер от сюда чорт</b> - ок
'''
    }

}