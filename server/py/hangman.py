from typing import List, Optional
import random
from enum import Enum
from pydantic import BaseModel
from server.py.game import Game, Player


class GuessLetterAction(BaseModel):
    letter: str


class GamePhase(str, Enum):
    SETUP = 'setup'            # before the game has started
    RUNNING = 'running'        # while the game is running
    FINISHED = 'finished'      # when the game is finished


class HangmanGameState(BaseModel):
    word_to_guess: str
    phase: GamePhase
    guesses: List[str]
    incorrect_guesses: List[str]

class Hangman(Game):

    def __init__(self) -> None:
        """ Important: Game initialization also requires a set_state call to set the 'word_to_guess' """
        self.word_to_guess = ""
        self.phase = GamePhase.SETUP
        self.guesses: List[str] = []
        self.incorrect_guesses: List[str] = []


    def get_state(self) -> HangmanGameState:
        """ this method should return the current HangmanGameState """
        return HangmanGameState(
            word_to_guess=self.word_to_guess,
            phase=self.phase,
            guesses=self.guesses,
            incorrect_guesses=self.incorrect_guesses
        )

    def set_state(self, state: HangmanGameState) -> None:
        """ Set the game to a given state """
        self.word_to_guess = state.word_to_guess
        self.phase = state.phase
        self.guesses = state.guesses
        self.incorrect_guesses = state.incorrect_guesses

    def print_state(self) -> None:
        """ this method should output the masked word, showing correctly guessed letters and hiding others. """
        masked_word = ''.join(
            letter if letter in self.guesses else '_'
            for letter in self.word_to_guess
        )
        print(f"Word: {masked_word}")
        print(f"Guesses: {', '.join(self.guesses)}")
        print(f"Incorrect guesses: {', '.join(self.incorrect_guesses)}")
        print(f"Remaining lives: {8 - len(self.incorrect_guesses)}")

    def get_list_action(self) -> List[GuessLetterAction]:
        """ Get a list of possible actions for the active player """
        if self.phase != GamePhase.RUNNING:
            return [] # there are no actions if GamePhase is SETUP or FINISHED
        all_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        unused_letters = [i for i in all_letters if i not in self.guesses]
        print(f"Unused letters: {unused_letters}")
        return [GuessLetterAction(letter=letter) for letter in unused_letters]

    def apply_action(self, action: GuessLetterAction) -> None:
        """ Apply the given action to the game """
        if self.phase != GamePhase.RUNNING:
            return

        guess = action.letter.strip().upper()

        if guess in self.guesses:
            return # Ignore already guessed letters

        self.guesses.append(guess) # Add the guessed letter to the list of guesses

        # Apply the guess action
        if guess in self.word_to_guess.upper():
            print(f"Good guess! {guess} is in the word.")
        else:
            print(f"Hmmm, {guess} is not in the word.")
            self.incorrect_guesses.append(guess)

        # Check if the game is over
        if len(self.incorrect_guesses) >= 8:
            self.phase = GamePhase.FINISHED
            print("Game over, better luck next time.")
        elif all(letter.upper() in self.guesses for letter in self.word_to_guess):
            self.phase = GamePhase.FINISHED
            print("Congratulations, you guessed the word!")

    def get_player_view(self, idx_player: int) -> HangmanGameState:
        masked_word = ''.join(
            letter if letter in self.guesses else '_'
            for letter in self.word_to_guess
        )

        # Return the masked state for the player
        return HangmanGameState(word_to_guess = masked_word,
                                phase = self.phase,
                                guesses =self.guesses,
                                incorrect_guesses=self.incorrect_guesses
                                )

class RandomPlayer(Player):
    # pylint: disable=too-few-public-methods
    def select_action(self, state: HangmanGameState, actions: List[GuessLetterAction]) -> Optional[GuessLetterAction]:
        """ Given masked game state and possible actions, select the next action """
        if len(actions) > 0:
            return random.choice(actions)
        return None


if __name__ == "__main__":

    # Initialize the game
    game = Hangman()

    # Input the word to guess (setup phase)
    while True:
        word_to_guess = input("Enter a word to guess (letters only): ").strip().upper()
        if word_to_guess.isalpha():
            break
        print("Invalid input. Please enter a valid word.")

    # Set initial game state
    game_state = HangmanGameState(
        word_to_guess=word_to_guess,
        phase=GamePhase.RUNNING,
        guesses=[],
        incorrect_guesses=[]
    )
    game.set_state(game_state)

    # create instance of Random Player class
    player = RandomPlayer()

    # Main game loop
    while game.phase == GamePhase.RUNNING:
        player_view = game.get_player_view(idx_player=0)
        print(f"Player's view: {player_view.word_to_guess}") # Showing the masked word
        player_actions = game.get_list_action() # Get possible actions
        player_action = player.select_action(game.get_state(), player_actions) # Player selects an action
        if player_action:
            print(f"Player guesses: {player_action.letter}")
            game.apply_action(player_action)

    game.print_state()
