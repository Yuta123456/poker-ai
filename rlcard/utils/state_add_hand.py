# number of suit, include diamond, spade, heart, club
NUMBER_OF_SUIT = 4
NUMBER_OF_NUM = 13
def state_add_hand(state):
    '''
    input state:
    input state is array that has 72 integer. (1 or 0)
    output new_state : 
    output state is array that has 7? integer
    The number of hand is 10
    '''
    hand_kind = [0 for i in range(10)]
    card_array = []
    
    for i in range(NUMBER_OF_SUIT):
        card_array.append(state[i * 13:(i+1) * 13])
    print(card_array)
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
            break
    print(hand_kind)
    return state + hand_kind
def is_royal_flush(card_array):

    for suit in range(NUMBER_OF_SUIT):
        if sum(card_array[suit][9:NUMBER_OF_NUM]) + card_array[suit][0] == 5:
            return True
    return False

def is_straight_flush(card_array):
    
    for suit in range(NUMBER_OF_SUIT): 
        for num in range(NUMBER_OF_NUM - 3):
            if num + 5 > NUMBER_OF_NUM - 1 :
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
    # これ結構めんどくさい
    return False

def is_flash(card_array):

    for suit in range(NUMBER_OF_SUIT):
        if sum(card_array[suit]) >= 5:
            return True
    return False

def is_straight(card_array):
    # これもめんどくさい
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

print("flash : ", state_add_hand([
    1,0,0,1,0,1,0,1,0,0,1,0,0,
    0,0,0,0,0,0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,0,0,0,0,0
    ]
))
print("royal_straight_flash : ",  state_add_hand([
    1,0,0,0,0,0,0,0,0,1,1,1,1,
    0,0,0,0,0,0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,0,0,0,0,0
    ]
))
print("two pair : ",  state_add_hand([
    0,0,0,0,0,1,0,0,0,0,0,0,1,
    0,0,0,0,0,1,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,0,0,0,0,1
    ]
))
print("one pair : ",  state_add_hand([
    0,0,0,0,0,0,0,0,0,0,0,0,1,
    0,0,0,0,0,0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,0,0,0,0,1
    ]
))
print("three card : ",  state_add_hand([
    0,0,0,0,0,0,0,0,0,0,0,0,1,
    0,0,0,0,0,0,0,0,0,0,0,0,1,
    0,0,0,0,0,0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,0,0,0,0,1
    ]
))