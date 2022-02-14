import math

from wordle import *
from collections import Counter

class NaiveSolver:
    def __init__(self, word: None) -> None:
        self.game = WordleGame(word)
        with open(POSSIBLE_WORDS_FILE) as possible_words_file:
            self.possible_words = possible_words_file.read().split('\n')
        with open(ALLOWED_WORDS_FILE) as allowed_words_file:
            self.allowed_words = allowed_words_file.read().split('\n')
        self.work_list = self.possible_words

    def compute_patterns(self, word):
        patterns = []
        for allowed_word in self.work_list:
            pattern = Pattern(allowed_word, word)
            patterns.append(pattern)
        return patterns

    def expected_information(self, guess):
        patterns = self.compute_patterns(guess)
        occurences = Counter(patterns)
        exp_info = 0
        for _, count in occurences.items():
            probability = count / len(self.work_list)
            exp_info += probability * math.log2(1 / probability)
        return exp_info

    def play(self):
        while not self.game.finished():
            best_word, max_info = max([(word, self.expected_information(word))
                                        for word in self.work_list],
                                        key=lambda x: x[1]) 
            print(f'Best guess is: {best_word} ({max_info} expected information)')
            guess = input('\rEnter your word: ')
            pattern = self.game.guess(guess)
            if pattern:
                self.work_list = [word for word in self.work_list
                                        if Pattern(word, guess) == pattern] 

