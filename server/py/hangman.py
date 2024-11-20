from mimetypes import guess_type
from typing import List, Optional
import random
from enum import Enum
from server.py.game import Game, Player


class GuessLetterAction:

    def __init__(self, letter: str) -> None:
        self.letter = letter


class GamePhase(str, Enum):
    SETUP = 'setup'            # before the game has started
    RUNNING = 'running'        # while the game is running
    FINISHED = 'finished'      # when the game is finished


class HangmanGameState:

    def __init__(self, word_to_guess: str, phase: GamePhase, guesses: List[str], incorrect_guesses: List[str]) -> None:
        self.word_to_guess = word_to_guess
        self.phase = phase
        self.guesses = guesses
        self.incorrect_guesses = incorrect_guesses


class Hangman(Game):

    def __init__(self) -> None:
        """ Important: Game initialization also requires a set_state call to set the 'word_to_guess' """
        super().__init__()
        self.set_state(game_state)


    def get_state(self) -> HangmanGameState:
        """ Get the complete, unmasked game state """
        pass

    def set_state(self, state: HangmanGameState) -> None:
        """ Set the game to a given state """
        self.word_to_guess = state.word_to_guess
        self.phase = state.phase
        self.guesses = state.guesses
        self.incorrect_guesses = state.incorrect_guesses

    def print_state(self) -> None:
        """ Print the current game state """
        pass

    def get_list_action(self) -> List[GuessLetterAction]:
        """ Get a list of possible actions for the active player """
        pass

    def apply_action(self, action: GuessLetterAction) -> None:
        """ Apply the given action to the game """
        pass

    def get_player_view(self, idx_player: int) -> HangmanGameState:
        """ Get the masked state for the active player (e.g. the opponent's cards are face down)"""
        pass


class RandomPlayer(Player):

    def select_action(self, state: HangmanGameState, actions: List[GuessLetterAction]) -> Optional[GuessLetterAction]:
        """ Given masked game state and possible actions, select the next action """
        if len(actions) > 0:
            return random.choice(actions)
        return None


if __name__ == "__main__":

    game = Hangman()
    game_state = HangmanGameState(word_to_guess='DevOps', phase=GamePhase.SETUP, guesses=[], incorrect_guesses=[])
    game.set_state(game_state)

    game_state.phase = GamePhase.RUNNING
    game.set_state(game_state)

    while game.phase == GamePhase.RUNNING:
        #Display the current game state
        print("Word to guess:", game.word_to_guess)
        print("Guessed letters", game.guesses)
        print("Incorrect guesses:", game.incorrect_guesses)

        #Ask for a guess
        guess = input("Guess a letter: ").lower()

        #Apply the guess action
        if guess in game.word_to_guess:
            print(f"Good guess! {guess} is in the word.")
            game.guesses.append(guess)
        else:
            print(f"Hmmm, {guess} is not in the word.")
            game.incorrect_guesses.append(guess)

        #Check if the game is over
        if len(game.incorrect_guesses) >= 8:
            game.phase = GamePhase.FINISHED
            print("Game over, better luck next time.")
        elif all(letter in game.guesses for letter in game.word_to_guess):
            game.phase = GamePhase.FINISHED
            print("Congratulations, you guessed the word!")

    #Show the final state
    print("Final word:", game.word_to_guess)
    print("Your guesses:", game.guesses)
    print("Incorrect guesses:", game.incorrect_guesses)

