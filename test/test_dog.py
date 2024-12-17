import pytest
from server.py.game import Game, Player
from server.py.dog import Dog, GameState, GamePhase, Action, PlayerState, Marble, Card, RandomPlayer


# Test class for Hangman game
class TestDogGame:
    CNT_PLAYERS = 4
    CNT_STEPS = 64
    CNT_BALLS = 4

    def test_initialization(self):
        game = Dog()
        assert game.state.cnt_round == 1
        assert game.state.phase == GamePhase.RUNNING
        assert game.state.bool_card_exchanged == False
        assert game.state.idx_player_active == game.state.idx_player_started  # Same as idx_player_started initially
        assert len(game.state.list_card_draw) == 86  # Will populate below
        assert len(game.state.list_card_discard) == 0  # Discard pile is initially empty
        assert len(game.state.list_player) == 4  # Will populate players below

    def test_get_list_action_1(self):
        game = Dog()
        list_card = [Card(suit='♦', rank='A'), Card(suit='♥', rank='K'), Card(suit='', rank='JKR')]

        for card in list_card:

            idx_player_active = 0
            game.state.cnt_round = 0
            game.state.idx_player_started = idx_player_active
            game.state.idx_player_active = idx_player_active
            game.state.bool_card_exchanged = True
            player = game.state.list_player[idx_player_active]
            player.list_card = [Card(suit='♣', rank='10'), Card(suit='♥', rank='Q'), Card(suit='♠', rank='7'),
                                Card(suit='♣', rank='J'), card]
            game.set_state(game.state)

            list_action_found = game.get_list_action()
            action = Action(card=card, pos_from=64, pos_to=0)

            assert action in list_action_found

    def test_get_list_action_2(self):
        pass

    def test_apply_action(self):
        pass

    # No idea how this test work
    def test_move_marble(self):
        game = Dog()

        list_test = [
            {'card': Card(suit='♣', rank='2'), 'list_steps': [2]},
            {'card': Card(suit='♦', rank='2'), 'list_steps': [2]},
            {'card': Card(suit='♥', rank='2'), 'list_steps': [2]},
            {'card': Card(suit='♠', rank='2'), 'list_steps': [2]},
        ]

        for card_data in list_test:
            idx_player_active = 0
            game.state.idx_player_started = idx_player_active
            game.state.idx_player_active = idx_player_active
            game.state.bool_card_exchanged = True

            # Set up the player and initial state
            player = game.state.list_player[idx_player_active]
            player.list_card = [card_data['card']]
            player.list_marble[0].pos = 2
            player.list_marble[0].is_save = True
            game.set_state(game.state)

            # Store initial state as string for debugging
            str_states = str(game.state)

            # Create and apply the action
            action = Action(card=card_data['card'], pos_from=2, pos_to=5)
            game.apply_action(action)
            str_states += f'Action: {action}\n'

            # Get updated game state
            state = game.get_state()
            str_states += str(game.state)

            # Check if a marble moved to position 5
            player = game.state.list_player[idx_player_active]
            found = self.get_idx_marble(player=player, pos=5) != -1

            # Assert marble is in the correct position
            assert found == False

    def test_exchange_marbles(self):
        pass

    def test_handle_collision(self):
        pass

    def test_is_overtaking_save_marble(self):
        game = Dog()
        idx_player = 0
        list_test = [{'card': Card(suit='♣', rank='2'), 'list_steps': [2]},
                     {'card': Card(suit='♦', rank='6'), 'list_steps': [6]}]

        for idx_player in range(4):
            pos_finish = self.CNT_STEPS + idx_player * self.CNT_BALLS * 2 + self.CNT_BALLS
            for i in range(3):
                pos_to = pos_finish + i + 1

                for test in list_test:
                    card = test['card']
                    for steps in test['list_steps']:
                        pos_start = idx_player * int(self.CNT_STEPS / self.CNT_PLAYERS)

                        if pos_to - steps < pos_finish:
                            pos_from = (pos_start - steps + (pos_to - pos_finish + 1) + self.CNT_STEPS) % self.CNT_STEPS
                        else:
                            pos_from = pos_to - steps

        for offset in [0, 1]:
            game.state.idx_player_started = idx_player
            game.state.idx_player_active = idx_player
            game.state.bool_card_exchanged = True
            player = game.state.list_player[idx_player]
            player.list_card = [card]
            player.list_marble[0].pos = pos_from
            player.list_marble[0].is_save = False
            player.list_marble[1].pos = pos_to - offset
            player.list_marble[1].is_save = False
            game.set_state(game.state)
            str_state = str(game.state)

            list_action_found = game.get_list_action()
            action = Action(card=card, pos_from=pos_from, pos_to=pos_to - offset)

            assert action not in list_action_found

    def test_get_seven_actions(self):
        pass

    def test_get_joker_actions_later_in_the_game(self):
        game = Dog()
        list_card = [Card(suit='', rank='JKR')]
        LIST_SUIT = ['♠', '♥', '♦', '♣']

        for card in list_card:
            game.idx_player_active = 0
            game.state.cnt_round = 0
            game.state.idx_player_started = game.idx_player_active
            game.state.idx_player_active = game.idx_player_active
            game.state.bool_card_exchanged = True
            for idx_player, player in enumerate(game.state.list_player):
                if idx_player == game.idx_player_active:
                    player.list_card = [card]
                marble = player.list_marble[0]
                marble.pos = idx_player * 16
                marble.is_save = True  # save oponents cant be moved!
                marble = player.list_marble[1]
                marble.pos = idx_player * 16 + 1
                marble.is_save = False
            game.set_state(game.state)

            list_action_found = game.get_list_action()
            list_action_expected = []
            for suit in LIST_SUIT:
                list_action_expected.extend([
                    Action(card=Card(suit='', rank='JKR'), pos_from=None, pos_to=None,
                           card_swap=Card(suit=suit, rank='2')),
                    Action(card=Card(suit='', rank='JKR'), pos_from=None, pos_to=None,
                           card_swap=Card(suit=suit, rank='3')),
                    Action(card=Card(suit='', rank='JKR'), pos_from=None, pos_to=None,
                           card_swap=Card(suit=suit, rank='4')),
                    Action(card=Card(suit='', rank='JKR'), pos_from=None, pos_to=None,
                           card_swap=Card(suit=suit, rank='5')),
                    Action(card=Card(suit='', rank='JKR'), pos_from=None, pos_to=None,
                           card_swap=Card(suit=suit, rank='6')),
                    Action(card=Card(suit='', rank='JKR'), pos_from=None, pos_to=None,
                           card_swap=Card(suit=suit, rank='7')),
                    Action(card=Card(suit='', rank='JKR'), pos_from=None, pos_to=None,
                           card_swap=Card(suit=suit, rank='8')),
                    Action(card=Card(suit='', rank='JKR'), pos_from=None, pos_to=None,
                           card_swap=Card(suit=suit, rank='9')),
                    Action(card=Card(suit='', rank='JKR'), pos_from=None, pos_to=None,
                           card_swap=Card(suit=suit, rank='10')),
                    Action(card=Card(suit='', rank='JKR'), pos_from=None, pos_to=None,
                           card_swap=Card(suit=suit, rank='A')),
                    Action(card=Card(suit='', rank='JKR'), pos_from=None, pos_to=None,
                           card_swap=Card(suit=suit, rank='J')),
                    Action(card=Card(suit='', rank='JKR'), pos_from=None, pos_to=None,
                           card_swap=Card(suit=suit, rank='K')),
                    Action(card=Card(suit='', rank='JKR'), pos_from=None, pos_to=None,
                           card_swap=Card(suit=suit, rank='Q')),
                ])
            assert len(list_action_found) == len(list_action_expected)

    def test_get_jack_actions(self):
        list_card = [Card(suit='♣', rank='J'), Card(suit='♦', rank='J'), Card(suit='♥', rank='J'),
                     Card(suit='♠', rank='J')]

        for card in list_card:
            game = Dog()

            idx_player_active = 0
            game.state.cnt_round = 0
            game.state.idx_player_started = idx_player_active
            game.state.idx_player_active = idx_player_active
            game.state.bool_card_exchanged = True
            for idx_player, player in enumerate(game.state.list_player):
                if idx_player == idx_player_active:
                    player.list_card = [card]
                marble = player.list_marble[0]
                marble.pos = idx_player * 16
                marble.is_save = True  # save opponents cant be moved!
                marble = player.list_marble[1]
                marble.pos = idx_player * 16 + 1
                marble.is_save = False

            game.set_state(game.state)

            list_action_found = game.get_list_action()
            list_action_expected = [
                Action(card=card, pos_from=0, pos_to=17),
                Action(card=card, pos_from=0, pos_to=33),
                Action(card=card, pos_from=0, pos_to=49),
                Action(card=card, pos_from=1, pos_to=17),
                Action(card=card, pos_from=1, pos_to=33),
                Action(card=card, pos_from=1, pos_to=49),
                Action(card=card, pos_from=17, pos_to=0),
                Action(card=card, pos_from=33, pos_to=0),
                Action(card=card, pos_from=49, pos_to=0),
                Action(card=card, pos_from=17, pos_to=1),
                Action(card=card, pos_from=33, pos_to=1),
                Action(card=card, pos_from=49, pos_to=1)
            ]

            assert len(list_action_found) == len(list_action_expected)

    def test_play_game(self):
        pass

    def test_end_start_round(self):
        pass

    def test_check_game_end(self):
        pass

    def test_deal_cards_to_players(self):
        game =  Dog()
        state = game.get_state()

        game.state.list_card_discard.extend(state.list_card_draw)
        game.state.list_card_discard.append(Card(suit='♥', rank='A'))  # additional card was discarded after JKR
        game.state.list_card_draw = []

        game.set_state(state)

        game.apply_action(None)
        game.apply_action(None)
        game.apply_action(None)
        game.apply_action(None)

        state = game.get_state()
        str_state = str(game.state)

        cnt_cards = len(game.state.list_card_draw)
        for player in game.state.list_player:
            cnt_cards += len(player.list_card)

        assert cnt_cards == 110

    def test_is_duplicated_action_1(self):
        game = Dog()
        idx_player_active = 0
        game.state.cnt_round = 0
        game.state.idx_player_started = idx_player_active
        game.state.idx_player_active = idx_player_active
        game.state.bool_card_exchanged = True

        player = game.state.list_player[idx_player_active]
        player.list_card = [Card(suit='♣', rank='5'), Card(suit='♣', rank='5')]
        player.list_marble[0].pos = 0

        game.set_state(game.state)
        str_state = str(game.state)

        list_action_found = game.get_list_action()

        hint = str_state
        hint += f'Error: List of actions contains duplicate actions.'
        assert len(list_action_found) == 1, hint

# ---- Other tests ------
    def test_folding_cards(self):
        game = Dog()

        idx_player_active = 0
        game.state.cnt_round = 0
        game.state.idx_player_started = idx_player_active
        game.state.idx_player_active = idx_player_active
        game.state.bool_card_exchanged = True
        player = game.state.list_player[idx_player_active]
        player.list_card = [Card(suit='♥', rank='2'), Card(suit='♠', rank='10'), Card(suit='♦', rank='4')]
        player = game.state.list_player[idx_player_active + 1]
        player.list_card = [Card(suit='♥', rank='A')]
        game.set_state(game.state)
        # str_states = str(game.state)

        game.apply_action(None)
        # str_states += f'Action: None\n'

        state = game.get_state()
        # str_states += str(state)

        player = game.state.list_player[idx_player_active]

        assert len(player.list_card) == 0

    def test_support_partner_at_the_end(self):

        card = Card(suit='♣', rank='5')
        for idx_player in range(4):

            game = Dog()
            state = game.get_state()

            game.state.idx_player_started = idx_player
            game.state.idx_player_active = idx_player
            game.state.bool_card_exchanged = True

            pos_finish = self.CNT_STEPS + idx_player * self.CNT_BALLS * 2 + self.CNT_BALLS
            player = game.state.list_player[idx_player]
            player.list_card = [card]
            for i in range(4):
                player.list_marble[i].pos = pos_finish + i

            idx_partner = (idx_player + 2) % self.CNT_PLAYERS
            pos_start = idx_partner * int(self.CNT_STEPS / self.CNT_PLAYERS)
            player = game.state.list_player[idx_partner]
            player.list_marble[0].pos = pos_start
            player.list_marble[0].is_save = False

            game.set_state(game.state)
            str_states = str(game.state)

            list_action_found = game.get_list_action()

            assert len(list_action_found) > 0

            pos_to = pos_start + 5
            action = Action(card=card, pos_from=pos_start, pos_to=pos_to)
            game.apply_action(action)
            str_states += f'Action: None\n'

            state = game.get_state()
            str_states += str(state)

            player = game.state.list_player[idx_partner]
            idx_marble = self.get_idx_marble(player=player, pos=pos_to)

            assert idx_marble != -1

    def test_chose_card_with_JOKER_4(self):
        game = Dog()

        card_swap = Card(suit='♥', rank='A')

        state = game.get_state()

        idx_player_active = 0
        game.state.cnt_round = 0
        game.state.idx_player_started = idx_player_active
        game.state.idx_player_active = idx_player_active
        game.state.bool_card_exchanged = True
        player = state.list_player[idx_player_active]
        player.list_card = [Card(suit='', rank='JKR'), Card(suit='', rank='JKR')]
        game.set_state(game.state)

        action = Action(card=Card(suit='', rank='JKR'), pos_from=None, pos_to=None, card_swap=card_swap)
        game.apply_action(action)

        state = game.get_state()

        player = game.state.list_player[idx_player_active]
        cnt_jkr = len([card for card in player.list_card if card == Card(suit='', rank='JKR')])
        assert cnt_jkr == 1

    def test_chose_card_with_JOKER_3(self):

        card_swap = Card(suit='♥', rank='A')

        game = Dog()
        state = game.get_state()

        idx_player_active = 0
        game.state.cnt_round = 0
        game.state.idx_player_started = idx_player_active
        game.state.idx_player_active = idx_player_active
        game.state.bool_card_exchanged = True
        player = state.list_player[idx_player_active]
        player.list_card = [Card(suit='', rank='JKR'), Card(suit='♠', rank='K')]
        game.set_state(game.state)

        action = Action(card=Card(suit='', rank='JKR'), pos_from=None, pos_to=None, card_swap=card_swap)
        game.apply_action(action)

        state = game.get_state()

        assert game.state.card_active == card_swap

        assert game.state.idx_player_active == idx_player_active

        list_action_found = game.get_list_action()
        action = Action(card=Card(suit='♠', rank='K'), pos_from=64, pos_to=0)

        assert action not in list_action_found

    def test_card_exchange_at_beginning_of_round_1(self):

        game = Dog()
        state = game.get_state()

        idx_player_active = 0
        game.state.cnt_round = 0
        game.state.idx_player_started = idx_player_active
        game.state.idx_player_active = idx_player_active
        game.set_state(state)

        list_action_found = game.get_list_action()
        list_action_expected = []

        player = game.state.list_player[idx_player_active]
        for card in player.list_card:
            action = Action(card=card, pos_from=None, pos_to=None)
            if action not in list_action_expected:
                list_action_expected.append(action)

        assert self.get_sorted_list_action(list_action_found) == self.get_sorted_list_action(list_action_expected)

    def test_swap_with_JAKE_3(self):

        list_card = [Card(suit='♣', rank='J'), Card(suit='♦', rank='J'), Card(suit='♥', rank='J'), Card(suit='♠', rank='J')]

        for card in list_card:
            game = Dog()
            state = game.get_state()

            idx_player_active = 0
            game.state.cnt_round = 0
            game.state.idx_player_started = idx_player_active
            game.state.idx_player_active = idx_player_active
            game.state.bool_card_exchanged = True
            for idx_player, player in enumerate(state.list_player):
                if idx_player == idx_player_active:
                    player.list_card = [card]
                marble = player.list_marble[0]
                marble.pos = idx_player * 16
                marble.is_save = True  # save oponents cant be moved!
                marble = player.list_marble[1]
                marble.pos = idx_player * 16 + 1
                marble.is_save = False

            game.set_state(state)

            action = Action(card=card, pos_from=0, pos_to=17)
            game.apply_action(action)

            state = game.get_state()

            player1 = game.state.list_player[idx_player_active]
            player2 = game.state.list_player[idx_player_active + 1]
            is_swapped = self.get_idx_marble(player=player1, pos=17) != -1 and \
                self.get_idx_marble(player=player2, pos=0) != -1

            assert is_swapped

    def test_move_with_SEVEN_multiple_steps_5(self):
        """Test 033: Test move with card SEVEN and can not play all steps [10 point]"""

        list_steps = [1, 2, 3]
        list_card = [Card(suit='♣', rank='7'), Card(suit='♦', rank='7'), Card(suit='♥', rank='7'), Card(suit='♠', rank='7')]

        for card in list_card:

            game = Dog()
            state = game.get_state()

            pos_blocked = 16
            pos_from = pos_blocked - sum(list_steps[:-1]) - 1
            idx_player_active = 0
            game.state.cnt_round = 0
            game.state.idx_player_started = idx_player_active
            game.state.idx_player_active = idx_player_active
            game.state.bool_card_exchanged = True
            player = game.state.list_player[idx_player_active]
            player.list_card = [card]
            marble = player.list_marble[0]
            marble.pos = pos_from
            marble.is_save = False
            player = state.list_player[idx_player_active + 1]
            marble = player.list_marble[0]
            marble.pos = pos_blocked
            marble.is_save = True
            marble = player.list_marble[1]
            marble.pos = pos_blocked - 1
            marble.is_save = False
            game.set_state(state)

            for i, steps in enumerate(list_steps):

                if i < len(list_steps) - 1:  # before last step
                    pos_to = (pos_from + steps + self.CNT_STEPS) % self.CNT_STEPS
                    action = Action(card=card, pos_from=pos_from, pos_to=pos_to)
                    game.apply_action(action)
                else:  # last step
                    list_action_found = game.get_list_action()

                    assert len(list_action_found) == 0

                    game.apply_action(None)

                    state = game.get_state()

                    # assert game state is reset

                    assert game.state.card_active is None

                pos_from = pos_to

    def test_move_with_SEVEN_multiple_steps_3(self):
        """Test 031: Test move with card SEVEN and kick out oponents [1 point]"""

        list_steps = [1, 2, 3, 4, 5, 6, 7]
        list_card = [Card(suit='♣', rank='7'), Card(suit='♦', rank='7'), Card(suit='♥', rank='7'), Card(suit='♠', rank='7')]

        for card in list_card:

            for steps in list_steps:

                game = Dog()
                state = game.get_state()

                pos_from = 0
                pos_oponent = pos_from + steps - 1 if steps > 1 else pos_from + 1
                idx_player_active = 0
                game.state.cnt_round = 0
                game.state.idx_player_started = idx_player_active
                game.state.idx_player_active = idx_player_active
                game.state.bool_card_exchanged = True
                player = game.state.list_player[idx_player_active]
                player.list_card = [card]
                marble = player.list_marble[0]
                marble.pos = pos_from
                marble.is_save = True
                player = state.list_player[idx_player_active + 1]
                player.list_card = [Card(suit='♥', rank='K')]
                marble = player.list_marble[0]
                marble.pos = pos_oponent
                marble.is_save = False
                game.set_state(state)

                pos_to = (pos_from + steps + self.CNT_STEPS) % self.CNT_STEPS
                action = Action(card=card, pos_from=pos_from, pos_to=pos_to)
                game.apply_action(action)

                state = game.get_state()

                player = state.list_player[idx_player_active]
                found = self.get_idx_marble(player=player, pos=pos_to) != -1
                assert found

                pos_from = pos_oponent
                pos_to = 72
                player = state.list_player[idx_player_active + 1]
                found = self.get_idx_marble(player=player, pos=pos_to) != -1
                assert found

# --- Helper functions --------

    def get_idx_marble(self, player: PlayerState, pos: int) -> int:
        for idx_marble, marble in enumerate(player.list_marble):
            if marble.pos == pos:
                return idx_marble
        return -1

    def test_home_with_simple_cards(self):

        list_card = [{'card': Card(suit='♥', rank='K'), 'list_steps': [13]},
        {'card': Card(suit='♠', rank='K'), 'list_steps': [13]}]

        self.send_home_test(pos_from=0, list_test=list_card)

    def send_home_test(self, pos_from: int, list_test: list[dict]) -> None:
        for test in list_test:
            card = test['card']
            for steps in test['list_steps']:
                pos_to = (pos_from + steps + self.CNT_STEPS) % self.CNT_STEPS
                for is_own_marble in [True, False]:
                    self.send_home_marble(card=card, pos_from=pos_from, pos_to=pos_to, is_own_marble=is_own_marble)

    def send_home_marble(self, card: str, pos_from: int, pos_to: int, is_own_marble: bool):
        game = Dog()
        state = game.get_state()

        idx_player_active = 0
        game.state.idx_player_started = idx_player_active
        game.state.idx_player_active = idx_player_active
        game.state.bool_card_exchanged = True
        player = state.list_player[idx_player_active]
        player.list_card = [card]
        player.list_marble[0].pos = pos_from
        player.list_marble[0].is_save = True
        if is_own_marble:
            player.list_marble[1].pos = pos_to
            player.list_marble[1].is_save = False
        else:
            player = state.list_player[idx_player_active + 1]
            player.list_marble[0].pos = pos_to
            player.list_marble[0].is_save = False
        game.set_state(state)

        action = Action(card=card, pos_from=pos_from, pos_to=pos_to)
        game.apply_action(action)

        state = game.get_state()

        if is_own_marble:
            cnt_in_kennel = self.get_cnt_marbles_in_kennel(state=state, idx_player=idx_player_active)
            found = cnt_in_kennel == 3
        else:
            cnt_in_kennel = self.get_cnt_marbles_in_kennel(state=state, idx_player=idx_player_active + 1)
            found = cnt_in_kennel == 4

        assert found

    def get_cnt_marbles_in_kennel(self, state: dict, idx_player: int) -> int:
        cnt_in_kennel = 0
        player = state.list_player[idx_player]
        for marble in player.list_marble:
            if marble.pos >= self.CNT_STEPS + idx_player * self.CNT_BALLS * 2 and \
                    marble.pos < self.CNT_STEPS + idx_player * self.CNT_BALLS * 2 + self.CNT_BALLS:
                cnt_in_kennel += 1
        return cnt_in_kennel

    def get_sorted_list_action(self, list_action):
        return sorted(list_action, key=lambda x: (
            str(x.card),
            -1 if x.pos_from is None else x.pos_from,
            -1 if x.pos_to is None else x.pos_to,
            str(x.card_swap))
        )