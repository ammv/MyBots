from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.helper import Helper, HelperMode, ListItem

class BaseStates(StatesGroup):
    # MENU
    IN_MENU = State()
    
class ComputerStates(StatesGroup):
    # user input count of stones
    INPUT_STONES = State()
    
    # user play with computer
    START_PLAY = State()
    
    # user end game with computer
    END_PLAY = State()
    
class RoomsStates(StatesGroup):
    # SHOW ROOMS
    # user can write room number and join it
    SHOW = State()
    
    # user create room and input title
    INPUT_TITLE = State()
    
    # user create room and input count of stones
    INPUT_STONES = State()
    
    # user after confirm started wait other user
    WAIT_OTHER_USER = State()
    
    # play with other user
    PLAY_WITH_USER = State()
    
    # end of play with other user
    END_WITH_USER = State()
    
    # wait play again
    WAIT_PLAY_AGAIN = State()