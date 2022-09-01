from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from src.config.custom_filters import IsIncorrect, IsInt

from .states import BaseStates, RoomsStates
from ..config.config import MESSAGES, EMOJI
from ..keyboard.keyboard import rooms_kb, menu_kb, end_game_kb, remove_kb, choice_kb

from ..utils.Rooms.rooms import RoomManager
from ..utils.StoneGame.StoneGame import StoneGame
from ..import_bot import BOT

# Dispatcher
disp = None
    
async def choice_rooms(message):
    await RoomsStates.SHOW.set()
    await message.answer(MESSAGES['rooms']['help'], reply_markup=rooms_kb)
    await message.answer(RoomManager.show_rooms())
    

async def create_refresh_back(message):
    if(message.text == rooms_kb.keyboard[0][0]):
        RoomManager.create_room((message.from_user.id, message.from_user.first_name))
        await RoomsStates.INPUT_TITLE.set()
        await message.answer(MESSAGES['rooms']['input_title'], reply_markup=remove_kb)
    elif(message.text == rooms_kb.keyboard[1][0]):
        await message.answer(RoomManager.show_rooms(), reply_markup=rooms_kb)
    elif(message.text == rooms_kb.keyboard[2][0]):
        await message.answer(MESSAGES['menu']['back'], reply_markup=menu_kb)
    else:
        await BaseStates.IN_MENU.set()
        await message.answer(MESSAGES['menu']['input_error'])
        
async def input_title(message):
    if len(message.text) <= 16:
        RoomManager.set_title(message.from_user.id, message.text)
        await RoomsStates.INPUT_STONES.set()
        await message.answer(MESSAGES['input_stones']['init'])
    else:
        await message.answer(MESSAGES['rooms']['input_title_error'])
        
async def input_stones(message):
    stones = StoneGame.check_initial_stones(message.text)
    if stones:
        
        RoomManager.set_stones(message.from_user.id, stones)
        RoomManager.move_room(message.from_user.id)
        room = RoomManager.get_room(message.from_user.id, 'host')
        StoneGame.games[room.host.id] = room.game
        
        await RoomsStates.WAIT_OTHER_USER.set()
        await message.answer(MESSAGES['rooms']['wait_other_user'])
    else:
        await message.answer(MESSAGES['input_stones']['input_error'])
        
async def wait_other_user(message):
    await message.answer(MESSAGES['rooms']['please_wait'])
    
async def do_first_step(room):
    first_player = room.game.choice_player()
    text = MESSAGES['rooms']['first_step'].replace('#user#', first_player.name)
    room.game.who_step = first_player
    await BOT.send_message(room.host.id, text, reply_markup=choice_kb)
    await BOT.send_message(room.other_user.id, text, reply_markup=choice_kb)
    
async def join_room(message, state: FSMContext):
    if RoomManager.check_room_number(message.text):
        room = RoomManager.get_room(message.text, 'index')
        if(room):
            if(RoomManager.if_free_room(room)):
                RoomManager.set_player(message.text, (message.from_user.id,
                    message.from_user.first_name))
                
                await RoomsStates.PLAY_WITH_USER.set()
                await message.answer(MESSAGES['rooms']['you_joined'])
                
                state = disp.current_state(chat=room.host.id, user=room.host.id)
                await state.set_state(RoomsStates.PLAY_WITH_USER)
                await BOT.send_message(room.host.id, MESSAGES['rooms']['user_joined']
                    .replace('#user#', message.from_user.first_name))
                
                await do_first_step(room)
            else:
                await message.answer(MESSAGES['rooms']['error_join'])
        else:
            await message.answer(MESSAGES['rooms']['invalid_room'])
    else:
        await message.answer(MESSAGES['rooms']['room_num_error'])
        
async def end_game(room):
    winner = room.host if room.game.who_step == room.host else room.other_user
    
    state1 = disp.current_state(chat=room.host.id, user=room.host.id)
    state2 = disp.current_state(chat=room.other_user.id, user=room.other_user.id)
    
    #RoomManager.delete_room(room.host.id)
    
    await state1.set_state(RoomsStates.END_WITH_USER)
    await state2.set_state(RoomsStates.END_WITH_USER)
    
    await BOT.send_message(room.host.id, MESSAGES['win']['user']
        .replace('#user#', winner.name), reply_markup=end_game_kb)
    await BOT.send_message(room.other_user.id, MESSAGES['win']['user']
        .replace('#user#', winner.name), reply_markup=end_game_kb)

async def play_again_or_back(message):
    room = RoomManager.get_room(message.from_user.id, 'other_user') or (
        RoomManager.get_room(message.from_user.id, 'host'))
    if message.text == end_game_kb.keyboard[0][0]: # play again
    
        state1 =  disp.current_state(chat=room.host.id, user=room.host.id)
        state2 =  disp.current_state(chat=room.other_user.id, user=room.other_user.id)
        
        st1 = await state1.get_state()
        st2 = await state2.get_state()
        
        if(st1 == 'RoomsStates:WAIT_PLAY_AGAIN' or (
            st2 == 'RoomsStates:WAIT_PLAY_AGAIN')):
            
            StoneGame.restart_game(room.host.id)
            
            await state1.set_state(RoomsStates.PLAY_WITH_USER)
            await state2.set_state(RoomsStates.PLAY_WITH_USER)
            
            await do_first_step(room)
            
        else:
            send_to = room.other_user.id if message.from_user.id == room.host.id else room.host.id
            await RoomsStates.WAIT_PLAY_AGAIN.set()
            await message.answer(MESSAGES['rooms']['please_wait'], reply_markup=remove_kb)
            await BOT.send_message(send_to, MESSAGES['rooms']['user_play_again']
                .replace('#user#', message.from_user.first_name))

    elif message.text == end_game_kb.keyboard[1][0]:
        if message.from_user.id == room.host.id:
            temp_id = room.other_user.id
            RoomManager.delete_room(room.host.id)
            state = disp.current_state(chat=temp_id, user=room.other_user.id)
            await state.set_state(RoomsStates.SHOW)
            
            await BaseStates.IN_MENU.set() 
            await message.answer(MESSAGES['menu']['back'], reply_markup=menu_kb)
            
            await BOT.send_message(temp_id, MESSAGES['stop']['user']
                .replace('#user#', room.host.name), reply_markup=rooms_kb)
            await BOT.send_message(temp_id, MESSAGES['rooms']['help'],
                reply_markup=rooms_kb)
            await BOT.send_message(temp_id, RoomManager.show_rooms())           
            
            RoomManager.delete_room(room.host.id)
        else:
            await message.answer(MESSAGES['menu']['back'], reply_markup=menu_kb)
            await BaseStates.IN_MENU.set() 
            
            await BOT.send_message(room.host.id, MESSAGES['stop']['user']
                .replace('#user#', room.host.name), reply_markup=remove_kb)
            await BOT.send_message(room.host.id, MESSAGES['rooms']['please_wait'])
            state = disp.current_state(chat=room.host.id, user=room.host.id)
            await state.set_state(RoomsStates.WAIT_OTHER_USER)
            
            StoneGame.restart_game(room.host.id)
            
            RoomManager.delete_player(room.host.id)
    else:
        await message.answer(MESSAGES['menu']['input_error'])
        
async def wait_play_again(message):
    await message.answer(MESSAGES['rooms']['please_wait'])
        
async def play_with_user(message):
    room = RoomManager.get_room(message.from_user.id, 'host') or (
        RoomManager.get_room(message.from_user.id, 'other_user'))
        
    if room.game.who_step.id == message.from_user.id:
        if(message.text in EMOJI):
            step = StoneGame.check_step(EMOJI[message.text], room.host.id)
            if(step):
                send_to = room.other_user.id if message.from_user.id == room.host.id else room.host.id
                await BOT.send_message(send_to, message.text)
                if(StoneGame.step(step, room.host.id)):
                    await end_game(room)
                else:
                    room.game.next_step()
            else:
                await message.answer(MESSAGES['input_stones']['too_much_error'])
        else:
            await message.answer(MESSAGES['input_stones']['input_error']) 
    else:
        await message.answer(MESSAGES['rooms']['wait_step']) 
    
async def stop(message):
    room = RoomManager.get_room(message.from_user.id, 'host') or (
        RoomManager.get_room(message.from_user.id, 'other_user'))
    if room:
        if message.from_user.id == room.host.id:
            if room.other_user:
                state = disp.current_state(chat=room.other_user.id, user=room.other_user.id)
                await state.set_state(RoomsStates.SHOW)
                await BOT.send_message(room.other_user.id, MESSAGES['rooms']['user_stop']
                    .replace('#user#', room.host.name), reply_markup=rooms_kb)
    
            await BaseStates.IN_MENU.set() 
            await message.answer(MESSAGES['menu']['back'], reply_markup=menu_kb)
            
            RoomManager.delete_room(message.from_user.id)
        else:
            state = disp.current_state(chat=room.host.id, user=room.host.id)
            await state.set_state(RoomsStates.WAIT_OTHER_USER)
            await BaseStates.IN_MENU.set() 
            
            RoomManager.delete_player(room.host.id)
            StoneGame.restart_game(room.host.id)
            await message.answer(MESSAGES['menu']['back'], reply_markup=menu_kb)
            
            await BOT.send_message(room.host.id, MESSAGES['rooms']['user_stop']
                .replace('#user#', room.host.name))
            await BOT.send_message(room.host.id, MESSAGES['rooms']['please_wait'],
                reply_markup=remove_kb) 
            
    else:
        RoomManager.delete_room(message.from_user.id)
        await BaseStates.IN_MENU.set() 
        await message.answer(MESSAGES['menu']['back'], reply_markup=menu_kb)
    
def set_stop_handlers():
    attrs = dir(RoomsStates)
    i = 0
    while attrs[i] != '__class__':
        disp.register_message_handler(stop, state=getattr(RoomsStates, attrs[i]), commands='stop')
        i += 1
    
def register_rooms(dp):
    global disp
    disp = dp
    
    set_stop_handlers()
    
    dp.register_message_handler(choice_rooms, state=BaseStates.IN_MENU)
    dp.register_message_handler(join_room, IsInt(), state=RoomsStates.SHOW)
    dp.register_message_handler(create_refresh_back, state=RoomsStates.SHOW)
    dp.register_message_handler(input_title, state=RoomsStates.INPUT_TITLE)
    dp.register_message_handler(input_stones, state=RoomsStates.INPUT_STONES)
    dp.register_message_handler(wait_other_user, state=RoomsStates.WAIT_OTHER_USER)
    dp.register_message_handler(play_with_user, state=RoomsStates.PLAY_WITH_USER)
    dp.register_message_handler(play_again_or_back, state=RoomsStates.END_WITH_USER)
    dp.register_message_handler(wait_play_again, state=RoomsStates.WAIT_PLAY_AGAIN)
    
    
    
