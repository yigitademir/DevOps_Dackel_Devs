# runcmd: cd ../.. & venv\Scripts\python server/py/dog_template.py
from server.py.game import Game, Player
from typing import List, Optional, ClassVar
from pydantic import BaseModel
from enum import Enum
import random


class Card(BaseModel):
    suit: str  # card suit (color)
    rank: str  # card rank


class Marble(BaseModel):
    pos: int       # position on board (0 to 95)
    is_save: bool  # true if marble was moved out of kennel and was not yet moved


class PlayerState(BaseModel):
    name: str                  # name of player
    list_card: List[Card]      # list of cards
    list_marble: List[Marble]  # list of marbles
    team_id: int               # team_id


class Action(BaseModel):
    card: Card                 # card to play
    pos_from: Optional[int]    # position to move the marble from
    pos_to: Optional[int]      # position to move the marble to
    card_swap: Optional[Card] = None  # optional card to swap ()


class GamePhase(str, Enum):
    SETUP = 'setup'            # before the game has started
    RUNNING = 'running'        # while the game is running
    FINISHED = 'finished'      # when the game is finished


class GameState(BaseModel):

    LIST_SUIT: ClassVar[List[str]] = ['♠', '♥', '♦', '♣']  # 4 suits (colors)
    LIST_RANK: ClassVar[List[str]] = [
        '2', '3', '4', '5', '6', '7', '8', '9', '10',      # 13 ranks + Joker
        'J', 'Q', 'K', 'A', 'JKR'
    ]
    LIST_CARD: ClassVar[List[Card]] = [
        # 2: Move 2 spots forward
        Card(suit='♠', rank='2'), Card(suit='♥', rank='2'), Card(suit='♦', rank='2'), Card(suit='♣', rank='2'),
        # 3: Move 3 spots forward
        Card(suit='♠', rank='3'), Card(suit='♥', rank='3'), Card(suit='♦', rank='3'), Card(suit='♣', rank='3'),
        # 4: Move 4 spots forward or back
        Card(suit='♠', rank='4'), Card(suit='♥', rank='4'), Card(suit='♦', rank='4'), Card(suit='♣', rank='4'),
        # 5: Move 5 spots forward
        Card(suit='♠', rank='5'), Card(suit='♥', rank='5'), Card(suit='♦', rank='5'), Card(suit='♣', rank='5'),
        # 6: Move 6 spots forward
        Card(suit='♠', rank='6'), Card(suit='♥', rank='6'), Card(suit='♦', rank='6'), Card(suit='♣', rank='6'),
        # 7: Move 7 single steps forward
        Card(suit='♠', rank='7'), Card(suit='♥', rank='7'), Card(suit='♦', rank='7'), Card(suit='♣', rank='7'),
        # 8: Move 8 spots forward
        Card(suit='♠', rank='8'), Card(suit='♥', rank='8'), Card(suit='♦', rank='8'), Card(suit='♣', rank='8'),
        # 9: Move 9 spots forward
        Card(suit='♠', rank='9'), Card(suit='♥', rank='9'), Card(suit='♦', rank='9'), Card(suit='♣', rank='9'),
        # 10: Move 10 spots forward
        Card(suit='♠', rank='10'), Card(suit='♥', rank='10'), Card(suit='♦', rank='10'), Card(suit='♣', rank='10'),
        # Jake: A marble must be exchanged
        Card(suit='♠', rank='J'), Card(suit='♥', rank='J'), Card(suit='♦', rank='J'), Card(suit='♣', rank='J'),
        # Queen: Move 12 spots forward
        Card(suit='♠', rank='Q'), Card(suit='♥', rank='Q'), Card(suit='♦', rank='Q'), Card(suit='♣', rank='Q'),
        # King: Start or move 13 spots forward
        Card(suit='♠', rank='K'), Card(suit='♥', rank='K'), Card(suit='♦', rank='K'), Card(suit='♣', rank='K'),
        # Ass: Start or move 1 or 11 spots forward
        Card(suit='♠', rank='A'), Card(suit='♥', rank='A'), Card(suit='♦', rank='A'), Card(suit='♣', rank='A'),
        # Joker: Use as any other card you want
        Card(suit='', rank='JKR'), Card(suit='', rank='JKR'), Card(suit='', rank='JKR')
    ] * 2

    cnt_player: int = 4                # number of players (must be 4)
    phase: GamePhase                   # current phase of the game
    cnt_round: int                     # current round
    bool_card_exchanged: bool          # true if cards was exchanged in round
    idx_player_started: int            # index of player that started the round
    idx_player_active: int             # index of active player in round
    list_player: List[PlayerState]     # list of players
    list_card_draw: List[Card]         # list of cards to draw
    list_card_discard: List[Card]      # list of cards discarded
    card_active: Optional[Card]        # active card (for 7 and JKR with sequence of actions)


class Dog(Game):
    BOARD = {
        "common_track": list(range(64)),  # Positions 0–63
        "kennels": {
            0: [64, 65, 66, 67], # blue
            1: [72, 73, 74, 75], # green
            2: [80, 81, 82, 83], # red
            3: [88, 89, 90, 91], # yellow
        },
        "finishes": {
            0: [68, 69, 70, 71], # blue
            1: [76, 77, 78, 79], # green
            2: [84, 85, 86, 87], # red
            3: [92, 93, 94, 95], # yellow
        },
        "starts": {
            0: 0, # blue starts at position 0
            1: 16, # green starts at position 16
            2: 32, # red starts at position 32
            3: 48, # yellow starts at position 48
        }
    }

    RANK_ACTIONS = {
    "2": {"start": False, "moves": [2]},
    "3": {"start": False, "moves": [3]},
    "4": {"start": False, "moves": [4, -4]},
    "5": {"start": False, "moves": [5]},
    "6": {"start": False, "moves": [6]},
    "7": {"start": False, "split": True, "moves": [7]},  # Special rule: Split
    "8": {"start": False, "moves": [8]},
    "9": {"start": False, "moves": [9]},
    "10": {"start": False, "moves": [10]},
    "J": {"start": False, "exchange": True},  # Special rule: Exchange
    "Q": {"start": False, "moves": [12]},
    "K": {"start": True, "moves": [13]},
    "A": {"start": True, "moves": [1, 11]},  # Start or move 1 or 11 spots forward
    "JKR": {"wildcard": True},  # Special rule: Can mimic any card
    }

    def __init__(self) -> None:
        self.state = GameState(
            phase = GamePhase.RUNNING, # Transition directly to RUNNING phase
            cnt_round = 1,             # First round
            bool_card_exchanged = False,
            idx_player_started = 0,    # Default starting player index - will assign random value below
            idx_player_active = 0,     # Same as idx_player_started initially
            list_card_draw = [],       # Will populate below
            list_card_discard = [],    # Discard pile is initially empty
            card_active = None,        # No active card at the start
            list_player = [],          # Will populate players below
        )
        # Create the players
        for i in range(4):  # 4 players
            team_id = i % 2 # Players 0 and 2 are team 0, 1 and 3 are team 1
            kennel_positions = Dog.BOARD["kennels"][i]
            player = PlayerState(
                name=f"Player {i + 1}",
                list_card=[],  # Will deal cards next
                list_marble=[Marble(pos=pos, is_save=False) for pos in kennel_positions], # 4 marbles for each player
                team_id=team_id
            )
            self.state.list_player.append(player)

        # Shuffle the deck to prepare for initial draw
        self.state.list_card_draw = random.sample(self.state.LIST_CARD, len(self.state.LIST_CARD))

        # Deal 6 cards to each player
        for player in self.state.list_player:
            player.list_card = [
                self.state.list_card_draw.pop() for _ in range(6)
            ]

        # Randomize the starting player
        self.state.idx_player_started = random.randint(0, 3)
        self.state.idx_player_active = self.state.idx_player_started
        self.cnt_none = 0

    def shuffle_deck(self):
        """Shuffle the card deck."""
        random.shuffle(self.state.LIST_CARD)
        self.state.list_card_draw = self.state.LIST_CARD.copy() # Set draw pile

    def reshuffle_cards(self) -> None:
        """Reshuffle cards from the discard pile to the draw pile if needed. Test 50"""
        if self.state.list_card_discard:
            # Transfer all cards from discard to draw pile
            self.state.list_card_draw.extend(self.state.list_card_discard)
            # Clear the discard pile
            self.state.list_card_discard.clear()
            # Shuffle the draw pile
            random.shuffle(self.state.list_card_draw)

    def set_state(self, state: GameState) -> None:
        self.state = state

    def get_state(self) -> GameState:
        return self.state

    def print_state(self) -> None:
        print(f"cnt_player: int = {self.state.cnt_player}")
        print(f"phase: {self.state.phase}")  # current phase of the game
        print(f"cnt_round: {self.state.cnt_round}")
        print(f"bool_card_exchanged: {self.state.bool_card_exchanged}")
        print(f"idx_player_started: {self.state.idx_player_started}")
        print(f"idx_player_active: {self.state.idx_player_active}")
        print(f"list_player: {self.state.list_player}")
        print(f"list_card_draw: {len(self.state.list_card_draw)}")
        print(f"list_card_discard: {len(self.state.list_card_discard)}")
        print(f"card_active: {self.state.card_active if self.state.card_active else None}")

    def get_list_action(self) -> List[Action]:
        """ Get a list of possible actions for the active player.
            Return lists of actions available depending on how many
            start cards the player has and whether marbles ar in kennel
            or not.Tests 3, 4 and 5"""
        actions = []
        player = self.state.list_player[self.state.idx_player_active]
        start_position = Dog.BOARD["starts"][self.state.idx_player_active]

        # Check if start position occupied by same player's marble
        if any(marble.pos == start_position for marble in player.list_marble):
            return actions

        # Case 1: All marbles are in the kennel, no start cards
        if all(marble.pos in Dog.BOARD["kennels"][self.state.idx_player_active] for marble in player.list_marble):
            # Filter for start cards (e.g., Ace, King, Joker)
            start_cards = [card for card in player.list_card if card.rank in ["A", "K", "JKR"]]

            # No start cards available, return empty actions list
            if not start_cards:
                return actions

            # Case 2 & 3: At least one start card
            # Add actions for each start card to move a marble out of the kennel
            for card in start_cards:
                # Determine the starting position for the active player
                pos_from = Dog.BOARD["kennels"][self.state.idx_player_active][0]  # First kennel position
                pos_to = Dog.BOARD["common_track"][0]  # Start of the track

                # Add the action for this start card
                actions.append(Action(card=card, pos_from=pos_from, pos_to=pos_to))

        # Further logic for additional game phases or card actions can go here...
        return actions

    def apply_action(self, action: Action) -> None:
        """
        Apply the given action or handle the current player's turn if action is None.
        If no valid actions are available, the player's cards are discarded.
        """
        current_player = self.state.list_player[self.state.idx_player_active]

        if action is None:
            # Determine available actions
            actions = self.get_list_action()

            if actions:
                # Select and apply an action (AI or user input)
                action = RandomPlayer.select_action(current_player, actions)
                self.apply_action(action)
                print(f"{current_player.name} played {action.card.rank}{action.card.suit}.")
            else:
                # No valid actions, discard all cards
                self.state.list_card_discard.extend(current_player.list_card)
                discarded_cards = current_player.list_card.copy()
                current_player.list_card.clear()
                print(f"{current_player.name} has no valid actions and discards all cards.")

            # Move to the next player
            self.state.idx_player_active = (self.state.idx_player_active + 1) % self.state.cnt_player

            # Count how many times players have nothing to play
            self.cnt_none += 1
            if self.cnt_none % self.state.cnt_player == 0: # if cnt_none can be divided by 4 then we start new round
                self.end_start_round()

        else:
            # Handle specific actions provided as input
            if action.pos_from is not None and action.pos_to is not None: # Check if action is moving a marble
                # Find the marble
                marble = next((m for m in current_player.list_marble if m.pos == action.pos_from), None)
                if marble:
                    # Update marble position
                    marble.pos = action.pos_to
                    # Moving from the kennel to the start position
                    start_position = Dog.BOARD["starts"][self.state.idx_player_active]
                    if action.pos_from in Dog.BOARD["kennels"][self.state.idx_player_active] and action.pos_to == start_position:
                        marble.is_save = True

        # Check if reshuffle is required before processing any actions. Test 50
        if not self.state.list_card_draw:
            self.reshuffle_cards()

    def get_player_view(self, idx_player: int) -> GameState:
        """ Get the masked state for the active player (e.g. the oppontent's cards are face down)"""
        pass

    def play_game(self):
        """Run the game automatically from start to finish."""
        print("Game started!\nFirst round!")

        while not self.state == GamePhase.FINISHED:
            self.apply_action(None)   # Play a single round
            self.check_game_end()   # Check if the game has ended

        print("Game Over!")
        # self.display_winner()   # No need for this function now

    def end_start_round(self):
        """End the current round and prepare for the next."""
        self.state.cnt_round += 1
        self.state.idx_player_active = (self.state.idx_player_started + self.state.cnt_round - 1) % self.state.cnt_player
        # self.state.idx_player_active = self.state.idx_player_started
        self.deal_cards_to_players()

    def check_game_end(self):
        """Check if the game-ending condition is met."""
        # Group players by team
        team_finish_status = {0: True, 1: True}  # Assume both teams are finished initially

        for player in self.state.list_player:
            finish_positions = Dog.BOARD["finishes"][self.state.list_player.index(player)]
            team_id = player.team_id
            # If any marble is not in a finish position, the team is not finished
            if not all(marble.pos in finish_positions for marble in player.list_marble):
                team_finish_status[team_id] = False

        # If any team is fully finished, the game ends
        if any(team_finish_status.values()):
            self.state.phase = GamePhase.FINISHED

    def deal_cards_to_players(self):
        """Deal new cards to players at the start of a new round."""
        cards_to_deal = [5, 4, 3, 2, 6][(self.state.cnt_round - 2) % 5]  # Calculate number of cards for distribution
        for player in self.state.list_player:
            while len(player.list_card) < cards_to_deal and self.state.list_card_draw:
                player.list_card.append(self.state.list_card_draw.pop())

        print(f"Starting Round {self.state.cnt_round}")

class RandomPlayer(Player):

    def select_action(self, state: GameState, actions: List[Action]) -> Optional[Action]:
        """ Given masked game state and possible actions, select the next action """
        if len(actions) > 0:
            return random.choice(actions)
        return None


if __name__ == '__main__':

    game = Dog() # Initialize the game
    game.play_game()