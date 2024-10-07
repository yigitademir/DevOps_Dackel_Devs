# runcmd: cd .. & venv\Scripts\python benchmark/benchmark_battleship.py python battleship.Battleship
import sys
import string
from benchmark import Benchmark


class BattleshipBenchmark(Benchmark):
    """
    initial game state (5 points)
    ships
    - correct field names (multiple iterations) (1 point)
    - use ships of correct length (3 points)
    - placement not overlapping (multiple iterations) (2 points)
    - vertical and horizontal placements (multiple iterations) (1 point)
    - placements change (are not fixed)(multiple iterations) (1 point)
    - ships are all set after the first 10 rounds (1 point)
    - ship placement actions?
    
    shots
    - no shots in the first 10 rounds (1 point)
    - correct shoot actions (1 point)
    - remember already targeted areas (1 point)
    """

    VALID_LOCATIONS = [x_name + str(y_name) for x_name in list(string.ascii_uppercase)[:10] for y_name in range(1, 11)]

    def play_first_n_rounds(self, num_rounds: int):
        self.game_server.reset()
        for _ in range(num_rounds):
            try:
                action = self.game_server.select_action()
            except ValueError:
                break
            self.game_server.apply_action(action)

    def test_initial_game_state_structure(self):
        """Test 001: Validate structure of initial game state (cnt_round=1) [5 points]"""
        self.game_server.reset()
        state = self.game_server.get_state()
        for player in state.players:
            assert player.shots == [], f"Error: Shots of '{player.name}' are not empty"
            for ship in  player.ships:
                assert ship.location is None, f"Error: Ship '{ship.name}' of player '{player.name}' is already set"

    def test_ships_locations(self):
        """Test 002: Correct ship location names [1 point]"""
        for _ in range(10):
            self.play_first_n_rounds(10)
            state = self.game_server.get_state()
            for player in state.players:
                for ship in  player.ships:
                    for field in ship.location:
                        assert field in self.VALID_LOCATIONS, f"Error: '{field}' is not a valid location"

    def test_ships_length(self):
        """Test 003: Ships with correct length [3 point]"""
        self.game_server.reset()
        state = self.game_server.get_state()
        for player in state.players:
            ship_lengths = sorted([ship.length for ship in player.ships])
            assert ship_lengths == [2,3,3,4,5], "Error: There have to be ships with exactly these lengths: 2,3,3,4,5"

    def test_ships_not_overlapping(self):
        """Test 004: Ships are not overlapping [2 point]"""
        for _ in range(10):
            self.play_first_n_rounds(10)
            state = self.game_server.get_state()
            for player in state.players:
                locations = [loc for ship in player.ships for loc in ship.location]
                assert len(locations) == len(set(locations)), "Error: Some ship locations are overlapping"

    def test_ships_vertical_and_horizontal(self):
        """Test 005: Ships are located vertical and horizontal [1 point]"""
        vertical = False
        horizontal = False
        for _ in range(10):
            self.play_first_n_rounds(10)
            state = self.game_server.get_state()
            for player in state.players:
                for ship in player.ships:
                    x_coord = set(field[0] for field in ship.location)
                    y_coord = set(field[1:] for field in ship.location)
                    if len(x_coord) == 1:
                        horizontal = True
                    elif len(y_coord) == 1:
                        vertical = True
        assert horizontal, "Error: Ships are only located vertically"
        assert vertical, "Error: Ships are only located horizontally"

    def test_ships_placements_changing(self):
        """Test 006: Location of ships is different on each run [1 point]"""
        states = []
        equals = 0
        for _ in range(10):
            self.play_first_n_rounds(10)
            state = self.game_server.get_state()
            state.idx_player_active = 0
            for past_state in states:
                if past_state == state:
                    equals += 1
            states.append(state)
        assert equals < 3, "Error: Location of ships does not change"

    def test_ships_all_set_after_10_rounds(self):
        """Test 007: After the first 10 rounds all ships are located [1 point]"""
        self.play_first_n_rounds(10)
        state = self.game_server.get_state()
        for player in state.players:
            for ship in player.ships:
                assert ship.location is not None, f"Ship {ship.name} is not located after the first 10 rounds"

    def test_shots_no_shots_first_10_rounds(self):
        """Test 008: No shots fired in the first 10 rounds [1 point]"""
        self.play_first_n_rounds(10)
        state = self.game_server.get_state()
        for player in state.players:
            assert len(player.shots) == 0, f"Player '{player.name}' fired too soon!"

    def test_shots_correct_actions(self):
        """Test 009: Correct shoot options [1 point]"""
        self.play_first_n_rounds(10)
        options = []
        for action in self.game_server.game.get_list_action():
            assert action.type == 'shoot', "After 10 rounds, game should return shoot actions"
            assert action.ship_name is None, "A shoot action, cannot have a ship name"
            options.extend(action.location)
        assert len(set(options).symmetric_difference(set(self.VALID_LOCATIONS))) == 0, "Invalid shoot locations"

    def test_shots_remember_targets(self):
        """Test 010: Remember areas already targeted [1 point]"""
        self.play_first_n_rounds(210)
        state = self.game_server.get_state()
        for player in state.players:
            assert len(set(player.shots)) == len(player.shots), "One target location has already been fired at once"


if __name__ == '__main__':

    benchmark = BattleshipBenchmark(sys.argv)
    benchmark.run_tests()
