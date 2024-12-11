import pytest
from server.py.game import Game, Player
from server.py.dog import Dog, GameState, GamePhase, Action, PlayerState, Marble, Card, RandomPlayer


# Test class for Hangman game
class TestHangmanGame:
    def test_initialization(self):
        game = Dog()
        assert game.state.cnt_round == 1
        assert game.state.phase == GamePhase.RUNNING
        assert game.state.bool_card_exchanged == False
        assert game.state.idx_player_started == 0  # Default starting player index - will assign random value below
        assert game.state.idx_player_active == 0  # Same as idx_player_started initially
        assert len(game.state.list_card_draw) == 86  # Will populate below
        assert len(game.state.list_card_discard) == 0  # Discard pile is initially empty
        assert len(game.state.list_player) == 4  # Will populate players below