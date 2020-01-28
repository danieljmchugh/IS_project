"""
RandomBot -- A simple strategy: enumerates all legal moves, and picks one
uniformly at random.
"""

# Import the API objects
from api import State, Deck, util
import random

# TODO: implement finishing move check
#

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
            
    Leading:
        if trump exchange:
            trump exchange
        if marriage
            if royal marriage
                royal marriage
            marriage
        if highest non-trump move
            highest non-trump move
            
        random
    Follow:
        x = other card
        if x is high (10 or A) and non-tump
            if tump
                lowest trump
        if same-suit as x
            if higher same-suit
                higher same suit
        if non-trump 
            lowest non-trump move
        random
"""



class Bot:

    def __init__(self):
        pass

    def get_move(self, state):
        # type: (State) -> Tuple[None, Any]
        """
        Function that gets called every turn. This is where to implement the strategies.
        Be sure to make a legal move. Illegal moves, like giving an index of a card you
        don't own or proposing an illegal mariage, will lose you the game.
       	TODO: add some more explanation
        :param State state: An object representing the gamestate. This includes a link to
            the states of all the cards, the trick and the points.
        :return: A tuple of integers or a tuple of an integer and None,
            indicating a move; the first indicates the card played in the trick, the second a
            potential spouse.
        """
        print()
        player_id = state.whose_turn()
        print("points: " + str(state.get_points(player_id)))
        player_hand = state.hand()
        print(player_hand)
        print_hand(player_hand)
        moves = state.moves()

        # leading trick
        if state.get_opponents_played_card() is None:
            print("leading trick")

            # check trump swap:
            #  (None, int): First element being None indicates a trump jack exchange,
            #             second element is the index of that trump jack
            for move in moves:
                if move[0] is None and isinstance(move[1], int):
                    print("move: Trump swap")
                    return move

            # check marriage:
            #   (int, int) : first element as above, second element completes a marriage
            possible_marriages = get_possible_marriages(moves)
            # check royal marriage
            for move in possible_marriages:
                if Deck.get_suit(move[0]) == state.get_trump_suit():
                    print("move: Royal marriage")
                    return move
            # else return random marriage if exists
            if possible_marriages:
                print("move: Normal marriage")
                return random.choice(possible_marriages)

            # play lowest, non-trump jack
            #   (int, None): first element indicates the index of the card that is placed down.
            non_trump_moves = get_non_trump_moves(state, moves)
            if non_trump_moves:
                print("move: Highest non-trump")
                return get_highest_value_move(non_trump_moves)
                #print("move: Highest non-trump")
                #return get_highest_value_move(non_trump_moves)

            # play random
            print("move: Random move")
            return random.choice(moves)

        # following trick
        else:
            print("following trick")
            played_card = state.get_opponents_played_card()
            print("other card: ", end="")
            print_card(played_card)

            # if high rank and non-trump
            if Deck.get_rank(played_card) == "10" or "A" and Deck.get_suit(played_card) != state.get_trump_suit():
                trump_moves = get_trump_moves(state, moves)
                if trump_moves:
                    print("reply: Smallest trump card")
                    return get_lowest_value_move(trump_moves)

            # play higher same suit
            same_suit_moves = get_moves_of_suit(moves, Deck.get_suit(played_card))
            if same_suit_moves:
                higher_value_move = get_higher_value_move(same_suit_moves, played_card)
                if higher_value_move:
                    print("reply: Higher same suit ", end="")
                    print_card(higher_value_move[0])
                    return higher_value_move
            # minimize loss
            non_trump_moves = get_non_trump_moves(state, moves)
            if non_trump_moves:
                print("reply: Smallest non-trump")
                return get_lowest_value_move(non_trump_moves)

            print("reply: Random move")
            return random.choice(moves)


# Functions which returns a move

def get_lowest_value_move(moves):
    smallest = moves[0]
    for move in moves:
        if Deck.get_rank(move[0]) < Deck.get_rank(smallest[0]):
            smallest = move
    return smallest


def get_highest_value_move(moves):
    highest = moves[0]
    for move in moves:
        if Deck.get_rank(move[0]) > Deck.get_rank(highest[0]):
            highest = move
    return highest


# returns the lowest value move WHICH is higher than rank given
def get_higher_value_move(moves, card):
    higher_value_move = []
    for move in moves:
        if (move[0] % 5) < (card % 5):
            higher_value_move.append(move)

    if higher_value_move:
        return get_lowest_value_move(higher_value_move)
    else:
        return None


# Functions which return a list of moves

def get_moves_of_suit(moves, suit):
    suit_moves = []
    for move in moves:
        if Deck.get_suit(move[0]) == suit and move[1] is None:
            suit_moves.append(move)
    return suit_moves


def get_possible_marriages(moves):
    possible_marriages = []
    for move in moves:
        if move[0] and move[1]:
            possible_marriages.append(move)
    return possible_marriages


def get_non_trump_moves(state, moves):
    non_trump_moves = []
    for move in moves:
        if move[0] is not None and Deck.get_suit(move[0]) != state.get_trump_suit():
            non_trump_moves.append(move)
    return non_trump_moves


def get_trump_moves(state, moves):
    trump_moves = []
    for move in moves:
        if move[0] is not None and Deck.get_suit(move[0]) == state.get_trump_suit():
            trump_moves.append(move)
    return trump_moves

# utility function

def print_hand(hand):
    for card in hand:
        print(str(Deck.get_rank(card) + Deck.get_suit(card)), end=' ')
    print()


def print_card(card):
    rank = Deck.get_rank(card)
    suit = Deck.get_suit(card)

    print(str(rank + suit))