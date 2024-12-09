from typing import List, Optional, ClassVar
from enum import Enum
import random
from itertools import permutations
from pydantic import BaseModel
from server.py.game import Game, Player

class Card(BaseModel):
    suit: str  # card suit (color)
    rank: str  # card rank

    # Add __eq__ and __hash__ methods to the Card class so that
    # it can be included in hashable objects like sets or dictionaries.

    def __eq__(self, other):
        if not isinstance(other, Card):
            return False
        return self.suit == other.suit and self.rank == other.rank

    def __hash__(self):
        return hash((self.suit, self.rank))

    def get_steps(self):
        # Map rank to allowed steps
        step_mapping = {'A': [1, 11], '2': [2], '3': [3], '4': [4, -4], '5': [5],
                        '6': [6], '8': [8], '9': [9], '10': [10], 'Q': [12], 'K': [13]}
        steps = step_mapping.get(self.rank, [])
        return steps

class Marble(BaseModel):
    pos: int       # position on board (0 to 95)
    is_save: bool = False # true if marble was moved out of kennel and was not yet moved
    passed_start: int = 0 # number of times the marble passes the start position

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

    # Add __eq__ and __hash__ methods to the Action class so that
    # it can be included in hashable objects like sets or dictionaries.

    def __eq__(self, other):
        if not isinstance(other, Action):
            return False
        return (self.card == other.card and
                self.pos_from == other.pos_from and
                self.pos_to == other.pos_to)

    def __hash__(self):
        return hash((self.card, self.pos_from, self.pos_to))

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

    def get_player_view(self, idx_player: int) -> GameState:
        """ Get the masked state for the active player (e.g. the oppontent's cards are face down)"""
        pass

    def get_list_action(self) -> List[Action]:
        """ Get a list of possible actions for the active player.
            Return lists of actions available depending on how many
            start cards the player has and whether marbles ar in kennel
            or not.Tests 3, 4 and 5"""
        actions = []
        player = self.state.list_player[self.state.idx_player_active]
        start_position = Dog.BOARD["starts"][self.state.idx_player_active]
        kennel_position = Dog.BOARD["kennels"][self.state.idx_player_active]
        state = self.get_state()

        if not self.state.bool_card_exchanged:
            seen_cards = set()
            for card in player.list_card:
                if card not in seen_cards:  # Avoid adding duplicate cards
                    actions.append(Action(card=card, pos_from=None, pos_to=None))
                    seen_cards.add(card)
            return actions

        # Game start: Checking if any marbles are in the kennel
        if any(marble.pos in kennel_position for marble in player.list_marble):

            # Check for self-block on start position
            if any(marble.pos == start_position and marble.is_save == True for marble in player.list_marble):
                return actions

            # Create a list of start cards (e.g., Ace, King, Joker)
            start_cards = [card for card in player.list_card if card.rank in ["A", "K", "JKR"]]

            # Check if player has start action or not and get corresponding action
            for card in start_cards:
                pos_from = kennel_position[0]
                pos_to = start_position
                actions.append(Action(card=card, pos_from=pos_from, pos_to=pos_to))

        # Add Jack card actions to the action list
        jack_actions = self.get_jack_actions(player)
        actions.extend(jack_actions)
        
        # Actions for marbles outside of kennel
        for marble in player.list_marble:
            if marble.pos not in Dog.BOARD["kennels"][self.state.idx_player_active]:  # Marble is outside the kennel
                for card in player.list_card:
                    if card.rank in Dog.RANK_ACTIONS:  # Ensure the card rank is valid
                        # Loop through all possible moves for the card
                        for move in Dog.RANK_ACTIONS[card.rank].get("moves", []):
                            new_position = (marble.pos + move) % len(Dog.BOARD["common_track"])
                            actions.append(Action(card=card, pos_from=marble.pos, pos_to=new_position)) # Add valid action

        def filter_invalid_actions_save_marble(actions, state):
            """Checks if actions are not overtaking a blocking marble."""
            filtered_actions = []

            for action in actions:
                action_valid = True

                for player in state.list_player:
                    for marble in player.list_marble:
                        if marble.is_save:
                            if action.pos_from < marble.pos <= action.pos_to:
                                action_valid = False
                                break
                    if not action_valid:
                        break
                if action_valid:
                    filtered_actions.append(action)

            return filtered_actions

        actions = filter_invalid_actions_save_marble(actions, state)

        validated_actions = set() # Using set for uniqueness

        # Validation of actions
        for action in actions:
            if action not in validated_actions: # checking for duplicated actions
                if self.validate_no_overtaking_in_finish(action): # checking overtaking in finish
                    validated_actions.add(action)
                # Further logic for additional game phases or card actions can go here...

        return list(validated_actions) # Ensuring to return a list

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
                random_player = RandomPlayer()  # Instantiate the RandomPlayer object
                action = random_player.select_action(self.state, actions)
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
            if action.card.rank == "J":
                self.exchange_marbles(current_player, action)
            elif action.pos_from is not None and action.pos_to is not None: # Check if action is moving a marble
                # Find the marble
                marble = next((m for m in current_player.list_marble if m.pos == action.pos_from), None)
                if marble:
                    movement_success = self.move_marble(marble, action.card, action.pos_to, current_player)
                    if movement_success:
                        print(f"Marble moved from {action.pos_from} to {action.pos_to}.")
                    else:
                        print(f"Invalid move from {action.pos_from} to {action.pos_to}.")

        # Check if reshuffle is required before processing any actions. Test 50
        if not self.state.list_card_draw:
            self.reshuffle_cards()

# ---- MARBLES METHODS----

    def move_marble(self, marble: Marble, card: Card, pos_to: int, player: PlayerState) -> bool:
        """
        Move marble to a new position and handle collisions.
        If a marble is at the destination, it is sent back to its kennel.
        Returns: True if the move is successful, False otherwise.
        """
        board = Dog.BOARD
        current_pos = marble.pos

        # Moving out of kennel
        kennel_positions = board["kennels"][self.state.idx_player_active]
        start_position = board["starts"][self.state.idx_player_active]
        if marble.pos in kennel_positions and pos_to == start_position:
            if not self.handle_collision(pos_to):
                return False
            marble.is_save = True
            print(f"Marble moved to start position {pos_to} and is now safe.")
            marble.pos = pos_to
            return True

        # Reset is_save after move away from start position
        if marble.pos == start_position and pos_to != start_position:
            marble.is_save = False
            print(f"Marble moved out of start position and is no longer safe.")

        # Determine valid positions based on steps.
        valid_steps = card.get_steps()  # Get the steps allowed for the card
        valid_positions = [(current_pos + step) % len(board["common_track"]) for step in valid_steps]

        if card.rank == "7":
            return True

        # Check if the move is valid
        if pos_to not in valid_positions:
            print(f"Invalid move: position {pos_to} is not reachable using card {card.rank}.")
            return False

        # Handle collision
        collision_resolved = self.handle_collision(pos_to)
        if not collision_resolved:
            return False

        # Handle finishing line rules
        finish_positions = board["finishes"][self.state.list_player.index(player)]
        if marble.pos in finish_positions and pos_to in finish_positions:
            # Ensure no overtaking inside the finish line
            if pos_to > max(m.pos for m in player.list_marble if m.pos in finish_positions):
                print(f"Invalid move: cannot overtake within the finish line to position {pos_to}.")
                return False

        # Move the marble
        marble.pos = pos_to
        return True
    
    def exchange_marbles(self, current_player: PlayerState, action: Action) -> None:
        """
        Handle the marble exchange between the current player and an other player.
        This is called when a Jack card is played.
        """
        # Ensure the action has valid positions for both marbles
        if action.pos_from is None or action.pos_to is None:
            print("Error: Invalid positions for marble exchange.")
            return

        # Find the player's marble to exchange
        own_marble = next((m for m in current_player.list_marble if m.pos == action.pos_from), None)
        if not own_marble:
            print(f"Error: Own marble at position {action.pos_from} not found for exchange.")
            return

        # Find the opponent's marble to exchange with
        other_player = next((p for p in self.state.list_player if p != current_player), None)
        other_marble = next((m for m in other_player.list_marble if m.pos == action.pos_to), None)
        if not other_marble:
            print(f"Error: Opponent's marble at position {action.pos_to} not found for exchange.")
            return

        # Swap positions of the two marbles
        own_marble.pos, other_marble.pos = other_marble.pos, own_marble.pos

        # Notify about the successful exchange
        print(f"Marble exchange successful: {current_player.name}'s marble moved to position {own_marble.pos} "
            f"and {other_player.name}'s marble moved to position {other_marble.pos}.")

    def handle_collision(self, pos_to: int) -> bool:
        """
        Handle collisions when a marble moves to a new position.
        If a marble is at the destination, it is sent back to its kennel.
        Returns True if no collision or collision is handled, False if collision is not resolved.
        """
        board = Dog.BOARD

        # Check for collisions with other marbles
        for other_player in self.state.list_player:
            for other_marble in other_player.list_marble:
                if other_marble.pos == pos_to:
                    if other_marble.is_save:
                        print(f"Impossible, marble at position {other_marble.pos} is safe.")
                        return False
                    else:
                        # Send the marble back to the kennel
                        empty_kennel_positions = [
                            pos for pos in board["kennels"][self.state.list_player.index(other_player)]
                            if all(m.pos != pos for m in other_player.list_marble)
                        ]
                        other_marble.pos = empty_kennel_positions[0]  # First available kennel slot
                        print(f"Collision! {other_player.name}'s marble sent back to kennel at position {other_marble.pos}.")
                        return True
        return True

    def validate_no_overtaking_in_finish(self, action):
        """Make sure the marbles cannot be overtaken in the finish"""
        # The function returns true or false
        player = self.state.list_player[self.state.idx_player_active]
        finish_position = Dog.BOARD["finishes"][self.state.idx_player_active]

        # Check if the action involves the finish area
        if action.pos_from in finish_position or action.pos_to in finish_position:
            # Ensure no marble in the finish area is overtaken or replaced
            for marble in player.list_marble:
                if marble.pos in finish_position and marble.pos >= action.pos_to:
                    # A marble would be overtaken or replaced
                    return False

        return True # Action is valid, on overtaking in the finish
    
# ---- CARDS METHODS ----

    def get_seven_step_combinations(self, total_steps = 7):
        """Generate all possible step combinations for card '7' to split between marbles."""
        step_splits = []
        for i in range(1, total_steps + 1): # Generate combinations up to total_steps
            splits = [steps for steps in permutations(range(1, total_steps + 1), i) if sum(steps) == total_steps]
            step_splits.extend(splits)
        return step_splits
    
    def get_jack_actions(self, player: PlayerState) -> List[Action]:
        """Generate a list of all possible actions when the player plays a Jack card."""
        jack_actions = []
        
        # Ensure the player has a Jack card in hand
        jack_cards = [card for card in player.list_card if card.rank == "J"]
        if not jack_cards:
            return jack_actions  # No Jack cards to play

        # Iterate over the active player's marbles
        for own_marble in player.list_marble:
            if own_marble.is_save:
                continue  # Skip marbles that are safe

            # Iterate over all opponent marbles
            for other_player in self.state.list_player:
                if other_player == player:
                    continue  # Skip the active player
                
                for other_marble in other_player.list_marble:
                    if other_marble.is_save:
                        continue  # Skip safe marbles
                    
                    # Create an exchange action
                    for jack_card in jack_cards:
                        action = Action(
                            card=jack_card,
                            pos_from=own_marble.pos,
                            pos_to=other_marble.pos,
                            card_swap=None
                        )
                        jack_actions.append(action)

        return jack_actions
    
# ---- GAMEPLAY METHODS----

    def play_game(self):
        """Run the game automatically from start to finish."""
        print("Game started!\nFirst round!")

        while self.state != GamePhase.FINISHED:
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
        self.state.bool_card_exchanged = False # set exchange to false for all players

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

    def reshuffle_cards(self) -> None:
        """Reshuffle cards from the discard pile to the draw pile if needed. Test 50"""
        if self.state.list_card_discard:
            # Transfer all cards from discard to draw pile
            self.state.list_card_draw.extend(self.state.list_card_discard)
            # Clear the discard pile
            self.state.list_card_discard.clear()
            # Shuffle the draw pile
            random.shuffle(self.state.list_card_draw)

class RandomPlayer(Player):

    def select_action(self, state: GameState, actions: List[Action]) -> Optional[Action]:
        """ Given masked game state and possible actions, select the next action """
        if len(actions) > 0:
            return random.choice(actions)
        return None


if __name__ == '__main__':

    game = Dog() # Initialize the game
    game.play_game()