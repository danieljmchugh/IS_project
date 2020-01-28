"""
RandomBot -- A simple strategy: enumerates all legal moves, and picks one
uniformly at random.
"""
# Import the API objects
from api import State
import random
from keras import initializers
from keras.models import load_model, Sequential
from keras.layers import Dense
import numpy as np
import time

class Bot:

    def __init__(self):
        self.model = load_model("start_bot.krs")
        self.turns = 0

    depth = 0
    own_id = 0
    __max_depth = 20
    def set_weights(self, weights):
        self.model.set_weights(weights)

    def get_move(self, state):
        # type: (State) -> tuple[int, int]
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
        self.own_id = state.whose_turn()
        # All legal moves

        moves = state.moves()
        if state.get_phase() == 2:
            val, move = self.value(state)
            return move
        return (self.eval(state), None)

    def get_turns(self):
        return self.turns

    def eval(self, state):
        input = np.zeros((20, 1))
        for move in state.moves():
            input[move[0]] = 1
        input = input.reshape((1, 20, ))
        start = time.time()
        answer = self.model.predict(input)
        #print(answer.shape)
        #print(time.time() - start, " sec")
        return int(np.where(answer[0] == max(answer[0]))[0][0])

    def value(self, state, depth=0):
        # type: (State, int) -> tuple[float, tuple[int, int]]
        """
        Return the value of this state and the associated move
        :param state:
        :param depth:
        :return: A tuple containing the value of this state, and the best move for the player currently to move
        """

        if state.finished():
            winner, points = state.winner()
            return (points, None) if winner == 1 else (-points, None)

        if depth == self.__max_depth:
            return heuristic(state)

        moves = state.moves()

        best_value = float('-inf') if maximizing(state) else float('inf')
        best_move = None

        for move in moves:

            next_state = state.next(move)

            # IMPLEMENT: Add a recursive function call so that 'value' will contain the
            # minimax value of 'next_state'
            value, m = self.value(next_state, depth + 1)

            if maximizing(state):
                if value > best_value:
                    best_value = value
                    best_move = move
            else:
                if value < best_value:
                    best_value = value
                    best_move = move

        return best_value, best_move

def maximizing(state):
    # type: (State) -> bool
    """
    Whether we're the maximizing player (1) or the minimizing player (2).

    :param state:
    :return:
    """
    return state.whose_turn() == 1
