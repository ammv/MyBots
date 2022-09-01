import emoji

from typing import Tuple, Union, Optional, Any
from ..StoneGame.StoneGame import Player, Game

rock_emoji = emoji.emojize(':rock:', language='alias')

class Room:
    def __init__(self, host: Player):
        self.host = host
        self.other_user = None
        self.title = None
        
    def get_title(self):
        return f'{self.title} {self.game.initial_stones}{rock_emoji}'
        
class RoomManager:
    rooms = {}
    creating_rooms = {}
    
    def show_rooms():
        if len(RoomManager.rooms):
            return 'List of rooms:\n' + ''.join(f'{index+1}\. {room.get_title()}'
                for index, room in enumerate(RoomManager.rooms.values()))
        return 'There are no rooms right now, but you can create your own\!'
        
    def create_room(host: Tuple[int, str]) -> None:
        player = Player(host[1], host[0])
        RoomManager.creating_rooms[player.id] = Room(player)
        
    def check_room_number(num: str) -> bool:
        if num.isdecimal():
            num = int(num)
            return 0 < num <= len(RoomManager.rooms)
        return False
        
    def get_room(num: str, by: Optional[str]) -> Optional[Room]:
        num = int(num)
        if by == 'host':
            return RoomManager.rooms.get(num, None)
        elif by == 'other_user':
            for room in RoomManager.rooms.values():
                if room.other_user.id == num:
                    return room
        elif by == 'index':
            return RoomManager.rooms[tuple(RoomManager.rooms.keys())[num-1]]
        return None
        
    def if_free_room(room: Room) -> bool:
        return room.other_user == None
        
    def delete_room(host_id: int) -> None:
        if host_id in RoomManager.rooms:
            del RoomManager.rooms[host_id]
        if host_id in RoomManager.creating_rooms:
            del RoomManager.creating_rooms[host_id]
        
    def _set_attr_room(host_id: int, attr: str, value: Union[int, str, Player],
        is_creating_room: bool = True) -> None:
        if is_creating_room:
            setattr(RoomManager.creating_rooms[host_id], attr, value)
        else:
            setattr(RoomManager.rooms[host_id], attr, value)
        
    def set_title(host_id, title: str) -> None:
        RoomManager._set_attr_room(host_id, 'title', title)
        
    def set_stones(host_id: int, stones: int) -> None:
        host = RoomManager.creating_rooms[host_id].host
        game = Game(Player(host.name, host.id), Player(None, None), stones)
        RoomManager._set_attr_room(host_id, 'game', game)
        
    def move_room(host_id: int) -> None:
        RoomManager.rooms[host_id] = RoomManager.creating_rooms[host_id]
        del RoomManager.creating_rooms[host_id]
        
    def set_player(num: str, user: Tuple[int, str]) -> None:
        room = RoomManager.get_room(num, 'index')
        player = Player(user[1], user[0])
        room.game.player2 = player
        RoomManager._set_attr_room(room.host.id, 'other_user', player, False)
        
    def delete_player(host_id: int) -> None:
        room = RoomManager.get_room(host_id, 'host')
        if room:
            room.other_user = None
            room.game.player2 = None