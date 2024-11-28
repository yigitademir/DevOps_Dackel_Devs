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
    
    def _convert_coordinate(self, coord: str) -> tuple:
        """Convert string coordinates like 'A1' into (row, col)."""
        row = ord(coord[0].upper()) - ord('A')  # Convert 'A' -> 0, 'B' -> 1, etc.
        col = int(coord[1:]) - 1  # Convert '1' -> 0, '2' -> 1, etc.
        return row, col
    
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

                # If all validations pass, assign the location and stop the loop
                ship.location = coordinates
                player.ships.append(ship)
                self.ships_to_place.remove(ship)  # Remove the ship from the list of ships to place
                valid_placement = True
                print(f"{ship.name} placed successfully at {', '.join(coordinates)}.")

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
        self.idx_player_active = state.idx_player_active
        self.phase = state.phase
        self.winner = state.winner
        self.players = state.players

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

    # Ship placement for Player 1 and Player 2
    for player_idx in range(len(game.state.players)):
        game.place_ships(player_idx)

    print("\nAll ships have been placed, ready to start the game.")
