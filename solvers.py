import math
import pandas as pd
import itertools

from wordle import *
from collections import Counter
from tqdm import tqdm as ProgressBar
from scipy.stats import entropy

PATTERN_MATRIX_FILE = os.path.join(WORDLE_DATA_DIR, 'patterns.npy')

class Solver:

    def __init__(self, game: WordleGame) -> None:
        self.game = game
        self._words_list = self.get_possible_words()
        self._work_list = self.get_allowed_words()
        self.pattern_grid = None

    def get_possible_words(self):
        with open(POSSIBLE_WORDS_FILE) as possible_words_file:
            return possible_words_file.read().split('\n')

    def get_allowed_words(self):
        with open(ALLOWED_WORDS_FILE) as allowed_words_file:
            return allowed_words_file.read().split('\n')

    def get_words_list(self):
        return self._words_list

    def get_work_list(self):
        return self._work_list

    def remove_words_from_work_list(self, guess, pattern):
        new_list = list(filter(lambda word: Pattern(word, guess).pattern == pattern.pattern,
                               self._work_list))
        self._work_list = new_list

    def generate_pattern_matrix(self, guess_words, base_words):
        pattern_matrix = []
        for guess in ProgressBar(guess_words, desc='Generating pattern matrix'):
            row = []
            for base in base_words:
                p = Pattern(base, guess)
                row.append(hash(p))
            pattern_matrix.append(row)

        return np.array(pattern_matrix, dtype=np.uint8)

    def get_pattern_matrix(self, words1, words2):
        if not self.pattern_grid:
            if not os.path.exists(PATTERN_MATRIX_FILE):
                words = self.get_work_list()
                grid = self.generate_pattern_matrix(words, words)
                np.save(PATTERN_MATRIX_FILE, grid)
            grid = np.load(PATTERN_MATRIX_FILE)
            self.pattern_grid = {
                'grid': grid,
                'words_to_index': dict(zip(
                    self.get_work_list(), itertools.count()
                ))
            }

        indices1 = [self.pattern_grid['words_to_index'][word] for word in words1]
        indices2 = [self.pattern_grid['words_to_index'][word] for word in words2]
        return self.pattern_grid['grid'][np.ix_(indices1, indices2)]

    def get_pattern(self, answer, guess):
        if self.pattern_grid:
            return self.get_pattern_matrix([answer], [guess]) [0, 0]
        return self.generate_pattern_matrix([answer], [guess]) [0, 0]


class NaiveSolver(Solver):

    def __init__(self, game: WordleGame) -> None:
        super().__init__(game)

    def entropy(self, patterns):
        _, counts = np.unique(patterns, return_counts=True)
        probabilities = counts / len(patterns)
        return entropy(probabilities, base=2)

    def best_guesses(self):
        words = self.get_work_list()
        pattern_matrix = self.get_pattern_matrix(words, words)
        entropies = np.apply_along_axis(self.entropy, 1, pattern_matrix)
        n = min(len(words), 10)
        indexes = np.argpartition(entropies, -n)[-n:]
        
        best_words = [words[i] for i in indexes]
        best_entropies = entropies[indexes]
        return sorted(list(zip(best_words, best_entropies)), key=lambda x: x[1], reverse=True)

    def best_guess(self):
        return self.best_guesses()[0]

    def play(self):
        while not self.game.finished():
            best_word, max_info = self.best_guess()
            print(f'Best guess is: {best_word} ({max_info} expected information)')
            guess = input('\rEnter your word: ')
            pattern = self.game.guess(guess)
            if pattern:
                self.remove_words_from_work_list(guess, pattern)
    
    def simulation(self):
        for word in ProgressBar(self.get_possible_words()):
            self.game = WordleGame(word)
            self._work_list = self.get_possible_words()
            while not self.game.finished():
                best_word, _ = self.best_guess()
                pattern = self.game.guess(best_word)
                if pattern:
                    self.remove_words_from_work_list(best_word, pattern)

    def interactive(self):
        while len(self.get_work_list()) > 0:
            best_words = self.best_guesses()
            print(f'Best guesses are: {best_words}')
            guess = input('Enter your guess: ')
            pattern_string = input('Enter given pattern: ')
            pattern = Pattern.from_str(pattern_string)
            if pattern_string == '22222':
                break
            self.remove_words_from_work_list(guess, pattern)


if __name__ == '__main__':
    naive = NaiveSolver(None)
    naive.simulation()
