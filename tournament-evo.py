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
import joblib
from keras.models import load_model

def run_tournament(options):

    bots = []
    boi1 = load_model("elite/boi1.krs").get_weights()
    boi2 = load_model("elite/boi2.krs").get_weights()
    boi3 = load_model("elite/boi3.krs").get_weights()
    for x in range(0, 12):
        bots.append(util.load_player("evo"))
        print(bots[-1].model.get_weights()[0][8][:10])

    bots[0].set_weights(boi1)
    bots[1].set_weights(boi2)
    bots[2].set_weights(boi3)

    for x in range(3, 6):
        a = np.array(boi1)
        b = a * (random.random() - 0.5) / 6
        bots[x].set_weights(a + b)
    for x in range(6, 9):
        a = np.array(boi2)
        b = a * (random.random() - 0.5) / 4
        bots[x].set_weights(a + b)
    for x in range(9, 12):
        a = np.array(boi3)
        b = a * (random.random() - 0.5) / 2
        bots[x].set_weights(a + b)
    print("*******************************")
    for x in range(0, 12):
        print(bots[x].model.get_weights()[0][8][:10])

    n = len(bots)
    wins = [0] * len(bots)
    matches = [(p1, p2) for p1 in range(n) for p2 in range(n) if p1 < p2]

    totalgames = (n*n - n)/2 * options.repeats
    playedgames = 0

    print('Playing {} games:'.format(int(totalgames)))
    for a, b in matches:
        for r in range(options.repeats):

            if random.choice([True, False]):
                p = [a, b]
            else:
                p = [b, a]

            # Generate a state with a random seed
            state = State.generate(phase=int(options.phase))

            winner, score = engine.play(bots[p[0]], bots[p[1]], state, options.max_time*1000, verbose=False, fast=options.fast)

            if winner is not None:
                winner = p[winner - 1]
                wins[winner] += score

            playedgames += 1
            print('Played {} out of {:.0f} games ({:.0f}%): {} \r'.format(playedgames, totalgames, playedgames/float(totalgames) * 100, wins))

    cutoff = sorted(wins)[-3]
    print(cutoff)
    print('Results:')
    j = 1
    for i in range(len(bots)):
        print('    bot {}: {} points'.format(bots[i], wins[i]))
        if wins[i] >= cutoff:
            bots[i].model.save("elite/boi" + str(j) + ".krs")
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

    run_tournament(options)