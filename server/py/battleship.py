from typing import List, Optional
from enum import Enum
import random
from server.py.game import Game, Player


class ActionType(str, Enum):
    SET_SHIP = 'set_ship'
    SHOOT = 'shoot'


class BattleshipAction:

    def __init__(self, action_type: ActionType, ship_name: Optional[str], location: List[str]) -> None:
        self.action_type = action_type
        self.ship_name = ship_name # only for set_ship actions
        self.location = location


class Ship:

    def __init__(self, name: str, length: int, location: Optional[List[str]]) -> None:
        self.name = name
        self.length = length
        self.location = location


class PlayerState:

    def __init__(self, name: str, ships: List[Ship], shots: List[str], successful_shots: List[str]) -> None:
        self.name = name
        self.ships = ships
        self.shots = shots
        self.successful_shots = successful_shots


class GamePhase(str, Enum):
    SETUP = 'setup'            # before the game has started (including setting ships)
    RUNNING = 'running'        # while the game is running (shooting)
    FINISHED = 'finished'      # when the game is finished


class BattleshipGameState:

    def __init__(self, idx_player_active: int, phase: GamePhase, winner: Optional[int], players: List[PlayerState]) -> None:
        self.idx_player_active = idx_player_active
        self.phase = phase
        self.winner = winner
        self.players = players


class Battleship(Game):

    def __init__(self):
        """ Game initialization (set_state call not necessary) """
        pass

    def print_state(self) -> None:
        """ Print the game to a given state """
        print(f"Player {self.current_player}'s view:")
        if self.current_player == 1:
            self._print_grid(self.player1_grid, show_ships=True)
        else:
            self._print_grid(self.player2_grid, show_ships=True)
        print("\nOpponent's view:")
        opponent_grid = self.player2_grid if self.current_player == 1 else self.player1_grid
        self._print_grid(opponent_grid, show_ships=False)

    def get_state(self) -> BattleshipGameState:
        """ Get the complete, unmasked game state """
        pass

    def set_state(self, state: BattleshipGameState) -> None:
        """ Set the game to a given state """
        pass

    def get_list_action(self) -> List[BattleshipAction]:
        """ Get a list of possible actions for the active player """
        pass

    def apply_action(self, action: BattleshipAction) -> None:
        """ Apply the given action to the game """
        pass

    def get_player_view(self, idx_player: int) -> BattleshipGameState:
        """ Get the masked state for the active player (e.g. the oppontent's cards are face down)"""
        masked_players = []
        for i, player in enumerate(self.players):
            masked_ships = [] if i != idx_player else player.ships
            masked_players.append(
                PlayerState(
                    name=player.name,
                    ships=masked_ships,
                    shots=player.shots,
                    successful_shots=player.successful_shots,
                )
            )
        return BattleshipGameState(
            idx_player_active=self.idx_player_active,
            phase=self.phase,
            winner=self.winner,
            players=masked_players,
        )


class RandomPlayer(Player):

    def select_action(self, state: BattleshipGameState, actions: List[BattleshipAction]) -> Optional[BattleshipAction]:
        """ Given masked game state and possible actions, select the next action """
        if len(actions) > 0:
            return random.choice(actions)
        return None

    def place_ships_randomly(self, state: BattleshipGameState, ships: List[Ship]) -> List[BattleshipAction]:
        """ Generate random valid ship placement actions """
        actions = []
        for ship in ships:
            while True:
                # Generate random starting coordinates and direction
                x, y = random.randint(0, 9), random.randint(0, 9)  # Assuming a 10x10 grid
                direction = random.choice(['horizontal', 'vertical'])

                # Calculate ship locations
                if direction == 'horizontal':
                    location = [f"{x},{y + i}" for i in range(ship.length) if y + i < 10]
                else:
                    location = [f"{x + i},{y}" for i in range(ship.length) if x + i < 10]

                # Ensure ship fits on the grid and doesn't overlap
                if len(location) == ship.length and all(
                        self.is_valid_location(loc, state.players[self.idx].ships) for loc in location):
                    actions.append(BattleshipAction(ActionType.SET_SHIP, ship.name, location))
                    break
        return actions

    def is_valid_location(self, loc: str, ships: List[Ship]) -> bool:
        """ Check if a location is valid (doesn't overlap with existing ships) """
        for ship in ships:
            if loc in ship.location:
                return False
        return True

    def shoot_randomly(self, state: BattleshipGameState) -> Optional[BattleshipAction]:
        """ Generate a random shooting coordinate that hasn't been guessed """
        opponent = state.players[1 - state.idx_player_active]
        possible_shots = [f"{x},{y}" for x in range(10) for y in range(10)
                          if f"{x},{y}" not in opponent.shots]
        if possible_shots:
            shot = random.choice(possible_shots)
            return BattleshipAction(ActionType.SHOOT, None, [shot])
        return None


if __name__ == "__main__":

    game = Battleship()
