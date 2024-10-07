# runcmd: cd .. & venv\Scripts\python benchmark/benchmark_hangman.py python hangman.Hangman

import sys
import string
from benchmark import Benchmark
from server.py.hangman import HangmanGameState, GamePhase, GuessLetterAction


class HangmanBenchmark(Benchmark):

    def test_initial_game_state_values(self):
        """Test 001: Validate values of initial game state [1 point]"""
        self.game_server.reset()
        state = self.game_server.get_state()
        assert isinstance(state, HangmanGameState)
        assert state.guesses == []

    def test_set_state_method(self):
        """Test 002: Set/get methods work properly [1 point]"""
        self.game_server.reset()
        state = HangmanGameState(word_to_guess='devops', guesses=[], phase=GamePhase.RUNNING)
        self.game_server.set_state(state)
        game_state = self.game_server.get_state()
        assert state == game_state

    def test_action_list(self):
        """Test 003: Action list contains only 'unused' capital letters [1 point]"""
        self.game_server.reset()

        # initial actions
        actions = self.game_server.get_list_action()
        assert {action.letter for action in actions} == set(string.ascii_uppercase)

        # testcase 1
        test_state1 = HangmanGameState(word_to_guess="", guesses=['A','B','C'], phase=GamePhase.RUNNING)
        self.game_server.set_state(test_state1)
        actions1 = self.game_server.get_list_action()
        assert {action.letter for action in actions1} == set(string.ascii_uppercase[3:])

        # testcase 2
        test_state2 = HangmanGameState(word_to_guess="", guesses=[*string.ascii_uppercase], phase=GamePhase.RUNNING)
        self.game_server.set_state(test_state2)
        actions2 = self.game_server.get_list_action()
        assert len(actions2) == 0

    def test_apply_action_general(self):
        """Test 004: Apply action method adds new guess to gamestate [1 point]"""
        self.game_server.reset()
        self.game_server.apply_action(GuessLetterAction(letter='D'))
        state = self.game_server.get_state()
        assert state.guesses == ['D']

    def test_apply_action_lowercase(self):
        """Test 005: Apply action also works for lowercase letters [1 point]"""
        self.game_server.reset()
        self.game_server.apply_action(GuessLetterAction(letter='x'))
        state = self.game_server.get_state()
        assert state.guesses == ['X']

    def test_game_ending(self):
        """Test 006: Game ends with 8 wrong guesses or when secret word is revealed [1 point]"""
        self.game_server.reset()

        # 8 wrong guesses
        test_state1 = HangmanGameState(word_to_guess="XY", guesses=[*'ABCDEFG'], phase=GamePhase.RUNNING)
        self.game_server.set_state(test_state1)
        self.game_server.apply_action(GuessLetterAction(letter='H'))
        assert self.game_server.get_state().phase == GamePhase.FINISHED

        # secret word is revealed
        test_state2 = HangmanGameState(word_to_guess="XY", guesses=[*'AX'], phase=GamePhase.RUNNING)
        self.game_server.set_state(test_state2)
        self.game_server.apply_action(GuessLetterAction(letter='Y'))
        assert self.game_server.get_state().phase == GamePhase.FINISHED

    def test_secret_word_lowercase_letters(self):
        """Test 007: Game also works when secret words contain lowercase letters [1 point]"""
        self.game_server.reset()
        test_state1 = HangmanGameState(word_to_guess="Xy", guesses=[*'AY'], phase=GamePhase.RUNNING)
        self.game_server.set_state(test_state1)
        self.game_server.apply_action(GuessLetterAction(letter='x'))
        assert self.game_server.get_state().phase == GamePhase.FINISHED


if __name__ == "__main__":

    benchmark = HangmanBenchmark(sys.argv)
    benchmark.run_tests()
