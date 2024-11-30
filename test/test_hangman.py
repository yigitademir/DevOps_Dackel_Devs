import pytest
from server.py.game import Game, Player
from server.py.hangman import Hangman, HangmanGameState, GamePhase, GuessLetterAction, RandomPlayer


# Test class for Hangman game
class TestHangmanGame:
    def test_initialization(self):
        game = Hangman()
        assert game.word_to_guess == ""
        assert game.phase == GamePhase.SETUP
        assert game.guesses == []
        assert game.incorrect_guesses == []

    def test_get_state(self):
        game = Hangman()
        game_state = game.get_state()
        assert game_state.word_to_guess == ""
        assert game_state.phase == GamePhase.SETUP
        assert game_state.guesses == []
        assert game_state.incorrect_guesses == []

    def test_set_state(self):
        game = Hangman()
        new_state = HangmanGameState(
            word_to_guess="PYTHON",
            phase=GamePhase.RUNNING,
            guesses=["P", "Y", "T", "X"],
            incorrect_guesses=["X"]
        )
        game.set_state(new_state)
        assert game.word_to_guess == "PYTHON"
        assert game.phase == GamePhase.RUNNING
        assert game.guesses == ["P", "Y", "T", "X"]
        assert game.incorrect_guesses == ["X"]

    def test_print_state(self, capfd):
        game = Hangman()
        game.word_to_guess = "PYTHON"
        game.guesses = ["P", "Y", "X"]
        game.incorrect_guesses = ["X"]
        
        game.print_state()
        
        # Capture the output
        captured = capfd.readouterr()
        assert "Word: PY____" in captured.out  # Checking the masked word
        assert "Guesses: P, Y, X" in captured.out
        assert "Incorrect guesses: X" in captured.out
        assert "Remaining lives: 7" in captured.out

    def test_get_list_action(self):
        game = Hangman()
        game.phase = GamePhase.SETUP
        actions = game.get_list_action()
        assert actions == []

        game.phase = GamePhase.RUNNING
        game.guesses = ["A", "B"]
        actions = game.get_list_action()
        assert len(actions) > 0
        assert all(action.letter not in game.guesses for action in actions)

    def test_get_player_view(self):
        game = Hangman()
        game.word_to_guess = "PYTHON"
        game.guesses = ["P", "Y", "X"]
        game.incorrect_guesses = ["X"]
        player_view = game.get_player_view(idx_player=0)
        assert player_view.word_to_guess == "PY____"
        assert player_view.guesses == ["P", "Y", "X"]
        assert player_view.incorrect_guesses == ["X"]


# Test class for GuessLetterAction
class TestGuessLetterAction:
    def test_action_creation(self):
        action = GuessLetterAction(letter="P")
        assert action.letter == "P"


# Test class for HangmanGameState
class TestHangmanGameState:
    def test_state_creation(self):
        state = HangmanGameState(
            word_to_guess="PYTHON",
            phase=GamePhase.RUNNING,
            guesses=["P", "Y", "X"],
            incorrect_guesses=["X"]
        )
        assert state.word_to_guess == "PYTHON"
        assert state.phase == GamePhase.RUNNING
        assert state.guesses == ["P", "Y", "X"]
        assert state.incorrect_guesses == ["X"]
    
    def test_state_empty(self):
        state = HangmanGameState(
            word_to_guess="",
            phase=GamePhase.SETUP,
            guesses=[],
            incorrect_guesses=[]
        )
        assert state.word_to_guess == ""
        assert state.phase == GamePhase.SETUP
        assert state.guesses == []
        assert state.incorrect_guesses == []


# Test class for handling invalid guesses and edge cases
class TestInvalidGuesses:
    def test_invalid_guess(self):
        game = Hangman()
        game.word_to_guess = "PYTHON"
        action = GuessLetterAction(letter="1")
        game.apply_action(action)
        assert len(game.guesses) == 0  # Invalid guesses shouldn't be added


# Test class for edge case: no actions available in non-running phases
class TestNoActionsInNonRunningPhases:
    def test_no_actions_in_non_running_phases(self):
        game = Hangman()
        
        # Test when game is in SETUP phase
        game.phase = GamePhase.SETUP
        actions = game.get_list_action()
        assert actions == []

        # Test when game is in FINISHED phase
        game.phase = GamePhase.FINISHED
        actions = game.get_list_action()
        assert actions == []
