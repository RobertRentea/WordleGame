import argparse
import sys

from wordle import WordleGame
from solvers import NaiveSolver

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--word', type=str,
                        help='Specify the word used in the game.')
    parser.add_argument('-n', '--naive', action='store_true',
                        help='Use the naive solver the guess the word.')
    args = parser.parse_args(sys.argv[1:])
    word = args.word if args.word else None

    if not any([args.naive]):
        game = WordleGame(word)
        try:
            while not game.finished():
                guess = input('\rEnter your word: ')
                game.guess(guess)
        except KeyboardInterrupt:
            print()
    else:
        if args.naive:
            solver = NaiveSolver(word)
            solver.play()