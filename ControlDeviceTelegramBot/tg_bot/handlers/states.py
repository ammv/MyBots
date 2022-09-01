from aiogram.dispatcher.filters.state import State, StatesGroup

class States(StatesGroup):
    IN_MENU = State()
    
    #ADD DEVICE
    ADD_DEVICE = State()
    CONFIRM_ADD_DEVICE = State()
    
    #SELECT DEVICE
    SELECT_DEVICE = State()
    CONTROL_DEVICE = State()
    
class CDStates(StatesGroup):
    OTHER = State()
    
    CAMERA = State()
    
    CURSOR = State()
    
    DESKTOP = State()
    
    EXPLORER = State()
    
    ALL = {'Прочее': OTHER, 'Камера': CAMERA, 'Курсор': CURSOR, 'Экран': DESKTOP, 'Проводник': EXPLORER}