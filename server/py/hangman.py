from pydantic import BaseModel
from mimetypes import guess_type
from typing import List, Optional
import random
from enum import Enum
from server.py.game import Game, Player


class GuessLetterAction(BaseModel):
    letter: str


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
        """ Get the complete, unmasked game state """ # this method should return the current HangmanGameState
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
        """ Print the current game state """ # this method should output the masked word, showing correctly guessed letters and hiding others.
        masked_word = ''.join(
            letter if letter in self.guesses else '_'
            for letter in self.word_to_guess
        )
        print(f"Word: {masked_word}")
        print(f"Incorrect guesses: {', '.join(self.incorrect_guesses)}")
        print(f"Remaining lives: {8 - len(self.incorrect_guesses)}")

    def get_list_action(self) -> List[GuessLetterAction]:
        """ Get a list of possible actions for the active player """
        if self.state is None or self.state.phase != GamePhase.RUNNING:
            return []                        # there are no actions if GamePhase is SETUP or FINISHED
        
        all_letters = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
        probability = [8.2,1.5,2.8,4.3,12.7,2.2,2.0,6.1,7.0,0.15,0.77,4.0,2.4,6.7,7.5,1.9,0.095,6.5,6.3,9.1,2.8,0.98,2.4,0.15,2.0,0.74]

        unused_letters = [i for i in all_letters if i not in self.state.guesses]
        unused_probabilities = [probability[all_letters.index(i)] for i in unused_letters]

        weighted_choices = random.choices(unused_letters, weights=unused_probabilities, k=len(unused_letters))
        return [GuessLetterAction(letter) for letter in weighted_choices]                      
                
    def apply_action(self, action: GuessLetterAction) -> None:
        """ Apply the given action to the game """
        if self.phase is None or self.phase != GamePhase.RUNNING:
            return

        guess = action.letter.lower()

        # Ignore already guessed letters
        if guess in self.guesses or guess in self.incorrect_guesses:
            return

<<<<<<< HEAD
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
        pass

    def get_player_view(self, idx_player: int) -> HangmanGameState:
        """ Get the masked state for the active player (e.g. the opponent's cards are face down)"""
        masked_word = ""
        for letter in self.state.word_to_guess:
            if letter.lower() in self.state.guesses:
                masked_word += letter
            else:
                masked_word += "_"
        return HangmanGameState(word_to_guess = masked_word,
                                guesses =self.state.guesses,
                                phase = self.state.phase)



class RandomPlayer(Player):

    def select_action(self, state: HangmanGameState, actions: List[GuessLetterAction]) -> Optional[GuessLetterAction]:
        """ Given masked game state and possible actions, select the next action """
        if len(actions) > 0:
            return random.choice(actions)
        return None


if __name__ == "__main__":

    # Setting up a game
    game = Hangman()
    word_to_guess = input("Word to guess is: ").lower() # Making sure the input word has only small letters
    game_state = HangmanGameState(word_to_guess=word_to_guess, phase=GamePhase.RUNNING, guesses=[], incorrect_guesses=[]) # KK: Why do we initialise the same with a word to guess?
    game.set_state(game_state)

    # Running a game
    player = RandomPlayer() # create instance of Random Player class
    while game.phase == GamePhase.RUNNING:
        game.print_state() # Printing state of the game
        actions = game.get_list_action() # Generate possible actions based on unused letters
        action = player.select_action(game.get_state(), actions)
        if action:
            print(f"Player guesses: {action.letter}")
            game.apply_action(action)

    game.print_state()
