from typing import List, Optional
import random
from enum import Enum


class GuessLetterAction:
    def __init__(self, letter: str) -> None:
        self.letter = letter


class GamePhase(str, Enum):
    SETUP = 'setup'  # before the game has started
    RUNNING = 'running'  # while the game is running
    FINISHED = 'finished'  # when the game is finished


class HangmanGameState:
    def __init__(self, word_to_guess: str, phase: GamePhase, guesses: List[str], incorrect_guesses: List[str]) -> None:
        self.word_to_guess = word_to_guess.lower()
        self.phase = phase
        self.guesses = guesses
        self.incorrect_guesses = incorrect_guesses


class Hangman:
    def __init__(self) -> None:
        self.state: Optional[HangmanGameState] = None

    def get_state(self) -> HangmanGameState:
        return self.state

    def set_state(self, state: HangmanGameState) -> None:
        self.state = state

    def print_state(self) -> None:
        if self.state is None:
            print("No game state set.")
            return

        # Display the current guessed word
        masked_word = " ".join(
            [letter if letter in self.state.guesses else "_" for letter in self.state.word_to_guess]
        )
        print(f"Word: {masked_word}")
        print(f"Guesses: {', '.join(self.state.guesses)}")
        print(f"Incorrect guesses: {', '.join(self.state.incorrect_guesses)}")

    def get_list_action(self) -> List[GuessLetterAction]:
        if self.state is None or self.state.phase != GamePhase.RUNNING:
            return []
        # Generate possible actions based on unused letters
        unused_letters = [chr(i) for i in range(97, 123) if chr(i) not in self.state.guesses]
        return [GuessLetterAction(letter) for letter in unused_letters]

    def apply_action(self, action: GuessLetterAction) -> None:
        if self.state is None or self.state.phase != GamePhase.RUNNING:
            return

        letter = action.letter.lower()

        # Ignore already guessed letters
        if letter in self.state.guesses or letter in self.state.incorrect_guesses:
            return

        if letter in self.state.word_to_guess:
            self.state.guesses.append(letter)
        else:
            self.state.incorrect_guesses.append(letter)

        # Check if the game is finished
        if all(letter in self.state.guesses for letter in self.state.word_to_guess):
            print("Congratulations! You've guessed the word!")
            self.state.phase = GamePhase.FINISHED
        elif len(self.state.incorrect_guesses) >= 6:  # Assuming 6 incorrect attempts allowed
            print("Game over! You've run out of attempts.")
            print(f"The word was: {self.state.word_to_guess}")
            self.state.phase = GamePhase.FINISHED

    def get_player_view(self, idx_player: int) -> HangmanGameState:
        # Player view is the same as the full state in this implementation
        return self.state


class RandomPlayer:
    def select_action(self, state: HangmanGameState, actions: List[GuessLetterAction]) -> Optional[GuessLetterAction]:
        if len(actions) > 0:
            return random.choice(actions)
        return None


if __name__ == "__main__":
    game = Hangman()
    word_to_guess = "DevOps"
    game_state = HangmanGameState(word_to_guess=word_to_guess, phase=GamePhase.RUNNING, guesses=[],
                                  incorrect_guesses=[])
    game.set_state(game_state)

    # Simulate game loop
    player = RandomPlayer()
    while game.get_state().phase == GamePhase.RUNNING:
        game.print_state()
        actions = game.get_list_action()
        action = player.select_action(game.get_state(), actions)
        if action:
            print(f"Player guesses: {action.letter}")
            game.apply_action(action)

    game.print_state()