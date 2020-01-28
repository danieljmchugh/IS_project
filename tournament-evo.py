#!usr/bin/env python
"""
A command line program for multiple games between several bots.

For all the options run
python play.py -h
"""

from argparse import ArgumentParser
from api import State, util, engine
import random, time
import numpy as np
import math
from keras.models import load_model

POPULATION = 15
ELITE = 5
N = int((POPULATION - ELITE) / ELITE)
def run_tournament(options):
    rdeep = util.load_player("rdeep")
    bots = []
    for x in range(0, POPULATION):
        bots.append([util.load_player("evo"), 0])
        #print(bots[-1].model.get_weights()[0][8][:10])
    for i in range(1, ELITE + 1):
        exec ("boi" + str(i) + " = load_model(\"elite/boi" + str(i) + ".krs\").get_weights()")
        exec ("bots[i - 1][0].set_weights(boi" + str(i) + ")")
        pass
    for i in range(0, POPULATION - ELITE):
        a = eval ("np.array(boi" + str(math.ceil((i + 1) / N)) + ")")
        for a1 in range(len(a)):
            for a2 in range(len(a[a1])):
                a[a1][a2] += (random.random() - 0.5) / 10**6
        bots[i + ELITE][0].set_weights(a)
        pass
    for x in range(0, ELITE):
        print(bots[x][0].model.get_weights()[0][8][:5])
        pass

    print("*******************************")
    for x in range(ELITE, POPULATION):
        print(bots[x][0].model.get_weights()[0][8][:5])
        pass

    n = len(bots)
    wins = [0] * len(bots)

    totalgames = POPULATION * options.repeats
    playedgames = 0

    print('Playing {} games:'.format(int(totalgames)))
    for x in range(0, len(bots)):

        for j in range(0, options.repeats):
            # Generate a state with a random seed
            state = State.generate(id=56, phase=int(options.phase))

            winner, score = engine.play(bots[x][0], rdeep, state, options.max_time*1000, verbose=False, fast=options.fast)


            if winner is not None:
                if state.revoked():
                    bots[x][1] -= 100
                print(bots[x][0].turns)
                bots[x][0].turns = 0
                if winner == 1:
                    bots[x][1] += score * 100

            for i in range(0, len(bots)):
                wins[i] = bots[i][1]
            playedgames += 1
            print('Played {} out of {:.0f} games ({:.0f}%): {} \r'.format(playedgames, totalgames, playedgames/float(totalgames) * 100, wins))

    bots = sorted(bots, key= lambda x: x[1])
    print("Average: " + str(sum(wins) / len(wins)))
    print('Results:')
    j = 1
    for i in range(len(bots)):
        print('    bot {}: {} points'.format(bots[i][0], bots[i][1]))
        if i >= len(bots) - ELITE:
            bots[i][0].model.save("elite/boi" + str(j) + ".krs")
            j += 1

if __name__ == "__main__":

    ## Parse the command line options
    parser = ArgumentParser()

    parser.add_argument("-s", "--starting-phase",
                        dest="phase",
                        help="Which phase the game should start at.",
                        default=1)

    parser.add_argument("-p", "--players",
                        dest="players",
                        help="Comma-separated list of player names (enclose with quotes).",
                        default="rand,bully,rdeep")

    parser.add_argument("-r", "--repeats",
                        dest="repeats",
                        help="How many matches to play for each pair of bots",
                        type=int, default=10)

    parser.add_argument("-t", "--max-time",
                        dest="max_time",
                        help="maximum amount of time allowed per turn in seconds (default: 5)",
                        type=int, default=5)

    parser.add_argument("-f", "--fast",
                        dest="fast",
                        action="store_true",
                        help="This option forgoes the engine's check of whether a bot is able to make a decision in the allotted time, so only use this option if you are sure that your bot is stable.")

    options = parser.parse_args()

    for x in range(0, 1):
        run_tournament(options)