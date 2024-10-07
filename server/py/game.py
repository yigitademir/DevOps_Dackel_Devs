from typing import List, Any, Dict
import abc

GameState = Any
GameAction = Any


class Game(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def set_state(self, state: GameState) -> None:
        """ Set the game to a given state """
        pass

    @abc.abstractmethod
    def get_state(self) -> GameState:
        """ Get the complete, unmasked game state """
        pass

    @abc.abstractmethod
    def print_state(self) -> None:
        """ Print the current game state """
        pass

    @abc.abstractmethod
    def get_list_action(self) -> List[GameAction]:
        """ Get a list of possible actions for the active player """
        pass

    @abc.abstractmethod
    def apply_action(self, action: GameAction) -> None:
        """ Apply the given action to the game """
        pass

    @abc.abstractmethod
    def get_player_view(self, idx_player: int) -> GameState:
        """ Get the masked state for the active player (e.g. the oppontent's cards are face down)"""
        pass


class Player(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def select_action(self, state: GameState, actions: List[GameAction]) -> GameAction:
        """ Given masked game state and possible actions, select the next action """
        pass
