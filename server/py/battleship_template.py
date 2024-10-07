from server.py.game import Game, Player
from typing import List, Optional
from pydantic import BaseModel
from enum import Enum
import random


class ActionType(str, Enum):
    SET_SHIP = 'set_ship'
    SHOOT = 'shoot'


class BattleshipAction(BaseModel):
    type: ActionType
    ship_name: Optional[str]
    location: List[str]


class Ship(BaseModel):
    name: str
    length: int
    location: Optional[List[str]] = None


class PlayerState(BaseModel):
    name: str
    ships: List[Ship] = [
        Ship(name="carrier", length=5),
        Ship(name="battleship", length=4),
        Ship(name="cruiser", length=3),
        Ship(name="submarine", length=3),
        Ship(name="destroyer", length=2),
    ]
    shots: List[str] = []
    successful_shots: List[str] = []


class BattleshipGameState(BaseModel):
    idx_player_active: int
    is_finished: bool
    winner: Optional[int]
    players: List[PlayerState]


class Battleship(Game):

    def __init__(self):
        pass

    def print_state(self) -> None:
        """ Set the game to a given state """
        pass

    def get_state(self) -> BattleshipGameState:
        """ Get the complete, unmasked game state """
        pass

    def set_state(self, state: BattleshipGameState) -> None:
        """ Print the current game state """
        pass

    def get_list_action(self) -> List[BattleshipAction]:
        """ Get a list of possible actions for the active player """
        pass

    def apply_action(self, action: BattleshipAction) -> None:
        """ Apply the given action to the game """
        pass

    def get_player_view(self, idx_player: int) -> BattleshipGameState:
        """ Get the masked state for the active player (e.g. the oppontent's cards are face down)"""
        pass


class RandomPlayer(Player):

    def select_action(self, state: BattleshipGameState, actions: List[BattleshipAction]) -> BattleshipAction:
        """ Given masked game state and possible actions, select the next action """
        if len(actions) > 0:
            return random.choice(actions)
        return None
