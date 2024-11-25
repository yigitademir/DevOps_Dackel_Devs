from typing import List, Optional
import random
from enum import Enum
from server.py.game import Game, Player


class GuessLetterAction:
    def __init__(self, letter: str):
        self.letter = letter


class GamePhase(str, Enum):
    SETUP = 'setup'            # before the game has started
    RUNNING = 'running'        # while the game is running
    FINISHED = 'finished'      # when the game is finished


class HangmanGameState:

    def __init__(self, word_to_guess: str, phase: str, guesses: List[str]) -> None:
        self.word_to_guess = word_to_guess
        self.phase = phase
        self.guesses = guesses


class Hangman(Game):

    def __init__(self) -> None:
        """ Important: Game initialization also requires a set_state call to set the 'word_to_guess' """
        self.word_to_guess = ""
        self.phase = GamePhase.SETUP
        self.guesses = []
        self.incorrect_guesses = []


    def get_state(self) -> HangmanGameState:
        """ this method should return the current HangmanGameState """
        return HangmanGameState(
            word_to_guess=self.word_to_guess,
            phase=self.phase,
            guesses=self.guesses,
        )

    def set_state(self, state: HangmanGameState) -> None:
        """ Set the game to a given state """
        self.word_to_guess = state.word_to_guess
        self.phase = state.phase
        self.guesses = state.guesses

    def print_state(self) -> None:
        """ this method should output the masked word, showing correctly guessed letters and hiding others. """
        masked_word = ''.join(
            letter if letter in self.guesses else '_'
            for letter in self.word_to_guess
        )
        print(f"Word: {masked_word}")
        print(f"Incorrect guesses: {', '.join(self.incorrect_guesses)}")
        print(f"Remaining lives: {8 - len(self.incorrect_guesses)}")

    def get_list_action(self) -> List[GuessLetterAction]:
        """ Get a list of possible actions for the active player """
        if self.phase != GamePhase.RUNNING:
            return [] # there are no actions if GamePhase is SETUP or FINISHED
        
        all_letters = "abcdefghijklmnopqrstuvwxyz"
        unused_letters = [i for i in all_letters if i not in self.guesses + self.incorrect_guesses]
        print(f"Unused letters: {unused_letters}")
        return [GuessLetterAction(letter) for letter in unused_letters]
                
    def apply_action(self, action: GuessLetterAction) -> None:
        """ Apply the given action to the game """
        if self.phase != GamePhase.RUNNING:
            return

        guess = action.letter.lower()

        # Ignore already guessed letters
        if guess in self.guesses or guess in self.incorrect_guesses:
            return

        # Apply the guess action
        if guess in self.word_to_guess:
            print(f"Good guess! {guess} is in the word.")
            self.guesses.append(guess)
        else:
            print(f"Hmmm, {guess} is not in the word.")
            self.incorrect_guesses.append(guess)

        # Check if the game is over
        if len(game.incorrect_guesses) >= 8:
            self.phase = GamePhase.FINISHED
            print("Game over, better luck next time.")
        elif all(letter in self.guesses for letter in self.word_to_guess):
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
                                guesses =self.guesses
                                )

class RandomPlayer(Player):

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
        word_to_guess = input("Enter a word to guess (letters only): ").lower()
        if word_to_guess.isalpha():
            break
        print("Invalid input. Please enter a valid word.")

    # Set initial game state
    game_state = HangmanGameState(
        word_to_guess=word_to_guess,
        phase=GamePhase.RUNNING,
        guesses=[]
    )
    game.set_state(game_state)

    # create instance of Random Player class
    player = RandomPlayer()

    # Main game loop
    while game.phase == GamePhase.RUNNING:
        player_view = game.get_player_view(idx_player=0)
        print(f"Player's view: {player_view.word_to_guess}") # Showing the masked word
        actions = game.get_list_action() # Get possible actions
        action = player.select_action(game.get_state(), actions) # Player selects an action
        if action:
            print(f"Player guesses: {action.letter}")
            game.apply_action(action)

    game.print_state()