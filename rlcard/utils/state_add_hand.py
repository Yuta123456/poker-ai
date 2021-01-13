# number of suit, include diamond, spade, heart, club
import numpy as np

NUMBER_OF_SUIT = 4
NUMBER_OF_NUM = 13

def state_add_hand(state):
    N = len(state)
    res = np.empty((N, 82))
    for i in range(N):
        res[i][:] = array_add_hand(state[i])
    return res
def array_add_hand(state):
    '''
    input state:
    input state is array that has 72 integer. (1 or 0)
    output new_state : 
    output state is array that has 82 integer
    The number of hand is 10
    '''
    hand_kind = np.zeros(10)
    card_array = np.empty((NUMBER_OF_SUIT,NUMBER_OF_NUM))
    for i in range(NUMBER_OF_SUIT):
        card_array[i][:] = state[i * 13:(i+1) * 13]
    check_hand_functions = [is_royal_flush,
                            is_straight_flush,
                            is_for_of_a_kind,
                            is_full_house,
                            is_flash,
                            is_straight,
                            is_three_of_a_kind,
                            is_two_pair,
                            is_one_pair,
                            ]
    
    for i in range(len(check_hand_functions)):
        if check_hand_functions[i](card_array):
            hand_kind[i] = 1
            return np.append(state, hand_kind)
    hand_kind[-1] = 1
    return np.append(state, hand_kind)


def is_royal_flush(card_array):
    for suit in range(NUMBER_OF_SUIT):
        if sum(card_array[suit][9:NUMBER_OF_NUM]) + card_array[suit][0] == 5:
            return True
    return False


def is_straight_flush(card_array):

    for suit in range(NUMBER_OF_SUIT):
        for num in range(NUMBER_OF_NUM - 3):
            if num + 5 > NUMBER_OF_NUM - 1:
                if sum(card_array[suit][num:num+4]) + card_array[suit][0] == 5:
                    return True
            if sum(card_array[suit][num:num + 5]) == 5:
                return True
    return False


def is_for_of_a_kind(card_array):

    for num in range(NUMBER_OF_NUM):
        if sum([card_array[i][num] for i in range(NUMBER_OF_SUIT)]) == 4:
            return True
    return False


def is_full_house(card_array):
    for i in range(NUMBER_OF_NUM):
        for j in range(NUMBER_OF_NUM):
            if i == j:
                continue
            if sum([card_array[suit][i] for suit in range(NUMBER_OF_SUIT)]) >= 2 and \
                sum([card_array[suit][j] for suit in range(NUMBER_OF_SUIT)]) >= 3:
                return True
    return False


def is_flash(card_array):

    for suit in range(NUMBER_OF_SUIT):
        if sum(card_array[suit]) >= 5:
            return True
    return False


def is_straight(card_array):
    # num move 0~9
    for num in range(NUMBER_OF_NUM - 3):
        # 13 -> A
        number_of_chain = 0
        if num + 4 > NUMBER_OF_NUM - 1:
            for j in range(num, num+4):
                number_of_chain += 1 if sum([card_array[i][j]
                                             for i in range(NUMBER_OF_SUIT)]) > 0 else 0
            number_of_chain += 1 if sum([card_array[i][0]
                                         for i in range(NUMBER_OF_SUIT)]) > 0 else 0
        else:
            for j in range(num, num+5):
                number_of_chain += 1 if sum([card_array[i][j]
                                             for i in range(NUMBER_OF_SUIT)]) > 0 else 0
        if number_of_chain >= 5:
            return True
    return False


def is_three_of_a_kind(card_array):
    for num in range(NUMBER_OF_NUM):
        if sum([card_array[i][num] for i in range(NUMBER_OF_SUIT)]) == 3:
            return True
    return False


def is_two_pair(card_array):

    pair_count = 0

    for num in range(NUMBER_OF_NUM):
        if sum([card_array[i][num] for i in range(NUMBER_OF_SUIT)]) == 2:
            pair_count += 1
    return True if pair_count >= 2 else False


def is_one_pair(card_array):

    pair_count = 0
    for num in range(NUMBER_OF_NUM):
        if sum([card_array[i][num] for i in range(NUMBER_OF_SUIT)]) == 2:
            pair_count += 1
    return True if pair_count == 1 else False

# test_array = np.empty(72)
# test_array[:] = [
#     1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0,
#     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#     1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
#     1, 1, 1, 1, 1, 1, 1
# ]
# state_add_hand(test_array)
# print("-------------------------------------------------")
# state_add_hand([
#     1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1,
#     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
# ]
# )
# print("-------------------------------------------------")
# state_add_hand([
#     0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1,
#     0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
#     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1
# ]
# )
# print("-------------------------------------------------")
# state_add_hand([
#     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
#     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1
# ]
# )
# print("-------------------------------------------------")
# state_add_hand([
#     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
#     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
#     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1
# ]
# )
# print("-------------------------------------------------")
# state_add_hand([
#     0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1,
#     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0,
#     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0,
#     1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
# ]
# )
# print("-------------------------------------------------")
# state_add_hand([
#     0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1,
#     0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1,
#     0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1,
#     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
# ]
# )