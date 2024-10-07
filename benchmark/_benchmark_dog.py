# runcmd: cd .. & venv\Scripts\python benchmark/_benchmark_dog.py python dog.Dog

import sys
import benchmark_dog


if __name__ == '__main__':

    if len(sys.argv) < 3:
        print("Error: Wrong number of arguments")
        print("Use: python benchmark_dog.py python [dog.py]")
        print("  or python benchmark_dog.py localhost [port]")
        print("  or python benchmark_dog.py remote [host:port]")
        sys.exit()

    benchmark = benchmark_dog.DogBenchmark(argv=sys.argv)

    if True:  # disable features
        benchmark.game_server.game.game_state._list_disabled_features = [
             'test_initial_game_state_values',
            # 'test_later_game_state_values',
            # 'test_get_list_action_without_start_cards',
            # 'test_get_list_action_with_one_start_card',
            # 'test_get_list_action_with_three_start_cards',
            # 'test_move_out_of_kennel_1',
            # 'test_move_out_of_kennel_2',
            # 'test_move_out_of_kennel_3',
            # 'test_move_with_ACE_from_start',
            # 'test_move_with_TWO_from_start',
            # 'test_move_with_THREE_from_start',
            # 'test_move_with_FOUR_from_start',
            # 'test_move_with_FIVE_from_start',
            # 'test_move_with_SIX_from_start',
            # 'test_move_with_SEVEN_from_start',
            # 'test_move_with_EIGHT_from_start',
            # 'test_move_with_NINE_from_start',
            # 'test_move_with_TEN_from_start',
            # 'test_move_with_QUEEN_from_start',
            # 'test_move_with_KING_from_start',
            # 'test_swap_with_JAKE_1',
            # 'test_swap_with_JAKE_2',
            # 'test_swap_with_JAKE_3',
            # 'test_swap_with_JAKE_4',
            # 'test_chose_card_with_JOKER_1',
            # 'test_chose_card_with_JOKER_2',
            # 'test_chose_card_with_JOKER_3',
            # 'test_move_with_SEVEN_multiple_steps_1',
            # 'test_move_with_SEVEN_multiple_steps_2',
            #'test_move_with_SEVEN_multiple_steps_3',
            #'test_move_with_SEVEN_multiple_steps_4',
            #'test_overtake_save_marble_1',
            #'test_overtake_save_marble_2',
            #'test_send_home_with_simple_cards',
            #'test_send_home_with_SEVEN_from_start',
            #'test_overtake_with_simple_cards',
            #'test_move_to_empty_finish_with_simple_cards',
            #'test_move_to_empty_finish_with_negative_steps',
            'test_not_overtaking_in_finish',
            #'test_card_exchange_at_beginning_of_round_1',
            #'test_card_exchange_at_beginning_of_round_2',
            #'test_number_of_cards_in_round_1',
            #'test_number_of_cards_in_round_2',
            #'test_number_of_cards_in_round_5',
            #'test_number_of_cards_in_round_6',
            #'test_stock_out_of_cards',
            #'test_folding_cards',
            #'test_support_partner_at_the_end',
            #'test_finish_game',
            'test_unique_actions',
            'test_chose_card_with_JOKER_4',
            'test_move_with_SEVEN_multiple_steps_7'
        ]

    if False:  # test all
        benchmark.run_tests()
    else:  # test single
        benchmark.test_initial_game_state_values()

    # TODO: Add winners
    # TODO: Roll back 7 when not all steps possible, but let player play other card
    # TODO: Test card SEVEN when part of 7 steps can be used to put all own marbles in finish, but remaining can be moved with oponent.

