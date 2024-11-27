from typing import List, Optional
from enum import Enum
import random
from game import Game, Player


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
        self.hit_count = 0

    @property
    def is_sunk(self) -> bool:
        """Determine if the ship is destroyed based on hit_count and length."""
        return self.hit_count >= self.length


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
        self.board_size = 10  # Board is 10x10
        self.ships_to_place = [
            Ship("carrier", 5, None),
            Ship("battleship", 4, None),
            Ship("cruiser", 3, None),
            Ship("submarine", 3, None),
            Ship("destroyer", 2, None)
        ]
        self.state = BattleshipGameState(
            idx_player_active=0,
            phase=GamePhase.SETUP,
            winner=None,
            players=[
                PlayerState("Player 1", [], [], []),
                PlayerState("Player 2", [], [], [])
            ]
        )
    
    def is_within_bounds(self, coordinates: List[str]) -> bool:
        """Check if all coordinates are within the board boundaries."""
        for coord in coordinates:
            row, col = self._convert_coordinate(coord)
            if row < 0 or row >= self.board_size or col < 0 or col >= self.board_size:
                return False
        return True

    def is_overlap(self, coordinates: List[str], player: PlayerState) -> bool:
        """Check if the given coordinates overlap with any existing ships."""
        for ship in player.ships:
            if ship.location:
                if set(coordinates) & set(ship.location):  # Check for intersection
                    return True
        return False
    
    def _convert_coordinate(self, coord: str) -> tuple:
        """Convert string coordinates like 'A1' into (row, col)."""
        row = ord(coord[0].upper()) - ord('A')  # Convert 'A' -> 0, 'B' -> 1, etc.
        col = int(coord[1:]) - 1  # Convert '1' -> 0, '2' -> 1, etc.
        return row, col

    def place_ships(self, player_idx: int) -> None:
        """Handle ship placement for a player."""
        player = self.state.players[player_idx]
        print(f"{player.name}, it's time to place your ships.")

        for ship in self.ships_to_place:
            valid_placement = False

            while not valid_placement:
                print(f"\nPlace your {ship.name} (length {ship.length}).")
                coordinates = input(f"Enter {ship.length} coordinates separated by space (e.g., A1 A2): ").strip().upper().split()

                # Validate the placement
                if len(coordinates) != ship.length:
                    print("Invalid input: Number of coordinates must match the ship's length.")
                    continue

                if not self.is_within_bounds(coordinates):
                    print("Invalid placement: One or more coordinates are out of bounds.")
                    continue

                if self.is_overlap(coordinates, player):
                    print("Invalid placement: Ship overlaps with another ship.")
                    continue

                # Validate that the coordinates are consecutive
                if not self._is_consecutive(coordinates):
                    print("Invalid placement: Coordinates must be consecutive in a straight line.")
                    continue

                # If all validations pass
                ship.location = coordinates
                player.ships.append(ship)
                valid_placement = True
                print(f"{ship.name} placed successfully at {', '.join(coordinates)}.")

    def _is_consecutive(self, coordinates: List[str]) -> bool:
        """Check if the coordinates are consecutive in a straight line."""
        rows, cols = [], []
        for coord in coordinates:
            row, col = self._convert_coordinate(coord)
            rows.append(row)
            cols.append(col)

        # Check for horizontal alignment (rows same, columns consecutive)
        if len(set(rows)) == 1 and sorted(cols) == list(range(min(cols), max(cols) + 1)):
            return True

        # Check for vertical alignment (columns same, rows consecutive)
        if len(set(cols)) == 1 and sorted(rows) == list(range(min(rows), max(rows) + 1)):
            return True

        return False

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

    def select_action(self, state: BattleshipGameState, actions: List[BattleshipAction]) -> Optional[BattleshipAction]:
        """ Given masked game state and possible actions, select the next action """
        if len(actions) > 0:
            return random.choice(actions)
        return None


if __name__ == "__main__":

    game = Battleship()

    # Ship placement for Player 1 and Player 2
    for player_idx in range(len(game.state.players)):
        game.place_ships(player_idx)

    print("\nAll ships have been placed, ready to start the game.")
