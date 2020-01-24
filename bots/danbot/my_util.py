from api import State, Deck, util
"""
         	    Aces  10s 	Kings 	Queens 	Jacks
        Clubs 	  0    1 	  2 	  3 	  4
        Diamonds  5    6 	  7 	  8 	  9
        Hearts 	 10   11 	 12 	 13 	 14
        Spades 	 15   16 	 17 	 18 	 19

        move[]
        - (int, None): first element indicates the index of the card that is placed down.
        - (int, int) : first element as above, second element completes a marriage
        - (None, int): First element being None indicates a trump jack exchange,
            second element is the index of that trump jack
"""


marriage_combos = [(2, 3), (7, 8), (12, 13), (17, 18)]

# returns index of trump jack if present, else None
def check_trump_jack(state, player_hand):
    for card in player_hand:
        if util.get_rank(card) == "J" and util.get_suit(card) == state.get_trump_suit():
            return player_hand.index(card)
    return None


def check_marriage(player_hand):
    possible_marriages = []
    """
    for combo in enumerate(marriage_combos):
        if combo[0] and combo[1] in given_hand:
            possible_marriage.append(combo)
    """
    if 2 in player_hand and 3 in player_hand:
        possible_marriages.append((2, 3))   # (King, Queen) format
        # possible_marriages.append((3, 2))
    if 7 in player_hand and 8 in player_hand:
        possible_marriages.append((7, 8))
        # possible_marriages.append((8, 7))
    if 12 in player_hand and 13 in player_hand:
        possible_marriages.append((12, 13))
        # possible_marriages.append((13, 12))
    if 17 in player_hand and 18 in player_hand:
        possible_marriages.append((17, 18))
        # possible_marriages.append((18, 17))

    return possible_marriages


def get_trump_card_indexes(state, player_hand):
    trump_card_indexes = []

    for card in player_hand:
        if util.get_suit(card) == state.get_trump_suit():
            trump_card_indexes.append(player_hand.index(card))

    return trump_card_indexes


def get_non_trump_card_indexes(state, player_hand):
    non_trump_card_indexes = []

    for card in player_hand:
        if util.get_suit(card) != state.get_trump_suit():
            non_trump_card_indexes.append(player_hand.index(card))

    return non_trump_card_indexes
