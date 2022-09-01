from aiogram.dispatcher.filters import Text

from .states import BaseStates, ComputerStates
from ..config.config import MESSAGES, STEPS, EMOJI
from ..keyboard.keyboard import (
    menu_kb, choice_kb, remove_kb, end_game_kb)
    
from ..utils.StoneGame.StoneGame import StoneGame
    
# If user choice 'Computer :robot:' button in the keyboard
async def choice_computer(message):
    await message.answer(MESSAGES['start_game']['computer'])
    await message.answer(MESSAGES['input_stones']['init'], reply_markup=remove_kb)
    await ComputerStates.INPUT_STONES.set()
    
# Choice who first step: user of computer
async def do_first_step(first_step: str, message):
    await message.answer(f'{first_step} goes first\!', reply_markup=choice_kb)
    if (first_step == 'Computer'):
        step = StoneGame.computer_step(message.from_user.id)
        StoneGame.step(step, message.from_user.id)
        await message.answer(STEPS[step])
    
# User input count of stones for game with computer
async def input_stones(message):
    stones = StoneGame.check_initial_stones(message.text)
    if(stones):
        await ComputerStates.START_PLAY.set()
        first_step = StoneGame.start_game(
            (message.from_user.first_name, message.from_user.id),
            ('Computer', None), stones
        )
        await do_first_step(first_step, message)
    else:
        await message.answer(MESSAGES['input_stones']['input_error'])
        
# send message about win 
async def send_win_message(who_win: str, message):
    await message.answer(MESSAGES['win'][who_win], reply_markup=end_game_kb)
        
# after correct input count of stones
async def play_with_computer(message):
    if(message.text in EMOJI):
        step = StoneGame.check_step(EMOJI[message.text], message.from_user.id)
        if(step):
            if(StoneGame.step(step, message.from_user.id)):
                await send_win_message('you', message)
                await ComputerStates.END_PLAY.set()
            else:
                step = StoneGame.computer_step(message.from_user.id)
                await message.answer(STEPS[step])
                if(StoneGame.step(step, message.from_user.id)):
                    await send_win_message('computer', message)
                    await ComputerStates.END_PLAY.set()
        else:
            await message.answer(MESSAGES['input_stones']['too_much_error'])
    else:
        await message.answer(MESSAGES['input_stones']['input_error'])  

# user or computer win and bot waited action from user: play again or back to menu
async def end_game_computer(message):
    if(message.text == end_game_kb.keyboard[0][0]):
        first_step = StoneGame.restart_game(message.from_user.id)
        await do_first_step(first_step, message)
        await ComputerStates.START_PLAY.set()
    elif(message.text == end_game_kb.keyboard[1][0]):
        StoneGame.end_game(message.from_user.id)
        await message.answer(MESSAGES['menu']['back'], reply_markup=menu_kb)
        await BaseStates.IN_MENU.set()
    else:
        await message.answer(MESSAGES['menu']['input_error'])
        
async def stop_game_computer(message):
    StoneGame.end_game(message.from_user.id)
    await message.answer(MESSAGES['menu']['back'], reply_markup=menu_kb)
    await BaseStates.IN_MENU.set()
    
def register_game_computer(dp):
    dp.register_message_handler(stop_game_computer, commands='stop',
        state=ComputerStates.START_PLAY)
    dp.register_message_handler(stop_game_computer, commands='stop',
        state=ComputerStates.INPUT_STONES)
    dp.register_message_handler(stop_game_computer, commands='stop',
        state=ComputerStates.END_PLAY)
        
    dp.register_message_handler(choice_computer, Text(equals = menu_kb.keyboard[0][0]),
        state=BaseStates.IN_MENU)
    dp.register_message_handler(input_stones, state=ComputerStates.INPUT_STONES)
    dp.register_message_handler(play_with_computer, state=ComputerStates.START_PLAY)
    dp.register_message_handler(end_game_computer, state=ComputerStates.END_PLAY)
        
    
        
