import emoji

from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from ..config.config import EMOJI

def add_buttons(kb, buttons):
    for button in buttons:
        if isinstance(button, tuple):
            kb.add(*button)
        else:
            kb.add(button)

menu_buttons = (
    emoji.emojize('Computer :robot:', language='alias'),
    emoji.emojize('Rooms :door:'))
menu_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
add_buttons(menu_kb, menu_buttons)

choice_buttons = tuple(EMOJI) # [1], [3], [4]
choice_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
add_buttons(choice_kb, choice_buttons)

end_game_buttons = (
    emoji.emojize('Play again :arrows_counterclockwise:', language='alias'),
    emoji.emojize('Back to the menu :back:', language='alias'))
end_game_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
add_buttons(end_game_kb, end_game_buttons)

rooms_buttons = (
    emoji.emojize('Create room :sparkle:', language='alias'),
    emoji.emojize('Refresh :arrows_counterclockwise:', language='alias'),
    emoji.emojize('Back to the menu :back:', language='alias'))
rooms_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

add_buttons(rooms_kb, rooms_buttons)

remove_kb = ReplyKeyboardRemove()