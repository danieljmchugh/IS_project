from api import State, util
from bots.danbot import danbot

#from bots.rdeep import rdeep

# Define the bot:
class Bot:

    def __init__(self):
        pass

    def get_move(self, state):

        moves = state.moves()

        return moves[0]


# Parameters of our experiment
STEPS = 1
REPEATS = 1
inc = 1.0/STEPS

# Make empty matrices to count how many times each player won for a given
# combination of parameters
won_by_1 = 0
won_by_2 = 0


# We will move through the parameters from 0 to 1 in STEPS steps, and play REPEATS games for each
# combination. If at combination (i, j) player 1 winds a game, we increment won_by_1[i][j]

for i in range(STEPS):
    for j in range(STEPS):
        for r in range(REPEATS):

            # Make the players
            player1 = danbot.Bot()
            player2 = danbot.Bot()

            # change player turn in state.generate
            # change cards config in deck.generate
            state = State.generate()

            # play the game
            while not state.finished():
                player = player1 if state.whose_turn() == 1 else player2
                state = state.next(player.get_move(state))

            #TODO Maybe add points for state.winner()
            if state.finished():
                winner, points = state.winner()
                if winner == 1:
                    won_by_1 += points
                else:
                    won_by_2 += points


print("player1 won by: " + str(won_by_1))
print("player2 won by: " + str(won_by_2))
