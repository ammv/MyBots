from .menu import register_menu
from .game_computer import register_game_computer
from .rooms import register_rooms

def register_handlers(dp):
    register_menu(dp)
    register_game_computer(dp)
    register_rooms(dp)
