from typing import List, Optional
from enum import Enum
import random
from game import Game, Player
import string


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

    VALID_LOCATIONS = [
        f"{letter}{number}"
        for letter in string.ascii_uppercase[:10]
        for number in range(1, 11)
    ]

    def __init__(self):
        """ Game initialization (set_state call not necessary) """
        self.state = BattleshipGameState(
            idx_player_active=0,
            phase=GamePhase.SETUP,
            winner=None,
            players=[
                PlayerState(name="Player 1",
                            ships=[
                                Ship("Carrier", 5),
                                Ship("Battleship", 4),
                                Ship("Cruiser", 3),
                                Ship("Submarine", 3),
                                Ship("Destroyer", 2),
                            ],
                            shots=[],
                            successful_shots=[]
                ),
                PlayerState(name="Player 2",
                            ships=[
                                Ship("Carrier", 5, ),
                                Ship("Battleship", 4, ),
                                Ship("Cruiser", 3),
                                Ship("Submarine", 3),
                                Ship("Destroyer", 2),
                            ],
                            shots=[],
                            successful_shots=[]
                ),
            ],
        )

    def print_state(self) -> None:
        """ Print the current game state """
        for i, player in enumerate(self.state.players):
            print(f"Player {i + 1}: {player.name}")
            for ship in player.ships:
                print(f"  {ship.name} (Length {ship.length}): {ship.location or 'Not placed'}")
            print(f"Shots: {player.shots}")
            print(f"Successful Shots: {player.successful_shots}")
        print(f"Active Player: Player {self.state.idx_player_active + 1}")
        print(f"Game Phase: {self.state.phase}")
        if self.state.winner is not None:
            print(f"Winner: Player {self.state.winner + 1}")

    def get_state(self) -> BattleshipGameState:
        """ Get the complete, unmasked game state """
        return self.state

    def set_state(self, state: BattleshipGameState) -> None:
        """ Set the game to a given state """
        self.state = state

    def get_list_action(self) -> List[BattleshipAction]:
        """ Get a list of possible actions for the active player """
        active_player = self.state.players[self.state.idx_player_active]
        if self.state.phase == GamePhase.SETUP:
            actions = []
            for ship in active_player.ships:
                if not ship.location:
                    for i in range(10):
                        x_start = random.randint(0, 10 - ship.length)
                        orientation = random.choice(["H", "V"])
                        if orientation == "H":
                            location = [f"{chr(65 + x_start + j)}{i + 1}" for j in range(ship.length)]
                        else:
                            location = [f"{chr(65 + x_start)}{i + 1 + j}" for j in range(ship.length)]
                        if all(loc in self.VALID_LOCATIONS for loc in location):
                            actions.append(BattleshipAction(ActionType.SET_SHIP, ship.name, location))
            return actions
        elif self.state.phase == GamePhase.RUNNING:
            actions = [
                BattleshipAction(ActionType.SHOOT, None, [loc])
                for loc in self.VALID_LOCATIONS
                if loc not in active_player.shots
            ]
            return actions
        return []

    def apply_action(self, action: BattleshipAction) -> None:
        """ Apply the given action to the game """
        active_player = self.state.players[self.state.idx_player_active]
        opponent = self.state.players[1 - self.state.idx_player_active]

        if action.action_type == ActionType.SET_SHIP:
            for ship in active_player.ships:
                if ship.name == action.ship_name:
                    ship.location = action.location
            if all(ship.location for ship in active_player.ships):
                if self.state.idx_player_active == 0:
                    self.state.idx_player_active = 1
                else:
                    self.state.phase = GamePhase.RUNNING
                    self.state.idx_player_active = 0
        elif action.action_type == ActionType.SHOOT:
            target = action.location[0]
            active_player.shots.append(target)
            hit = any(target in ship.location for ship in opponent.ships if ship.location)
            if hit:
                active_player.successful_shots.append(target)
                for ship in opponent.ships:
                    if target in ship.location:
                        ship.location.remove(target)
            if all(not ship.location for ship in opponent.ships):
                self.state.phase = GamePhase.FINISHED
                self.state.winner = self.state.idx_player_active
            else:
                self.state.idx_player_active = 1 - self.state.idx_player_active

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
    # Initialize the game
    game = Battleship()

    while game.state.phase != GamePhase.FINISHED:
        game.print_state()
        actions = game.get_list_action()
        if not actions:
            break
        action = RandomPlayer().select_action(game.get_state(), actions)
        game.apply_action(action)

    game.print_state()
    print("Game Over!")
