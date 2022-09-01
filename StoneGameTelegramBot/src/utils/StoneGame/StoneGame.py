from random import choice
from typing import Optional, Tuple

from .compute_step import ComputeStep

class Player:
    def __init__(self, name: str, _id: Optional[int] = None):
        self.name = name
        self.id = _id
        
class Game:
    def __init__(self, player1: Player, player2: Player, stones: int):
        self.player1 = player1
        self.player2 = player2
        self.initial_stones = stones
        self.stones = stones
        self.who_step = None
        
    def choice_player(self) -> str:
        if self.player2 is None:
            return self.player1
        return choice((self.player1, self.player2))
        
    def next_step(self) -> None:
        self.who_step = self.player1 if self.who_step == self.player2 else self.player2
        
class StoneGame:
    games = {}
    
    @staticmethod
    def start_game(player1_data: Tuple[str, int],
        player2_data:Tuple[str, Optional[int]],
        stones: int) -> str:
        
        player1 = Player(*player1_data)
        player2 = Player(*player2_data)
        game_id = player1.id
        game = Game(player1, player2, stones)
                    
        StoneGame.games[game_id] = game
        
        return game.choice_player().name
        
    @staticmethod
    def get_game(game_id: int) -> Optional[Game]:
        if game_id in StoneGame.games:
            return StoneGame.games[game_id]
        return None
        
    @staticmethod
    def restart_game(game_id: int) -> str:
        game = StoneGame.games[game_id]
        game.stones = game.initial_stones
        
        return game.choice_player().name
        
    @staticmethod    
    def check_initial_stones(stones: str) -> int:
        if(stones.isdecimal()):
            stones = int(stones)
            if(stones > 6):
                return stones
        return 0
        
    @staticmethod
    def check_step(step: int, game_id: int) -> int:
        return step if StoneGame.games[game_id].stones - step >= 0 else 0
        
    @staticmethod
    def step(step: int, game_id: int) -> bool:
        #print('Step =', step, 'Stones =', StoneGame.games[game_id].stones)
        StoneGame.games[game_id].stones -= step
        return StoneGame.games[game_id].stones == 0
        
    @staticmethod
    def end_game(game_id: int) -> None:
        if(game_id in StoneGame.games):
            del StoneGame.games[game_id];
        
    @staticmethod
    def computer_step(game_id: int) -> int:
        return ComputeStep.compute(StoneGame.games[game_id].stones)
        
        