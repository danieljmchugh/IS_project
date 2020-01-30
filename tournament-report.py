#!usr/bin/env python

from argparse import ArgumentParser
from api import State, util, engine
import random, time

def run_tournament(options):

    botnames = options.players.split(",")

    bots = []
    for botname in botnames:
        bots.append(util.load_player(botname))

    n = len(bots)
    wins = [0] * len(bots)
    ranks = [0] * len(bots)

    matches = [(p1, p2) for p1 in range(n) for p2 in range(n) if p1 < p2]

    totalgames = (n*n - n)/2 * options.repeats
    playedgames = 0

    print('Playing {} games:'.format(int(totalgames)))
    for a, b in matches:
        for r in range(options.repeats):

            p = [a, b] if random.choice([True, False]) else [b, a]  # randomly chooses who starts
            # p = [a, b]  # first starts
            # p = [b, a]  # second starts

            # add starting_state argument here
            starting_state = None  # None, one_marriage, two marriage, all_jacks, all_aces, same_suit, all_ace_jack
            state = State.generate(phase=int(options.phase), starting_state=starting_state)

            winner, score = engine.play(bots[p[0]], bots[p[1]], state, options.max_time*1000, verbose=False, fast=options.fast)

            if winner is not None:
                winner = p[winner - 1]
                wins[winner] += score
                ranks[winner] += 1

            playedgames += 1
            #print('Played {} out of {:.0f} games ({:.0f}%): {} \r'.format(playedgames, totalgames, playedgames/float(totalgames) * 100, wins))

    for i in range(len(bots)):
        ranks[i] = wins[i]/(totalgames)
        print('    bot {}: {} points, {} rank'.format(bots[i], wins[i], ranks[i]))




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
